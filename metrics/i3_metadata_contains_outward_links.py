from urllib.parse import urlparse

from fair_test import FairTest, FairTestEvaluation


class MetricTest(FairTest):
    metric_path = 'i3-metadata-contains-outward-links'
    applies_to_principle = 'I3'
    title = 'Metadata contains outward references'
    description = """Maturity Indicator to test if the metadata links outward to third-party resources.
It only tests metadata that can be represented as Linked Data.
It will succeed if you have at least 1 object in your metadata that uses a different host than the subject URI evaluated."""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    topics = ['metadata', 'linked data']
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://doi.org/10.1594/PANGAEA.908011': 1,
        'http://example.com': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):        
        # https://github.com/vemonet/fuji/blob/master/fuji_server/helper/preprocessor.py#L190
        g = eval.retrieve_metadata(eval.subject)
        if not isinstance(g, (list, dict)) and len(g) > 1:
            eval.info(f'Successfully found and parsed RDF metadata available at {eval.subject}. It contains {str(len(g))} triples')
        else:
            eval.failure(f"No RDF metadata found at the subject URL {eval.subject}")
            return eval.response()
            
        subject_loc = None
        result = urlparse(eval.subject)
        if result.scheme and result.netloc:
            subject_loc = result.netloc
        else:
            eval.failure(f'Could not parse the subject as a URL: {eval.subject}')
            return eval.response()

        outward_links_count = 0
        for s, p, o in g.triples((None, None, None)):
            result = urlparse(str(o))
            if result.netloc != subject_loc:
                outward_links_count += 1
            if outward_links_count >= 10:
                break

        if outward_links_count > 0:
            eval.success(f"More than {outward_links_count} outward links has been found as objects")
        else:
            eval.failure(f"No outward links has been found in the metadata")

        return eval.response()
