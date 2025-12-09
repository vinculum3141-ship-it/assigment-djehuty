# Phase 2 Solution Architecture: Author-Level Faculty Statistics

**Project:** 4TU.ResearchData Faculty-Level Statistics - Phase 2  
**Date:** December 9, 2025  
**Status:** Future Enhancement Specification  
**Prerequisites:** Phase 1 (Depositor-Only Statistics) must be completed

---

## Document Structure

This architecture is broken into multiple sections to avoid length limits:

1. **PHASE2_OVERVIEW.md** (this document) - Executive summary and scope
2. **PHASE2_DATA_MODEL.md** - RDF schema extensions for author-level faculty
3. **PHASE2_MIGRATION.md** - Migration strategy for unregistered authors
4. **PHASE2_STATISTICS.md** - Multi-valued statistics queries and aggregation
5. **PHASE2_API_UI.md** - API endpoints and UI for author-level features
6. **PHASE2_IMPLEMENTATION.md** - Timeline, testing, and deployment

---

## Executive Summary

### What Phase 2 Adds

**Phase 1 (Assignment Scope):**
- Track depositor's faculty via `djht:Account.faculty_id`
- Statistics: "Datasets deposited by each faculty"
- Limitation: Co-author affiliations not tracked

**Phase 2 (This Document):**
- Track **all authors'** faculties via `djht:Author.faculty_id`
- Statistics: "Datasets authored by each faculty" (includes co-authors)
- Multi-faculty collaboration metrics
- Unregistered author faculty assignment

---

## Problem Statement

### Current Limitation (Post-Phase 1)

After Phase 1 implementation, the system can answer:
- ✅ "How many datasets did Faculty of Aerospace **deposit**?" (depositor-based)

But it **cannot** answer:
- ❌ "How many datasets have Faculty of Aerospace **authors**?" (authorship-based)
- ❌ "Which datasets are multi-faculty collaborations?"
- ❌ "What are the top faculty collaboration pairs?"

### Real-World Example

**Dataset:** "Aviation NOx Emissions Modeling"
- **Depositor:** Dr. Smith (Faculty of Aerospace, has account)
- **Co-author 1:** Hebly, Scott J. (Faculty of Aerospace, NO account)
- **Co-author 2:** Dr. Johnson (Faculty of EEMCS, has account but didn't deposit)
- **Co-author 3:** Dr. Garcia (DLR Germany, external, NO account)

**Phase 1 Statistics:**
- ✅ Counts for: Faculty of Aerospace (depositor only)
- ❌ Missing: Faculty of EEMCS contribution (co-author)

**Phase 2 Statistics:**
- ✅ Counts for: Faculty of Aerospace (2 authors)
- ✅ Counts for: Faculty of EEMCS (1 author)
- ✅ Multi-faculty collaboration: Aerospace + EEMCS
- ⚠️ External author: DLR Germany (tracked but not in faculty stats)

---

## Key Differences from Phase 1

| Aspect | Phase 1 (Depositor-Only) | Phase 2 (Author-Inclusive) |
|--------|--------------------------|----------------------------|
| **Entity** | `djht:Account` | `djht:Author` |
| **Population** | ~200 registered users | ~5,000+ all authors |
| **Assignment** | At registration | During dataset creation + migration |
| **Registered authors** | faculty_id from account | faculty_id from account (auto-copy) |
| **Unregistered authors** | N/A (ignored) | faculty_id from Organizations parser |
| **Statistics** | 1 dataset = 1 faculty | 1 dataset = 1-N faculties |
| **Double-counting** | No | Yes (by design) |
| **Complexity** | Low | High |

---

## Scope

### In Scope

1. **Data Model:**
   - Add `djht:faculty_id` predicate to `djht:Author` entity
   - Support multiple authors per dataset with different faculties
   - Link author faculty to depositor faculty where applicable

2. **Migration:**
   - Assign faculty to existing ~5,000 authors in system
   - Parse Organizations field for unregistered authors
   - Copy faculty_id from accounts for registered authors
   - Manual review workflow for ambiguous cases

3. **Statistics:**
   - "Datasets by faculty authorship" (multi-valued counts)
   - "Multi-faculty collaboration matrix"
   - "Top faculty collaboration pairs"
   - "Internal vs external collaboration ratios"

4. **API:**
   - Author faculty assignment endpoints
   - Multi-faculty statistics queries
   - Collaboration network data

5. **UI:**
   - Author-level faculty selection in dataset forms
   - Multi-faculty collaboration dashboard
   - Author profile faculty display

### Out of Scope

1. Department-level granularity (below faculty)
2. Research group tracking
3. Temporal analysis (faculty changes over time)
4. Citation network integration
5. Author disambiguation (ORCID matching)

---

## Assumptions

1. **Organizations field format:** Contains faculty information for most datasets
2. **TU Delft focus:** Initial rollout covers TU Delft faculties only
3. **Static faculty:** Authors' faculty affiliations don't change over time (historical snapshots)
4. **ORCID optional:** ORCID IDs help but are not required for faculty assignment
5. **External authors:** Tracked but excluded from faculty statistics (institution_id ≠ 28586)

---

## Success Criteria

### Technical Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Author migration coverage | ≥85% | Authors with faculty_id / Total TU Delft authors |
| Registered author accuracy | 100% | Auto-copied from account (no errors expected) |
| Unregistered author accuracy | ≥80% | Manual validation of Organizations parsing |
| Statistics query performance | <200ms | Multi-faculty aggregation with caching |
| API response time | <150ms | Author faculty assignment endpoints |

### User Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Author faculty selection rate | ≥70% | New datasets with author-level faculty assignments |
| Manual review completion rate | ≥90% | Ambiguous cases reviewed within 2 weeks |
| Collaboration dashboard usage | ≥50 views/month | Analytics tracking |

### Business Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Multi-faculty collaborations identified | ≥100 datasets | Datasets with authors from ≥2 faculties |
| External collaboration rate | Measurable | % datasets with non-TU Delft authors |
| Faculty research profile completeness | ≥80% | Faculties with ≥10 authored datasets |

---

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Organizations parsing accuracy <80% | Medium | High | Extended pattern library, manual review workflow |
| Double-counting confusion | High | Medium | Clear documentation, separate statistics views |
| External author noise in statistics | Medium | Low | Filter by institution_id in queries |
| Performance degradation with multi-valued queries | Low | Medium | Aggressive caching, materialized views |
| Unregistered author data quality | High | Medium | ORCID matching, manual curation tools |

---

## Dependencies

### Prerequisites (Must Complete Phase 1 First)

1. ✅ Faculty taxonomy defined in XML configuration
2. ✅ `djht:Faculty` entity created in RDF schema
3. ✅ Phase 1 migration complete (depositor accounts assigned)
4. ✅ Statistics infrastructure in place (caching, SPARQL templates)

### External Dependencies

1. **ORCID API:** For author disambiguation (optional enhancement)
2. **Manual review team:** For ambiguous author-faculty assignments
3. **Stakeholder input:** Faculty taxonomy validation for all 4TU institutions

---

## Timeline Estimate

**Duration:** 8-10 weeks (2 developers)

**Breakdown:**
- Week 1-2: Data model extensions, schema updates
- Week 3-5: Author migration (parsing, matching, manual review)
- Week 6-7: Statistics queries, API development
- Week 8-9: UI implementation, collaboration dashboard
- Week 10: Testing, validation, deployment

**Comparison to Phase 1:**
- Phase 1: 5 weeks, 1 developer (depositor-only)
- Phase 2: 10 weeks, 2 developers (all authors, 25x more entities)

---

## Architecture Principles (Inherited from Phase 1)

1. **RDF-Native:** Use RDF predicates, not denormalized data
2. **Backward Compatible:** All new fields are optional
3. **Configuration-Driven:** Faculty taxonomy in XML, not hardcoded
4. **SPARQL-First:** Statistics via SPARQL aggregation, not application logic
5. **Cached Results:** Expensive queries cached, invalidated on write

**New for Phase 2:**
6. **Multi-Valued Semantics:** Accept that 1 dataset can count for multiple faculties
7. **Graduated Confidence:** Track confidence scores for auto-assigned faculties
8. **External Author Filtering:** Separate internal vs external statistics

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Presentation Layer                         │
├─────────────────────────────────────────────────────────────┤
│  - Author Faculty Assignment UI                              │
│  - Multi-Faculty Collaboration Dashboard                     │
│  - Author Profile with Faculty Badge                         │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ HTTP/JSON
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                          │
├─────────────────────────────────────────────────────────────┤
│  - AuthorFacultyManager (assign, validate, review)           │
│  - CollaborationStatisticsService (multi-faculty queries)    │
│  - AuthorMigrationService (parse Organizations, match)       │
│  - ConfidenceScorer (ML-based pattern matching)              │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ SPARQL
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
├─────────────────────────────────────────────────────────────┤
│  Virtuoso RDF Store                                          │
│  - djht:Author entities (~5,000)                             │
│  - djht:Author.faculty_id predicate (NEW)                    │
│  - djht:Author.faculty_confidence (NEW)                      │
│  - djht:Faculty entities (from Phase 1)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Next Steps

1. **Read detailed architecture documents:**
   - `PHASE2_DATA_MODEL.md` - RDF schema changes
   - `PHASE2_MIGRATION.md` - Author migration strategy
   - `PHASE2_STATISTICS.md` - Multi-valued queries
   - `PHASE2_API_UI.md` - Endpoints and UI
   - `PHASE2_IMPLEMENTATION.md` - Timeline and testing

2. **Stakeholder validation:**
   - Confirm author-level statistics are desired
   - Validate complexity vs value trade-off
   - Approve extended timeline (10 weeks vs 5 weeks)

3. **Prioritization:**
   - Decide if Phase 2 should follow immediately or wait for Phase 1 feedback
   - Identify pilot faculty for testing (e.g., Faculty of Aerospace)

4. **Resource planning:**
   - Allocate 2 developers (vs 1 for Phase 1)
   - Budget for manual review team (20-30 hours)
   - Plan for ongoing curation tools

---

## Document Navigation

**Current:** PHASE2_OVERVIEW.md ← YOU ARE HERE

**Next:** PHASE2_DATA_MODEL.md (RDF schema extensions)

**See also:**
- `ARCHITECTURE_CORRECTION_AUTHORS.md` - Analysis of author vs account distinction
- `SOLUTION_ARCHITECTURE.md` - Phase 1 complete specification
- `ARCHITECTURE_SUMMARY.md` - Phase 1 quick reference

---

*This document provides the strategic overview. Technical details in subsequent documents.*
