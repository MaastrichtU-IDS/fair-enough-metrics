import os

from fair_test import FairTest, FairTestEvaluation


class MetricTest(FairTest):
    metric_path = "i3-use-references"
    applies_to_principle = "I3"
    title = "Use Qualified References"
    description = """Relationships within (meta)data, and between local 
and third-party data, have explicit and 'useful' semantic meaning. 
The linksets must have qualified references: at least one of the links must be in a different Web domain 
(or the equivalent of a different namespace for non-URI identifiers)"""
    metric_version = "0.1.0"

    def evaluate(self, eval: FairTestEvaluation):

        eval.info("Checking RDF metadata vocabularies")

        return eval.response()
