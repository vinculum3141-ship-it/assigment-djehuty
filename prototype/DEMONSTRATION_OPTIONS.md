# Prototype Demonstration Options

This document lists all the ways you can demonstrate the Faculty Statistics prototype output, both for institution-level and faculty-level statistics.

---

## 🎯 Quick Summary

You have **4 different ways** to demonstrate the prototype:

1. **Command-line demonstration** - Full statistics output
2. **Visual dashboard** - Charts and graphs  
3. **API testing** - Backend method testing
4. **SPARQL queries** - Raw RDF queries

---

## 1️⃣ Command-Line Demonstration (RECOMMENDED for interview)

### Run the comprehensive demo script:

```bash
python3 prototype/demo_statistics.py
```

### What it shows:
- ✅ **Institution statistics** - Table with ID, name, count
- ✅ **Faculty statistics** - Table with code, name, count  
- ✅ **Granularity comparison** - Shows improvement multiplier
- ✅ **JSON output** - Sample API response format
- ✅ **Summary** - Status of each component

### Output example:
```
================================================================================
  INSTITUTION-LEVEL STATISTICS (Current System)
================================================================================

Institution ID  Name                           Datasets  
------------------------------------------------------------
28586           TU Delft                       3         
28598           Utrecht University             4         
28592           TU Eindhoven                   1         
28589           University of Twente           1         

================================================================================
  FACULTY-LEVEL STATISTICS (Prototype Feature)
================================================================================

Faculty Code    Name                                          Datasets  
---------------------------------------------------------------------------
AE              Faculty of Aerospace Engineering              0         
AS              Faculty of Applied Sciences                   0         
EEMCS           Faculty of Electrical Engineering, Math...    0         
```

---

## 2️⃣ Visual Dashboard (RECOMMENDED for visual learners)

### Option A: Open directly in browser

```bash
# Get the full path
realpath prototype/faculty_dashboard.html

# Then open in browser:
# file:///home/ruby/Projects/assigment-djehuty/prototype/faculty_dashboard.html
```

Or on Linux:
```bash
xdg-open prototype/faculty_dashboard.html
```

### Option B: Open in VS Code Simple Browser

In VS Code:
1. Right-click `prototype/faculty_dashboard.html`
2. Select "Open with Live Server" or "Preview"

### What it shows:
- 📊 **5 interactive charts**:
  1. Datasets per Institution (bar chart)
  2. Datasets per Faculty (bar chart)
  3. Institution vs Faculty granularity (pie chart)
  4. Faculty distribution within TU Delft (pie chart)
  5. Timeline showing progression

- 🎨 **Professional styling** with Chart.js
- 📱 **Responsive design**
- ⚠️ **Disclaimer** about mock data clearly displayed

### Data source:
The dashboard reads from `prototype/dashboard_data.json`

---

## 3️⃣ API Testing (RECOMMENDED for technical demo)

### Run the backend method tests:

```bash
python3 prototype/test_faculty_statistics.py
```

### What it tests:
- ✅ `faculty_statistics()` method
- ✅ Filtering by institution_id
- ✅ Pagination (limit parameter)
- ✅ JSON serialization for API
- ✅ `institution_statistics()` wrapper

### Output example:
```
======================================================================
TEST 1: Get all faculty statistics
======================================================================

📊 Found 3 faculties:

Faculty: AE
  ID: 285860002
  Full Name: Faculty of Aerospace Engineering
  Institution ID: 28586
  Dataset Count: 0

✅ TEST 1 PASSED - faculty_statistics() works!
```

---

## 4️⃣ SPARQL Queries (RECOMMENDED for RDF experts)

### Access the SPARQL interface:

```
http://localhost:8890/sparql
```

### Query 1: List Faculty entities (WORKS - Returns 3 results)

```sparql
PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT (STR(?faculty_name) AS ?name) (STR(?faculty_short_name) AS ?short_name) ?group_id
WHERE {
  GRAPH <https://data.4tu.nl/portal/self-test> {
    ?faculty rdf:type djht:Faculty ;
             djht:faculty_name ?faculty_name ;
             djht:faculty_short_name ?faculty_short_name ;
             djht:group_id ?group_id .
  }
}
```

**Result**: Returns 3 faculties (EEMCS, AE, AS) ✅

### Query 2: Institution statistics (WORKS - Returns group_ids)

```sparql
PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?group_id (COUNT(DISTINCT ?dataset) AS ?dataset_count)
WHERE {
  GRAPH <https://data.4tu.nl> {
    ?container rdf:type djht:DatasetContainer ;
               djht:latest_published_version ?dataset .
    ?dataset   rdf:type djht:Dataset ;
               djht:is_public "true"^^xsd:boolean ;
               djht:group_id ?group_id .
  }
}
GROUP BY ?group_id
ORDER BY DESC(?dataset_count)
```

**Result**: Returns institution group_ids with dataset counts ✅

### Query 3: Faculty statistics with datasets (Returns empty)

```sparql
PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT (STR(?faculty_name) AS ?name) (STR(?faculty_short_name) AS ?short_name) (COUNT(DISTINCT ?dataset) AS ?dataset_count)
WHERE {
  GRAPH <https://data.4tu.nl/portal/self-test> {
    ?faculty      rdf:type                      djht:Faculty ;
                  djht:group_id                 ?group_id ;
                  djht:faculty_name             ?faculty_name ;
                  djht:faculty_short_name       ?faculty_short_name .
  }
  
  GRAPH <https://data.4tu.nl> {
    ?container    rdf:type                      djht:DatasetContainer ;
                  djht:latest_published_version ?dataset .
    ?dataset      rdf:type                      djht:Dataset ;
                  djht:is_public                "true"^^xsd:boolean ;
                  djht:group_id                 ?group_id .
  }
}
GROUP BY ?faculty_name ?faculty_short_name
ORDER BY DESC(?dataset_count)
```

**Result**: Returns empty (datasets not migrated to faculty group_ids yet) ⚠️

**Why**: Faculty entities exist, but datasets still use institution group_ids (28586) instead of faculty group_ids (285860001, etc.)

---

## 📋 Interview Demonstration Flow (RECOMMENDED)

### Option 1: Quick Demo (5 minutes)

1. **Run demo script**: `python3 prototype/demo_statistics.py`
2. **Explain output**: "Institution-level shows 4 institutions, faculty-level shows 3 faculties"
3. **Show dashboard**: Open `faculty_dashboard.html` in browser
4. **Key point**: "Faculties exist, datasets not migrated yet due to write permissions"

### Option 2: Technical Deep Dive (10 minutes)

1. **Show Faculty entities exist**: SPARQL Query 1 → 3 results ✅
2. **Show institution data exists**: SPARQL Query 2 → group_ids with counts ✅
3. **Show migration gap**: SPARQL Query 3 → empty (expected) ⚠️
4. **Explain**: "Faculty entities created, migration logic ready, execution blocked"
5. **Run tests**: `python3 prototype/test_faculty_statistics.py`
6. **Show JSON**: Point to JSON output in test results

### Option 3: Visual First (7 minutes)

1. **Open dashboard**: `faculty_dashboard.html` in browser
2. **Walk through charts**: "5 visualizations showing institution vs faculty"
3. **Explain disclaimer**: "Mock data because migration blocked"
4. **Run demo script**: Show command-line output
5. **Key takeaway**: "Architecture works, data exists, just need write permissions"

---

## 🎯 What Each Method Demonstrates

| Method | Demonstrates | Best For |
|--------|--------------|----------|
| **demo_statistics.py** | Complete output, comparison, JSON | General interview |
| **faculty_dashboard.html** | Visual charts, professional UI | Management/stakeholders |
| **test_faculty_statistics.py** | Backend methods, API testing | Technical interview |
| **SPARQL queries** | RDF data model, entity existence | RDF/semantic web experts |

---

## ✅ Key Points to Emphasize

1. **Faculty entities exist** (proven by SPARQL Query 1)
2. **Faculty statistics method works** (proven by test_faculty_statistics.py)
3. **Institution statistics wrapper works** (proven by demo_statistics.py)
4. **Migration logic is complete** (shown in migrate_sample_faculty.py)
5. **Write permissions block execution** (expected limitation, documented)

---

## 🚨 Expected Questions & Answers

### Q: "Why are dataset counts zero for faculties?"

**A**: "Faculty RDF entities exist in the `portal/self-test` graph (you can verify with SPARQL). However, datasets in the base graph still reference institution group_ids (28586) instead of faculty group_ids (285860001). The migration script is ready but write permissions are disabled in the test environment. The prototype demonstrates the architecture and data model—execution would be straightforward in production."

### Q: "How do you know the faculty_statistics() method works?"

**A**: "Run `python3 prototype/test_faculty_statistics.py` - it connects to the SPARQL endpoint, queries Faculty entities, and returns structured data. All 5 tests pass. The method correctly retrieves faculty metadata (name, code, institution_id) from RDF. Dataset counts are zero because migration hasn't run, but the infrastructure works."

### Q: "Can you show me the actual data in the RDF store?"

**A**: "Yes, open http://localhost:8890/sparql and run this query: [paste Query 1]. You'll see 3 faculties: EEMCS (group_id: 285860001), AE (285860002), and AS (285860003). These are real RDF entities with proper djht:Faculty type and all required properties."

---

## 📁 Related Files

- `prototype/demo_statistics.py` - Main demonstration script
- `prototype/test_faculty_statistics.py` - API testing script  
- `prototype/faculty_dashboard.html` - Visual dashboard
- `prototype/dashboard_data.json` - Dashboard data source
- `prototype/MANUAL_QUERY_EXPLANATION.md` - SPARQL query documentation
- `prototype/check_data.py` - Quick RDF store verification

---

## 🔗 Quick Links

- SPARQL Interface: http://localhost:8890/sparql
- Dashboard: file:///home/ruby/Projects/assigment-djehuty/prototype/faculty_dashboard.html
- Demo Script: `python3 prototype/demo_statistics.py`
- Tests: `python3 prototype/test_faculty_statistics.py`
