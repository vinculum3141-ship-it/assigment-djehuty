# Phase 2: Data Model Extensions

**Document:** PHASE2_DATA_MODEL.md  
**Part of:** Phase 2 Solution Architecture (Author-Level Faculty Statistics)  
**Prerequisites:** Phase 1 complete, read PHASE2_OVERVIEW.md first

---

## Table of Contents

1. RDF Schema Extensions
2. Entity Relationships
3. Faculty Assignment Semantics
4. Confidence Scoring Model
5. Code Examples
6. Migration Mappings
7. Validation Rules

---

## 1. RDF Schema Extensions

### 1.1 New Predicates on Author Entity

**Add these predicates to `djht:Author`:**

```turtle
# Namespace definition
@prefix djht: <https://data.4tu.nl/ontology/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2001/XMLSchema#> .

# Faculty ID predicate (NEW for Phase 2)
djht:faculty_id a rdf:Property ;
    rdfs:domain djht:Author ;
    rdfs:range xsd:integer ;
    rdfs:label "Faculty ID" ;
    rdfs:comment "Links author to their faculty affiliation. Optional. Can differ from depositor's faculty for co-authors." .

# Faculty confidence score (NEW for Phase 2)
djht:faculty_confidence a rdf:Property ;
    rdfs:domain djht:Author ;
    rdfs:range xsd:float ;
    rdfs:label "Faculty Assignment Confidence" ;
    rdfs:comment "Confidence score (0.0-1.0) for auto-assigned faculty. 1.0 = manually verified or from account." .

# Faculty assignment source (NEW for Phase 2)
djht:faculty_source a rdf:Property ;
    rdfs:domain djht:Author ;
    rdfs:range xsd:string ;
    rdfs:label "Faculty Assignment Source" ;
    rdfs:comment "How faculty was assigned: 'account', 'organizations_auto', 'organizations_manual', 'orcid', 'manual_review'" .

# Faculty assignment date (NEW for Phase 2)
djht:faculty_assigned_date a rdf:Property ;
    rdfs:domain djht:Author ;
    rdfs:range xsd:dateTime ;
    rdfs:label "Faculty Assignment Date" ;
    rdfs:comment "When faculty_id was assigned (for audit trail)" .
```

### 1.2 Complete Author Entity Schema (Phase 2)

```turtle
# Author entity with all predicates (Phase 1 + Phase 2)
djht:Author a rdfs:Class ;
    rdfs:label "Author" ;
    rdfs:comment "Represents a person who authored or contributed to a dataset. May or may not have a registered account." .

# Existing predicates (from Phase 1)
djht:id                  # Author ID (integer)
djht:first_name          # First name (string, optional)
djht:last_name           # Last name (string, optional)
djht:full_name           # Full name (string, required)
djht:email               # Email (string, optional)
djht:orcid_id            # ORCID (string, optional)
djht:institution_id      # Institution ID (integer, optional)
djht:group_id            # Institution group ID (integer, optional)
djht:is_active           # Active flag (boolean)
djht:is_public           # Public visibility (boolean)
djht:job_title           # Job title (string, optional)
djht:url_name            # URL slug (string, optional)
djht:created_by          # Account that created this author record (URI)
djht:account             # Linked account (URI, optional - only if registered)

# NEW predicates (Phase 2)
djht:faculty_id          # Faculty ID (integer, optional)
djht:faculty_confidence  # Confidence score (float 0.0-1.0, optional)
djht:faculty_source      # Assignment source (string, optional)
djht:faculty_assigned_date # Assignment timestamp (dateTime, optional)
```

---

## 2. Entity Relationships

### 2.1 Author-Faculty Relationship

```turtle
# Example: Registered author (faculty from account)
<author:12345> a djht:Author ;
    djht:full_name "Dr. Jane Smith" ;
    djht:email "j.smith@tudelft.nl" ;
    djht:orcid_id "0000-0003-1234-5678" ;
    djht:institution_id 28586 ;
    djht:account <account:67890> ;
    djht:faculty_id 285860001 ;          # Aerospace Engineering
    djht:faculty_confidence "1.0"^^xsd:float ;
    djht:faculty_source "account" ;
    djht:faculty_assigned_date "2025-12-09T10:30:00Z"^^xsd:dateTime .

# The linked account also has faculty_id (from Phase 1)
<account:67890> a djht:Account ;
    djht:email "j.smith@tudelft.nl" ;
    djht:faculty_id 285860001 ;          # Same as author
    djht:institution_id 28586 .

# The faculty entity
<faculty:285860001> a djht:Faculty ;
    djht:id 285860001 ;
    djht:name "Faculty of Aerospace Engineering" ;
    djht:short_name "Aerospace" ;
    djht:institution_id 28586 .
```

```turtle
# Example: Unregistered author (faculty from Organizations parsing)
<author:23456> a djht:Author ;
    djht:full_name "Hebly, Scott J." ;
    djht:institution_id 28586 ;
    djht:faculty_id 285860001 ;          # Aerospace Engineering
    djht:faculty_confidence "0.85"^^xsd:float ;  # Auto-detected
    djht:faculty_source "organizations_auto" ;
    djht:faculty_assigned_date "2025-12-09T11:15:00Z"^^xsd:dateTime .
    # NO djht:account (unregistered)
    # NO email or ORCID (unknown)
```

```turtle
# Example: External author (not in faculty statistics)
<author:34567> a djht:Author ;
    djht:full_name "Dr. Hans Garcia" ;
    djht:institution_id 99999 ;          # DLR Germany
    # NO faculty_id (external institution)
    # NO djht:account
```

### 2.2 Dataset-Author-Faculty Chain

```turtle
# Dataset with multiple authors from different faculties
<dataset:aviation-nox> a djht:Dataset ;
    djht:title "Aviation NOx Emissions Modeling" ;
    djht:institution_id 28586 ;
    djht:container <container:abc123> ;
    djht:authors (
        <author:12345>    # Faculty of Aerospace (registered)
        <author:23456>    # Faculty of Aerospace (unregistered)
        <author:45678>    # Faculty of EEMCS (registered)
        <author:34567>    # External (DLR Germany)
    ) .

<container:abc123> djht:account <account:67890> .  # Depositor

# Query: Which faculties authored this dataset?
SELECT DISTINCT ?faculty_name
WHERE {
    <dataset:aviation-nox> djht:authors/rdf:rest*/rdf:first ?author .
    ?author djht:faculty_id ?faculty_id .
    ?faculty djht:id ?faculty_id ;
             djht:name ?faculty_name .
}
# Result: 
# - Faculty of Aerospace Engineering
# - Faculty of EEMCS
# (External author excluded - no faculty_id)
```

---

## 3. Faculty Assignment Semantics

### 3.1 Assignment Rules

**Rule 1: Registered authors (have `djht:account`)**
- Faculty MUST be copied from account's `faculty_id` (set in Phase 1)
- Confidence = 1.0 (verified)
- Source = "account"

**Rule 2: Unregistered authors with institution_id = 28586 (TU Delft)**
- Faculty extracted from dataset's Organizations field
- Confidence = 0.5-0.9 (pattern-based)
- Source = "organizations_auto" or "organizations_manual"

**Rule 3: Unregistered authors with institution_id ≠ 28586 (external)**
- NO faculty_id assigned
- Excluded from faculty statistics

**Rule 4: Authors with ORCID but no account**
- FUTURE: Query ORCID API for affiliation
- Source = "orcid"
- For Phase 2, treat as Rule 2

### 3.2 Confidence Levels

| Confidence Range | Meaning | Action | Examples |
|------------------|---------|--------|----------|
| 1.0 | Verified | Auto-assign | Copied from account, manually reviewed |
| 0.8-0.99 | High confidence | Auto-assign | "Faculty of Aerospace Engineering" in Organizations |
| 0.5-0.79 | Medium confidence | Manual review | "Aerospace" (abbreviation), partial match |
| 0.1-0.49 | Low confidence | Manual review | Ambiguous text, multiple faculties mentioned |
| 0.0 | No match | Leave null | Organizations field empty or unrelated |

---

## 4. Confidence Scoring Model

### 4.1 Pattern Matching Algorithm

```python
def calculate_faculty_confidence(organizations_text, faculty_id):
    """
    Calculate confidence score for faculty assignment based on Organizations field.
    
    Args:
        organizations_text: Free-text Organizations field
        faculty_id: Candidate faculty ID
    
    Returns:
        float: Confidence score 0.0-1.0
    """
    if not organizations_text:
        return 0.0
    
    score = 0.0
    
    # Get faculty patterns from configuration
    patterns = FACULTY_PATTERNS[faculty_id]
    
    # Pattern matching with weights
    for pattern in patterns:
        if re.search(pattern['regex'], organizations_text, re.IGNORECASE):
            score += pattern['weight']
    
    # Bonus for exact institutional structure
    if re.search(r'TU Delft.*Faculty of', organizations_text):
        score += 0.2
    
    # Penalty for multiple faculty mentions
    faculty_mentions = count_faculty_mentions(organizations_text)
    if faculty_mentions > 1:
        score *= 0.7  # Ambiguous
    
    # Penalty for external institution mentions
    external_mentions = count_external_institutions(organizations_text)
    if external_mentions > 0:
        score *= 0.8
    
    # Clamp to 0.0-1.0 range
    return min(max(score, 0.0), 1.0)
```

### 4.2 Pattern Library Structure

```python
FACULTY_PATTERNS = {
    285860001: {  # Aerospace Engineering
        'patterns': [
            {'regex': r'Faculty of Aerospace Engineering', 'weight': 0.9},
            {'regex': r'Aerospace Engineering', 'weight': 0.7},
            {'regex': r'\bAE\b', 'weight': 0.5},
            {'regex': r'Flight Performance and Propulsion', 'weight': 0.6},
            {'regex': r'Aircraft Noise', 'weight': 0.5},
            {'regex': r'Control and Simulation', 'weight': 0.5},
        ],
        'exclusions': [
            r'Faculty of EEMCS',  # Exclude if other faculty mentioned
        ]
    },
    285860005: {  # EEMCS
        'patterns': [
            {'regex': r'Faculty of Electrical Engineering, Mathematics and Computer Science', 'weight': 0.95},
            {'regex': r'Faculty of EEMCS', 'weight': 0.9},
            {'regex': r'\bEEMCS\b', 'weight': 0.7},
            {'regex': r'\bEWI\b', 'weight': 0.7},
            {'regex': r'Computer Science', 'weight': 0.6},
            {'regex': r'Electrical Engineering', 'weight': 0.6},
        ],
        'exclusions': []
    },
    # ... other faculties
}
```

---

## 5. Code Examples

### 5.1 Insert Author with Faculty (Python)

```python
def insert_author_with_faculty(self, first_name=None, last_name=None, 
                                full_name=None, institution_id=None,
                                account_uuid=None, faculty_id=None,
                                faculty_confidence=None, faculty_source=None):
    """
    Insert author with Phase 2 faculty fields.
    
    If account_uuid provided, faculty_id should be copied from account.
    """
    graph = Graph()
    author_uri = rdf.unique_node("author")
    
    # Basic author properties (Phase 1)
    rdf.add(graph, author_uri, RDF.type, rdf.DJHT["Author"], "uri")
    rdf.add(graph, author_uri, rdf.DJHT["first_name"], first_name, XSD.string)
    rdf.add(graph, author_uri, rdf.DJHT["last_name"], last_name, XSD.string)
    rdf.add(graph, author_uri, rdf.DJHT["full_name"], full_name, XSD.string)
    rdf.add(graph, author_uri, rdf.DJHT["institution_id"], institution_id)
    
    # Link to account if registered
    if account_uuid is not None:
        account_uri = URIRef(rdf.uuid_to_uri(account_uuid, "account"))
        rdf.add(graph, author_uri, rdf.DJHT["account"], account_uri, "uri")
        
        # If account has faculty_id, copy it to author (Phase 2)
        if faculty_id is None:
            faculty_id = self.get_account_faculty_id(account_uuid)
        if faculty_id is not None:
            faculty_confidence = 1.0  # From account = verified
            faculty_source = "account"
    
    # Phase 2 faculty fields (optional)
    if faculty_id is not None:
        rdf.add(graph, author_uri, rdf.DJHT["faculty_id"], faculty_id)
        rdf.add(graph, author_uri, rdf.DJHT["faculty_confidence"], 
                faculty_confidence or 1.0, XSD.float)
        rdf.add(graph, author_uri, rdf.DJHT["faculty_source"], 
                faculty_source or "manual", XSD.string)
        rdf.add(graph, author_uri, rdf.DJHT["faculty_assigned_date"], 
                datetime.now(timezone.utc), XSD.dateTime)
    
    if self.add_triples_from_graph(graph):
        return rdf.uri_to_uuid(author_uri)
    
    return None
```

### 5.2 Update Author Faculty (SPARQL)

**File:** `update_author_faculty.sparql`

```sparql
{% extends "prefixes.sparql" %}
{% block query %}
DELETE {
  GRAPH <{{state_graph}}> {
    ?author djht:faculty_id              ?old_faculty_id .
    ?author djht:faculty_confidence      ?old_confidence .
    ?author djht:faculty_source          ?old_source .
    ?author djht:faculty_assigned_date   ?old_date .
  }
}
INSERT {
  GRAPH <{{state_graph}}> {
    ?author djht:faculty_id              {{faculty_id}} .
    ?author djht:faculty_confidence      "{{faculty_confidence}}"^^xsd:float .
    ?author djht:faculty_source          "{{faculty_source}}"^^xsd:string .
    ?author djht:faculty_assigned_date   "{{assigned_date}}"^^xsd:dateTime .
  }
}
WHERE {
  GRAPH <{{state_graph}}> {
    ?author rdf:type djht:Author .
    OPTIONAL { ?author djht:faculty_id ?old_faculty_id . }
    OPTIONAL { ?author djht:faculty_confidence ?old_confidence . }
    OPTIONAL { ?author djht:faculty_source ?old_source . }
    OPTIONAL { ?author djht:faculty_assigned_date ?old_date . }
  }
  FILTER (?author = <author:{{author_uuid}}>)
}
{% endblock %}
```

### 5.3 Query Authors by Faculty

**File:** `authors_by_faculty.sparql`

```sparql
{% extends "prefixes.sparql" %}
{% block query %}
SELECT DISTINCT ?author_uuid ?full_name ?institution_id 
                ?faculty_id ?faculty_confidence ?faculty_source
                ?email ?orcid_id ?has_account
WHERE {
  GRAPH <{{state_graph}}> {
    ?author rdf:type djht:Author .
    ?author djht:full_name ?full_name .
    
    # Faculty filter (Phase 2)
    {%- if faculty_id is not none %}
    ?author djht:faculty_id {{faculty_id}} .
    {%- endif %}
    
    OPTIONAL { ?author djht:institution_id ?institution_id . }
    OPTIONAL { ?author djht:faculty_id ?faculty_id . }
    OPTIONAL { ?author djht:faculty_confidence ?faculty_confidence . }
    OPTIONAL { ?author djht:faculty_source ?faculty_source . }
    OPTIONAL { ?author djht:email ?email . }
    OPTIONAL { ?author djht:orcid_id ?orcid_id . }
    
    # Check if registered
    BIND(EXISTS { ?author djht:account ?account . } AS ?has_account)
    
    BIND(STRAFTER(STR(?author), "author:") AS ?author_uuid)
  }
  
  {%- if min_confidence is not none %}
  FILTER (?faculty_confidence >= {{min_confidence}})
  {%- endif %}
  
  {%- if only_tu_delft %}
  FILTER (?institution_id = 28586)
  {%- endif %}
}
ORDER BY ?full_name
{% endblock %}
```

---

## 6. Migration Mappings

### 6.1 Author Types and Migration Strategies

```python
AUTHOR_MIGRATION_STRATEGIES = {
    'registered_with_faculty': {
        'description': 'Author has account with faculty_id from Phase 1',
        'query': '''
            SELECT ?author_uuid ?account_uuid ?faculty_id
            WHERE {
                ?author djht:account ?account .
                ?account djht:faculty_id ?faculty_id .
                BIND(STRAFTER(STR(?author), "author:") AS ?author_uuid)
                BIND(STRAFTER(STR(?account), "account:") AS ?account_uuid)
            }
        ''',
        'action': 'copy_from_account',
        'confidence': 1.0,
        'source': 'account',
        'estimated_count': 150  # ~150 registered TU Delft authors
    },
    
    'registered_without_faculty': {
        'description': 'Author has account but account has no faculty_id',
        'query': '''
            SELECT ?author_uuid ?account_uuid
            WHERE {
                ?author djht:account ?account .
                FILTER NOT EXISTS { ?account djht:faculty_id ?fid . }
                BIND(STRAFTER(STR(?author), "author:") AS ?author_uuid)
                BIND(STRAFTER(STR(?account), "account:") AS ?account_uuid)
            }
        ''',
        'action': 'manual_review',  # Ask user to update account first
        'confidence': None,
        'source': 'manual_review',
        'estimated_count': 50
    },
    
    'unregistered_tu_delft': {
        'description': 'No account, institution_id = 28586',
        'query': '''
            SELECT ?author_uuid ?full_name ?institution_id
            WHERE {
                ?author djht:institution_id 28586 .
                FILTER NOT EXISTS { ?author djht:account ?acc . }
                ?author djht:full_name ?full_name .
                BIND(STRAFTER(STR(?author), "author:") AS ?author_uuid)
            }
        ''',
        'action': 'parse_organizations',  # Main migration task
        'confidence': 'variable',  # 0.5-0.9 depending on pattern match
        'source': 'organizations_auto',
        'estimated_count': 800  # Majority of authors
    },
    
    'unregistered_external': {
        'description': 'No account, institution_id ≠ 28586 or null',
        'query': '''
            SELECT ?author_uuid ?full_name ?institution_id
            WHERE {
                ?author djht:full_name ?full_name .
                FILTER NOT EXISTS { ?author djht:account ?acc . }
                OPTIONAL { ?author djht:institution_id ?institution_id . }
                FILTER (!BOUND(?institution_id) || ?institution_id != 28586)
                BIND(STRAFTER(STR(?author), "author:") AS ?author_uuid)
            }
        ''',
        'action': 'skip',  # Don't assign faculty to external authors
        'confidence': None,
        'source': None,
        'estimated_count': 300
    }
}
```

### 6.2 Organizations Field Parsing Workflow

```
                        ┌─────────────────────┐
                        │  Author Entity      │
                        │  (unregistered)     │
                        └──────────┬──────────┘
                                   │
                        ┌──────────▼──────────┐
                        │ Get Datasets        │
                        │ Where Author Listed │
                        └──────────┬──────────┘
                                   │
                        ┌──────────▼──────────┐
                        │ Collect All         │
                        │ Organizations Fields│
                        └──────────┬──────────┘
                                   │
                        ┌──────────▼──────────┐
                        │ Run Pattern Matcher │
                        │ on Each Field       │
                        └──────────┬──────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
         ┌──────────▼────┐  ┌─────▼─────┐  ┌────▼─────┐
         │ High Confidence│  │  Medium   │  │   Low    │
         │   (≥0.8)      │  │ (0.5-0.8) │  │  (<0.5)  │
         └──────────┬────┘  └─────┬─────┘  └────┬─────┘
                    │              │              │
         ┌──────────▼────┐  ┌─────▼──────┐ ┌────▼──────┐
         │ Auto-Assign    │  │ Manual     │ │ Manual    │
         │ faculty_id     │  │ Review     │ │ Review    │
         └───────────────┘  └────────────┘ └───────────┘
```

---

## 7. Validation Rules

### 7.1 Data Integrity Constraints

```sparql
# Rule 1: Author with faculty_id MUST have institution_id = 28586
SELECT ?author_uuid ?faculty_id ?institution_id
WHERE {
    ?author djht:faculty_id ?faculty_id .
    OPTIONAL { ?author djht:institution_id ?institution_id . }
    FILTER (!BOUND(?institution_id) || ?institution_id != 28586)
    BIND(STRAFTER(STR(?author), "author:") AS ?author_uuid)
}
# Expected result: EMPTY (no violations)
```

```sparql
# Rule 2: faculty_id MUST reference existing Faculty entity
SELECT ?author_uuid ?faculty_id
WHERE {
    ?author djht:faculty_id ?faculty_id .
    FILTER NOT EXISTS {
        ?faculty djht:id ?faculty_id .
    }
    BIND(STRAFTER(STR(?author), "author:") AS ?author_uuid)
}
# Expected result: EMPTY (all faculty IDs valid)
```

```sparql
# Rule 3: Registered author faculty_id MUST match account faculty_id
SELECT ?author_uuid ?author_faculty ?account_faculty
WHERE {
    ?author djht:account ?account .
    ?author djht:faculty_id ?author_faculty .
    ?account djht:faculty_id ?account_faculty .
    FILTER (?author_faculty != ?account_faculty)
    BIND(STRAFTER(STR(?author), "author:") AS ?author_uuid)
}
# Expected result: EMPTY (no mismatches)
```

```sparql
# Rule 4: faculty_confidence MUST be between 0.0 and 1.0
SELECT ?author_uuid ?faculty_confidence
WHERE {
    ?author djht:faculty_confidence ?faculty_confidence .
    FILTER (?faculty_confidence < 0.0 || ?faculty_confidence > 1.0)
    BIND(STRAFTER(STR(?author), "author:") AS ?author_uuid)
}
# Expected result: EMPTY (all valid)
```

### 7.2 Statistical Validation

```python
def validate_migration_results():
    """
    Validate Phase 2 migration completed successfully.
    """
    validations = []
    
    # Check 1: TU Delft author coverage
    total_tudelft_authors = count_authors_by_institution(28586)
    authors_with_faculty = count_authors_with_faculty(28586)
    coverage = authors_with_faculty / total_tudelft_authors
    
    validations.append({
        'check': 'TU Delft author coverage',
        'target': 0.85,
        'actual': coverage,
        'status': 'PASS' if coverage >= 0.85 else 'FAIL'
    })
    
    # Check 2: High confidence assignments
    high_confidence_count = count_authors_by_confidence(min_confidence=0.8)
    high_confidence_ratio = high_confidence_count / authors_with_faculty
    
    validations.append({
        'check': 'High confidence ratio',
        'target': 0.70,  # At least 70% should be high confidence
        'actual': high_confidence_ratio,
        'status': 'PASS' if high_confidence_ratio >= 0.70 else 'FAIL'
    })
    
    # Check 3: No external authors with faculty_id
    external_with_faculty = count_external_authors_with_faculty()
    
    validations.append({
        'check': 'External authors excluded',
        'target': 0,
        'actual': external_with_faculty,
        'status': 'PASS' if external_with_faculty == 0 else 'FAIL'
    })
    
    # Check 4: Registered author consistency
    mismatched_accounts = count_author_account_faculty_mismatches()
    
    validations.append({
        'check': 'Account-Author faculty consistency',
        'target': 0,
        'actual': mismatched_accounts,
        'status': 'PASS' if mismatched_accounts == 0 else 'FAIL'
    })
    
    return validations
```

---

## Summary

### Phase 2 Data Model Additions

1. **4 new predicates** on `djht:Author`:
   - `faculty_id` (integer, optional)
   - `faculty_confidence` (float 0.0-1.0, optional)
   - `faculty_source` (string, optional)
   - `faculty_assigned_date` (dateTime, optional)

2. **3 faculty assignment sources**:
   - "account" (confidence 1.0) - from registered user
   - "organizations_auto" (confidence 0.5-0.9) - pattern matching
   - "manual_review" (confidence 1.0) - human verified

3. **~1,000 author entities** to migrate (TU Delft only):
   - 150 registered (copy from account)
   - 800 unregistered (parse Organizations)
   - 50 edge cases (manual review)

4. **Validation**: 4 integrity rules + 4 statistical checks

---

**Next Document:** PHASE2_MIGRATION.md (Migration scripts and workflow)

**Navigation:**
- Previous: PHASE2_OVERVIEW.md
- Current: PHASE2_DATA_MODEL.md
- Next: PHASE2_MIGRATION.md
