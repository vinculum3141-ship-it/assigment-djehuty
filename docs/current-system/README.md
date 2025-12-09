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

---

### 3. DATASET_ANALYSIS.md (8 pages, ~20 min read)

**Purpose:** Analysis of live datasets from 4TU.ResearchData to understand real-world data.

**Contents:**
- Live dataset scraping results (3 datasets)
- ORCID profile analysis (1 author)
- Institution data format examples
- Author metadata structure
- Data quality observations

**When to read:**
- You need real-world examples
- You're designing data parsers
- You want to see actual dataset metadata

---

### 4. ⭐ **NEW** INSTITUTION_STATISTICS_GUIDE.md (15 pages, ~35 min read)

**Purpose:** Step-by-step guide explaining how the current system displays institution-level statistics.

**Contents:**
- How to access the portal home page statistics
- Institution tiles and navigation
- Individual institution pages (`/institutions/<name>`)
- Backend code flow and SPARQL queries
- RDF data model for institutions
- What's missing (the assignment gap)
- How to run and test the current portal
- Key files reference (Python, SPARQL, HTML templates)

**When to read:**
- ✅ **You want to understand how institution statistics currently work**
- You need to see where to add faculty statistics
- You're looking for code examples to extend
- You want to test the current system before implementing changes
- You need to understand the UI/UX patterns

---

### 5. ⭐ **NEW** STATISTICS_OUTPUT_EXAMPLES.md (12 pages, ~30 min read)

**Purpose:** Shows the exact output format of statistics queries in the current system and what Phase 1 needs to produce.

**Contents:**
- Repository-wide statistics output (Python dict format)
- Portal HTML display with formatting
- Institution-specific data (what exists vs. what's missing)
- SPARQL query output examples (JSON bindings)
- Phase 1 expected output formats (API responses)
- HTML dashboard mockup for faculty statistics
- Current vs. Phase 1 comparison table
- Testing instructions to query current system

**When to read:**
- ✅ **You want to know the exact output format of institution-wide statistics**
- You're designing API responses for Phase 1
- You need to understand SPARQL output structure
- You're writing tests and need expected data formats
- You want to see what the dashboard should display

---

### 6. ⭐ **NEW** STATISTICS_DEFINITION_CLARIFICATION.md (20 pages, ~50 min read)

**Purpose:** Resolves ambiguity in "statistics per institute" requirement by providing clear definitions based on current implementation patterns.

**Contents:**
- The ambiguity problem (what metrics? what granularity? depositor vs author?)
- Learning from current implementation (repository-wide patterns)
- Proposed definition (extending existing patterns to faculty level)
- What "statistics" should include (Tier 1-4 metrics with priorities)
- Extending current implementation pattern (repository → institution → faculty)
- Concrete examples (API responses, HTML dashboard, SPARQL queries)
- Minimum viable statistics (Phase 1 scope: MUST/SHOULD/NICE TO HAVE)
- Implementation checklist with validation criteria
- Clear resolution: What to build vs. what to skip

**When to read:**
- ✅ **The assignment feels vague about "statistics per institute"**
- ✅ **You need to decide which metrics to include**
- ✅ **You're uncertain about scope boundaries**
- You need stakeholder alignment on requirements
- You want to extend current patterns correctly
- You're writing the technical specification
- You need validation criteria for testing

---

### 7. ⭐ **NEW** CURRENT_STATISTICS_IMPLEMENTATION.md (25 pages, ~60 min read)

**Purpose:** Complete documentation of current statistics implementation WITHOUT any Phase 1 extension discussion.

**Contents:**
- Repository-wide statistics (what exists today)
- Complete source code with explanations
- SPARQL query details (datasets, authors, collections)
- Portal home page implementation
- Institution pages (list view, not statistics)
- RDF data model for institutions
- Data flow diagrams
- Testing instructions
- Key files reference
- What does NOT exist (gaps)

**When to read:**
- ✅ **You want to focus ONLY on current implementation**
- ✅ **You don't want Phase 1 extension discussion yet**
- You're learning how Djehuty statistics work today
- You need complete source code examples
- You want to understand the data flow
- You're testing the current portal
- You need a reference for "as-is" state

---

## 📋 Quick Decision Guide

**"I just want to understand the current implementation, ignore Phase 1 extensions"**
→ Read **CURRENT_STATISTICS_IMPLEMENTATION.md** (pure as-is documentation, no future plans)

**"The assignment is vague about 'statistics per institute' - what should I build?"**
→ Read **STATISTICS_DEFINITION_CLARIFICATION.md** (complete analysis with clear recommendations)

**"What metrics should be included in faculty statistics?"**
→ Read **STATISTICS_DEFINITION_CLARIFICATION.md** Section "What Statistics Should Include"

**"What is the output of institution-wide statistics?"**
→ Read **STATISTICS_OUTPUT_EXAMPLES.md** (shows exact data formats and outputs)

**"How do I display stats per institute in the current implementation?"**
→ Read **INSTITUTION_STATISTICS_GUIDE.md** (shows you exactly how it works today)

**"I'm new to Djehuty, where do I start?"**
→ Read **CODEBASE_ANALYSIS.md** then **TECHNICAL_FINDINGS_SUMMARY.md**

**"What's missing for faculty statistics?"**
→ Read **TECHNICAL_FINDINGS_SUMMARY.md** Section 3 (Critical Gaps)

**"I need real-world data examples"**
→ Read **DATASET_ANALYSIS.md**

**"Where is the code for X?"**
→ Search **CODEBASE_ANALYSIS.md** Section 7 (Code Locations)

**"How are SPARQL queries structured?"**
→ Read **CODEBASE_ANALYSIS.md** Section 8 (SPARQL Query Patterns)

**"What's the current RDF schema?"**
→ Read **CODEBASE_ANALYSIS.md** Section 1 (Data Model & Ontology)

**"What format should my API return for Phase 1?"**
→ Read **STATISTICS_OUTPUT_EXAMPLES.md** (Phase 1 expected outputs section)

**"How do I extend the current pattern correctly?"**
→ Read **STATISTICS_DEFINITION_CLARIFICATION.md** Section "Extending Current Implementation Pattern"

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
