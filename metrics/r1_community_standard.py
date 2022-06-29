import pyshacl
from fair_test import FairTest, FairTestEvaluation
from rdflib import RDF, Literal, URIRef

# from rdflib.namespace import DC, DCTERMS, FOAF, OWL, RDFS, SKOS, VOID, XSD


class MetricTest(FairTest):
    metric_path = 'r1-community-standards'
    applies_to_principle = 'R1'
    title = 'Conforms to community standards'
    description = """Check metadata schema conforms to a specific SHACL shape."""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test = {
        'https://raw.githubusercontent.com/MaastrichtU-IDS/fair-enough-metrics/main/resources/metadata_sample_success.ttl': 1,
        'https://raw.githubusercontent.com/MaastrichtU-IDS/fair-enough-metrics/main/resources/metadata_sample_fail.ttl': 0,
    }
    


    def validate(self, data_graph, shapes_graph):
        results = pyshacl.validate(
            data_graph,
            shacl_graph=shapes_graph,
            data_graph_format="json-ld",
            shacl_graph_format="ttl",
            inference="rdfs",
            debug=True,
            serialize_report_graph="ttl",
        )
        conforms, report_graph, report_text = results
        return conforms


    def evaluate(self, eval: FairTestEvaluation):

        g = eval.retrieve_metadata(eval.subject)

        if len(g) == 0:
            eval.failure('No RDF found at the subject URL provided.')
            return eval.response()
        else:
            eval.info(f'RDF metadata containing {len(g)} triples found at the subject URL provided.')

        validated = False

        schema_pred = 'http://purl.org/dc/terms/conformsTo'
        eval.info(f"Checking for SHACL shape in RDF metadata using predicate {str(schema_pred)}")

        for s, p, o in g.triples((None, URIRef(schema_pred), None)):
            shacl_g = eval.retrieve_metadata(str(o))
            validated = self.validate(g, shacl_g)
            break
        

        if validated:
            eval.success('Metadata is validated by the Schema')

        return eval.response()
