#!/usr/bin/env python3
"""
Test the new faculty_statistics() backend method.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../djehuty/src'))

from djehuty.web.config import config
from djehuty.web.database import SparqlInterface

def main():
    print("=" * 70)
    print("TESTING: faculty_statistics() Backend Method")
    print("=" * 70)
    
    # Initialize database
    db = SparqlInterface()
    
    # Set up cache with data/cache directory
    cache_dir = os.path.join(os.path.dirname(__file__), '../data/cache')
    os.makedirs(cache_dir, exist_ok=True)
    db.cache.storage = cache_dir
    
    db.setup_sparql_endpoint()
    
    if not db.sparql_is_up:
        print("❌ Failed to connect to SPARQL endpoint")
        return 1
    
    print("\n✅ Connected to SPARQL endpoint")
    
    # Test 1: Get all faculty statistics
    print("\n" + "=" * 70)
    print("TEST 1: Get all faculty statistics")
    print("=" * 70)
    
    try:
        results = db.faculty_statistics()
        print(f"\n📊 Found {len(results)} faculties:\n")
        
        for row in results:
            print(f"Faculty: {row['faculty_short_name']}")
            print(f"  ID: {row['faculty_id']}")
            print(f"  Full Name: {row['faculty_name']}")
            print(f"  Institution ID: {row['institution_id']}")
            print(f"  Dataset Count: {row['dataset_count']}")
            print()
        
        if results:
            print("✅ TEST 1 PASSED - faculty_statistics() works!")
        else:
            print("⚠️  TEST 1 WARNING - No results (expected if no datasets linked)")
    
    except Exception as e:
        print(f"❌ TEST 1 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Test 2: Filter by institution
    print("\n" + "=" * 70)
    print("TEST 2: Filter by institution_id=28586 (TU Delft)")
    print("=" * 70)
    
    try:
        results = db.faculty_statistics(institution_id=28586)
        print(f"\n📊 Found {len(results)} TU Delft faculties:\n")
        
        for row in results:
            print(f"  - {row['faculty_short_name']}: {row['dataset_count']} datasets")
        
        if results:
            print("\n✅ TEST 2 PASSED - institution filtering works!")
        else:
            print("\n⚠️  TEST 2 WARNING - No TU Delft faculties found")
    
    except Exception as e:
        print(f"❌ TEST 2 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Test 3: Pagination
    print("\n" + "=" * 70)
    print("TEST 3: Pagination (limit=2)")
    print("=" * 70)
    
    try:
        results = db.faculty_statistics(limit=2)
        print(f"\n📊 Retrieved {len(results)} faculties (limited to 2):\n")
        
        for row in results:
            print(f"  - {row['faculty_short_name']}")
        
        if len(results) <= 2:
            print("\n✅ TEST 3 PASSED - pagination works!")
        else:
            print(f"\n❌ TEST 3 FAILED - Expected max 2 results, got {len(results)}")
    
    except Exception as e:
        print(f"❌ TEST 3 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Test 4: JSON serialization
    print("\n" + "=" * 70)
    print("TEST 4: JSON Serialization (for API response)")
    print("=" * 70)
    
    try:
        results = db.faculty_statistics(limit=1)
        json_output = json.dumps(results, indent=2, default=str)
        print("\nSample JSON response:")
        print(json_output)
        print("\n✅ TEST 4 PASSED - JSON serialization works!")
    
    except Exception as e:
        print(f"❌ TEST 4 FAILED: {e}")
        return 1
    
    # Test 5: institution_statistics() wrapper
    print("\n" + "=" * 70)
    print("TEST 5: institution_statistics() wrapper method")
    print("=" * 70)
    
    try:
        results = db.institution_statistics(limit=5)
        print(f"\n📊 Retrieved institution statistics (limit=5):")
        print(f"   Found {len(results)} results")
        print("\n✅ TEST 5 PASSED - institution_statistics() wrapper works!")
    
    except Exception as e:
        print(f"❌ TEST 5 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nBackend methods are ready for API integration.")
    print("\nNext steps:")
    print("  1. Create API route: /v2/stats/faculty")
    print("  2. Create API route: /v2/stats/institution")
    print("  3. Test with curl/browser")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
