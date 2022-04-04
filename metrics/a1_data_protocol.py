from fair_test import FairTest, FairTestEvaluation
from urllib.parse import urlparse


class MetricTest(FairTest):
    metric_path = 'a1-data-protocol'
    applies_to_principle = 'A1.1'
    title = 'Uses an open free protocol for data retrieval'
    description = """Data may be retrieved by an open and free protocol. Tests metadata GUID for its resolution protocol.
    
Successful if the subject is a URL."""
    topics = ['data']
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://doi.org/10.1594/PANGAEA.908011': 1,
    }


    def evaluate(self, eval: FairTestEvaluation):
        # TODO: use https://pythonhosted.org/IDUtils

        g = eval.retrieve_metadata(eval.subject)
        if not isinstance(g, (list, dict)) and len(g) > 0:
            eval.info(f'Successfully found and parsed RDF metadata. It contains {str(len(g))} triples')
        else:
            eval.failure(f"No RDF metadata found at the subject URL {eval.subject}")
            return eval.response()

        subject_uri = eval.extract_metadata_subject(g, eval.data['alternative_uris'])
        # Retrieve URI of the data in the RDF metadata
        data_res = eval.extract_data_subject(g, subject_uri)
        if len(eval.data['content_url']) < 1:
            eval.failure("Could not find the data URI in the subject metadata.")

        # We check the content URL, because data_res can be a BNode
        for data_uri in eval.data['content_url']:
            eval.info(f'Checking if the data URI {data_uri} is a valid URL using urllib.urlparse')
            result = urlparse(data_uri)
            if result.scheme and result.netloc:
                # Get URI protocol retrieved in f1_1_assess_unique_identifier
                eval.data['uri_protocol'] = result.scheme
                eval.data['uri_location'] = result.netloc
                if result.netloc == 'doi.org':
                    eval.data['uri_doi'] = result.path[1:]
                eval.success('Validated the data URI ' + data_uri + ' is a URL')
            else:
                eval.warn('Could not validate the data URI ' + data_uri + ' is a URL')    


        return eval.response()
