# Phase 1 Focus - Prototype for Interview Presentation

**For the remainder of this discussion, we are focused EXCLUSIVELY on Phase 1.**

**⚠️ UPDATED December 9, 2024:** Approach changed from **full implementation (2.5 weeks)** to **working prototype (4-6 days)** for interview presentation context. See [PROTOTYPE_PLAN.md](./PROTOTYPE_PLAN.md) for complete strategy.

---

## 📋 Phase 1 Scope (Interview Presentation)

**Goal:** Create working prototype demonstrating faculty-level statistics for 15-minute interview presentation

**Approach:** Prototype + migration analysis + visualization (proves concept with concrete evidence)

**Timeline:** **4-6 days** (reduced from 2.5 weeks full implementation)

**Context:** Interview presentation (10-15 minutes), not production deployment. Working demo more valuable than theoretical design.

**Key Discovery:** Institution filtering infrastructure (`dataset_statistics(group_ids=[...])`) already exists, enabling rapid extension prototype.

**Deliverables:**
1. ✅ Working faculty statistics backend (core functionality)
2. ✅ Sample data migration (20 datasets, proves feasibility)
3. ✅ Migration analysis script (scans all datasets, provides concrete numbers)
4. ✅ Visualization dashboard (4 charts demonstrating end-to-end solution)
5. ✅ 15-minute presentation with live demo

---

## 📂 Phase 1 Documentation

**Prototype Plan** (PRIMARY - Current Approach):
```
docs/analysis/
└── PROTOTYPE_PLAN.md              ← Complete 4-6 day prototype strategy (START HERE)
```

**Original Full Implementation Plan** (Reference - 2.5 weeks):
```
docs/assignment/
├── README.md                      ← Phase 1 overview and guide
├── SOLUTION_ARCHITECTURE.md       ← Complete 61-page specification
├── IMPLEMENTATION_ROADMAP.md      ← 2.5-week schedule
├── ROADMAP_EXECUTIVE_SUMMARY.md   ← Executive summary (50 hours)
├── ARCHITECTURE_SUMMARY.md        ← Quick reference
└── archive/                       ← Original v1.0 documents (pre-discovery, 5-week timeline)
```

**Discovery Documentation**:
```
docs/analysis/
├── PARTIAL_IMPLEMENTATION_INDEX.md      ← Quick navigation
├── PARTIAL_IMPLEMENTATION_ANALYSIS.md   ← Technical deep dive (30 pages)
├── PHASE1_IMPACT_SUMMARY.md             ← Executive summary (12 pages)
└── PHASE1_FOCUS.md                      ← This document
```

**Why Prototype Instead of Full Implementation:**
- Interview context: 15-minute presentation benefits more from working demo than full implementation
- Time efficiency: 4-6 days vs 2.5 weeks
- Concrete evidence: Live demo + migration analysis provides definitive answers to "how confident are you?"
- Risk mitigation: Validates approach before committing to full development
- More impressive: Working code is more compelling than theoretical design for technical interview

See [PROTOTYPE_PLAN.md](./PROTOTYPE_PLAN.md) for complete strategy, timeline, and implementation details.

**Phase 2 and future work are OUT OF SCOPE for current discussion.**

---

## 🎯 What We're Building (Phase 1 Only)

### Data Model
- **Add:** Faculty entity (8 TU Delft faculties)
- **Extend:** Account entity with `faculty_id` predicate
- **Keep:** Organizations field unchanged (display only)

### Features
- Statistics: "Datasets deposited by each faculty"
- Faculty selection during account registration
- Auto-fill faculty on dataset submission (from depositor's account)
- Admin UI for updating account faculty

### API Endpoints (6 total)
1. `GET /v2/faculties` - List all faculties
2. `GET /v2/faculties/{id}` - Get faculty details
3. `GET /v2/statistics/faculties` - Faculty statistics
4. `GET /v2/statistics/faculties/{id}/datasets` - Datasets by faculty
5. `PATCH /v2/accounts/{uuid}` - Update account faculty (extended)
6. `POST /v2/datasets` - Create dataset (extended with auto-fill)

### Migration
- ~200 depositor accounts
- Manual review of Organizations field
- CSV-based workflow
- Target: ≥90% coverage

---

## ❌ What We're NOT Building (Phase 1)

- ❌ Faculty tracking for unregistered authors (co-authors without accounts)
- ❌ Pattern matching / automated Organizations parsing
- ❌ Confidence scoring
- ❌ Author-level statistics
- ❌ Multi-valued statistics (datasets counted for multiple faculties)
- ❌ Collaboration network visualization
- ❌ ORCID integration

**All of the above are Phase 2 - deferred for future consideration.**

---

## 📖 Key Phase 1 Documents

### For Implementation
**Primary:** `docs/assignment/SOLUTION_ARCHITECTURE.md`
- Section 1: Executive Summary
- Section 4: Data Model Design
- Section 5: System Components
- Section 6: API Design
- Section 7: User Interface Design
- Section 8: Migration Strategy
- Section 9: Implementation Timeline (5 weeks)

**Quick Reference:** `docs/assignment/ARCHITECTURE_SUMMARY.md`
- Architecture overview
- Component checklist
- API endpoints summary
- Faculty codes table

### For Presentation
**Stakeholders:** `docs/assignment/PRESENTATION_OUTLINE.md`
- 14 slides with speaker notes
- Problem statement
- Solution overview
- Timeline and benefits

### For Discovery Understanding
**Technical Deep Dive:** `docs/analysis/PARTIAL_IMPLEMENTATION_ANALYSIS.md` (30 pages)
- What exists today (infrastructure discovered)
- What is missing (4-6 hours of work)
- Impact analysis (50% timeline reduction)
- Strategic recommendations

**Executive Summary:** `docs/analysis/PHASE1_IMPACT_SUMMARY.md` (12 pages)
- Discovery timeline
- Before/after comparison
- Component-by-component breakdown
- Risk assessment

**Quick Start:** `docs/analysis/PARTIAL_IMPLEMENTATION_INDEX.md` (6 pages)
- 30-second summary
- Document guide by role
- Quick decision guide

---

## 🔍 Key Discovery (December 9, 2024)

**Found during code analysis:**

✅ **What EXISTS:**
- `dataset_statistics(group_ids=[...])` - Institution filtering already works
- `djht:group_id` predicate - Institution tracking in RDF schema
- SPARQL templates with filtering - Dynamic query support
- Production code, tested, working

❌ **What's MISSING:**
- Aggregation layer (sum results instead of returning list)
- Estimated: 4-6 hours to add

**Impact:**
- Timeline: ~~5 weeks~~ → **2.5 weeks** (50% reduction)
- Effort: ~~100 hours~~ → **50 hours** (50% reduction)
- Approach: ~~Build from scratch~~ → **Leverage existing + extend**
- Risk: ~~Medium~~ → **Low** (proven production code)

**Why this matters:**
- Shows thorough code analysis skills
- Demonstrates pragmatic engineering (leverage vs. rebuild)
- Reduces risk (using tested code)
- Faster time-to-value

---

## 🚀 Next Steps (Phase 1)

**Updated Timeline: 2.5 weeks** (revised after discovering partial implementation)

**Phase 0: Discovery & Setup (0.5 days)**
- Discovered: Institution filtering infrastructure exists
- Decision: Leverage `dataset_statistics(group_ids=[...])` instead of rebuilding
- Plan: Wrap existing method for faculty aggregation

**Week 1: Foundation (5 days)**
1. Configure faculties in `djehuty.xml`
2. Extend RDF schema with `faculty_id` on Account
3. Create faculty validation and management functions
4. Write unit tests
5. **Leverage existing:** Institution group infrastructure

**Week 2: Migration & API (5 days)**
1. Export depositor accounts
2. Manual review of Organizations field
3. Import faculty assignments (validate coverage ≥90%)
4. Implement 6 endpoints (leverage existing patterns)
5. Integration tests

**Week 2.5: UI & Deployment (2.5 days)**
1. Faculty dropdown in registration
2. Auto-fill on dataset submission
3. **Statistics dashboard (wrap existing `dataset_statistics`)**
4. End-to-end testing
5. Production deployment

**Key Change:** Institution statistics infrastructure already works, so we focus on faculty-specific extensions rather than building from scratch.

---

## 💬 Discussion Focus

For the rest of our conversation, please:

✅ **DO ask about:**
- Phase 1 implementation details
- Depositor faculty tracking
- Account entity changes
- Migration strategy for ~200 accounts
- Phase 1 API endpoints
- Phase 1 UI components
- Phase 1 statistics queries
- **2.5-week timeline** (updated after discovery)
- **Leveraging existing infrastructure** (discovered partial implementation)
- Testing Phase 1
- Deploying Phase 1

❌ **DON'T ask about:**
- Author-level faculty tracking (Phase 2)
- Unregistered authors (Phase 2)
- Pattern matching (Phase 2)
- Confidence scoring (Phase 2)
- Multi-valued statistics (Phase 2)
- Collaboration networks (Phase 2)
- 10-week timeline (Phase 2)

---

## 📊 Phase 1 Requirements Coverage

From your original 15 questions, Phase 1 addresses:

1. ✅ Stats per institute - Already exists
2. ✅ **Stats per faculty - CORE FEATURE**
3. ⚠️ Cross-referencing - Manual review only
4. ⚠️ Parse free-text - Manual only
5. ❌ Associate to authors - No (depositors only)
6. ✅ Missing data stats - Coverage metrics
7. ✅ Handle Organizations - Hybrid approach
8. ✅ Contributors per institute - Already exists
9. ❌ First author stats - Out of scope
10. ✅ Extensible stats - Yes (SPARQL)
11. ✅ Modular schema - Yes (RDF)
12. ❌ Unregistered authors - No (Phase 2)
13. ✅ DB improvements - Faculty entity
14. ⚠️ Auto-population - Limited (depositor only)
15. ✅ Graceful failures - Yes

**Phase 1 Coverage: 9 fully addressed, 3 partially, 3 deferred to Phase 2**

---

## 🎯 Success Criteria (Phase 1)

| Metric | Target |
|--------|--------|
| Migration coverage | ≥90% depositor accounts |
| Migration accuracy | 100% (manual verification) |
| API response time | <100ms |
| Statistics query time | <150ms |
| Dashboard load time | <2 seconds |
| User adoption | ≥80% within 3 months |

---

*All subsequent discussion will focus exclusively on Phase 1 implementation.*
