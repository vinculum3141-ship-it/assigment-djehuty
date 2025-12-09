# Phase 1 Implementation Roadmap
## Faculty-Level Statistics for 4TU.ResearchData

**⚠️ ARCHIVED DOCUMENT - Version 1.0 (Original 5-Week Plan)**

**Archive Date:** December 9, 2024  
**Original Dates:** December 6-8, 2024  
**Reason for Archiving:** Partial implementation discovered - timeline reduced by 50%  
**Current Version:** See `/docs/assignment/IMPLEMENTATION_ROADMAP.md` (updated with 2.5-week timeline)  
**Context:** See `/docs/assignment/archive/README.md` for full explanation

---

## About This Archived Version

**Original Estimates (Build from Scratch):**
- **Duration:** 5 weeks (25 working days)  
- **Effort:** ~100 person-hours  
- **Approach:** Build institution infrastructure (2 weeks) + faculty infrastructure (2 weeks) + UI (1 week)

**Revised Estimates (Leverage Existing):**
- **Duration:** 2.5 weeks (12.5 working days) → **50% reduction**
- **Effort:** ~50 person-hours → **50% reduction**
- **Approach:** Wrap existing institution infrastructure (0.5 days) + faculty infrastructure (1.5 weeks) + UI (1 week)

**What Changed:**
- Week 1-2 (institution infrastructure): ~~2 weeks~~ → 4-6 hours (already exists!)
- Week 3-4 (faculty infrastructure): 2 weeks → 1.5 weeks (reuse pattern)
- Week 5 (UI & testing): 1 week → 1 week (unchanged)

**See Updated Version For:**
- Current 2.5-week timeline
- Revised task breakdowns
- Updated resource estimates
- Discovery impact section

---

**Original Document Content Follows Below**

---

# Phase 1 Implementation Roadmap
## Faculty-Level Statistics for 4TU.ResearchData

**Project Duration:** 5 weeks (25 working days)  
**Team Size:** 1 developer  
**Estimated Effort:** ~100 person-hours  
**Go-Live Date:** [Week of January 13, 2025]

---

## 🎯 Executive Summary

### What We're Building

A new feature that enables **faculty-level statistics** for TU Delft datasets in the 4TU.ResearchData repository.

**Current State:**
- ✅ Statistics available by institution (TU Delft, UT, TU/e, WUR)
- ❌ No statistics by faculty within TU Delft

**Future State:**
- ✅ Statistics available by institution
- ✅ **NEW:** Statistics by faculty (Aerospace, EEMCS, Civil Engineering, etc.)

**Business Value:**
- Faculty leaders can track their research output
- Institutional reporting becomes more granular
- Better visibility into faculty-level research contributions

---

## 📊 What Success Looks Like

### For End Users (Faculty Leaders & Institutional Staff)

**Before Phase 1:**
- Question: "How many datasets has the Faculty of Aerospace deposited?"
- Answer: ❌ "We don't know - we only track by institution"

**After Phase 1:**
- Question: "How many datasets has the Faculty of Aerospace deposited?"
- Answer: ✅ "Faculty of Aerospace has deposited 87 datasets (15% of TU Delft total)"

### Measurable Success Criteria

| Metric | Target | How We Measure |
|--------|--------|----------------|
| **Migration Coverage** | ≥90% | 90% of depositor accounts have faculty assigned |
| **Data Accuracy** | 100% | Manual verification of all faculty assignments |
| **Performance** | <2 sec | Statistics dashboard loads in under 2 seconds |
| **API Response** | <100ms | Faculty API endpoints respond in under 100ms |
| **User Adoption** | ≥80% | 80% of new users select faculty during registration within 3 months |
| **Zero Errors** | 100% | No production errors during first month |

---

## 🗓️ 5-Week Delivery Timeline

### Week 1: Foundation (Dec 16-20, 2024)
**Focus:** Build the technical infrastructure

**Developer Tasks:**
- Configure 8 TU Delft faculties in system configuration
- Extend database schema to support faculty data
- Create faculty management service
- Write automated tests

**Deliverables:**
- Faculty configuration file
- Updated database schema
- FacultyManager service (200 lines of code)
- 15 unit tests

**Milestone:** ✅ System can store and retrieve faculty data

**Stakeholder View:** _"Infrastructure is in place - system ready for faculty tracking"_

---

### Week 2: Data Migration (Dec 23-27, 2024)
**Focus:** Assign faculties to existing users

**Developer Tasks:**
- Export ~200 depositor accounts
- Parse "Organizations" field to detect faculties
- Manual review and correction workflow
- Import faculty assignments into database

**Deliverables:**
- Migrated accounts CSV file (~200 rows)
- Migration validation report
- Coverage report (≥90% target)

**Milestone:** ✅ All existing depositor accounts have faculties assigned

**Stakeholder View:** _"Historical data is now enriched with faculty information"_

**⚠️ Note:** This week includes holidays - may extend to early January

---

### Week 3: API Development (Jan 6-10, 2025)
**Focus:** Build the backend services

**Developer Tasks:**
- Implement 6 API endpoints for faculty data
- Create database query templates
- Add input validation and error handling
- Write integration tests

**API Endpoints Created:**
1. List all faculties
2. Get faculty details
3. Get faculty statistics
4. Get datasets by faculty
5. Update user's faculty
6. Auto-fill faculty on dataset submission

**Deliverables:**
- 6 working API endpoints
- API documentation
- 20 integration tests

**Milestone:** ✅ Backend services ready for UI integration

**Stakeholder View:** _"APIs are working - ready to build the user interface"_

---

### Week 4: User Interface (Jan 13-17, 2025)
**Focus:** Build the user-facing features

**Developer Tasks:**
- Add faculty dropdown to user registration
- Auto-fill faculty when depositing datasets
- Build faculty statistics dashboard
- Create admin interface for updating faculties

**UI Components Created:**
1. **Registration Page:** Faculty selection dropdown
2. **Dataset Submission:** Auto-fill depositor's faculty
3. **Statistics Dashboard:** Visual charts by faculty
4. **Admin Panel:** Update user faculties

**Deliverables:**
- 4 updated web pages
- Faculty statistics dashboard
- Admin management interface

**Milestone:** ✅ Users can interact with faculty features

**Stakeholder View:** _"Feature is visible and usable by end users"_

---

### Week 5: Testing & Deployment (Jan 20-24, 2025)
**Focus:** Ensure quality and go live

**Developer Tasks:**
- End-to-end testing (user workflows)
- Performance testing (load testing)
- User acceptance testing with pilot group
- Production deployment
- Post-deployment monitoring

**Testing Coverage:**
- ✅ Unit tests (80% code coverage)
- ✅ Integration tests (all API endpoints)
- ✅ End-to-end tests (5 user scenarios)
- ✅ Performance tests (100 concurrent users)
- ✅ UAT with 3-5 pilot users

**Deliverables:**
- Test results report
- Deployment plan
- Production deployment
- Monitoring dashboard

**Milestone:** ✅ Feature live in production

**Stakeholder View:** _"Faculty statistics are now available to all users"_

---

## 📅 Detailed Week-by-Week Schedule

### Week 1: Foundation (8 working days, 32 hours)

| Day | Task | Hours | Deliverable |
|-----|------|-------|-------------|
| Mon | Configure faculties in djehuty.xml | 4 | Faculty config file |
| Tue | Extend RDF schema with Faculty entity | 6 | Updated schema.ttl |
| Wed | Create FacultyManager service class | 6 | faculty.py (200 LOC) |
| Thu | Implement faculty validation logic | 4 | Validation methods |
| Fri | Write unit tests | 6 | 15 unit tests |
| Mon | Code review and refactoring | 4 | Clean code |
| Tue | Documentation updates | 2 | API docs |

**End of Week 1 Demo:** Show that system can create, read, update faculties via Python console

---

### Week 2: Migration (5 working days, 20 hours)
**Note:** Dec 25-26 are holidays - adjust schedule accordingly

| Day | Task | Hours | Deliverable |
|-----|------|-------|-------------|
| Mon | Write export script for depositors | 4 | export_depositors.py |
| Tue | Export accounts, parse Organizations | 4 | accounts.csv |
| Wed | Manual review of faculty assignments | 6 | Corrected assignments |
| Thu | Write import script | 3 | import_faculty.py |
| Fri | Run migration, validate coverage | 3 | Coverage report (≥90%) |

**End of Week 2 Demo:** Show statistics query returning datasets by faculty (backend only)

---

### Week 3: API Development (5 working days, 28 hours)

| Day | Task | Hours | Deliverable |
|-----|------|-------|-------------|
| Mon | Implement GET /v2/faculties endpoints (2) | 6 | List & detail endpoints |
| Tue | Implement GET /v2/statistics/faculties | 6 | Statistics endpoint |
| Wed | Implement GET datasets by faculty | 4 | Dataset listing endpoint |
| Thu | Extend PATCH /v2/accounts for faculty | 4 | Account update endpoint |
| Fri | Extend POST /v2/datasets for auto-fill | 4 | Dataset creation endpoint |
| Mon | Write integration tests | 4 | 20 integration tests |

**End of Week 3 Demo:** Show all 6 API endpoints working via Postman/curl

---

### Week 4: User Interface (5 working days, 26 hours)

| Day | Task | Hours | Deliverable |
|-----|------|-------|-------------|
| Mon | Add faculty dropdown to registration | 6 | Updated register.html |
| Tue | Auto-fill faculty on dataset submission | 6 | Updated submit_dataset.html |
| Wed | Build statistics dashboard (charts) | 8 | statistics_faculty.html |
| Thu | Create admin faculty update interface | 4 | admin_accounts.html |
| Fri | UI polish and responsive design | 2 | Polished UI |

**End of Week 4 Demo:** Complete user walkthrough - register, submit dataset, view statistics

---

### Week 5: Testing & Deployment (5 working days, 28 hours)

| Day | Task | Hours | Deliverable |
|-----|------|-------|-------------|
| Mon | End-to-end testing (5 scenarios) | 6 | E2E test results |
| Tue | Performance testing (load tests) | 4 | Performance report |
| Wed | User acceptance testing with pilots | 6 | UAT feedback |
| Thu | Fix bugs from testing | 6 | Bug fixes |
| Fri AM | Deploy to production | 3 | Production deployment |
| Fri PM | Post-deployment monitoring | 3 | Monitoring report |

**End of Week 5 Demo:** Live production feature demo to stakeholders

---

## 👥 Team & Responsibilities

### Development Team

**Lead Developer** (1 person, full-time)
- Backend development (RDF schema, Python services, API)
- Frontend development (HTML/JavaScript UI)
- Database migration
- Testing and deployment

**Estimated Total Effort:** ~100 person-hours over 5 weeks

### Supporting Roles (Part-Time)

**Technical Lead / Architect** (consultation as needed)
- Code review (end of each week, 1-2 hours)
- Architecture guidance
- Risk mitigation

**Product Owner** (minimal involvement)
- Week 1: Approve faculty list (30 min)
- Week 2: Review migration results (1 hour)
- Week 4: UAT participation (2 hours)
- Week 5: Go/No-Go decision (1 hour)

**QA / Tester** (Week 5 only)
- User acceptance testing (4 hours)
- Bug reporting
- Sign-off

**Total Team Effort:** ~110 person-hours

---

## 💰 Resource Requirements

### Development Environment

**Infrastructure (Already Available):**
- ✅ Development server (existing Djehuty instance)
- ✅ Virtuoso triple store (existing database)
- ✅ Git repository (version control)
- ✅ Testing framework (pytest)

**No New Infrastructure Required** - we use existing systems

### External Dependencies

**None** - this is a self-contained feature using existing technology stack

### Budget Considerations

**Development Cost:**
- 1 developer × 5 weeks × 20 hours/week = 100 hours
- At typical hourly rate: [Your organization's rate]

**Ongoing Costs:**
- Negligible - minimal database storage
- No performance impact (<0.1% query overhead)
- No additional infrastructure

**ROI:**
- Improved institutional reporting → Time saved for faculty administrators
- Better research visibility → Potential funding impact
- Foundation for future enhancements (Phase 2)

---

## 📋 Key Deliverables & Artifacts

### Code Deliverables

| Deliverable | Description | Size | Location |
|-------------|-------------|------|----------|
| **Faculty Configuration** | List of 8 TU Delft faculties | ~50 lines | `djehuty.xml` |
| **RDF Schema Extension** | Faculty entity definition | ~100 lines | `schema.ttl` |
| **FacultyManager Service** | Core business logic | ~200 lines | `faculty.py` |
| **API Endpoints** | 6 REST endpoints | ~300 lines | `ui.py` |
| **SPARQL Templates** | Database queries | ~150 lines | `faculties.sparql` |
| **UI Components** | HTML/JavaScript | ~400 lines | `*.html` |
| **Migration Scripts** | One-time migration | ~250 lines | `scripts/` |
| **Tests** | Unit + integration | ~500 lines | `tests/` |

**Total New Code:** ~950 lines + ~300 lines of changes to existing files

### Documentation Deliverables

| Document | Audience | Purpose |
|----------|----------|---------|
| **API Documentation** | Developers | How to use faculty APIs |
| **User Guide** | End users | How to use faculty features |
| **Admin Guide** | Administrators | How to manage faculties |
| **Migration Report** | Stakeholders | Data quality results |
| **Test Results** | QA/Stakeholders | Quality assurance evidence |
| **Deployment Plan** | Operations | How to deploy |

### Data Deliverables

| Deliverable | Description | Audience |
|-------------|-------------|----------|
| **Migrated Accounts** | ~200 accounts with faculties | Database |
| **Coverage Report** | % of accounts with faculties | Product Owner |
| **Validation Report** | Data quality metrics | Technical Lead |

---

## 🎬 Rollout Strategy

### Pre-Launch (Week 5, Day 1-4)

**Internal Testing:**
- Developer self-testing (complete workflows)
- Technical team review (peer testing)
- Pilot group UAT (3-5 institutional users)

**Pilot Group:**
- 1-2 faculty administrators
- 1-2 researchers who frequently deposit
- 1 institutional staff member

**Success Criteria for Go-Live:**
- ✅ All UAT scenarios pass
- ✅ No critical bugs
- ✅ Performance targets met
- ✅ Product Owner approval

---

### Launch Day (Week 5, Friday)

**Timeline:**
- **6:00 AM:** Deploy to production (low traffic time)
- **7:00 AM:** Smoke tests (verify all endpoints working)
- **8:00 AM:** Enable feature for all users
- **9:00 AM:** Monitor error logs and performance
- **10:00 AM:** Send announcement email to users
- **All Day:** Active monitoring, ready to rollback if needed

**Deployment Steps:**
1. Backup production database (30 min)
2. Deploy code to production server (15 min)
3. Run database migration script (5 min)
4. Restart application services (5 min)
5. Run smoke tests (15 min)
6. Monitor for 1 hour (60 min)
7. **GO/NO-GO decision** ✅

**Rollback Plan:**
- If critical issues detected within first 2 hours
- Restore from backup (~30 min)
- Rollback deployment (~15 min)
- Investigate issues, fix, reschedule deployment

---

### Post-Launch (Week 6+)

**Week 1 After Launch:**
- Daily monitoring (error rates, performance, usage)
- Respond to user feedback within 24 hours
- Hot-fix deployment if critical bugs found

**Week 2-4 After Launch:**
- Weekly usage reports (how many users selecting faculties?)
- Bi-weekly sync with Product Owner
- Document lessons learned

**Month 2-3:**
- Measure user adoption (target ≥80%)
- Gather feedback for improvements
- Plan Phase 2 (if desired)

---

## 📊 Monitoring & Success Metrics

### Technical Metrics (Automated Monitoring)

**Daily Dashboard:**
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| API Error Rate | <0.1% | >1% |
| API Response Time | <100ms | >200ms |
| Dashboard Load Time | <2 sec | >5 sec |
| Database Query Time | <50ms | >100ms |
| System Uptime | 99.9% | <99% |

**Tools:**
- Application logs (automatically monitored)
- Performance monitoring (response times)
- Error tracking (exception alerts)

---

### Business Metrics (Manual Reporting)

**Weekly Reports:**
| Metric | Measurement | Target (Month 3) |
|--------|-------------|------------------|
| Users with Faculty Assigned | Count from database | 200 (existing) + 80% of new |
| Datasets with Faculty | % of TU Delft datasets | 100% (depositor faculty) |
| Faculty Stats Page Views | Google Analytics | ≥100 views/month |
| User Adoption (New Registrations) | % selecting faculty | ≥80% |

**Monthly Review:**
- Stakeholder presentation with metrics
- User feedback summary
- Improvement backlog prioritization

---

## ⚠️ Risks & Mitigation

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Migration Data Quality** | Medium | High | Manual review all assignments, aim for 100% accuracy |
| **Performance Degradation** | Low | Medium | Performance testing in Week 5, caching if needed |
| **API Breaking Changes** | Low | High | Backward compatibility checks, versioned APIs |
| **Production Deployment Issues** | Medium | High | Backup before deployment, rollback plan ready |

### Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Holiday Delays (Week 2)** | High | Low | Buffer time in Week 5, can extend to Week 6 if needed |
| **Developer Unavailability** | Low | High | Knowledge transfer documentation, backup developer identified |
| **Scope Creep** | Medium | Medium | Strict scope control, Phase 2 for new requests |
| **UAT Delays** | Medium | Low | Pre-schedule UAT participants, backup testers ready |

### Business Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Low User Adoption** | Medium | Medium | Training materials, user communication plan |
| **Stakeholder Expectation Mismatch** | Low | Medium | Clear scope documentation, weekly demos |
| **Data Quality Concerns** | Low | High | 100% manual verification during migration |

---

## ✅ Quality Assurance

### Testing Strategy

**Level 1: Unit Tests (Week 1)**
- Test individual functions in isolation
- Target: 80% code coverage
- Tools: pytest
- Duration: Ongoing during development

**Level 2: Integration Tests (Week 3)**
- Test API endpoints end-to-end
- All 6 endpoints tested with valid/invalid inputs
- Tools: pytest + requests library
- Duration: 1 day

**Level 3: End-to-End Tests (Week 5)**
- Test complete user workflows
- 5 scenarios:
  1. New user registers with faculty
  2. User deposits dataset (faculty auto-filled)
  3. Admin updates user's faculty
  4. User views faculty statistics
  5. Export faculty statistics to CSV

**Level 4: Performance Tests (Week 5)**
- Load testing: 100 concurrent users
- Stress testing: 200 concurrent users
- Target: <2 sec response time under load
- Tools: JMeter or Locust

**Level 5: User Acceptance Testing (Week 5)**
- 3-5 pilot users
- Real-world scenarios
- Feedback collection
- Sign-off required for go-live

---

### Code Quality Standards

**Code Review:**
- All code reviewed by Technical Lead
- Weekly review sessions (end of each week)
- Review checklist:
  - ✅ Code readability
  - ✅ Test coverage
  - ✅ Error handling
  - ✅ Documentation
  - ✅ Performance

**Standards:**
- Python PEP 8 style guide
- Meaningful variable names
- Inline comments for complex logic
- Docstrings for all functions

---

## 📢 Communication Plan

### Internal Communication (Development Team)

**Daily:**
- Morning standup (15 min)
- Slack updates on progress/blockers

**Weekly:**
- End-of-week demo to Technical Lead
- Week-ahead planning

**Ad-Hoc:**
- Code review sessions
- Pair programming if blocked

---

### Stakeholder Communication

**Week 1:**
- **Email Update:** "Phase 1 kickoff - Foundation week"
- **Demo:** Show faculty configuration (technical stakeholders only)

**Week 2:**
- **Email Update:** "Migration complete - [X]% coverage achieved"
- **Report:** Migration coverage report to Product Owner

**Week 3:**
- **Email Update:** "APIs complete - backend ready"
- **Demo:** API demo via Postman (optional)

**Week 4:**
- **Email Update:** "UI complete - feature ready for testing"
- **Demo:** Full UI walkthrough to all stakeholders

**Week 5:**
- **Monday:** "Testing week - UAT invitation"
- **Wednesday:** UAT session with pilot users
- **Thursday:** "Go/No-Go decision meeting"
- **Friday AM:** "Deployment notification - downtime window"
- **Friday PM:** "✅ Launch announcement - faculty statistics live!"

---

### User Communication

**Pre-Launch (Week 4):**
- Email to power users: "New feature coming soon"
- Documentation published: User guide on website

**Launch Day (Week 5):**
- Announcement email: "New faculty statistics now available"
- In-app notification banner
- Blog post on 4TU.ResearchData website

**Post-Launch (Week 6+):**
- Tutorial video (optional)
- FAQ document
- Support channel for questions

---

## 📖 Training & Documentation

### User Documentation

**User Guide: "How to Use Faculty Statistics"**
- How to select your faculty during registration
- How your faculty is used on datasets
- How to view faculty statistics
- How to update your faculty (contact admin)

**Target Audience:** All 4TU.ResearchData users  
**Format:** Web page + PDF  
**Length:** 2-3 pages with screenshots

---

### Admin Documentation

**Admin Guide: "Managing User Faculties"**
- How to view users by faculty
- How to update a user's faculty
- How to generate faculty reports
- Troubleshooting common issues

**Target Audience:** Institutional administrators  
**Format:** Internal wiki page  
**Length:** 4-5 pages

---

### Developer Documentation

**Technical Documentation:**
- API endpoint specifications
- Database schema changes
- SPARQL query templates
- Code structure overview

**Target Audience:** Future developers  
**Format:** Code comments + README  
**Length:** Inline documentation + 5-page README

---

### Training Sessions (Optional)

**For Administrators (1 hour):**
- Overview of faculty feature
- How to manage user faculties
- How to generate reports
- Q&A

**For End Users (Optional):**
- Self-service via user guide
- No formal training needed (simple UI)

---

## 🎁 Benefits & Value Proposition

### For Faculty Leaders

**Before Phase 1:**
- ❌ "How many datasets has my faculty deposited?" → Unknown
- ❌ "Which faculty contributes most to the repository?" → Unknown
- ❌ Annual reporting requires manual data gathering

**After Phase 1:**
- ✅ Real-time statistics dashboard
- ✅ Sortable/filterable faculty comparisons
- ✅ One-click CSV export for reports

**Value:** Save 2-3 hours per year per faculty on manual reporting

---

### For Institutional Staff

**Before Phase 1:**
- ❌ Only institution-level granularity
- ❌ Cannot answer faculty-specific questions
- ❌ Manual email queries to users

**After Phase 1:**
- ✅ Faculty-level granularity
- ✅ Self-service statistics for common questions
- ✅ Automated tracking

**Value:** Faster response to data requests, better institutional insights

---

### For Researchers

**Before Phase 1:**
- No change in deposit workflow

**After Phase 1:**
- ✅ Faculty auto-filled on dataset submission (less typing)
- ✅ Visibility into faculty's research output
- ✅ Pride in faculty contributions

**Value:** Minor workflow improvement, increased transparency

---

### For the Institution

**Strategic Benefits:**
- ✅ Better understanding of faculty research output
- ✅ Data-driven decision making
- ✅ Foundation for future analytics (Phase 2: collaboration networks, etc.)
- ✅ Competitive advantage over other repositories

**Measurable ROI:**
- Time saved on reporting: ~20 hours/year across all faculties
- Improved data quality: 100% of deposits tagged with faculty
- Foundation for Phase 2: ~€10-15k in future savings by having clean data

---

## 🔄 Post-Launch Roadmap

### Immediate Next Steps (Month 1)

**Week 1 After Launch:**
- Monitor adoption rates daily
- Respond to user feedback
- Fix any bugs reported
- Publish success metrics

**Week 2-4:**
- Assess user adoption (target ≥80%)
- Gather feature requests
- Document lessons learned
- Celebrate success! 🎉

---

### Future Enhancements (Month 2+)

**Phase 1.1 (Quick Wins):**
- Export faculty statistics to Excel
- Faculty comparison charts (bar/pie charts)
- Email notifications for faculty milestones
- Historical trend charts (datasets over time)

**Phase 2 (Author-Level, 10 weeks):**
- Track faculty for ALL authors (not just depositors)
- Collaboration networks between faculties
- Confidence scoring for automated assignments
- See `docs/future-work/` for detailed specification

**Phase 3+ (Long-Term Vision):**
- Department-level tracking
- Research group statistics
- ORCID integration
- Cross-institutional collaboration analytics

---

## 📞 Support & Escalation

### During Development (Week 1-5)

**Technical Issues:**
- **Developer → Technical Lead** (same day)
- **Technical Lead → CTO** (if critical)

**Schedule Issues:**
- **Developer → Product Owner** (within 1 day)
- **Product Owner → Steering Committee** (if impacts go-live)

**Scope Issues:**
- **Anyone → Product Owner** (immediately)
- **Product Owner makes final call** (defer to Phase 2 if needed)

---

### Post-Launch Support

**User Issues:**
- **Users → Help Desk** (email/ticket)
- **Help Desk → Developer** (if technical)
- **SLA:** Respond within 24 hours, resolve within 72 hours

**Critical Bugs:**
- **Anyone → Developer** (immediately, phone/Slack)
- **Developer → Technical Lead** (if rollback needed)
- **Rollback decision:** Within 2 hours of discovery

---

## ✅ Sign-Off & Approvals

### Required Approvals

**Before Development Starts (Week 0):**
- [ ] Product Owner: Approve scope and timeline
- [ ] Technical Lead: Approve architecture
- [ ] Budget Owner: Approve resource allocation

**Before Production Deployment (Week 5, Thursday):**
- [ ] QA Team: Sign-off on testing results
- [ ] Product Owner: Approve go-live
- [ ] Operations: Confirm deployment window

**After Launch (Week 6):**
- [ ] Users: Feedback collected
- [ ] Product Owner: Success criteria met
- [ ] Project closure: Lessons learned documented

---

## 📎 Appendices

### Appendix A: Faculty List (8 TU Delft Faculties)

| Faculty ID | Faculty Name | Abbreviation |
|------------|--------------|--------------|
| 285860001 | Faculty of Aerospace Engineering | AE |
| 285860002 | Faculty of Architecture and the Built Environment | A+BE |
| 285860003 | Faculty of Applied Sciences | AS |
| 285860004 | Faculty of Civil Engineering and Geosciences | CEG |
| 285860005 | Faculty of Electrical Engineering, Mathematics and Computer Science | EEMCS |
| 285860006 | Faculty of Industrial Design Engineering | IDE |
| 285860007 | Faculty of Mechanical Engineering | ME |
| 285860008 | Faculty of Technology, Policy and Management | TPM |

---

### Appendix B: Technical Stack

**Backend:**
- Python 3.12
- Werkzeug (web framework)
- RDFlib (RDF processing)
- Virtuoso (triple store database)

**Frontend:**
- HTML5
- JavaScript (vanilla)
- Jinja2 (templating)
- CSS3

**Infrastructure:**
- Docker (containerization)
- Git (version control)
- pytest (testing)

---

### Appendix C: Key Documents

**For Implementation:**
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Complete technical specification (61 pages)
- `docs/assignment/ARCHITECTURE_SUMMARY.md` - Quick reference (6 pages)
- `docs/PHASE1_FOCUS.md` - Scope boundaries

**For Stakeholders:**
- `docs/assignment/PRESENTATION_OUTLINE.md` - 14-slide presentation
- This roadmap document - Implementation plan

**For Context:**
- `docs/current-system/CODEBASE_ANALYSIS.md` - Current system analysis
- `docs/REQUIREMENTS_SUMMARY.md` - Requirements coverage

---

### Appendix D: Glossary

**For Non-Technical Stakeholders:**

- **Faculty:** Academic division within TU Delft (e.g., Aerospace Engineering)
- **Depositor:** Person who uploads a dataset to the repository
- **Migration:** Process of adding faculty information to existing user accounts
- **API:** Application Programming Interface - how software components communicate
- **Dashboard:** Visual display of statistics and metrics
- **UAT:** User Acceptance Testing - testing by real users before launch
- **Rollback:** Reverting to the previous version if problems occur
- **Coverage:** Percentage of users who have faculty assigned

---

## 🎯 Summary

**This roadmap delivers:**
✅ Clear timeline: 5 weeks from start to production  
✅ Defined scope: Faculty statistics for depositors  
✅ Measurable success: ≥90% coverage, 100% accuracy  
✅ Managed risks: Mitigation plans for all identified risks  
✅ Quality assurance: 5 levels of testing  
✅ Communication plan: Regular updates to all stakeholders  
✅ Rollout strategy: Phased deployment with rollback plan  

**Questions? Contact:**
- **Technical Questions:** [Technical Lead Name/Email]
- **Business Questions:** [Product Owner Name/Email]
- **Schedule Questions:** [Project Manager Name/Email]

---

**Document Version:** 1.0  
**Last Updated:** December 9, 2024  
**Next Review:** End of Week 1 (Dec 20, 2024)

---

*Let's build faculty statistics together! 🚀*
