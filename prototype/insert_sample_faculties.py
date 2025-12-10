#!/usr/bin/env python3
"""
Prototype Script: Insert Sample Faculty Data

This script demonstrates Phase 1 of the faculty statistics prototype by:
1. Inserting sample faculty entities into the RDF store
2. Linking existing datasets to these faculties via group_id

This is a proof-of-concept showing how the faculty extension pattern works.
"""

import sys
import os

# Add djehuty to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../djehuty/src'))

from rdflib import Graph, Literal, Namespace, RDF, XSD
from djehuty.web.config import config
from djehuty.web.database import SparqlInterface
from djehuty.utils import rdf

# Sample faculties to insert
SAMPLE_FACULTIES = [
    {
        "id": 285860001,
        "group_id": 285860001,
        "name": "Faculty of Electrical Engineering, Mathematics and Computer Science",
        "short_name": "EEMCS",
        "code": "EEMCS",
        "institution_id": 28586
    },
    {
        "id": 285860002,
        "group_id": 285860002,
        "name": "Faculty of Aerospace Engineering",
        "short_name": "AE",
        "code": "AE",
        "institution_id": 28586
    },
    {
        "id": 285860003,
        "group_id": 285860003,
        "name": "Faculty of Applied Sciences",
        "short_name": "AS",
        "code": "AS",
        "institution_id": 28586
    },
]

def insert_faculty_entities(db):
    """
    Insert sample faculty entities into the triple store.
    
    This demonstrates extending the RDF schema with new Faculty entities.
    Uses the same pattern as InstitutionGroup.
    """
    print("\n=== Inserting Faculty Entities ===")
    
    for faculty in SAMPLE_FACULTIES:
        graph = Graph()
        
        # Create unique faculty URI
        faculty_uri = rdf.ROW[f"faculty_{faculty['id']}"]
        
        # Add faculty triples
        rdf.add(graph, faculty_uri, RDF.type, rdf.DJHT["Faculty"], "uri")
        rdf.add(graph, faculty_uri, rdf.DJHT["id"], faculty['id'], XSD.integer)
        rdf.add(graph, faculty_uri, rdf.DJHT["group_id"], faculty['group_id'], XSD.integer)
        rdf.add(graph, faculty_uri, rdf.DJHT["faculty_name"], faculty['name'], XSD.string)
        rdf.add(graph, faculty_uri, rdf.DJHT["faculty_short_name"], faculty['short_name'], XSD.string)
        rdf.add(graph, faculty_uri, rdf.DJHT["faculty_code"], faculty['code'], XSD.string)
        rdf.add(graph, faculty_uri, rdf.DJHT["institution_id"], faculty['institution_id'], XSD.integer)
        
        # Insert into triple store
        if db.add_triples_from_graph(graph):
            print(f"✅ Inserted faculty: {faculty['name']} (ID: {faculty['id']})")
        else:
            print(f"❌ Failed to insert faculty: {faculty['name']}")
    
    print("\n✅ Faculty entities inserted successfully!")


def link_datasets_to_faculties(db):
    """
    Link sample datasets to faculties by updating their group_id.
    
    This demonstrates the extension pattern: datasets already have group_id
    (for institutions), we're just using finer-grained faculty IDs.
    """
    print("\n=== Linking Datasets to Faculties ===")
    
    # Query to find datasets with TU Delft institution (28586)
    query = """
    PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT DISTINCT ?dataset ?container ?title
    WHERE {
        GRAPH <%(state_graph)s> {
            ?container rdf:type djht:DatasetContainer ;
                       djht:latest_published_version ?dataset .
            ?dataset rdf:type djht:Dataset ;
                     djht:is_public "true"^^xsd:boolean ;
                     djht:group_id 28586 .
            OPTIONAL { ?dataset djht:title ?title . }
        }
    }
    LIMIT 10
    """ % {"state_graph": config.state_graph}
    
    try:
        results = db._SparqlInterface__run_query(query)
        
        if not results:
            print("⚠️  No datasets found with institution_id 28586")
            return
        
        print(f"Found {len(results)} TU Delft datasets to link to faculties\n")
        
        # Distribute datasets across faculties (simple round-robin for demo)
        faculty_ids = [f['group_id'] for f in SAMPLE_FACULTIES]
        
        for idx, row in enumerate(results):
            dataset_uri = row['dataset']
            title = row.get('title', 'Untitled')
            faculty_id = faculty_ids[idx % len(faculty_ids)]
            faculty = SAMPLE_FACULTIES[idx % len(SAMPLE_FACULTIES)]
            
            # Update query to change group_id to faculty group_id
            update_query = """
            PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            
            WITH <%(state_graph)s>
            DELETE { <%(dataset)s> djht:group_id ?old_group_id . }
            INSERT { <%(dataset)s> djht:group_id %(faculty_id)s . }
            WHERE { <%(dataset)s> djht:group_id ?old_group_id . }
            """ % {
                "state_graph": config.state_graph,
                "dataset": dataset_uri,
                "faculty_id": faculty_id
            }
            
            success = db._SparqlInterface__run_query(update_query)
            if success:
                print(f"✅ Linked dataset to {faculty['short_name']}: {title[:60]}")
            else:
                print(f"❌ Failed to link dataset: {title[:60]}")
        
        print(f"\n✅ Successfully linked {len(results)} datasets to faculties!")
        
    except Exception as e:
        print(f"❌ Error linking datasets: {e}")


def verify_faculty_data(db):
    """
    Verify that faculties were inserted and datasets linked correctly.
    """
    print("\n=== Verification ===")
    
    # Count faculties
    faculty_query = """
    PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT (COUNT(?faculty) AS ?count)
    WHERE {
        GRAPH <%(state_graph)s> {
            ?faculty rdf:type djht:Faculty .
        }
    }
    """ % {"state_graph": config.state_graph}
    
    result = db._SparqlInterface__run_query(faculty_query)
    if result:
        faculty_count = result[0].get('count', 0)
        print(f"✅ Faculty entities in store: {faculty_count}")
    
    # Count datasets per faculty
    dataset_query = """
    PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?faculty_id ?faculty_name (COUNT(?dataset) AS ?dataset_count)
    WHERE {
        GRAPH <%(state_graph)s> {
            ?faculty rdf:type djht:Faculty ;
                     djht:group_id ?faculty_id ;
                     djht:faculty_short_name ?faculty_name .
            
            ?container rdf:type djht:DatasetContainer ;
                       djht:latest_published_version ?dataset .
            ?dataset rdf:type djht:Dataset ;
                     djht:is_public "true"^^xsd:boolean ;
                     djht:group_id ?faculty_id .
        }
    }
    GROUP BY ?faculty_id ?faculty_name
    ORDER BY DESC(?dataset_count)
    """ % {"state_graph": config.state_graph}
    
    results = db._SparqlInterface__run_query(dataset_query)
    if results:
        print("\n📊 Datasets per Faculty:")
        for row in results:
            print(f"   {row['faculty_name']}: {row['dataset_count']} datasets")
    else:
        print("⚠️  No datasets linked to faculties yet")


def main():
    """Main execution function."""
    print("=" * 70)
    print("PROTOTYPE: Faculty Statistics - Phase 1 Data Model")
    print("=" * 70)
    
    # Load configuration (simplified - use environment variable or default)
    config_file = os.environ.get('DJEHUTY_CONFIG', '../djehuty/djehuty.xml')
    config_file = os.path.join(os.path.dirname(__file__), config_file)
    
    if not os.path.exists(config_file):
        print(f"❌ Configuration file not found: {config_file}")
        print("Please set DJEHUTY_CONFIG environment variable or place djehuty.xml in ../djehuty/")
        return 1
    
    print(f"\n📄 Using configuration: {config_file}")
    print(f"📊 SPARQL endpoint: {config.endpoint}")
    print(f"🗂️  State graph: {config.state_graph}")
    
    # Initialize database connection
    print("\n🔌 Connecting to SPARQL endpoint...")
    db = SparqlInterface()
    db.setup_sparql_endpoint()
    
    if not db.sparql_is_up:
        print("❌ Failed to connect to SPARQL endpoint")
        return 1
    
    print("✅ Connected successfully!")
    
    # Execute prototype steps
    try:
        insert_faculty_entities(db)
        link_datasets_to_faculties(db)
        verify_faculty_data(db)
        
        print("\n" + "=" * 70)
        print("✅ PROTOTYPE PHASE 1 COMPLETE!")
        print("=" * 70)
        print("\nNext steps:")
        print("  1. Implement faculty_statistics() backend method")
        print("  2. Create API endpoint: /v2/stats/faculty")
        print("  3. Build dashboard visualization")
        print("\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
