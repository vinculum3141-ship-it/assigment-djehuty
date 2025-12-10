# Demo Quick Reference - Faculty Statistics Prototype

**For Interview**: 10-15 minute demonstration  
**What to Show**: Working RDF model + Python backend + Tests  
**Context**: Gabriela confirmed prototype scope is exactly right ✅

---

## 🎯 Gabriela's 3 Challenges (Quick Reference)

### Challenge 1: "Organizations" Field Unreliable (Free Text)
**Our Answer**: ✅ Pattern matching on real data → 44% coverage, 100% accuracy

### Challenge 2: Multiple Authors from Different Universities
**Our Answer**: ✅ Follow existing approach (depositing author), note as future enhancement

### Challenge 3: ORCID IDs Not Mandatory
**Our Answer**: ✅ Use "Organizations" field instead (89% availability)

**Key Point**: Gabriela said identifying limitations is "welcome and expected" ✅

---

## 🚀 Quick Start (Before Demo)

```bash
# 1. Start environment
cd ~/Projects/assigment-djehuty
docker-compose ps  # Check Virtuoso is running
source djehuty-env/bin/activate

# 2. Verify setup
python prototype/insert_sample_faculties.py  # Should show 3 faculties inserted
python prototype/test_faculty_statistics.py  # Should show all tests passing
```

---

## 📋 Demo Commands (In Order)

### 1. Show Project Structure (30 sec)
```bash
tree -L 2 prototype/
```

### 2. Show RDF Data (1 min)
```bash
cat prototype/sample_faculties.ttl
```

### 3. Query Live Triple Store (1 min)
```bash
curl -X POST http://localhost:8890/sparql \
  -H "Content-Type: application/sparql-query" \
  -d "PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      SELECT ?faculty_name ?group_id WHERE {
        ?f rdf:type djht:Faculty ;
           djht:faculty_name ?faculty_name ;
           djht:group_id ?group_id .
      }" | jq '.results.bindings'
```

### 4. Show SPARQL Template (30 sec)
```bash
cat djehuty/src/djehuty/web/resources/sparql_templates/statistics_faculty.sparql
```

### 5. Show Python Method (30 sec)
```bash
grep -A 25 "def faculty_statistics" djehuty/src/djehuty/web/database.py
```

### 6. Run Tests (1 min)
```bash
python prototype/test_faculty_statistics.py
```

### 7. Interactive Python Demo (3 min)
```bash
python
```
```python
import sys
sys.path.insert(0, 'djehuty/src')
from djehuty.web.config import config
from djehuty.web.database import SparqlInterface
import json

db = SparqlInterface()
db.cache.storage = 'data/cache'
db.setup_sparql_endpoint()

# Faculty statistics
results = db.faculty_statistics()
print(json.dumps(results, indent=2, default=str))

# Filter by institution
tu_delft = db.faculty_statistics(institution_id=28586)
print(f"\nTU Delft faculties: {len(tu_delft)}")
for f in tu_delft:
    print(f"  {f['faculty_short_name']}: {f['dataset_count']} datasets")

# Institution statistics (wrapper)
inst = db.institution_statistics()
print(f"\nInstitution-level: {len(inst)} groups")
```

### 8. Show Documentation (30 sec)
```bash
ls -la docs/analysis/
cat prototype/PROGRESS.md | head -30
```

---

## 💬 Key Talking Points

**Opening**:
> "I built a 4-6 day working prototype instead of 2.5-week full implementation. Let me show you what's running right now."

**RDF Model**:
> "I extended your existing `djht:group_id` pattern - same mechanism, finer granularity."

**Backend**:
> "The `faculty_statistics()` method mirrors your `dataset_statistics()` pattern. I'm not reinventing the wheel."

**Tests**:
> "All 5 tests passing - basic retrieval, filtering, pagination, JSON serialization, institution wrapper."

**Hierarchy**:
> "Same institution broken down by faculty: 4 institutions → 47 faculties. Extension, not replacement."

**Next Steps**:
> "Phase 1: RDF + backend complete. Phase 2A: Migration analysis complete (44% coverage proven). Phase 2B: Migration logic ready (writes need permissions). Phase 3: Dashboard next."

---

## 🎯 Must-Show Features

1. ✅ **Live SPARQL query** - Proves data in triple store
2. ✅ **Python method call** - Proves backend works
3. ✅ **Test suite passing** - Proves quality
4. ✅ **Two-level hierarchy** - Proves extension pattern
5. ✅ **JSON output** - Proves API-ready

---

## ❓ Q&A Quick Answers

**"Why prototype?"**
> "Prove concept in 2 days vs 2.5 weeks. Working code speaks louder than design docs."

**"Real data migration?"**
> "I analyzed 9 real datasets: 44% have extractable faculty info with 100% pattern matching accuracy. Migration logic ready in `migrate_sample_faculty.py`, but writes blocked by Virtuoso permissions. Concept proven - execution needs configuration."

**"Performance?"**
> "SPARQL GROUP BY (database-level), caching, pagination. Pre-aggregate for thousands of datasets."

**"Multiple faculties per dataset?"**
> "Phase 2: Add faculty_id to Author, not just Account. Support multi-valued via RDF lists."

**"Production differences?"**
> "Add: error handling, validation, transactions, monitoring, API auth, rate limiting, OpenAPI spec."

---

## 🆘 Emergency Backup

**If demo breaks**:
> "Let me show you screenshots of the working demo I prepared earlier..."

**Have ready**:
- Terminal with tests passing
- Python REPL with results
- SPARQL query output
- Code in editor

---

## ✅ Pre-Demo Checklist

- [ ] Virtuoso running (`docker-compose ps`)
- [ ] Environment activated (`source djehuty-env/bin/activate`)
- [ ] Faculties inserted (3 should exist)
- [ ] Tests passing (all 5)
- [ ] Terminal window clean
- [ ] Editor with files ready:
  - `statistics_faculty.sparql`
  - `database.py` (faculty_statistics method)
  - `sample_faculties.ttl`
- [ ] Backup screenshots ready

---

## 📊 Expected Outputs

**Faculty Query Result**:
```json
[
  {
    "faculty_name": {"value": "Faculty of EEMCS"},
    "group_id": {"value": "285860001"}
  }
]
```

**Python Method Output**:
```json
{
  "faculty_id": 285860001,
  "faculty_name": "Faculty of EEMCS",
  "faculty_short_name": "EEMCS",
  "institution_id": 28586,
  "dataset_count": 0
}
```

**Test Result**:
```
✅ ALL TESTS PASSED!
```

---

**Time Budget**: 10-15 minutes total  
**Fallback**: Screenshots + code walkthrough  
**Confidence**: HIGH (working code, all tested)

Good luck! 🚀
