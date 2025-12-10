# Faculty Statistics Prototype

This directory contains the **working prototype** for the faculty-level statistics feature, created as part of the interview assignment for 4TU.ResearchData.

## 🎯 Purpose

Demonstrate a **4-6 day prototype** (instead of 2.5-week full implementation) that shows:
1. **RDF schema extension** - Faculty entities and predicates
2. **Backend aggregation** - Python methods for faculty statistics
3. **Migration analysis** - Data quality assessment and sample migration
4. **Visualization** - Dashboard showing both institution and faculty levels

## 📁 Structure

```
prototype/
├── README.md                      # This file
├── sample_faculties.ttl           # RDF data: 3 sample faculties
├── insert_sample_faculties.py     # Script: Insert faculties into triple store
├── check_data.py                  # Utility: Inspect triple store contents
└── (more files to come)
```

## ✅ Phase 1: RDF Data Model Extension (COMPLETE)

### What We Built

1. **Sample Faculty Entities** (`sample_faculties.ttl`)
   - 3 TU Delft faculties in Turtle (RDF) format
   - Follows existing `djht:InstitutionGroup` pattern
   - Each faculty has: id, group_id, name, short_name, code, institution_id

2. **Insertion Script** (`insert_sample_faculties.py`)
   - Connects to Virtuoso SPARQL endpoint
   - Inserts faculty entities using RDF triples
   - Links datasets to faculties via `group_id` predicate
   - Verification queries to confirm success

### How to Run

```bash
# From assigment-djehuty root directory
cd prototype

# Insert sample faculty data
python insert_sample_faculties.py

# Check what's in the store
python check_data.py
```

### What the Data Looks Like

```turtle
# Faculty Entity
djehuty:faculty_285860001
    rdf:type djht:Faculty ;
    djht:id "285860001"^^xsd:integer ;
    djht:faculty_name "Faculty of EEMCS"@en ;
    djht:faculty_short_name "EEMCS"@en ;
    djht:faculty_code "EEMCS" ;
    djht:institution_id "28586"^^xsd:integer ;
    djht:group_id "285860001"^^xsd:integer .
```

### Key Design Decision: Reuse `group_id`

**Why**: Existing Djehuty uses `djht:group_id` for institution grouping. Our faculty implementation **extends this pattern** at finer granularity.

**Advantage**: Proves the extension pattern works without replacing existing infrastructure.

**Evidence for Interview**: "We're not reinventing the wheel - we're showing how the existing grouping mechanism scales to sub-institutional levels."

## 📊 Current Status

| Task | Status | Notes |
|------|--------|-------|
| RDF Schema Extension | ✅ Complete | 3 sample faculties inserted |
| Backend Methods | 🔄 In Progress | Next: faculty_statistics() |
| API Endpoints | ⏳ Pending | After backend methods |
| Migration Analysis | ⏳ Pending | Phase 2 |
| Dashboard | ⏳ Pending | Phase 3 |

## 🔜 Next Steps

### Immediate (Phase 1 - Backend)

1. **Create `faculty_statistics()` method**
   - File: `djehuty/src/djehuty/web/database.py`
   - Pattern: Similar to existing `dataset_statistics(group_ids=[])`
   - SPARQL query: Aggregate datasets by faculty group_id

2. **Create API endpoint**
   - Route: `/v2/stats/faculty` or `/v2/stats/faculty/<id>`
   - File: `djehuty/src/djehuty/web/wsgi.py`
   - Returns: JSON with faculty statistics

3. **Test with curl**
   ```bash
   curl http://localhost:8080/v2/stats/faculty
   ```

### Phase 2 (Migration Prototype)

- Analysis script: Scan existing datasets for faculty info
- Sample migration: Extract faculty from metadata (ORCID, organizations field)
- Data quality report: Coverage percentage, edge cases

### Phase 3 (Visualization)

- Dashboard HTML with 5 charts
- Show BOTH institution (existing) AND faculty (new) levels
- Live demo-ready for interview presentation

## 🎤 Interview Talking Points

### "Why a prototype, not full implementation?"

> "I assessed the assignment scope and realized a 2.5-week full implementation would be too much for an interview presentation. Instead, I built a **4-6 day working prototype** that demonstrates:
>
> 1. **Technical understanding** - I can extend your RDF schema
> 2. **System knowledge** - I understand how Djehuty's grouping mechanism works
> 3. **Practical approach** - The prototype proves the design works before committing to full development
> 4. **Interview-ready** - I have live demo-able code in 10-15 minutes"

### "Why show both institution AND faculty statistics?"

> "This was a key insight from analyzing the partial implementation. By showing:
> - **Institution level** (existing - 4 groups)
> - **Faculty level** (new - 47 groups)
>
> I demonstrate that the extension pattern WORKS. You get finer granularity (4 → 47 breakdown) without replacing existing infrastructure. This answers 'Why not just institutions?' preemptively."

### "What's the advantage of this approach?"

> "Three main advantages:
> 1. **Low risk** - Extends existing `group_id` pattern, doesn't replace it
> 2. **Backwards compatible** - Institutions still work as before
> 3. **Scalable** - Same pattern can extend to departments, labs, research groups in the future"

## 📝 Documentation References

- **Full Prototype Plan**: `docs/analysis/PROTOTYPE_PLAN.md` (1700+ lines)
- **Phase 1 Focus**: `docs/analysis/PHASE1_FOCUS.md`
- **Assignment Requirements**: `docs/requirements/REQUIREMENTS_ANALYSIS.md`
- **Current System Analysis**: `docs/current-system/CODEBASE_ANALYSIS.md`

## 🧪 Testing

```bash
# Check if Virtuoso is running
curl http://localhost:8890/sparql

# Run prototype scripts
python prototype/insert_sample_faculties.py
python prototype/check_data.py

# Query SPARQL directly (optional)
curl -X POST http://localhost:8890/sparql \
  -H "Content-Type: application/sparql-query" \
  -d "PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
      SELECT ?faculty_name WHERE { ?f a djht:Faculty ; djht:faculty_name ?faculty_name . }"
```

## 🐛 Troubleshooting

### "Cannot connect to SPARQL endpoint"
```bash
# Check if Virtuoso Docker container is running
cd djehuty
docker-compose ps

# If not running, start it
docker-compose up -d
```

### "No datasets linked to faculties"
This is expected! The system starts empty. We inserted faculty entities to demonstrate the RDF schema extension. Dataset linking would happen during real migration.

### "Configuration file not found"
```bash
# Make sure you're in the correct directory
cd /home/ruby/Projects/assigment-djehuty
python prototype/insert_sample_faculties.py
```

## 📈 Timeline

- **Day 1 (Dec 10)**: RDF model + sample data ✅
- **Day 2 (Next)**: Backend methods + API
- **Day 3-4**: Migration analysis + sample migration
- **Day 5-6**: Dashboard with both levels
- **Day 7**: Presentation prep

---

**Last Updated**: December 10, 2024  
**Author**: Job Interview Candidate  
**Purpose**: 10-15 minute demo for Senior Software Developer position
