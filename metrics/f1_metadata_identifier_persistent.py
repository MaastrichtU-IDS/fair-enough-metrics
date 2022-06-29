from urllib.parse import urlparse

import requests
from fair_test import FairTest, FairTestEvaluation

# import idutils


class MetricTest(FairTest):
    metric_path = 'f1-metadata-identifier-persistent'
    applies_to_principle = 'F1'
    title = 'Resource identifier is persistent'
    description = """Metric to test if the unique identifier of the metadata resource is likely to be persistent. 
We test known URL persistence schemas (purl, doi, w3id, identifiers.org)."""
    topics = ['metadata', 'persistence']
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        '10.1016/j.jbi.2008.03.004': 1,
        'doi:10.1016/j.jbi.2008.03.004': 1,
        'https://raw.githubusercontent.com/ejp-rd-vp/resource-metadata-schema/master/data/example-rdf/turtle/patientRegistry.ttl': 0,
        'http://example.com': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):
        
        accepted_persistent = [
            'doi.org', 
            'purl.org', 'purl.oclc.org', 'purl.net', 'purl.com', 
            'identifiers.org', 
            'w3id.org',
        ]

        subject_url = eval.get_url(eval.subject)
        if not subject_url:
            eval.failure(f'The resource {eval.subject} does not use a valid identifier schema, such as URL, DOI, or handle')
            return eval.response()

        eval.info(f"Check if the given resource URI {subject_url} use a persistent URI, one of: {', '.join(accepted_persistent)}")
        r = urlparse(subject_url)
        if r.netloc and r.netloc in accepted_persistent:
            eval.success(f'Validated the given resource URI {subject_url} is a persistent URL')
        else:
            eval.failure(f'The given resource URI {subject_url} is not considered a persistent URL')

        return eval.response()
