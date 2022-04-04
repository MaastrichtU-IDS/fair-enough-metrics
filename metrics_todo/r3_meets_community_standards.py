from fair_test import FairTest, FairTestEvaluation
from fastapi.responses import JSONResponse, PlainTextResponse
import os
import requests
from rdflib import URIRef, RDF
from rdflib.namespace import DCTERMS
from pyshex import ShExEvaluator
from pyshex.utils.schema_loader import SchemaLoader


class MetricTest(FairTest):
    metric_path = 'r3-meets-community-standards'
    applies_to_principle = 'R3'
    title = 'Meets Community Standards'
    description = """Such certification services may not exist, but this principle serves to encourage the community 
to create both the standard(s) and the verification services for those standards.  
A potentially useful side-effect of this is that it might provide an opportunity for content-verification
e.g. the certification service provides a hash of the data, which can be used to validate that it has not been edited at a later date.
"""
    metric_version = '0.1.0'
    
    # Test with: https://raw.githubusercontent.com/ejp-rd-vp/resource-metadata-schema/master/data/example-rdf/turtle/patientRegistry.ttl

    def evaluate(self, eval: FairTestEvaluation):

        g = eval.retrieve_metadata(eval.subject)

        # for s, p, o in g.triples((None, DCTERMS.conformsTo, None)):
        #     eval.info(f'Found a value for dcterms:conformsTo: {str(o)}')
        #     res = requests.get(str(o))
        #     conformsToShape = res.text
        #     eval.info(conformsToShape)

        # dct:conformsTo point to URI of JSON schema?
        # People could use it to point to the JSON standard (not ideal)
        # Best: get the schema (e.g. JSON schema)

        # Check also: rdfs:isDefinedBy, rdfs:seeAlso?

        # if isinstance(schema, str):
        #     schema = SchemaLoader().loads(schema)


        shex_failed = False

        if len(g) == 0:
            eval.failure('No RDF found at the subject URL provided.')
            return JSONResponse(eval.toJsonld())

        evaluator = ShExEvaluator(g.serialize(format='turtle'), patientregistry_shex,
            start="http://purl.org/ejp-rd/metadata-model/v1/shex/ejprdResourceShape",
            # start="http://purl.org/ejp-rd/metadata-model/v1/shex/patientRegistryShape",
        )
        
        # Validate all entities with the following types:
        validate_types = [ 
            URIRef('http://purl.org/ejp-rd/vocabulary/PatientRegistry'), 
            URIRef('http://purl.org/ejp-rd/vocabulary/Biobank'), 
            URIRef('http://purl.org/ejp-rd/vocabulary/Guideline'), 
            URIRef('http://www.w3.org/ns/dcat#Dataset')
        ]
        patient_registry_found = False
        for validate_type in validate_types: 
            
            for s, p, o in g.triples((None, RDF.type, validate_type)):
                patient_registry_found = True
                # print('ShEx evaluate focus entity ' + str(s))
                # For specific RDF format: evaluator.evaluate(rdf_format="json-ld")
                for shex_eval in evaluator.evaluate(focus=str(s)):
                    # comment = comment + f"{result.focus}: "
                    if shex_eval.result:
                        if not shex_failed:
                            eval.success(f'ShEx validation passing for type <{validate_type}> with focus <{shex_eval.focus}>')
                        else:
                            eval.info(f'ShEx validation passing for type <{validate_type}> with focus <{shex_eval.focus}>')
                    else:
                        eval.failure(f'ShEx validation failing for type <{validate_type}> with focus <{shex_eval.focus}> due to {shex_eval.reason}')
                        shex_failed = True

        if patient_registry_found == False:
            eval.failure(f'No subject with the type <http://purl.org/ejp-rd/vocabulary/PatientRegistry> found in the RDF metadata available at <{input.subject}>')


        return eval.response()


patientregistry_shex = """PREFIX : <http://purl.org/ejp-rd/metadata-model/v1/shex/>
PREFIX dcat:  <http://www.w3.org/ns/dcat#>
PREFIX dct:   <http://purl.org/dc/terms/>
PREFIX ejp:   <http://purl.org/ejp-rd/vocabulary/>
PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX sio:  <http://semanticscience.org/resource/>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>

:ejprdResourceShape IRI {
    a [ejp:PatientRegistry ejp:Biobank ejp:Guideline dcat:Dataset];
    a [dcat:Resource]*;
    dct:title xsd:string;
    dct:description xsd:string*;
    dcat:theme IRI+;
    foaf:page IRI*
}"""
