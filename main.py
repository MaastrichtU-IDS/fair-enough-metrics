from fair_test import FairTestAPI


app = FairTestAPI(
    title='FAIR Enough Metrics tests API',
    metrics_folder_path='metrics',
    description="""FAIR Metrics tests API for generic resources related to research. Follows the specifications described by the [FAIRMetrics](https://github.com/FAIRMetrics/Metrics) working group.

[Metrics Tests source code here](https://github.com/MaastrichtU-IDS/fair-enough-metrics), built with the [**fair-test** library](https://maastrichtu-ids.github.io/fair-test)

[![Test Metrics](https://github.com/MaastrichtU-IDS/fair-enough-metrics/actions/workflows/test.yml/badge.svg)](https://github.com/MaastrichtU-IDS/fair-enough-metrics/actions/workflows/test.yml)
""",
    license_info = {
        "name": "MIT license",
        "url": "https://opensource.org/licenses/MIT"
    },
)
