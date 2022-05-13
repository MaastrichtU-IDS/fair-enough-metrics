from urllib.parse import urlparse

from fair_test import FairTest, FairTestEvaluation
from rdflib import RDF, Literal, URIRef
from rdflib.namespace import DC, DCTERMS, FOAF, OWL, RDFS, SKOS, VOID, XSD


class MetricTest(FairTest):
    metric_path = 'f3-metadata-identifier-in-metadata'
    applies_to_principle = 'F3'
    title = 'Metadata identifier explicitly in metadata'
    description = """Metric to test if the metadata contains the unique identifier to the metadata itself.
Whether the metadata document contains the globally unique and persistent identifier for the digital resource.

Parse the metadata to search for the given digital resource GUID.
If found, retrieve informations about this resource (title, description, date created, etc)"""
    topics = ['metadata']
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://doi.org/10.1594/PANGAEA.908011': 1,
        'https://w3id.org/AmIFAIR': 1,
        'http://example.com': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):

        g = eval.retrieve_metadata(eval.subject)
        if not isinstance(g, (list, dict)) and len(g) > 1:
            eval.info(f'Successfully found and parsed RDF metadata available at {eval.subject}. It contains {str(len(g))} triples')
        else:
            eval.failure(f"No RDF metadata found at the subject URL {eval.subject}")
            return eval.response()

        # FDP specs: https://github.com/FAIRDataTeam/FAIRDataPoint-Spec/blob/master/spec.md
        # Stats for KG: https://www.w3.org/TR/hcls-dataset

        eval.info(f"Checking RDF metadata to find links to all the alternative identifiers: <{'>, <'.join(eval.data['alternative_uris'])}>")
        subject_uri = eval.extract_metadata_subject(g, eval.data['alternative_uris'])

        if subject_uri:
            if 'properties' in eval.data['identifier_in_metadata'].keys():
                eval.info('Found properties/links for the subject URI in the metadata: ' 
                    + ', '.join(list(eval.data['identifier_in_metadata']['properties'].keys()))
                )
            if 'linked_to' in eval.data['identifier_in_metadata'].keys():
                eval.info('Found properties/links for the subject URI in the metadata: ' 
                    + ', '.join(list(eval.data['identifier_in_metadata']['linked_to'].keys()))
                )
            eval.success(f"Found the metadata identifier in the metadata: {str(subject_uri)}")

            # Try to extract some metadata from the parsed RDF
            title_preds = [ 
                DC.title, DCTERMS.title, 
                RDFS.label, 
                URIRef('https://schema.org/name'),
                URIRef('https://schema.org/headline'),
                URIRef('http://ogp.me/ns#title'),    
            ]
            # titles = eval.extract_prop(g, title_preds, eval.data['alternative_uris'])
            titles = [str(s) for s in eval.extract_prop(g, title_preds, subject_uri)] 
            if len(titles) > 0:
                eval.log(f"Found titles: {' ,'.join(titles)}")
                eval.data['title'] = titles


            description_preds = [ 
                DCTERMS.description, 
                URIRef('http://schema.org/description'), 
                URIRef('https://schema.org/description'),
                URIRef('http://ogp.me/ns#description'),    
            ]
            descriptions = [str(s) for s in eval.extract_prop(g, description_preds, subject_uri)] 
            if len(descriptions) > 0:
                eval.log(f"Found descriptions: {' ,'.join(descriptions)}")
                eval.data['description'] = descriptions

            date_created_preds = [ 
                DCTERMS.created, 
                URIRef('http://schema.org/dateCreated'), 
                URIRef('http://schema.org/datePublished')
            ]
            dates = [str(s) for s in eval.extract_prop(g, date_created_preds, subject_uri)] 
            if len(dates) > 0:
                eval.log(f"Found created date: {' ,'.join(dates)}")
                eval.data['created'] = dates
        
        else: 
            eval.failure(f'Could not find links to the metadata identifier {str(subject_uri)} in the RDF metadata')

        return eval.response()
