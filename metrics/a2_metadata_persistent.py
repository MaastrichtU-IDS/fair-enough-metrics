import requests
from fair_test import FairTest, FairTestEvaluation
from rdflib import RDF, Literal, URIRef
from rdflib.namespace import DC, DCTERMS, FOAF, OWL, RDFS, SKOS, VOID, XSD


class MetricTest(FairTest):
    metric_path = 'a2-metadata-persistent'
    applies_to_principle = 'A2'
    title = 'Metadata is persistent'
    description = """Metric to test if the metadata contains a persistence policy, explicitly identified by a persistencePolicy key (in hashed data) or a http://www.w3.org/2000/10/swap/pim/doc#persistencePolicy predicate in Linked Data."""
    topics = ['metadata', 'persistence']
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 0,
        'https://doi.org/10.1594/PANGAEA.908011': 0,
        'https://w3id.org/AmIFAIR': 0,
        'http://example.com': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):        
        g = eval.retrieve_metadata(eval.subject)

        if not isinstance(g, (list, dict)) and len(g) > 1:
            eval.info(f'Successfully found and parsed RDF metadata. It contains {str(len(g))} triples')
        else:
            eval.failure(f"No RDF metadata found at the subject URL {eval.subject}")
            return eval.response()

        eval.info(f"Checking RDF metadata to find links to all the alternative identifiers: <{'>, <'.join(eval.data['alternative_uris'])}>")
        subject_uri = eval.extract_metadata_subject(g, eval.data['alternative_uris'])

        check_preds = [
            'http://www.w3.org/2000/10/swap/pim/doc#persistencePolicy',
        ]

        eval.info(f"Checking for a persistence policy in RDF metadata using predicates: {str(check_preds)}")
        extracted = [str(s) for s in eval.extract_prop(g, check_preds, subject_uri)] 
        if len(extracted) > 0:
            eval.success(f"Found a persistence policy: {' ,'.join(extracted)}")
            eval.data['persistence_policy'] = extracted
        else:
            eval.failure(f"Could not find a persistence policy in the metadata. Searched for the following predicates: {str(check_preds)}")


        return eval.response()
