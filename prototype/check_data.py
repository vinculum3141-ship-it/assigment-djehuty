#!/usr/bin/env python3
"""
Quick script to check what data exists in the triple store.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../djehuty/src'))

from djehuty.web.config import config
from djehuty.web.database import SparqlInterface

def main():
    print("Checking triple store data...")
    
    db = SparqlInterface()
    db.setup_sparql_endpoint()
    
    # Check institutions
    query = f"""
    PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT DISTINCT ?group_id (COUNT(?dataset) AS ?count)
    WHERE {{
        GRAPH <{config.state_graph}> {{
            ?container rdf:type djht:DatasetContainer ;
                       djht:latest_published_version ?dataset .
            ?dataset rdf:type djht:Dataset ;
                     djht:is_public "true"^^xsd:boolean ;
                     djht:group_id ?group_id .
        }}
    }}
    GROUP BY ?group_id
    ORDER BY DESC(?count)
    LIMIT 10
    """
    
    results = db._SparqlInterface__run_query(query)
    print("\nInstitutions with datasets:")
    for row in results:
        print(f"  Institution {row['group_id']}: {row['count']} datasets")
    
    # Check total datasets (including private)
    query2 = f"""
    PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT (COUNT(?dataset) AS ?total)
    WHERE {{
        GRAPH <{config.state_graph}> {{
            ?dataset rdf:type djht:Dataset .
        }}
    }}
    """
    
    result = db._SparqlInterface__run_query(query2)
    if result:
        print(f"\nTotal datasets (any status): {result[0]['total']}")
    
    # Check faculties
    query3 = f"""
    PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?faculty_name ?group_id
    WHERE {{
        GRAPH <{config.state_graph}> {{
            ?faculty rdf:type djht:Faculty ;
                     djht:faculty_name ?faculty_name ;
                     djht:group_id ?group_id .
        }}
    }}
    """
    
    results = db._SparqlInterface__run_query(query3)
    print("\nFaculties in store:")
    for row in results:
        print(f"  {row['faculty_name'][:50]} (group_id: {row['group_id']})")

if __name__ == "__main__":
    main()
