from turtle import title
from fastapi import FastAPI, APIRouter, Body
from typing import List
from pydantic import BaseModel, Field
import os
import importlib
import pathlib
from rdflib import Graph

from api.config import settings
# from api.metrics_test import FairEvaluationInput

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
    # print('Import ' + assess_module)
    import importlib
    MetricTest = getattr(importlib.import_module('metrics.' + assess_module), "MetricTest")
    # module = __import__('app.assessments.' + assess_name, fromlist=['Assessment'])
    # Assessment = getattr(module, 'Assessment')
    # assess_list.append(Assessment(assess_name).dict(by_alias=True))

    ## If the object constructor requires args:
    # metric = MetricTest(assess_name)
    metric = MetricTest()
    # metric_id = metric.metric_id + '-' + metric.title.lower().replace(' ', '-')

    # TODO: import the Assessment.metric() (@app decorated) to the APIRouter
    try:
        # router.include_router(metric.api, tags=["metrics"])
        # cf. https://github.com/tiangolo/fastapi/blob/master/fastapi/routing.py#L479
        router.add_api_route(
            path=f"/{metric.metric_path}",
            methods=["POST"],
            endpoint=metric.evaluate,
            name=metric.title,
            openapi_extra={
                'description': metric.description
            },
            tags=[metric.applies_to_principle]
            # tags=[f"{metric.applies_to_principle} {metric.title}"]
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

    # @router.post(
    #     "/" + metric_id,
    #     name=metric.title,
    #     description=metric.description,
    #     response_description="FAIR metric score", 
    #     # response_model=List[AssessmentModel]
    # )
    # async def fair_metrics(input: EvalInput = Body(...)) -> List[AssessmentModel]:
    #     try: 
    #         init_eval = {
    #             'resource_uri': input.subject,
    #             'title': 'Run assessment',
    #             'collection': 'fair-metrics',
    #             'data': {'alternative_uris': [input.subject]},
    #             '@id': f'{settings.BASE_URI}/evaluation/run-assessment',
    #             '@context': settings.CONTEXT
    #         }
    #         eval = EvaluationModel(**init_eval)
    #         g = Graph()

    #         eval, g = metric.runEvaluate(eval, g)
    #         # return eval.results[0].dict(with_alias=True)
    #         print(eval.results[0])
    #         eval.results[0]['data'] = eval.data
    #         return eval.results[0]

    #     except Exception as e:
    #         print('❌ Error running the assessment ' + metric_id)
    #         print(e)
