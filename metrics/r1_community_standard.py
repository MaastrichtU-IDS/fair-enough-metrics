import pyshacl
import requests
from fair_test import FairTest, FairTestEvaluation
from rdflib import RDF, Literal, URIRef
from rdflib.namespace import DC, DCTERMS, FOAF, OWL, RDFS, SKOS, VOID, XSD


class MetricTest(FairTest):
    metric_path = 'r1-community-standards'
    applies_to_principle = 'R1'
    title = 'Conforms to community standards'
    description = """Check metadata schema conforms to a specific SHACL shape."""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test = {
        # 'https://raw.githubusercontent.com/MaastrichtU-IDS/fair-enough-metrics/main/resources/metadata_sample.ttl': 1,
        # 'https://doi.org/10.1594/PANGAEA.908011': 1,
        # 'https://w3id.org/AmIFAIR': 1,
        # 'http://example.com': 0,
    }
    


    def validate(data_graph, shapes_graph):
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

        print("conforms", conforms)
        return conforms


    def evaluate(self, eval: FairTestEvaluation):
        # found_license = False
        # Issue with extracting license from some URIs, such as https://www.uniprot.org/uniprot/P51587
        # Getting a URI that is not really the license as output

        g = eval.retrieve_metadata(eval.subject)

        if len(g) == 0:
            eval.failure('No RDF found at the subject URL provided.')
            return eval.response()
        else:
            eval.info(f'RDF metadata containing {len(g)} triples found at the subject URL provided.')

        # eval.info(f"Checking RDF metadata to find links to all the alternative identifiers: <{'>, <'.join(eval.data['alternative_uris'])}>")
        # subject_uri = eval.extract_metadata_subject(g, eval.data['alternative_uris'])

        # TODO: check DataCite too?
        schema_preds = [
            'http://purl.org/dc/terms/conformsTo'
        ]
        # graph_data_preds = [
        #     'http://www.w3.org/ns/dcat#distribution',
        #     'https://schema.org/distribution'
        # ]

        validated = False

        eval.info(f"Checking for schema in RDF metadata using predicates: {str(schema_preds)}")
        for s, p, o in g.triples((None, URIRef('http://purl.org/dc/terms/conformsTo'), None)):
            shacl_g = eval.retrieve_metadata(str(o))

            eval.info(f"SHACL graph contains {len(shacl_g)} triples")
            
            validated = self.validate(g, shacl_g)
            break
        

        if validated:
            eval.success('KG data is validated by the Schema')


        # schemas = eval.extract_prop(g, schema_preds, subject_uri)
        # data_graph = eval.extract_prop(g, graph_data_preds, subject_uri)
        # if len(schemas) > 0:
        #     eval.success(f"Found schema : {' ,'.join(schemas)}")
        #     eval.data['schema'] = schemas
        # else:
        #     eval.failure(
        #         f"Could not find a schema in the metadata. Searched for the following predicates: {str(schema)}")

        # if 'schema' in eval.data.keys():
        #     for schema_found in eval.data['schema']:
        #         eval.info(
        #             f"Check if KG is validate by the schema {eval.data['schema']}")
        #         # https://github.com/vemonet/fuji/blob/master/fuji_server/helper/preprocessor.py#L229
        #         if self.validate(data_graph, schema_found):
        #             eval.bonus('KG data is validated by the Schema (' +
        #                        str(eval.data['schema']) + ')')

        return eval.response()