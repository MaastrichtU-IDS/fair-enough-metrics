from fair_test import FairTest
import os
import requests
from rdflib.namespace import DCTERMS


class MetricTest(FairTest):
    metric_path = 'r3-meets-community-standards'
    applies_to_principle = 'R3'
    title = 'Meets Community Standards'
    description = """Such certification services may not exist, but this principle serves to encourage the community 
to create both the standard(s) and the verification services for those standards.  
A potentially useful side-effect of this is that it might provide an opportunity for content-verification
e.g. the certification service provides a hash of the data, which can be used to validate that it has not been edited at a later date.
"""
    metric_version = '0.1.0'
    

    def evaluate(self):

        g = self.retrieve_rdf(self.subject)

        for s, p, o in g.triples((None, DCTERMS.conformsTo, None)):
            self.info(f'Found a value for dcterms:conformsTo: {str(o)}')
            res = requests.get(str(o))
            conformsToShape = res.text
            self.info(conformsToShape)

        # dct:conformsTo point to URI of JSON schema?
        # People could use it to point to the JSON standard (not ideal)
        # Best: get the schema (e.g. JSON schema)

        # Check also: rdfs:isDefinedBy, rdfs:seeAlso?

        return self.response()

