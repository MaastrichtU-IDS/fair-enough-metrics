from api.metrics_test import TestInput, FairTest
import os
import requests

class DefaultInput(TestInput):
    subject = 'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972'


class MetricTest(FairTest):
    metric_version = '0.1.0'
    metric_path = 'r3-meets-community-standards'
    applies_to_principle = 'R3'
    title = 'Meets Community Standards'
    description = """Such certification services may not exist, but this principle serves to encourage the community 
to create both the standard(s) and the verification services for those standards.  
A potentially useful side-effect of this is that it might provide an opportunity for content-verification
e.g. the certification service provides a hash of the data, which can be used to validate that it has not been edited at a later date."""
    max_score = 1
    max_bonus = 0

    def evaluate(self, input: DefaultInput):
        self.subject = input.subject


        self.info('Checking RDF metadata')
        # dct:conformsTo point to URI of JSON schema?
        # People could use it to point to the JSON standard (not ideal)
        # Best: get the schema (e.g. JSON schema)

        # Check also: rdfs:isDefinedBy, rdfs:seeAlso?

        return self.response()

