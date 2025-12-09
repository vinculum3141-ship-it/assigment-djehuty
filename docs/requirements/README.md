# Requirements Analysis Documents

This folder contains all documents analyzing and interpreting the assignment requirements.

## 📋 Purpose

These documents bridge the gap between the original assignment statement and the technical implementation, answering questions like:
- What exactly is being asked for?
- How do we interpret ambiguous requirements?
- What's in-scope vs. out-of-scope?
- How do assignment requirements map to existing code?

---

## 📄 Documents in This Folder

### 1. **REQUIREMENTS_SUMMARY.md** (5 pages, START HERE)

**Purpose:** Quick answers to common questions from reading the assignment

**Read this if:** You want fast answers to "Is this in scope?" questions

**Contents:**
- Your questions → Our answers (direct mapping)
- What's in Phase 1 vs Phase 2
- What's out of scope
- Quick reference table

**Read time:** 5 minutes

**Example questions answered:**
- ✅ "Do we track faculty for ALL authors or just depositors?" → Phase 1: Depositors only
- ✅ "What about unregistered co-authors?" → Phase 2 (future work)
- ✅ "Do we need department-level tracking?" → Out of scope
- ✅ "What about ORCID integration?" → Phase 3+ (long-term vision)

---

### 2. **REQUIREMENTS_ANALYSIS.md** (20 pages, DETAILED ANALYSIS)

**Purpose:** Deep dive into each requirement with code examples and solutions

**Read this if:** You need detailed technical interpretation of requirements

**Contents:**
- Requirement-by-requirement breakdown
- Code examples showing implementation approach
- SPARQL query examples
- RDF schema implications
- Document cross-references
- Edge cases and clarifications

**Read time:** 30-45 minutes

**Key sections:**
- Functional requirements (faculty tracking, statistics, UI)
- Non-functional requirements (performance, scalability)
- Data quality requirements (accuracy, validation)
- Integration requirements (RDF schema, API)

---

### 3. **ASSIGNMENT_STATEMENT_ANALYSIS.md** (8 pages, INTERPRETATION GUIDE)

**Purpose:** Analyzes potential ambiguity in assignment statement vs. provided code

**Read this if:** You're wondering about institution-level vs faculty-level focus

**Contents:**
- Assignment statement interpretation
- Evidence from provided code
- Two possible interpretations explored
- Recommended approach
- Comparison table showing what exists vs. what's needed

**Key insight:** Assignment emphasizes faculty-level tracking, institution-level is context/foundation

**Read time:** 15 minutes

**Critical question answered:**
> "The assignment mentions institution-level statistics but the provided code already has `dataset_statistics(group_ids=[...])` - is this a mistake?"

**Answer:** No - institution infrastructure provides context. Assignment focus is faculty-level (genuinely new work).

---

## 🗺️ Reading Path by Role

### First-Time Reader (New to Project)
1. **REQUIREMENTS_SUMMARY.md** (5 min) - Get oriented
2. **ASSIGNMENT_STATEMENT_ANALYSIS.md** (15 min) - Understand scope
3. **REQUIREMENTS_ANALYSIS.md** (30 min) - Deep dive on specific requirements

### Developer (Implementing Features)
1. **REQUIREMENTS_SUMMARY.md** (5 min) - Quick scope check
2. **REQUIREMENTS_ANALYSIS.md** - Reference specific sections as needed during development
3. Use as lookup reference when questions arise

### Product Owner/Reviewer
1. **REQUIREMENTS_SUMMARY.md** (5 min) - Coverage overview
2. **ASSIGNMENT_STATEMENT_ANALYSIS.md** (15 min) - Understand interpretation decisions
3. **REQUIREMENTS_ANALYSIS.md** - Reference for specific requirement questions

### Interviewer/Evaluator
1. **ASSIGNMENT_STATEMENT_ANALYSIS.md** (15 min) - See interpretation approach
2. **REQUIREMENTS_SUMMARY.md** (5 min) - See completeness of coverage
3. **REQUIREMENTS_ANALYSIS.md** - Evaluate technical depth

---

## 🔗 Related Documentation

**Implementation Specifications:**
- `../assignment/SOLUTION_ARCHITECTURE.md` - How requirements are implemented
- `../assignment/IMPLEMENTATION_ROADMAP.md` - Development schedule based on requirements

**Discovery Analysis:**
- `../analysis/PARTIAL_IMPLEMENTATION_ANALYSIS.md` - What infrastructure already exists
- `../analysis/PHASE1_IMPACT_SUMMARY.md` - How discovery affected requirements delivery

**System Analysis:**
- `../current-system/CODEBASE_ANALYSIS.md` - Current system capabilities
- `../current-system/TECHNICAL_FINDINGS_SUMMARY.md` - Gaps and required changes

**Future Work:**
- `../future-work/PHASE2_OVERVIEW.md` - Requirements deferred to Phase 2

---

## 📊 Requirements Coverage Summary

| Requirement Category | Phase 1 Coverage | Phase 2 Coverage | Notes |
|---------------------|------------------|------------------|-------|
| **Faculty Tracking** | ✅ 100% (depositors) | ✅ 100% (all authors) | Phase 1: ~200 accounts, Phase 2: ~5,000 authors |
| **Institution Tracking** | ✅ Exists (leverage) | N/A | Already implemented in current code |
| **Statistics API** | ✅ 100% | ✅ Enhanced | Faculty stats (P1), collaboration metrics (P2) |
| **UI/Dashboard** | ✅ 100% | ✅ Enhanced | Basic UI (P1), advanced visualizations (P2) |
| **Migration** | ✅ 100% (~200 users) | ✅ 100% (~950 authors) | High accuracy P1, lower accuracy P2 |
| **Data Quality** | ✅ ~95% accuracy | ✅ ~80% accuracy | Depositors cleaner than unregistered authors |
| **Testing** | ✅ 100% | ✅ 100% | Unit, integration, E2E for both phases |
| **Documentation** | ✅ 100% | ✅ 100% | Full specs for both phases |

---

## 🎯 Key Decisions Made

### 1. **Depositor-Only for Phase 1**
- **Decision:** Track faculty only for depositors (registered accounts) in Phase 1
- **Rationale:** Simpler data (95% accuracy), faster delivery (2.5 weeks vs 10 weeks)
- **Trade-off:** Can't answer "Which datasets have our faculty **authored**?" until Phase 2
- **Document:** See `../analysis/PHASE1_FOCUS.md`

### 2. **Institution Infrastructure is Existing**
- **Decision:** Leverage existing `dataset_statistics(group_ids=[...])` instead of building new
- **Rationale:** Production code, tested, working - reduces risk and timeline
- **Impact:** 50% time savings (2 weeks → 4-6 hours)
- **Document:** See `../analysis/PARTIAL_IMPLEMENTATION_ANALYSIS.md`

### 3. **Faculty as Flat List (Not Hierarchy)**
- **Decision:** Faculty as simple list in `djehuty.xml`, no department sub-structure in Phase 1
- **Rationale:** Assignment asks for faculty-level only, departments are future enhancement
- **Extensibility:** Can add departments in Phase 3 without breaking changes
- **Document:** See `REQUIREMENTS_ANALYSIS.md` section 2.3

### 4. **Single Faculty per Depositor**
- **Decision:** 1 account = 1 faculty (no multi-faculty affiliations in Phase 1)
- **Rationale:** Depositor has single affiliation at deposit time
- **Contrast:** Phase 2 allows multi-faculty (1 dataset = N faculties via different authors)
- **Document:** See `REQUIREMENTS_ANALYSIS.md` section 3.1

---

## ❓ Common Questions

**Q: Why separate Phase 1 and Phase 2?**  
A: **Complexity and timeline.** Phase 1 (depositors, 200 accounts, 95% accuracy) is 2.5 weeks. Phase 2 (all authors, 5,000 contributors, 80% accuracy, manual review) is 10 weeks. Different entities, different challenges.

**Q: Is Phase 1 a "partial" implementation?**  
A: **No - it's a deliberate scoping decision.** Phase 1 delivers complete faculty tracking for depositors (which answers most business questions). Phase 2 is an enhancement for authorship-based metrics.

**Q: What if requirements change?**  
A: **Modular design supports changes.** Adding new fields, faculties, or metrics is straightforward. See `../assignment/SOLUTION_ARCHITECTURE.md` section 3.1 (Architectural Principles).

**Q: How accurate are the migration estimates?**  
A: **Based on production data analysis.** Analyzed actual datasets, counted TU Delft depositors, checked Organizations field patterns. See `../current-system/DATASET_ANALYSIS.md` for data evidence.

---

## 🎯 Bottom Line

These requirements documents provide:

1. **Clarity:** Clear interpretation of ambiguous assignment requirements
2. **Scope:** Explicit boundaries (Phase 1 vs Phase 2 vs out-of-scope)
3. **Decisions:** Documented rationale for key technical decisions
4. **Coverage:** Mapping of every requirement to implementation approach
5. **Traceability:** Links to technical specs, code analysis, and implementation plans

**Start with REQUIREMENTS_SUMMARY.md** for quick answers, then dive into detailed analysis as needed.

---

**Navigation:** [← Back to docs](../README.md) | [View Analysis →](../analysis/) | [View Assignment Specs →](../assignment/)
