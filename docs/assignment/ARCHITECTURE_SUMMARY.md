# Faculty-Level Statistics: Architecture Summary

**Quick Reference Guide**

---

## 📋 Overview

**Problem:** 4TU.ResearchData needs faculty-level statistics but currently only tracks institutional affiliation.

**Solution:** Extend RDF data model with Faculty entity, add faculty selection to user workflows, migrate existing data.

**Timeline:** 5 weeks | **Effort:** 1 developer | **Accuracy:** ≥90% migration

---

## 🏗️ Architecture Components

### 1. Data Model (RDF Extensions)

```
NEW Entity: djht:Faculty
├── id (integer)
├── name (string)
├── short_name (string)
├── code (string)
├── institution_id (integer)
└── url (URI)

EXTENDED Entities:
├── Account + faculty_id
├── Dataset + faculty_id
└── Author + faculty_id (optional)
```

**Storage:** Virtuoso RDF triple store  
**Query:** SPARQL templates with Jinja2

### 2. System Components

```
Presentation Layer
├── Registration UI (faculty dropdown)
├── Dataset Form UI (faculty field)
└── Statistics Dashboard (faculty breakdown)

Application Layer
├── FacultyManager (taxonomy management)
├── FacultyStatisticsService (aggregation)
└── FacultyMigrationService (data migration)

Data Layer
├── SPARQL Templates (faculties.sparql, statistics_faculty.sparql)
└── Database Methods (insert_faculty, faculty_statistics)
```

### 3. API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v2/institutions/{id}/faculties` | GET | List faculties |
| `/v2/faculties/{id}` | GET | Faculty details |
| `/v2/statistics/faculties` | GET | Faculty statistics |
| `/v2/statistics/faculties/{id}/datasets` | GET | Faculty datasets |
| `/v2/account` | PATCH | Update account faculty |

---

## 🔄 Migration Strategy

### 3-Phase Approach

**Phase 1: Automated Detection (70-80%)**
- Parse Organizations field using regex patterns
- Auto-assign high-confidence matches (≥0.8)
- Flag medium/low confidence for review

**Phase 2: Manual Review (15-20%)**
- CSV export of flagged cases
- Human validation and assignment
- Import reviewed assignments

**Phase 3: Validation (100%)**
- Referential integrity checks
- Statistics consistency validation
- Quality assurance sign-off

### Confidence Scoring

```
High (≥0.8):    AUTO_ASSIGN (450 datasets)
Medium (0.5-0.8): MANUAL_REVIEW (80 datasets)
Low (<0.5):      MANUAL_REVIEW (50 datasets)
Total:           580 datasets
```

---

## 📊 Faculty Taxonomy (TU Delft Example)

```
TU Delft (28586)
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

**Configuration:** XML file (`djehuty.xml`) with version control

---

## 🎯 Key Decisions

### 1. Data Model

**Decision:** Add `faculty_id` as optional predicate to Account/Dataset/Author  
**Rationale:** Backward compatible, flexible for future enhancements  
**Alternative Rejected:** Replace Organizations field (would lose historical data)

### 2. Migration Approach

**Decision:** Hybrid (automated + manual review)  
**Rationale:** Balance accuracy and effort  
**Alternative Rejected:** Fully manual (too slow), fully automated (insufficient accuracy)

### 3. UI Integration

**Decision:** Faculty dropdown at registration, auto-fill in dataset form  
**Rationale:** Capture at source, minimize user effort  
**Alternative Rejected:** Post-deposit tagging (lower adoption)

### 4. Statistics Aggregation

**Decision:** SPARQL GROUP BY with caching  
**Rationale:** Leverage existing infrastructure, good performance  
**Alternative Rejected:** Application-level aggregation (slower, more complex)

---

## ⚙️ Implementation Phases

### Phase 1: Foundation (Weeks 1-2)
- [ ] RDF schema design
- [ ] XML faculty configuration
- [ ] Database insertion methods
- [ ] SPARQL query templates
- [ ] Unit tests

### Phase 2: API & Services (Weeks 2-3)
- [ ] FacultyManager service
- [ ] Statistics service
- [ ] API endpoints
- [ ] Integration tests

### Phase 3: Migration (Weeks 3-4)
- [ ] Migration scripts
- [ ] Pattern detection
- [ ] Manual review
- [ ] Bulk import
- [ ] Validation

### Phase 4: UI Development (Weeks 4-5)
- [ ] Registration form
- [ ] Dataset form
- [ ] Statistics dashboard
- [ ] Charts and visualizations

### Phase 5: Testing & Deployment (Week 5)
- [ ] E2E testing
- [ ] UAT
- [ ] Documentation
- [ ] Production deployment

---

## 📈 Success Metrics

### Technical
- ✅ API response time < 100ms
- ✅ Migration accuracy ≥ 90%
- ✅ Test coverage ≥ 80%
- ✅ Zero breaking changes

### User
- ✅ ≥80% faculty selection rate
- ✅ ≥90% datasets with faculty_id
- ✅ User satisfaction ≥4/5

### Business
- ✅ Faculty statistics for all 4TU institutions
- ✅ Exportable reports
- ✅ Adoption by 3+ institutions

---

## 🔐 Security & Performance

### Security
- Input validation on all faculty_id values
- SPARQL injection prevention (parameterized queries)
- Audit logging for all assignments
- No GDPR concerns (institutional data)

### Performance
- Multi-layer caching (in-memory, file-based)
- Virtuoso indexing on faculty_id
- Query optimization with OPTIONAL clauses
- Target: <100ms for statistics

---

## ⚠️ Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| **Migration Errors** | Dry-run testing, backups, rollback plan |
| **Performance Issues** | Load testing, caching, query optimization |
| **User Confusion** | Clear UI, help text, training docs |
| **Scope Creep** | Fixed feature set, phase 2 roadmap |

---

## 🚀 Quick Start Commands

### 1. Export Datasets for Migration
```bash
python scripts/export_datasets_for_migration.py
```

### 2. Detect Faculty Patterns
```bash
python scripts/detect_faculty_patterns.py
```

### 3. Import Faculty Assignments (Dry Run)
```bash
python scripts/import_faculty_assignments.py --dry-run
```

### 4. Import Faculty Assignments (Production)
```bash
python scripts/import_faculty_assignments.py
```

### 5. Validate Migration
```bash
python scripts/validate_migration.py
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `SOLUTION_ARCHITECTURE.md` | **Full architecture document (this file)** |
| `CODEBASE_ANALYSIS.md` | Detailed code structure analysis |
| `TECHNICAL_FINDINGS_SUMMARY.md` | Technical findings and gaps |
| `DATASET_ANALYSIS.md` | Production data patterns |
| `README.txt` | Original project readme |

---

## 💡 Future Enhancements (Phase 2)

1. **Department-Level Granularity**
   - Add Department entity below Faculty
   - Multi-level hierarchy (Institution → Faculty → Department)

2. **Multi-Faculty Attribution**
   - Support datasets with multiple faculties
   - Proportional counting in statistics

3. **Research Group Tracking**
   - Add ResearchGroup entity
   - Link datasets to specific research groups

4. **ORCID Integration**
   - Fetch faculty from ORCID if available
   - Auto-suggest faculty based on ORCID data

5. **Advanced Analytics**
   - Time-series faculty trends
   - Inter-faculty collaboration metrics
   - Geographic distribution of collaborators

6. **Admin UI**
   - Web interface for faculty taxonomy management
   - Bulk edit faculty assignments
   - Migration review dashboard

---

## 🎓 TU Delft Faculty Codes Reference

| Code | Faculty |
|------|---------|
| AE / LR | Aerospace Engineering |
| A+BE / BK | Architecture and Built Environment |
| AS / TNW | Applied Sciences |
| CEG / CiTG | Civil Engineering and Geosciences |
| EEMCS / EWI | Electrical Engineering, Math & CS |
| IDE / IO | Industrial Design Engineering |
| ME / 3mE | Mechanical Engineering |
| TPM / TBM | Technology, Policy and Management |

---

## 📞 Contact & Support

**Technical Questions:** See detailed architecture in `SOLUTION_ARCHITECTURE.md`  
**Migration Support:** Refer to scripts in `/scripts/` directory  
**API Documentation:** Section 6 of main architecture document

---

*Last Updated: December 9, 2025*
