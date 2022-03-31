from fair_test import FairTest, FairTestEvaluation
from urllib.parse import urlparse


class MetricTest(FairTest):
    metric_path = 'a1-data-protocol'
    applies_to_principle = 'A1.1'
    title = 'Uses an open free protocol for data retrieval'
    description = """Data may be retrieved by an open and free protocol. Tests metadata GUID for its resolution protocol. Accept URLs."""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://doi.org/10.1594/PANGAEA.908011': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):
        # TODO: use https://pythonhosted.org/IDUtils

        g = eval.retrieve_rdf(eval.subject)
        if len(g) > 1:
            eval.info(f'Successfully found and parsed RDF metadata. It contains {str(len(g))} triples')

        subject_uri = eval.extract_subject_from_metadata(g, eval.data['alternative_uris'])
        # Retrieve URI of the data in the RDF metadata
        data_res = eval.extract_data_uri(g, subject_uri)
        if len(data_res) < 1:
            eval.failure("Could not find data URI in the metadata.")


        for data_uri in data_res:
            eval.info('Checking if the data URI ' + data_uri + ' is a valid URL using urllib.urlparse')
            result = urlparse(data_uri)
            if result.scheme and result.netloc:
                # Get URI protocol retrieved in f1_1_assess_unique_identifier
                eval.data['uri_protocol'] = result.scheme
                eval.data['uri_location'] = result.netloc
                if result.netloc == 'doi.org':
                    eval.data['uri_doi'] = result.path[1:]
                eval.success('Validated the data URI ' + data_uri + ' is a URL')
            else:
                eval.failure('Could not validate the data URI ' + data_uri + ' is a URL')    


        return eval.response()
