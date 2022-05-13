from urllib.parse import urlparse

import requests
from fair_test import FairTest, FairTestEvaluation


class MetricTest(FairTest):
    metric_path = 'f1-metadata-identifier-unique'
    applies_to_principle = 'F1'
    title = 'Resource metadata identifier is unique'
    description = """Metric to test if the metadata resource has a unique identifier. This is done by checking if the GUID is a URL"""
    topics = ['metadata']
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://raw.githubusercontent.com/ejp-rd-vp/resource-metadata-schema/master/data/example-rdf/turtle/patientRegistry.ttl': 1,
        'http://example.com': 1,
        'Wrong entry': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):
        # TODO: use https://pythonhosted.org/IDUtils
        
        eval.info('Checking if the given resource URI ' + eval.subject + ' is a valid URL using urllib.urlparse')
        result = urlparse(eval.subject)
        if result.scheme and result.netloc:
            # Get URI protocol retrieved in f1_1_assess_unique_identifier
            eval.data['uri_protocol'] = result.scheme
            eval.data['uri_location'] = result.netloc
            if result.netloc == 'doi.org':
                eval.data['uri_doi'] = result.path[1:]
            eval.success('Validated the given resource URI ' + eval.subject + ' is a URL')
        else:
            eval.failure('Could not validate the given resource URI ' + eval.subject + ' is a URL')    

        return eval.response()
