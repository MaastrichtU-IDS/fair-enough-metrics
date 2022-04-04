from fair_test import FairTest, FairTestEvaluation


class MetricTest(FairTest):
    metric_path = 'i1-data-knowledge-representation-semantic'
    applies_to_principle = 'I1'
    title = 'Data uses a formal semantic knowledge representation language'
    description = """Maturity Indicator to test if the data uses a formal language broadly applicable for knowledge representation.
This particular test takes a broad view of what defines a 'knowledge representation language'; in this evaluation, a knowledge representation language is interpreted as one in which terms are semantically-grounded in ontologies.
Any form of ontologically-grounded linked data will pass this test."""
    topics = ['data', 'linked data', 'advanced compliance']
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        # 'https://doi.org/10.1594/PANGAEA.908011': 1,
        'http://example.com': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):        
        g = eval.retrieve_metadata(eval.subject)
        if not isinstance(g, (list, dict)) and len(g) > 0:
            eval.info(f'Successfully found and parsed RDF metadata available at {eval.subject}. It contains {str(len(g))} triples')
        else:
            eval.failure(f"No RDF metadata found at the subject URL {eval.subject}")
            return eval.response()

        subject_uri = eval.extract_metadata_subject(g, eval.data['alternative_uris'])
        # Retrieve URI of the data in the RDF metadata
        data_res = eval.extract_data_subject(g, subject_uri)
        if len(eval.data['content_url']) < 1:
            eval.failure("Could not find data URI in the metadata.")

        # Check if RDF data can be found at the data URI
        for value in eval.data['content_url']:
            data_g = eval.retrieve_metadata(value)
            if not isinstance(data_g, (list, dict)) and len(data_g) > 0:
                eval.success(f'Successfully found and parsed RDF metadata available at {value}. It contains {str(len(data_g))} triples')
            else:
                eval.warn(f"No RDF metadata found at the subject URL {value}")

        return eval.response()
