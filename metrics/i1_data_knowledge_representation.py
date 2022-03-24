from fair_test import FairTest
import json
import rdflib
# JSON-LD workaround 
# from pyld import jsonld
# from rdflib import ConjunctiveGraph
# from rdflib.serializer import Serializer


class MetricTest(FairTest):
    metric_path = 'i1-data-knowledge-representation'
    applies_to_principle = 'I1'
    title = 'Data uses a formal knowledge representation language (strong)'
    description = """Maturity Indicator to test if the data uses a formal language broadly applicable for knowledge representation.
This particular test takes a broad view of what defines a 'knowledge representation language'; in this evaluation, a knowledge representation language is interpreted as one in which terms are semantically-grounded in ontologies.
Any form of ontologically-grounded linked data will pass this test."""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'


    def evaluate(self):        
        g = self.getRDF(self.subject)
        if len(g) > 1:
            self.info(f'Successfully found and parsed RDF metadata. It contains {str(len(g))} triples')

        data_props = [
            "http://www.w3.org/ns/ldp#contains", "http://xmlns.com/foaf/0.1/primaryTopic", 
            "https://schema.org/about", "https://schema.org/mainEntity", "https://schema.org/codeRepository",
            "https://schema.org/distribution", "https://www.w3.org/ns/dcat#distribution", 
            "http://semanticscience.org/resource/SIO_000332", "http://semanticscience.org/resource/is-about", 
            "https://purl.obolibrary.org/obo/IAO_0000136"
        ]

        data_res = self.getProps(data_props)
        if len(data_res.keys() < 1):
            self.failure("Could not find data for the metadata. Searched for the following predicates: " + ', '.join(data_props))

        for pred, value in data_res.items():
            data_g = self.getRDF(value)
            if len(data_g) > 1:
                self.success(f'Successfully parsed the RDF for the {pred} data at {value}. It contains {str(len(g))} triples')

        return self.response()

