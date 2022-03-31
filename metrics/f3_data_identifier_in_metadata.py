from fair_test import FairTest, FairTestEvaluation
from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDFS, XSD, DC, DCTERMS, VOID, OWL, SKOS, FOAF
from urllib.parse import urlparse


class MetricTest(FairTest):
    metric_path = 'f3-data-identifier-in-metadata'
    applies_to_principle = 'F3'
    title = 'Data identifier explicitly in metadata'
    description = """Metric to test if the metadata contains the unique identifier to the data. 
This is done by searching for a variety of properties, including foaf:primaryTopic, schema:mainEntity, schema:distribution, sio:is-about, and iao:is-about. schema codeRepository is used for software releases."""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        # 'https://doi.org/10.1594/PANGAEA.908011': 1,
        # 'https://w3id.org/AmIFAIR': 1,
        'http://example.com': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):
        g = eval.retrieve_rdf(eval.subject)
        if len(g) > 1:
            eval.info(f'Successfully found and parsed RDF metadata. It contains {str(len(g))} triples')

        subject_uri = eval.extract_subject_from_metadata(g, eval.data['alternative_uris'])
        # Retrieve URI of the data in the RDF metadata
        data_res = eval.extract_data_uri(g, subject_uri)

        if len(data_res) > 1:
            eval.success(f"Found the data URI in the metadata: {', '.join(data_res)}")
        else: 
            eval.failure("Could not find data URI in the metadata.")

        return eval.response()
