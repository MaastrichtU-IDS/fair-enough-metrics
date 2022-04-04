from fair_test import FairTest, FairTestEvaluation
from urllib.parse import urlparse
from rdflib.namespace import RDFS, XSD, DC, DCTERMS, VOID, OWL, SKOS


class MetricTest(FairTest):
    metric_path = 'a1-data-authorization'
    applies_to_principle = 'A1.2'
    title = 'Data authentication and authorization'
    description = """Test a discovered data GUID for the ability to implement authentication and authorization in its resolution protocol. Accepts URLs. 
It also searches the metadata for the Dublin Core 'accessRights' property, which may point to a document describing the data access process. Recognition of other identifiers will be added upon request by the community."""
    topics = ['data']
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://doi.org/10.1594/PANGAEA.908011': 1,
        'http://example.com': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):
        # TODO: use https://pythonhosted.org/IDUtils

        g = eval.retrieve_metadata(eval.subject)
        if not isinstance(g, (list, dict)) and len(g) > 0:
            eval.info(f'Successfully found and parsed RDF metadata. It contains {str(len(g))} triples')
        else:
            eval.failure(f"No RDF metadata found at the subject URL {eval.subject}")
            return eval.response()
        
        subject_uri = eval.extract_metadata_subject(g, eval.data['alternative_uris'])
        # Extract the download URL of the data from the RDF metadata
        data_res = eval.extract_data_subject(g, subject_uri)
        if len(eval.data['content_url']) < 1:
            eval.failure("Could not find data URI in the metadata.")


        found_access_rights = False
        access_rights_preds = [ DCTERMS.accessRights ]

        for data_uri in eval.data['content_url']:
            eval.info('Checking if the data URI ' + data_uri + ' is a valid URL using urllib.urlparse')
            result = urlparse(data_uri)
            if result.scheme and result.netloc:
                eval.success('Validated the data URI ' + data_uri + ' is a URL')
            else:
                eval.failure('Could not validate the data URI ' + data_uri + ' is a URL')    


            eval.info('Authorization: checking for dct:accessRights in metadata')
            for pred in access_rights_preds:
                for s, p, accessRights in g.triples((data_uri,  pred, None)):
                    eval.info(f'Found authorization informations with dcterms:accessRights: {str(accessRights)}')
                    # eval.data['accessRights'] = str(accessRights)
                    found_access_rights = True

        if found_access_rights:
            eval.success(f'Found dcterms:accessRights in metadata: {str(accessRights)}')
        else:
            eval.warn(f"Could not find dcterms:accessRights information in metadata. Make sure your metadata contains informations about access rights using one of those predicates: {', '.join(access_rights_preds)}")


        return eval.response()
