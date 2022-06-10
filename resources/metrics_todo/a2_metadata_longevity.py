import os

import requests
from fair_test import FairTest, FairTestEvaluation


class MetricTest(FairTest):
    metric_version = "0.1.0"
    metric_path = "a2-metadata-longevity"
    applies_to_principle = "A2"
    title = "Metadata Longevity"
    description = """The existence of metadata even in the absence/removal of data
Cross-references to data from third-party's FAIR data and metadata will 
naturally degrade over time, and become 'stale links'.  
In such cases, it is important for FAIR providers to continue to provide 
descriptors of what the data was to assist in the continued interpretation of 
those third-party data. As per FAIR Principle F3, this metadata remains 
discoverable, even in the absence of the data, because it contains an 
explicit reference to the IRI of the data"""

    def evaluate(self, eval: FairTestEvaluation):

        eval.info("Checking for metadata in long term repository?")

        return eval.response()
