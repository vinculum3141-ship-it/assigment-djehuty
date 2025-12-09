# Clarifying "Statistics Per Institute" - Resolving Assignment Ambiguity

## Document Purpose

This document addresses the ambiguity in the assignment requirement for "statistics per institute" by:
1. Analyzing what "statistics" should mean based on current implementation
2. Proposing clear definitions extending current patterns
3. Providing concrete examples of what to build

---

## The Ambiguity Problem

### Assignment Statement (Vague)

> "The current system provides repository-wide statistics. We want to extend this to provide **statistics per institute**, specifically at the **faculty level** for TU Delft."

### Questions This Raises

1. **What metrics constitute "statistics"?**
   - Just dataset counts?
   - Downloads, views, citations?
   - Authors, files, storage?
   - Time-series data?

2. **What level of granularity?**
   - Institution-wide → Faculty-level?
   - Institution → Faculty → Department?
   - Just faculty or also author-level?

3. **What does "per institute" mean when focusing on faculties?**
   - Statistics for TU Delft broken down by faculty?
   - Statistics for all 4TU institutions, each showing faculty breakdown?
   - Only TU Delft faculties (as assignment suggests)?

4. **Depositor-based or author-based?**
   - Count datasets by who deposited them?
   - Count datasets by who authored them?
   - Both?

---

## Learning from Current Implementation

### What the Current System Provides

**Repository-Wide Statistics** (`repository_statistics()`):

```python
{
    "datasets": 1234,      # Total published dataset containers
    "authors": 567,        # Total public authors
    "collections": 89,     # Total published collections
    "files": 4567,         # Total files across datasets
    "bytes": 1234567890    # Total storage in bytes
}
```

**Key Patterns to Extract:**

1. **Metrics Categories:**
   - **Entities:** Count of primary entities (datasets, authors, collections)
   - **Engagement:** User interaction metrics (views, downloads, citations, shares)
   - **Storage:** Files and bytes

2. **Aggregation Level:**
   - Repository-wide (all institutions combined)
   - No breakdown by institution or faculty

3. **Data Source:**
   - SPARQL queries counting published public entities
   - No filtering by depositor or author

4. **Implementation Pattern:**
   - Multiple SPARQL queries (one per metric)
   - Results combined into single dictionary
   - Caching for performance

---

## Proposed Definition: "Statistics Per Institute/Faculty"

### Clear Definition

**"Statistics per institute" means:**

> Extending the existing repository-wide statistics pattern to provide the same set of metrics, but **grouped and filtered** by:
> 1. **Institution** (TU Delft, UT, TU/e, WUR)
> 2. **Faculty** (within TU Delft: Aerospace, EEMCS, Civil Engineering, etc.)

### What This Includes (Concrete)

#### Level 1: Repository-Wide (EXISTS TODAY)

```python
repository_statistics()
→ {"datasets": 1234, "authors": 567, "collections": 89, "files": 4567, "bytes": 1234567890}
```

#### Level 2: Institution-Level (PARTIALLY EXISTS)

```python
institution_statistics(institution_id=28586)  # TU Delft
→ {
    "institution_id": 28586,
    "institution_name": "TU Delft",
    "datasets": 572,       # Datasets deposited by TU Delft accounts
    "authors": 234,        # Authors affiliated with TU Delft
    "collections": 45,     # Collections from TU Delft
    "files": 2345,         # Files in TU Delft datasets
    "bytes": 567890123     # Storage used by TU Delft datasets
}
```

**Current Gap:** This query doesn't exist, but data is available (institutions are tracked via `group_id`).

#### Level 3: Faculty-Level (DOES NOT EXIST - TO BE BUILT)

```python
faculty_statistics(institution_id=28586)  # All TU Delft faculties
→ [
    {
        "faculty_id": "AE",
        "faculty_name": "Faculty of Aerospace Engineering",
        "datasets": 87,
        "percentage": 15.2,      # 87 / 572 * 100
        "total_views": 15000,
        "total_downloads": 3500,
        "total_cites": 120,
        "total_shares": 45
    },
    {
        "faculty_id": "AS",
        "faculty_name": "Faculty of Applied Sciences",
        "datasets": 120,
        "percentage": 21.0,
        "total_views": 28000,
        "total_downloads": 5200,
        "total_cites": 215,
        "total_shares": 78
    },
    # ... 6 more faculties
]
```

**This is Phase 1 scope.**

#### Level 4: Individual Faculty Detail (TO BE BUILT)

```python
faculty_statistics(institution_id=28586, faculty_id="AE")
→ {
    "faculty_id": "AE",
    "faculty_name": "Faculty of Aerospace Engineering",
    "statistics": {
        "datasets": 87,
        "depositors": 12,             # Unique accounts from this faculty
        "collections": 5,
        "files": 432,
        "bytes": 123456789,
        "total_views": 15000,
        "total_downloads": 3500,
        "total_cites": 120,
        "total_shares": 45,
        "avg_downloads_per_dataset": 40.2
    },
    "percentages": {
        "of_institution_datasets": 15.2,   # 87 / 572
        "of_repository_datasets": 7.1      # 87 / 1234
    },
    "timeline": {
        "first_deposit": "2018-03-15",
        "last_deposit": "2024-11-28",
        "deposits_this_year": 12
    }
}
```

---

## What "Statistics" Should Include

### Tier 1: Core Metrics (MUST HAVE - Phase 1)

Based on current implementation pattern, these are **essential**:

| Metric | Description | Current Equivalent |
|--------|-------------|-------------------|
| **datasets** | Count of datasets deposited by faculty | `repository_statistics()["datasets"]` |
| **percentage** | % of institution's datasets | Calculated: `faculty_datasets / institution_datasets * 100` |

### Tier 2: Engagement Metrics (SHOULD HAVE - Phase 1)

These exist in dataset entities, should be aggregated:

| Metric | Description | Data Source |
|--------|-------------|------------|
| **total_views** | Sum of views across faculty datasets | `djht:total_views` |
| **total_downloads** | Sum of downloads | `djht:total_downloads` |
| **total_cites** | Sum of citations | `djht:total_cites` |
| **total_shares** | Sum of shares | `djht:total_shares` |

### Tier 3: Extended Metrics (NICE TO HAVE - Phase 1.1)

Additional insights:

| Metric | Description | Calculation |
|--------|-------------|-------------|
| **depositors** | Unique accounts from faculty | `COUNT(DISTINCT account_id WHERE faculty_id=X)` |
| **collections** | Collections from faculty | `COUNT(DISTINCT collection WHERE faculty_id=X)` |
| **files** | Total files | `COUNT(files WHERE dataset.faculty_id=X)` |
| **bytes** | Total storage | `SUM(file.size WHERE dataset.faculty_id=X)` |
| **avg_downloads_per_dataset** | Mean downloads | `total_downloads / datasets` |

### Tier 4: Advanced Analytics (OUT OF SCOPE - Phase 2)

Author-level, collaboration networks:

- **multi_faculty_datasets**: Datasets with authors from multiple faculties
- **external_collaborations**: Datasets with non-TU Delft authors
- **collaboration_matrix**: Cross-faculty collaboration counts

---

## Extending Current Implementation Pattern

### Pattern 1: Repository-Wide → Faculty-Level

**Current: Repository Statistics**

```python
# SPARQL: Count all published datasets
SELECT (COUNT(DISTINCT ?container) AS ?datasets)
WHERE {
  ?container djht:latest_published_version ?dataset .
  ?dataset djht:is_public "true"^^xsd:boolean .
}
```

**Extension: Faculty Statistics**

```python
# SPARQL: Count datasets by faculty
SELECT ?faculty_id (COUNT(DISTINCT ?container) AS ?datasets)
WHERE {
  ?container djht:latest_published_version ?dataset .
  ?dataset djht:is_public "true"^^xsd:boolean ;
           djht:faculty_id ?faculty_id .
}
GROUP BY ?faculty_id
```

**Key Change:** Add `GROUP BY ?faculty_id` and filter `djht:faculty_id`

### Pattern 2: Institution Page → Faculty Dashboard

**Current: Institution Page (`/institutions/Delft_University_of_Technology`)**

```python
def ui_institution(self, request, institution_name):
    # Returns: List of datasets (NOT statistics)
    datasets = self.db.datasets(groups=[institution_id], limit=100)
    return render("institutions.html", articles=datasets)
```

**Extension: Faculty Statistics Dashboard**

```python
def ui_faculty_statistics(self, request):
    # Returns: Statistics table
    stats = self.db.faculty_statistics(institution_id=28586)
    return render("faculty_stats.html", statistics=stats)
```

**Key Change:** Query aggregates (counts), not raw datasets

### Pattern 3: Python Dict → JSON API

**Current: Portal displays repository stats**

```python
# Backend
summary_data = self.db.repository_statistics()
# {"datasets": 1234, "authors": 567, ...}

# Frontend (portal.html)
<div>{{summary_data.datasets}} datasets</div>
```

**Extension: API returns faculty stats**

```python
# Backend
@app.route("/v3/faculties/statistics")
def api_faculty_statistics():
    stats = self.db.faculty_statistics(institution_id=28586)
    return json.dumps(stats)

# Response
[
  {"faculty_id": "AE", "datasets": 87, "percentage": 15.2},
  {"faculty_id": "AS", "datasets": 120, "percentage": 21.0}
]
```

---

## Concrete Examples: What to Build

### Example 1: API Endpoint

**Endpoint:** `GET /v3/faculties/statistics?institution=28586`

**Response:**
```json
{
  "institution_id": 28586,
  "institution_name": "TU Delft",
  "total_datasets": 572,
  "statistics": [
    {
      "faculty_id": "AE",
      "faculty_name": "Faculty of Aerospace Engineering",
      "datasets": 87,
      "percentage": 15.2,
      "total_views": 15000,
      "total_downloads": 3500,
      "total_cites": 120,
      "total_shares": 45
    },
    {
      "faculty_id": "AS",
      "faculty_name": "Faculty of Applied Sciences",
      "datasets": 120,
      "percentage": 21.0,
      "total_views": 28000,
      "total_downloads": 5200,
      "total_cites": 215,
      "total_shares": 78
    }
    // ... 6 more faculties
  ],
  "last_updated": "2024-12-09T10:30:00Z"
}
```

### Example 2: HTML Dashboard

**Page:** `/admin/faculties/statistics`

**UI Mockup:**

```
Faculty Statistics Dashboard - TU Delft
═════════════════════════════════════════════════════════════

Total Datasets: 572  |  Last Updated: 2024-12-09 10:30:00

┌──────────────────────────────────────────────────┬──────────┬────────┬───────────┬─────────────┐
│ Faculty                                          │ Datasets │   %    │ Downloads │    Views    │
├──────────────────────────────────────────────────┼──────────┼────────┼───────────┼─────────────┤
│ Faculty of Applied Sciences                      │   120    │ 21.0%  │   5,200   │   28,000    │
│ Faculty of Civil Engineering and Geosciences     │    95    │ 16.6%  │   4,100   │   22,000    │
│ Faculty of Aerospace Engineering                 │    87    │ 15.2%  │   3,500   │   15,000    │
│ Faculty of EEMCS                                 │    78    │ 13.6%  │   3,200   │   18,000    │
│ Faculty of Mechanical Engineering                │    65    │ 11.4%  │   2,800   │   12,000    │
│ Faculty of Architecture and Built Environment    │    52    │  9.1%  │   2,100   │   10,000    │
│ Faculty of TPM                                   │    45    │  7.9%  │   1,800   │    8,500    │
│ Faculty of Industrial Design Engineering         │    30    │  5.2%  │   1,100   │    5,200    │
└──────────────────────────────────────────────────┴──────────┴────────┴───────────┴─────────────┘

[Export CSV] [Export JSON] [View Charts]
```

### Example 3: SPARQL Query

**Template:** `statistics_faculty.sparql`

```sparql
{% extends "prefixes.sparql" %}
{% block query %}
SELECT ?faculty_id 
       (COUNT(DISTINCT ?container) AS ?datasets)
       (SUM(?total_views) AS ?total_views)
       (SUM(?total_downloads) AS ?total_downloads)
       (SUM(?total_cites) AS ?total_cites)
       (SUM(?total_shares) AS ?total_shares)
WHERE {
  GRAPH <{{state_graph}}> {
    # Get published datasets
    ?container rdf:type djht:DatasetContainer ;
               djht:latest_published_version ?dataset .
    
    ?dataset rdf:type djht:Dataset ;
             djht:is_public "true"^^xsd:boolean ;
             djht:faculty_id ?faculty_id .
    
    # Filter by institution (TU Delft only)
    ?dataset djht:institution_id {{institution_id}} .
    
    # Get engagement metrics
    OPTIONAL { ?dataset djht:total_views ?total_views . }
    OPTIONAL { ?dataset djht:total_downloads ?total_downloads . }
    OPTIONAL { ?dataset djht:total_cites ?total_cites . }
    OPTIONAL { ?dataset djht:total_shares ?total_shares . }
  }
}
GROUP BY ?faculty_id
ORDER BY DESC(?datasets)
{% endblock %}
```

---

## Resolution: Minimum Viable Statistics

### Recommended Scope (Phase 1)

**MUST HAVE (Tier 1):**
- ✅ `datasets` (count)
- ✅ `percentage` (of institution total)

**SHOULD HAVE (Tier 2):**
- ✅ `total_views`
- ✅ `total_downloads`
- ✅ `total_cites`
- ✅ `total_shares`

**RATIONALE:**
- Mirrors existing `repository_statistics()` pattern
- Data already exists in RDF store
- Single SPARQL query can retrieve all metrics
- No additional data collection required

### Out of Scope (Phase 1)

❌ **Multi-faculty attribution** (one dataset, multiple faculties) → Phase 2  
❌ **Author-level statistics** (by author faculty, not depositor) → Phase 2  
❌ **Department-level breakdown** (within faculties) → Phase 3  
❌ **Time-series analytics** (trends over time) → Phase 1.1  
❌ **Collaboration networks** (cross-faculty) → Phase 2  
❌ **Geographical mapping** (faculty locations) → Out of scope  

---

## Implementation Checklist

### Step 1: Define Metrics Clearly

- [x] Document: This file defines metrics
- [ ] Stakeholder approval: Get sign-off on metric list
- [ ] Test data: Create sample expected outputs

### Step 2: Extend RDF Schema

```turtle
djht:Account
  djht:faculty_id "AE"^^xsd:string .

djht:Dataset
  djht:faculty_id "AE"^^xsd:string .

djht:Faculty
  rdf:type djht:Faculty ;
  djht:id "AE"^^xsd:string ;
  djht:faculty_name "Faculty of Aerospace Engineering"^^xsd:string ;
  djht:institution_id 28586 .
```

### Step 3: Create SPARQL Queries

- [ ] `faculties.sparql` - List all faculties
- [ ] `statistics_faculty.sparql` - Aggregate by faculty
- [ ] `datasets_by_faculty.sparql` - Filter datasets by faculty

### Step 4: Implement Database Methods

```python
def faculty_statistics(self, institution_id=28586, faculty_id=None):
    """Returns list of dicts with faculty stats."""
    pass

def faculty_datasets(self, faculty_id, limit=10):
    """Returns datasets for a faculty."""
    pass
```

### Step 5: Build API Endpoints

- [ ] `GET /v3/faculties` - List faculties
- [ ] `GET /v3/faculties/statistics` - Get all faculty stats
- [ ] `GET /v3/faculties/{id}` - Get one faculty detail
- [ ] `GET /v3/faculties/{id}/datasets` - Get faculty datasets

### Step 6: Create UI Dashboard

- [ ] HTML template `faculty_statistics.html`
- [ ] Table with sortable columns
- [ ] Export buttons (CSV, JSON)
- [ ] Refresh button (invalidate cache)

---

## Validation Criteria

### How to Know If Implementation is Correct

✅ **Completeness:**
- All 8 TU Delft faculties appear in statistics
- Sum of faculty datasets ≤ total TU Delft datasets (some may have no faculty)
- Percentages sum to ≤ 100%

✅ **Accuracy:**
- Manual count of 5 random faculties matches API output
- Faculty A datasets when queried individually = Faculty A datasets in aggregate query
- No double-counting (each dataset counted once per faculty)

✅ **Performance:**
- Statistics query completes in <150ms
- Dashboard page loads in <2 seconds
- Caching reduces repeated query time to <10ms

✅ **Consistency:**
```python
# Validation query
repo_stats = db.repository_statistics()
tu_delft_stats = db.institution_statistics(28586)
faculty_stats = db.faculty_statistics(28586)

assert sum(f["datasets"] for f in faculty_stats) <= tu_delft_stats["datasets"]
assert tu_delft_stats["datasets"] <= repo_stats["datasets"]
```

---

## Summary: Clear Definition

**"Statistics per institute" in this assignment means:**

1. **Institute = TU Delft (Institution ID 28586)**
2. **"Per" = Grouped by faculty within TU Delft**
3. **Statistics = Same metrics as repository-wide:**
   - Dataset count (MUST)
   - Percentage of total (MUST)
   - Views, downloads, cites, shares (SHOULD)
4. **Approach = Depositor-based** (not author-based)
5. **Scope = Tier 1 + Tier 2 metrics**

**Output Example:**
```json
[
  {"faculty": "Aerospace Engineering", "datasets": 87, "%": 15.2, "downloads": 3500},
  {"faculty": "Applied Sciences", "datasets": 120, "%": 21.0, "downloads": 5200}
]
```

**Not Included:**
- Multi-faculty datasets
- Author-level attribution
- Department-level breakdown
- Time-series trends
- Network analysis

---

## Related Documents

- [STATISTICS_OUTPUT_EXAMPLES.md](STATISTICS_OUTPUT_EXAMPLES.md) - Current output formats
- [INSTITUTION_STATISTICS_GUIDE.md](INSTITUTION_STATISTICS_GUIDE.md) - How current stats work
- [../assignment/SOLUTION_ARCHITECTURE.md](../assignment/SOLUTION_ARCHITECTURE.md) - Full Phase 1 spec
- [../assignment/IMPLEMENTATION_ROADMAP.md](../assignment/IMPLEMENTATION_ROADMAP.md) - 5-week plan
