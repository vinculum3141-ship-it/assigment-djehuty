# Phase 2: Author-Level Faculty Statistics (Future Work)

This folder contains the **complete specification for Phase 2** - extending faculty tracking to **all authors** (registered + unregistered co-authors), not just depositors.

⚠️ **Prerequisites:** Phase 1 must be completed first.

---

## 📋 What is Phase 2?

**Scope:** Add faculty tracking for **ALL authors** on datasets (registered + unregistered)

**Approach:**
- Add `faculty_id` to **Author entity** (all ~5,000 contributors)
- Add confidence scoring (`faculty_confidence`, `faculty_source`, `faculty_assigned_date`)
- Statistics: "Datasets **authored** by each faculty"
- 1 dataset = 1-N faculties (multi-valued, intentional double-counting)
- Migration: ~950 TU Delft authors
  - 150 from accounts (100% accuracy)
  - 600 auto-detected from Organizations (≥80% accuracy)
  - 200 manual review (100% accuracy after human verification)

**Why Phase 2?**
- Answer research questions: "Which datasets have our faculty researchers **authored**?"
- Track multi-faculty collaborations
- More accurate research metrics (bibliometric standard)
- Enable future enhancements (department-level, research groups)

**Trade-off:** 2x complexity (10 weeks vs 5 weeks, 2 developers vs 1, lower data quality 80% vs 100%)

---

## 🚨 Critical Decision Point

**Should you implement Phase 2?**

Read `PHASE2_QUICK_REFERENCE.md` first - it provides:
- Decision framework (arguments for/against)
- Phase 1 vs Phase 2 comparison table
- Risk assessment
- Pilot option (test with one faculty first)

**Then read `ARCHITECTURE_CORRECTION_AUTHORS.md`** to understand:
- Why the original architecture missed this
- Author vs Account distinction
- Depositor-only vs Author-inclusive trade-offs

---

## 📄 Documents (Reading Order)

### 🎯 START HERE

#### 1. ARCHITECTURE_CORRECTION_AUTHORS.md (15 pages, ~30 min read)

**Purpose:** Explains the critical insight that triggered Phase 2.

**Key Finding:**
- `djht:Author` ≠ `djht:Account`
- Most authors (like "Hebly, Scott J.") are **unregistered** - just names, no accounts
- Phase 1 tracks faculty for depositors only (~200 accounts)
- Phase 2 tracks faculty for all authors (~5,000 authors)

**Contents:**
- The critical gap discovered
- Depositor-Only Interpretation (Phase 1)
- Author-Inclusive Interpretation (Phase 2)
- Technical comparison
- Recommended approach
- Extensibility considerations

**When to read:** Before making any Phase 2 decisions. This document explains **why Phase 2 exists**.

---

#### 2. PHASE2_QUICK_REFERENCE.md (5 pages, ~15 min read)

**Purpose:** Executive summary and decision framework.

**Contents:**
- What is Phase 2? (one-page summary)
- Phase 1 vs Phase 2 comparison table
- Scope (in/out)
- Timeline & resources (10 weeks, 2 developers)
- Success metrics
- Document navigation
- Key files
- **Decision framework:** Arguments for/against Phase 2
- Quick start commands

**When to read:** After ARCHITECTURE_CORRECTION_AUTHORS.md, to decide if Phase 2 is worth it.

---

### 📚 Phase 2 Specification (If Approved)

#### 3. PHASE2_OVERVIEW.md (8 pages, ~20 min read)

**Purpose:** Problem statement, scope, and high-level architecture.

**Contents:**
- Problem: What Phase 1 can't do
- Real-world example (multi-faculty collaboration)
- Phase 1 vs Phase 2 differences
- Phase 2 scope (in/out of scope)
- High-level architecture (3 layers)
- Timeline overview (10 weeks)
- Resource requirements
- Key risks

**When to read:** Start of Phase 2 planning.

---

#### 4. PHASE2_DATA_MODEL.md (18 pages, ~45 min read)

**Purpose:** RDF schema extensions and confidence scoring model.

**Contents:**
- 4 new predicates on Author entity:
  - `djht:faculty_id` (integer, optional)
  - `djht:faculty_confidence` (float 0.0-1.0)
  - `djht:faculty_source` ("account", "organizations_auto", "manual_review")
  - `djht:faculty_assigned_date` (dateTime)
- Complete Author entity schema
- Entity relationships (registered, unregistered, external authors)
- Faculty assignment semantics
- Confidence scoring model (pattern matching algorithm)
- FACULTY_PATTERNS dictionary (8 faculties with regex patterns)
- Python code examples
- SPARQL query templates
- Migration mappings
- 7 validation rules

**When to read:** Week 1-2 of implementation (Foundation phase).

---

#### 5. PHASE2_MIGRATION.md (22 pages, ~60 min read)

**Purpose:** Complete migration strategy for ~1,000 authors.

**Contents:**
- Migration overview (4 phases)
- Author segmentation (150 registered, 800 unregistered, 300 external)
- **3 complete Python scripts:**
  1. `export_registered_authors.py` - Copy from accounts
  2. `export_unregistered_authors.py` - Get Organizations texts
  3. `detect_author_faculty.py` - Pattern matching with confidence
- FACULTY_PATTERNS dictionary (regex patterns and weights)
- `import_author_faculty.py` - Bulk import
- Manual review workflow (CSV template)
- Edge cases (multi-faculty authors, joint appointments)
- 5 validation queries (≥85% coverage target)
- Statistical validation
- Rollback plan

**When to read:** Week 3-5 of implementation (Migration phases 2A/2B/2C).

---

#### 6. PHASE2_STATISTICS.md (16 pages, ~45 min read)

**Purpose:** Multi-valued statistics queries and collaboration metrics.

**Contents:**
- Multi-valued semantics (intentional double-counting)
- 3 statistical views (Deposited, Authored, Collaborations)
- **5 SPARQL query templates:**
  1. `statistics_faculty_authored.sparql` - Dataset/author counts by faculty
  2. `statistics_faculty_collaborations.sparql` - Collaboration matrix
  3. `faculty_research_profile.sparql` - Detailed faculty profile
  4. `datasets_by_faculty_authored.sparql` - Paginated dataset list
  5. `author_contributions_by_faculty.sparql` - Top authors by faculty
- Caching strategy (invalidation rules, TTL)
- Collaboration metrics (network analysis)
- Performance optimization (indexing, materialized views)
- Phase 1 vs Phase 2 comparison query

**When to read:** Week 6-7 of implementation (API & Statistics phase).

---

#### 7. PHASE2_API_UI.md (20 pages, ~50 min read)

**Purpose:** API endpoints and UI components.

**Contents:**
- **6 API endpoints:**
  1. `GET /v2/authors/{uuid}/faculty` - Get author faculty
  2. `PATCH /v2/authors/{uuid}/faculty` - Update author faculty
  3. `GET /v2/statistics/faculties/authored` - Faculty-authored stats
  4. `GET /v2/statistics/faculties/{id}/datasets` - Datasets by faculty
  5. `GET /v2/statistics/collaborations` - Collaboration network
  6. `GET /v2/authors?faculty_id={id}` - Authors by faculty
- Full request/response JSON examples
- Python route handler implementations
- **3 UI components:**
  1. Author faculty badge (HTML/CSS with confidence indicator)
  2. Multi-faculty collaboration dashboard (D3.js force-directed network)
  3. Phase 1 vs Phase 2 comparison charts (Chart.js)
- JavaScript implementations
- Workflow integration (dataset submission)
- Error handling

**When to read:** Week 6-9 of implementation (API & UI phases).

---

#### 8. PHASE2_IMPLEMENTATION.md (14 pages, ~35 min read)

**Purpose:** 10-week timeline, testing strategy, and deployment plan.

**Contents:**
- **10-week timeline breakdown:**
  - Week 1-2: Foundation (RDF schema, FacultyManager, tests)
  - Week 3-5: Migration (2A registered, 2B unregistered, 2C manual review)
  - Week 6-7: API & Statistics
  - Week 8-9: UI Development
  - Week 10: Testing & Deployment
- Detailed task breakdown (owner, hours, deliverables)
- Testing strategy (unit, integration, performance, UAT)
- Deployment plan (Saturday 2AM-6AM, 12-step procedure)
- Success criteria (12 metrics)
- 6 risks with mitigation
- Post-deployment monitoring
- Documentation updates
- Training sessions

**When to read:** Project planning phase and throughout implementation.

---

## 🏗️ Phase 2 Architecture Overview

### New Components

```
Phase 1 Foundation (Account.faculty_id)
    ↓
Author.faculty_id (NEW)
Author.faculty_confidence (NEW)
Author.faculty_source (NEW)
Author.faculty_assigned_date (NEW)
    ↓
Migration Engine
    ├── RegisteredAuthorMigrator
    ├── UnregisteredAuthorDetector (pattern matching)
    └── ManualReviewWorkflow
    ↓
Enhanced FacultyManager
    ├── Confidence scoring
    ├── Source tracking
    └── Validation
    ↓
6 New API Endpoints
    ↓
3 New UI Components
    ├── Faculty badge on author profiles
    ├── Collaboration network (D3.js)
    └── Phase 1 vs 2 comparison charts
    ↓
Multi-Valued Statistics
```

### Data Flow

```
Dataset with 3 authors:
├── Author 1: Dr. Smith (registered, Aerospace, confidence 1.0)
├── Author 2: Dr. Johnson (registered, EEMCS, confidence 1.0)
└── Author 3: Hebly, Scott J. (unregistered, Aerospace, confidence 0.85)

Faculty Statistics:
├── Aerospace: +1 dataset (2 authors)
└── EEMCS: +1 dataset (1 author)

Note: Same dataset counted twice (multi-valued semantics)
```

---

## 📊 Timeline & Resources

| Aspect | Phase 1 | Phase 2 |
|--------|---------|---------|
| **Duration** | 5 weeks | 10 weeks |
| **Team** | 1 developer | 2 developers + 2 reviewers |
| **Effort** | ~100 person-hours | ~200 person-hours |
| **Entities** | Account (~200) | Author (~5,000) |
| **Migration** | Manual entry | Hybrid (auto + manual) |
| **Accuracy** | 100% | 80-90% |
| **Statistics** | Deposited (single-valued) | Authored (multi-valued) |

---

## ✅ Success Metrics

| Metric | Target | Phase 1 Comparison |
|--------|--------|-------------------|
| Author coverage | ≥85% TU Delft authors | N/A |
| Migration accuracy | ≥80% | 100% |
| High confidence ratio | ≥70% (confidence ≥0.8) | 100% |
| API response time | <150ms | <100ms |
| Statistics query time | <200ms | <100ms |
| Multi-faculty collaborations | ≥100 detected | 0 |
| Dashboard load time | <3 seconds | <2 seconds |

---

## 🎯 Quick Start (If Approved)

### Week 1 - Day 1

```bash
# 1. Review complete Phase 2 specification
cd docs/future-work

# 2. Read decision documents
cat ARCHITECTURE_CORRECTION_AUTHORS.md  # 30 min
cat PHASE2_QUICK_REFERENCE.md            # 15 min
cat PHASE2_OVERVIEW.md                   # 20 min

# 3. If approved, read data model
cat PHASE2_DATA_MODEL.md                 # 45 min

# 4. Set up development branch
cd ../../djehuty
git checkout -b phase2-author-faculty

# 5. Extend RDF schema
vim src/djehuty/rdf/schema.ttl
# Add: faculty_id, faculty_confidence, faculty_source, faculty_assigned_date

# 6. Run unit tests
pytest tests/test_author_faculty.py -v
```

---

## ⚠️ Important Constraints

1. **Phase 1 required:** Account.faculty_id must exist first
2. **TU Delft only:** Author faculty assignment limited to TU Delft institution
3. **Confidence scoring required:** Every auto-assigned faculty needs confidence
4. **Manual review mandatory:** Low confidence (<0.8) requires human verification
5. **Multi-valued semantics:** 1 dataset can count for multiple faculties (intentional)
6. **External authors excluded:** No faculty_id for non-TU Delft authors
7. **Backward compatible:** Existing authors without faculty_id continue to work

---

## 🤔 Common Questions

**Q: Why does Phase 2 take twice as long as Phase 1?**
A: Migrating ~1,000 authors (vs ~200 accounts), pattern matching Organizations field (vs manual entry), manual review workflow, multi-valued statistics complexity, collaboration network visualization.

**Q: What's "multi-valued semantics"?**
A: A dataset with authors from 2 faculties counts for **both** faculties. This is intentional and aligns with bibliometric standards (universities count the same paper multiple times if it has authors from multiple departments).

**Q: How accurate is the pattern matching?**
A: ≥80% target. FACULTY_PATTERNS with regex achieves ~70-80% auto-assignment. Remaining 20% requires manual review. See `PHASE2_MIGRATION.md` Section 4 for details.

**Q: Can we skip manual review?**
A: Not recommended. Pattern matching has edge cases (joint appointments, multi-faculty authors). Manual review ensures ≥95% overall accuracy.

**Q: What if Phase 1 statistics are sufficient?**
A: Then Phase 2 is optional. Monitor Phase 1 usage for 3-6 months, gather stakeholder feedback, then decide.

**Q: Can we do a pilot first?**
A: Yes! Implement Phase 2 for **one faculty** (e.g., Aerospace). Validate accuracy, performance, user satisfaction. Scale if successful. See `PHASE2_QUICK_REFERENCE.md` Section 10.

**Q: What about ORCID integration?**
A: Out of scope for Phase 2. Could be Phase 3. ORCID data quality is variable (many researchers don't maintain it).

---

## 📞 Need Help?

**Specific topics:**
- **Why Phase 2?** `ARCHITECTURE_CORRECTION_AUTHORS.md`
- **Decision framework:** `PHASE2_QUICK_REFERENCE.md`
- **RDF Schema:** `PHASE2_DATA_MODEL.md` Section 2-3
- **Migration:** `PHASE2_MIGRATION.md` Section 3-6
- **Pattern matching:** `PHASE2_MIGRATION.md` Section 4.3
- **Statistics:** `PHASE2_STATISTICS.md` Section 2-5
- **API:** `PHASE2_API_UI.md` Section 1-2
- **UI:** `PHASE2_API_UI.md` Section 3
- **Timeline:** `PHASE2_IMPLEMENTATION.md` Section 2
- **Testing:** `PHASE2_IMPLEMENTATION.md` Section 3
- **Deployment:** `PHASE2_IMPLEMENTATION.md` Section 4

**Cross-reference:**
- `../assignment/SOLUTION_ARCHITECTURE.md` for Phase 1 foundation
- `../current-system/DATASET_ANALYSIS.md` for Organizations field examples

---

## 🔄 Phase 2 Workflow

### Planning (Before Week 1)

1. ✅ **Complete Phase 1** and deploy to production
2. ✅ **Gather feedback** on depositor-only statistics (3-6 months)
3. ✅ **Make decision** using `PHASE2_QUICK_REFERENCE.md`
4. ✅ **Get stakeholder approval** for 10-week project
5. ✅ **Assemble team** (2 developers + 2 manual reviewers)

### Development (Week 1-10)

6. 📖 **Week 1-2:** Read `PHASE2_DATA_MODEL.md`, implement foundation
7. 🔄 **Week 3:** Read `PHASE2_MIGRATION.md`, migrate registered authors (Phase 2A)
8. 🤖 **Week 4-5:** Migrate unregistered authors (Phase 2B + 2C)
9. 🔌 **Week 6-7:** Read `PHASE2_STATISTICS.md` + `PHASE2_API_UI.md`, implement API
10. 🎨 **Week 8-9:** Implement UI (faculty badge, collaboration dashboard)
11. ✅ **Week 10:** Read `PHASE2_IMPLEMENTATION.md` Section 3-4, test and deploy

### Post-Deployment

12. 📊 **Month 1:** Monitor metrics (coverage, accuracy, performance)
13. 🎓 **Training:** Conduct sessions for users and admins
14. 📝 **Review:** Assess success criteria, gather feedback
15. 🚀 **Iterate:** Plan future enhancements (department-level, research groups)

---

## 🎓 Learning Path

**For Decision Makers (1 hour):**
1. `ARCHITECTURE_CORRECTION_AUTHORS.md` (30 min) - Understand the problem
2. `PHASE2_QUICK_REFERENCE.md` (15 min) - Decision framework
3. `PHASE2_OVERVIEW.md` (20 min) - Scope and timeline
4. Make go/no-go decision

**For Developers (5 hours):**
1. `ARCHITECTURE_CORRECTION_AUTHORS.md` (30 min)
2. `PHASE2_OVERVIEW.md` (20 min)
3. `PHASE2_DATA_MODEL.md` (45 min)
4. `PHASE2_MIGRATION.md` (60 min)
5. `PHASE2_STATISTICS.md` (45 min)
6. `PHASE2_API_UI.md` (50 min)
7. `PHASE2_IMPLEMENTATION.md` (35 min)

**For Data Specialists (2 hours):**
1. `ARCHITECTURE_CORRECTION_AUTHORS.md` (30 min)
2. `../current-system/DATASET_ANALYSIS.md` (25 min)
3. `PHASE2_MIGRATION.md` (60 min) - Focus on Sections 4-6

---

*Phase 2 is a significant enhancement that extends faculty tracking to all authors. Start with the decision documents (ARCHITECTURE_CORRECTION_AUTHORS + PHASE2_QUICK_REFERENCE) before committing to the 10-week implementation.*
