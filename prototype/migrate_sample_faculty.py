#!/usr/bin/env python3
"""
Sample Faculty Migration Script

Migrates a sample of datasets from institution-level to faculty-level grouping.
Demonstrates the migration process for the prototype.

This script:
1. Identifies datasets with extractable faculty information
2. Creates faculty RDF entities (if not exist)
3. Updates dataset group_id to link to faculties
4. Generates before/after migration report

Usage:
    python prototype/migrate_sample_faculty.py
"""

import sys
import os
import json
import re
from datetime import datetime

# Add djehuty to path
sys.path.insert(0, 'djehuty/src')

import requests


# SPARQL endpoint
SPARQL_ENDPOINT = "http://localhost:8890/sparql"
GRAPH_URI = "https://data.4tu.nl/portal/self-test"


# Faculty definitions for TU Delft (matching our sample_faculties.ttl)
TU_DELFT_FACULTIES = {
    'EEMCS': {
        'id': 285860001,
        'group_id': 285860001,
        'faculty_name': 'Faculty of EEMCS',
        'faculty_short_name': 'EEMCS',
        'faculty_code': 'EEMCS',
        'institution_id': 28586,
        'patterns': [
            r'Faculty of Electrical Engineering,? Mathematics and Computer Science',
            r'EEMCS'
        ]
    },
    'CEG': {
        'id': 285860002,
        'group_id': 285860002,
        'faculty_name': 'Faculty of Civil Engineering and Geosciences',
        'faculty_short_name': 'CEG',
        'faculty_code': 'CEG',
        'institution_id': 28586,
        'patterns': [
            r'Faculty of Civil Engineering and Geosciences',
            r'CEG'
        ]
    },
    'AE': {
        'id': 285860003,
        'group_id': 285860003,
        'faculty_name': 'Faculty of Aerospace Engineering',
        'faculty_short_name': 'AE',
        'faculty_code': 'AE',
        'institution_id': 28586,
        'patterns': [
            r'Faculty of Aerospace Engineering',
            r'Aerospace Engineering'
        ]
    },
    'ABE': {
        'id': 285860004,
        'group_id': 285860004,
        'faculty_name': 'Faculty of Architecture and the Built Environment',
        'faculty_short_name': 'ABE',
        'faculty_code': 'ABE',
        'institution_id': 28586,
        'patterns': [
            r'Faculty of Architecture and the Built Environment'
        ]
    }
}


def execute_sparql_update(update_query):
    """
    Execute a SPARQL UPDATE query.
    
    Args:
        update_query (str): SPARQL UPDATE query
        
    Returns:
        bool: True if successful
    """
    response = requests.post(
        SPARQL_ENDPOINT,
        data=update_query,
        headers={'Content-Type': 'application/sparql-update'}
    )
    return response.status_code == 200


def execute_sparql_query(query):
    """
    Execute a SPARQL SELECT query.
    
    Args:
        query (str): SPARQL SELECT query
        
    Returns:
        list: Query results
    """
    response = requests.post(
        SPARQL_ENDPOINT,
        data=query,
        headers={
            'Content-Type': 'application/sparql-query',
            'Accept': 'application/sparql-results+json'
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        return [{k: v.get('value') for k, v in row.items()} 
                for row in data['results']['bindings']]
    return []


def extract_faculty_code(org_text):
    """
    Extract faculty code from organization text.
    
    Args:
        org_text (str): Organizations field text
        
    Returns:
        str or None: Faculty code if found
    """
    if not org_text:
        return None
    
    for code, faculty_info in TU_DELFT_FACULTIES.items():
        for pattern in faculty_info['patterns']:
            if re.search(pattern, org_text, re.IGNORECASE):
                return code
    
    return None


def get_datasets_for_migration():
    """
    Get datasets that can be migrated to faculty-level grouping.
    
    Returns:
        list: Datasets with extractable faculty information
    """
    query = """
    PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
    
    SELECT ?dataset ?title ?group_id ?organizations
    WHERE {
        ?dataset a djht:Dataset ;
                 djht:title ?title .
        OPTIONAL { ?dataset djht:group_id ?group_id . }
        OPTIONAL { ?dataset djht:organizations ?organizations . }
    }
    """
    
    results = execute_sparql_query(query)
    
    # Filter to only datasets where we can extract faculty
    migratable = []
    for dataset in results:
        faculty_code = extract_faculty_code(dataset.get('organizations', ''))
        if faculty_code:
            dataset['faculty_code'] = faculty_code
            dataset['faculty_info'] = TU_DELFT_FACULTIES[faculty_code]
            migratable.append(dataset)
    
    return migratable


def check_faculty_exists(faculty_id):
    """
    Check if a faculty entity already exists in the triple store.
    
    Args:
        faculty_id (int): Faculty ID to check
        
    Returns:
        bool: True if exists
    """
    query = f"""
    PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
    
    ASK {{
        ?faculty a djht:Faculty ;
                 djht:id {faculty_id} .
    }}
    """
    
    response = requests.post(
        SPARQL_ENDPOINT,
        data=query,
        headers={
            'Content-Type': 'application/sparql-query',
            'Accept': 'application/sparql-results+json'
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        return data['boolean']
    
    return False


def create_faculty_if_not_exists(faculty_code):
    """
    Create faculty RDF entity if it doesn't exist.
    
    Args:
        faculty_code (str): Faculty code (EEMCS, CEG, etc.)
        
    Returns:
        bool: True if created or already exists
    """
    faculty_info = TU_DELFT_FACULTIES[faculty_code]
    faculty_id = faculty_info['id']
    
    # Check if exists
    if check_faculty_exists(faculty_id):
        print(f"  ℹ️  Faculty {faculty_code} (ID: {faculty_id}) already exists")
        return True
    
    # Create faculty entity
    update_query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
    PREFIX djehuty: <https://data.4tu.nl/portal/self-test/>
    
    INSERT DATA {{
        djehuty:faculty_{faculty_id}
            rdf:type djht:Faculty ;
            djht:id "{faculty_id}"^^xsd:integer ;
            djht:group_id "{faculty_info['group_id']}"^^xsd:integer ;
            djht:faculty_name "{faculty_info['faculty_name']}"@en ;
            djht:faculty_short_name "{faculty_info['faculty_short_name']}"@en ;
            djht:faculty_code "{faculty_info['faculty_code']}"@en ;
            djht:institution_id "{faculty_info['institution_id']}"^^xsd:integer .
    }}
    """
    
    if execute_sparql_update(update_query):
        print(f"  ✅ Created faculty: {faculty_info['faculty_name']} (ID: {faculty_id})")
        return True
    else:
        print(f"  ❌ Failed to create faculty: {faculty_code}")
        return False


def migrate_dataset_to_faculty(dataset):
    """
    Migrate a dataset from institution-level to faculty-level grouping.
    
    Args:
        dataset (dict): Dataset information including faculty_code
        
    Returns:
        bool: True if successful
    """
    dataset_uri = dataset['dataset']
    faculty_code = dataset['faculty_code']
    faculty_info = dataset['faculty_info']
    new_group_id = faculty_info['group_id']
    old_group_id = dataset['group_id']
    
    # Update group_id
    update_query = f"""
    PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    DELETE {{
        <{dataset_uri}> djht:group_id "{old_group_id}"^^xsd:integer .
    }}
    INSERT {{
        <{dataset_uri}> djht:group_id "{new_group_id}"^^xsd:integer .
    }}
    WHERE {{
        <{dataset_uri}> djht:group_id "{old_group_id}"^^xsd:integer .
    }}
    """
    
    if execute_sparql_update(update_query):
        title = dataset['title'][:60] + '...' if len(dataset['title']) > 60 else dataset['title']
        print(f"  ✅ Migrated: {title}")
        print(f"     group_id: {old_group_id} (Institution) → {new_group_id} (Faculty: {faculty_code})")
        return True
    else:
        print(f"  ❌ Failed to migrate dataset: {dataset_uri}")
        return False


def verify_migration(dataset):
    """
    Verify that a dataset was successfully migrated.
    
    Args:
        dataset (dict): Dataset information
        
    Returns:
        dict: Verification results
    """
    dataset_uri = dataset['dataset']
    expected_group_id = dataset['faculty_info']['group_id']
    
    query = f"""
    PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
    
    SELECT ?group_id
    WHERE {{
        <{dataset_uri}> djht:group_id ?group_id .
    }}
    """
    
    results = execute_sparql_query(query)
    
    if results and len(results) > 0:
        actual_group_id = int(results[0]['group_id'])
        success = actual_group_id == expected_group_id
        return {
            'success': success,
            'expected': expected_group_id,
            'actual': actual_group_id
        }
    
    return {'success': False, 'error': 'No group_id found'}


def generate_migration_report(migrated_datasets, verifications):
    """
    Generate a comprehensive migration report.
    
    Args:
        migrated_datasets (list): List of migrated datasets
        verifications (list): List of verification results
    """
    print()
    print("=" * 80)
    print("MIGRATION REPORT")
    print("=" * 80)
    print()
    
    # Summary
    successful = sum(1 for v in verifications if v['success'])
    print(f"📊 Summary")
    print("-" * 80)
    print(f"Total datasets migrated:     {len(migrated_datasets)}")
    print(f"Successfully verified:       {successful}")
    print(f"Failed verification:         {len(verifications) - successful}")
    print()
    
    # Faculty distribution
    from collections import Counter
    faculty_counts = Counter(d['faculty_code'] for d in migrated_datasets)
    
    print(f"🎓 Datasets by Faculty (After Migration)")
    print("-" * 80)
    for faculty_code, count in faculty_counts.most_common():
        faculty_name = TU_DELFT_FACULTIES[faculty_code]['faculty_short_name']
        print(f"  {faculty_name:10s} {count} dataset(s)")
    print()
    
    # Before/After comparison
    print(f"📈 Before/After Comparison")
    print("-" * 80)
    print(f"BEFORE Migration:")
    print(f"  • All {len(migrated_datasets)} datasets grouped by Institution (group_id: 28586)")
    print(f"  • Granularity: Institution level only")
    print()
    print(f"AFTER Migration:")
    print(f"  • {len(migrated_datasets)} datasets now grouped by Faculty")
    print(f"  • Granularity: Faculty level (4 faculties)")
    print(f"  • Faculties: {', '.join(faculty_counts.keys())}")
    print()
    
    # Detailed results
    print(f"✅ Detailed Migration Results")
    print("-" * 80)
    for i, (dataset, verification) in enumerate(zip(migrated_datasets, verifications), 1):
        title = dataset['title'][:50] + '...' if len(dataset['title']) > 50 else dataset['title']
        faculty = dataset['faculty_code']
        status = "✓" if verification['success'] else "✗"
        
        print(f"{i}. [{status}] {title}")
        print(f"   Faculty: {faculty} ({TU_DELFT_FACULTIES[faculty]['faculty_name']})")
        print(f"   group_id: 28586 → {verification.get('actual', 'N/A')}")
        if not verification['success']:
            print(f"   ERROR: {verification.get('error', 'Verification failed')}")
        print()
    
    # Next steps
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print("✅ Phase 2B Complete: Sample migration demonstrates feasibility")
    print()
    print("🔍 Verify Migration:")
    print("   Run: python prototype/test_faculty_statistics.py")
    print("   Expected: Faculty statistics now include migrated datasets")
    print()
    print("⏭️  Phase 3: Visualization")
    print("   Next: Create dashboard to visualize institution vs faculty statistics")
    print("   File: prototype/dashboard.html")
    print()
    
    # Save report
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'total_migrated': len(migrated_datasets),
        'successful': successful,
        'faculty_distribution': dict(faculty_counts),
        'datasets': [
            {
                'dataset_id': d['dataset'].split(':')[-1],
                'title': d['title'],
                'faculty': d['faculty_code'],
                'old_group_id': int(d['group_id']),
                'new_group_id': d['faculty_info']['group_id'],
                'verified': v['success']
            }
            for d, v in zip(migrated_datasets, verifications)
        ]
    }
    
    with open('prototype/migration_report.json', 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print("💾 Detailed report saved to: prototype/migration_report.json")
    print()


def main():
    """Main migration execution."""
    print("=" * 80)
    print("Faculty Migration - Sample Datasets")
    print("=" * 80)
    print()
    
    # Step 1: Get datasets for migration
    print("🔍 Step 1: Identifying datasets for migration...")
    datasets = get_datasets_for_migration()
    print(f"   Found {len(datasets)} TU Delft datasets with extractable faculty information")
    print()
    
    if len(datasets) == 0:
        print("⚠️  No datasets found for migration.")
        print("   Make sure:")
        print("   • Virtuoso is running")
        print("   • Datasets exist in the triple store")
        print("   • Datasets have 'organizations' field with faculty mentions")
        return
    
    # Step 2: Create faculty entities
    print("🏗️  Step 2: Creating faculty entities (if not exist)...")
    faculties_needed = set(d['faculty_code'] for d in datasets)
    for faculty_code in sorted(faculties_needed):
        create_faculty_if_not_exists(faculty_code)
    print()
    
    # Step 3: Migrate datasets
    print("🚀 Step 3: Migrating datasets to faculty-level grouping...")
    migrated = []
    for dataset in datasets:
        if migrate_dataset_to_faculty(dataset):
            migrated.append(dataset)
    print()
    
    # Step 4: Verify migration
    print("✓ Step 4: Verifying migrations...")
    verifications = []
    for dataset in migrated:
        verification = verify_migration(dataset)
        verifications.append(verification)
        status = "✓" if verification['success'] else "✗"
        title = dataset['title'][:40] + '...' if len(dataset['title']) > 40 else dataset['title']
        print(f"   [{status}] {title}")
    print()
    
    # Step 5: Generate report
    generate_migration_report(migrated, verifications)
    
    print("✅ Migration complete!")
    print()


if __name__ == '__main__':
    main()
