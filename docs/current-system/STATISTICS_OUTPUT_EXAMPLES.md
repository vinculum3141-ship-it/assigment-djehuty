# Statistics Output Examples - Current Djehuty Implementation

This document shows the **exact output format** of statistics in the current Djehuty system.

---

## Repository-Wide Statistics

### Method: `repository_statistics()`

**Location:** `djehuty/src/djehuty/web/database.py` (Line 510)

### Output Format (Python Dictionary)

```python
{
    "datasets": 1234,      # Count of published dataset containers
    "authors": 567,        # Count of public authors
    "collections": 89,     # Count of published collection containers
    "files": 4567,         # Count of files across all datasets
    "bytes": 1234567890    # Total storage used in bytes
}
```

### Example with Real Numbers

```python
{
    "datasets": 1234,
    "authors": 567,
    "collections": 89,
    "files": 4567,
    "bytes": 1234567890
}
```

### How It's Calculated

1. **Datasets Count:**
   - SPARQL query: `statistics_datasets.sparql`
   - Counts distinct `djht:DatasetContainer` with `is_public=true`

2. **Authors Count:**
   - SPARQL query: `statistics_authors.sparql`
   - Counts distinct `djht:Author` with `is_public=true`

3. **Collections Count:**
   - SPARQL query: `statistics_collections.sparql`
   - Counts distinct `djht:CollectionContainer` with `is_public=true`

4. **Files Count:**
   - Calls `repository_file_statistics()` + `repository_datalink_statistics()`
   - Sums all files and datalinks across all datasets

5. **Bytes Total:**
   - Sums `bytes` field from all files and datalinks

---

## Portal Display (HTML Output)

### Location: `/portal` or `/`

**Template:** `djehuty/src/djehuty/web/resources/html_templates/portal.html`

### What Users See

```
Summary
═══════════════════════════════════════

   1,234    │ datasets
     567    │ authors
      89    │ collections
   4,567    │ files
1,234,567,890 │ bytes
```

### Formatting Applied

Numbers are formatted with thousand separators (commas):

```python
# In wsgi.py (Line 3510-3512)
for key in summary_data:
    summary_data[key] = f"{int(summary_data[key]):,}"
```

**Before formatting:**
```python
{"datasets": 1234, "authors": 567, ...}
```

**After formatting:**
```python
{"datasets": "1,234", "authors": "567", ...}
```

---

## Institution-Specific Statistics

### Current Limitation: NO STATISTICS PER INSTITUTION

The current system **does NOT provide statistics broken down by institution**. 

### What Exists Today

When you visit `/institutions/Delft_University_of_Technology`, you get:

✅ **List of datasets** (up to 100)
❌ **NOT statistics** (no count, no breakdown)

### Code for Institution Page

**Location:** `djehuty/src/djehuty/web/wsgi.py` (Line 3977)

```python
def ui_institution(self, request, institution_name):
    """Implements /institutions/<name>."""
    
    group_name = institution_name.replace('_', ' ')
    group = self.db.group_by_name(group_name)
    sub_groups = self.db.group_by_name(group_name, startswith=True)
    sub_group_ids = [item['group_id'] for item in sub_groups]
    
    # Returns DATASETS (list), not statistics (counts)
    datasets = self.db.datasets(groups=sub_group_ids,
                                is_published=True,
                                limit=100)
    
    return self.__render_template(request, "institutions.html",
                                   articles=datasets,  # List of datasets
                                   group=group,
                                   sub_groups=sub_groups)
```

### Output: Dataset List (NOT Statistics)

```python
datasets = [
    {
        "container_uuid": "a1b2c3d4-...",
        "title": "Dataset Title 1",
        "published_date": "2024-01-15T10:30:00Z",
        "doi": "10.4121/12345678",
        ...
    },
    {
        "container_uuid": "e5f6g7h8-...",
        "title": "Dataset Title 2",
        "published_date": "2024-02-20T14:45:00Z",
        "doi": "10.4121/87654321",
        ...
    },
    # ... up to 100 datasets
]
```

---

## What You CAN Query (Current System)

### Datasets by Institution/Group

**Method:** `datasets(groups=[group_ids])`

**Location:** `djehuty/src/djehuty/web/database.py` (Line 395)

**Parameters:**
```python
datasets = db.datasets(
    groups=[1, 2, 3],        # Filter by group IDs
    is_published=True,       # Only published datasets
    limit=100,               # Max results
    offset=0,                # Pagination offset
    order="published_date",  # Sort field
    order_direction="desc"   # Sort direction
)
```

**Returns:** List of dataset dictionaries (NOT a count)

### Institution/Group Information

**Method:** `group_by_name(group_name)`

**Location:** `djehuty/src/djehuty/web/database.py` (Line 2943)

**Example:**
```python
group = db.group_by_name("Delft University of Technology")
```

**Returns:**
```python
{
    "group_id": 898,
    "group_name": "Delft University of Technology"
}
```

---

## What You CANNOT Query (Missing Functionality)

❌ **Statistics per institution:**
```python
# THIS DOES NOT EXIST
stats = db.institution_statistics(group_id=898)
# Expected: {"datasets": 50, "authors": 20, ...}
```

❌ **Statistics per faculty:**
```python
# THIS DOES NOT EXIST
stats = db.faculty_statistics(faculty_id="AE")
# Expected: {"datasets": 10, "depositors": 5, ...}
```

❌ **All institutions with their statistics:**
```python
# THIS DOES NOT EXIST
stats = db.all_institutions_statistics()
# Expected: [
#   {"institution": "TU Delft", "datasets": 50, ...},
#   {"institution": "TU Eindhoven", "datasets": 30, ...}
# ]
```

❌ **All faculties with their statistics:**
```python
# THIS DOES NOT EXIST
stats = db.all_faculties_statistics()
# Expected: [
#   {"faculty": "Faculty of Aerospace Engineering", "datasets": 10, ...},
#   {"faculty": "Faculty of Applied Sciences", "datasets": 15, ...}
# ]
```

---

## SPARQL Query Output Examples

### 1. Repository Datasets Count

**Template:** `statistics_datasets.sparql`

**SPARQL Query:**
```sparql
PREFIX djht: <https://data.4tu.nl/ontologies/djehuty#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT (COUNT(DISTINCT ?container) AS ?datasets)
WHERE {
  GRAPH <https://data.4tu.nl/portal/self-test> {
    ?container  rdf:type                      djht:DatasetContainer ;
                djht:latest_published_version ?dataset .
    ?dataset    rdf:type                      djht:Dataset ;
                djht:is_public                "true"^^xsd:boolean .
  }
}
```

**Output (JSON):**
```json
{
  "results": {
    "bindings": [
      {
        "datasets": {
          "type": "literal",
          "datatype": "http://www.w3.org/2001/XMLSchema#integer",
          "value": "1234"
        }
      }
    ]
  }
}
```

**Python Result:**
```python
[{"datasets": 1234}]
```

### 2. Repository Authors Count

**Template:** `statistics_authors.sparql`

**SPARQL Query:**
```sparql
SELECT (COUNT(DISTINCT ?author) AS ?authors)
WHERE {
  GRAPH <https://data.4tu.nl/portal/self-test> {
    ?author     rdf:type        djht:Author .
    ?author     djht:is_public  "true"^^xsd:boolean .
  }
}
```

**Output:**
```python
[{"authors": 567}]
```

### 3. Repository Collections Count

**Template:** `statistics_collections.sparql`

**SPARQL Query:**
```sparql
SELECT (COUNT(DISTINCT ?container) AS ?collections)
WHERE {
  GRAPH <https://data.4tu.nl/portal/self-test> {
    ?container  rdf:type                      djht:CollectionContainer ;
                djht:latest_published_version ?collection .
    ?collection rdf:type                      djht:Collection ;
                djht:is_public                "true"^^xsd:boolean .
  }
}
```

**Output:**
```python
[{"collections": 89}]
```

### 4. Institution Group Query

**Template:** `group_by_name.sparql`

**SPARQL Query:**
```sparql
SELECT ?group_id ?group_name
WHERE {
  GRAPH <https://data.4tu.nl/portal/self-test> {
    ?group      rdf:type   djht:InstitutionGroup .
    ?group      djht:id    ?group_id .
    ?group      djht:name  ?group_name .
  }
  FILTER (STR(?group_name) = "Delft University of Technology")
}
```

**Output:**
```python
[{
    "group_id": 898,
    "group_name": "Delft University of Technology"
}]
```

---

## What Phase 1 Needs to Output

### Faculty Statistics (NEW - To Be Implemented)

**Endpoint:** `GET /v3/faculties/statistics`

**Expected Output Format:**
```json
[
  {
    "faculty_id": "AE",
    "faculty_name": "Faculty of Aerospace Engineering",
    "datasets_count": 87,
    "percentage": 15.2,
    "last_updated": "2024-12-09T10:30:00Z"
  },
  {
    "faculty_id": "AS",
    "faculty_name": "Faculty of Applied Sciences",
    "datasets_count": 120,
    "percentage": 21.0,
    "last_updated": "2024-12-09T10:30:00Z"
  },
  {
    "faculty_id": "CEG",
    "faculty_name": "Faculty of Civil Engineering and Geosciences",
    "datasets_count": 95,
    "percentage": 16.6,
    "last_updated": "2024-12-09T10:30:00Z"
  }
  // ... 5 more faculties
]
```

### Individual Faculty Statistics

**Endpoint:** `GET /v3/faculties/{faculty_id}/statistics`

**Expected Output:**
```json
{
  "faculty_id": "AE",
  "faculty_name": "Faculty of Aerospace Engineering",
  "statistics": {
    "datasets_count": 87,
    "depositors_count": 12,
    "total_institution_datasets": 572,
    "percentage_of_institution": 15.2,
    "first_deposit": "2018-03-15T09:20:00Z",
    "last_deposit": "2024-11-28T14:45:00Z"
  },
  "last_updated": "2024-12-09T10:30:00Z"
}
```

### HTML Dashboard Output (Phase 1)

**Page:** `/admin/faculties/statistics`

**What Users Will See:**

```
Faculty Statistics Dashboard
═════════════════════════════════════════════════════════════

Total Datasets (TU Delft): 572

┌──────────────────────────────────────────────────┬──────────┬────────────┐
│ Faculty                                          │ Datasets │ Percentage │
├──────────────────────────────────────────────────┼──────────┼────────────┤
│ Faculty of Applied Sciences                      │   120    │   21.0%    │
│ Faculty of Civil Engineering and Geosciences     │    95    │   16.6%    │
│ Faculty of Aerospace Engineering                 │    87    │   15.2%    │
│ Faculty of Electrical Engineering, Mathematics...│    78    │   13.6%    │
│ Faculty of Mechanical Engineering                │    65    │   11.4%    │
│ Faculty of Architecture and the Built Environment│    52    │    9.1%    │
│ Faculty of Technology, Policy and Management     │    45    │    7.9%    │
│ Faculty of Industrial Design Engineering         │    30    │    5.2%    │
└──────────────────────────────────────────────────┴──────────┴────────────┘

Last updated: 2024-12-09 10:30:00
```

---

## Summary: Current vs. Phase 1 Output

| Feature | Current System | Phase 1 (To Build) |
|---------|---------------|-------------------|
| **Repository-wide statistics** | ✅ `{"datasets": 1234, "authors": 567, ...}` | ✅ Same (no change) |
| **Institution statistics** | ❌ Only dataset lists, no counts | ⚠️ Out of scope (Phase 1 = faculties only) |
| **Faculty statistics** | ❌ Does not exist | ✅ `[{"faculty_id": "AE", "datasets_count": 87, ...}]` |
| **Faculty detail** | ❌ Does not exist | ✅ `{"faculty_id": "AE", "statistics": {...}}` |
| **HTML dashboard** | ❌ Does not exist | ✅ Table with faculty breakdown |
| **API endpoints** | ❌ 0 faculty endpoints | ✅ 6 new endpoints |
| **SPARQL queries** | ❌ No faculty queries | ✅ 4 new templates |

---

## How to Test Current System

### 1. Start Djehuty

```bash
cd /home/ruby/Projects/assigment-djehuty/djehuty
python3 -m djehuty.web.ui --address 0.0.0.0 --port 8080 --config-file djehuty.xml
```

### 2. Query Repository Statistics (Python Console)

```python
from djehuty.web.database import SparqlInterface

db = SparqlInterface()
stats = db.repository_statistics()
print(stats)
# Output: {'datasets': 1234, 'authors': 567, 'collections': 89, 'files': 4567, 'bytes': 1234567890}
```

### 3. Query Institution Datasets

```python
group = db.group_by_name("Delft University of Technology")
print(group)
# Output: {'group_id': 898, 'group_name': 'Delft University of Technology'}

datasets = db.datasets(groups=[898], is_published=True, limit=10)
print(f"Found {len(datasets)} datasets")
# Output: Found 10 datasets (list of dataset dicts)
```

### 4. View in Browser

- Repository stats: `http://localhost:8080/`
- Institution page: `http://localhost:8080/institutions/Delft_University_of_Technology`

---

## Key Takeaways

1. **Current system outputs:** Repository-wide statistics only (5 metrics)
2. **Institution pages:** Show dataset **lists**, not statistics
3. **No faculty data:** Phase 1 will add faculty statistics from scratch
4. **Output format:** Python dictionaries → JSON API → HTML tables
5. **SPARQL returns:** Lists of bindings that Python code aggregates

---

## Related Documents

- [INSTITUTION_STATISTICS_GUIDE.md](INSTITUTION_STATISTICS_GUIDE.md) - How current statistics work
- [CODEBASE_ANALYSIS.md](CODEBASE_ANALYSIS.md) - Full code structure analysis
- [../assignment/SOLUTION_ARCHITECTURE.md](../assignment/SOLUTION_ARCHITECTURE.md) - Phase 1 implementation plan
