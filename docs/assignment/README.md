# Phase 1: Faculty Statistics Implementation (The Assignment)

This folder contains the **complete specification for implementing faculty-level statistics** using the depositor-only approach (5-week timeline, 1 developer).

---

## 📋 What is Phase 1?

**Scope:** Add faculty tracking for **depositors only** (registered users who upload datasets)

**Approach:**
- Add `faculty_id` to **Account entity** (not Author)
- Statistics: "Datasets **deposited** by each faculty"
- 1 dataset = 1 faculty (depositor's faculty)
- Migration: ~200 depositor accounts
- **No tracking of co-author faculties**

**Why depositor-only?**
- Simpler: Only ~200 accounts vs ~5,000 authors
- Faster: 5 weeks vs 10 weeks
- Matches existing behavior: `institution_id` is also depositor-only
- Good enough for institutional reporting: "Which faculty deposited the most datasets?"

**Trade-off:** Can't answer "Which datasets have our faculty researchers **authored**?" (requires Phase 2)

---

## 📄 Documents

### 1. IMPLEMENTATION_ROADMAP.md (30 pages, ~45 min read) ⭐ **NEW**

**Purpose:** Complete 5-week delivery plan for stakeholders (technical and non-technical).

**Contents:**
- Executive summary with business value
- Detailed week-by-week schedule with tasks and deliverables
- Team roles and resource requirements
- Budget and ROI analysis
- Testing strategy and quality assurance
- Rollout and deployment plan
- Risk assessment and mitigation
- Communication and training plan
- Success metrics and monitoring
- Post-launch roadmap

**When to use:**
- Project planning and approval
- Stakeholder presentations
- Team onboarding
- Progress tracking during implementation

---

### 2. ROADMAP_EXECUTIVE_SUMMARY.md (2 pages, ~5 min read) ⭐ **NEW**

**Purpose:** 1-page overview of the roadmap for busy stakeholders.

**Contents:**
- What we're building
- 5-week timeline (table format)
- Success metrics
- Resource requirements
- Key risks
- Approvals required
- Business value

**When to use:**
- Quick stakeholder briefings
- Budget approval meetings
- Executive summaries

---

### 3. SOLUTION_ARCHITECTURE.md (61 pages, ~2 hours read)

**Purpose:** Complete technical specification for implementation.

**Contents:**
1. Executive Summary
2. Requirements Analysis
3. Architectural Principles
4. Data Model Design (RDF schema extensions)
5. System Components (FacultyManager service, validators)
6. API Design (6 endpoints with request/response examples)
7. User Interface Design (mockups, workflows)
8. Migration Strategy (3 phases, Python scripts)
9. Implementation Phases (5-week timeline)
10. Security & Privacy Considerations
11. Performance & Scalability
12. Testing Strategy
13. Risks & Mitigation
14. Success Metrics

**When to read:**
- You're implementing the solution
- You need detailed specifications
- You want code examples
- You're planning the development

**Key sections for developers:**
- Section 4: RDF schema changes
- Section 5: Python code structure
- Section 6: API endpoints
- Section 8: Migration scripts

---

### 4. ARCHITECTURE_SUMMARY.md (6 pages, ~15 min read)

**Purpose:** Quick reference guide for daily development.

**Contents:**
- Architecture overview diagram
- Component summary
- API endpoints quick reference
- Migration strategy overview
- Faculty codes table (8 TU Delft faculties)
- Implementation checklist
- Quick start commands

**When to read:**
- You need a quick lookup during development
- You're onboarding a new team member
- You want a high-level overview
- You need the faculty code reference table

**Use this as:** Your daily companion document during implementation.

---

### 5. PRESENTATION_OUTLINE.md (14 slides, ~15 min presentation)

**Purpose:** Present the solution to stakeholders for approval.

**Contents:**
- Slide 1: Title & Overview
- Slide 2: Problem Statement
- Slide 3: Current System Limitations
- Slide 4: Proposed Solution
- Slide 5: Faculty Taxonomy
- Slide 6: Architecture Overview
- Slide 7: User Workflows
- Slide 8: Migration Strategy
- Slide 9: Implementation Timeline (5 weeks)
- Slide 10: Technical Details
- Slide 11: Benefits
- Slide 12: Success Metrics
- Slide 13: Risks & Mitigation
- Slide 14: Next Steps

**When to use:**
- Stakeholder approval meetings
- Project kickoff presentations
- Team briefings
- Executive summaries

**Includes:** Speaker notes for each slide.

---

## 🏗️ Architecture Overview

### New Components

```
Faculty Configuration (djehuty.xml)
    ↓
Faculty Entity (RDF)
    ↓
Account.faculty_id (new predicate)
    ↓
FacultyManager Service
    ↓
API Endpoints (6 new)
    ↓
UI Components (3 new)
    ↓
Statistics Dashboard
```

### RDF Schema Changes

**New entity:**
```turtle
djht:Faculty
    djht:id "285860001"
    djht:name "Faculty of Aerospace Engineering"
    djht:abbreviation "AE"
```

**Extended entity:**
```turtle
djht:Account
    # Existing predicates...
    djht:faculty_id "285860001"  # NEW: Required for TU Delft accounts
```

### 6 API Endpoints

1. `GET /v2/faculties` - List all faculties
2. `GET /v2/faculties/{id}` - Get faculty details
3. `GET /v2/statistics/faculties` - Faculty statistics
4. `GET /v2/statistics/faculties/{id}/datasets` - Datasets by faculty
5. `PATCH /v2/accounts/{uuid}` - Update account faculty (extended)
6. `POST /v2/datasets` - Create dataset (extended)

---

## 🚀 Implementation Timeline

**Total: 5 weeks, 1 developer**

### Week 1: Foundation (8 days)
- Configure faculties in djehuty.xml
- Extend RDF schema with Faculty entity
- Create FacultyManager service
- Write unit tests

### Week 2: Data Migration (5 days)
- Export depositor accounts (~200)
- Parse Organizations field for faculty
- Manual review workflow
- Import faculty_id assignments

### Week 3: API Development (5 days)
- Implement 6 API endpoints
- Create SPARQL query templates
- Add input validation
- Write integration tests

### Week 4: UI Development (5 days)
- Add faculty dropdown to registration
- Auto-fill faculty on dataset submission
- Build statistics dashboard
- Create faculty filter

### Week 5: Testing & Deployment (5 days)
- End-to-end testing
- Performance testing
- User acceptance testing
- Production deployment

---

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Migration coverage | ≥90% depositor accounts |
| Migration accuracy | 100% (manual verification) |
| API response time | <100ms |
| Statistics query time | <150ms |
| Dashboard load time | <2 seconds |
| User adoption | ≥80% within 3 months |

---

## 🎯 Quick Start

### For Developers

**Day 1:**
```bash
# 1. Read the quick reference
cd docs/assignment
cat ARCHITECTURE_SUMMARY.md

# 2. Review RDF schema changes
cat SOLUTION_ARCHITECTURE.md | grep -A 50 "Section 4"

# 3. Set up development environment
cd ../../djehuty
git checkout -b feature/faculty-statistics

# 4. Configure faculties
vim djehuty.xml
# Add <faculty> entries from SOLUTION_ARCHITECTURE.md Section 4.1
```

**Week 1:**
- Read SOLUTION_ARCHITECTURE.md Sections 4-5 (Data Model & Components)
- Implement FacultyManager service
- Write unit tests for faculty validation

**Week 2:**
- Read SOLUTION_ARCHITECTURE.md Section 8 (Migration)
- Run migration scripts
- Manual review of Organizations field

**Week 3-4:**
- Read SOLUTION_ARCHITECTURE.md Sections 6-7 (API & UI)
- Implement endpoints and UI components

**Week 5:**
- Read SOLUTION_ARCHITECTURE.md Section 12 (Testing)
- Execute test plans and deploy

---

### For Project Managers

**Pre-Kickoff:**
1. Review PRESENTATION_OUTLINE.md (15 min)
2. Present to stakeholders for approval
3. Review SOLUTION_ARCHITECTURE.md Section 9 (timeline) and Section 13 (risks)

**Weekly Check-ins:**
- Use ARCHITECTURE_SUMMARY.md Section 5 (Implementation Checklist)
- Track progress against 5-week timeline
- Review success metrics from SOLUTION_ARCHITECTURE.md Section 14

---

## 🔍 Key Files to Implement

From SOLUTION_ARCHITECTURE.md Section 5:

| Component | File Path | Lines of Code |
|-----------|-----------|---------------|
| FacultyManager | `src/djehuty/web/faculty.py` | ~200 |
| API routes | `src/djehuty/ui.py` | ~300 |
| SPARQL templates | `src/djehuty/web/resources/sparql/faculties.sparql` | ~150 |
| UI templates | `src/djehuty/web/resources/html/register.html` | ~50 |
| Migration script | `scripts/migrate_faculty.py` | ~250 |

**Total:** ~950 lines of new code + ~300 lines of changes to existing files

---

## ⚠️ Important Constraints

1. **Depositor-only:** Do NOT track faculty for co-authors (that's Phase 2)
2. **TU Delft only:** Faculty field is optional for other institutions
3. **Backward compatible:** Existing accounts without faculty_id continue to work
4. **No ORCID integration:** Manual faculty assignment only
5. **Organizations field remains:** Keep for display, add faculty_id for aggregation

---

## 🤔 Common Questions

**Q: Why not track all author faculties?**
A: That's Phase 2 (10 weeks, 2 developers). Phase 1 focuses on depositors only to meet the 5-week timeline. See `../future-work/ARCHITECTURE_CORRECTION_AUTHORS.md` for details.

**Q: What if a depositor changes faculty?**
A: Faculty is assigned at registration time. If they change faculty, admin can update via PATCH /v2/accounts/{uuid}.

**Q: How accurate is the Organizations field parsing?**
A: ~95% for TU Delft depositors (simpler data). Phase 2 migration has lower accuracy (~80%) because unregistered authors have messier data.

**Q: Can we track department-level?**
A: Not in Phase 1. Focus is faculty-level only. Department tracking could be Phase 3.

**Q: What about external institutions?**
A: Faculty field is TU Delft-specific. Accounts from UT, TU/e, WUR do not require faculty_id.

---

## 📞 Need Help?

**Specific topics:**
- **RDF Schema:** SOLUTION_ARCHITECTURE.md Section 4
- **Migration:** SOLUTION_ARCHITECTURE.md Section 8
- **API Design:** SOLUTION_ARCHITECTURE.md Section 6
- **UI Mockups:** SOLUTION_ARCHITECTURE.md Section 7
- **Testing:** SOLUTION_ARCHITECTURE.md Section 12
- **Deployment:** SOLUTION_ARCHITECTURE.md Section 9.6

**Cross-reference with current system:**
- `../current-system/CODEBASE_ANALYSIS.md` for existing code structure
- `../current-system/DATASET_ANALYSIS.md` for Organizations field examples

---

## 🔄 After Phase 1

**If stakeholders request author-level statistics:**
- See `../future-work/` for Phase 2 specification
- Start with `PHASE2_QUICK_REFERENCE.md` for decision framework
- Review `ARCHITECTURE_CORRECTION_AUTHORS.md` to understand the difference

**If Phase 1 is sufficient:**
- Monitor usage metrics for 3 months
- Gather user feedback
- Consider Phase 2 in 6-12 months

---

*This is the complete specification for the 5-week assignment. Start with ARCHITECTURE_SUMMARY.md for a quick overview, then dive into SOLUTION_ARCHITECTURE.md for detailed implementation guidance.*
