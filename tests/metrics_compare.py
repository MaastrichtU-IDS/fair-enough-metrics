import requests

# import pytest
# from fastapi.testclient import TestClient
# import json
# from main import app

# python tests/metrics_compare.py
# pytest tests/test_metrics_compare.py -s


eval_list = {
    'f2-machine-readable-metadata':[
        {
            'subject': 'https://w3id.org/fair-enough/evaluations/fd302af6970ef794a340de9a87436ae8afcb6a02',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
        {
            'subject': 'https://w3id.org/FAIR_Evaluator/evaluations/6259.json',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
        {
            'subject': 'https://doi.org/10.1594/PANGAEA.908011',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
        {
            'subject': 'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
        {
            'subject': 'https://doi.org/10.1186/2041-1480-5-14',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
        {
            'subject': 'https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
        {
            'subject': 'https://doi.org/10.5281/zenodo.5541440',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
        {
            'subject': 'https://doi.org/10.34894/DR3I2A',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
        {
            'subject': 'https://doi.org/10.1045/november2015-vandesompel',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
        {
            'subject': 'https://doi.org/10.1016/j.jbi.2008.03.004',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
        {
            'subject': 'https://doi.org/10.1038/sdata.2016.18',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
        {
            'subject': 'https://doi.org/10.1016/J.JBI.2019.103292',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
        {
            'subject': 'https://w3id.org/AmIFAIR',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
        # {
        #     'subject': 'https://purl.uniprot.org/uniprot/P51587',
        #     'score-fair-enough': 1,
        #     'score-fair-evaluator': 1,
        # },
        {
            'subject': 'https://github.com/MaastrichtU-IDS/fair-test',
            'score-fair-enough': 1,
            'score-fair-evaluator': 1,
        },
    ]
}


# endpoint = TestClient(app)
api_fair_evaluator = 'https://w3id.org/FAIR_Tests/tests'
api_fair_enough = 'https://w3id.org/fair-enough/metrics/tests'

map_metrics_url = {
    'f2-machine-readable-metadata': 'gen2_structured_metadata'
}

# def test_compare():
def main():
    print("Checking FAIR evaluation services results when retrieving RDF metadata for URIs")
    success_count = {
        'fair-enough': 0,
        'fair-evaluator': 0,
    }
    for metric_id, evals in eval_list.items():
        for eval in evals:
            # Test for FAIR enough
            r = requests.post(f"{api_fair_enough}/{metric_id}",
                json={ 'subject': eval['subject'] },
                headers={"Accept": "application/json"}
            )
            print(f"🔎 Testing for \033[1m{eval['subject']}\033[0m")
            # assert r.status_code == 200
            res_fair_enough = r.json()

            # Check score:
            score_fair_enough = int(res_fair_enough[0]['http://semanticscience.org/resource/SIO_000300'][0]['@value'])
            if score_fair_enough > 0:
                success_count['fair-enough'] += 1


            # Test for the FAIR evaluator
            r = requests.post(f"{api_fair_evaluator}/{map_metrics_url[metric_id]}",
                json={"subject": eval['subject']},
                # timeout=60,
                # headers={"Accept": "application/ld+json"}
            )
            res_fair_evaluator = r.json()
            score_fair_evaluator = int(res_fair_evaluator[0]['http://semanticscience.org/resource/SIO_000300'][0]['@value'])
            if score_fair_evaluator > 0:
                success_count['fair-evaluator'] += 1

            print(f"\033[95mFAIR enough {score_fair_enough}\033[0m / \033[91m{score_fair_evaluator} FAIR evaluator\033[0m")

    print('')
    print(f"FAIR enough found metadata for \033[1m{success_count['fair-enough']}\033[0m subjects URIs")
    print(f"FAIR evaluator found metadata for \033[1m{success_count['fair-evaluator']}\033[0m subjects URIs")
            # assert score_fair_enough == eval['score-fair-enough']
            # assert score_fair_evaluator == eval['score-fair-evaluator']


if __name__ == "__main__":
    main()