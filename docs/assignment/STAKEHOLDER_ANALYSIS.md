# Stakeholder Analysis

**Document Version:** 1.0  
**Date:** December 10, 2024  
**Status:** Active  
**Owner:** Project Manager & Product Owner  
**Purpose:** Identify, analyze, and engage stakeholders for faculty statistics feature

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Stakeholder Identification](#stakeholder-identification)
3. [Power/Interest Matrix](#powerinterest-matrix)
4. [Stakeholder Profiles](#stakeholder-profiles)
5. [Benefit Mapping](#benefit-mapping)
6. [Engagement Strategy](#engagement-strategy)
7. [Communication Plan](#communication-plan)
8. [Influence & Decision-Making](#influence--decision-making)

---

## 1. Executive Summary

### Why Stakeholder Analysis Matters

**Without stakeholder analysis:**
- Build wrong features (don't understand needs)
- Miss critical requirements (didn't talk to right people)
- Face resistance (stakeholders feel ignored)
- Launch fails (no champions, no adoption)

**With stakeholder analysis:**
- ✅ Build right features (understand needs)
- ✅ Get buy-in early (stakeholders feel heard)
- ✅ Champions advocate for feature
- ✅ Successful adoption

### Key Findings

**Total Stakeholders Identified:** 23 individuals/groups

**By Category:**
- 🎯 **Executive (4):** CIO, Repository Manager, Data Protection Officer, Dean of Research
- 👥 **Operational (6):** Data stewards, repository staff, IT support
- 💻 **Technical (3):** Developers, data engineers, system administrators
- 📊 **End Users (10):** Faculty deans, research managers, policy makers, depositors, researchers

**By Power/Interest:**
- 🔴 **High Power, High Interest (6):** MANAGE CLOSELY - Key decision-makers
- 🟠 **High Power, Low Interest (4):** KEEP SATISFIED - Need their approval but less involved
- 🟡 **Low Power, High Interest (8):** KEEP INFORMED - Champions and users
- 🟢 **Low Power, Low Interest (5):** MONITOR - Minimal engagement needed

### Top 5 Stakeholders to Engage

1. **Repository Manager** - Project sponsor, decision-maker, budget owner
2. **Gabriela (Data Manager)** - Already engaged, provides valuable feedback, champion
3. **Faculty Deans (3 faculties)** - Primary beneficiaries, pilot users, champions
4. **Data Protection Officer** - Critical for GDPR compliance approval
5. **Lead Developer (Djehuty)** - Technical implementation owner

---

## 2. Stakeholder Identification

### 2.1 Executive Stakeholders

| Stakeholder | Role | Organization | Why They Matter |
|-------------|------|--------------|-----------------|
| **CIO (Chief Information Officer)** | Strategic decision-maker | 4TU.ResearchData | Budget approval, strategic alignment, IT infrastructure |
| **Repository Manager** | Product owner / sponsor | 4TU.ResearchData | Project sponsor, prioritization, resource allocation |
| **Data Protection Officer (DPO)** | Compliance gatekeeper | 4TU / University | GDPR compliance approval (required before launch) |
| **Dean of Research** | Strategic stakeholder | University (TU Delft example) | Represents faculty interests, uses data for strategy |

### 2.2 Operational Stakeholders

| Stakeholder | Role | Organization | Why They Matter |
|-------------|------|--------------|-----------------|
| **Data Stewards (3-5 people)** | Data curators | 4TU.ResearchData | Manage faculty assignments, ensure data quality |
| **Repository Staff (5-10 people)** | Support & operations | 4TU.ResearchData | User support, training, communication |
| **IT Support Team** | Infrastructure support | 4TU / University IT | Server infrastructure, deployment, monitoring |
| **Training Coordinator** | User training | 4TU.ResearchData | Trains users on new features |
| **Communication Manager** | External communication | 4TU.ResearchData | Announces new features, writes blog posts |
| **Gabriela (Data Manager)** | Data manager / power user | 4TU.ResearchData | Early adopter, feedback provider, champion |

### 2.3 Technical Stakeholders

| Stakeholder | Role | Organization | Why They Matter |
|-------------|------|--------------|-----------------|
| **Lead Developer (Djehuty)** | Technical lead | Development team | Implements feature, architectural decisions |
| **Data Engineer** | Database administrator | Technical team | Manages Virtuoso RDF database, performance tuning |
| **System Administrator** | Infrastructure | IT team | Deployment, monitoring, backups |

### 2.4 End User Stakeholders

| Stakeholder | Role | Organization | Why They Matter |
|-------------|------|--------------|-----------------|
| **Faculty Deans (8 faculties at TU Delft)** | Strategic decision-makers | Universities | Primary users of faculty statistics, decision-making |
| **Research Managers (per faculty)** | Operational managers | Universities | Use statistics for reporting, resource allocation |
| **Policy Makers / Administrators** | Strategic planning | Universities / 4TU | Use statistics for policy decisions, funding allocation |
| **Research Support Staff** | Operational support | Universities | Help researchers deposit data, verify faculty assignments |
| **Depositors (Researchers)** | Content creators | Universities | Deposit datasets, need to select/update faculty |
| **Researchers (General)** | Content consumers | Universities / Public | Browse datasets by faculty, discover research |
| **External Stakeholders (Funders, NWO)** | Funding agencies | External | May use statistics to evaluate university research output |
| **Public / Media** | General public | External | May view aggregated statistics (transparency) |

### 2.5 Indirect Stakeholders

| Stakeholder | Role | Why They Matter |
|-------------|------|-----------------|
| **DANS (Data Archiving and Networked Services)** | National data infrastructure | Partner organization, potential collaboration |
| **Other Research Data Repositories (OpenAIRE, Zenodo)** | Competitors / partners | Benchmark, learn from their approaches |
| **Djehuty Open Source Community** | Contributors | May contribute code, provide feedback |

---

## 3. Power/Interest Matrix

### 3.1 Matrix Visualization

```
               High Power
                  ↑
    ┌─────────────┼─────────────┐
    │             │             │
    │  KEEP       │   MANAGE    │
    │  SATISFIED  │   CLOSELY   │
    │             │             │
    │ • CIO       │ • Repo Mgr  │
    │ • IT Supp   │ • DPO       │
Low │ • SysAdmin  │ • Lead Dev  │ High
Int │ • Dean Res  │ • Gabriela  │ Interest
    │             │ • Fac Deans │
    ├─────────────┼─────────────┤
    │             │             │
    │  MONITOR    │   KEEP      │
    │             │   INFORMED  │
    │             │             │
    │ • Public    │ • Data Stew │
    │ • Media     │ • Repo Staff│
    │ • Funders   │ • Res Mgrs  │
    │             │ • Depositors│
    └─────────────┼─────────────┘
                  ↓
               Low Power
```

### 3.2 Quadrant Strategies

**🔴 Manage Closely (High Power, High Interest)**
- **Who:** Repository Manager, DPO, Lead Developer, Gabriela, Faculty Deans (3 pilot)
- **Strategy:** Active engagement, frequent updates, collaboration on design
- **Engagement Level:** Weekly/bi-weekly meetings, demos, feedback sessions

**🟠 Keep Satisfied (High Power, Low Interest)**
- **Who:** CIO, IT Support, Dean of Research, System Administrator
- **Strategy:** Keep informed of major milestones, get approval when needed
- **Engagement Level:** Monthly updates, involve in key decisions

**🟡 Keep Informed (Low Power, High Interest)**
- **Who:** Data Stewards, Repository Staff, Research Managers, Depositors, Training Coordinator
- **Strategy:** Regular communication, gather feedback, provide updates
- **Engagement Level:** Email newsletters, training sessions, surveys

**🟢 Monitor (Low Power, Low Interest)**
- **Who:** Public, Media, External Funders, DANS
- **Strategy:** Minimal engagement, inform when relevant
- **Engagement Level:** Public announcements, blog posts

### 3.3 Stakeholder Mapping Table

| Stakeholder | Power | Interest | Quadrant | Engagement Level |
|-------------|-------|----------|----------|------------------|
| **Repository Manager** | High | High | 🔴 Manage Closely | Weekly meetings, demos |
| **Gabriela** | Medium | High | 🔴 Manage Closely | Weekly feedback, pilot user |
| **Faculty Deans (3 pilot)** | High | High | 🔴 Manage Closely | Bi-weekly interviews, pilot |
| **Data Protection Officer** | High | High | 🔴 Manage Closely | PIA review, GDPR approval |
| **Lead Developer** | Medium | High | 🔴 Manage Closely | Daily collaboration |
| **CIO** | High | Low | 🟠 Keep Satisfied | Monthly status report |
| **IT Support** | Medium | Low | 🟠 Keep Satisfied | Deployment coordination |
| **Dean of Research** | High | Medium | 🟠 Keep Satisfied | Quarterly update |
| **System Administrator** | Medium | Low | 🟠 Keep Satisfied | Deployment support |
| **Data Stewards** | Low | High | 🟡 Keep Informed | Training, email updates |
| **Repository Staff** | Low | High | 🟡 Keep Informed | Training, demos |
| **Research Managers** | Low | High | 🟡 Keep Informed | User testing, surveys |
| **Depositors** | Low | High | 🟡 Keep Informed | UI changes, self-service |
| **Training Coordinator** | Low | High | 🟡 Keep Informed | Collaborate on training |
| **Communication Manager** | Low | Medium | 🟡 Keep Informed | Collaborate on announcements |
| **Data Engineer** | Medium | Medium | 🟡 Keep Informed | Performance tuning |
| **Researchers (General)** | Low | Medium | 🟡 Keep Informed | Public announcements |
| **Public** | Low | Low | 🟢 Monitor | Public blog posts |
| **Media** | Low | Low | 🟢 Monitor | Press releases (if needed) |
| **Funders (NWO, etc.)** | Medium | Low | 🟢 Monitor | Public statistics |
| **DANS** | Low | Low | 🟢 Monitor | Partnership opportunities |

---

## 4. Stakeholder Profiles

### 4.1 Repository Manager (Project Sponsor)

**Profile:**
- **Name:** [TBD - likely named in assignment context]
- **Role:** Manager of 4TU.ResearchData repository
- **Power:** High (budget approval, go/no-go decisions)
- **Interest:** High (wants successful feature launch)

**Needs & Goals:**
- ✅ Successful feature launch (on time, on budget)
- ✅ Positive user feedback (demonstrates value)
- ✅ Minimal risk (no security breaches, GDPR compliance)
- ✅ Stakeholder satisfaction (faculty deans, CIO)

**Concerns:**
- ⚠️ Timeline delays
- ⚠️ Budget overruns
- ⚠️ GDPR non-compliance
- ⚠️ Low user adoption

**Communication Preferences:**
- Weekly status emails (concise, bullet points)
- Bi-weekly meetings (30 minutes, in-person or video)
- Escalation for major issues (immediately)

**Engagement Strategy:**
- Involve in major decisions (architecture, GDPR approach)
- Demo after each wave (show progress)
- Transparent about risks and mitigations

---

### 4.2 Gabriela (Data Manager - Early Adopter)

**Profile:**
- **Name:** Gabriela
- **Role:** Data Manager at 4TU.ResearchData
- **Power:** Medium (influential, but not final decision-maker)
- **Interest:** High (provided detailed feedback on prototype)

**Needs & Goals:**
- ✅ Easy access to faculty-level statistics (her job easier)
- ✅ Accurate data (for reporting to stakeholders)
- ✅ User-friendly interface (no technical skills required)
- ✅ Export to Excel (for further analysis)

**Concerns:**
- ⚠️ Data quality (too many NULL/missing values)
- ⚠️ Complexity (too technical, hard to explain to stakeholders)
- ⚠️ Performance (slow queries frustrating)

**Communication Preferences:**
- Email + Slack for quick questions
- Weekly check-ins (informal, 15 minutes)
- Hands-on testing (loves to try prototypes)

**Engagement Strategy:**
- ✅ Already engaged (provided feedback on prototype)
- Involve in design decisions (dashboard layout, etc.)
- Pilot user for Wave 1 & Wave 2
- Collect testimonial after launch (champion)

**Quote from Feedback:**
> "This will help us a lot! But we need to make sure the data is accurate first."

---

### 4.3 Faculty Deans (Primary Users)

**Profile:**
- **Number:** 8 faculties at TU Delft (example: Aerospace, EEMCS, Civil Engineering, etc.)
- **Role:** Strategic decision-makers for their faculties
- **Power:** High (influential, can champion or block feature)
- **Interest:** High (use statistics for strategic planning)

**Needs & Goals:**
- ✅ Understand research output of their faculty
- ✅ Benchmark against other faculties
- ✅ Report to university leadership (data for meetings)
- ✅ Identify trends (growth, decline, emerging topics)

**Concerns:**
- ⚠️ Data accuracy (don't want to report wrong numbers)
- ⚠️ Privacy (ensure faculty data is not misused)
- ⚠️ Complexity (busy people, need simple interface)

**Communication Preferences:**
- Email (formal, official)
- Quarterly meetings (strategic updates)
- Demos (visual, interactive)

**Engagement Strategy:**
- Identify 3 faculties for pilot (diverse: large, small, different disciplines)
- Personal invitations to participate
- Monthly interviews during pilot (15-30 minutes)
- Showcase their faculty in demos (personalized data)
- Collect testimonials for communication

**Example Faculties for Pilot:**
1. **Faculty of Aerospace Engineering** (large, high research output)
2. **Faculty of EEMCS** (very large, diverse research topics)
3. **Faculty of Industrial Design Engineering** (smaller, unique characteristics)

---

### 4.4 Data Protection Officer (DPO)

**Profile:**
- **Role:** Ensures GDPR compliance for 4TU / University
- **Power:** High (can block launch if non-compliant)
- **Interest:** High (personal data is involved)

**Needs & Goals:**
- ✅ GDPR compliance (legal requirement)
- ✅ Privacy Impact Assessment completed
- ✅ User rights implemented (access, rectification, erasure)
- ✅ Data minimization (only collect necessary data)

**Concerns:**
- ⚠️ Personal data exposure (faculty assignments are personal data)
- ⚠️ Data breaches (security vulnerabilities)
- ⚠️ User rights not implemented
- ⚠️ No lawful basis for processing

**Communication Preferences:**
- Formal documentation (Privacy Impact Assessment)
- Meetings for clarification (scheduled, agenda-driven)
- Legal review of privacy notice

**Engagement Strategy:**
- Schedule PIA review early (Week 1-2)
- Provide comprehensive documentation (SECURITY_AND_AUDIT.md)
- Address concerns proactively
- Get written approval before production launch

**Deliverables for DPO:**
- [ ] Privacy Impact Assessment document
- [ ] Privacy notice (user-facing)
- [ ] Data retention policy
- [ ] User rights implementation plan
- [ ] Security audit report

---

### 4.5 Lead Developer (Technical Owner)

**Profile:**
- **Role:** Implements faculty statistics feature
- **Power:** Medium (technical decisions, timeline estimates)
- **Interest:** High (responsible for delivery)

**Needs & Goals:**
- ✅ Clear requirements (no ambiguity)
- ✅ Realistic timeline (not rushed)
- ✅ Technical support (help from team, vendor)
- ✅ Quality code (maintainable, tested)

**Concerns:**
- ⚠️ Unrealistic deadlines
- ⚠️ Scope creep
- ⚠️ Technical debt
- ⚠️ Insufficient testing time

**Communication Preferences:**
- Daily stand-ups (team synchronization)
- Slack for quick questions
- Code reviews (peer feedback)

**Engagement Strategy:**
- Involve in planning (realistic estimates)
- Empower decision-making (architecture choices)
- Protect from interruptions (focus time)
- Celebrate achievements (recognition)

---

### 4.6 Data Stewards (Operational Users)

**Profile:**
- **Number:** 3-5 people
- **Role:** Curate faculty assignments, ensure data quality
- **Power:** Low (operational, not decision-makers)
- **Interest:** High (feature affects their daily work)

**Needs & Goals:**
- ✅ Easy faculty assignment workflow (bulk updates, CSV import)
- ✅ Data quality dashboard (identify missing/incorrect faculty)
- ✅ Validation tools (prevent invalid faculty assignments)

**Concerns:**
- ⚠️ Manual work increases (too many accounts to update)
- ⚠️ No tools to find data quality issues
- ⚠️ Users blame them for incorrect data

**Communication Preferences:**
- Email for updates
- Training sessions (hands-on)
- Support channels (Slack, ticketing system)

**Engagement Strategy:**
- Involve in Wave 1 testing (validate data cleanup process)
- Provide training before launch
- Create user guide (step-by-step instructions)
- Collect feedback on workflow improvements

---

## 5. Benefit Mapping

### 5.1 Benefits by Stakeholder Group

| Stakeholder Group | Primary Benefit | Secondary Benefits | How They Benefit |
|-------------------|-----------------|--------------------|--------------------|
| **Faculty Deans** | Strategic insight | Benchmarking, reporting | Use statistics for faculty planning, resource allocation, leadership meetings |
| **Research Managers** | Operational reporting | Trend analysis | Monthly/quarterly reports on faculty research output |
| **Repository Manager** | Feature success | User satisfaction, strategic value | Demonstrates repository value to stakeholders, justifies funding |
| **Gabriela (Data Manager)** | Time savings | Data accuracy | Automated statistics vs. manual queries, better data quality |
| **Data Stewards** | Data quality tools | Workflow efficiency | Dashboard highlights data quality issues, bulk update tools |
| **Depositors** | Self-service | Transparency | Update their own faculty (no need to contact support) |
| **IT/Technical Team** | Reduced support burden | System reliability | Fewer manual queries, automated workflows |
| **CIO** | ROI | Strategic alignment | Feature demonstrates IT investment value |
| **Researchers** | Discovery | Faculty-specific browsing | Find datasets from specific faculties |
| **Public** | Transparency | Open data | View aggregated research output statistics |

### 5.2 Value Proposition by Stakeholder

**For Faculty Deans:**
> **"Understand your faculty's research data output in 2 minutes, not 2 days."**
> 
> - See dataset counts, file sizes, downloads per faculty
> - Benchmark against other faculties (anonymized)
> - Export to Excel for board meetings
> - Monthly email summaries (automated)

**For Gabriela (Data Manager):**
> **"Spend less time on manual queries, more time on strategic analysis."**
> 
> - Automated statistics (no more SPARQL queries)
> - Data quality dashboard (find missing faculty assignments)
> - Beautiful visualizations (share with stakeholders)

**For Data Stewards:**
> **"Find and fix data quality issues in minutes."**
> 
> - Dashboard highlights accounts without faculty
> - Bulk update tools (CSV import)
> - Validation prevents errors

**For Repository Manager:**
> **"Demonstrate repository value to stakeholders."**
> 
> - Data-driven decision-making (statistics support funding requests)
> - User satisfaction (feature requested by stakeholders)
> - Competitive advantage (other repositories don't have this)

---

## 6. Engagement Strategy

### 6.1 Engagement Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│  Phase 1: AWARENESS                                      │
│  Goal: Stakeholders know feature is coming              │
│  Activities:                                             │
│    • Email announcement                                  │
│    • Presentation at repository meeting                  │
│    • Blog post / newsletter                              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Phase 2: INTEREST                                       │
│  Goal: Stakeholders understand benefits                 │
│  Activities:                                             │
│    • Prototype demonstrations                            │
│    • User interviews (understand needs)                  │
│    • Use case examples                                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Phase 3: DESIRE                                         │
│  Goal: Stakeholders want to use feature                 │
│  Activities:                                             │
│    • Personalized demos (show THEIR faculty data)        │
│    • Testimonials from early users                       │
│    • Highlight pain points feature solves               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Phase 4: ACTION                                         │
│  Goal: Stakeholders use feature                          │
│  Activities:                                             │
│    • Training sessions                                   │
│    • User guides                                         │
│    • Support channels                                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Phase 5: RETENTION                                      │
│  Goal: Stakeholders continue using feature              │
│  Activities:                                             │
│    • Regular updates (new features)                      │
│    • Monthly usage tips                                  │
│    • Collect feedback for improvements                   │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Engagement Activities by Phase

**Phase 1: Awareness (Week 1-2)**

| Activity | Audience | Owner | Timeline |
|----------|----------|-------|----------|
| Email announcement | All stakeholders | Communication Manager | Week 1 |
| Presentation at repository meeting | Repository staff | Project Manager | Week 2 |
| Blog post | Public | Communication Manager | Week 2 |

**Phase 2: Interest (Week 3-6)**

| Activity | Audience | Owner | Timeline |
|----------|----------|-------|----------|
| Prototype demonstrations | Repository Manager, Gabriela | Lead Developer | Week 3-4 |
| User interviews | Faculty Deans (3) | Product Owner | Week 4-6 |
| Use case document | All stakeholders | Product Owner | Week 5 |

**Phase 3: Desire (Week 7-10)**

| Activity | Audience | Owner | Timeline |
|----------|----------|-------|----------|
| Personalized demos | Faculty Deans | Product Owner | Week 7-8 |
| Testimonials video | Gabriela, 1 Faculty Dean | Communication Manager | Week 9 |
| Pain point presentation | Repository Manager, CIO | Project Manager | Week 10 |

**Phase 4: Action (Week 11-14 - Launch)**

| Activity | Audience | Owner | Timeline |
|----------|----------|-------|----------|
| Training webinar | Data stewards, repository staff | Training Coordinator | Week 11 |
| User guide publication | All users | Documentation Team | Week 12 |
| Launch announcement | All stakeholders | Communication Manager | Week 13 |
| Office hours (support) | All users | Repository Staff | Week 13-14 |

**Phase 5: Retention (Ongoing)**

| Activity | Audience | Owner | Frequency |
|----------|----------|-------|-----------|
| Usage tips newsletter | All users | Communication Manager | Monthly |
| Feature updates announcement | All users | Communication Manager | After each wave |
| User satisfaction survey | All users | Product Owner | Quarterly |
| Advanced training | Power users | Training Coordinator | Bi-annually |

---

## 7. Communication Plan

### 7.1 Communication Matrix

| Message | Audience | Channel | Frequency | Owner |
|---------|----------|---------|-----------|-------|
| **Project status** | Repository Manager, CIO | Email report | Weekly | Project Manager |
| **Demo** | Repository Manager, Gabriela, Faculty Deans | Video call | After each wave | Lead Developer |
| **PIA review** | Data Protection Officer | Meeting | Once (Week 1-2) | Project Manager |
| **Technical decisions** | Lead Developer, Data Engineer | Slack, meetings | Daily/weekly | Lead Developer |
| **User feedback** | Product Owner, Project Manager | Interviews, surveys | Weekly (pilot), monthly (post-launch) | Product Owner |
| **Feature announcement** | All stakeholders | Email, blog post | Major releases | Communication Manager |
| **Training materials** | Data stewards, repository staff | Documentation, webinar | Before launch, ongoing | Training Coordinator |
| **Support requests** | Repository Staff | Ticketing system, Slack | Ongoing | Support Team |
| **Usage metrics** | Repository Manager | Dashboard | Monthly | Data Engineer |
| **Retrospectives** | Development Team | Meeting | After each wave | Project Manager |

### 7.2 Communication Templates

#### Email Template: Project Status Update

```
Subject: Faculty Statistics Feature - Week [X] Update

Dear [Repository Manager],

**Progress This Week:**
- ✅ [Achievement 1]
- ✅ [Achievement 2]
- ⏳ [In Progress: Activity]

**Metrics:**
- Development: [X%] complete
- Testing: [Y%] complete
- User feedback: [Z] interviews completed

**Risks & Issues:**
- ⚠️ [Risk 1]: [Mitigation strategy]
- ✅ [Issue resolved]: [How it was fixed]

**Next Week:**
- [ ] [Activity 1]
- [ ] [Activity 2]

**Need Your Input:**
- [Question or decision needed]

Best regards,
[Your Name]
```

#### Email Template: Feature Announcement

```
Subject: NEW FEATURE: Faculty-Level Statistics Now Available! 📊

Dear [Stakeholders],

We're excited to announce the launch of **Faculty-Level Statistics** in 4TU.ResearchData!

**What's New:**
✅ View dataset counts per faculty
✅ Compare faculties (anonymized benchmarking)
✅ Visual dashboard with interactive charts
✅ Export to Excel for reports

**How to Access:**
1. Log in to 4TU.ResearchData
2. Navigate to Statistics → Faculty Statistics
3. Explore your faculty's research data output!

**Resources:**
- User Guide: [Link]
- Video Tutorial: [Link]
- FAQ: [Link]

**Need Help?**
- Office Hours: [Dates/Times]
- Email Support: support@4tu.nl

We'd love to hear your feedback! Please reply to this email or join our next feedback session on [Date].

Happy exploring!  
[Your Name]  
4TU.ResearchData Team
```

---

## 8. Influence & Decision-Making

### 8.1 Decision Authority Matrix (RACI)

**Key Decisions:**

| Decision | Responsible (Does the work) | Accountable (Final approval) | Consulted (Input) | Informed (Kept updated) |
|----------|----------------------------|------------------------------|-------------------|------------------------|
| **Feature scope** | Product Owner | Repository Manager | Gabriela, Faculty Deans, Lead Developer | All stakeholders |
| **Architecture** | Lead Developer | Repository Manager | Data Engineer, System Admin | Product Owner |
| **GDPR compliance** | Product Owner, Legal | Data Protection Officer | Repository Manager, Lead Developer | All stakeholders |
| **Timeline** | Project Manager | Repository Manager | Lead Developer, Product Owner | All stakeholders |
| **Budget** | Project Manager | CIO, Repository Manager | - | All stakeholders |
| **UI/UX design** | Product Owner | Repository Manager | Gabriela, Faculty Deans, Lead Developer | All stakeholders |
| **Go/No-Go launch** | Project Manager | Repository Manager | DPO, Lead Developer, CIO | All stakeholders |
| **Post-launch priorities** | Product Owner | Repository Manager | Users (via feedback) | All stakeholders |

### 8.2 Escalation Path

**Issue Severity Levels:**

| Level | Example | Escalation Path | Timeline |
|-------|---------|-----------------|----------|
| **Low** | Minor bug, cosmetic issue | → Support Team → Lead Developer | Resolve in next sprint |
| **Medium** | Feature request, data quality issue | → Product Owner → Repository Manager | Prioritize for next wave |
| **High** | Performance issue, security vulnerability | → Lead Developer → Repository Manager → CIO | Resolve within 1 week |
| **Critical** | GDPR breach, system down, data loss | → Project Manager → Repository Manager → CIO → DPO (if GDPR) | Immediate (24/7 on-call) |

**Escalation Example:**

```
User reports: "Dashboard is very slow (10+ seconds)"

1. Support Team investigates (Level: Medium → High if confirmed)
2. Escalate to Lead Developer (investigate root cause)
3. If database issue, involve Data Engineer
4. If requires significant refactoring, escalate to Repository Manager
5. Repository Manager decides: "Fix immediately" or "Defer to Wave 3"
6. Project Manager updates stakeholders
```

### 8.3 Conflict Resolution

**Common Conflicts:**

| Conflict | Stakeholders Involved | Resolution Strategy |
|----------|----------------------|---------------------|
| **Privacy vs. Transparency** | DPO (privacy) vs. Faculty Deans (want detailed data) | Balance: Aggregate stats OK, individual-level requires anonymization |
| **Timeline vs. Quality** | Repository Manager (fast launch) vs. Lead Developer (needs more time) | Phased delivery: MVP fast, enhancements later |
| **Scope Creep** | Faculty Deans (want more features) vs. Product Owner (control scope) | Backlog: Log requests, prioritize for future waves |
| **Resource Allocation** | Faculty Statistics (this feature) vs. Other Projects | Repository Manager decides based on strategic priorities |

**Resolution Process:**
1. **Identify conflict** (early detection)
2. **Understand root cause** (why do stakeholders disagree?)
3. **Explore options** (brainstorm solutions)
4. **Decide** (accountable person makes final call)
5. **Communicate** (explain decision to all parties)
6. **Document** (record decision and rationale)

---

## Appendix A: Stakeholder Contact List

| Stakeholder | Email | Phone | Preferred Contact |
|-------------|-------|-------|-------------------|
| **Repository Manager** | manager@4tu.nl | +31 XX XXX XXXX | Email (weekdays 9-17) |
| **Gabriela** | gabriela@4tu.nl | - | Email, Slack |
| **Faculty Dean (Aerospace)** | dean.ae@tudelft.nl | - | Email (formal) |
| **Faculty Dean (EEMCS)** | dean.eemcs@tudelft.nl | - | Email (formal) |
| **Faculty Dean (IDE)** | dean.ide@tudelft.nl | - | Email (formal) |
| **Data Protection Officer** | dpo@4tu.nl | +31 XX XXX XXXX | Email, meetings |
| **Lead Developer** | dev.lead@4tu.nl | - | Slack, stand-ups |
| **Data Engineer** | data.engineer@4tu.nl | - | Slack, email |
| **CIO** | cio@4tu.nl | +31 XX XXX XXXX | Email (executive summary only) |

---

## Appendix B: Stakeholder Engagement Tracker

**Use this table to track engagement activities:**

| Stakeholder | Last Contact | Next Planned Contact | Status | Notes |
|-------------|--------------|----------------------|--------|-------|
| Repository Manager | Dec 9, 2024 | Dec 16, 2024 (weekly meeting) | ✅ Engaged | Approved prototype |
| Gabriela | Dec 8, 2024 | Dec 15, 2024 (feedback session) | ✅ Engaged | Very positive feedback |
| Faculty Dean (Aerospace) | Nov 20, 2024 | Dec 12, 2024 (pilot invitation) | ⏳ Pending | Need to schedule demo |
| DPO | Not yet | Dec 10, 2024 (PIA review) | ⚠️ Critical | Must contact this week |
| Lead Developer | Dec 9, 2024 | Dec 10, 2024 (daily stand-up) | ✅ Engaged | Working on production code |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Dec 10, 2024 | Documentation Team | Initial stakeholder analysis |

**Next Review:** After Wave 1 pilot (estimated Week 6)

**Approval Required From:**
- [ ] Repository Manager
- [ ] Product Owner
- [ ] Project Manager

---

**END OF DOCUMENT**
