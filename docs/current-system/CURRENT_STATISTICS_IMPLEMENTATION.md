# Current Djehuty Statistics Implementation - As-Is Documentation

## Purpose

This document describes **only** the current statistics implementation in Djehuty v25.6, without any reference to future enhancements or Phase 1 extensions.

---

## Overview

The current Djehuty system provides **repository-wide statistics** that aggregate metrics across all institutions in the 4TU.ResearchData repository.

### What Exists Today

- ✅ **Repository-wide statistics** (total counts across all data)
- ✅ **Institution pages** (lists of datasets per institution)
- ❌ **NO statistics broken down by institution**
- ❌ **NO statistics broken down by faculty**
- ❌ **NO statistics dashboard**

---

## Repository-Wide Statistics

### Where It's Displayed

**URL:** `http://localhost:8080/` or `http://localhost:8080/portal`

**What Users See:**

```
Summary
═══════════════════════════════════════

   1,234    │ datasets
     567    │ authors
      89    │ collections
   4,567    │ files
1,234,567,890 │ bytes
```

### Backend Implementation

**Method:** `repository_statistics()`

**Location:** `djehuty/src/djehuty/web/database.py` (Line 510)

**Source Code:**

```python
def repository_statistics(self):
    """Procedure to retrieve repository-wide statistics."""

    datasets_query    = self.__query_from_template("statistics_datasets")
    collections_query = self.__query_from_template("statistics_collections")
    authors_query     = self.__query_from_template("statistics_authors")

    row = {"datasets": 0, "authors": 0, "collections": 0, "files": 0, "bytes": 0}
    try:
        datasets    = self.__run_query(datasets_query, datasets_query, "repository_statistics")
        authors     = self.__run_query(authors_query, authors_query, "repository_statistics")
        collections = self.__run_query(collections_query, collections_query, "repository_statistics")
        files       = self.repository_file_statistics(use_cache=True)
        datalinks   = self.repository_datalink_statistics(use_cache=True)
        
        number_of_files = 0
        number_of_bytes = 0
        for entry in files:
            number_of_files += 1
            number_of_bytes += int(float(entry["bytes"]))

        for entry in datalinks:
            number_of_bytes += int(float(entry["bytes"]))

        files_results = {
            "files": number_of_files,
            "bytes": number_of_bytes
        }
        row = {**datasets[0], **authors[0], **collections[0], **files_results}
    except (IndexError, KeyError):
        pass

    return row
```

### Return Value

**Type:** Python dictionary

**Format:**

```python
{
    "datasets": 1234,      # Count of published dataset containers
    "authors": 567,        # Count of public authors  
    "collections": 89,     # Count of published collection containers
    "files": 4567,         # Total number of files
    "bytes": 1234567890    # Total storage in bytes
}
```

### How It Works

1. **Execute 3 SPARQL queries:**
   - `statistics_datasets.sparql` → counts datasets
   - `statistics_authors.sparql` → counts authors
   - `statistics_collections.sparql` → counts collections

2. **Call 2 helper methods:**
   - `repository_file_statistics()` → gets file list with sizes
   - `repository_datalink_statistics()` → gets datalink sizes

3. **Aggregate results:**
   - Count files
   - Sum bytes
   - Merge all dictionaries

4. **Return combined dictionary**

---

## SPARQL Queries

### Query 1: Count Datasets

**Template:** `statistics_datasets.sparql`

**Location:** `djehuty/src/djehuty/web/resources/sparql_templates/statistics_datasets.sparql`

**Query:**

```sparql
PREFIX djht: <https://data.4tu.nl/ontologies/djehuty#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT (COUNT(DISTINCT ?container) AS ?datasets)
WHERE {
  GRAPH <{{state_graph}}> {
    ?container  rdf:type                      djht:DatasetContainer ;
                djht:latest_published_version ?dataset .
    ?dataset    rdf:type                      djht:Dataset ;
                djht:is_public                "true"^^xsd:boolean .
  }
}
```

**What It Counts:**
- Only **published** datasets (`djht:latest_published_version`)
- Only **public** datasets (`djht:is_public = true`)
- Counts **containers** (not individual versions)

**Result:**

```python
[{"datasets": 1234}]
```

### Query 2: Count Authors

**Template:** `statistics_authors.sparql`

**Location:** `djehuty/src/djehuty/web/resources/sparql_templates/statistics_authors.sparql`

**Query:**

```sparql
PREFIX djht: <https://data.4tu.nl/ontologies/djehuty#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT (COUNT(DISTINCT ?author) AS ?authors)
WHERE {
  GRAPH <{{state_graph}}> {
    ?author     rdf:type        djht:Author .
    ?author     djht:is_public  "true"^^xsd:boolean .
  }
}
```

**What It Counts:**
- All **public** authors in the system
- Includes both registered and unregistered authors

**Result:**

```python
[{"authors": 567}]
```

### Query 3: Count Collections

**Template:** `statistics_collections.sparql`

**Location:** `djehuty/src/djehuty/web/resources/sparql_templates/statistics_collections.sparql`

**Query:**

```sparql
PREFIX djht: <https://data.4tu.nl/ontologies/djehuty#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT (COUNT(DISTINCT ?container) AS ?collections)
WHERE {
  GRAPH <{{state_graph}}> {
    ?container  rdf:type                      djht:CollectionContainer ;
                djht:latest_published_version ?collection .
    ?collection rdf:type                      djht:Collection ;
                djht:is_public                "true"^^xsd:boolean .
  }
}
```

**What It Counts:**
- Only **published** collections
- Only **public** collections
- Counts **containers** (not individual versions)

**Result:**

```python
[{"collections": 89}]
```

---

## Portal Home Page

### HTTP Request Handler

**Route:** `/` or `/portal`

**Method:** `ui_home(request)`

**Location:** `djehuty/src/djehuty/web/wsgi.py` (Line 3503)

**Source Code:**

```python
def ui_home(self, request):
    """Implements /portal."""
    if not self.accepts_html(request):
        return self.error_406("text/html")

    # Get statistics
    summary_data = self.db.repository_statistics()
    
    # Format numbers with thousand separators
    try:
        for key in summary_data:
            summary_data[key] = f"{int(summary_data[key]):,}"
    except ValueError:
        summary_data = {"datasets": 0, "authors": 0, "collections": 0, "files": 0, "bytes": 0}

    # Get latest datasets (for display below statistics)
    latest = []
    try:
        records = self.db.latest_datasets_portal(15)
        for rec in records:
            authors = self.db.authors(item_uri=rec["dataset_uri"],
                                     item_type="dataset",
                                     limit=None)
            pub_date = rec['published_date'][:10]
            url = f'/datasets/{rec["container_uuid"]}'
            latest.append((url, rec['title'], pub_date, authors))
    except (IndexError, KeyError):
        pass

    return self.__render_template(request, "portal.html",
                                   summary_data=summary_data,
                                   latest=latest,
                                   notice_message=config.notice_message,
                                   show_portal_summary=config.show_portal_summary,
                                   show_institutions=config.show_institutions,
                                   show_science_categories=config.show_science_categories,
                                   show_latest_datasets=config.show_latest_datasets)
```

### Number Formatting

**Before:**
```python
{"datasets": 1234, "authors": 567, ...}
```

**After:**
```python
{"datasets": "1,234", "authors": "567", ...}
```

This is done by:
```python
summary_data[key] = f"{int(summary_data[key]):,}"
```

### HTML Template

**Template:** `portal.html`

**Location:** `djehuty/src/djehuty/web/resources/html_templates/portal.html`

**Relevant Section:**

```html
<h1 class="corporate-identity-h1">Summary</h1>
<div id="portal-summary">
{%- for item in ["datasets", "authors", "collections", "files", "bytes"]: %}
<div class="portal-summary-item">
  <div class="portal-summary-item-left">{{summary_data[item]}}</div><!--
--><div class="portal-summary-item-right">{{item}}</div>
</div>
{%- endfor %}
</div>
```

**Rendered Output:**

```html
<div id="portal-summary">
  <div class="portal-summary-item">
    <div class="portal-summary-item-left">1,234</div>
    <div class="portal-summary-item-right">datasets</div>
  </div>
  <div class="portal-summary-item">
    <div class="portal-summary-item-left">567</div>
    <div class="portal-summary-item-right">authors</div>
  </div>
  <!-- ... etc -->
</div>
```

---

## Institution Pages

### What They Display

**URL Pattern:** `/institutions/<institution_name>`

**Examples:**
- `/institutions/Delft_University_of_Technology`
- `/institutions/University_of_Twente`
- `/institutions/Eindhoven_University_of_Technology`
- `/institutions/Wageningen_University_Research`

**What Users See:**
- Institution name (e.g., "Delft University of Technology")
- **List of datasets** from that institution (up to 100)
- **NOT statistics** (no counts, no percentages)

### HTTP Request Handler

**Route:** `/institutions/<institution_name>`

**Method:** `ui_institution(request, institution_name)`

**Location:** `djehuty/src/djehuty/web/wsgi.py` (Line 3977)

**Source Code:**

```python
def ui_institution(self, request, institution_name):
    """Implements /institutions/<name>."""
    if not self.accepts_html(request):
        return self.error_406("text/html")

    # Convert URL format to group name
    # "Delft_University_of_Technology" → "Delft University of Technology"
    group_name = institution_name.replace('_', ' ')
    
    # Get institution group info
    group = self.db.group_by_name(group_name)
    
    # Get all sub-groups (e.g., faculties, if they existed)
    sub_groups = self.db.group_by_name(group_name, startswith=True)
    sub_group_ids = [item['group_id'] for item in sub_groups]
    
    # Get datasets for this institution
    datasets = self.db.datasets(groups=sub_group_ids,
                                is_published=True,
                                limit=100)
    
    return self.__render_template(request, "institutions.html",
                                   articles=datasets,
                                   group=group,
                                   sub_groups=sub_groups)
```

### Institution Lookup

**Method:** `group_by_name(group_name, startswith=False)`

**Location:** `djehuty/src/djehuty/web/database.py` (Line 2943)

**Source Code:**

```python
def group_by_name(self, group_name, startswith=False):
    """Procedure to return group information by its name."""

    query = self.__query_from_template("group_by_name", {
        "startswith": startswith,
        "group_name": rdf.escape_string_value(group_name)
    })

    results = self.__run_query(query, query, "group")
    if startswith:
        return results  # List of matching groups
    try:
        return results[0]  # Single group
    except IndexError:
        return None
```

**SPARQL Template:** `group_by_name.sparql`

**Query:**

```sparql
PREFIX djht: <https://data.4tu.nl/ontologies/djehuty#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?group_id ?group_name
WHERE {
  GRAPH <{{state_graph}}> {
    ?group      rdf:type   djht:InstitutionGroup .
    ?group      djht:id    ?group_id .
    ?group      djht:name  ?group_name .
  }
  FILTER (STR(?group_name) = "Delft University of Technology")
}
```

**Result:**

```python
{
    "group_id": 898,
    "group_name": "Delft University of Technology"
}
```

### Dataset Filtering by Institution

**Method:** `datasets(groups=[group_ids], is_published=True, limit=100)`

**Location:** `djehuty/src/djehuty/web/database.py` (Line 395)

**What It Does:**
1. Takes list of group IDs (institution IDs)
2. Filters datasets where `djht:group_id` matches
3. Returns list of dataset dictionaries (NOT counts)

**Result Format:**

```python
[
    {
        "container_uuid": "a1b2c3d4-...",
        "title": "Dataset Title 1",
        "published_date": "2024-01-15T10:30:00Z",
        "doi": "10.4121/12345678",
        "group_id": 898,
        ...
    },
    {
        "container_uuid": "e5f6g7h8-...",
        "title": "Dataset Title 2",
        "published_date": "2024-02-20T14:45:00Z",
        "doi": "10.4121/87654321",
        "group_id": 898,
        ...
    },
    # ... up to 100 datasets
]
```

**Important:** This returns a **list of datasets**, not **statistics**.

---

## How Institutions Are Stored

### RDF Entity: InstitutionGroup

**Type:** `djht:InstitutionGroup`

**Properties:**
- `djht:id` - Numeric ID (e.g., 898 for TU Delft)
- `djht:name` - Full name (e.g., "Delft University of Technology")

**Example RDF:**

```turtle
<https://data.4tu.nl/institution/898> 
    rdf:type djht:InstitutionGroup ;
    djht:id 898 ;
    djht:name "Delft University of Technology" .
```

### How Datasets Link to Institutions

Datasets are linked to institutions **through accounts** (depositors):

```
djht:Account
  ├─ djht:account_id: "12345"
  ├─ djht:email: "researcher@tudelft.nl"
  └─ djht:group_id: 898  ← Link to institution

djht:Dataset
  ├─ djht:dataset_id: "67890"
  └─ djht:account_id: "12345"  ← Link to depositor account
```

**Query Pattern:**

```sparql
# Find datasets by institution
SELECT ?dataset ?title
WHERE {
  # Dataset deposited by account
  ?dataset djht:account_id ?account_id .
  
  # Account belongs to institution
  ?account djht:account_id ?account_id ;
           djht:group_id 898 .  # TU Delft
  
  ?dataset djht:title ?title .
}
```

---

## Portal Institution Tiles

### HTML Display

**Template:** `portal.html`

**Section:**

```html
<h1 class="corporate-identity-h1">Institutions</h1>
<div class="tiles-wrapper">
  <ul class="tiles">
    <li>
      <div class="tile institute-tile">
        <div class="tile-row-image">
          <a href="/institutions/Delft_University_of_Technology">
            <img src="/static/images/portal/tudelft.jpg" alt="TU Delft">
          </a>
        </div>
      </div>
    </li>
    <li>
      <div class="tile institute-tile">
        <div class="tile-row-image">
          <a href="/institutions/University_of_Twente">
            <img src="/static/images/portal/utwente.jpg" alt="UTwente">
          </a>
        </div>
      </div>
    </li>
    <li>
      <div class="tile institute-tile">
        <div class="tile-row-image">
          <a href="/institutions/Eindhoven_University_of_Technology">
            <img src="/static/images/portal/tueindhoven.jpg" alt="TU Eindhoven">
          </a>
        </div>
      </div>
    </li>
    <li>
      <div class="tile institute-tile">
        <div class="tile-row-image">
          <a href="/institutions/Wageningen_University_Research">
            <img src="/static/images/portal/wur.jpg" alt="WUR">
          </a>
        </div>
      </div>
    </li>
  </ul>
</div>
```

**What Happens When Clicked:**
- User clicks on institution tile
- Browser navigates to `/institutions/<name>`
- Server shows list of datasets (see "Institution Pages" section above)

---

## Data Flow Summary

### Portal Statistics Flow

```
User requests "/"
    ↓
wsgi.py: ui_home()
    ↓
database.py: repository_statistics()
    ↓
Execute 3 SPARQL queries:
  - statistics_datasets.sparql  → {"datasets": 1234}
  - statistics_authors.sparql   → {"authors": 567}
  - statistics_collections.sparql → {"collections": 89}
    ↓
Call helper methods:
  - repository_file_statistics() → list of files
  - repository_datalink_statistics() → list of datalinks
    ↓
Aggregate results:
  - Count files: 4567
  - Sum bytes: 1234567890
    ↓
Merge dictionaries:
  {"datasets": 1234, "authors": 567, "collections": 89, "files": 4567, "bytes": 1234567890}
    ↓
Format numbers with commas:
  {"datasets": "1,234", "authors": "567", ...}
    ↓
Render portal.html template
    ↓
Display to user
```

### Institution Page Flow

```
User clicks "/institutions/Delft_University_of_Technology"
    ↓
wsgi.py: ui_institution("Delft_University_of_Technology")
    ↓
Convert to group name: "Delft University of Technology"
    ↓
database.py: group_by_name("Delft University of Technology")
    ↓
Execute SPARQL: group_by_name.sparql
    ↓
Result: {"group_id": 898, "group_name": "Delft University of Technology"}
    ↓
database.py: datasets(groups=[898], is_published=True, limit=100)
    ↓
Execute SPARQL: datasets.sparql with filter on group_id
    ↓
Result: List of 100 datasets from TU Delft
    ↓
Render institutions.html template
    ↓
Display list of datasets to user
```

---

## Key Files Reference

### Python Code

| File | Path | Purpose |
|------|------|---------|
| `wsgi.py` | `djehuty/src/djehuty/web/wsgi.py` | HTTP request handlers |
| `database.py` | `djehuty/src/djehuty/web/database.py` | SPARQL interface and query execution |
| `config.py` | `djehuty/src/djehuty/web/config.py` | Configuration state |

### SPARQL Templates

| File | Path | Purpose |
|------|------|---------|
| `statistics_datasets.sparql` | `djehuty/src/djehuty/web/resources/sparql_templates/` | Count published datasets |
| `statistics_authors.sparql` | `djehuty/src/djehuty/web/resources/sparql_templates/` | Count public authors |
| `statistics_collections.sparql` | `djehuty/src/djehuty/web/resources/sparql_templates/` | Count published collections |
| `group_by_name.sparql` | `djehuty/src/djehuty/web/resources/sparql_templates/` | Find institution by name |
| `datasets.sparql` | `djehuty/src/djehuty/web/resources/sparql_templates/` | Query datasets with filters |

### HTML Templates

| File | Path | Purpose |
|------|------|---------|
| `portal.html` | `djehuty/src/djehuty/web/resources/html_templates/` | Home page with statistics |
| `institutions.html` | `djehuty/src/djehuty/web/resources/html_templates/` | Institution page with dataset list |
| `layout.html` | `djehuty/src/djehuty/web/resources/html_templates/` | Base template |

---

## Testing the Current System

### Start Djehuty

```bash
cd /home/ruby/Projects/assigment-djehuty/djehuty
python3 -m djehuty.web.ui --address 0.0.0.0 --port 8080 --config-file djehuty.xml
```

### Access in Browser

**Portal Home Page:**
```
http://localhost:8080/
```
Shows repository-wide statistics

**TU Delft Institution Page:**
```
http://localhost:8080/institutions/Delft_University_of_Technology
```
Shows list of TU Delft datasets

### Query Statistics Programmatically

```python
from djehuty.web.database import SparqlInterface

db = SparqlInterface()

# Get repository statistics
stats = db.repository_statistics()
print(stats)
# {'datasets': 1234, 'authors': 567, 'collections': 89, 'files': 4567, 'bytes': 1234567890}

# Get institution info
group = db.group_by_name("Delft University of Technology")
print(group)
# {'group_id': 898, 'group_name': 'Delft University of Technology'}

# Get datasets for institution
datasets = db.datasets(groups=[898], is_published=True, limit=10)
print(f"Found {len(datasets)} datasets")
# Found 10 datasets
```

---

## What Does NOT Exist

The current system does **NOT** provide:

❌ **Statistics per institution:**
```python
# This method does NOT exist
institution_statistics(institution_id=898)
```

❌ **Statistics per faculty:**
```python
# This method does NOT exist
faculty_statistics(institution_id=898)
```

❌ **Faculty information:**
- No `djht:Faculty` entity type
- No `djht:faculty_id` predicate on accounts
- No faculty dropdown in registration
- No faculty display on dataset pages

❌ **Statistics dashboard:**
- No admin page showing breakdowns
- No export functionality (CSV, JSON)
- No filtering by institution

❌ **Engagement metrics aggregation:**
- Views, downloads, citations exist per dataset
- But NOT aggregated by institution or faculty

---

## Summary

**What Exists:**
- ✅ Repository-wide statistics (5 metrics: datasets, authors, collections, files, bytes)
- ✅ Institution pages (show list of datasets, not statistics)
- ✅ Institution tiles on portal home page

**What is Missing:**
- ❌ No statistics broken down by institution
- ❌ No statistics broken down by faculty
- ❌ No faculty tracking in data model
- ❌ No statistics dashboard

**Key Pattern:**
- Single level: Repository-wide aggregation
- No grouping by institution or faculty
- Lists of entities, not statistical summaries

---

## Related Documents

- [CODEBASE_ANALYSIS.md](CODEBASE_ANALYSIS.md) - Full code structure analysis
- [TECHNICAL_FINDINGS_SUMMARY.md](TECHNICAL_FINDINGS_SUMMARY.md) - Gaps and required changes
- [DATASET_ANALYSIS.md](DATASET_ANALYSIS.md) - Live data examples
