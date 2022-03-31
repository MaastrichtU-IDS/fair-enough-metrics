from fair_test import FairTest, FairTestEvaluation
import requests
from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDFS, XSD, DC, DCTERMS, VOID, OWL, SKOS, FOAF


class MetricTest(FairTest):
    metric_path = 'a2-metadata-persistent'
    applies_to_principle = 'A2'
    title = 'Metadata is persistent'
    description = """Metric to test if the metadata contains a persistence policy, explicitly identified by a persistencePolicy key (in hashed data) or a http://www.w3.org/2000/10/swap/pim/doc#persistencePolicy predicate in Linked Data."""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 0,
        'https://doi.org/10.1594/PANGAEA.908011': 0,
        'https://w3id.org/AmIFAIR': 0,
        'http://example.com': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):        
        g = eval.retrieve_rdf(eval.subject)

        if len(g) == 0:
            eval.failure('No RDF found at the subject URL provided.')
            return eval.response()
        else:
            eval.info(f'RDF metadata containing {len(g)} triples found at the subject URL provided.')


        eval.info(f"Checking RDF metadata to find links to all the alternative identifiers: <{'>, <'.join(eval.data['alternative_uris'])}>")
        subject_uri = eval.extract_subject_from_metadata(g, eval.data['alternative_uris'])

        check_preds = [
            'http://www.w3.org/2000/10/swap/pim/doc#persistencePolicy',
        ]

        eval.info(f"Checking for license in RDF metadata using predicates: {str(check_preds)}")
        extracted = eval.extract_prop(g, check_preds, subject_uri)
        if len(extracted) > 0:
            eval.success(f"Found a persistent policy: {' ,'.join(extracted)}")
            eval.data['persistence_policy'] = extracted
        else:
            eval.failure(f"Could not find a license in the metadata. Searched for the following predicates: {str(check_preds)}")


        return eval.response()
