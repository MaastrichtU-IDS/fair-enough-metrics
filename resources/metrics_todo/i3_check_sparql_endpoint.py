import os

from fair_test import FairTest, FairTestEvaluation


class MetricTest(FairTest):
    metric_version = "0.1.0"
    metric_path = "i3-check-sparl-endpoint"
    applies_to_principle = "I3"
    title = "Check the content of a SPARQL endpoint"
    description = """An assessment to run queries to check the content of a SPARQL endpoint
For a collection on evaluation knowledge graphs
Reuse https://github.com/MaastrichtU-IDS/d2s-cli/blob/master/d2s/generate_metadata.py"""

    def evaluate(self, eval: FairTestEvaluation):

        eval.info("Checking DMP")

        return eval.response()
