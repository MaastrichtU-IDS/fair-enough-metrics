from fair_test import FairTest, FairTestEvaluation
import requests
from urllib.parse import urlparse
import json
import os
from duckduckgo_search import ddg
# from googlesearch import search
# import qwant
# from fastapi import APIRouter, Body, Depends
# from fastapi_utils.cbv import cbv


class MetricTest(FairTest):
    metric_version = '0.1.0'
    metric_path = 'f4-searchable'
    applies_to_principle = 'F4'
    title = 'The resource is indexed in a searchable resource'
    description = """Extract the title from RDF metadata, or from the DataCite API (in case it is a DOI), 
then search for the resource URL in popular search engines using the extracted title:
- DuckDuckGo search engine (no limitations, but it misses some scientific data repositories)
- Google custom search API (results are not as good as the regular Google search though, limited to 100 queries per day)
- Bing search engine (qualitative results, but limited to 1000 queries per months, used as last recourse)"""
    topics = []
    author = 'https://orcid.org/0000-0002-1501-1082'
    test_test={
        'https://doi.org/10.1045/november2015-vandesompel': 1,
        'https://doi.org/10.1038/sdata.2016.18': 1,
        'https://purl.uniprot.org/uniprot/P51587': 1,
        'https://doi.org/10.1016/J.JBI.2019.103292': 1,
        'https://github.com/MaastrichtU-IDS/fair-test': 1,
        # 'https://doi.org/10.1594/PANGAEA.908011': 1,
        'Wrong entry': 0,
    }
    

    def evaluate(self, eval: FairTestEvaluation):
        g = eval.retrieve_rdf(eval.subject)

        # print(g.serialize(format='turtle'))

        datacite_dois_api = 'https://api.datacite.org/dois/'
        # datacite_endpoint = 'https://api.datacite.org/repositories'
        # re3data_endpoint = 'https://re3data.org/api/beta/repositories'
        # metadata_catalog = https://rdamsc.bath.ac.uk/api/m
        headers = {"Accept": "application/json"}
        titles = []
        doi = None
        result = urlparse(eval.subject)
        if result.scheme and result.netloc:
            if result.netloc == 'doi.org':
                doi = result.path[1:]
                eval.info('The subject resource URI ' + eval.subject + ' is a DOI')
        else:
            eval.warn('Could not validate the given resource URI ' + eval.subject + ' is a URL')    

        # If DOI, we first check for metadata in the DataCite API
        if doi:
            try:
                # if self.subject.startswith('https://doi.org/') or self.subject.startswith('http://doi.org/'):
                eval.info('Checking DataCite API for metadata about the DOI: ' + doi)
                r = requests.get(datacite_dois_api + doi, timeout=10)
                datacite_json = r.json()
                datacite_data = datacite_json['data']['attributes']
                # print(datacite_json['data']['attributes'].keys())
                # ['id', 'type', 'attributes', 'relationships']
                if datacite_data:
                    # eval.success('Found ' + doi + ' in DataCite')
                    eval.info('Found ' + doi + ' in DataCite')
                    eval.data['datacite'] = {}
                    # print('datacite_data')
                    # print(datacite_data.keys())

                    if 'titles' in datacite_data.keys():
                        titles = [datacite_data['titles'][0]['title']]
                        eval.data['datacite']['title'] = datacite_data['titles'][0]['title']
                        # print(eval.data['datacite']['title'])
                        if not 'title' in eval.data:
                            eval.data['title'] = titles

                    if 'descriptions' in datacite_data.keys():
                        eval.data['datacite']['description'] = datacite_data['descriptions'][0]['description']

                    # eval.info('Checking RE3data APIs from DataCite API for metadata about ' + uri)
                    # p = {'query': 're3data_id:*'}
                    # req = requests.get(datacite_endpoint, params=p, headers=headers)
                    # print(req.json())
            except Exception as e:
                eval.warn('Search in DataCite API failed: ' + e.args[0])        
        else:
            eval.warn('DOI could not be found, skipping search in DataCite API')


        # If no title found through DataCite, try to get it from the subject URL RDF metadata
        if len(titles) < 1:
            if len(g) == 0:
                eval.failure('Could not extract title: no RDF found at the subject URL provided.')
                return eval.response()
            else:
                eval.info(f'RDF metadata containing {len(g)} triples found at the subject URL provided.')
            subject_uri = eval.extract_metadata_subject(g, eval.data['alternative_uris'])
            if subject_uri:
                title_preds = [ 
                    'http://purl.org/dc/elements/1.1/title', 
                    'http://purl.org/dc/terms/title', 
                    'http://www.w3.org/2000/01/rdf-schema#label', 
                    'https://schema.org/name', 'http://ogp.me/ns#title', 
                    'https://schema.org/headline',
                ]
                titles = [str(s) for s in eval.extract_prop(g, title_preds, subject_uri)] 
                eval.data['title'] = titles


        ## Check search engines using the resource title and its alternative URIs
        if len(titles) > 0:
            title = titles[0]
            resource_uris = eval.data['alternative_uris']

            # Search DuckDuckGo
            try:
                eval.info(f'Searching DuckDuckGo for: {title}')
                search_results = ddg(title, region='wt-wt', max_results=80)
                # ddg(keywords, region='wt-wt', safesearch='Moderate', time=None, max_results=50):
                # print(json.dumps(search_results, indent=2))
                uris_found = [s['href'] for s in search_results] 
                
                for uri_found in uris_found:
                    for subject_uri in resource_uris:
                        if uri_found.startswith(subject_uri):
                            eval.success(f'Found the resource URI {uri_found} when searching in DuckDuckGo for ' + title)
                            return eval.response()

                eval.warn(f"Resource not found when searching in DuckDuckGo for {title}")
            except Exception as e:
                eval.warn(f'Error running DuckDuckGo search: {str(e)}')


            # Google free limitations: 100 queries per day, and poor quality results
            google_apikey = os.getenv('APIKEY_GOOGLE_SEARCH')
            # google_cx   = os.getenv('CX_GOOGLE_SEARCH')
            google_cx = 'b6774763e7b060a30'
            google_endpoint = 'https://www.googleapis.com/customsearch/v1'
            # To create new cx: go to https://cse.google.com/all
            # Create a new engine using google.com as search website
            # Once created, edit this engine in Setup > Basics
            # Enable "Search the entire web"
            # Test custom cx search: https://cse.google.com/cse?cx=b6774763e7b060a30
            if google_apikey:
                eval.info(f'Searching Google Custom Search Engine https://cse.google.com/cse?cx={google_cx} for: {title}')
                try:
                    params = {
                        'q': title,
                        'key': google_apikey,
                        'cx': google_cx,
                    }
                    search_res = requests.get(google_endpoint, params=params).json()
                    # print(json.dumps(search_res, indent=2))
                    for item in search_res['items']:
                        for subject_uri in resource_uris:
                            if item['link'].startswith(subject_uri):
                                eval.success(f"Found the resource URI {item['link']} when searching in Google for {title}")
                                return eval.response()
                        # if item['link'] in resource_uris:
                        #     eval.success(f"Found the resource URI {search_res['displayUrl']} when searching in Bing for: {title}")
                        #     return eval.response()

                    eval.warn(f"Could not find the resource in Google searching for: {title}")
                except Exception as e:
                    eval.warn(f"Error running Google search: {str(e)}")


            # Bing Search requires an API key: go to https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.Bing%2Faccounts
            # or search for "Bing Resources" in the Azure portal
            # Free plan limitations: 1k queries per month
            bing_apikey = os.getenv('APIKEY_BING_SEARCH')
            bing_endpoint = 'https://api.bing.microsoft.com/v7.0/search'
            if bing_apikey:
                eval.info('Searching Bing for: ' + title)
                try:
                    headers = {"Ocp-Apim-Subscription-Key": bing_apikey}
                    params = {"q": title}
                    # params = {"q": title, "textDecorations": True, "textFormat": "HTML"}
                    response = requests.get(bing_endpoint, headers=headers, params=params)
                    response.raise_for_status()
                    search_results = response.json()
                    for search_res in search_results['webPages']['value']:
                        for subject_uri in resource_uris:
                            if search_res['displayUrl'].startswith(subject_uri):
                                eval.success(f"Found the resource URI {search_res['displayUrl']} when searching in Bing for {title}")
                                return eval.response()
                        # if search_res['displayUrl'] in resource_uris:
                        #     eval.success(f"Found the resource URI {search_res['displayUrl']} when searching in Bing for: {title}")
                        #     return eval.response()
                except Exception as e:
                    eval.warn(f"Error running Bing search: {str(e)}")
            else:
                eval.warn(f"No Bing API key found, skipping Bing search.")


            # Qwant search API not working
            # https://api.qwant.com/api/search/web?q=test&locale=en_us&count=10

        else:
            eval.warn('No resource title found, cannot search in Search Engine')

        return eval.response()

