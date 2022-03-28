from fair_test import FairTest, FairTestEvaluation
import os
import requests


class MetricTest(FairTest):
    metric_path = 'r2-detailed-provenance'
    applies_to_principle = 'R2'

    title = 'Detailed Provenance'
    description = """That there is provenance information associated with the data, covering at least two primary types of provenance information:
- Who/what/When produced the data (i.e. for citation)
- Why/How was the data produced (i.e. to understand context and relevance of the data)
"""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'

    def evaluate(self, eval: FairTestEvaluation):
        
        eval.info('Checking RDF metadata for prov and pav metadata')
        # Author, contributor, creationDate

        return eval.response()

