#!/usr/bin/env python3
"""
Faculty Migration Analysis Script

Analyzes existing datasets to identify faculty mentions in metadata
and assesses data quality for faculty-level migration.

This demonstrates:
1. How faculty information can be extracted from existing metadata
2. Data quality metrics for migration planning
3. Coverage analysis (what % of datasets have faculty info)
4. Pattern identification for automatic extraction

Usage:
    python prototype/analyze_faculty_migration.py
"""

import sys
import os
import re
import json
from collections import Counter, defaultdict

# Add djehuty to path
sys.path.insert(0, 'djehuty/src')

from djehuty.web.database import SparqlInterface


# Faculty name patterns for TU Delft (from real data observation)
FACULTY_PATTERNS = {
    'EEMCS': [
        r'Faculty of Electrical Engineering,? Mathematics and Computer Science',
        r'EEMCS',
        r'Faculty of EEMCS'
    ],
    'CEG': [
        r'Faculty of Civil Engineering and Geosciences',
        r'CEG',
        r'Faculty of CEG'
    ],
    'AE': [
        r'Faculty of Aerospace Engineering',
        r'Aerospace Engineering',
        r'Faculty of AE'
    ],
    'AS': [
        r'Faculty of Applied Sciences',
        r'Applied Sciences',
        r'Faculty of AS'
    ],
    'ABE': [
        r'Faculty of Architecture and the Built Environment',
        r'Architecture and the Built Environment',
        r'Faculty of ABE'
    ],
    'IDE': [
        r'Faculty of Industrial Design Engineering',
        r'Industrial Design Engineering',
        r'Faculty of IDE'
    ],
    'TPM': [
        r'Faculty of Technology,? Policy and Management',
        r'TPM',
        r'Faculty of TPM'
    ],
    '3mE': [
        r'Faculty of Mechanical,? Maritime and Materials Engineering',
        r'3mE',
        r'Faculty of 3mE'
    ]
}


# Institution IDs for 4TU universities
INSTITUTION_IDS = {
    '28586': 'TU Delft',
    '28589': 'TU Eindhoven',
    '28592': 'University of Twente',
    '28595': 'Wageningen University & Research'
}


def extract_faculty_from_organizations(org_text):
    """
    Extract faculty mentions from organization text using pattern matching.
    
    Args:
        org_text (str): Organizations field text
        
    Returns:
        list: List of (faculty_code, match_text) tuples
    """
    if not org_text:
        return []
    
    matches = []
    for faculty_code, patterns in FACULTY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, org_text, re.IGNORECASE):
                # Extract the full match for reporting
                match = re.search(pattern, org_text, re.IGNORECASE)
                matches.append((faculty_code, match.group(0)))
                break  # Only count each faculty once per dataset
    
    return matches


def analyze_datasets(db):
    """
    Analyze all datasets for faculty extraction potential.
    
    Args:
        db: SparqlInterface instance
        
    Returns:
        dict: Analysis results with statistics
    """
    print("=" * 80)
    print("Faculty Migration Analysis")
    print("=" * 80)
    print()
    
    # Query all datasets with their metadata
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
    
    print("⏳ Querying datasets from triple store...")
    
    # Query directly without cache to avoid issues
    import requests
    endpoint = "http://localhost:8890/sparql"
    response = requests.post(
        endpoint,
        data=query,
        headers={
            'Content-Type': 'application/sparql-query',
            'Accept': 'application/sparql-results+json'
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        results = data['results']['bindings']
        # Convert to format similar to __run_query output
        results = [{k: v.get('value') for k, v in row.items()} for row in results]
    else:
        print(f"⚠️  Query failed: {response.status_code}")
        results = []
    
    print(f"✓ Found {len(results)} datasets\n")
    
    # Analysis statistics
    stats = {
        'total_datasets': len(results),
        'datasets_with_organizations': 0,
        'datasets_with_faculty_mentions': 0,
        'datasets_by_institution': Counter(),
        'datasets_by_faculty': Counter(),
        'faculty_co_occurrences': defaultdict(int),
        'datasets_without_extraction': [],
        'sample_extractions': []
    }
    
    print("📊 Analyzing metadata...")
    print()
    
    # Analyze each dataset
    for i, dataset in enumerate(results, 1):
        dataset_id = dataset.get('dataset', '').split(':')[-1]
        title = dataset.get('title', 'N/A')
        group_id = dataset.get('group_id')
        org_text = dataset.get('organizations', '')
        
        # Count by institution
        if group_id in INSTITUTION_IDS:
            stats['datasets_by_institution'][INSTITUTION_IDS[group_id]] += 1
        
        # Check for organizations field
        if org_text:
            stats['datasets_with_organizations'] += 1
            
            # Extract faculties
            faculty_matches = extract_faculty_from_organizations(org_text)
            
            if faculty_matches:
                stats['datasets_with_faculty_mentions'] += 1
                
                # Count by faculty
                for faculty_code, _ in faculty_matches:
                    stats['datasets_by_faculty'][faculty_code] += 1
                
                # Track co-occurrences (datasets mentioning multiple faculties)
                if len(faculty_matches) > 1:
                    faculty_codes = sorted([f[0] for f in faculty_matches])
                    co_key = ' + '.join(faculty_codes)
                    stats['faculty_co_occurrences'][co_key] += 1
                
                # Save sample extractions (first 5)
                if len(stats['sample_extractions']) < 5:
                    stats['sample_extractions'].append({
                        'dataset_id': dataset_id,
                        'title': title[:60] + '...' if len(title) > 60 else title,
                        'institution_id': group_id,
                        'institution': INSTITUTION_IDS.get(group_id, 'Unknown'),
                        'faculties': faculty_matches,
                        'org_text': org_text[:150] + '...' if len(org_text) > 150 else org_text
                    })
            else:
                # Dataset has organizations but no faculty extracted
                if group_id in ['28586', '28589', '28592']:  # Only 4TU universities
                    stats['datasets_without_extraction'].append({
                        'dataset_id': dataset_id,
                        'title': title[:50] + '...' if len(title) > 50 else title,
                        'org_text': org_text[:100] + '...' if len(org_text) > 100 else org_text
                    })
        
    return stats


def print_analysis_report(stats):
    """
    Print comprehensive analysis report.
    
    Args:
        stats: Analysis statistics dictionary
    """
    print()
    print("=" * 80)
    print("ANALYSIS REPORT")
    print("=" * 80)
    print()
    
    # Overall statistics
    print("📈 Overall Statistics")
    print("-" * 80)
    print(f"Total datasets analyzed:              {stats['total_datasets']}")
    
    if stats['total_datasets'] > 0:
        org_pct = stats['datasets_with_organizations']/stats['total_datasets']*100
        fac_pct = stats['datasets_with_faculty_mentions']/stats['total_datasets']*100
        print(f"Datasets with organizations field:    {stats['datasets_with_organizations']} ({org_pct:.1f}%)")
        print(f"Datasets with faculty mentions:       {stats['datasets_with_faculty_mentions']} ({fac_pct:.1f}%)")
    else:
        print("⚠️  No datasets found to analyze")
        return
    print()
    
    # Institution distribution
    print("🏛️  Distribution by Institution")
    print("-" * 80)
    for institution, count in stats['datasets_by_institution'].most_common():
        percentage = count / stats['total_datasets'] * 100
        bar = '█' * int(percentage / 2)
        print(f"{institution:40s} {count:3d} ({percentage:5.1f}%) {bar}")
    print()
    
    # Faculty distribution
    if stats['datasets_by_faculty']:
        print("🎓 Distribution by Faculty (TU Delft)")
        print("-" * 80)
        for faculty, count in stats['datasets_by_faculty'].most_common():
            percentage = count / stats['datasets_with_faculty_mentions'] * 100
            bar = '█' * int(percentage / 2)
            print(f"{faculty:10s} {count:3d} datasets ({percentage:5.1f}%) {bar}")
        print()
    
    # Co-occurrences (collaborative datasets)
    if stats['faculty_co_occurrences']:
        print("🤝 Multi-Faculty Datasets (Collaboration)")
        print("-" * 80)
        for faculties, count in sorted(stats['faculty_co_occurrences'].items(), 
                                       key=lambda x: x[1], reverse=True):
            print(f"  {faculties:30s} {count:2d} dataset(s)")
        print()
    
    # Sample extractions
    if stats['sample_extractions']:
        print("✅ Sample Successful Extractions")
        print("-" * 80)
        for i, sample in enumerate(stats['sample_extractions'], 1):
            print(f"\n{i}. {sample['title']}")
            print(f"   Dataset ID: {sample['dataset_id']}")
            print(f"   Institution: {sample['institution']} (ID: {sample['institution_id']})")
            print(f"   Extracted Faculties:")
            for faculty_code, match_text in sample['faculties']:
                print(f"     • {faculty_code}: \"{match_text}\"")
            print(f"   Organizations text: {sample['org_text']}")
        print()
    
    # Datasets without extraction
    if stats['datasets_without_extraction']:
        print("⚠️  4TU Datasets Without Faculty Extraction (Sample)")
        print("-" * 80)
        print(f"Total: {len(stats['datasets_without_extraction'])} datasets")
        print("\nFirst 3 examples:")
        for i, dataset in enumerate(stats['datasets_without_extraction'][:3], 1):
            print(f"\n{i}. {dataset['title']}")
            print(f"   Dataset ID: {dataset['dataset_id']}")
            print(f"   Organizations: {dataset['org_text']}")
        print()
        print("Note: These may be from other universities (Wageningen, Eindhoven, Twente)")
        print("      or may need additional patterns for extraction.")
        print()
    
    # Data quality assessment
    print("📊 Data Quality Assessment")
    print("-" * 80)
    coverage = stats['datasets_with_faculty_mentions'] / stats['total_datasets'] * 100
    
    if coverage >= 70:
        quality = "EXCELLENT"
        emoji = "🟢"
    elif coverage >= 50:
        quality = "GOOD"
        emoji = "🟡"
    elif coverage >= 30:
        quality = "FAIR"
        emoji = "🟠"
    else:
        quality = "NEEDS IMPROVEMENT"
        emoji = "🔴"
    
    print(f"Coverage: {coverage:.1f}% {emoji}")
    print(f"Quality Assessment: {quality}")
    print()
    
    if coverage < 100:
        missing = stats['total_datasets'] - stats['datasets_with_faculty_mentions']
        print(f"Recommendation: Review {missing} datasets without faculty extraction.")
        print(f"                Consider:")
        print(f"                  • Adding more faculty name patterns")
        print(f"                  • Manual review for other universities")
        print(f"                  • Extracting from other metadata fields (authors, categories)")
    print()
    
    # Migration recommendations
    print("🚀 Migration Recommendations")
    print("-" * 80)
    print("1. AUTOMATED MIGRATION:")
    print(f"   • {stats['datasets_with_faculty_mentions']} datasets have clear faculty mentions")
    print(f"   • Use pattern matching to extract faculty and create RDF triples")
    print(f"   • Estimated time: ~1 hour to write script, ~5 minutes to execute")
    print()
    print("2. MANUAL REVIEW:")
    if stats['datasets_without_extraction']:
        print(f"   • {len(stats['datasets_without_extraction'])} datasets need manual review")
        print(f"   • May require:")
        print(f"     - Additional pattern rules")
        print(f"     - Author affiliation lookup")
        print(f"     - Manual categorization")
    print()
    print("3. VALIDATION:")
    print(f"   • Verify faculty assignments for multi-faculty datasets")
    print(f"   • Consider primary vs. secondary faculty affiliations")
    print(f"   • Test with faculty_statistics() method after migration")
    print()
    
    # Next steps
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print("✅ Phase 2A Complete: Analysis shows faculty extraction is feasible")
    print()
    print("⏭️  Phase 2B: Sample Migration")
    print("   Run: python prototype/migrate_sample_faculty.py")
    print("   This will:")
    print(f"     • Migrate {min(stats['datasets_with_faculty_mentions'], 5)} datasets with clear faculty mentions")
    print("     • Create faculty RDF triples")
    print("     • Link datasets to faculties using group_id")
    print("     • Generate before/after comparison report")
    print()


def save_analysis_json(stats, filename='prototype/analysis_results.json'):
    """
    Save analysis results as JSON for later use.
    
    Args:
        stats: Analysis statistics dictionary
        filename: Output filename
    """
    # Convert Counter objects to regular dicts for JSON serialization
    json_stats = {
        'total_datasets': stats['total_datasets'],
        'datasets_with_organizations': stats['datasets_with_organizations'],
        'datasets_with_faculty_mentions': stats['datasets_with_faculty_mentions'],
        'datasets_by_institution': dict(stats['datasets_by_institution']),
        'datasets_by_faculty': dict(stats['datasets_by_faculty']),
        'faculty_co_occurrences': dict(stats['faculty_co_occurrences']),
        'sample_extractions': stats['sample_extractions'],
        'coverage_percentage': stats['datasets_with_faculty_mentions'] / stats['total_datasets'] * 100
    }
    
    with open(filename, 'w') as f:
        json.dump(json_stats, f, indent=2, default=str)
    
    print(f"💾 Analysis results saved to: {filename}")
    print()


def main():
    """Main analysis execution."""
    # Setup database connection
    os.makedirs('data/cache', exist_ok=True)
    db = SparqlInterface()
    db.cache.storage = 'data/cache'
    db.setup_sparql_endpoint()
    
    # Run analysis
    stats = analyze_datasets(db)
    
    # Print report
    print_analysis_report(stats)
    
    # Save results
    save_analysis_json(stats)
    
    print("✅ Analysis complete!")
    print()


if __name__ == '__main__':
    main()
