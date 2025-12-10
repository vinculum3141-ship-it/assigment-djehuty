# Risk Register - Faculty Statistics Feature

**Document Version:** 1.0  
**Date:** December 10, 2024  
**Status:** Active  
**Owner:** Project Team  
**Review Frequency:** Monthly during implementation, Quarterly after launch

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Risk Assessment Framework](#risk-assessment-framework)
3. [Technical Risks](#technical-risks)
4. [Data Risks](#data-risks)
5. [Operational Risks](#operational-risks)
6. [Project Risks](#project-risks)
7. [Assumptions Log](#assumptions-log)
8. [Mitigation Tracking](#mitigation-tracking)

---

## 1. Executive Summary

### Purpose

This document consolidates all identified risks, assumptions, and mitigation strategies for the faculty-level statistics feature. It serves as a central reference for risk management throughout the project lifecycle.

### Risk Summary Dashboard

**Total Risks Identified:** 24  
**By Priority:**
- 🔴 **Critical (P0):** 3 risks
- 🟠 **High (P1):** 8 risks
- 🟡 **Medium (P2):** 9 risks
- 🟢 **Low (P3):** 4 risks

**By Status:**
- ⚠️ **Active:** 20 risks (need mitigation)
- ✅ **Mitigated:** 4 risks (mitigation in place)
- 📊 **Accepted:** 0 risks (no action planned)

**Top 3 Risks to Monitor:**
1. **R-DATA-001**: Data quality - Inconsistent faculty assignments (P1, High impact)
2. **R-TECH-001**: Virtuoso RDF limitations - Performance issues (P1, High impact)
3. **R-OPS-002**: User adoption - Feature not used by stakeholders (P1, High impact)

---

## 2. Risk Assessment Framework

### 2.1 Probability Scale

| Level | Score | Likelihood | Description |
|-------|-------|------------|-------------|
| **Very Low** | 1 | <10% | Unlikely to occur |
| **Low** | 2 | 10-30% | Could happen but not expected |
| **Medium** | 3 | 30-60% | Might happen |
| **High** | 4 | 60-80% | Likely to occur |
| **Very High** | 5 | >80% | Almost certain to occur |

### 2.2 Impact Scale

| Level | Score | Impact | Description |
|-------|-------|--------|-------------|
| **Very Low** | 1 | Negligible | Minor inconvenience, no business impact |
| **Low** | 2 | Minor | Small delays, workarounds available |
| **Medium** | 3 | Moderate | Noticeable impact, requires effort to fix |
| **High** | 4 | Significant | Major disruption, affects stakeholders |
| **Very High** | 5 | Critical | Project failure, data loss, or compliance breach |

### 2.3 Risk Score Calculation

**Risk Score = Probability × Impact**

| Score Range | Priority | Action Required |
|-------------|----------|-----------------|
| 16-25 | 🔴 **P0 (Critical)** | Immediate mitigation required |
| 10-15 | 🟠 **P1 (High)** | Mitigation plan required |
| 5-9 | 🟡 **P2 (Medium)** | Monitor and prepare contingency |
| 1-4 | 🟢 **P3 (Low)** | Accept or monitor |

---

## 3. Technical Risks

### R-TECH-001: Virtuoso RDF Performance Limitations

| Attribute | Value |
|-----------|-------|
| **Category** | Technical / Performance |
| **Probability** | 4 (High) |
| **Impact** | 4 (Significant) |
| **Risk Score** | 16 🔴 **P0 (Critical)** |
| **Status** | ⚠️ Active |
| **Owner** | Backend Developer |

**Description:**  
Virtuoso may not efficiently support complex SPARQL queries needed for faculty statistics, especially with large datasets (10,000+ accounts). Performance degradation could make the feature unusable.

**Indicators:**
- Query response time > 5 seconds
- Database CPU usage > 80%
- Timeout errors in production

**Mitigation Strategy:**

1. **Phase 1 (Immediate):**
   - Benchmark SPARQL queries with production-scale data
   - Add SPARQL query caching (TTL: 1 hour)
   - Optimize queries (avoid OPTIONAL, use FILTER efficiently)
   - Create indexes on frequently queried predicates

2. **Phase 2 (If needed):**
   - Implement materialized views (pre-compute statistics nightly)
   - Add PostgreSQL caching layer for hot data
   - Use connection pooling to reduce overhead

3. **Contingency Plan:**
   - Fallback to Python-based aggregation (slower but reliable)
   - Add "Statistics are being calculated..." loading state
   - Schedule statistics refresh during off-peak hours

**Cost of Mitigation:** 1-2 weeks development time

**Residual Risk After Mitigation:** 6 (2×3 = Medium)

---

### R-TECH-002: SPARQL Injection Vulnerabilities

| Attribute | Value |
|-----------|-------|
| **Category** | Technical / Security |
| **Probability** | 3 (Medium) |
| **Impact** | 5 (Critical - data breach) |
| **Risk Score** | 15 🟠 **P1 (High)** |
| **Status** | ✅ Mitigated |
| **Owner** | Backend Developer |

**Description:**  
If user inputs (e.g., faculty IDs, account UUIDs) are concatenated into SPARQL queries, attackers could inject malicious SPARQL to access unauthorized data.

**Example Attack:**
```sparql
# If faculty_id comes from user input:
SELECT * WHERE { ?s djht:faculty_id 1; DROP ALL }
```

**Mitigation Strategy:**

1. ✅ **Use parameterized queries** (RDFLib's `prepareQuery` with `initBindings`)
2. ✅ **Validate all inputs** (UUIDs must match regex, faculty IDs must be integers)
3. ✅ **Escape special characters** (if string inputs are allowed)
4. **Test with OWASP injection payloads** (during security audit)

**Status:** Mitigated in prototype, must verify in production code.

**Residual Risk After Mitigation:** 3 (1×3 = Low)

---

### R-TECH-003: RDF Schema Evolution Breaking Changes

| Attribute | Value |
|-----------|-------|
| **Category** | Technical / Data Model |
| **Probability** | 3 (Medium) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 9 🟡 **P2 (Medium)** |
| **Status** | ⚠️ Active |
| **Owner** | Architect |

**Description:**  
If the RDF schema changes (e.g., `djht:faculty_id` renamed to `djht:faculty`), existing SPARQL queries will break.

**Mitigation Strategy:**

1. **Version the RDF schema** (use named graphs for different versions)
2. **Create schema migration scripts** (update triples when schema changes)
3. **Add schema validation tests** (detect breaking changes early)
4. **Document schema in formal spec** (OWL ontology or SHACL shapes)
5. **Deprecation policy:** Support old schema for 12 months before removal

**Contingency Plan:**
- Keep backward-compatible predicates (e.g., support both `djht:faculty_id` and `djht:faculty`)
- Add schema migration tool to convert old data

**Residual Risk After Mitigation:** 4 (2×2 = Low)

---

### R-TECH-004: Prototype Code Not Production-Ready

| Attribute | Value |
|-----------|-------|
| **Category** | Technical / Code Quality |
| **Probability** | 5 (Very High - known issue) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 15 🟠 **P1 (High)** |
| **Status** | ⚠️ Active |
| **Owner** | Development Team |

**Description:**  
The prototype was built for demonstration, not production. It lacks error handling, edge case coverage, logging, and performance optimization.

**Known Issues:**
- No exception handling in some functions
- No retry logic for database failures
- No rate limiting
- No authentication/authorization
- Hardcoded values (e.g., file paths)

**Mitigation Strategy:**

**Phase 1: Code Hardening (2-3 weeks)**
1. Add comprehensive error handling (try/except with logging)
2. Add input validation to all endpoints
3. Remove hardcoded values → configuration
4. Add retry logic for database operations
5. Implement logging (application + audit logs)
6. Code review by senior developer

**Phase 2: Production Readiness (1-2 weeks)**
1. Add authentication/authorization (see SECURITY_AND_AUDIT.md)
2. Performance testing with production-scale data
3. Load testing (simulate 100 concurrent users)
4. Security audit (penetration testing)

**Acceptance Criteria for Production:**
- [ ] All endpoints have error handling
- [ ] All endpoints have input validation
- [ ] Code coverage ≥ 80%
- [ ] Load test: 100 concurrent users, <2s response time
- [ ] Security audit: No P0 or P1 vulnerabilities
- [ ] Code review approved

**Cost:** 3-5 weeks total development time

**Residual Risk After Mitigation:** 6 (2×3 = Medium)

---

### R-TECH-005: External Dependencies Unavailable

| Attribute | Value |
|-----------|-------|
| **Category** | Technical / Dependencies |
| **Probability** | 2 (Low) |
| **Impact** | 4 (Significant) |
| **Risk Score** | 8 🟡 **P2 (Medium)** |
| **Status** | ⚠️ Active |
| **Owner** | DevOps |

**Description:**  
If external dependencies (e.g., Virtuoso SPARQL endpoint, PyPI packages) become unavailable, the feature breaks.

**Dependencies:**
- Virtuoso SPARQL endpoint (critical)
- RDFLib (critical)
- Flask/FastAPI (critical)
- Plotly (for dashboards)
- Python packages from PyPI

**Mitigation Strategy:**

1. **Vendor lock-in mitigation:**
   - Use standard SPARQL (not Virtuoso-specific extensions)
   - Abstract database layer (easily swap Virtuoso for Blazegraph, etc.)

2. **Dependency management:**
   - Pin dependency versions in `requirements.txt`
   - Use private PyPI mirror (Artifactory, Nexus)
   - Regularly update dependencies (monthly security patches)

3. **Fallback mechanisms:**
   - If SPARQL endpoint down, fallback to cached statistics
   - If Plotly unavailable, fallback to simple table view

**Contingency Plan:**
- Keep Docker images with all dependencies pre-installed
- Have offline package archive for critical packages

**Residual Risk After Mitigation:** 3 (1.5×2 ≈ Low)

---

### R-TECH-006: Browser Compatibility Issues

| Attribute | Value |
|-----------|-------|
| **Category** | Technical / Frontend |
| **Probability** | 3 (Medium) |
| **Impact** | 2 (Minor) |
| **Risk Score** | 6 🟡 **P2 (Medium)** |
| **Status** | ⚠️ Active |
| **Owner** | Frontend Developer |

**Description:**  
The visual dashboard (HTML + Plotly.js) may not render correctly in older browsers (e.g., IE11, old Safari).

**Mitigation Strategy:**

1. **Test on target browsers:**
   - Chrome (latest)
   - Firefox (latest)
   - Safari (latest)
   - Edge (latest)

2. **Graceful degradation:**
   - Detect unsupported browsers, show warning
   - Provide fallback (plain table view without charts)

3. **Browser requirements:**
   - Document minimum browser versions
   - Add browser check to dashboard

**Contingency Plan:**
If dashboard doesn't work, users can still access JSON API.

**Residual Risk After Mitigation:** 2 (1×2 = Low)

---

## 4. Data Risks

### R-DATA-001: Inconsistent Faculty Assignments

| Attribute | Value |
|-----------|-------|
| **Category** | Data / Data Quality |
| **Probability** | 5 (Very High - known issue) |
| **Impact** | 4 (Significant) |
| **Risk Score** | 20 🔴 **P0 (Critical)** |
| **Status** | ⚠️ Active |
| **Owner** | Data Steward |

**Description:**  
Existing accounts may have:
- Missing faculty assignments (`faculty_id = NULL`)
- Incorrect faculty assignments (user moved departments, not updated)
- Multiple faculty assignments (user affiliated with multiple faculties)
- Retired faculties (faculty no longer exists)

**Impact on Statistics:**
- "Other" category inflated due to NULL values
- Statistics don't reflect reality
- Stakeholders lose trust in data

**Mitigation Strategy:**

**Phase 1: Data Audit (1 week)**
1. Query all accounts to find data quality issues:
   ```sql
   SELECT 
     COUNT(*) FILTER (WHERE faculty_id IS NULL) AS missing_faculty,
     COUNT(*) FILTER (WHERE faculty_id NOT IN (SELECT id FROM faculties)) AS invalid_faculty,
     COUNT(*) FILTER (WHERE updated_at < NOW() - INTERVAL '2 years') AS stale_faculty
   FROM accounts;
   ```

2. Report findings to stakeholders

**Phase 2: Data Cleanup (2-4 weeks)**
1. **Missing faculty assignments:**
   - Contact users to select their faculty
   - Use heuristics (email domain → faculty)
   - Assign to "Other" if no response

2. **Incorrect faculty assignments:**
   - Send bulk email: "Please verify your faculty"
   - Provide self-service update interface
   - Data stewards review and approve changes

3. **Retired faculties:**
   - Migrate users to successor faculty (e.g., "Old IT Faculty" → "EEMCS")
   - Document mapping in configuration

**Phase 3: Ongoing Data Quality (Post-launch)**
1. **Validation at account creation:**
   - Require faculty selection during signup
   - Validate faculty_id exists

2. **Periodic reminders:**
   - Annual email: "Please verify your faculty"
   - Show reminder banner if faculty not updated in 2 years

3. **Data quality dashboard:**
   - Track % accounts with faculty assigned
   - Alert if % drops below threshold (e.g., 90%)

**Acceptance Criteria for Launch:**
- [ ] ≥90% accounts have valid faculty assignments
- [ ] Data quality report approved by stakeholders
- [ ] Data stewards trained on cleanup process

**Cost:** 3-5 weeks (1 week audit + 2-4 weeks cleanup)

**Residual Risk After Mitigation:** 8 (2×4 = Medium)

---

### R-DATA-002: Faculty Organizational Changes

| Attribute | Value |
|-----------|-------|
| **Category** | Data / Organizational Change |
| **Probability** | 3 (Medium - happens occasionally) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 9 🟡 **P2 (Medium)** |
| **Status** | ⚠️ Active |
| **Owner** | Repository Manager |

**Description:**  
Universities reorganize faculties (merge, split, rename). If not handled, historical statistics become meaningless.

**Examples:**
- Faculty A + Faculty B → New Faculty C (merger)
- Faculty D → Faculty E + Faculty F (split)
- Faculty G → Faculty G' (renamed)

**Mitigation Strategy:**

1. **Version faculties in RDF:**
   ```sparql
   <faculty/1> a djht:Faculty ;
     djht:name "Faculty of Aerospace Engineering" ;
     djht:valid_from "2000-01-01"^^xsd:date ;
     djht:valid_until "2025-12-31"^^xsd:date .
   
   <faculty/10> a djht:Faculty ;
     djht:name "Faculty of Engineering" ;
     djht:valid_from "2026-01-01"^^xsd:date ;
     djht:successor_of <faculty/1>, <faculty/2> .
   ```

2. **Historical statistics handling:**
   - **Option 1: Rewrite history** (adjust old datasets to new faculty)
   - **Option 2: Keep history as-is** (show "Faculty A (archived)")
   - **Recommended: Hybrid** (show both old and new faculty, with note)

3. **Change management process:**
   - Data steward notified of organizational changes
   - Migration plan created (map old → new faculty)
   - Users notified of changes
   - Statistics updated with explanation

**Contingency Plan:**
Add "Faculty history" view that shows statistics over time with organizational changes marked.

**Residual Risk After Mitigation:** 4 (2×2 = Low)

---

### R-DATA-003: Personal Data Compliance (GDPR)

| Attribute | Value |
|-----------|-------|
| **Category** | Data / Compliance |
| **Probability** | 4 (High - regulatory requirement) |
| **Impact** | 5 (Critical - fines, reputational damage) |
| **Risk Score** | 20 🔴 **P0 (Critical)** |
| **Status** | ✅ Mitigated (documented) |
| **Owner** | Data Protection Officer |

**Description:**  
Faculty assignments are personal data under GDPR. Non-compliance could result in:
- Fines (up to €20M or 4% of revenue)
- Reputational damage
- User trust loss
- Legal action

**GDPR Requirements:**
- Lawful basis for processing
- User consent (if required)
- User rights (access, rectification, erasure)
- Privacy notice
- Data retention policy
- Privacy Impact Assessment

**Mitigation Strategy:**

✅ **All requirements documented in SECURITY_AND_AUDIT.md**

Key Mitigations:
1. ✅ Lawful basis: Legitimate interest (institutional need)
2. ✅ User rights: All GDPR rights implemented (see Section 4)
3. ✅ Privacy notice: User-facing documentation
4. ✅ Privacy Impact Assessment: To be conducted before launch
5. ✅ Data retention: 7 years for audit logs, then deleted
6. ✅ Audit trail: All data changes logged

**Action Required Before Launch:**
- [ ] Privacy Impact Assessment approved by DPO
- [ ] Legal review of privacy notice
- [ ] GDPR compliance sign-off

**Cost:** 1-2 weeks (PIA + legal review)

**Residual Risk After Mitigation:** 4 (1×4 = Low - compliant but must maintain)

---

### R-DATA-004: Data Loss or Corruption

| Attribute | Value |
|-----------|-------|
| **Category** | Data / Integrity |
| **Probability** | 2 (Low) |
| **Impact** | 5 (Critical) |
| **Risk Score** | 10 🟠 **P1 (High)** |
| **Status** | ⚠️ Active |
| **Owner** | DevOps |

**Description:**  
Hardware failure, software bug, or human error could corrupt or delete faculty assignments.

**Scenarios:**
- Database corruption
- Accidental DELETE query
- Ransomware attack
- Hardware failure (disk crash)

**Mitigation Strategy:**

1. **Backups (Prevention):**
   - Daily automated backups (RDF database)
   - Offsite backup storage (AWS S3, Azure Blob)
   - Encrypted backups (GPG)
   - Test restores monthly

2. **Data integrity checks:**
   - Database constraints (foreign keys, NOT NULL)
   - Checksum validation
   - Periodic integrity audits

3. **Disaster recovery:**
   - Recovery Time Objective (RTO): 4 hours
   - Recovery Point Objective (RPO): 24 hours (daily backups)
   - Documented recovery procedure
   - Quarterly disaster recovery drills

4. **Audit trail for recovery:**
   - If data corrupted, restore from audit logs
   - Replay transactions to rebuild state

**Acceptance Criteria:**
- [ ] Daily backups configured
- [ ] Backup restore tested successfully
- [ ] Disaster recovery procedure documented
- [ ] Recovery drill conducted

**Cost:** 1 week setup + ongoing monitoring

**Residual Risk After Mitigation:** 2 (1×2 = Low)

---

### R-DATA-005: Data Inconsistency Between Systems

| Attribute | Value |
|-----------|-------|
| **Category** | Data / Integration |
| **Probability** | 3 (Medium) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 9 🟡 **P2 (Medium)** |
| **Status** | ⚠️ Active |
| **Owner** | Data Architect |

**Description:**  
If faculty data exists in multiple systems (RDF database, PostgreSQL, LDAP, HR system), they may become out of sync.

**Example:**
- User updates faculty in RDF database
- HR system still shows old faculty
- Statistics don't match HR reports

**Mitigation Strategy:**

1. **Single source of truth:**
   - RDF database is authoritative for faculty assignments
   - Other systems sync FROM RDF (not bidirectional)

2. **Data synchronization:**
   - Scheduled sync jobs (e.g., nightly export to PostgreSQL)
   - Event-driven sync (webhook when faculty changes)
   - Validate sync success (row counts, checksums)

3. **Conflict resolution:**
   - If conflict detected, flag for manual review
   - Data steward resolves conflicts
   - Document resolution in audit log

4. **Monitoring:**
   - Alert if sync fails
   - Dashboard showing sync status

**Contingency Plan:**
If sync fails, provide manual export/import tools.

**Residual Risk After Mitigation:** 4 (2×2 = Low)

---

## 5. Operational Risks

### R-OPS-001: Insufficient Developer Capacity

| Attribute | Value |
|-----------|-------|
| **Category** | Operational / Resources |
| **Probability** | 4 (High - known constraint) |
| **Impact** | 3 (Moderate - delays) |
| **Risk Score** | 12 🟠 **P1 (High)** |
| **Status** | ⚠️ Active |
| **Owner** | Project Manager |

**Description:**  
The Djehuty development team has limited capacity (likely 1-2 developers). Faculty statistics is one of many priorities. Insufficient capacity could delay implementation.

**Mitigation Strategy:**

1. **Phased delivery:**
   - Phase 1: Minimum viable feature (basic statistics)
   - Phase 2: Enhancements (advanced visualizations, etc.)
   - Don't try to do everything at once

2. **Leverage existing code:**
   - Reuse existing Djehuty components (authentication, API framework)
   - Use well-tested libraries (RDFLib, Plotly)
   - Prototype accelerates development (70% done)

3. **Clear prioritization:**
   - Product owner prioritizes features
   - Say NO to scope creep
   - Focus on P0 and P1 requirements only

4. **External help (if needed):**
   - Hire contractor for specific tasks (e.g., frontend)
   - Intern/student project
   - Vendor support (Virtuoso consultant)

**Acceptance Criteria:**
- [ ] Realistic timeline agreed by team
- [ ] Buffer time included (20% contingency)
- [ ] Team committed and trained

**Cost:** No additional cost if timeline is realistic

**Residual Risk After Mitigation:** 6 (3×2 = Medium)

---

### R-OPS-002: Low User Adoption

| Attribute | Value |
|-----------|-------|
| **Category** | Operational / User Adoption |
| **Probability** | 4 (High - new feature, unknown demand) |
| **Impact** | 4 (Significant - wasted effort) |
| **Risk Score** | 16 🔴 **P0 (Critical)** |
| **Status** | ⚠️ Active |
| **Owner** | Product Owner |

**Description:**  
If stakeholders don't use the faculty statistics feature, the development effort is wasted. Reasons for low adoption:
- Feature doesn't meet needs
- UI too complex
- Data quality too poor
- Not aware feature exists

**Mitigation Strategy:**

**Phase 1: Validate Demand (Before Development)**
1. ✅ Stakeholder interviews (done - Gabriela provided feedback)
2. ✅ Prototype demonstration (done - validates concept)
3. User research: Survey faculty deans/research managers
4. Competitive analysis: How do other repositories handle this?

**Phase 2: User-Centered Design**
1. Involve users in design (show mockups, get feedback)
2. Iterative development (release MVP, gather feedback, improve)
3. Usability testing (watch users use the feature)

**Phase 3: Launch & Promotion**
1. **Communication plan:**
   - Email announcement to stakeholders
   - Blog post / news article
   - Demo video
   - User guide / FAQ

2. **Training:**
   - Webinar for faculty deans
   - Office hours (support sessions)
   - Documentation

3. **Feedback loop:**
   - User feedback form
   - Monthly usage analytics
   - User interviews (post-launch)

**Phase 4: Measure Success**
- Track usage (API calls, dashboard views)
- Survey satisfaction (NPS score)
- Collect testimonials

**Acceptance Criteria:**
- [ ] ≥5 stakeholders confirmed they will use feature
- [ ] Communication plan executed
- [ ] Usage tracked and reported

**Cost:** 1-2 weeks communication + training

**Residual Risk After Mitigation:** 6 (3×2 = Medium)

---

### R-OPS-003: Unclear Requirements

| Attribute | Value |
|-----------|-------|
| **Category** | Operational / Requirements |
| **Probability** | 3 (Medium) |
| **Impact** | 3 (Moderate - rework) |
| **Risk Score** | 9 🟡 **P2 (Medium)** |
| **Status** | ✅ Mitigated |
| **Owner** | Product Owner |

**Description:**  
Ambiguous requirements lead to building the wrong feature, requiring costly rework.

**Examples of Ambiguity:**
- "Faculty-level statistics" - which statistics exactly?
- "Dashboard" - what charts, what filters?
- "Update faculty" - who can update, what validation?

**Mitigation Strategy:**

1. ✅ **Detailed requirements document** (PHASE1_FOCUS.md, etc.)
2. ✅ **Prototype** demonstrates exact functionality
3. ✅ **User stories** with acceptance criteria
4. **Mockups/wireframes** for UI features
5. **Review cycles:** Stakeholder reviews requirements before coding

**Status:** Requirements well-documented. Low risk now.

**Residual Risk After Mitigation:** 3 (1×3 = Low)

---

### R-OPS-004: Knowledge Silos / Bus Factor

| Attribute | Value |
|-----------|-------|
| **Category** | Operational / Knowledge Management |
| **Probability** | 4 (High - small team) |
| **Impact** | 4 (Significant) |
| **Risk Score** | 16 🔴 **P0 (Critical)** |
| **Status** | ⚠️ Active |
| **Owner** | Team Lead |

**Description:**  
If only one person understands the faculty statistics implementation ("bus factor = 1"), their departure or unavailability cripples maintenance.

**Mitigation Strategy:**

1. **Documentation:**
   - ✅ Comprehensive design documents (46 files!)
   - Code comments (docstrings for all functions)
   - README with setup instructions
   - Architecture decision records (ADRs)

2. **Knowledge sharing:**
   - Pair programming (two developers work together)
   - Code reviews (all code reviewed by peer)
   - Brown bag sessions (team presents to each other)
   - "Lunch and learn" demos

3. **Cross-training:**
   - Rotate tasks (don't let one person "own" a component)
   - Shadow senior developers
   - Onboarding documentation for new team members

4. **External knowledge:**
   - Open source similar projects (learn from them)
   - Vendor support (Virtuoso, RDFLib communities)

**Acceptance Criteria:**
- [ ] ≥2 developers can explain architecture
- [ ] ≥2 developers have contributed code
- [ ] Documentation complete and up-to-date

**Cost:** Ongoing (part of normal development process)

**Residual Risk After Mitigation:** 6 (2×3 = Medium)

---

### R-OPS-005: Inadequate Testing

| Attribute | Value |
|-----------|-------|
| **Category** | Operational / Quality Assurance |
| **Probability** | 3 (Medium) |
| **Impact** | 4 (Significant - bugs in production) |
| **Risk Score** | 12 🟠 **P1 (High)** |
| **Status** | ⚠️ Active |
| **Owner** | QA / Development Team |

**Description:**  
Without comprehensive testing, bugs reach production, causing:
- Data errors (wrong statistics)
- Security vulnerabilities
- System crashes
- User frustration

**Mitigation Strategy:**

**Testing Pyramid:**

```
         /\
        /  \  E2E Tests (10%)
       /    \  - Full user workflows
      /------\
     /        \ Integration Tests (30%)
    /          \ - API tests, database tests
   /------------\
  /              \ Unit Tests (60%)
 /                \ - Function-level tests
/------------------\
```

**Test Strategy:**

1. **Unit Tests (60% of tests):**
   - Test individual functions
   - Mock external dependencies
   - Target: ≥80% code coverage
   - ✅ Prototype has 5/5 tests passing

2. **Integration Tests (30%):**
   - Test API endpoints end-to-end
   - Test database interactions
   - Test SPARQL query execution
   - Test error handling

3. **End-to-End Tests (10%):**
   - Test full user workflows (Selenium, Playwright)
   - Test dashboard rendering
   - Test authentication flows

4. **Performance Tests:**
   - Load testing (100 concurrent users)
   - Stress testing (find breaking point)
   - Benchmarking (query response times)

5. **Security Tests:**
   - OWASP Top 10 testing
   - Penetration testing
   - SQL/SPARQL injection tests

**Test Automation:**
- Tests run on every commit (CI/CD)
- Automated test reporting
- Fail build if tests fail

**Acceptance Criteria:**
- [ ] Code coverage ≥80%
- [ ] All critical paths have E2E tests
- [ ] Load test: 100 users, <2s response
- [ ] Security audit passed

**Cost:** 2-3 weeks testing effort

**Residual Risk After Mitigation:** 4 (2×2 = Low)

---

### R-OPS-006: Deployment Failures

| Attribute | Value |
|-----------|-------|
| **Category** | Operational / Deployment |
| **Probability** | 3 (Medium) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 9 🟡 **P2 (Medium)** |
| **Status** | ⚠️ Active |
| **Owner** | DevOps |

**Description:**  
Deployment to production fails, causing downtime or rollback.

**Common Causes:**
- Configuration differences (dev vs. prod)
- Missing dependencies
- Database migration failures
- Network issues

**Mitigation Strategy:**

1. **Infrastructure as Code:**
   - Docker containers (consistent environment)
   - Docker Compose / Kubernetes (orchestration)
   - Ansible/Terraform (infrastructure automation)

2. **Staging environment:**
   - Test deployment in staging first
   - Staging mirrors production exactly
   - Smoke tests in staging before prod

3. **Deployment checklist:**
   - [ ] Backup database before deployment
   - [ ] Run database migrations (test in staging)
   - [ ] Deploy to staging, run smoke tests
   - [ ] Deploy to production during maintenance window
   - [ ] Monitor logs for errors (30 minutes post-deploy)
   - [ ] Rollback plan ready

4. **Blue-green deployment:**
   - Deploy to "green" environment (parallel to "blue")
   - Switch traffic to "green" when ready
   - If issues, switch back to "blue" (instant rollback)

5. **Canary deployment:**
   - Deploy to 10% of users first
   - Monitor for errors
   - Gradually roll out to 100%

**Acceptance Criteria:**
- [ ] Deployment procedure documented
- [ ] Rollback procedure tested
- [ ] Staging environment available

**Cost:** 1 week setup

**Residual Risk After Mitigation:** 3 (1×3 = Low)

---

## 6. Project Risks

### R-PROJ-001: Timeline Pressure / Unrealistic Deadlines

| Attribute | Value |
|-----------|-------|
| **Category** | Project / Schedule |
| **Probability** | 4 (High - common in projects) |
| **Impact** | 3 (Moderate - quality suffers) |
| **Risk Score** | 12 🟠 **P1 (High)** |
| **Status** | ⚠️ Active |
| **Owner** | Project Manager |

**Description:**  
Pressure to deliver quickly may lead to:
- Skipping tests
- Cutting corners on security
- Inadequate documentation
- Technical debt

**Mitigation Strategy:**

1. **Realistic estimation:**
   - Use evidence-based estimates (prototype took X days, production will take ~3X)
   - Include buffer (20% contingency)
   - Be transparent about unknowns

2. **Prioritization:**
   - **Must-have (P0):** Basic statistics, authentication, audit logs
   - **Should-have (P1):** Dashboard, advanced filters
   - **Nice-to-have (P2):** Complex visualizations, export features

3. **Push back on unrealistic deadlines:**
   - Explain trade-offs: "We can deliver fast OR secure, not both"
   - Show data: "Similar features took X weeks elsewhere"
   - Propose phased delivery: "MVP in 4 weeks, full version in 8 weeks"

4. **Communicate early and often:**
   - Weekly status updates
   - Flag risks immediately (don't wait until deadline)
   - Adjust plan as needed

**Acceptance Criteria:**
- [ ] Timeline agreed by team and stakeholders
- [ ] Scope prioritized (P0/P1/P2)
- [ ] Buffer time included

**Residual Risk After Mitigation:** 6 (3×2 = Medium)

---

### R-PROJ-002: Scope Creep

| Attribute | Value |
|-----------|-------|
| **Category** | Project / Scope |
| **Probability** | 4 (High - common in projects) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 12 🟠 **P1 (High)** |
| **Status** | ⚠️ Active |
| **Owner** | Product Owner |

**Description:**  
Stakeholders request additional features mid-project, causing delays and budget overruns.

**Examples:**
- "Can we also show statistics by department, not just faculty?"
- "Can we add pie charts?"
- "Can we export to Excel?"

**Mitigation Strategy:**

1. **Clear scope definition:**
   - ✅ Requirements documented
   - ✅ Acceptance criteria defined
   - Sign-off from stakeholders

2. **Change control process:**
   - New requests logged in backlog
   - Impact assessment (time, cost)
   - Stakeholder decides: "Add to scope (delay launch) or defer to Phase 2?"

3. **Say NO (politely):**
   - "Great idea! Let's add it to Phase 2."
   - "That's out of scope for this release."
   - Explain trade-offs: "If we add this, we'll delay by 2 weeks."

4. **Backlog grooming:**
   - Review requests regularly
   - Prioritize for future releases

**Acceptance Criteria:**
- [ ] Scope baseline documented
- [ ] Change control process defined
- [ ] Stakeholders aware of scope

**Residual Risk After Mitigation:** 6 (3×2 = Medium)

---

### R-PROJ-003: Stakeholder Misalignment

| Attribute | Value |
|-----------|-------|
| **Category** | Project / Stakeholders |
| **Probability** | 3 (Medium) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 9 🟡 **P2 (Medium)** |
| **Status** | ⚠️ Active |
| **Owner** | Project Manager |

**Description:**  
Different stakeholders have conflicting expectations (e.g., faculty deans want detailed stats, privacy advocates want minimal data).

**Mitigation Strategy:**

1. **Stakeholder analysis:**
   - Identify all stakeholders
   - Understand their needs and concerns
   - Map power/interest (see STAKEHOLDER_ANALYSIS.md)

2. **Communication plan:**
   - Regular stakeholder meetings
   - Demos to show progress
   - Transparent about trade-offs

3. **Conflict resolution:**
   - Escalate conflicts to steering committee
   - Find win-win solutions
   - Document decisions

**Acceptance Criteria:**
- [ ] Stakeholder analysis complete
- [ ] Communication plan executed
- [ ] No unresolved conflicts

**Cost:** Ongoing (part of project management)

**Residual Risk After Mitigation:** 4 (2×2 = Low)

---

### R-PROJ-004: Loss of Executive Support

| Attribute | Value |
|-----------|-------|
| **Category** | Project / Sponsorship |
| **Probability** | 2 (Low) |
| **Impact** | 5 (Critical - project canceled) |
| **Risk Score** | 10 🟠 **P1 (High)** |
| **Status** | ⚠️ Active |
| **Owner** | Executive Sponsor |

**Description:**  
If executive sponsor loses interest or leaves, project may be deprioritized or canceled.

**Mitigation Strategy:**

1. **Demonstrate value early:**
   - ✅ Prototype shows quick wins
   - Show ROI (time saved, better decisions)
   - Collect testimonials from users

2. **Regular updates to executives:**
   - Monthly status report
   - Highlight achievements
   - Show usage metrics post-launch

3. **Build coalition:**
   - Multiple sponsors (not just one)
   - Support from different departments

**Acceptance Criteria:**
- [ ] Executive sponsor engaged
- [ ] Value proposition clear
- [ ] Stakeholder support documented

**Residual Risk After Mitigation:** 4 (2×2 = Low)

---

## 7. Assumptions Log

**Assumptions = Things we believe to be true but have not verified.**

| ID | Assumption | Impact if Wrong | Verification Method | Status |
|----|------------|-----------------|---------------------|--------|
| **A-001** | Djehuty already has an authentication system | Medium - need to build auth from scratch | Review Djehuty codebase | ⚠️ Not verified |
| **A-002** | Virtuoso SPARQL supports complex aggregations efficiently | High - may need fallback | Benchmark with production data | ⚠️ Not verified |
| **A-003** | Stakeholders will provide timely feedback | Medium - delays design | Schedule feedback sessions | ✅ Verified (Gabriela responded) |
| **A-004** | RDF schema will not change frequently | High - queries break often | Discuss with maintainers | ⚠️ Not verified |
| **A-005** | Faculty structure is stable (no major reorganizations imminent) | Medium - need to handle changes soon | Check with university admin | ⚠️ Not verified |
| **A-006** | Users will update their own faculty assignments | Medium - need data stewards to do it | User research | ⚠️ Not verified |
| **A-007** | Python 3.8+ is available in production | Low - easy to upgrade | Check production environment | ⚠️ Not verified |
| **A-008** | Sufficient server resources for Virtuoso + new feature | High - performance issues | Capacity planning | ⚠️ Not verified |
| **A-009** | Legal/DPO will approve GDPR approach | Critical - can't launch | Schedule PIA review | ⚠️ Not verified |
| **A-010** | Users access dashboard from modern browsers | Low - can provide fallback | Check analytics | ⚠️ Not verified |
| **A-011** | Existing API framework (Flask/FastAPI) can be reused | Low - can switch frameworks | Review codebase | ⚠️ Not verified |
| **A-012** | Faculty IDs are stable (won't be reassigned) | Medium - confusing statistics | Confirm with maintainers | ⚠️ Not verified |

**Action Required:**
- Verify assumptions marked ⚠️ before production launch
- Update risk register if assumptions are wrong

---

## 8. Mitigation Tracking

### 8.1 Mitigation Status Dashboard

| Risk ID | Priority | Mitigation Status | Owner | Due Date | Progress |
|---------|----------|-------------------|-------|----------|----------|
| R-TECH-001 | P0 | In Progress | Backend Dev | Week 2 | 30% - Benchmarking started |
| R-TECH-002 | P1 | ✅ Mitigated | Backend Dev | Completed | 100% - Parameterized queries |
| R-TECH-004 | P1 | Planned | Dev Team | Week 4-8 | 0% - Code hardening planned |
| R-DATA-001 | P0 | Planned | Data Steward | Week 1-5 | 0% - Data audit scheduled |
| R-DATA-003 | P0 | Documented | DPO | Week 1-2 | 80% - PIA in progress |
| R-DATA-004 | P1 | Planned | DevOps | Week 2 | 0% - Backup config pending |
| R-OPS-001 | P1 | Ongoing | PM | - | 50% - Timeline negotiated |
| R-OPS-002 | P0 | In Progress | Product Owner | Week 1-3 | 70% - Communication plan draft |
| R-OPS-004 | P0 | Ongoing | Team Lead | - | 40% - Documentation in progress |
| R-OPS-005 | P1 | Planned | QA | Week 5-7 | 0% - Test plan pending |
| R-PROJ-001 | P1 | Ongoing | PM | - | 60% - Realistic timeline set |
| R-PROJ-002 | P1 | Ongoing | Product Owner | - | 50% - Scope baseline defined |

### 8.2 Mitigation Effort Summary

**Total Effort for Critical Mitigations (P0):**
- R-DATA-001 (Data cleanup): 3-5 weeks
- R-DATA-003 (GDPR compliance): 1-2 weeks (PIA + legal review)
- R-OPS-002 (User adoption): 1-2 weeks (communication + training)
- R-OPS-004 (Knowledge management): Ongoing (documentation)

**Total: ~6-10 weeks** (can be parallelized)

**Timeline Impact:**
- If done sequentially: +10 weeks
- If done in parallel: +5 weeks (some dependencies)

**Recommendation:** Allocate 5-6 weeks for risk mitigation activities before production launch.

---

## Appendix A: Risk Heat Map

```
Impact
  5 |                    [R-DATA-003]    [R-DATA-004]
    |                    [R-OPS-004]
    |                       GDPR           Data Loss
  4 |  [R-DATA-001]     [R-TECH-001]    [R-OPS-001]
    |  Data Quality     Performance     Capacity
    |                    [R-OPS-002]
  3 |                    User Adoption  [R-TECH-003]
    |  [R-DATA-002]     [R-OPS-003]     [R-TECH-004]
    |  Org Changes      Requirements    Code Quality
  2 |  [R-TECH-006]     [R-DATA-005]    [R-OPS-006]
    |  Browser Compat   Data Sync       Deployment
  1 |
    +--------------------------------------------------
       1         2         3         4         5
                     Probability
```

**Legend:**
- 🔴 Red Zone (P0): Score 16-25 → Immediate action required
- 🟠 Orange Zone (P1): Score 10-15 → Mitigation plan required
- 🟡 Yellow Zone (P2): Score 5-9 → Monitor and prepare contingency
- 🟢 Green Zone (P3): Score 1-4 → Accept or monitor

---

## Appendix B: Risk Review Schedule

**Monthly Risk Review (During Implementation):**
- Review all active risks
- Update probability/impact if needed
- Check mitigation progress
- Identify new risks

**Quarterly Risk Review (Post-Launch):**
- Review risk register
- Archive closed risks
- Update mitigation strategies

**Ad-Hoc Review:**
- When new risks identified
- When assumptions are invalidated
- After incidents

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Dec 10, 2024 | Documentation Team | Initial risk register |

**Next Review:** Before Phase 1 kick-off (estimated Jan 2025)

**Approval Required From:**
- [ ] Project Manager
- [ ] Technical Lead
- [ ] Product Owner
- [ ] Executive Sponsor

---

**END OF DOCUMENT**
