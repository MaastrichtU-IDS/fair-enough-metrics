import os

from fair_test import FairTest, FairTestEvaluation


class MetricTest(FairTest):
    metric_path = "i3-data-management-plan"
    applies_to_principle = "I3"
    title = "Check Data Management Plan"
    description = """An assessment to test if a DMP is properly defined. To be developed
For a collection on evaluating digital Data Management Plans
We can reuse SPARQL queries from the maDMP-evaluation repository: 
https://github.com/raffaelfoidl/maDMP-evaluation/tree/v1.2/queries"""
    metric_version = "0.1.0"

    def evaluate(self, eval: FairTestEvaluation):

        eval.info("Checking DMP")

        return eval.response()
