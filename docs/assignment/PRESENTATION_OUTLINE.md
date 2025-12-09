# Presentation Outline: Faculty-Level Statistics for 4TU.ResearchData

**Duration:** 10-15 minutes  
**Audience:** Technical stakeholders, product owners  
**Goal:** Present conceptual design and technical approach for faculty-level statistics feature

---

## Slide 1: Title & Introduction (1 min)

**Title:** Faculty-Level Statistics for 4TU.ResearchData Repository  
**Subtitle:** Conceptual Design & Technical Approach

**Speaker Notes:**
- Introduction: "I'm presenting a solution architecture for adding faculty-level statistics to the Djehuty repository system"
- Context: "4TU.ResearchData currently tracks datasets at institutional level - we need to break this down by faculty"

---

## Slide 2: Problem Statement (1-2 min)

**Current State:**
- ❌ Only institution-level tracking (e.g., "TU Delft")
- ❌ "Organizations" field is free-text (unusable for aggregation)
- ❌ Multi-author datasets only counted for depositor's institution
- ❌ No way to generate faculty reports

**Example:**
```
Dataset: "Wing Aerodynamics Study"
Current: Counted for "TU Delft" ✓
Needed:  Counted for "Faculty of Aerospace Engineering" ✗
```

**Impact:**
- Faculties cannot track research output
- Institutional reports lack granularity
- Strategic planning decisions lack data

**Speaker Notes:**
- Show example dataset from production: "Aviation NOx Emissions"
- Highlight Organizations field: "TU Delft, Faculty of Aerospace Engineering, Section Aircraft Noise..."
- "This free-text format works for display but not for statistics"

---

## Slide 3: Proposed Solution Overview (2 min)

**High-Level Approach:**

```
1. Extend RDF Data Model
   └── Add Faculty entity and faculty_id predicate

2. Capture Faculty at Source
   └── Registration form + Dataset deposit form

3. Migrate Historical Data
   └── Parse Organizations field + Manual review

4. Generate Statistics
   └── SPARQL aggregation with caching
```

**Key Benefits:**
- ✅ Accurate faculty-level attribution
- ✅ Better insights for faculties and institutions
- ✅ Backward compatible (no breaking changes)
- ✅ Extensible (can add departments later)

**Speaker Notes:**
- "The solution has four main components"
- "Most importantly, it's additive - existing functionality continues to work"
- "We're not removing the Organizations field, just adding structured data alongside it"

---

## Slide 4: Technical Architecture (3 min)

**System Architecture Diagram:**

```
┌─────────────────────────────────────────────────┐
│           Presentation Layer                    │
│  ┌──────────────┐  ┌─────────────────────────┐ │
│  │ Registration │  │ Statistics Dashboard    │ │
│  │ (Faculty    │  │ (Faculty breakdown)     │ │
│  │  Dropdown)   │  │                         │ │
│  └──────────────┘  └─────────────────────────┘ │
└─────────────┬───────────────────────────────────┘
              │ REST API
┌─────────────┴───────────────────────────────────┐
│          Application Layer                      │
│  ┌────────────────────────────────────────────┐ │
│  │ FacultyManager | StatisticsService        │ │
│  │ MigrationService                           │ │
│  └────────────────────────────────────────────┘ │
└─────────────┬───────────────────────────────────┘
              │ SPARQL Queries
┌─────────────┴───────────────────────────────────┐
│          Data Layer (RDF)                       │
│  Account ──faculty_id──→ Faculty ←── Dataset   │
│                            ↓                    │
│                      (statistics)               │
└─────────────────────────────────────────────────┘
```

**RDF Schema Extension:**

```turtle
# NEW Entity
djht:Faculty rdf:type owl:Class .

# NEW Predicates
djht:faculty_id → Links Account/Dataset to Faculty
djht:faculty_name → Faculty display name
djht:institution_id → Faculty belongs to Institution
```

**Speaker Notes:**
- "We're extending the existing RDF schema with a Faculty entity"
- "This sits between Institution and individual researchers"
- "Faculty_id is optional, maintaining backward compatibility"
- "All queries use existing SPARQL infrastructure"

---

## Slide 5: Data Model & Faculty Taxonomy (2 min)

**Faculty Taxonomy (TU Delft Example):**

```
TU Delft (Institution ID: 28586)
├── Faculty of Aerospace Engineering (285860001)
├── Faculty of Architecture and Built Environment (285860002)
├── Faculty of Applied Sciences (285860003)
├── Faculty of Civil Engineering and Geosciences (285860004)
├── Faculty of EEMCS (285860005)
├── Faculty of Industrial Design Engineering (285860006)
├── Faculty of Mechanical Engineering (285860007)
├── Faculty of TPM (285860008)
└── Other / Unspecified (285860999)
```

**Configuration (XML):**

```xml
<group id="28586" name="TU Delft">
  <faculties>
    <faculty id="285860001" code="AE">
      <name>Faculty of Aerospace Engineering</name>
      <short-name>AE</short-name>
    </faculty>
    <!-- ... more faculties ... -->
  </faculties>
</group>
```

**Speaker Notes:**
- "Faculty taxonomy is configuration-driven, not hardcoded"
- "Each institution can define their own faculty structure"
- "TU Delft has 8 faculties - this is based on their official structure"
- "Configuration is version-controlled and validated before deployment"

---

## Slide 6: User Experience (2 min)

**1. Registration: Faculty Selection**

```
┌──────────────────────────────────────┐
│  Complete Your Profile               │
├──────────────────────────────────────┤
│  Email: john.doe@tudelft.nl ✓       │
│  Institution: TU Delft (detected)    │
│                                      │
│  Faculty *                           │
│  ┌────────────────────────────────┐ │
│  │ Select Faculty...          ▼  │ │
│  └────────────────────────────────┘ │
│                                      │
│  [ Save & Continue ]                 │
└──────────────────────────────────────┘
```

**2. Dataset Deposit: Auto-Fill**

```
┌──────────────────────────────────────┐
│  Dataset Metadata                    │
├──────────────────────────────────────┤
│  Title: Wing Aerodynamics Study      │
│                                      │
│  Faculty                             │
│  ┌────────────────────────────────┐ │
│  │ Aerospace Eng. (from profile)│ │
│  └────────────────────────────────┘ │
│  (can be changed if needed)          │
│                                      │
│  [ Publish ]                         │
└──────────────────────────────────────┘
```

**3. Statistics Dashboard**

```
Faculty                    │ Datasets │ Downloads
──────────────────────────┼──────────┼──────────
Aerospace Engineering     │    42    │   3,500
Civil Engineering         │    38    │   2,800
Applied Sciences          │    35    │   2,100
```

**Speaker Notes:**
- "User experience is streamlined - faculty selected once at registration"
- "Auto-filled in dataset form to minimize effort"
- "Can override if dataset belongs to different faculty"
- "Statistics dashboard provides clear breakdown by faculty"

---

## Slide 7: Migration Strategy (2-3 min)

**Challenge:** 580+ existing datasets need faculty assignment

**Solution: Hybrid Approach**

**Phase 1: Automated Detection (70-80% coverage)**

```python
# Pattern matching on Organizations field
"TU Delft, Faculty of Aerospace Engineering..."
    ↓ Pattern: r"Aerospace Engineering"
    ↓ Confidence: 0.95
    → AUTO-ASSIGN: faculty_id = 285860001
```

**Phase 2: Manual Review (15-20%)**

```csv
uuid,title,organizations,suggested_faculty,confidence
abc123,"Building Study","TU Delft",285860002,0.6
def456,"Materials Research","TU Delft",NULL,0.0
```

**Phase 3: Validation**
- Referential integrity checks
- Statistics consistency validation
- Quality assurance sign-off

**Expected Results:**
- ✅ 450 datasets auto-assigned (confidence ≥0.8)
- ⚠️ 130 datasets manual review needed
- 🎯 Target: ≥90% accuracy

**Speaker Notes:**
- "We can't achieve 100% automated accuracy due to free-text variations"
- "Hybrid approach balances efficiency and accuracy"
- "Manual review is manageable - 130 datasets over 2 weeks"
- "CSV export makes review process straightforward"

---

## Slide 8: API Design (1-2 min)

**New Endpoints:**

```http
GET /v2/institutions/28586/faculties
→ List all faculties for TU Delft

GET /v2/statistics/faculties?institution=28586
→ Faculty-level statistics
{
  "statistics": [
    {
      "faculty_id": 285860001,
      "faculty_name": "Faculty of Aerospace Engineering",
      "datasets": 42,
      "total_downloads": 3500
    }
  ]
}

PATCH /v2/account
→ Update user's faculty
{ "faculty_id": 285860001 }
```

**Backward Compatibility:**
- All endpoints optional (no breaking changes)
- Existing queries continue to work
- Faculty fields return `null` if not set

**Speaker Notes:**
- "API is RESTful and follows existing patterns"
- "Faculty field is optional everywhere - backward compatible"
- "Response format matches existing statistics endpoints"

---

## Slide 9: Implementation Timeline (1 min)

**5-Week Implementation Plan:**

| Week | Phase | Deliverables |
|------|-------|--------------|
| 1-2 | Foundation | RDF schema, config, DB methods |
| 2-3 | API & Services | Endpoints, statistics service |
| 3-4 | Migration | Scripts, detection, bulk import |
| 4-5 | UI Development | Forms, dashboard, charts |
| 5 | Testing & Deploy | UAT, docs, production |

**Resource Requirements:**
- 1 Full-stack developer (5 weeks)
- Institutional input for faculty taxonomy validation
- User acceptance testing participation

**Speaker Notes:**
- "Timeline is realistic based on codebase analysis"
- "Phases can overlap slightly for efficiency"
- "Critical path: Migration quality depends on faculty taxonomy accuracy"

---

## Slide 10: Advantages & Trade-offs (2 min)

**✅ Advantages:**

1. **Accuracy**
   - Structured data vs free-text
   - Validated against official faculty list
   
2. **Performance**
   - SPARQL aggregation (database-level)
   - Multi-layer caching
   - Target: <100ms response time

3. **Maintainability**
   - Configuration-driven taxonomy
   - No hardcoded faculty lists
   - Easy to extend to other institutions

4. **User Experience**
   - Minimal clicks (select once)
   - Auto-fill reduces effort
   - Clear visualization

5. **Future-Proof**
   - Can add departments later
   - Can support multi-faculty attribution
   - Extensible to research groups

**⚠️ Trade-offs:**

1. **Migration Effort**
   - Need manual review for ~130 datasets
   - Estimated 2 weeks for complete migration
   - **Mitigation:** Hybrid approach, clear workflow

2. **User Burden**
   - Extra field during registration
   - Possible confusion about faculty vs department
   - **Mitigation:** Help text, optional initially

3. **Maintenance**
   - Faculty taxonomy needs updates when organizational changes occur
   - **Mitigation:** Version-controlled config, clear change process

4. **Historical Data Gaps**
   - Some old datasets may lack reliable faculty data
   - **Mitigation:** Accept ~10% "Other/Unspecified" category

**Speaker Notes:**
- "No solution is perfect - we've balanced accuracy with effort"
- "Migration is the biggest challenge, but manageable"
- "User burden is minimal - one dropdown during registration"
- "Future benefits outweigh initial investment"

---

## Slide 11: Risk Mitigation (1 min)

**Top Risks & Mitigation:**

| Risk | Mitigation Strategy |
|------|---------------------|
| **Data Migration Errors** | • Dry-run testing<br>• Backup before import<br>• Rollback plan |
| **Performance Issues** | • Load testing<br>• Caching strategy<br>• Query optimization |
| **Low User Adoption** | • Clear UI/UX<br>• Training materials<br>• Make optional initially |
| **Faculty Taxonomy Changes** | • Version control<br>• Documented change process |

**Speaker Notes:**
- "We've identified and planned for key risks"
- "Most important: Data migration quality - hence hybrid approach"
- "Performance tested in dev environment before production"

---

## Slide 12: Success Metrics (1 min)

**How We'll Measure Success:**

**Technical:**
- ✅ API response time < 100ms
- ✅ Migration accuracy ≥ 90%
- ✅ Test coverage ≥ 80%
- ✅ Zero breaking changes

**User:**
- ✅ ≥80% of new users select faculty
- ✅ ≥90% of new datasets have faculty_id
- ✅ User satisfaction ≥4/5

**Business:**
- ✅ Faculty statistics for all 4TU institutions
- ✅ Exportable reports available
- ✅ Feature adopted by 3+ institutions

**Speaker Notes:**
- "Success is measurable and concrete"
- "Technical metrics ensure quality and performance"
- "User metrics validate adoption and usability"
- "Business metrics confirm value delivery"

---

## Slide 13: Next Steps & Recommendations (1 min)

**Immediate Next Steps:**

1. **Stakeholder Validation** (Week 0)
   - Review and approve TU Delft faculty taxonomy
   - Confirm feature requirements
   - Identify other 4TU institutions interested

2. **Development Kickoff** (Week 1)
   - Assign developer resources
   - Set up development environment
   - Create project backlog

3. **Pilot with TU Delft** (Weeks 1-5)
   - Implement for single institution first
   - Validate approach before scaling
   - Gather user feedback

4. **Rollout to 4TU** (Weeks 6-8)
   - Extend to other institutions
   - Customize faculty taxonomies
   - Final testing and deployment

**Recommendation:**
- ✅ Approve solution architecture
- ✅ Proceed with Phase 1 (Foundation)
- ✅ Use TU Delft as pilot institution
- ✅ Plan rollout to other 4TU partners after validation

**Speaker Notes:**
- "We recommend starting with TU Delft as pilot"
- "Validates approach before investing in all institutions"
- "Allows us to refine based on real usage"
- "Total timeline: 8 weeks to full 4TU rollout"

---

## Slide 14: Q&A (Remaining time)

**Anticipated Questions:**

**Q: Why not just parse the Organizations field?**  
A: Free-text format has too many variations. Pattern matching achieves ~80% accuracy. We need ≥90% for reliable statistics.

**Q: What about datasets with authors from multiple faculties?**  
A: Phase 1 assigns to depositor's faculty. Phase 2 (future) can support multi-faculty attribution.

**Q: How do we handle faculty reorganizations?**  
A: Configuration-based approach allows updates without code changes. Migration scripts can reassign datasets.

**Q: Performance impact on existing queries?**  
A: Minimal - faculty_id is optional field with indexed queries. Existing statistics unaffected.

**Q: Can users change their faculty after registration?**  
A: Yes - editable in profile settings. Dataset faculty can also be overridden per-dataset.

**Q: What if ORCID has faculty information?**  
A: Currently ORCID shows institution only. If enhanced in future, we can auto-populate from ORCID.

---

## Supporting Materials

**Provided Documents:**

1. **SOLUTION_ARCHITECTURE.md** (61 pages)
   - Complete technical specification
   - All code examples and SPARQL queries
   - Full migration scripts

2. **ARCHITECTURE_SUMMARY.md** (Quick reference)
   - Component overview
   - Key decisions
   - Quick start guide

3. **CODEBASE_ANALYSIS.md**
   - Current system analysis
   - Code locations
   - Gap analysis

4. **TECHNICAL_FINDINGS_SUMMARY.md**
   - Data model review
   - Statistics query analysis
   - Performance considerations

5. **DATASET_ANALYSIS.md**
   - Production data patterns
   - Organizations field analysis
   - Edge cases

---

## Presentation Tips

**Time Management:**
- **Slides 1-3:** 4 min (Problem + Solution)
- **Slides 4-6:** 7 min (Technical details)
- **Slides 7-8:** 3 min (Migration + API)
- **Slides 9-13:** 5 min (Implementation + Conclusion)
- **Slide 14:** 5 min (Q&A buffer)

**Key Messages:**
1. "Faculty-level statistics are essential for institutional reporting"
2. "Solution is backward-compatible and extensible"
3. "Hybrid migration balances accuracy and effort"
4. "5-week implementation timeline with clear deliverables"

**Demo Opportunities:**
- Show production dataset with Organizations field
- Live query of current statistics (institution-level only)
- Mockup of proposed statistics dashboard with faculty breakdown

**Emphasis Points:**
- ⭐ Backward compatibility (no breaking changes)
- ⭐ Configuration-driven (easy to maintain)
- ⭐ Realistic migration plan (90% accuracy target)
- ⭐ Clear success metrics (measurable outcomes)

---

*End of Presentation Outline*
