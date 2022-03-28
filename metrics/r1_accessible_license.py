from fair_test import FairTest, FairTestEvaluation
import requests
from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDFS, XSD, DC, DCTERMS, VOID, OWL, SKOS, FOAF


class MetricTest(FairTest):
    metric_path = 'r1-accessible-license'
    applies_to_principle = 'R1'
    title = 'Check accessible Usage License'
    description = """The existence of a license document, for BOTH (independently) the data and its associated metadata, and the ability to retrieve those documents
Resolve the licenses IRI"""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'


    def evaluate(self, eval: FairTestEvaluation):        
        found_license = False
        # Issue with extracting license from some URIs, such as https://www.uniprot.org/uniprot/P51587
        # Getting a URI that is not really the license as output
        g = eval.retrieve_rdf(eval.subject)
        if len(g) == 0:
            eval.failure('No RDF found at the subject URL provided.')
            return eval.response()
        else:
            eval.info(f'RDF metadata containing {len(g)} triples found at the subject URL provided.')

        # TODO: check DataCite too
        license_preds = [
            DCTERMS.license, 
            URIRef('https://schema.org/license'), 
            URIRef('http://www.w3.org/1999/xhtml/vocab#license')
        ]

        eval.info(f"Checking for license in RDF metadata using predicates: {str(license_preds)}")
        licenses = eval.extract_prop(g, license_preds, eval.data['alternative_uris'])
        if len(licenses) > 0:
            eval.success(f"Found licenses: {' ,'.join(licenses)}")
            eval.data['license'] = licenses
        else:
            eval.failure("Could not find data for the metadata. Searched for the following predicates: " + ', '.join(license_uris))

        if 'license' in eval.data.keys():
            for license in eval.data['license']:
                eval.info(f"Check if license {eval.data['license']} is approved by the Open Source Initiative, in the SPDX licenses list")
                # https://github.com/vemonet/fuji/blob/master/fuji_server/helper/preprocessor.py#L229
                spdx_licenses_url = 'https://raw.github.com/spdx/license-list-data/master/json/licenses.json'
                spdx_licenses = requests.get(spdx_licenses_url).json()['licenses']
                for license in spdx_licenses:
                    if eval.data['license'] in license['seeAlso']:
                        if license['isOsiApproved'] == True:
                            eval.bonus('License approved by the Open Source Initiative (' + str(eval.data['license']) + ')')

        return eval.response()


    test_test={
        'https://doi.org/10.1594/PANGAEA.908011': 1,
    }