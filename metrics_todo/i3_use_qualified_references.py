from api.metrics_test import TestInput, FairTest
import os

class DefaultInput(TestInput):
    subject = 'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972'


class MetricTest(FairTest):
    metric_version = '0.1.0'
    metric_path = 'i3-use-references'
    applies_to_principle = 'I3'

    title = 'Use Qualified References'
    description = """Relationships within (meta)data, and between local 
and third-party data, have explicit and 'useful' semantic meaning. 
The linksets must have qualified references: at least one of the links must be in a different Web domain 
(or the equivalent of a different namespace for non-URI identifiers)"""
    max_score = 1
    max_bonus = 0

    def evaluate(self, input: DefaultInput):
        self.subject = input.subject

        self.info('Checking RDF metadata vocabularies')
            
        return self.response()

