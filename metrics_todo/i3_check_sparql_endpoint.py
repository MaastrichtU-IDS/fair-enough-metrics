from api.metrics_test import TestInput, FairTest
import os

class DefaultInput(TestInput):
    subject = 'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972'


class MetricTest(FairTest):
    metric_version = '0.1.0'
    metric_path = 'i3-check-sparl-endpoint'
    applies_to_principle = 'I3'

    title = 'Check the content of a SPARQL endpoint'
    description = """An assessment to run queries to check the content of a SPARQL endpoint
For a collection on evaluation knowledge graphs
Reuse https://github.com/MaastrichtU-IDS/d2s-cli/blob/master/d2s/generate_metadata.py"""
    max_score = 1
    max_bonus = 0

    def evaluate(self, input: DefaultInput):
        self.subject = input.subject

        self.info('Checking DMP')
            
        return self.response()

