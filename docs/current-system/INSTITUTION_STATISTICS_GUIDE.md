# Institution Statistics in Current Djehuty Implementation

## Overview

This document explains how the current Djehuty implementation displays statistics per institution (organization). The system currently provides **institution-level** statistics but NOT faculty-level statistics (which is what the assignment asks you to implement).

---

## How Institution Statistics Are Currently Displayed

### 1. **Portal Home Page (`/portal` or `/`)**

**Location:** `/home/ruby/Projects/assigment-djehuty/djehuty/src/djehuty/web/wsgi.py` (Line 3508)

#### Code Flow:

```python
def ui_home(self, request):
    """Implements /portal."""
    
    # Get repository-wide statistics
    summary_data = self.db.repository_statistics()
    
    # Format the numbers with commas
    for key in summary_data:
        summary_data[key] = f"{int(summary_data[key]):,}"
    
    # Render the portal template
    return self.__render_template(request, "portal.html",
                                   summary_data=summary_data,
                                   show_portal_summary=config.show_portal_summary,
                                   show_institutions=config.show_institutions,
                                   ...)
```

#### What Statistics Are Shown:

The portal displays **repository-wide** statistics (NOT per institution):

- **Datasets**: Total number of published datasets
- **Authors**: Total number of public authors
- **Collections**: Total number of published collections
- **Files**: Total number of files
- **Bytes**: Total storage used

#### Template Location:

`/home/ruby/Projects/assigment-djehuty/djehuty/src/djehuty/web/resources/html_templates/portal.html`

The statistics are displayed in a centered summary box:

```html
<div id="portal-summary">
  <div class="portal-summary-item">
    <div class="portal-summary-item-left">{{summary_data[item]}}</div>
    <div class="portal-summary-item-right">{{item}}</div>
  </div>
</div>
```

---

### 2. **Institution Tiles on Portal**

The portal home page shows clickable tiles for each institution:

```html
<h1>Institutions</h1>
<div class="tiles-wrapper">
  <ul class="tiles">
    <li><a href="/institutions/Delft_University_of_Technology">
        <img src="/static/images/portal/tudelft.jpg" alt="TU Delft"></a></li>
    <li><a href="/institutions/University_of_Twente">
        <img src="/static/images/portal/utwente.jpg" alt="UTwente"></a></li>
    <li><a href="/institutions/Eindhoven_University_of_Technology">
        <img src="/static/images/portal/tueindhoven.jpg" alt="TU Eindhoven"></a></li>
    <li><a href="/institutions/Wageningen_University_Research">
        <img src="/static/images/portal/wur.jpg" alt="WUR"></a></li>
  </ul>
</div>
```

These tiles link to individual institution pages.

---

### 3. **Individual Institution Page (`/institutions/<institution_name>`)**

**Route:** `/institutions/<institution_name>` (e.g., `/institutions/Delft_University_of_Technology`)

**Location:** `/home/ruby/Projects/assigment-djehuty/djehuty/src/djehuty/web/wsgi.py` (Line 3977)

#### Code Flow:

```python
def ui_institution(self, request, institution_name):
    """Implements /institutions/<name>."""
    
    # Convert URL format to group name (e.g., "Delft_University_of_Technology" → "Delft University of Technology")
    group_name = institution_name.replace('_', ' ')
    
    # Get the institution group from the database
    group = self.db.group_by_name(group_name)
    
    # Get all sub-groups (e.g., faculties within the institution)
    sub_groups = self.db.group_by_name(group_name, startswith=True)
    sub_group_ids = [item['group_id'] for item in sub_groups]
    
    # Get datasets for this institution and all its sub-groups
    datasets = self.db.datasets(groups=sub_group_ids,
                                is_published=True,
                                limit=100)
    
    # Render the institution template
    return self.__render_template(request, "institutions.html",
                                   articles=datasets,
                                   group=group,
                                   sub_groups=sub_groups)
```

#### What This Page Shows:

- **Institution name** (e.g., "Delft University of Technology")
- **List of datasets** deposited by this institution (up to 100)
- **Sub-groups** (if any exist in the RDF store)

**Note:** This page shows a **list of datasets** but does NOT show statistics like:
- Total number of datasets per institution
- Total number of datasets per faculty
- Breakdown by faculty

---

## How Statistics Are Calculated (Backend)

### SPARQL Queries

Statistics are calculated using SPARQL queries against the Virtuoso triple store.

**Location:** `/home/ruby/Projects/assigment-djehuty/djehuty/src/djehuty/web/resources/sparql_templates/`

#### 1. **Total Datasets** (`statistics_datasets.sparql`)

```sparql
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

#### 2. **Total Authors** (`statistics_authors.sparql`)

```sparql
SELECT (COUNT(DISTINCT ?author) AS ?authors)
WHERE {
  GRAPH <{{state_graph}}> {
    ?author     rdf:type        djht:Author .
    ?author     djht:is_public  "true"^^xsd:boolean .
  }
}
```

#### 3. **Total Collections** (`statistics_collections.sparql`)

```sparql
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

#### 4. **Files and Bytes**

Calculated in Python code by summing file sizes from `repository_file_statistics()` and `repository_datalink_statistics()`.

---

## How Institutions Are Stored in RDF

Institutions are stored as `djht:InstitutionGroup` entities in the triple store.

### SPARQL Query to Get Institution by Name

**Template:** `group_by_name.sparql`

```sparql
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

### Datasets Linked to Institutions

Datasets are linked to institutions via the `djht:group_id` predicate on the `djht:Account` (depositor).

**Current Structure:**
```
djht:Account
  ├─ djht:account_id
  ├─ djht:email
  ├─ djht:group_id → djht:InstitutionGroup
  └─ ...

djht:Dataset
  ├─ djht:account_id → djht:Account
  └─ ...
```

When you query datasets by institution, the system:
1. Finds the `group_id` for the institution
2. Finds all accounts with that `group_id`
3. Finds all datasets deposited by those accounts

---

## What's Missing (The Assignment Gap)

### Current System Limitations:

❌ **No faculty-level statistics**
- The portal shows only repository-wide totals
- Institution pages show only a list of datasets (not statistics)
- No breakdown by faculty within an institution

❌ **No faculty information stored**
- `djht:Account` has `group_id` (institution) but **NO** `faculty_id`
- No way to filter/aggregate datasets by faculty

❌ **No statistics dashboard**
- No page that shows "Faculty X has deposited Y datasets"
- No admin interface to view faculty statistics
- No API endpoints to retrieve faculty statistics

---

## What You Need to Implement (Phase 1)

Based on the assignment requirements, you need to add:

### 1. **Data Model Changes**

Add `faculty_id` to `djht:Account`:

```
djht:Account
  ├─ djht:account_id
  ├─ djht:email
  ├─ djht:group_id → djht:InstitutionGroup (EXISTING - institution)
  ├─ djht:faculty_id (NEW - faculty within institution)
  └─ ...
```

### 2. **New SPARQL Queries**

Create queries to:
- Get all faculties (e.g., `statistics_faculties.sparql`)
- Count datasets per faculty (e.g., `datasets_by_faculty.sparql`)
- Get faculty details by ID

### 3. **New API Endpoints**

- `GET /v3/faculties` - List all faculties
- `GET /v3/faculties/{id}` - Get faculty details
- `GET /v3/faculties/{id}/datasets` - List datasets by faculty
- `GET /v3/faculties/statistics` - Get statistics for all faculties
- `PATCH /v3/accounts/{id}` - Update account faculty
- `POST /v3/datasets` - Auto-fill faculty from depositor

### 4. **New UI Components**

- **Registration form:** Dropdown to select faculty (extend existing `/account/register` page)
- **Dataset deposit form:** Auto-fill faculty from depositor account (extend existing `/my/data` page)
- **Statistics dashboard:** New page `/admin/faculties/statistics` showing table with columns:
  - Faculty Name
  - Number of Datasets
  - Percentage of Total
  - Last Updated

### 5. **Migration Script**

Migrate ~200 existing depositor accounts from `Organizations` field to `faculty_id` predicate.

---

## How to Access the Current Portal

1. **Start Djehuty:**
   ```bash
   cd /home/ruby/Projects/assigment-djehuty/djehuty
   python3 -m djehuty.web.ui --address 0.0.0.0 --port 8080 --config-file djehuty.xml
   ```

2. **Access in Browser:**
   - Home page with repository statistics: `http://localhost:8080/`
   - Specific institution: `http://localhost:8080/institutions/Delft_University_of_Technology`

3. **View Statistics:**
   - Repository-wide totals are shown on the home page in the "Summary" section
   - Click on an institution tile to see datasets for that institution

---

## Key Files Reference

### Backend (Python)

| File | Purpose |
|------|---------|
| `djehuty/src/djehuty/web/wsgi.py` | Main HTTP request handler, routes |
| `djehuty/src/djehuty/web/database.py` | SPARQL query interface |
| `djehuty/src/djehuty/web/config.py` | Configuration state |

### SPARQL Templates

| File | Purpose |
|------|---------|
| `statistics_datasets.sparql` | Count total datasets |
| `statistics_authors.sparql` | Count total authors |
| `statistics_collections.sparql` | Count total collections |
| `statistics_files.sparql` | Get file sizes |
| `group_by_name.sparql` | Get institution by name |
| `datasets.sparql` | Query datasets with filters |

### HTML Templates

| File | Purpose |
|------|---------|
| `portal.html` | Home page with statistics |
| `institutions.html` | Institution page with dataset list |
| `layout.html` | Base template for all pages |

---

## Summary

**Current Djehuty Implementation:**
- ✅ Shows **repository-wide** statistics (datasets, authors, collections, files, bytes)
- ✅ Shows **institution tiles** on portal home page
- ✅ Shows **list of datasets per institution** on `/institutions/<name>` page
- ❌ Does NOT show **faculty-level statistics**
- ❌ Does NOT have a **statistics dashboard**
- ❌ Does NOT store **faculty information** in `djht:Account`

**What You Need to Build (Phase 1):**
- Add `faculty_id` to `djht:Account`
- Create SPARQL queries for faculty statistics
- Build 6 API endpoints
- Build 3 UI components (registration dropdown, dataset auto-fill, statistics dashboard)
- Migrate ~200 depositor accounts

**Documentation Reference:**
- Complete Phase 1 architecture: [`docs/assignment/SOLUTION_ARCHITECTURE.md`](../assignment/SOLUTION_ARCHITECTURE.md)
- Implementation roadmap: [`docs/assignment/IMPLEMENTATION_ROADMAP.md`](../assignment/IMPLEMENTATION_ROADMAP.md)
- Quick reference: [`docs/assignment/ARCHITECTURE_SUMMARY.md`](../assignment/ARCHITECTURE_SUMMARY.md)

---

**Next Steps:** Review the implementation roadmap and start with Week 1 (Foundation) to configure faculties and extend the RDF schema to support `faculty_id`.
