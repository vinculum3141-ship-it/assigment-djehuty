# Codebase Analysis: Institution/Author Data Storage & Processing

**Analysis Date:** December 9, 2025  
**Purpose:** Understand how institution and author data is stored/processed in Djehuty to design faculty-level statistics feature

---

## Executive Summary

The Djehuty system stores institution/author data in an RDF triple store (Virtuoso) using SPARQL queries. **Institution affiliation is tracked at only ONE level** - the depositing account's institution. The "Organizations" field is a free-text custom field stored as a string literal, not a structured entity.

### Critical Findings

1. **Institution tracking is single-point**: Only `institution_id` from depositor's account
2. **Authors have institution_id but it's optional**: Not always populated
3. **Organizations field is unstructured text**: Stored as `djht:organizations` string literal
4. **No faculty-level entity exists**: Current hierarchy only has Account → Institution → Group
5. **Statistics aggregate at institution level only**: No code paths for sub-institution breakdowns

---

## 1. Data Model: RDF Schema

### 1.1 Core Entities

The system uses custom DJHT (Djehuty) ontology predicates:

```sparql
# Account entity
?account rdf:type djht:Account
?account djht:institution_id ?institution_id  # Links to Institution entity
?account djht:group_id ?group_id             # Links to InstitutionGroup
?account djht:institution_user_id ?email     # e.g., "user@tudelft.nl"

# Author entity  
?author rdf:type djht:Author
?author djht:id ?author_id
?author djht:institution_id ?institution_id   # OPTIONAL - often null
?author djht:group_id ?group_id               # OPTIONAL
?author djht:first_name ?first_name
?author djht:last_name ?last_name
?author djht:orcid_id ?orcid_id              # OPTIONAL

# Dataset entity
?dataset rdf:type djht:Dataset
?dataset djht:institution_id ?institution_id  # From depositor's account
?dataset djht:group_id ?group_id              # From depositor's account
?dataset djht:authors ?authors                # RDF list of Author entities
?dataset djht:organizations ?organizations    # FREE-TEXT STRING (custom field)
```

**Key Insight:** The `djht:organizations` field is NOT an RDF relationship to structured entities. It's a plain string literal containing free-text like:

```
"TU Delft, Faculty of Aerospace Engineering, Section Aircraft Noise..."
```

---

## 2. Storage Locations

### 2.1 Author Data Storage

**File:** `djehuty/src/djehuty/backup/database.py`  
**Function:** `insert_author()` (lines 238-267)

```python
def insert_author (self, record):
    """Procedure to insert an author record."""
    
    author_id = value_or_none (record, "id")
    uri = self.record_uri ("Author", "id", author_id)
    
    # Key institutional fields:
    rdf.add (self.store, uri, rdf.DJHT["institution_id"], 
             value_or (record, "institution_id", None), XSD.integer)
    rdf.add (self.store, uri, rdf.DJHT["group_id"],
             value_or (record, "group_id", None), XSD.integer)
    rdf.add (self.store, uri, rdf.DJHT["orcid_id"],
             value_or (record, "orcid_id", None), XSD.string)
```

**Observations:**
- `institution_id` is optional (can be `None`)
- No faculty-level field exists
- `group_id` refers to InstitutionGroup, not faculty
- Authors are stored as separate entities linked to datasets via RDF lists

### 2.2 Dataset Institutional Affiliation

**File:** `djehuty/src/djehuty/backup/database.py`  
**Function:** `insert_collection()` / dataset insertion (lines 500-530)

```python
# Dataset institutional metadata
rdf.add (self.store, uri, rdf.DJHT["institution_id"], 
         value_or_none (record, "institution_id"), XSD.integer)
rdf.add (self.store, uri, rdf.DJHT["group_id"],
         value_or_none (record, "group_id"), XSD.integer)

# Authors list (separate from institution_id)
self.insert_author_list (uri, value_or (record, "authors", []))
```

**Critical Issue:** The dataset's `institution_id` comes from the **depositor's account**, NOT from co-authors. Multi-institutional datasets only count toward depositor's institution.

### 2.3 Organizations Custom Field

**File:** `djehuty/src/djehuty/backup/database.py`  
**Function:** `handle_custom_fields()` (lines 476-484)

```python
# Replace contributors by organizations and (optional) contributors
if field['name'] == 'Contributors':
    try:
        extra = self.extra_contributors_organizations[item_type][item_id][version]
        contributors = extra['contributors']
        if contributors:
            field['value'] = contributors
            self.insert_custom_field (uri, field)
        field = {'name': 'Organizations', 'value': extra['organizations']}
    except KeyError:
        pass
```

**Data Source:** External JSON file at `djehuty/src/djehuty/backup/resources/contributors_organizations.json`  
This contains manual mappings for legacy Figshare data migration.

**File:** `djehuty/src/djehuty/web/database.py`  
**Function:** `insert_custom_field_value()` (lines 2070-2092)

```python
def insert_custom_field_value (self, name=None, value=None,
                               item_uri=None, graph=None):
    """Procedure to add a custom field value to the state graph."""
    
    allowed_custom_fields = [ "contributors", "data_link", "derived_from",
                              "format", "geolocation", "language",
                              "latitude", "license_remarks", "longitude",
                              "organizations", "publisher", "same_as",
                              "time_coverage" ]
    
    name = conv.custom_field_name (name)
    if name.lower() not in allowed_custom_fields:
        self.log.warning ("Blocked inserting custom field '%s'", name)
        return False
    
    rdf.add (graph, item_uri, rdf.DJHT[name], value, XSD.string)
    return True
```

**Key Points:**
- "organizations" is a whitelisted custom field name
- Stored as `XSD.string` (plain text, not structured)
- No validation or parsing of faculty information
- Direct RDF triple: `<dataset_uri> djht:organizations "Free text here"^^xsd:string`

---

## 3. Data Retrieval & Processing

### 3.1 SPARQL Query Templates

**File:** `djehuty/src/djehuty/web/resources/sparql_templates/datasets.sparql` (line 151)

```sparql
OPTIONAL { ?dataset djht:organizations ?organizations . }
```

The organizations field is retrieved as-is with no parsing or structuring.

**File:** `djehuty/src/djehuty/web/resources/sparql_templates/authors.sparql` (lines 47-50)

```sparql
OPTIONAL { ?author djht:institution_id ?institution_id . }
OPTIONAL { ?author djht:group_id ?group_id . }
OPTIONAL { ?author djht:orcid_id ?orcid_id . }
```

Authors can have `institution_id` but it's rarely populated in practice.

### 3.2 Statistics Aggregation

**File:** `djehuty/src/djehuty/web/database.py`  
**Function:** `repository_statistics()` (lines 512-547)

```python
def repository_statistics (self):
    """Procedure to retrieve repository-wide statistics."""
    
    datasets_query    = self.__query_from_template ("statistics_datasets")
    collections_query = self.__query_from_template ("statistics_collections")
    authors_query     = self.__query_from_template ("statistics_authors")
    
    datasets    = self.__run_query (datasets_query, datasets_query, "repository_statistics")
    authors     = self.__run_query (authors_query, authors_query, "repository_statistics")
    collections = self.__run_query (collections_query, collections_query, "repository_statistics")
    files       = self.repository_file_statistics (use_cache=True)
    
    row = { **datasets[0], **authors[0], **collections[0], **files_results }
    return row
```

**SPARQL Template:** `statistics_datasets.sparql`

```sparql
SELECT (COUNT(DISTINCT ?container) AS ?datasets)
WHERE {
  GRAPH <{{state_graph}}> {
    ?container rdf:type djht:DatasetContainer ;
               djht:latest_published_version ?dataset .
    ?dataset   rdf:type djht:Dataset ;
               djht:is_public "true"^^xsd:boolean .
  }
}
```

**Critical Gap:** No filtering by `institution_id` or `group_id` - this is repository-wide only.

**File:** `djehuty/src/djehuty/web/database.py`  
**Function:** `dataset_statistics()` (lines 549-570)

```python
def dataset_statistics (self, item_type="downloads",
                              order="downloads",
                              order_direction="desc",
                              group_ids=None,         # ← GROUP filtering exists
                              category_ids=None,       # ← CATEGORY filtering exists
                              limit=10,
                              offset=0):
    """Procedure to retrieve dataset statistics."""
    
    filters = ""
    filters += rdf.sparql_in_filter ("category_id", category_ids)
    filters += rdf.sparql_in_filter ("group_id", group_ids)
```

**Finding:** Statistics CAN be filtered by `group_ids`, but "group" means InstitutionGroup (e.g., "TU Delft Students"), NOT faculty.

### 3.3 Search Functionality

**File:** `djehuty/src/djehuty/web/database.py`  
**Function:** `__search_query_to_sparql_filters_v2()` (lines 373-393)

```python
# Search fields include organizations as plain text
fields = ["title", "resource_title", "description", "tag", "organizations"]
for field in fields:
    filter_list.append(f"CONTAINS(LCASE(?{field}), {search_term_safe})")
```

**Capability:** Full-text search in organizations field works, but returns datasets, not aggregated statistics.

---

## 4. Institution/Group Hierarchy

### 4.1 InstitutionGroup Entity

**File:** `djehuty/src/djehuty/backup/database.py`  
**Function:** `insert_institution_group()` (lines 922-926)

```python
def insert_institution_group (self, record):
    """Procedure to insert a institution group record."""
    
    uri = rdf.unique_node ("institution_group")
    self.store.add ((uri, RDF.type, rdf.DJHT["InstitutionGroup"]))
```

**Configuration:** `djehuty/djehuty.xml`

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
  ├── TU Delft (ID 28586)
  │     └── TU Delft Students (ID 28696)
  ├── University of Twente
  ├── Eindhoven University of Technology
  └── Wageningen University & Research
```

**Gap:** No faculty level exists below institution level. Would need new intermediate layer like:

```
TU Delft
  ├── Faculty of Aerospace Engineering
  ├── Faculty of Civil Engineering and Geosciences
  ├── Faculty of Electrical Engineering, Mathematics and Computer Science
  └── ...
```

### 4.2 Account-to-Group Mapping

**File:** `djehuty/src/djehuty/backup/database.py`  
**Function:** `insert_account()` (lines 189-192)

```python
institution_user_id = value_or (record, "institution_user_id", None)
if institution_user_id is not None:
    domain = institution_user_id.partition("@")[2]
    # Domain matched to group (e.g., tudelft.nl → group 28586)
```

**Mechanism:** Email domain (`@tudelft.nl`) automatically maps to InstitutionGroup via XML config.

**Challenge for Faculty:** Email domains don't distinguish faculties (all use `@tudelft.nl`). Would need alternative mapping method.

---

## 5. Data Flow Summary

### Deposit Flow

```
1. User logs in → Account created
   ├── institution_id set from email domain
   └── group_id set from XML hierarchy

2. User creates dataset → Dataset entity created
   ├── institution_id copied from Account
   ├── group_id copied from Account
   ├── Authors added (with optional institution_id per author)
   └── Organizations custom field = free-text string

3. Dataset published → Statistics counted
   └── Counted toward depositor's institution_id only
```

### Statistics Flow

```
1. repository_statistics() called
   └── Counts all public datasets (no institution filter)

2. dataset_statistics(group_ids=[...]) called
   └── Filters by InstitutionGroup (not faculty)
   └── Returns top N datasets by downloads/views/etc.
```

**Missing:** No faculty-level aggregation anywhere in the pipeline.

---

## 6. Technical Constraints & Opportunities

### Constraints

1. **No faculty entity in RDF schema**: Would need new `djht:Faculty` type
2. **No faculty field in accounts**: Would need `djht:faculty_id` predicate
3. **Organizations field unparseable**: Free-text with inconsistent formatting
4. **Email domains institution-wide**: Can't auto-detect faculty from `@tudelft.nl`
5. **580+ existing datasets**: Need migration strategy for historical data

### Opportunities

1. **Group hierarchy is extensible**: Can add faculty groups under institutions
2. **SPARQL templates modular**: Can create new `statistics_faculty.sparql`
3. **Custom field validation exists**: Can add faculty selection UI
4. **RDF model flexible**: Can add `djht:faculty_id` without breaking existing data
5. **Caching infrastructure ready**: Statistics cache at `data/cache/repository_statistics`

---

## 7. Code Locations Reference

### Author/Institution Processing

| Component | File | Function | Lines |
|-----------|------|----------|-------|
| Author insertion | `backup/database.py` | `insert_author()` | 238-267 |
| Account-institution link | `backup/database.py` | `insert_account()` | 175-213 |
| Institution entity | `backup/database.py` | `insert_institution()` | 214-230 |
| InstitutionGroup | `backup/database.py` | `insert_institution_group()` | 922-926 |
| Organizations custom field | `backup/database.py` | `handle_custom_fields()` | 476-490 |
| Custom field insertion | `web/database.py` | `insert_custom_field_value()` | 2070-2092 |

### Statistics Generation

| Component | File | Function | Lines |
|-----------|------|----------|-------|
| Repository statistics | `web/database.py` | `repository_statistics()` | 512-547 |
| Dataset statistics | `web/database.py` | `dataset_statistics()` | 549-570 |
| File statistics | `web/database.py` | `repository_file_statistics()` | 486-497 |

### SPARQL Templates

| Template | Purpose | Key Fields |
|----------|---------|------------|
| `statistics_datasets.sparql` | Count all public datasets | `?container`, `?dataset` |
| `statistics_authors.sparql` | Count all public authors | `?author` |
| `dataset_statistics.sparql` | Top datasets by metric | `?group_id`, `?category_id` |
| `datasets.sparql` | Retrieve dataset details | `?institution_id`, `?organizations` |
| `authors.sparql` | Retrieve author details | `?institution_id`, `?orcid_id` |

### Configuration

| File | Purpose | Relevant Content |
|------|---------|------------------|
| `djehuty.xml` | Institution/group hierarchy | `<group>` elements with domain matching |
| `contributors_organizations.json` | Legacy data mappings | Manual organization strings (backup only) |

---

## 8. Recommended Next Steps

### For Solution Design

1. **Extend RDF schema** with `djht:Faculty` entity and `djht:faculty_id` predicate
2. **Modify account creation** to capture faculty selection during registration
3. **Add faculty field to datasets** inherited from depositor account
4. **Create faculty hierarchy** in XML config under each institution
5. **Build faculty statistics template** similar to `dataset_statistics.sparql`
6. **Design migration strategy** for 580+ existing datasets (possibly via Organizations field parsing + manual review)

### For Stakeholder Discussion

1. **Faculty taxonomy**: Should it be standardized across 4TU or per-institution?
2. **Legacy data handling**: Parse Organizations field or manual curation?
3. **Multi-faculty attribution**: How to count datasets with authors from multiple faculties?
4. **ORCID enhancement**: Should system fetch faculty from ORCID (not currently there)?
5. **UI/UX**: Where does user select faculty? Registration only or per-dataset?
6. **Reporting period**: Do faculty stats need historical data or only new deposits?

---

## 9. Gap Analysis

| Required for Faculty Stats | Current State | Gap |
|-----------------------------|---------------|-----|
| Faculty entity in RDF | ❌ Not exists | Need to create `djht:Faculty` |
| Faculty field in Account | ❌ Not exists | Need `djht:faculty_id` predicate |
| Faculty field in Dataset | ❌ Not exists | Need `djht:faculty_id` predicate |
| Faculty hierarchy config | ❌ Not exists | Need XML `<group>` entries |
| Faculty SPARQL queries | ❌ Not exists | Need `statistics_faculty.sparql` |
| Faculty filtering in API | ❌ Not exists | Need web endpoint `/statistics/faculty` |
| Faculty UI selection | ❌ Not exists | Need dropdown/autocomplete in forms |
| Migration tool | ❌ Not exists | Need script to populate faculty_id |

**Conclusion:** Faculty-level statistics is not currently possible without extending the data model, adding new predicates, and implementing faculty selection UI. The Organizations field contains relevant data but is unusable for aggregation due to free-text format.
