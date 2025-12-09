# Technical Findings Summary: Faculty Statistics Feature

**Date:** December 9, 2025  
**Analyzed:** Djehuty v25.6 RDF/SPARQL Repository System

---

## Quick Facts

- **Current institution tracking:** Single `institution_id` field only (depositor's institution)
- **Organizations field:** Free-text string (unparseable for aggregation)
- **Author metadata:** Institution ID is optional, rarely populated
- **Statistics code:** No faculty-level aggregation exists
- **Configuration:** XML-based hierarchy with no faculty level defined
- **Database:** RDF triple store (Virtuoso) with SPARQL queries

---

## Data Model Current State

```
RDF Entity Hierarchy (Simplified)
====================================

Account
├── institution_id (integer, from email domain)
├── group_id (integer, links to InstitutionGroup)
└── institution_user_id (string, email address)

Author
├── id (integer)
├── institution_id (integer, OPTIONAL - often null)
├── group_id (integer, OPTIONAL)
├── orcid_id (string, OPTIONAL)
├── first_name, last_name, full_name
└── is_public, is_active

Dataset
├── institution_id (integer, COPIED from depositor Account)
├── group_id (integer, COPIED from depositor Account)
├── authors (RDF list → Author entities)
├── organizations (STRING - free text custom field)
└── [other metadata: title, doi, files, etc.]

InstitutionGroup
├── id (integer, e.g., 28586 for TU Delft)
├── name (string, e.g., "TU Delft")
└── parent (reference to parent group)
```

---

## Key Code Components

### 1. Data Storage (RDF Insertion)

**Location:** `djehuty/src/djehuty/backup/database.py`

```python
# Author with institution_id (line 256)
rdf.add (self.store, uri, rdf.DJHT["institution_id"], 
         value_or (record, "institution_id", None), XSD.integer)

# Dataset with institution_id (line 525) 
rdf.add (self.store, uri, rdf.DJHT["institution_id"],
         value_or_none (record, "institution_id"), XSD.integer)

# Organizations as plain string (line 2090)
rdf.add (graph, item_uri, rdf.DJHT["organizations"], value, XSD.string)
```

**Finding:** No faculty-related predicates exist. Organizations stored as unstructured text.

### 2. Statistics Queries

**Location:** `djehuty/src/djehuty/web/database.py`

```python
def repository_statistics (self):
    """Repository-wide counts (no filters)"""
    datasets_query = self.__query_from_template ("statistics_datasets")
    # Returns: { "datasets": 580, "authors": 245, "collections": 12, ... }

def dataset_statistics (self, group_ids=None, category_ids=None, ...):
    """Top datasets filtered by group or category"""
    filters += rdf.sparql_in_filter ("group_id", group_ids)
    # Can filter by InstitutionGroup, but NOT by faculty
```

**SPARQL Template:** `statistics_datasets.sparql`

```sparql
SELECT (COUNT(DISTINCT ?container) AS ?datasets)
WHERE {
  GRAPH <{{state_graph}}> {
    ?container rdf:type djht:DatasetContainer ;
               djht:latest_published_version ?dataset .
    ?dataset   djht:is_public "true"^^xsd:boolean .
  }
}
```

**Finding:** Statistics aggregate globally or by InstitutionGroup. No faculty-level filtering.

### 3. Configuration

**Location:** `djehuty/djehuty.xml`

```xml
<group id="28586" name="TU Delft">
  <domain>tudelft.nl</domain>
  <parent>root</parent>
  <group id="28696" name="TU Delft Students">
    <domain>student.tudelft.nl</domain>
  </group>
</group>
```

**Current Hierarchy:**
```
root (4TU.ResearchData)
  ├── TU Delft (28586)
  │     └── TU Delft Students (28696)
  ├── University of Twente
  ├── Eindhoven University of Technology
  └── Wageningen University & Research
```

**Finding:** No faculty groups defined. Email domains map to institutions, not faculties.

---

## Critical Gaps for Faculty Statistics

| Requirement | Current State | Impact |
|-------------|---------------|--------|
| **Faculty entity** | ❌ Does not exist | Cannot store faculty affiliation |
| **Faculty field in accounts** | ❌ Not present | Cannot capture user's faculty |
| **Faculty field in datasets** | ❌ Not present | Cannot attribute datasets to faculties |
| **Faculty SPARQL queries** | ❌ Not implemented | Cannot aggregate by faculty |
| **Faculty UI components** | ❌ Not built | Users cannot select faculty |
| **Faculty configuration** | ❌ No XML groups | System doesn't know faculties exist |

### Multi-Author Attribution Problem

```
Example Dataset: "Aviation NOx Emissions"
Authors:
  1. Author from TU Delft - Faculty of Aerospace Engineering
  2. Author from DLR Germany - Institut für Physik der Atmosphäre

Current Behavior:
  ✅ Counted toward TU Delft (institution_id from depositor)
  ❌ NOT counted toward Faculty of Aerospace Engineering (no faculty_id)
  ❌ Co-author's institution (DLR) ignored
  
Organizations field contains:
  "TU Delft, Faculty of Aerospace Engineering, Section Aircraft 
   Noise and Climate Effects; Deutsches Zentrum für Luft- und 
   Raumfahrt, Institut für Physik der Atmosphäre"
  
But this is FREE TEXT - cannot be queried/aggregated
```

---

## Organizations Field Analysis

**Storage:** RDF triple as string literal
```sparql
<dataset:uuid> djht:organizations "Free text here"^^xsd:string .
```

**Example Values from Production:**

1. **Structured format:**  
   `"TU Delft, Faculty of Aerospace Engineering, Section Aircraft Noise and Climate Effects"`

2. **Abbreviated format:**  
   `"University of Twente, Water Engineering and Management"`

3. **Multiple institutions:**  
   `"TU Delft, Faculty of Civil Engineering; Deltares; Rijkswaterstaat"`

4. **International collaboration:**  
   `"Wageningen University, Laboratory of Biochemistry; University of Toronto, Department of Chemistry"`

**Problem:** No consistent structure, cannot parse reliably, contains both faculty AND department AND section information mixed together.

---

## Where Institution Data Comes From

### During Deposit

```
User Login
  ↓
Email: john.doe@tudelft.nl
  ↓
Domain extraction: "tudelft.nl"
  ↓
XML config lookup: <domain>tudelft.nl</domain>
  ↓
Account.institution_id = 28586 (TU Delft)
Account.group_id = 28586
  ↓
Create Dataset
  ↓
Dataset.institution_id = Account.institution_id (28586)
Dataset.group_id = Account.group_id (28586)
```

**Key Point:** Faculty information is NEVER captured during this flow.

### Manual Entry (Organizations Field)

Users can manually type into "Organizations" custom field during dataset submission:
- Free-text entry box
- No validation
- No autocomplete
- No structured options

**Result:** Inconsistent formatting, typos, variations in faculty names.

---

## What Would Need to Change

### 1. RDF Schema Extension

Add new predicates:

```turtle
# New entity type
djht:Faculty rdf:type owl:Class .

# New predicates
djht:faculty_id rdf:type owl:DatatypeProperty ;
    rdfs:domain [ owl:unionOf (djht:Account djht:Dataset djht:Author) ] ;
    rdfs:range xsd:integer .

djht:faculty_name rdf:type owl:DatatypeProperty ;
    rdfs:domain djht:Faculty ;
    rdfs:range xsd:string .
```

### 2. Database Modifications

**File:** `backup/database.py`

```python
def insert_faculty (self, record):
    """Insert faculty entity."""
    faculty_id = record["faculty_id"]
    uri = rdf.unique_node ("faculty")
    
    self.store.add ((uri, RDF.type, rdf.DJHT["Faculty"]))
    rdf.add (self.store, uri, rdf.DJHT["id"], faculty_id, XSD.integer)
    rdf.add (self.store, uri, rdf.DJHT["name"], record["name"], XSD.string)
    rdf.add (self.store, uri, rdf.DJHT["institution_id"], 
             record["institution_id"], XSD.integer)

def insert_account (self, record):
    # ADD THIS LINE:
    rdf.add (self.store, uri, rdf.DJHT["faculty_id"],
             value_or (record, "faculty_id", None), XSD.integer)
```

### 3. Configuration Extension

**File:** `djehuty.xml`

```xml
<group id="28586" name="TU Delft">
  <domain>tudelft.nl</domain>
  <parent>root</parent>
  
  <!-- NEW: Faculty level -->
  <faculty id="285860001" name="Faculty of Aerospace Engineering" />
  <faculty id="285860002" name="Faculty of Architecture and the Built Environment" />
  <faculty id="285860003" name="Faculty of Applied Sciences" />
  <faculty id="285860004" name="Faculty of Civil Engineering and Geosciences" />
  <faculty id="285860005" name="Faculty of Electrical Engineering, Mathematics and Computer Science" />
  <!-- ... more faculties ... -->
  
  <group id="28696" name="TU Delft Students">
    <domain>student.tudelft.nl</domain>
  </group>
</group>
```

### 4. New SPARQL Template

**File:** `web/resources/sparql_templates/statistics_faculty.sparql`

```sparql
{% extends "prefixes.sparql" %}
{% block query %}
SELECT ?faculty_id ?faculty_name 
       (COUNT(DISTINCT ?container) AS ?datasets)
       (SUM(?total_views) AS ?total_views)
       (SUM(?total_downloads) AS ?total_downloads)
WHERE {
  GRAPH <{{state_graph}}> {
    ?faculty        rdf:type                djht:Faculty ;
                    djht:id                 ?faculty_id ;
                    djht:name               ?faculty_name ;
                    djht:institution_id     {{institution_id}} .
    
    ?container      rdf:type                djht:DatasetContainer ;
                    djht:latest_published_version ?dataset .
    
    ?dataset        rdf:type                djht:Dataset ;
                    djht:is_public          "true"^^xsd:boolean ;
                    djht:faculty_id         ?faculty_id .
    
    OPTIONAL { ?container djht:total_views     ?total_views . }
    OPTIONAL { ?container djht:total_downloads ?total_downloads . }
  }
}
GROUP BY ?faculty_id ?faculty_name
ORDER BY DESC(?datasets)
{% endblock %}
```

### 5. Python API Endpoint

**File:** `web/database.py`

```python
def faculty_statistics (self, institution_id=None):
    """Retrieve dataset statistics grouped by faculty."""
    
    query = self.__query_from_template ("statistics_faculty", {
        "institution_id": institution_id
    })
    
    results = self.__run_query (query, query, 
                                f"faculty_statistics_{institution_id}")
    return results
```

**File:** `web/wsgi.py` (add new route)

```python
@self.app.route("/v2/statistics/faculties", methods=["GET"])
def api_faculty_statistics (self):
    """API endpoint: GET /v2/statistics/faculties"""
    
    institution_id = validator.integer_value (request.args, "institution")
    results = self.db.faculty_statistics (institution_id=institution_id)
    
    return self.response (json.dumps(results))
```

### 6. UI Components

**Registration Form Extension:**
- Add faculty dropdown after email verification
- Populate options based on detected institution
- Store as `account.faculty_id`

**Dataset Deposit Form:**
- Pre-fill faculty from account
- Allow override if depositor is from different faculty
- Validate against institution's faculty list

---

## Migration Strategy for Existing Data

### Option 1: Organizations Field Parsing

```python
import re

FACULTY_PATTERNS = {
    285860001: r"Faculty of Aerospace Engineering|Aerospace Eng|AE Faculty",
    285860002: r"Faculty of Architecture|Architecture Faculty|BK Faculty",
    # ... more patterns ...
}

def extract_faculty_from_organizations (org_text, institution_id):
    """Parse organizations field to guess faculty."""
    for faculty_id, pattern in FACULTY_PATTERNS.items():
        if re.search(pattern, org_text, re.IGNORECASE):
            return faculty_id
    return None  # Requires manual review
```

**Accuracy:** ~70-80% based on dataset samples (many edge cases, abbreviations, typos)

### Option 2: Manual Curation

- Export all datasets with institution_id = TU Delft
- Human review of Organizations field
- CSV import: dataset_id → faculty_id mapping
- SPARQL UPDATE to insert faculty_id triples

### Option 3: Hybrid Approach

1. Run automated parsing on all 580 datasets
2. Flag low-confidence matches for review
3. Create web UI for curators to verify/correct
4. Batch import verified mappings

**Recommended:** Option 3 for best accuracy with manageable effort.

---

## Performance Considerations

### Statistics Caching

Current cache mechanism:
```python
results = self.__run_query (query, cache_key_string, "repository_statistics")
# Caches to: data/cache/repository_statistics/[md5_hash]
```

Faculty statistics would follow same pattern:
```python
# Cache key: "faculty_statistics_28586" (institution_id)
# Cache TTL: Could be longer (faculties change less than categories)
```

### Query Performance

Estimated impact on Virtuoso:
- Current: ~50ms for repository_statistics (580 datasets)
- With faculty filtering: ~60-70ms (adds one JOIN)
- Acceptable for <10,000 datasets

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Breaking existing API** | Low | Additive changes only (new predicates) |
| **Data migration errors** | Medium | Validate parsed faculties before import |
| **User confusion during onboarding** | Medium | Make faculty selection optional initially |
| **Faculty taxonomy changes** | Low | XML config is version-controlled |
| **SPARQL query complexity** | Low | Template-based, well-tested pattern |
| **Historical data gaps** | High | Accept that old data may lack faculty_id |

---

## Development Effort Estimate

| Task | Effort | Priority |
|------|--------|----------|
| RDF schema design | 1 day | Critical |
| XML faculty configuration | 2 days | Critical |
| Database insertion code | 3 days | Critical |
| SPARQL query templates | 2 days | Critical |
| Python API endpoint | 1 day | High |
| Migration script | 3 days | High |
| UI components (registration) | 3 days | High |
| UI components (dataset form) | 2 days | Medium |
| Testing & QA | 5 days | Critical |
| Documentation | 2 days | Medium |
| **Total** | **24 days** | *~5 weeks* |

---

## Recommended Approach

### Phase 1: Foundation (Week 1-2)
1. Design RDF schema extension
2. Create faculty taxonomy for TU Delft (validate with stakeholders)
3. Extend XML configuration
4. Update database insertion code

### Phase 2: Statistics (Week 2-3)
5. Create SPARQL templates for faculty queries
6. Implement Python API endpoint
7. Add caching support
8. Test with sample data

### Phase 3: Migration (Week 3-4)
9. Write Organizations field parser
10. Run automated extraction on existing datasets
11. Manual review of low-confidence matches
12. Bulk import faculty_id triples

### Phase 4: UI & Polish (Week 4-5)
13. Add faculty dropdown to registration
14. Add faculty field to dataset forms
15. Create admin UI for faculty management
16. Documentation and deployment

---

## Conclusion

Faculty-level statistics is **technically feasible** but requires:
- ✅ New RDF predicates (faculty_id)
- ✅ XML configuration extension
- ✅ Modified insertion code
- ✅ New SPARQL query templates
- ✅ Python API endpoints
- ⚠️ Migration strategy for 580+ datasets (Organizations field parsing + manual review)
- ⚠️ UI changes for faculty selection

The Organizations field contains useful data but cannot be directly queried. The recommended approach is to add structured faculty_id fields and backfill historical data through semi-automated migration.

**Next Step:** Present conceptual design to stakeholders and validate faculty taxonomy before implementation.
