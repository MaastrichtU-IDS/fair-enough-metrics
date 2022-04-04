from fair_test import FairTest, FairTestEvaluation
import requests
from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDFS, XSD, DC, DCTERMS, VOID, OWL, SKOS, FOAF


class MetricTest(FairTest):
    metric_path = 'r1-includes-license'
    applies_to_principle = 'R1'
    title = 'Metadata includes a License'
    description = """Maturity Indicator to test if the linked data metadata contains an explicit pointer to the license. Tests: xhtml, dvia, dcterms, cc, data.gov.au, and Schema license predicates in linked data."""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    topics = ['metadata', 'minimal compliance']
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://doi.org/10.1594/PANGAEA.908011': 1,
        'https://w3id.org/AmIFAIR': 1,
        'http://example.com': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):        
        # found_license = False
        # Issue with extracting license from some URIs, such as https://www.uniprot.org/uniprot/P51587
        # Getting a URI that is not really the license as output
        
        g = eval.retrieve_rdf(eval.subject)
        # g = eval.retrieve_rdf(eval.subject, use_harvester=True, harvester_url='http://wrong-url-for-testing')

        if len(g) == 0:
            eval.failure('No RDF found at the subject URL provided.')
            return eval.response()
        else:
            eval.info(f'RDF metadata containing {len(g)} triples found at the subject URL provided.')


        eval.info(f"Checking RDF metadata to find links to all the alternative identifiers: <{'>, <'.join(eval.data['alternative_uris'])}>")
        subject_uri = eval.extract_metadata_subject(g, eval.data['alternative_uris'])

        # TODO: check DataCite too?
        license_preds = [
            'http://purl.org/dc/terms/license',
            'https://schema.org/license', 
            'http://www.w3.org/1999/xhtml/vocab#license',
            'http://purl.org/ontology/dvia#hasLicense',
            'http://creativecommons.org/ns#license',
            'http://reference.data.gov.au/def/ont/dataset#hasLicense',
        ]

        eval.info(f"Checking for license in RDF metadata using predicates: {str(license_preds)}")
        licenses = [str(s) for s in eval.extract_prop(g, license_preds, subject_uri)] 
        if len(licenses) > 0:
            eval.success(f"Found licenses: {' ,'.join(licenses)}")
            eval.data['license'] = licenses
        else:
            eval.failure(f"Could not find a license in the metadata. Searched for the following predicates: {str(license_preds)}")

        return eval.response()
