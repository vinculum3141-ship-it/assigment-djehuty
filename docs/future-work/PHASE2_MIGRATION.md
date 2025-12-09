# Phase 2: Author Migration Strategy

**Document:** PHASE2_MIGRATION.md  
**Part of:** Phase 2 Solution Architecture (Author-Level Faculty Statistics)  
**Prerequisites:** PHASE2_DATA_MODEL.md, Phase 1 migration complete

---

## Table of Contents

1. Migration Overview
2. Author Segmentation
3. Migration Scripts
4. Manual Review Workflow
5. Quality Assurance
6. Rollback Plan
7. Timeline & Resources

---

## 1. Migration Overview

### 1.1 Goals

**Primary Objective:** Assign `faculty_id` to ~1,000 existing TU Delft author entities

**Targets:**
- ≥85% coverage (authors with faculty_id assigned)
- ≥80% accuracy (correct faculty assignments)
- ≥70% high confidence (confidence ≥ 0.8)
- 0 external authors with faculty_id (proper filtering)

### 1.2 Migration Phases

```
Phase 2A: Registered Authors (Week 1)
├── Export ~150 registered TU Delft authors
├── Copy faculty_id from linked accounts
├── Validate consistency with Phase 1
└── Import with confidence = 1.0

Phase 2B: Unregistered Authors - Automated (Week 2-3)
├── Export ~800 unregistered TU Delft authors
├── Get Organizations fields from their datasets
├── Run pattern matching algorithm
├── Auto-assign high confidence (≥0.8)
└── Flag medium/low for manual review

Phase 2C: Manual Review (Week 4-5)
├── Review ~200 flagged authors
├── Research using ORCID, email patterns, dataset context
├── Manual faculty assignment
└── Import with confidence = 1.0

Phase 2D: Validation & Cleanup (Week 5)
├── Run integrity checks
├── Validate statistics
├── Fix any errors
└── Final report
```

---

## 2. Author Segmentation

### 2.1 Author Categories

```python
# Query to segment authors
AUTHOR_SEGMENTS = """
SELECT 
    (COUNT(*) AS ?total),
    (SUM(?is_registered) AS ?registered),
    (SUM(?is_tu_delft) AS ?tu_delft),
    (SUM(?is_external) AS ?external),
    (SUM(?has_orcid) AS ?with_orcid)
WHERE {
    ?author rdf:type djht:Author .
    
    BIND(EXISTS { ?author djht:account ?acc . } AS ?is_registered)
    BIND(EXISTS { ?author djht:institution_id 28586 . } AS ?is_tu_delft)
    BIND(EXISTS { 
        ?author djht:institution_id ?inst_id . 
        FILTER(?inst_id != 28586) 
    } AS ?is_external)
    BIND(EXISTS { ?author djht:orcid_id ?orcid . } AS ?has_orcid)
}
"""
```

**Expected Results:**
| Category | Count | Migration Action |
|----------|-------|------------------|
| Registered TU Delft | 150 | Copy from account (Phase 2A) |
| Unregistered TU Delft | 800 | Parse Organizations (Phase 2B) |
| Unregistered TU Delft with ORCID | 100 | Enhanced matching (Phase 2B) |
| External authors | 300 | Skip (no faculty_id) |
| **TOTAL** | **1,250** | **950 migrated** |

### 2.2 Dataset-Author Linkage

```python
def get_organizations_for_author(author_uuid):
    """
    Get all Organizations field values from datasets where author appears.
    
    Returns list of (dataset_uuid, organizations_text) tuples.
    """
    query = f"""
    PREFIX djht: <https://data.4tu.nl/ontology/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?dataset_uuid ?organizations
    WHERE {{
        ?dataset djht:authors/rdf:rest*/rdf:first <author:{author_uuid}> .
        ?dataset djht:custom_fields/rdf:rest*/rdf:first ?custom_field .
        ?custom_field djht:name "Organizations" ;
                      djht:value ?organizations .
        BIND(STRAFTER(STR(?dataset), "dataset:") AS ?dataset_uuid)
    }}
    """
    
    results = execute_sparql(query)
    return [(row['dataset_uuid'], row['organizations']) for row in results]
```

**Insight:** Unregistered authors may appear on multiple datasets with **different** Organizations values:
- Author "Hebly, Scott J." appears on 3 datasets
  - Dataset 1: "TU Delft, Faculty of Aerospace Engineering"
  - Dataset 2: "Aerospace Engineering, TU Delft"
  - Dataset 3: "Delft University of Technology, AE"
- **Strategy:** Combine all Organizations texts, run pattern matching, take highest confidence match

---

## 3. Migration Scripts

### 3.1 Phase 2A: Export Registered Authors

**Script:** `export_registered_authors.py`

```python
#!/usr/bin/env python3
"""
Export registered TU Delft authors with account faculty_id.
Output: CSV ready for import.
"""

import csv
from datetime import datetime, timezone

def export_registered_authors(output_csv='phase2a_registered_authors.csv'):
    """
    Export registered authors where account has faculty_id from Phase 1.
    """
    query = """
    PREFIX djht: <https://data.4tu.nl/ontology/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?author_uuid ?account_uuid ?faculty_id ?full_name
    WHERE {
        GRAPH <https://data.4tu.nl> {
            ?author rdf:type djht:Author .
            ?author djht:account ?account .
            ?author djht:full_name ?full_name .
            ?account djht:faculty_id ?faculty_id .
            ?account djht:institution_id 28586 .  # TU Delft only
            
            # Ensure author doesn't already have faculty_id
            FILTER NOT EXISTS { ?author djht:faculty_id ?existing . }
            
            BIND(STRAFTER(STR(?author), "author:") AS ?author_uuid)
            BIND(STRAFTER(STR(?account), "account:") AS ?account_uuid)
        }
    }
    ORDER BY ?full_name
    """
    
    results = execute_sparql(query)
    
    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'author_uuid', 'account_uuid', 'full_name', 'faculty_id',
            'faculty_confidence', 'faculty_source', 'faculty_assigned_date'
        ])
        writer.writeheader()
        
        for row in results:
            writer.writerow({
                'author_uuid': row['author_uuid'],
                'account_uuid': row['account_uuid'],
                'full_name': row['full_name'],
                'faculty_id': row['faculty_id'],
                'faculty_confidence': 1.0,  # From account = verified
                'faculty_source': 'account',
                'faculty_assigned_date': datetime.now(timezone.utc).isoformat()
            })
    
    print(f"Exported {len(results)} registered authors to {output_csv}")
    return output_csv

if __name__ == '__main__':
    export_registered_authors()
```

**Expected Output:** `phase2a_registered_authors.csv`

```csv
author_uuid,account_uuid,full_name,faculty_id,faculty_confidence,faculty_source,faculty_assigned_date
12345-abc,67890-def,"Dr. Jane Smith",285860001,1.0,account,2025-12-09T10:00:00Z
23456-bcd,78901-efg,"Prof. John Doe",285860005,1.0,account,2025-12-09T10:00:01Z
...
```

### 3.2 Phase 2B: Export Unregistered Authors

**Script:** `export_unregistered_authors.py`

```python
#!/usr/bin/env python3
"""
Export unregistered TU Delft authors with Organizations field data.
Output: CSV with author info + all Organizations texts.
"""

import csv

def get_organizations_for_author(author_uuid):
    """Get all Organizations field values for author's datasets."""
    query = f"""
    PREFIX djht: <https://data.4tu.nl/ontology/>
    SELECT DISTINCT ?organizations
    WHERE {{
        ?dataset djht:authors/rdf:rest*/rdf:first <author:{author_uuid}> .
        ?dataset djht:custom_fields/rdf:rest*/rdf:first ?custom_field .
        ?custom_field djht:name "Organizations" ;
                      djht:value ?organizations .
    }}
    """
    results = execute_sparql(query)
    return [row['organizations'] for row in results]

def export_unregistered_authors(output_csv='phase2b_unregistered_authors.csv'):
    """
    Export unregistered TU Delft authors.
    """
    query = """
    PREFIX djht: <https://data.4tu.nl/ontology/>
    SELECT ?author_uuid ?full_name ?institution_id ?orcid_id
    WHERE {
        ?author rdf:type djht:Author .
        ?author djht:full_name ?full_name .
        ?author djht:institution_id 28586 .  # TU Delft
        
        # Unregistered (no account)
        FILTER NOT EXISTS { ?author djht:account ?acc . }
        
        # No faculty_id yet
        FILTER NOT EXISTS { ?author djht:faculty_id ?fid . }
        
        OPTIONAL { ?author djht:orcid_id ?orcid_id . }
        OPTIONAL { ?author djht:institution_id ?institution_id . }
        
        BIND(STRAFTER(STR(?author), "author:") AS ?author_uuid)
    }
    ORDER BY ?full_name
    """
    
    results = execute_sparql(query)
    
    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'author_uuid', 'full_name', 'institution_id', 'orcid_id',
            'organizations_combined', 'dataset_count'
        ])
        writer.writeheader()
        
        for row in results:
            author_uuid = row['author_uuid']
            
            # Get all Organizations texts for this author
            org_texts = get_organizations_for_author(author_uuid)
            org_combined = " | ".join(org_texts)  # Concatenate with separator
            
            writer.writerow({
                'author_uuid': author_uuid,
                'full_name': row['full_name'],
                'institution_id': row.get('institution_id', ''),
                'orcid_id': row.get('orcid_id', ''),
                'organizations_combined': org_combined,
                'dataset_count': len(org_texts)
            })
    
    print(f"Exported {len(results)} unregistered authors to {output_csv}")
    return output_csv

if __name__ == '__main__':
    export_unregistered_authors()
```

**Expected Output:** `phase2b_unregistered_authors.csv`

```csv
author_uuid,full_name,institution_id,orcid_id,organizations_combined,dataset_count
abc-123,"Hebly, Scott J.",28586,,"TU Delft, Faculty of Aerospace Engineering | Aerospace Engineering, TU Delft",2
def-456,"van der Berg, Maria",28586,0000-0003-1234-5678,"Faculty of EEMCS, TU Delft",1
...
```

### 3.3 Phase 2B: Detect Faculty Patterns

**Script:** `detect_author_faculty.py`

```python
#!/usr/bin/env python3
"""
Detect faculty from Organizations field for unregistered authors.
Uses pattern matching with confidence scoring.
"""

import csv
import re
from datetime import datetime, timezone

# Faculty pattern library (from PHASE2_DATA_MODEL.md)
FACULTY_PATTERNS = {
    285860001: {  # Aerospace Engineering
        'name': 'Faculty of Aerospace Engineering',
        'patterns': [
            (r'Faculty of Aerospace Engineering', 0.9),
            (r'Aerospace Engineering', 0.7),
            (r'\bAE\b', 0.5),
            (r'Flight Performance', 0.6),
            (r'Aircraft Noise', 0.5),
        ]
    },
    285860002: {  # Architecture
        'name': 'Faculty of Architecture and the Built Environment',
        'patterns': [
            (r'Faculty of Architecture', 0.9),
            (r'Architecture and the Built Environment', 0.85),
            (r'\bA\+BE\b', 0.7),
            (r'\bBK\b', 0.6),
        ]
    },
    285860003: {  # Applied Sciences
        'name': 'Faculty of Applied Sciences',
        'patterns': [
            (r'Faculty of Applied Sciences', 0.9),
            (r'Applied Sciences', 0.75),
            (r'\bAS\b', 0.5),
            (r'\bTNW\b', 0.6),
        ]
    },
    285860004: {  # Civil Engineering
        'name': 'Faculty of Civil Engineering and Geosciences',
        'patterns': [
            (r'Faculty of Civil Engineering', 0.9),
            (r'Civil Engineering and Geosciences', 0.85),
            (r'\bCEG\b', 0.7),
            (r'\bCiTG\b', 0.7),
        ]
    },
    285860005: {  # EEMCS
        'name': 'Faculty of Electrical Engineering, Mathematics and Computer Science',
        'patterns': [
            (r'Faculty of Electrical Engineering, Mathematics and Computer Science', 0.95),
            (r'Faculty of EEMCS', 0.9),
            (r'\bEEMCS\b', 0.7),
            (r'\bEWI\b', 0.7),
            (r'Computer Science', 0.6),
            (r'Electrical Engineering', 0.6),
        ]
    },
    285860006: {  # Industrial Design
        'name': 'Faculty of Industrial Design Engineering',
        'patterns': [
            (r'Faculty of Industrial Design', 0.9),
            (r'Industrial Design Engineering', 0.85),
            (r'\bIDE\b', 0.7),
            (r'\bIO\b', 0.6),
        ]
    },
    285860007: {  # Mechanical Engineering
        'name': 'Faculty of Mechanical, Maritime and Materials Engineering',
        'patterns': [
            (r'Faculty of Mechanical', 0.9),
            (r'Mechanical, Maritime and Materials Engineering', 0.85),
            (r'\b3mE\b', 0.7),
            (r'\bME\b', 0.5),
        ]
    },
    285860008: {  # TPM
        'name': 'Faculty of Technology, Policy and Management',
        'patterns': [
            (r'Faculty of Technology, Policy and Management', 0.9),
            (r'Technology, Policy and Management', 0.85),
            (r'\bTPM\b', 0.7),
            (r'\bTBM\b', 0.7),
        ]
    },
}

def detect_faculty(organizations_text):
    """
    Detect faculty from Organizations field text.
    
    Returns: (faculty_id, confidence_score, matched_pattern)
    """
    if not organizations_text:
        return None, 0.0, None
    
    best_match = None
    best_confidence = 0.0
    matched_pattern = None
    
    for faculty_id, config in FACULTY_PATTERNS.items():
        for pattern, weight in config['patterns']:
            if re.search(pattern, organizations_text, re.IGNORECASE):
                if weight > best_confidence:
                    best_match = faculty_id
                    best_confidence = weight
                    matched_pattern = pattern
    
    # Bonus for explicit "Faculty of" structure
    if best_match and re.search(r'Faculty of', organizations_text):
        best_confidence = min(best_confidence + 0.1, 1.0)
    
    # Penalty for multiple faculty mentions
    faculty_count = sum(1 for fid, cfg in FACULTY_PATTERNS.items() 
                       if any(re.search(p, organizations_text, re.IGNORECASE) 
                             for p, w in cfg['patterns']))
    if faculty_count > 1:
        best_confidence *= 0.7  # Ambiguous
    
    return best_match, best_confidence, matched_pattern

def process_unregistered_authors(input_csv, output_csv):
    """
    Process unregistered authors and detect faculty from Organizations.
    """
    with open(input_csv) as f_in:
        reader = csv.DictReader(f_in)
        rows = list(reader)
    
    with open(output_csv, 'w', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=[
            'author_uuid', 'full_name', 'faculty_id', 'faculty_confidence',
            'faculty_source', 'faculty_assigned_date', 'matched_pattern',
            'organizations_text', 'action', 'review_priority'
        ])
        writer.writeheader()
        
        stats = {'high': 0, 'medium': 0, 'low': 0, 'none': 0}
        
        for row in rows:
            author_uuid = row['author_uuid']
            full_name = row['full_name']
            organizations = row['organizations_combined']
            
            faculty_id, confidence, pattern = detect_faculty(organizations)
            
            # Determine action
            if confidence >= 0.8:
                action = 'AUTO_ASSIGN'
                priority = 'LOW'
                stats['high'] += 1
            elif confidence >= 0.5:
                action = 'MANUAL_REVIEW'
                priority = 'MEDIUM'
                stats['medium'] += 1
            elif confidence > 0.0:
                action = 'MANUAL_REVIEW'
                priority = 'HIGH'
                stats['low'] += 1
            else:
                action = 'MANUAL_REVIEW'
                priority = 'HIGH'
                stats['none'] += 1
                faculty_id = None
            
            writer.writerow({
                'author_uuid': author_uuid,
                'full_name': full_name,
                'faculty_id': faculty_id if faculty_id else '',
                'faculty_confidence': f"{confidence:.2f}",
                'faculty_source': 'organizations_auto' if confidence >= 0.8 else 'organizations_manual',
                'faculty_assigned_date': datetime.now(timezone.utc).isoformat(),
                'matched_pattern': pattern if pattern else '',
                'organizations_text': organizations[:200],  # Truncate for readability
                'action': action,
                'review_priority': priority
            })
    
    print(f"\nProcessed {len(rows)} unregistered authors:")
    print(f"  High confidence (≥0.8): {stats['high']} - AUTO_ASSIGN")
    print(f"  Medium confidence (0.5-0.8): {stats['medium']} - MANUAL_REVIEW")
    print(f"  Low confidence (<0.5): {stats['low']} - MANUAL_REVIEW")
    print(f"  No match: {stats['none']} - MANUAL_REVIEW")
    print(f"\nOutput: {output_csv}")
    
    return output_csv

if __name__ == '__main__':
    input_file = 'phase2b_unregistered_authors.csv'
    output_file = 'phase2b_faculty_detected.csv'
    process_unregistered_authors(input_file, output_file)
```

**Expected Output:** `phase2b_faculty_detected.csv`

```csv
author_uuid,full_name,faculty_id,faculty_confidence,faculty_source,faculty_assigned_date,matched_pattern,organizations_text,action,review_priority
abc-123,"Hebly, Scott J.",285860001,0.90,organizations_auto,2025-12-09T12:00:00Z,"Faculty of Aerospace Engineering","TU Delft, Faculty of Aerospace Engineering | Aerospace Engineering, TU Delft",AUTO_ASSIGN,LOW
def-456,"van der Berg, Maria",285860005,0.85,organizations_auto,2025-12-09T12:00:01Z,"Faculty of EEMCS","Faculty of EEMCS, TU Delft",AUTO_ASSIGN,LOW
ghi-789,"Smith, Robert",285860001,0.65,organizations_manual,2025-12-09T12:00:02Z,"Aerospace Engineering","Aerospace Engineering",MANUAL_REVIEW,MEDIUM
jkl-012,"Johnson, Emily",,0.00,organizations_manual,2025-12-09T12:00:03Z,,"",MANUAL_REVIEW,HIGH
...
```

### 3.4 Phase 2B: Import Auto-Assigned Authors

**Script:** `import_author_faculty.py`

```python
#!/usr/bin/env python3
"""
Import faculty assignments for authors.
Supports dry-run mode and filtering by action.
"""

import csv
import sys

def import_faculty_assignments(input_csv, dry_run=True, action_filter='AUTO_ASSIGN'):
    """
    Import faculty assignments to Author entities.
    
    Args:
        input_csv: CSV from detect_author_faculty.py
        dry_run: If True, print SPARQL without executing
        action_filter: Only import rows with this action (AUTO_ASSIGN, MANUAL_REVIEW, or ALL)
    """
    with open(input_csv) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    if action_filter != 'ALL':
        rows = [r for r in rows if r['action'] == action_filter]
    
    # Filter out rows without faculty_id
    rows = [r for r in rows if r.get('faculty_id')]
    
    print(f"Importing {len(rows)} faculty assignments...")
    if dry_run:
        print("[DRY RUN MODE - no changes will be made]")
    
    imported = 0
    errors = 0
    
    for row in rows:
        author_uuid = row['author_uuid']
        faculty_id = row['faculty_id']
        confidence = row['faculty_confidence']
        source = row['faculty_source']
        assigned_date = row['faculty_assigned_date']
        
        sparql_query = f"""
        PREFIX djht: <https://data.4tu.nl/ontology/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        INSERT {{
            GRAPH <https://data.4tu.nl> {{
                <author:{author_uuid}> djht:faculty_id {faculty_id} .
                <author:{author_uuid}> djht:faculty_confidence "{confidence}"^^xsd:float .
                <author:{author_uuid}> djht:faculty_source "{source}"^^xsd:string .
                <author:{author_uuid}> djht:faculty_assigned_date "{assigned_date}"^^xsd:dateTime .
            }}
        }}
        WHERE {{
            GRAPH <https://data.4tu.nl> {{
                <author:{author_uuid}> rdf:type djht:Author .
                # Ensure no existing faculty_id
                FILTER NOT EXISTS {{ <author:{author_uuid}> djht:faculty_id ?existing . }}
            }}
        }}
        """
        
        if dry_run:
            print(f"\n--- Author: {row['full_name']} ({author_uuid}) ---")
            print(f"Faculty: {faculty_id}, Confidence: {confidence}")
            print(sparql_query[:200] + "...")
        else:
            try:
                execute_sparql_update(sparql_query)
                imported += 1
                if imported % 50 == 0:
                    print(f"  Imported {imported}/{len(rows)}...")
            except Exception as e:
                print(f"ERROR importing {author_uuid}: {e}")
                errors += 1
    
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Summary:")
    print(f"  Total rows: {len(rows)}")
    print(f"  Imported: {imported}")
    print(f"  Errors: {errors}")
    
    return imported, errors

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Import author faculty assignments')
    parser.add_argument('input_csv', help='CSV file with faculty assignments')
    parser.add_argument('--execute', action='store_true', help='Execute import (default is dry-run)')
    parser.add_argument('--action', default='AUTO_ASSIGN', 
                       choices=['AUTO_ASSIGN', 'MANUAL_REVIEW', 'ALL'],
                       help='Filter by action type')
    
    args = parser.parse_args()
    
    import_faculty_assignments(
        args.input_csv,
        dry_run=not args.execute,
        action_filter=args.action
    )
```

**Usage:**

```bash
# Dry run (preview only)
python import_author_faculty.py phase2b_faculty_detected.csv

# Import AUTO_ASSIGN only (high confidence)
python import_author_faculty.py phase2b_faculty_detected.csv --execute --action AUTO_ASSIGN

# Import everything (after manual review)
python import_author_faculty.py phase2c_manually_reviewed.csv --execute --action ALL
```

---

## 4. Manual Review Workflow

### 4.1 Manual Review CSV Template

**File:** `phase2c_manual_review_template.csv`

Rows flagged with `action=MANUAL_REVIEW` are exported for human review:

```csv
author_uuid,full_name,suggested_faculty_id,suggested_faculty_name,confidence,organizations_text,orcid_id,dataset_count,reviewer_notes,final_faculty_id,final_confidence,review_status
ghi-789,"Smith, Robert",285860001,"Faculty of Aerospace Engineering",0.65,"Aerospace Engineering",,2,,,,PENDING
jkl-012,"Johnson, Emily",,"",0.00,"",,1,,,,PENDING
mno-345,"Lee, David",285860005,"Faculty of EEMCS",0.55,"Computer Science, TU Delft",0000-0003-1234-5678,3,,,,PENDING
...
```

### 4.2 Review Process

**Step 1: Researcher investigates using:**
1. Author full name (Google Scholar, institutional page)
2. ORCID profile (if available)
3. Dataset titles and descriptions
4. Email domain patterns (if available in account table)
5. Co-author affiliations

**Step 2: Fill in columns:**
- `reviewer_notes`: Evidence for assignment (e.g., "ORCID shows Aerospace affiliation 2020-present")
- `final_faculty_id`: Confirmed faculty ID
- `final_confidence`: 1.0 (manually verified)
- `review_status`: CONFIRMED, UNCLEAR, or EXTERNAL

**Step 3: Import reviewed authors:**
```bash
python import_author_faculty.py phase2c_manually_reviewed.csv --execute --action ALL
```

### 4.3 Edge Cases

**Case 1: Multi-faculty author (changed faculties over time)**
- **Example:** Author was in Aerospace (2015-2020), moved to TPM (2020-present)
- **Solution:** Assign faculty based on **dataset publication date** (future enhancement)
- **Phase 2:** Assign most recent faculty, add note

**Case 2: Joint appointments**
- **Example:** Author affiliated with both EEMCS and Applied Sciences
- **Solution:** Phase 2 allows only 1 faculty_id per author
- **Workaround:** Assign primary faculty, document in notes

**Case 3: External collaborator misidentified as TU Delft**
- **Example:** Author has institution_id=28586 but actually external
- **Solution:** Update institution_id to correct value, skip faculty assignment

---

## 5. Quality Assurance

### 5.1 Post-Migration Validation Queries

**Validation 1: Coverage check**

```sparql
# What % of TU Delft authors have faculty_id?
SELECT 
    (COUNT(*) AS ?total_authors)
    (SUM(?has_faculty) AS ?with_faculty)
    (SUM(?has_faculty) * 100.0 / COUNT(*) AS ?coverage_pct)
WHERE {
    ?author djht:institution_id 28586 .
    BIND(EXISTS { ?author djht:faculty_id ?fid . } AS ?has_faculty)
}
```

**Target:** ≥85% coverage

**Validation 2: Registered author consistency**

```sparql
# All registered authors should have matching faculty_id
SELECT ?author_uuid ?author_faculty ?account_faculty
WHERE {
    ?author djht:account ?account .
    ?author djht:faculty_id ?author_faculty .
    ?account djht:faculty_id ?account_faculty .
    FILTER(?author_faculty != ?account_faculty)
    BIND(STRAFTER(STR(?author), "author:") AS ?author_uuid)
}
```

**Target:** 0 mismatches

**Validation 3: External author exclusion**

```sparql
# No external authors should have faculty_id
SELECT ?author_uuid ?institution_id ?faculty_id
WHERE {
    ?author djht:faculty_id ?faculty_id .
    ?author djht:institution_id ?institution_id .
    FILTER(?institution_id != 28586)
    BIND(STRAFTER(STR(?author), "author:") AS ?author_uuid)
}
```

**Target:** 0 external authors with faculty

### 5.2 Statistical Validation

```python
def validate_phase2_migration():
    """Run comprehensive validation suite."""
    
    results = {}
    
    # Check 1: Total authors migrated
    total_migrated = count_authors_with_faculty(institution_id=28586)
    total_tudelft = count_authors(institution_id=28586)
    coverage = total_migrated / total_tudelft
    
    results['coverage'] = {
        'total_authors': total_tudelft,
        'with_faculty': total_migrated,
        'percentage': coverage * 100,
        'target': 85.0,
        'status': 'PASS' if coverage >= 0.85 else 'FAIL'
    }
    
    # Check 2: Confidence distribution
    high_conf = count_authors_by_confidence(min_conf=0.8, institution_id=28586)
    medium_conf = count_authors_by_confidence(min_conf=0.5, max_conf=0.8, institution_id=28586)
    low_conf = count_authors_by_confidence(max_conf=0.5, institution_id=28586)
    
    results['confidence_distribution'] = {
        'high (≥0.8)': high_conf,
        'medium (0.5-0.8)': medium_conf,
        'low (<0.5)': low_conf,
        'high_percentage': (high_conf / total_migrated * 100) if total_migrated > 0 else 0,
        'target': 70.0,
        'status': 'PASS' if (high_conf / total_migrated) >= 0.70 else 'FAIL'
    }
    
    # Check 3: Faculty distribution
    faculty_counts = {}
    for faculty_id in range(285860001, 285860009):
        count = count_authors_by_faculty(faculty_id)
        faculty_name = get_faculty_name(faculty_id)
        faculty_counts[faculty_name] = count
    
    results['faculty_distribution'] = faculty_counts
    
    # Check 4: External author leakage
    external_with_faculty = count_authors_with_faculty(exclude_institution=28586)
    results['external_leakage'] = {
        'count': external_with_faculty,
        'target': 0,
        'status': 'PASS' if external_with_faculty == 0 else 'FAIL'
    }
    
    return results

# Example output:
# {
#     'coverage': {
#         'total_authors': 950,
#         'with_faculty': 825,
#         'percentage': 86.8,
#         'target': 85.0,
#         'status': 'PASS'
#     },
#     'confidence_distribution': {
#         'high (≥0.8)': 650,
#         'medium (0.5-0.8)': 150,
#         'low (<0.5)': 25,
#         'high_percentage': 78.8,
#         'target': 70.0,
#         'status': 'PASS'
#     },
#     'faculty_distribution': {
#         'Faculty of Aerospace Engineering': 120,
#         'Faculty of Architecture': 80,
#         'Faculty of Applied Sciences': 95,
#         ...
#     },
#     'external_leakage': {
#         'count': 0,
#         'target': 0,
#         'status': 'PASS'
#     }
# }
```

---

## 6. Rollback Plan

### 6.1 Backup Before Migration

```bash
# Create backup of RDF store before Phase 2
virtuoso-isql -U dba -P dba << EOF
checkpoint;
backup_context_clear();
backup_online('backup_phase2_pre_migration_', 1000);
EOF
```

### 6.2 Rollback Script

**Script:** `rollback_phase2_migration.py`

```python
#!/usr/bin/env python3
"""
Rollback Phase 2 author faculty assignments.
"""

def rollback_author_faculty_migration():
    """
    Remove all Phase 2 faculty assignments from Author entities.
    """
    query = """
    PREFIX djht: <https://data.4tu.nl/ontology/>
    
    DELETE {
        GRAPH <https://data.4tu.nl> {
            ?author djht:faculty_id ?faculty_id .
            ?author djht:faculty_confidence ?confidence .
            ?author djht:faculty_source ?source .
            ?author djht:faculty_assigned_date ?assigned_date .
        }
    }
    WHERE {
        GRAPH <https://data.4tu.nl> {
            ?author rdf:type djht:Author .
            OPTIONAL { ?author djht:faculty_id ?faculty_id . }
            OPTIONAL { ?author djht:faculty_confidence ?confidence . }
            OPTIONAL { ?author djht:faculty_source ?source . }
            OPTIONAL { ?author djht:faculty_assigned_date ?assigned_date . }
        }
    }
    """
    
    print("WARNING: This will delete ALL author faculty assignments!")
    confirm = input("Type 'ROLLBACK' to confirm: ")
    
    if confirm == 'ROLLBACK':
        execute_sparql_update(query)
        print("Rollback complete. All author faculty_id predicates removed.")
    else:
        print("Rollback cancelled.")

if __name__ == '__main__':
    rollback_author_faculty_migration()
```

---

## 7. Timeline & Resources

### 7.1 Migration Schedule

| Week | Phase | Tasks | Deliverables | Resources |
|------|-------|-------|--------------|-----------|
| 1 | 2A | Export registered authors, import from accounts | 150 authors migrated | 1 developer (8 hours) |
| 2 | 2B | Export unregistered, run pattern detection | Faculty detected for 800 authors | 1 developer (16 hours) |
| 3 | 2B | Auto-import high confidence (≥0.8) | ~600 authors auto-assigned | 1 developer (8 hours) |
| 4 | 2C | Manual review (medium/low confidence) | ~150 authors manually reviewed | 2 reviewers (20 hours each) |
| 5 | 2C/2D | Final imports, validation, QA | Migration complete, report | 1 developer + 1 QA (16 hours) |

**Total Effort:** ~100 person-hours (2.5 weeks full-time equivalent)

### 7.2 Resource Requirements

**Development:**
- 1 senior developer (familiar with SPARQL, Python, RDF)
- Access to production RDF store (read/write)
- Virtuoso backup capabilities

**Manual Review:**
- 2 institutional researchers or librarians
- Knowledge of TU Delft faculty structure
- Access to ORCID, Google Scholar, institutional directories

**Infrastructure:**
- Staging environment for migration testing
- Backup storage for pre-migration snapshot (~10GB)

---

## Summary

Phase 2 migration covers **3 author categories**:
1. **Registered authors** (150): Copy from account (100% accuracy)
2. **Unregistered high-confidence** (600): Auto-assign from Organizations (≥80% accuracy)
3. **Manual review** (200): Human verification (100% accuracy)

**Expected outcome:** 950 TU Delft authors with faculty_id (85-90% coverage)

---

**Next Document:** PHASE2_STATISTICS.md (Multi-valued queries and aggregation)

**Navigation:**
- Previous: PHASE2_DATA_MODEL.md
- Current: PHASE2_MIGRATION.md
- Next: PHASE2_STATISTICS.md
