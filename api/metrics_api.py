from fastapi import APIRouter
import os
import importlib
import pathlib

router = APIRouter()

metrics_path = str(pathlib.Path(__file__).parent.resolve()) + '/../metrics'

# First get the metrics tests filepath
assess_name_list = []
for path, subdirs, files in os.walk(metrics_path):
    for filename in files:
        if not path.endswith('__pycache__') and not filename.endswith('__init__.py'):
            filepath = path.replace(metrics_path, '')
            if filepath:
                assess_name_list.append(filepath[1:] + '/' + filename[:-3])
            else:
                assess_name_list.append(filename[:-3])

assess_list = []
# Then import each metric test listed in the metrics folder
for assess_name in assess_name_list:
    assess_module = assess_name.replace('/', '.')
    import importlib
    MetricTest = getattr(importlib.import_module('metrics.' + assess_module), "MetricTest")

    metric = MetricTest()

    try:
        # cf. https://github.com/tiangolo/fastapi/blob/master/fastapi/routing.py#L479
        router.add_api_route(
            path=f"/{metric.metric_path}",
            methods=["POST"],
            endpoint=metric.doEvaluate,
            name=metric.title,
            openapi_extra={
                'description': metric.description
            },
            tags=[metric.applies_to_principle]
        )

        router.add_api_route(
            path=f"/{metric.metric_path}",
            methods=["GET"],
            endpoint=metric.openapi_yaml,
            name=metric.title,
            openapi_extra={
                'description': metric.description
            },
            tags=[metric.applies_to_principle]
        )
    except Exception as e:
        print('❌ No API defined for ' + metric.metric_path)
