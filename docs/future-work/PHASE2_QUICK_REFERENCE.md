# Phase 2 Quick Reference

**Project:** Author-Level Faculty Statistics (Phase 2 Enhancement)  
**Status:** Future Enhancement Specification  
**Prerequisites:** Phase 1 (Depositor-Only) must be completed

---

## What is Phase 2?

**Phase 1 (Assignment Scope):**
- Tracks depositor's faculty only
- Statistics: "Datasets deposited by each faculty"
- 1 dataset = 1 faculty

**Phase 2 (Future Enhancement):**
- Tracks ALL authors' faculties (registered AND unregistered)
- Statistics: "Datasets authored by each faculty"
- 1 dataset = 1-N faculties (multi-valued)

---

## Key Difference: The Author vs Account Distinction

| Entity | Represents | Count | Has Faculty? |
|--------|------------|-------|--------------|
| **Account** | Registered users who can log in | ~200 | ✅ Yes (Phase 1) |
| **Author** | ALL contributors (registered + unregistered) | ~5,000 | ✅ Yes (Phase 2) |

**Example Dataset:**
- **Depositor:** Dr. Smith (has account, faculty = Aerospace) ← Phase 1 tracks this
- **Co-author 1:** Hebly, Scott J. (NO account, faculty = Aerospace) ← Phase 2 adds this
- **Co-author 2:** Dr. Johnson (has account, faculty = EEMCS) ← Phase 2 adds this
- **Co-author 3:** Dr. Garcia (external, DLR Germany) ← Phase 2 excludes this

**Phase 1 Count:** 1 dataset for Aerospace (depositor only)  
**Phase 2 Count:** 1 dataset for Aerospace + 1 dataset for EEMCS = 2 counts

---

## Phase 2 Scope

### In Scope

1. **Data Model:** Add `faculty_id` to Author entity (not just Account)
2. **Migration:** Assign faculty to ~1,000 existing TU Delft authors
   - 150 registered: Copy from account (100% accuracy)
   - 600 unregistered: Auto-detect from Organizations field (≥80% accuracy)
   - 200 manual review: Human verification (100% accuracy)
3. **Statistics:** Multi-faculty collaboration metrics
4. **API:** 6 new endpoints for author-level queries
5. **UI:** Collaboration dashboard, network visualization

### Out of Scope

- Department-level tracking
- Temporal analysis (faculty changes over time)
- ORCID integration (future)
- Research group tracking

---

## Timeline & Resources

**Duration:** 10 weeks  
**Team:** 2 developers + 2 manual reviewers  
**Budget:** ~200 person-hours

**Breakdown:**
- Week 1-2: Foundation (RDF schema, code structure)
- Week 3-5: Migration (3 phases)
- Week 6-7: API & Statistics
- Week 8-9: UI Development
- Week 10: Testing & Deployment

---

## Success Metrics

| Metric | Target | Phase 1 Comparison |
|--------|--------|-------------------|
| Author coverage | ≥85% | N/A (accounts only) |
| Migration accuracy | ≥80% | 100% (manual entry) |
| High confidence ratio | ≥70% | 100% (all verified) |
| API response time | <150ms | <100ms |
| Statistics query time | <200ms | <100ms |
| Multi-faculty collaborations | ≥100 | 0 (not tracked) |

---

## Document Navigation

**Start here if you're new to Phase 2:**
1. Read `ARCHITECTURE_CORRECTION_AUTHORS.md` to understand the problem
2. Read `PHASE2_OVERVIEW.md` for executive summary
3. Dive into specific documents based on your role:

**For Developers:**
- `PHASE2_DATA_MODEL.md` - RDF schema changes
- `PHASE2_MIGRATION.md` - Migration scripts
- `PHASE2_API_UI.md` - Implementation details

**For Project Managers:**
- `PHASE2_OVERVIEW.md` - Scope and goals
- `PHASE2_IMPLEMENTATION.md` - Timeline and resources
- Risk assessment section

**For Data Specialists:**
- `PHASE2_MIGRATION.md` - Organizations field parsing
- `PHASE2_STATISTICS.md` - Multi-valued queries

---

## Key Files to Review

### Migration Scripts
- `export_registered_authors.py` - Export ~150 registered authors
- `export_unregistered_authors.py` - Export ~800 unregistered authors
- `detect_author_faculty.py` - Pattern matching with confidence scoring
- `import_author_faculty.py` - Bulk import with dry-run support

### SPARQL Templates
- `statistics_faculty_authored.sparql` - Datasets by author faculty
- `statistics_faculty_collaborations.sparql` - Collaboration matrix
- `authors_by_faculty.sparql` - Author contributions
- `update_author_faculty.sparql` - Faculty assignment updates

### API Endpoints
- `GET /v2/authors/{uuid}/faculty` - Get author faculty
- `PATCH /v2/authors/{uuid}/faculty` - Update author faculty
- `GET /v2/statistics/faculties/authored` - Faculty-authored statistics
- `GET /v2/statistics/collaborations` - Collaboration network

---

## Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| Organizations parsing <80% accurate | Manual review workflow + pattern refinement |
| Performance degradation | Caching (6-12 hour TTL) + Virtuoso indexing |
| User confusion about double-counting | Clear UI labels + documentation |
| External authors incorrectly assigned | Validation: faculty.institution = author.institution |

---

## Decision: Should We Implement Phase 2?

### Arguments FOR Phase 2:

✅ **More accurate research metrics:** Captures all faculty contributions, not just depositors  
✅ **Collaboration visibility:** Identifies multi-faculty partnerships  
✅ **Aligns with bibliometrics:** Industry standard to count multi-institutional papers for all institutions  
✅ **Future-proof:** Enables department-level, research group tracking later  
✅ **Valuable insights:** Which faculties collaborate most? External collaboration rates?

### Arguments AGAINST Phase 2:

❌ **Higher complexity:** 10 weeks vs 5 weeks, 2 developers vs 1  
❌ **Data quality challenges:** 80% accuracy vs 100% for Phase 1  
❌ **Double-counting confusion:** Requires user education  
❌ **Maintenance burden:** Need to keep pattern library updated  
❌ **Phase 1 might be sufficient:** Depositor-based stats may meet stakeholder needs

---

## Recommendation

**Approach:**
1. **Complete Phase 1 first** (assignment scope)
2. **Gather stakeholder feedback** on depositor-only statistics
3. **If stakeholders request author-level metrics**, proceed with Phase 2
4. **If Phase 1 sufficient**, defer Phase 2 or cancel

**Pilot Option:**
- Implement Phase 2 for **one faculty only** (e.g., Aerospace)
- Validate accuracy, performance, user satisfaction
- Scale to all faculties if successful

---

## Quick Start (If Approved)

**Week 1 - Day 1:**
```bash
# 1. Review complete Phase 2 specification
cd /home/ruby/Projects/assigment-djehuty
cat PHASE2_OVERVIEW.md
cat PHASE2_DATA_MODEL.md

# 2. Set up development environment
git checkout -b phase2-author-faculty

# 3. Extend RDF schema
vim djehuty/src/djehuty/rdf/schema.ttl
# Add: djht:faculty_id, djht:faculty_confidence, djht:faculty_source, djht:faculty_assigned_date

# 4. Run unit tests
pytest tests/test_author_faculty.py -v

# 5. Begin migration script development
vim scripts/phase2/export_registered_authors.py
```

---

## Contact & Questions

**Architecture Questions:** See `PHASE2_DATA_MODEL.md` Section 7 (Validation Rules)  
**Migration Questions:** See `PHASE2_MIGRATION.md` Section 5 (Quality Assurance)  
**API Questions:** See `PHASE2_API_UI.md` Section 1 (API Endpoints)  
**Timeline Questions:** See `PHASE2_IMPLEMENTATION.md` Section 2 (Development Phases)

---

## Summary Table

| Aspect | Phase 1 (Assignment) | Phase 2 (Enhancement) |
|--------|---------------------|----------------------|
| **Scope** | Depositor-only | All authors |
| **Entities** | Account (~200) | Author (~5,000) |
| **Statistics** | Deposited datasets | Authored datasets |
| **Count Type** | Single-valued | Multi-valued |
| **Timeline** | 5 weeks | 10 weeks |
| **Accuracy** | 100% (manual) | 80-90% (hybrid) |
| **Complexity** | Low | High |
| **Value** | Institutional reporting | Research metrics |

---

**Next Steps:**
1. Present Phase 1 results to stakeholders
2. Gauge interest in author-level statistics
3. If approved: Begin Phase 2 Week 1 (Foundation)
4. If deferred: Monitor usage patterns, revisit in 6 months

---

*This quick reference summarizes the complete Phase 2 architecture. For full details, see the 6 Phase 2 documents.*
