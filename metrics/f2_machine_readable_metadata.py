from fair_test import FairTest, FairTestEvaluation
import requests


class MetricTest(FairTest):
    metric_path = 'f2-machine-readable-metadata'
    applies_to_principle = 'F2'
    title = 'Metadata is machine-readable'
    description = """This assessment will try to extract metadata from the resource URI:
- Search for structured metadata at the resource URI. 
- Use HTTP requests with content-negotiation (RDF, JSON-LD, JSON), 
- Extract metadata from the HTML landing page using extruct"""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test={
        'https://doi.org/10.1594/PANGAEA.908011': 1,
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://doi.org/10.1186/2041-1480-5-14': 1,
        'https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge': 1,
        'https://doi.org/10.5281/zenodo.5541440': 1,
        'https://doi.org/10.34894/DR3I2A': 1,
        'https://doi.org/10.1045/november2015-vandesompel': 1,
        'https://doi.org/10.1016/j.jbi.2008.03.004': 1,
        'https://doi.org/10.25504/FAIRsharing.jptb1m': 1,
        'https://doi.org/10.1038/sdata.2016.18': 1,
        'https://doi.org/10.1016/J.JBI.2019.103292': 1,
        'https://w3id.org/AmIFAIR': 1,
        'https://github.com/MaastrichtU-IDS/fair-test': 0,
        # 'https://www.proteinatlas.org/ENSG00000084110-HAL': 1,
        # 'https://data.rivm.nl/meta/srv/eng/rdf.metadata.get?uuid=1c0fcd57-1102-4620-9cfa-441e93ea5604&approved=true': 1,
    }


    def evaluate(self, eval: FairTestEvaluation):
        eval.info('Checking if machine readable data (e.g. RDF, JSON-LD) can be retrieved using content-negotiation at ' + eval.subject)
        g = eval.retrieve_rdf(eval.subject)
        if len(g) > 0:
            eval.success(f'RDF metadata containing {len(g)} triples found at the subject URL provided.')
        else:
            eval.failure('No RDF found at the subject URL provided.')
        
        return eval.response()
