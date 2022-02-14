from fair_test import FairTestAPI


app = FairTestAPI(
    title='FAIR Metrics tests API',
    metrics_folder_path='metrics',
    description="""FAIR Metrics tests API for resources related to research. Follows the specifications described by the [FAIRMetrics](https://github.com/FAIRMetrics/Metrics) working group.""",
    license_info = {
        "name": "MIT license",
        "url": "https://opensource.org/licenses/MIT"
    },
)
