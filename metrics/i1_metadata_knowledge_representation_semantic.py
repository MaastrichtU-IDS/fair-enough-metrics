from fair_test import FairTest, FairTestEvaluation


class MetricTest(FairTest):
    metric_path = 'i1-metadata-knowledge-representation-semantic'
    applies_to_principle = 'I1'
    title = 'Metadata uses a formal semantic knowledge representation language'
    description = """Maturity Indicator to test if the metadata uses a formal language broadly applicable for knowledge representation.
This particular test takes a broad view of what defines a 'knowledge representation language'; in this evaluation, a knowledge representation language is interpreted as one in which terms are semantically-grounded in ontologies.
Any form of RDF will pass this test"""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    topics = ['metadata', 'linked data', 'advanced compliance']
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://doi.org/10.1594/PANGAEA.908011': 1,
        'http://example.com': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):        
        # https://github.com/vemonet/fuji/blob/master/fuji_server/helper/preprocessor.py#L190
        g = eval.retrieve_metadata(eval.subject)
        if not isinstance(g, (list, dict)) and len(g) > 0:
            eval.success(f'Successfully found and parsed RDF metadata available at {eval.subject}. It contains {str(len(g))} triples')
        else:
            eval.failure(f"No RDF metadata found at the subject URL {eval.subject}")
            
        return eval.response()
