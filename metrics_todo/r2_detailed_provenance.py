from api.metrics_test import TestInput, FairTest
import os
import requests

class DefaultInput(TestInput):
    subject = 'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972'


class MetricTest(FairTest):
    metric_version = '0.1.0'
    metric_path = 'r2-detailed-provenance'
    applies_to_principle = 'R2'

    title = 'Detailed Provenance'
    description = """That there is provenance information associated with the data, covering at least two primary types of provenance information:
- Who/what/When produced the data (i.e. for citation)
- Why/How was the data produced (i.e. to understand context and relevance of the data)
"""
    author = 'https://orcid.org/0000-0002-1501-1082'

    def evaluate(self, input: DefaultInput):
        self.subject = input.subject

        self.info('Checking RDF metadata for prov and pav metadata')
        # Author, contributor, creationDate

            
        return self.response()

