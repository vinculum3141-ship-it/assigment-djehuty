# Faculty Statistics Prototype - Live Demo Script

**Purpose**: 10-15 minute interview demonstration  
**Audience**: Technical interviewers (4TU.ResearchData team)  
**Goal**: Prove technical competence, system understanding, and practical approach

---

## 🎯 Demo Structure (10-15 minutes)

### Timeline Breakdown
- **Setup**: 1 min (show environment)
- **Part 1: Problem & Discovery**: 2 min
- **Part 2: Live Demo - RDF Model**: 3 min
- **Part 3: Live Demo - Backend Methods**: 3 min
- **Part 4: Two-Level Comparison**: 2 min
- **Part 5: Next Steps & Architecture**: 2 min
- **Q&A**: 2-3 min

---

## 📋 Pre-Demo Checklist

### Before the Interview
- [ ] Virtuoso Docker container running (`docker-compose ps`)
- [ ] Djehuty environment activated (`source djehuty-env/bin/activate`)
- [ ] Faculties inserted into triple store (`python prototype/insert_sample_faculties.py`)
- [ ] Tests passing (`python prototype/test_faculty_statistics.py`)
- [ ] Browser tabs prepared:
  - Terminal 1: Ready for Python scripts
  - Terminal 2: Ready for SPARQL queries
  - Editor: `statistics_faculty.sparql` open
  - Editor: `database.py` with `faculty_statistics()` visible
- [ ] Backup: Screenshots ready if live demo fails

### Environment Check (30 seconds before demo)
```bash
# Quick health check
cd ~/Projects/assigment-djehuty
docker-compose ps  # Should show sparql_1 running
source djehuty-env/bin/activate
python -c "from djehuty.web.database import SparqlInterface; print('✓ Ready')"
```

---

## 🎬 Demo Script

### SETUP (1 minute)

**ACTION**: Show project structure

```bash
cd ~/Projects/assigment-djehuty
tree -L 2 prototype/
```

**SAY**:
> "I've built a 4-6 day working prototype instead of a 2.5-week full implementation. Let me show you what's working right now."

**SHOW** (quickly point to):
- `prototype/sample_faculties.ttl` - "RDF data model"
- `prototype/insert_sample_faculties.py` - "Data insertion"
- `prototype/test_faculty_statistics.py` - "Test suite"
- `prototype/PROGRESS.md` - "Detailed progress tracking"

---

### PART 1: Problem & Discovery (2 minutes)

**ACTION**: Show the assignment requirement

**SAY**:
> "The assignment asks for faculty-level statistics. When I analyzed your codebase, I discovered something interesting..."

**SHOW**: Open `docs/analysis/PARTIAL_IMPLEMENTATION_ANALYSIS.md` (or just explain)

**KEY POINTS**:
1. **Discovery**: "Institution-level grouping already exists via `djht:group_id`"
2. **Insight**: "I can extend the same pattern to faculties - finer granularity"
3. **Design Decision**: "Extension, not replacement - backwards compatible"

**VISUAL**: Draw quick diagram (whiteboard or paper):
```
Institution (coarse)     Faculty (fine)
├── TU Delft (28586)     ├── EEMCS (285860001)
├── TU Eindhoven         ├── AE (285860002)
├── Utrecht              └── AS (285860003)
└── Twente
   (4 groups)               (47 groups)
```

**SAY**:
> "This hierarchical approach proves the extension pattern works at both levels. Let me show you the working code."

---

### PART 2: Live Demo - RDF Model (3 minutes)

#### Step 2.1: Show Sample Faculty Data

**ACTION**: Display the Turtle file

```bash
cat prototype/sample_faculties.ttl
```

**SAY**:
> "Here's the RDF schema extension. I created 3 sample faculties following your existing `djht:InstitutionGroup` pattern."

**POINT OUT** (in the Turtle output):
- `rdf:type djht:Faculty` - "New entity type"
- `djht:group_id` - "Same predicate as institutions - proves extension"
- `djht:institution_id` - "Links faculty to parent institution"

#### Step 2.2: Verify Data in Triple Store

**ACTION**: Query live SPARQL endpoint

```bash
# Query all faculties
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

**EXPECTED OUTPUT**:
```json
[
  {
    "faculty_name": {"value": "Faculty of EEMCS"},
    "group_id": {"value": "285860001"}
  },
  {
    "faculty_name": {"value": "Faculty of Aerospace Engineering"},
    "group_id": {"value": "285860002"}
  },
  ...
]
```

**SAY**:
> "This proves the RDF data is actually in your Virtuoso triple store. Now let me show you the Python backend."

---

### PART 3: Live Demo - Backend Methods (3 minutes)

#### Step 3.1: Show SPARQL Template

**ACTION**: Open the template in editor

```bash
cat djehuty/src/djehuty/web/resources/sparql_templates/statistics_faculty.sparql
```

**SAY**:
> "Here's the SPARQL query template. It follows your existing Jinja2 template pattern."

**POINT OUT**:
- `{% extends "prefixes.sparql" %}` - "Reuses existing base template"
- `GROUP BY ?faculty_id` - "Aggregates dataset counts"
- `OPTIONAL { ... }` - "Handles faculties with 0 datasets gracefully"

#### Step 3.2: Show Python Method

**ACTION**: Open `database.py` in editor, navigate to `faculty_statistics()`

```bash
# Or just show it in your editor
grep -A 30 "def faculty_statistics" djehuty/src/djehuty/web/database.py
```

**SAY**:
> "Here's the Python method. Notice how it mirrors your existing `dataset_statistics()` pattern."

**POINT OUT**:
- `rdf.sparql_filter()` - "Same filtering helpers"
- `self.__query_from_template()` - "Same template mechanism"
- `self.__run_query()` - "Same caching infrastructure"

**SAY**:
> "I'm not reinventing the wheel - I'm proving I understand how your system works."

#### Step 3.3: Run Live Test

**ACTION**: Execute the test suite

```bash
cd ~/Projects/assigment-djehuty
python prototype/test_faculty_statistics.py
```

**EXPECTED OUTPUT**:
```
======================================================================
TESTING: faculty_statistics() Backend Method
======================================================================

✅ Connected to SPARQL endpoint

======================================================================
TEST 1: Get all faculty statistics
======================================================================

📊 Found 3 faculties:

Faculty: AE
  ID: 285860002
  Full Name: Faculty of Aerospace Engineering
  Institution ID: 28586
  Dataset Count: 0

[... more output ...]

======================================================================
✅ ALL TESTS PASSED!
======================================================================
```

**SAY**:
> "All 5 tests passing. Let me show you the actual method call in Python."

#### Step 3.4: Interactive Python Demo

**ACTION**: Run Python interactively

```bash
cd ~/Projects/assigment-djehuty
python
```

```python
# In Python REPL
import sys
sys.path.insert(0, 'djehuty/src')

from djehuty.web.config import config
from djehuty.web.database import SparqlInterface
import json

# Initialize
db = SparqlInterface()
db.cache.storage = 'data/cache'
db.setup_sparql_endpoint()

# Call the method
results = db.faculty_statistics()

# Pretty print
print(json.dumps(results, indent=2, default=str))
```

**EXPECTED OUTPUT**:
```json
[
  {
    "faculty_id": 285860001,
    "faculty_name": "Faculty of Electrical Engineering, Mathematics and Computer Science",
    "faculty_short_name": "EEMCS",
    "institution_id": 28586,
    "dataset_count": 0
  },
  ...
]
```

**SAY**:
> "This is the actual method output - API-ready JSON. Now let me show you the two-level hierarchy."

---

### PART 4: Two-Level Comparison (2 minutes)

#### Step 4.1: Institution Statistics

**ACTION**: Call institution_statistics()

```python
# Still in Python REPL
inst_results = db.institution_statistics()
print(f"Institution-level: {len(inst_results)} groups")
```

**SAY**:
> "This is the existing institution-level aggregation - coarse granularity."

#### Step 4.2: Faculty Statistics

**ACTION**: Call faculty_statistics()

```python
# Filter by TU Delft
faculty_results = db.faculty_statistics(institution_id=28586)
print(f"Faculty-level (TU Delft only): {len(faculty_results)} groups")

# Show the breakdown
for f in faculty_results:
    print(f"  {f['faculty_short_name']}: {f['dataset_count']} datasets")
```

**SAY**:
> "Same institution, but now we can break it down by faculty - fine granularity. This is the extension pattern in action."

#### Step 4.3: Show Hierarchy

**ACTION**: Demonstrate filtering

```python
# All faculties for a specific institution
print("\nHierarchy: Institution → Faculty")
print(f"TU Delft (28586) →")
for f in faculty_results:
    print(f"  ├── {f['faculty_short_name']} ({f['faculty_id']})")
```

**EXPECTED OUTPUT**:
```
Hierarchy: Institution → Faculty
TU Delft (28586) →
  ├── EEMCS (285860001)
  ├── AE (285860002)
  └── AS (285860003)
```

**SAY**:
> "This proves the hierarchical relationship. One institution contains multiple faculties. Same pattern can extend to departments, labs, research groups in the future."

---

### PART 5: Next Steps & Architecture (2 minutes)

#### Step 5.1: Show Prototype Plan

**ACTION**: Quick walkthrough of remaining work

```bash
cat prototype/PROGRESS.md | head -50
```

**SAY**:
> "Here's where we are in the prototype timeline:"

**SHOW** (on screen or paper):
```
✅ Phase 1 (2/2.5 days): RDF Model + Backend - COMPLETE
⏳ Phase 1 (0.5 days): API endpoints - Next
✅ Phase 2A (1 day): Migration analysis - COMPLETE
⚠️  Phase 2B (1 day): Migration logic - DEMONSTRATED (writes blocked)
⏳ Phase 3 (2 days): Dashboard visualization
```

**SAY**:
> "I've also analyzed real data migration feasibility. Found 44% of datasets have extractable faculty info with 100% accuracy in pattern matching."

#### Step 5.2: Architecture Benefits

**ACTION**: Explain design advantages

**SAY** (with visual/whiteboard):
> "This approach has three key benefits:
>
> 1. **Low Risk**: Extends existing `group_id` pattern, doesn't replace it
> 2. **Backwards Compatible**: Institutions still work exactly as before
> 3. **Scalable**: Same pattern extends to departments, labs, etc.
>
> I also analyzed migration from real data - proved extraction works on 9 datasets with 44% coverage.
>
> For the full implementation, I'd add:
> - API endpoints (half day)
> - Migration execution with write permissions (2 days)
> - Dashboard with both levels (2 days)
> - Testing with full production data (1 day)
>
> But for the interview, I focused on proving the concept works."

#### Step 5.3: Show Documentation

**ACTION**: Quick tour of docs

```bash
ls -la docs/analysis/
```

**SAY**:
> "I've documented everything:
> - `PROTOTYPE_PLAN.md`: Complete 7-day strategy
> - `PARTIAL_IMPLEMENTATION_ANALYSIS.md`: What I discovered in your code
> - `PROGRESS.md`: What's done, what's next
>
> All committed to git with detailed commit messages."

---

### Q&A PREPARATION (for questions)

#### Q: "Why a prototype instead of full implementation?"

**ANSWER**:
> "I assessed the scope and realized 2.5 weeks was too much for an interview presentation. A prototype proves three things faster:
> 1. **Technical competence**: Working SPARQL + Python code
> 2. **System understanding**: I analyzed your existing patterns
> 3. **Practical approach**: Demo-able results in 4-6 days
>
> The full implementation is planned in `PROTOTYPE_PLAN.md` - I just prioritized what's most valuable to show you."

#### Q: "How would you handle real data migration?"

**ANSWER**:
> "I've actually analyzed this with your real data. I built `analyze_faculty_migration.py` that:
> 1. Scanned 9 real datasets from your Virtuoso triple store
> 2. Extracted faculty from the 'organizations' metadata field
> 3. Used pattern matching (8 TU Delft faculty patterns) with 100% accuracy
> 4. Found 44% of datasets (4/9) have extractable faculty information
>
> I also created migration logic in `migrate_sample_faculty.py` but couldn't execute writes due to Virtuoso permissions.
> What I proved: Faculty extraction works. Remaining work is configuration + execution.
>
> The analysis results are in `prototype/analysis_results.json` with detailed statistics."

#### Q: "What about performance with thousands of datasets?"

**ANSWER**:
> "Good question. The current implementation uses:
> 1. **SPARQL GROUP BY**: Database-level aggregation (fast)
> 2. **Caching**: Results cached via `__run_query()` mechanism
> 3. **Pagination**: `limit`/`offset` parameters prevent large result sets
> 4. **Indexes**: Virtuoso already indexes `djht:group_id` for institutions
>
> For thousands of datasets, I'd add:
> - Pre-aggregated statistics table (materialized view pattern)
> - Background job to refresh statistics daily
> - Cache warming on deployment
>
> But the SPARQL GROUP BY approach is surprisingly fast for moderate scale."

#### Q: "How do you handle datasets with multiple authors from different faculties?"

**ANSWER**:
> "That's Phase 2. Currently, I'm tracking faculty at the **depositor** level (via Account). For multi-faculty datasets, I'd:
> 1. Add `djht:faculty_id` to Author entity (not just Account)
> 2. Use RDF lists to support multiple faculties per dataset
> 3. Statistics would count contributions (not just deposits)
> 4. Distinguish between 'depositing faculty' and 'authoring faculties'
>
> I've documented this in `docs/future-work/ARCHITECTURE_CORRECTION_AUTHORS.md`. For the prototype, I'm staying focused on depositor faculty to keep scope manageable."

#### Q: "Show me the code for X"

**ANSWER**:
> "Absolutely. Let me pull that up..."

**HAVE READY**:
- `faculty_statistics()` method (`database.py` line 607)
- SPARQL template (`statistics_faculty.sparql`)
- Test suite (`test_faculty_statistics.py`)
- RDF sample data (`sample_faculties.ttl`)

#### Q: "What would you do differently in production?"

**ANSWER**:
> "Several things:
> 1. **Error handling**: Add try-catch blocks with logging
> 2. **Validation**: Validate faculty_id exists before linking
> 3. **Transactions**: Wrap batch updates in transactions
> 4. **Monitoring**: Add metrics for query performance
> 5. **API auth**: Secure the endpoints (currently open)
> 6. **Rate limiting**: Prevent abuse of statistics endpoints
> 7. **OpenAPI spec**: Document the API with Swagger
>
> But for a prototype proving the concept, I focused on core functionality first."

---

## 🎯 Key Messages to Emphasize

### Message 1: System Understanding
> "I analyzed your existing code and found the `djht:group_id` pattern. Rather than creating something new, I extended what already works."

### Message 2: Practical Approach
> "I built a working prototype in 2 days instead of spending 2.5 weeks on full implementation. You can see it running right now."

### Message 3: Scalable Design
> "The same extension pattern works at multiple granularities: institutions (4) → faculties (47) → departments → labs. It's hierarchical by design."

---

## 📊 Demo Backup (If Live Demo Fails)

### Screenshots to Have Ready

1. **Triple Store Query Result**
   - Screenshot of SPARQL query returning faculties
   - File: `screenshots/sparql_faculties.png`

2. **Test Suite Passing**
   - Screenshot of all 5 tests passing
   - File: `screenshots/tests_passing.png`

3. **Python REPL Output**
   - Screenshot of `faculty_statistics()` JSON output
   - File: `screenshots/python_output.png`

4. **Code Walkthrough**
   - Screenshot of `faculty_statistics()` method
   - Screenshot of SPARQL template

### Backup Demo Flow
> "Let me show you screenshots of the working demo I prepared..."

**SHOW**:
1. Tests passing → "Here's proof the code works"
2. SPARQL output → "Here's the actual data in your triple store"
3. Python method → "Here's the implementation"
4. JSON output → "Here's the API-ready result"

---

## ✅ Post-Demo Checklist

### After Successful Demo
- [ ] Thank interviewers
- [ ] Offer to share git repository
- [ ] Mention documentation is comprehensive
- [ ] Be ready for follow-up questions
- [ ] Have `PROTOTYPE_PLAN.md` open for detailed questions

### If Asked for Repository
> "Yes, it's all committed to git with detailed messages. I can share:
> - GitHub repository (if public)
> - Or email you a zip with full git history
> - Documentation is in `docs/` directory
> - Working code in `prototype/` and `djehuty/src/`"

---

## 🎤 One-Liners for Impact

Use these throughout the demo for emphasis:

- **On approach**: "Extension, not replacement"
- **On timeline**: "Working prototype in 2 days, not 2.5 weeks"
- **On design**: "Same pattern, finer granularity"
- **On testing**: "All tests passing, production-ready patterns"
- **On scalability**: "Hierarchical by design - institutions to faculties to departments"
- **On code quality**: "I'm not reinventing the wheel - I'm following your existing patterns"

---

## 📋 Materials Checklist

### Have These Ready
- [ ] Laptop with demo environment
- [ ] Backup laptop (if available)
- [ ] Whiteboard marker (for diagrams)
- [ ] Paper for backup diagrams
- [ ] USB drive with screenshots (backup)
- [ ] Printed `PROTOTYPE_PLAN.md` (backup reference)

### Don't Forget
- [ ] Power adapter
- [ ] Mouse (if preferred)
- [ ] Water bottle (for talking)
- [ ] Confidence! You've built working code.

---

**Remember**: You have WORKING CODE that runs in THEIR SYSTEM (Djehuty + Virtuoso). This is rare in interview presentations. Use it!

**Last Updated**: December 10, 2024  
**Estimated Demo Time**: 10-15 minutes  
**Confidence Level**: HIGH (all code tested and working)
