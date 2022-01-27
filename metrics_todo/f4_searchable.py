from api.metrics_test import TestInput, FairTest
import requests
# from googlesearch import search

from fastapi import APIRouter, Body, Depends
# from fastapi_utils.cbv import cbv
from rdflib import Graph

class DefaultInput(TestInput):
    subject = 'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972'


class MetricTest(FairTest):
    metric_version = '0.1.0'
    metric_path = 'f4-searchable'
    applies_to_principle = 'F4'

    title = 'The resource is indexed in a searchable resource'
    description = """Search for existing metadata about the resource URI in data repositories, such as DataCite, RE3data."""
    author = 'https://orcid.org/0000-0002-1501-1082'
    max_score = 1
    max_bonus = 0

    def evaluate(self, input: DefaultInput):
        self.subject = input.subject

        datacite_endpoint = 'https://api.datacite.org/repositories'
        re3data_endpoint = 'https://re3data.org/api/beta/repositories'
        datacite_dois_api = 'https://api.datacite.org/dois/'
        # metadata_catalog = https://rdamsc.bath.ac.uk/api/m
        # headers = {"Accept": "application/json"}

        # If DOI: check for metadata in DataCite API
        try:
            if 'uri_doi' in self.data and self.data['uri_doi']:
                doi = self.data['uri_doi']
                self.info('Checking DataCite API for metadata about the DOI: ' + doi)
                r = requests.get(datacite_dois_api + doi, timeout=10)
                datacite_json = r.json()
                datacite_data = datacite_json['data']['attributes']
                print(datacite_json['data']['attributes'].keys())
                # ['id', 'type', 'attributes', 'relationships']
                if datacite_data:
                    self.success('Retrieved metadata about ' + doi + ' from DataCite API')
                    self.data['datacite'] = {}
                    print('datacite_data')
                    print(datacite_data.keys())

                    if 'titles' in datacite_data.keys():
                        self.data['datacite']['title'] = datacite_data['titles'][0]['title']
                        print(self.data['datacite']['title'])
                        if not 'resource_title' in self.data:
                            self.data['resource_title'] = self.data['datacite']['title']

                    if 'descriptions' in datacite_data.keys():
                        self.data['datacite']['description'] = datacite_data['descriptions'][0]['description']
                    
            else:
                self.warn('DOI could not be found, skipping search in DataCite API')
        except Exception as e:
            self.warn('Search in DataCite API failed: ' + e.args[0])

        # self.info('Checking RE3data APIs from DataCite API for metadata about ' + uri)
        # p = {'query': 're3data_id:*'}
        # req = requests.get(datacite_endpoint, params=p, headers=headers)
        # print(req.json())


        ## Check google search using the resource title and its alternative URIs
        ## Might be against Google TOS
        # if 'resource_title' in self.data.keys():
        #     resource_title = self.data['resource_title']
            
        #     resource_uris = self.data['alternative_uris']

        #     self.info('Running Google search for: ' + resource_title)
        #     search_results = list(search(resource_title, tld="co.in", num=20, stop=20, pause=1))
        #     print(search_results)

        #     found_uris = list(set(resource_uris).intersection(search_results))
        #     # if any(i in resource_uris for i in search_results):
        #     if found_uris:
        #         self.success('Found the resource URI ' + ', '.join(found_uris) + ' when searching on Google for ' + resource_title)
        #     else:
        #         self.failure('Did not find one of the resource URIs ' + ', '.join(resource_uris) + ' in: '+ ', '.join(search_results))
        # else:
        #     self.failure('No resource title found, cannot search in google')

            
        return self.response() 


