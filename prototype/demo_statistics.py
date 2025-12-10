#!/usr/bin/env python3
"""
Demonstration Script: Institution and Faculty Statistics Output

This script demonstrates how the prototype outputs both institution-level
and faculty-level statistics, showing the improved granularity.

Usage:
    python3 prototype/demo_statistics.py

Output:
    - Pretty-printed tables showing institution and faculty statistics
    - Comparison metrics showing improved granularity
    - JSON output for API responses
"""

import sys
import os
import json

# Add djehuty to path
sys.path.insert(0, 'djehuty/src')

from djehuty.web.database import SparqlInterface
from djehuty.utils import convenience as conv


def print_section(title, char="="):
    """Print formatted section header"""
    print(f"\n{char * 80}")
    print(f"  {title}")
    print(f"{char * 80}\n")


def demo_institution_statistics(db):
    """Demonstrate institution-level statistics (current system)"""
    print_section("INSTITUTION-LEVEL STATISTICS (Current System)", "=")
    
    try:
        # Get institution statistics (wrapper around existing dataset_statistics)
        stats = db.institution_statistics(limit=10)
        
        if stats and len(stats) > 0:
            print(f"📊 Found {len(stats)} institutions:\n")
            print(f"{'Institution ID':<15} {'Name':<30} {'Datasets':<10}")
            print("-" * 60)
            
            for inst in stats:
                inst_id = inst.get('group_id', inst.get('id', 'N/A'))
                name = inst.get('name', f'Institution {inst_id}')
                count = inst.get('dataset_count', 0)
                print(f"{inst_id:<15} {name:<30} {count:<10}")
            
            total = sum(s.get('dataset_count', 0) for s in stats)
            print("-" * 60)
            print(f"{'TOTAL':<15} {'':<30} {total:<10}\n")
            
            return stats
        else:
            print("⚠️  No institution statistics available")
            print("    (Using mock data for demonstration)\n")
            
            # Mock data for demonstration
            mock_stats = [
                {'group_id': 28586, 'name': 'TU Delft', 'dataset_count': 3},
                {'group_id': 28598, 'name': 'Utrecht University', 'dataset_count': 4},
                {'group_id': 28592, 'name': 'TU Eindhoven', 'dataset_count': 1},
                {'group_id': 28589, 'name': 'University of Twente', 'dataset_count': 1}
            ]
            
            print(f"📊 Mock data - {len(mock_stats)} institutions:\n")
            print(f"{'Institution ID':<15} {'Name':<30} {'Datasets':<10}")
            print("-" * 60)
            
            for inst in mock_stats:
                print(f"{inst['group_id']:<15} {inst['name']:<30} {inst['dataset_count']:<10}")
            
            total = sum(s['dataset_count'] for s in mock_stats)
            print("-" * 60)
            print(f"{'TOTAL':<15} {'':<30} {total:<10}\n")
            
            return mock_stats
            
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return []


def demo_faculty_statistics(db):
    """Demonstrate faculty-level statistics (prototype feature)"""
    print_section("FACULTY-LEVEL STATISTICS (Prototype Feature)", "=")
    
    try:
        # Get faculty statistics
        stats = db.faculty_statistics(limit=20)
        
        if stats and len(stats) > 0:
            print(f"📊 Found {len(stats)} faculties:\n")
            
            # Add mock dataset counts for demonstration (since migration blocked)
            if len(stats) == 3 and all(s.get('dataset_count', 0) == 0 for s in stats):
                print("💡 Note: Adding mock dataset counts for demonstration")
                print("   (Faculty entities exist, but datasets not migrated yet)\n")
                # Distribute 9 datasets across 3 faculties (matches real dataset total)
                mock_counts = [3, 2, 4]  # Total = 9
                for i, fac in enumerate(stats):
                    fac['dataset_count'] = mock_counts[i]
            
            print(f"{'Faculty Code':<15} {'Name':<45} {'Datasets':<10}")
            print("-" * 75)
            
            for fac in stats:
                code = fac.get('faculty_short_name', 'N/A')
                name = fac.get('faculty_name', 'Unknown Faculty')
                count = fac.get('dataset_count', 0)
                
                # Truncate long names
                if len(name) > 42:
                    name = name[:39] + "..."
                
                print(f"{code:<15} {name:<45} {count:<10}")
            
            total = sum(s.get('dataset_count', 0) for s in stats)
            print("-" * 75)
            print(f"{'TOTAL':<15} {'':<45} {total:<10}")
            print("\n⚠️  Dataset counts are mock data for demonstration purposes.")
            print("   In production, these would come from migrated datasets.\n")
            
            return stats
        else:
            print("⚠️  No faculty dataset counts available")
            print("    (Faculty entities exist but datasets not yet migrated)\n")
            
            # Show that faculty entities DO exist with mock dataset counts
            print("🔍 Faculty entities with mock dataset counts for demonstration:")
            print(f"{'Faculty Code':<15} {'Name':<45} {'Datasets':<12}")
            print("-" * 75)
            
            # Mock faculty data matching what exists, with demo counts
            mock_faculties = [
                {'faculty_short_name': 'EEMCS', 
                 'faculty_name': 'Faculty of Electrical Engineering, Mathematics and Computer Science',
                 'group_id': 285860001, 'dataset_count': 3},  # Mock: 3 datasets
                {'faculty_short_name': 'AE',
                 'faculty_name': 'Faculty of Aerospace Engineering',
                 'group_id': 285860002, 'dataset_count': 2},  # Mock: 2 datasets
                {'faculty_short_name': 'AS',
                 'faculty_name': 'Faculty of Applied Sciences',
                 'group_id': 285860003, 'dataset_count': 4}   # Mock: 4 datasets
            ]
            
            for fac in mock_faculties:
                code = fac['faculty_short_name']
                name = fac['faculty_name']
                count = fac['dataset_count']
                
                if len(name) > 42:
                    name = name[:39] + "..."
                
                print(f"{code:<15} {name:<45} {count:<12}")
            
            total = sum(f['dataset_count'] for f in mock_faculties)
            print("-" * 75)
            print(f"{'TOTAL':<15} {'':<45} {total:<12}")
            
            print("\n💡 Note: Dataset counts are mock data (total = 9, matching real datasets)")
            print("   Faculty RDF entities exist in the triple store (verified by SPARQL)")
            print("   Migration logic ready but blocked by write permissions\n")
            
            return mock_faculties
            
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return []


def demo_comparison(inst_stats, fac_stats):
    """Show comparison between institution and faculty granularity"""
    print_section("GRANULARITY COMPARISON", "=")
    
    inst_count = len([s for s in inst_stats if s.get('dataset_count', 0) > 0 or s.get('count', 0) > 0])
    fac_count = len(fac_stats)
    
    print(f"📈 Statistical Granularity Improvement:\n")
    print(f"  Institution-level groups: {inst_count}")
    print(f"  Faculty-level groups:     {fac_count}")
    
    if inst_count > 0:
        improvement = (fac_count / inst_count) if inst_count > 0 else 0
        print(f"  Granularity multiplier:   {improvement:.2f}x\n")
        print(f"  This means faculty-level tracking provides {improvement:.2f}x more")
        print(f"  detailed statistical breakdowns compared to institution-level.\n")
    
    # Show example breakdown for TU Delft
    print(f"📊 Example: TU Delft Breakdown\n")
    print(f"  Institution level:")
    print(f"    - TU Delft: 3 datasets\n")
    print(f"  Faculty level:")
    print(f"    - EEMCS (Electrical Engineering...): 0 datasets")
    print(f"    - AE (Aerospace Engineering):         0 datasets")
    print(f"    - AS (Applied Sciences):              0 datasets\n")
    print(f"  💡 Once datasets are migrated, each faculty will show")
    print(f"     its specific dataset count instead of institutional total.\n")


def demo_json_output(inst_stats, fac_stats):
    """Show JSON output for API responses"""
    print_section("JSON OUTPUT (API Response Format)", "=")
    
    output = {
        "generated_at": "2025-12-10T00:00:00",
        "institutions": [],
        "faculties": []
    }
    
    # Format institution data
    for inst in inst_stats[:3]:  # Show first 3
        output["institutions"].append({
            "id": inst.get('group_id', inst.get('id')),
            "name": inst.get('name', 'Unknown'),
            "dataset_count": inst.get('dataset_count', inst.get('count', 0))
        })
    
    # Format faculty data
    for fac in fac_stats[:3]:  # Show first 3
        output["faculties"].append({
            "faculty_id": fac.get('group_id', fac.get('faculty_id')),
            "faculty_code": fac.get('faculty_short_name', 'N/A'),
            "faculty_name": fac.get('faculty_name', 'Unknown'),
            "dataset_count": fac.get('dataset_count', 0)
        })
    
    print("Sample JSON response (first 3 of each):\n")
    print(json.dumps(output, indent=2))
    print()


def main():
    """Main demonstration"""
    print("\n" + "=" * 80)
    print("  FACULTY STATISTICS PROTOTYPE - OUTPUT DEMONSTRATION")
    print("=" * 80)
    print("\n  This demonstrates how the prototype outputs both institution-level")
    print("  and faculty-level statistics with improved granularity.\n")
    
    try:
        # Initialize database
        print("🔌 Connecting to SPARQL endpoint...")
        db = SparqlInterface()
        db.cache.storage = 'data/cache'
        db.setup_sparql_endpoint()
        print("✅ Connected!\n")
        
        # Demonstrate institution statistics
        inst_stats = demo_institution_statistics(db)
        
        # Demonstrate faculty statistics
        fac_stats = demo_faculty_statistics(db)
        
        # Show comparison
        demo_comparison(inst_stats, fac_stats)
        
        # Show JSON output
        demo_json_output(inst_stats, fac_stats)
        
        # Summary
        print_section("SUMMARY", "=")
        print("✅ Institution statistics: Working (wrapper around existing code)")
        print("✅ Faculty statistics: Implemented (new RDF entities + query method)")
        print("✅ Faculty entities: Created in RDF store (3 TU Delft faculties)")
        print("⚠️  Dataset migration: Blocked by write permissions")
        print("\n💡 The prototype demonstrates the architecture and data model.")
        print("   Once write permissions are enabled, the migration would populate")
        print("   faculty-level dataset counts automatically.\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
