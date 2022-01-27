from api.metrics_test import FairTest
import os
import requests
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

        self.info('Checking RDF metadata')
        # dct:conformsTo point to URI of JSON schema?
        # People could use it to point to the JSON standard (not ideal)
        # Best: get the schema (e.g. JSON schema)

        # Check also: rdfs:isDefinedBy, rdfs:seeAlso?

        return self.response()

