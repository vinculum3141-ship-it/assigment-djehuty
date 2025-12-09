# Phase 2: Implementation Plan

**Document:** PHASE2_IMPLEMENTATION.md  
**Part of:** Phase 2 Solution Architecture (Author-Level Faculty Statistics)  
**Prerequisites:** Complete Phase 1, read all Phase 2 documents

---

## Table of Contents

1. Implementation Timeline
2. Development Phases
3. Testing Strategy
4. Deployment Plan
5. Success Criteria
6. Risks & Mitigation
7. Post-Deployment Monitoring

---

## 1. Implementation Timeline

### 1.1 Overview

**Total Duration:** 10 weeks  
**Team Size:** 2 developers + 2 manual reviewers  
**Dependencies:** Phase 1 complete and validated

```
Week 1-2:  Foundation (RDF schema, code structure)
Week 3-5:  Migration (registered + unregistered authors)
Week 6-7:  API & Statistics (endpoints, queries)
Week 8-9:  UI Development (dashboards, visualizations)
Week 10:   Testing & Deployment
```

### 1.2 Gantt Chart

```
Phase             Week 1   Week 2   Week 3   Week 4   Week 5   Week 6   Week 7   Week 8   Week 9   Week 10
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
Foundation        [████████]
Migration Phase 2A          [████████]
Migration Phase 2B                    [████████████████████████]
Migration Phase 2C                              [████████████████████████]
API Development                                          [████████████████]
Statistics Queries                                                [████████████████]
UI Components                                                              [████████████████]
Testing                                                                              [████████████████]
Deployment                                                                                    [████████]
```

---

## 2. Development Phases

### 2.1 Week 1-2: Foundation

**Objective:** Extend RDF schema and code infrastructure for author-level faculty.

**Tasks:**

| Task | Owner | Hours | Deliverable |
|------|-------|-------|-------------|
| Add `faculty_id` predicate to Author entity in RDF schema | Dev 1 | 4 | Updated schema.ttl |
| Add `faculty_confidence`, `faculty_source`, `faculty_assigned_date` predicates | Dev 1 | 2 | Updated schema.ttl |
| Extend `insert_author()` method to accept faculty parameters | Dev 1 | 6 | Updated database.py |
| Create `update_author_faculty.sparql` template | Dev 1 | 3 | New SPARQL file |
| Create `authors_by_faculty.sparql` template | Dev 1 | 3 | New SPARQL file |
| Add `FacultyManager` service class | Dev 2 | 8 | New faculty_manager.py |
| Unit tests for schema extensions | Dev 2 | 8 | test_author_faculty.py |
| Update djehuty.xml with all 4TU faculty taxonomies | Dev 1 | 4 | Updated djehuty.xml |

**Acceptance Criteria:**
- ✅ Author entity can store faculty_id with confidence scores
- ✅ SPARQL queries can filter by author faculty_id
- ✅ Unit tests pass (≥80% coverage on new code)

---

### 2.2 Week 3-5: Migration

**Objective:** Assign faculty to ~1,000 existing TU Delft authors.

#### **Week 3: Phase 2A - Registered Authors**

| Task | Owner | Hours | Deliverable |
|------|-------|-------|-------------|
| Write `export_registered_authors.py` script | Dev 1 | 4 | Migration script |
| Run export on production RDF store | Dev 1 | 2 | phase2a_*.csv |
| Validate exported data (spot checks) | Dev 2 | 2 | Validation report |
| Write `import_author_faculty.py` script | Dev 1 | 6 | Import script |
| Dry-run import on staging environment | Dev 1 | 2 | Dry-run log |
| Execute import on production | Dev 1 | 1 | 150 authors migrated |
| Validation queries (consistency checks) | Dev 2 | 3 | Validation report |

**Milestone:** 150 registered authors have faculty_id (confidence = 1.0)

#### **Week 4-5: Phase 2B - Unregistered Authors (Automated)**

| Task | Owner | Hours | Deliverable |
|------|-------|-------|-------------|
| Write `export_unregistered_authors.py` script | Dev 1 | 6 | Export script |
| Build faculty pattern library | Dev 1 | 8 | FACULTY_PATTERNS dict |
| Write `detect_author_faculty.py` script | Dev 2 | 12 | Detection script |
| Run detection on staging data | Dev 2 | 4 | phase2b_*.csv |
| Analyze confidence distribution | Dev 2 | 2 | Analysis report |
| Tune patterns to achieve ≥70% high confidence | Dev 1 + Dev 2 | 8 | Updated patterns |
| Import high-confidence assignments (≥0.8) | Dev 1 | 2 | ~600 authors migrated |
| Validation queries | Dev 2 | 4 | Validation report |

**Milestone:** ~600 unregistered authors auto-assigned (confidence ≥ 0.8)

#### **Week 5: Phase 2C - Manual Review**

| Task | Owner | Hours | Deliverable |
|------|-------|-------|-------------|
| Export manual review CSV (~200 authors) | Dev 1 | 2 | phase2c_review.csv |
| Distribute to manual reviewers | Dev 1 | 1 | Email + instructions |
| Manual review (2 reviewers, 100 each) | Reviewer 1 + 2 | 20 each | Reviewed CSV |
| Import manually reviewed assignments | Dev 1 | 2 | ~150 authors migrated |
| Final validation (all checks) | Dev 2 | 4 | Validation report |

**Milestone:** ≥85% TU Delft authors have faculty_id, ≥80% accuracy

---

### 2.3 Week 6-7: API & Statistics

**Objective:** Implement Phase 2 API endpoints and statistics queries.

#### **Week 6: Core API Endpoints**

| Task | Owner | Hours | Deliverable |
|------|-------|-------|-------------|
| Implement `GET /v2/authors/{uuid}/faculty` | Dev 1 | 4 | Route handler |
| Implement `PATCH /v2/authors/{uuid}/faculty` | Dev 1 | 6 | Route handler |
| Add validation logic (institution match, faculty exists) | Dev 1 | 4 | Validation functions |
| Unit tests for API endpoints | Dev 2 | 8 | test_api_faculty.py |
| Integration tests (full request/response cycle) | Dev 2 | 6 | test_integration_faculty.py |

#### **Week 7: Statistics Endpoints**

| Task | Owner | Hours | Deliverable |
|------|-------|-------|-------------|
| Create `statistics_faculty_authored.sparql` | Dev 1 | 4 | SPARQL template |
| Implement `GET /v2/statistics/faculties/authored` | Dev 1 | 6 | Route handler |
| Add caching logic (6-hour TTL) | Dev 1 | 3 | Cache integration |
| Create `statistics_faculty_collaborations.sparql` | Dev 2 | 6 | SPARQL template |
| Implement `GET /v2/statistics/collaborations` | Dev 2 | 6 | Route handler |
| CSV export support | Dev 2 | 4 | CSV formatter |
| Performance testing (query execution time) | Dev 2 | 4 | Performance report |

**Milestone:** 6 Phase 2 API endpoints live and tested

---

### 2.4 Week 8-9: UI Development

**Objective:** Build user interfaces for Phase 2 features.

#### **Week 8: Core UI Components**

| Task | Owner | Hours | Deliverable |
|------|-------|-------|-------------|
| Design faculty badge component (mockup) | Dev 1 | 2 | HTML/CSS mockup |
| Implement author faculty badge on profile pages | Dev 1 | 6 | Updated author.html |
| Add faculty dropdown to dataset author form | Dev 1 | 8 | Updated dataset_form.html |
| JavaScript for auto-populating faculty from account | Dev 2 | 6 | dataset_form.js |
| CSS styling for faculty badges and indicators | Dev 2 | 4 | Updated styles.css |

#### **Week 9: Collaboration Dashboard**

| Task | Owner | Hours | Deliverable |
|------|-------|-------|-------------|
| Design collaboration dashboard layout | Dev 1 | 3 | Mockup |
| Implement D3.js network visualization | Dev 1 | 12 | collaboration_network.js |
| Create collaboration table | Dev 2 | 4 | HTML/JS |
| Implement Phase 1 vs Phase 2 comparison chart | Dev 2 | 8 | Chart.js charts |
| Responsive design for mobile | Dev 2 | 4 | Updated CSS |

**Milestone:** All Phase 2 UI components functional and responsive

---

### 2.5 Week 10: Testing & Deployment

**Objective:** Comprehensive testing and production deployment.

| Task | Owner | Hours | Deliverable |
|------|-------|-------|-------------|
| End-to-end testing (user workflows) | Dev 1 + Dev 2 | 8 | Test report |
| Performance testing (load testing) | Dev 2 | 4 | Performance report |
| UAT with institutional users | Product Owner | 6 | UAT feedback |
| Fix critical bugs from UAT | Dev 1 + Dev 2 | 8 | Bug fixes |
| Write deployment checklist | Dev 1 | 2 | Checklist |
| Production deployment (off-hours) | Dev 1 + Dev 2 | 4 | Deployed system |
| Post-deployment smoke tests | Dev 2 | 2 | Smoke test report |
| Documentation update | Dev 1 | 4 | Updated docs |
| Knowledge transfer to support team | Dev 1 | 2 | Training session |

**Milestone:** Phase 2 live in production

---

## 3. Testing Strategy

### 3.1 Unit Tests

**Coverage Target:** ≥80%

**Key Test Files:**

```python
# tests/test_author_faculty.py
def test_insert_author_with_faculty():
    """Test author creation with faculty_id."""
    author_uuid = db.insert_author(
        full_name="Test Author",
        institution_id=28586,
        faculty_id=285860001,
        faculty_confidence=1.0,
        faculty_source="test"
    )
    assert author_uuid is not None
    
    # Verify faculty was stored
    author = db.author(author_uuid)
    assert author['faculty_id'] == 285860001
    assert author['faculty_confidence'] == 1.0

def test_update_author_faculty():
    """Test faculty assignment update."""
    # Create author without faculty
    author_uuid = db.insert_author(full_name="Test", institution_id=28586)
    
    # Update faculty
    success = db.update_author_faculty(
        author_uuid=author_uuid,
        faculty_id=285860005,
        confidence=0.85,
        source="organizations_auto"
    )
    assert success
    
    # Verify update
    author = db.author(author_uuid)
    assert author['faculty_id'] == 285860005

def test_faculty_institution_validation():
    """Test faculty must match author institution."""
    with pytest.raises(ValidationError):
        db.insert_author(
            full_name="Test",
            institution_id=28587,  # UT
            faculty_id=285860001   # TU Delft faculty - should fail
        )
```

### 3.2 Integration Tests

```python
# tests/test_api_faculty_integration.py
def test_get_author_faculty(client):
    """Test GET /v2/authors/{uuid}/faculty endpoint."""
    response = client.get('/v2/authors/test-uuid/faculty')
    assert response.status_code == 200
    
    data = response.json()
    assert 'faculty_id' in data
    assert 'faculty_confidence' in data

def test_update_author_faculty_api(client, auth_token):
    """Test PATCH /v2/authors/{uuid}/faculty endpoint."""
    response = client.patch(
        '/v2/authors/test-uuid/faculty',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={
            'faculty_id': 285860001,
            'confidence': 1.0,
            'source': 'manual'
        }
    )
    assert response.status_code == 200

def test_faculty_statistics(client):
    """Test GET /v2/statistics/faculties/authored endpoint."""
    response = client.get('/v2/statistics/faculties/authored?institution_id=28586')
    assert response.status_code == 200
    
    data = response.json()
    assert 'statistics' in data
    assert len(data['statistics']) == 8  # 8 TU Delft faculties
```

### 3.3 Performance Tests

**Tool:** Apache JMeter or Locust

**Scenarios:**

1. **Statistics Query Load Test**
   - Endpoint: `GET /v2/statistics/faculties/authored`
   - Concurrent users: 50
   - Duration: 5 minutes
   - Target: <200ms average response time

2. **Author Faculty Lookup**
   - Endpoint: `GET /v2/authors/{uuid}/faculty`
   - Concurrent users: 100
   - Duration: 5 minutes
   - Target: <100ms average response time

3. **Collaboration Matrix**
   - Endpoint: `GET /v2/statistics/collaborations`
   - Concurrent users: 20
   - Duration: 5 minutes
   - Target: <500ms average response time

### 3.4 User Acceptance Testing (UAT)

**Participants:** 3-5 institutional users from TU Delft

**Scenarios:**

| Scenario | User Action | Expected Outcome |
|----------|-------------|------------------|
| View faculty statistics | Navigate to /statistics/faculties | See Phase 1 vs Phase 2 comparison charts |
| Explore collaboration network | Navigate to /statistics/collaborations | See D3.js network graph with faculty collaborations |
| View author profile | Navigate to /authors/{uuid} | See faculty badge (if assigned) |
| Submit dataset with co-authors | Create new dataset, add authors | Faculty auto-populated for registered, dropdown for unregistered |
| Export statistics to CSV | Click "Export CSV" button | Download CSV file with faculty statistics |

**Feedback Collection:**
- Usability survey (1-5 scale)
- Bug reports (severity: critical/high/medium/low)
- Feature requests

---

## 4. Deployment Plan

### 4.1 Pre-Deployment Checklist

- [ ] Phase 1 migration validated (all depositor accounts have faculty_id)
- [ ] Phase 2 migration completed (≥85% authors have faculty_id)
- [ ] All unit tests passing (≥80% coverage)
- [ ] All integration tests passing
- [ ] Performance tests meet targets
- [ ] UAT feedback reviewed and critical issues resolved
- [ ] Staging environment tested end-to-end
- [ ] Backup of production RDF store created
- [ ] Rollback procedure documented and tested
- [ ] Deployment checklist reviewed with team
- [ ] Support team trained on Phase 2 features

### 4.2 Deployment Steps

**Timing:** Saturday 2:00 AM - 6:00 AM (off-peak hours)

**Team:** 2 developers + 1 DevOps

| Step | Time | Action | Responsible |
|------|------|--------|-------------|
| 1 | 02:00 | Create production backup | DevOps |
| 2 | 02:15 | Put system in maintenance mode | DevOps |
| 3 | 02:20 | Deploy RDF schema updates | Dev 1 |
| 4 | 02:30 | Deploy code changes (API, UI) | Dev 1 + Dev 2 |
| 5 | 02:45 | Run database migrations (if any) | Dev 1 |
| 6 | 03:00 | Restart Virtuoso RDF store | DevOps |
| 7 | 03:10 | Restart web application | DevOps |
| 8 | 03:20 | Smoke tests (critical paths) | Dev 2 |
| 9 | 03:40 | Verify statistics generation | Dev 1 |
| 10 | 04:00 | End maintenance mode | DevOps |
| 11 | 04:10 | Monitor logs for errors | All |
| 12 | 05:00 | Final verification | Dev 1 + Dev 2 |

### 4.3 Rollback Procedure

**If critical issues detected:**

1. Put system in maintenance mode
2. Restore RDF store backup from Step 1
3. Revert code deployment
4. Restart services
5. Verify system functionality
6. End maintenance mode
7. Post-mortem analysis

**Rollback Time:** ~30 minutes

---

## 5. Success Criteria

### 5.1 Technical Metrics

| Metric | Target | Measurement | Status |
|--------|--------|-------------|--------|
| Author migration coverage | ≥85% | Authors with faculty_id / Total TU Delft authors | |
| Migration accuracy | ≥80% | Manual validation sample (50 authors) | |
| High confidence ratio | ≥70% | Authors with confidence ≥0.8 / Total migrated | |
| API response time | <150ms | Average for GET endpoints | |
| Statistics query performance | <200ms | Average with caching | |
| Test coverage | ≥80% | pytest --cov report | |
| Zero regressions | 0 | Phase 1 functionality still works | |

### 5.2 User Metrics

| Metric | Target | Measurement | Timeline |
|--------|--------|-------------|----------|
| Faculty statistics page views | ≥100/month | Analytics tracking | Month 1-3 |
| Collaboration dashboard usage | ≥50/month | Analytics tracking | Month 1-3 |
| CSV exports | ≥20/month | API logs | Month 1-3 |
| New datasets with author faculty | ≥70% | Datasets created after deployment | Month 1-3 |
| User satisfaction | ≥4.0/5.0 | UAT survey + post-launch survey | Month 3 |

### 5.3 Business Metrics

| Metric | Target | Measurement | Timeline |
|--------|--------|-------------|----------|
| Multi-faculty collaborations identified | ≥100 | SPARQL query | Month 1 |
| Faculty research profiles complete | 8/8 | All TU Delft faculties with ≥10 datasets | Month 3 |
| 4TU institution expansion | 2/4 | Extend to UT and TU/e | Month 6-12 |

---

## 6. Risks & Mitigation

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| **Organizations parsing accuracy <80%** | High | High | - Extensive pattern library<br>- Manual review for low confidence<br>- Continuous pattern refinement | - Lower threshold to 75%<br>- Allocate more manual review resources |
| **Performance degradation** | Medium | High | - Aggressive caching<br>- Virtuoso indexing<br>- Query optimization | - Add materialized views<br>- Scale Virtuoso infrastructure |
| **User confusion about double-counting** | High | Medium | - Clear UI labels ("Deposited" vs "Authored")<br>- Help text and documentation<br>- Training sessions | - Default to Phase 1 view<br>- Add toggle to switch views |
| **External authors incorrectly assigned faculty** | Low | High | - Validation: faculty.institution_id must match author.institution_id<br>- Automated integrity checks | - Run cleanup script<br>- Manual review of external authors |
| **Deployment failure** | Low | Critical | - Thorough staging testing<br>- Pre-deployment checklist<br>- Backup before deployment | - Immediate rollback<br>- Root cause analysis<br>- Reschedule deployment |
| **SPARQL injection vulnerability** | Low | Critical | - Input validation<br>- Parameterized queries<br>- Security review | - Emergency patch<br>- Security audit |

---

## 7. Post-Deployment Monitoring

### 7.1 Week 1 Monitoring

**Daily Checks:**

- [ ] Error rate in logs (<0.1% of requests)
- [ ] API response times (meet targets)
- [ ] Cache hit rate (≥80% for statistics)
- [ ] Database connection pool (no leaks)
- [ ] User-reported issues (Slack/email)

**Metrics Dashboard:**
```
+----------------------------------+
| Phase 2 Health Dashboard         |
+----------------------------------+
| API Requests (24h): 1,234        |
| Average Response Time: 87ms      |
| Error Rate: 0.03%                |
| Cache Hit Rate: 84%              |
|                                  |
| Faculty Statistics Views: 45     |
| Collaboration Dashboard: 12      |
| CSV Exports: 8                   |
+----------------------------------+
```

### 7.2 Month 1 Review

**Review Meeting Agenda:**

1. **Metrics Review**
   - Technical metrics vs targets
   - User engagement metrics
   - Business impact

2. **User Feedback**
   - UAT survey results
   - Support tickets summary
   - Feature requests

3. **Issues & Resolutions**
   - Bugs fixed
   - Performance optimizations
   - Data quality improvements

4. **Next Steps**
   - Pattern refinement (if accuracy <80%)
   - Additional manual review
   - UI/UX improvements

---

## 8. Documentation & Training

### 8.1 Documentation Updates

| Document | Updates Needed | Owner |
|----------|----------------|-------|
| User Guide | Add Phase 2 statistics sections | Dev 1 |
| API Documentation | Document 6 new endpoints | Dev 2 |
| Admin Guide | Add migration instructions | Dev 1 |
| Developer Guide | Explain author-faculty data model | Dev 2 |
| FAQ | Add Phase 1 vs Phase 2 comparison | Product Owner |

### 8.2 Training Sessions

**Session 1: For Institutional Users (1 hour)**
- Overview of Phase 2 features
- How to interpret authored vs deposited statistics
- Using the collaboration dashboard
- Exporting statistics to CSV

**Session 2: For Repository Administrators (2 hours)**
- Phase 2 data model
- Manual review workflow
- Author faculty assignment
- Troubleshooting common issues

---

## Summary

**Phase 2 Implementation:**
- **Duration:** 10 weeks
- **Team:** 2 developers + 2 reviewers
- **Deliverables:** 
  - ~950 authors migrated
  - 6 API endpoints
  - 3 UI components
  - Complete test suite
  - Updated documentation

**Key Milestones:**
- Week 2: Foundation complete
- Week 5: Migration complete (≥85% coverage)
- Week 7: API complete
- Week 9: UI complete
- Week 10: Deployed to production

**Success Criteria:** ≥85% author coverage, ≥80% accuracy, <200ms statistics queries

---

**This completes the Phase 2 Solution Architecture documentation.**

**Full Document Set:**
1. PHASE2_OVERVIEW.md - Executive summary
2. PHASE2_DATA_MODEL.md - RDF schema extensions
3. PHASE2_MIGRATION.md - Author migration strategy
4. PHASE2_STATISTICS.md - Multi-valued queries
5. PHASE2_API_UI.md - Endpoints and interfaces
6. PHASE2_IMPLEMENTATION.md - Timeline and testing ← YOU ARE HERE

**Return to:** PHASE2_OVERVIEW.md to review all documents
