import io
import re
from urllib.parse import urlparse

import requests
from fair_test import FairTest, FairTestEvaluation


class MetricTest(FairTest):
    metric_path = 'i2-fair-vocabularies-resolve'
    applies_to_principle = 'I2'
    title = 'Metadata uses resolvable FAIR Vocabularies'
    description = """Maturity Indicator to test if the linked data metadata uses terms that resolve to linked (FAIR) data.
One predicate from each hostname is tested, the test is successful if more than 60% of the hostnames resolve to RDF."""
    author = 'https://orcid.org/0000-0002-1501-1082'
    metric_version = '0.1.0'
    topics = ['metadata', 'linked data', 'advanced compliance']
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://doi.org/10.1594/PANGAEA.908011': 1,
        'http://example.com': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):        
        g = eval.retrieve_metadata(eval.subject)
        if not isinstance(g, (list, dict)) and len(g) > 1:
            eval.info(f'Successfully found and parsed RDF metadata available at {eval.subject}. It contains {str(len(g))} triples')
        else:
            eval.failure(f"No RDF metadata found at the subject URL {eval.subject}")
            return eval.response()

        domains_tested = []
        domains_resolving = 0
        for s, p, o in g.triples((None, None, None)):
            result = urlparse(str(p))
            if result.netloc in domains_tested:
                continue
            eval.info(f"Testing URI {str(p)} for the domain {result.netloc}")
            domains_tested.append(result.netloc)
            g_test = eval.retrieve_metadata(str(p))
            if not isinstance(g_test, (list, dict)) and len(g_test) > 0:
                domains_resolving += 1
            else:
                eval.warn(f"URI not resolving to RDF: {str(p)} (we consider the domain {result.netloc} does not resolve to Linked Data)")
            
        eval.info(f"{str(domains_resolving)} URLs resolving, in {len(domains_tested)} domains tested: {', '.join(domains_tested)}")

        # Success if more than 60% of domains resolves
        percent_resolves = domains_resolving / len(domains_tested)
        if percent_resolves >= 0.6:
            eval.success(f"{str(percent_resolves*100)}% of the domains URL used by predicates resolves to RDF")
        else:
            eval.failure(f"Only {str(percent_resolves*100)}% of the domains URL used by predicates resolves to RDF (60% required). Make sure you are using URIs that resolves to RDF as predicates.")

            
        return eval.response()
