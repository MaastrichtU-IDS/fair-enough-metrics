from api.metrics_test import TestInput, FairTest
import os

class DefaultInput(TestInput):
    subject = 'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972'


class MetricTest(FairTest):
    metric_version = '0.1.0'
    metric_path = 'i3-data-management-plan'
    applies_to_principle = 'I3'

    title = 'Check Data Management Plan'
    description = """An assessment to test if a DMP is properly defined. To be developed
For a collection on evaluating digital Data Management Plans
We can reuse SPARQL queries from the maDMP-evaluation repository: 
https://github.com/raffaelfoidl/maDMP-evaluation/tree/v1.2/queries"""
    max_score = 1
    max_bonus = 0

    def evaluate(self, input: DefaultInput):
        self.subject = input.subject

        self.info('Checking DMP')
            
        return self.response()

