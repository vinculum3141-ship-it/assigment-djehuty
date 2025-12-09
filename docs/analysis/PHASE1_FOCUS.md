# Phase 1 Focus - Assignment Implementation

**For the remainder of this discussion, we are focused EXCLUSIVELY on Phase 1.**

---

## 📋 Phase 1 Scope (The Assignment)

**Goal:** Implement faculty-level statistics for the 4TU.ResearchData repository

**Approach:** Depositor-only (track faculty for registered users who upload datasets)

**Timeline:** 5 weeks, 1 developer

**Deliverables:**
1. Faculty entity in RDF schema
2. `faculty_id` on Account entity
3. 6 API endpoints for faculty data
4. Statistics dashboard showing datasets by faculty
5. Migration of ~200 depositor accounts

---

## 📂 Phase 1 Documentation

All Phase 1 documentation is in `docs/assignment/`:

```
docs/assignment/
├── README.md                      ← Phase 1 overview and guide
├── SOLUTION_ARCHITECTURE.md       ← Complete 61-page specification
└── ARCHITECTURE_SUMMARY.md        ← 6-page quick reference
```

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

---

## 🚀 Next Steps (Phase 1)

**Week 1: Foundation**
1. Configure faculties in `djehuty.xml`
2. Extend RDF schema with Faculty entity
3. Create FacultyManager service
4. Write unit tests

**Week 2: Migration**
1. Export depositor accounts
2. Manual review of Organizations field
3. Import faculty assignments
4. Validate coverage ≥90%

**Week 3: API**
1. Implement 6 endpoints
2. Create SPARQL templates
3. Add validation
4. Integration tests

**Week 4: UI**
1. Faculty dropdown in registration
2. Auto-fill on dataset submission
3. Statistics dashboard
4. Admin update interface

**Week 5: Testing & Deployment**
1. End-to-end testing
2. Performance testing
3. User acceptance testing
4. Production deployment

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
- 5-week timeline
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
