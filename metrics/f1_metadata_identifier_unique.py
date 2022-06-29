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
        
        eval.info(f"Checking if the resource identifier {eval.subject} uses a valid protocol, such as URL, DOI, or handle")
        subject_url = eval.get_url(eval.subject)

        if subject_url:
            eval.success(f'The resource {eval.subject} uses a valid protocol')

        else:
            eval.failure(f'The resource {eval.subject} does not use a valid protocol, such as URL, DOI, or handle')

        return eval.response()
