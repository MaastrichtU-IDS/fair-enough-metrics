from urllib.parse import urlparse

import requests
from fair_test import FairTest, FairTestEvaluation
from rdflib.namespace import DC, DCTERMS, OWL, RDFS, SKOS, VOID, XSD


class MetricTest(FairTest):
    metric_path = 'a1-metadata-authorization'
    applies_to_principle = 'A1.2'
    title = 'Metadata authentication and authorization'
    description = """Tests metadata GUID for the ability to implement authentication and authorization in its resolution protocol. Accept URLs, DOIs, handles."""
    topics = ['metadata']
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    tests={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://raw.githubusercontent.com/ejp-rd-vp/resource-metadata-schema/master/data/example-rdf/turtle/patientRegistry.ttl': 1,
        'Wrong entry': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):
        
        eval.info(f"Checking if the resource identifier {eval.subject} uses a valid protocol that enables authorization, such as URL, DOI, or handle")
        subject_url = eval.get_url(eval.subject)

        if subject_url:
            eval.success(f'The resource {eval.subject} uses a valid protocol that enables authorization')

        else:
            eval.failure(f'The resource {eval.subject} does not use a valid protocol that enables authorization, such as URL, DOI, or handle')

        return eval.response()
