import requests

# python tests/services_compare.py

# List of subject URLs to evaluate
eval_list = [
    # {
    #     'subject': 'https://w3id.org/fair-enough/evaluations/53d76f04ab36cc17ce455b149d7c3583e5621d29',
    #     'provider': 'FAIR enough',
    # },
    {
        'subject': 'https://w3id.org/FAIR_Evaluator/evaluations/6259.json',
        'provider': 'FAIR evaluator',
    },
    {
        'subject': 'https://doi.org/10.1594/PANGAEA.908011',
        'provider': 'Pangaea',
    },
    {
        'subject': 'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972',
        'provider': 'FAIR Data Point',
    },
    {
        'subject': 'https://doi.org/10.1186/2041-1480-5-14',
        'provider': 'Zenodo',
    },
    {
        'subject': 'https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge',
        'provider': 'Kaggle',
    },
    {
        'subject': 'https://doi.org/10.5281/zenodo.5541440',
        'provider': 'Zenodo',
    },
    {
        'subject': 'https://doi.org/10.34894/DR3I2A',
        'provider': 'Zenodo',
    },
    {
        'subject': 'https://doi.org/10.1045/november2015-vandesompel',
        'provider': 'Zenodo',
    },
    {
        'subject': 'https://doi.org/10.1016/j.jbi.2008.03.004',
        'provider': 'Zenodo',
    },
    {
        'subject': 'https://doi.org/10.1038/sdata.2016.18',
        'provider': 'Science',
    },
    {
        'subject': 'https://doi.org/10.1016/J.JBI.2019.103292',
        'provider': 'Zenodo',
    },
    {
        'subject': 'https://w3id.org/AmIFAIR',
        'provider': 'FAIR evaluator',
    },
    {
        'subject': 'https://purl.uniprot.org/uniprot/P51587',
        'provider': 'UniProt',
    },
    {
        'subject': 'https://github.com/MaastrichtU-IDS/fair-test',
        'provider': 'GitHub',
    },
]


api_fair_enough = 'https://w3id.org/fair-enough/evaluations'

# TODO: ?
map_metrics_url = {
    'f2-structured-metadata': 'gen2_structured_metadata',
}

eval_collecs = [
    'fair-enough-dataset',
    'fair-evaluator-maturity-indicators'
]

# def test_compare():
def main():
    
    for eval in eval_list:
        print(f"🔎 Evaluating \033[1m{eval['subject']}\033[0m")
        for collec in eval_collecs:
            try:
                r2 = requests.post(f"{api_fair_enough}",
                    json={ 
                        'subject': eval['subject'],
                        'collection': collec,
                    },
                    # timeout=60,
                    # headers={"Accept": "application/ld+json"}
                )
                res = r2.json()
                print(f"\033[1m{collec}\033[0m : \033[95m\033[1m{res['score']}\033[0m/{res['score_max']} in {round(float(res['duration']), 1)}s")
            except Exception as e:
                print(f"🐞 Error while evaluating {eval['subject']} with collection {collec}")
                print(e)


if __name__ == "__main__":
    main()