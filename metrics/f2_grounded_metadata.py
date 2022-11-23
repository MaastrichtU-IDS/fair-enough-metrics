from fair_test import FairTest, FairTestEvaluation


class MetricTest(FairTest):
    metric_path = 'f2-grounded-metadata'
    applies_to_principle = 'F2'
    title = 'Metadata is grounded and machine-readable'
    description = """Tests whether a machine is able to find 'grounded' metadata. i.e. metadata terms that are in a resolvable namespace, where resolution leads to a definition of the meaning of the term.
Examples include JSON-LD, embedded schema, or any form of RDF.
This assessment will try to extract metadata from the resource URI:
- Extract metadata from the HTML landing page using extruct
- Use HTTP requests with content-negotiation (RDF, JSON-LD)
- Check for Signposting links redirection (aka. Web Linking)"""
    topics = ['metadata', 'linked data']
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
        'https://doi.org/10.1038/sdata.2016.18': 1,
        'https://doi.org/10.1016/J.JBI.2019.103292': 1,
        'https://w3id.org/AmIFAIR': 1,
        'https://purl.uniprot.org/uniprot/P51587': 1,
        # 'https://w3id.org/FAIR_Evaluator/evaluations/6259.json': 1,
        'http://semanticscience.org/resource/metadata': 1,
        'http://example.com': 0,
        # 'https://w3id.org/FAIR_Tests/tests/gen2_structured_metadata': 0,
        # FAIRsharing not consistent, most of the time give 1, but sometimes fails (their server timeout)
        # 'https://doi.org/10.25504/FAIRsharing.jptb1m': 1,
        # 'https://www.proteinatlas.org/ENSG00000084110-HAL': 1,
        # 'https://data.rivm.nl/meta/srv/eng/rdf.metadata.get?uuid=1c0fcd57-1102-4620-9cfa-441e93ea5604&approved=true': 1,
    }


    def evaluate(self, eval: FairTestEvaluation):
        eval.info('Checking if machine readable data (e.g. RDF, JSON-LD) can be retrieved using content-negotiation at ' + eval.subject)

        g = eval.retrieve_metadata(eval.subject)

        if not isinstance(g, (list, dict)) and len(g) > 1:
            eval.success(f'RDF metadata containing {len(g)} triples found at the subject URL provided.')
        else:
            eval.failure(f"No RDF metadata found at the subject URL {eval.subject}")

        return eval.response()
