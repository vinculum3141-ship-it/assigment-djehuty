# Current System Analysis

This folder contains analysis of the **existing Djehuty codebase** to understand how data is currently stored and processed.

---

## 📄 Documents

### 1. CODEBASE_ANALYSIS.md (18 pages, ~45 min read)

**Purpose:** Comprehensive analysis of Djehuty's code structure, RDF schema, and SPARQL queries.

**Contents:**
- Section 1: Data Model & Ontology (RDF schema, entity relationships)
- Section 2: Organization & Institution Handling (how institutions are tracked)
- Section 3: Current Statistics Implementation (existing SPARQL queries)
- Section 4: Author Management (how authors are stored)
- Section 5: Account Management (user registration system)
- Section 6: Dataset Submission Workflow
- Section 7: Code Locations (where to find specific functionality)
- Section 8: SPARQL Query Patterns
- Section 9: Key Findings & Gaps

**When to read:**
- You're new to Djehuty
- You need to understand the RDF data model
- You're looking for specific code locations
- You need to know existing SPARQL query patterns

---

### 2. TECHNICAL_FINDINGS_SUMMARY.md (12 pages, ~30 min read)

**Purpose:** Executive summary of critical gaps and required changes.

**Contents:**
- Executive Summary
- Current Data Model (what exists today)
- Critical Gaps (what's missing for faculty statistics)
- Required Changes (what needs to be built)
- Organizations Field Analysis (why it's unparseable)
- Migration Strategy Options
- Performance Considerations
- Risk Assessment
- Effort Estimates

**When to read:**
- You need a quick technical overview
- You're making architectural decisions
- You need to understand what's missing
- You're estimating effort

---

### 3. DATASET_ANALYSIS.md (8 pages, ~25 min read)

**Purpose:** Analysis of production data patterns from live 4TU.ResearchData datasets.

**Contents:**
- Overview of 3 scraped datasets
- Author metadata patterns
- Organizations field analysis (real examples)
- ORCID profile analysis
- Edge cases and data quality issues
- Metadata structure examples

**When to read:**
- You need to understand real-world data
- You're planning data migration
- You need examples of Organizations field values
- You want to see edge cases

---

## 🎯 Key Findings

### What Exists Today

✅ **RDF/SPARQL-based architecture** with Virtuoso triple store  
✅ **Account entity** (~200 registered users) with institution_id  
✅ **Author entity** (~5,000+ all contributors) without institution/faculty tracking  
✅ **Organizations field** (custom field) containing faculty names but unparseable  
✅ **Statistics system** for basic metrics (views, downloads)

### What's Missing

❌ **No faculty_id predicate** on Account or Author entities  
❌ **No Faculty entity** for TU Delft's 8 faculties  
❌ **No faculty statistics** (datasets by faculty)  
❌ **Organizations field is free-text** - can't be aggregated  
❌ **No faculty selection** in dataset submission UI

### Critical Distinction Discovered

**Account vs Author:**
- `djht:Account` = Registered users who can log in (~200)
- `djht:Author` = ALL contributors on datasets (~5,000+)
- Most authors (like "Hebly, Scott J.") have **no account** - just names

This distinction is why we have two phases:
- **Phase 1:** Track faculty for depositors only (Account entity)
- **Phase 2:** Track faculty for all authors (Author entity)

---

## 🔍 Code Locations Quick Reference

From `CODEBASE_ANALYSIS.md` Section 7:

| Component | File Path |
|-----------|-----------|
| RDF schema | `djehuty/src/djehuty/rdf/schema.ttl` |
| Database layer | `djehuty/src/djehuty/database.py` |
| Account SPARQL | `djehuty/src/djehuty/web/resources/sparql/accounts.sparql` |
| Dataset SPARQL | `djehuty/src/djehuty/web/resources/sparql/datasets.sparql` |
| Statistics SPARQL | `djehuty/src/djehuty/web/resources/sparql/statistics.sparql` |
| UI templates | `djehuty/src/djehuty/web/resources/html/*.html` |
| Account management | `djehuty/src/djehuty/ui.py` (accounts_* functions) |

---

## 📊 Organizations Field Examples

From real production datasets (see `DATASET_ANALYSIS.md`):

**Dataset 1 (Aerospace):**
```
Organizations:
- Faculty of Aerospace Engineering, TU Delft
- Faculty of Aerospace Engineering
```

**Dataset 2 (Multi-faculty):**
```
Organizations:
- Faculty of Aerospace Engineering, Delft University of Technology
- Faculty of Civil Engineering and Geosciences, Delft University of Technology
```

**Problem:** Free-text, inconsistent formatting, can't be parsed for aggregation.

---

## 🚀 Next Steps After Reading

**For developers:**
1. Read these current system documents (1-2 hours)
2. Move to `../assignment/` folder
3. Read `ARCHITECTURE_SUMMARY.md` for solution overview
4. Read `SOLUTION_ARCHITECTURE.md` for implementation details

**For architects:**
1. Read `TECHNICAL_FINDINGS_SUMMARY.md` (30 min)
2. Review `CODEBASE_ANALYSIS.md` Sections 1-3 (30 min)
3. Move to `../assignment/SOLUTION_ARCHITECTURE.md` Sections 1-6

**For project managers:**
1. Skim `TECHNICAL_FINDINGS_SUMMARY.md` Sections 1-2, 7-8 (15 min)
2. Move to `../assignment/PRESENTATION_OUTLINE.md`

---

## 💡 Key Insights

1. **Djehuty uses RDF triples, not relational database** - all data is subject-predicate-object
2. **SPARQL is the query language** - like SQL but for RDF
3. **Virtuoso is the triple store** - runs in Docker on port 8890
4. **Existing institution_id is depositor-only** - only tracks who uploaded, not all authors
5. **Organizations field was intended for display, not aggregation** - no structured data

---

*After understanding the current system, proceed to `../assignment/` for the solution specification.*
