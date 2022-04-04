from fair_test import FairTest, FairTestEvaluation
from urllib.parse import urlparse


class MetricTest(FairTest):
    metric_path = 'f1-data-identifier-persistent'
    applies_to_principle = 'F1'
    title = 'Data identifier is persistent'
    description = """Metric to test if the unique identifier of the data resource is likely to be persistent. 
We test known URL persistence schemas (purl, doi, w3id, identifiers.org)."""
    topics = ['data', 'persistence']
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://doi.org/10.1594/PANGAEA.908011': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):
        # TODO: use https://pythonhosted.org/IDUtils
        accepted_persistent = [
            'doi.org', 
            'purl.org', 'purl.oclc.org', 'purl.net', 'purl.com', 
            'identifiers.org', 
            'w3id.org',
        ]

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
            eval.failure("Could not find data URI in the metadata.")
        else:
            eval.info(f"Check if the data URI uses a persistent URI, one of: {', '.join(accepted_persistent)}")

        for data_uri in eval.data['content_url']:
            eval.info('Check if the data URI ' + data_uri + ' use a persistent URI, one of: ' + ', '.join(accepted_persistent))
            r = urlparse(data_uri)
            if r.netloc and r.netloc in accepted_persistent:
                eval.success(f'Validated the data URI {data_uri} is a persistent URL')
            else:
                eval.failure('The data URI ' + data_uri + ' is not considered a persistent URL')


        return eval.response()
