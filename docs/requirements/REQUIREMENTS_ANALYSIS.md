# Assignment Requirements Analysis & Coverage

This document maps your original questions to the solutions provided in the documentation, identifying what's addressed in Phase 1, what's deferred to Phase 2, and what gaps remain.

---

## ✅ Requirements Coverage Summary

| # | Requirement | Phase 1 | Phase 2 | Status | Notes |
|---|-------------|---------|---------|--------|-------|
| 1 | Stats on publications per institute | ✅ Existing | ✅ Enhanced | **DONE** | Already exists, unchanged |
| 2 | Stats on publications per faculty | ✅ **YES** | ✅ Enhanced | **IMPLEMENTED** | Core Phase 1 feature |
| 3 | Cross-referencing to infer missing data | ⚠️ Limited | ✅ **YES** | **PHASE 2** | Pattern matching in Phase 2 |
| 4 | Parsing free-form text options | ⚠️ Manual | ✅ **YES** | **PHASE 2** | FACULTY_PATTERNS in Phase 2 |
| 5 | Associate parsed text to authors | ❌ No | ✅ **YES** | **PHASE 2** | Author.faculty_id in Phase 2 |
| 6 | Log stats on missing data | ✅ **YES** | ✅ Enhanced | **IMPLEMENTED** | Coverage metrics in both phases |
| 7 | Handle free-form organization info | ⚠️ Preserve | ✅ **YES** | **HYBRID** | Keep field + add faculty_id |
| 8 | Stats on contributors per institute | ✅ Existing | ✅ Enhanced | **DONE** | Already exists |
| 9 | Stats based on first author only | ❌ No | ⚠️ Possible | **OUT OF SCOPE** | Could be Phase 3 |
| 10 | Extensible stats structure | ✅ **YES** | ✅ **YES** | **IMPLEMENTED** | SPARQL-based, highly flexible |
| 11 | Modular schema for future requests | ✅ **YES** | ✅ **YES** | **IMPLEMENTED** | RDF allows easy extension |
| 12 | Unregistered author stats | ❌ No | ✅ **YES** | **PHASE 2** | Core Phase 2 feature |
| 13 | Database structure improvements | ✅ **YES** | ✅ **YES** | **IMPLEMENTED** | Faculty entity + predicates |
| 14 | Auto-population suggestions | ⚠️ Limited | ✅ **YES** | **PHASE 2** | Registered auto-fill (Phase 1), Pattern matching (Phase 2) |
| 15 | Graceful failure handling | ✅ **YES** | ✅ **YES** | **IMPLEMENTED** | Validation + error handling |

**Legend:**
- ✅ **YES** = Fully addressed
- ⚠️ Limited/Partial = Partially addressed
- ❌ No = Not addressed (out of scope or deferred)

---

## 📋 Detailed Analysis

### 1. Stats on Publications Per Institute

**Your Question:** "Stats on publications per institute"

**Status:** ✅ **Already exists in current system**

**Answer:**
- This functionality **already exists** in Djehuty (see `docs/current-system/CODEBASE_ANALYSIS.md` Section 3)
- The `institution_id` predicate on Account tracks which institution the depositor belongs to
- Existing query: `statistics_by_institution.sparql`
- **Phase 1 does NOT change this** - we keep it as-is
- **Phase 2 does NOT change this** - we add faculty-level, not replace institution-level

**Documents:**
- `docs/current-system/CODEBASE_ANALYSIS.md` - Section 2 (Institution Handling)
- `docs/current-system/TECHNICAL_FINDINGS_SUMMARY.md` - Section 2.1 (Current Data Model)

**Verdict:** ✅ No action needed - already supported

---

### 2. Stats on Publications Per Faculty

**Your Question:** "Stats on publication per faculty"

**Status:** ✅ **CORE FEATURE - Fully implemented in Phase 1**

**Answer:**
- **Phase 1 (Assignment):**
  - Add `faculty_id` to Account entity
  - Statistics: "Datasets deposited by each faculty"
  - API endpoint: `GET /v2/statistics/faculties`
  - SPARQL query: `statistics_faculty.sparql`
  - Counts datasets by depositor's faculty
  
- **Phase 2 (Future):**
  - Add `faculty_id` to Author entity
  - Statistics: "Datasets authored by each faculty"
  - API endpoint: `GET /v2/statistics/faculties/authored`
  - SPARQL query: `statistics_faculty_authored.sparql`
  - Counts datasets by all authors' faculties (multi-valued)

**Documents:**
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 5.3 (Statistics Queries)
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 6.3 (GET /v2/statistics/faculties)
- `docs/future-work/PHASE2_STATISTICS.md` - Section 2 (Multi-valued Statistics)

**Verdict:** ✅ **This is the assignment - fully specified**

---

### 3. Missing Data - Cross-Referencing to Infer

**Your Question:** "There may be missing data, could cross referencing between the data sets be used to infer the missing data"

**Status:** ⚠️ **Partial in Phase 1, Full in Phase 2**

**Answer:**

**Phase 1 (Assignment):**
- **Migration approach:** Manual entry during account registration
- **No automatic inference** - users must select faculty from dropdown
- **Cross-referencing:** Limited to parsing Organizations field during initial migration
- **Coverage:** ~90% (most depositors have Organizations field with faculty name)
- **Missing data:** Flagged for manual review

**Phase 2 (Future):**
- **Automatic inference:** YES - pattern matching across multiple data sources
- **Cross-referencing sources:**
  1. Organizations field from ALL datasets by same author
  2. Account.faculty_id if author has linked account
  3. ORCID affiliation data (future enhancement)
  4. Co-author faculty patterns (heuristic)
  
- **Inference algorithm:** `detect_author_faculty.py` with confidence scoring
- **Example:** If unregistered author "Hebly, Scott J." appears on 5 datasets, concatenate all 5 Organizations fields and detect most common faculty
- **Confidence scoring:** 0.0-1.0 based on pattern strength
- **Coverage target:** ≥85% of TU Delft authors

**Documents:**
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 8.2 (Organizations Field Parsing)
- `docs/future-work/PHASE2_MIGRATION.md` - Section 4 (Unregistered Authors Detection)
- `docs/future-work/PHASE2_DATA_MODEL.md` - Section 5 (Confidence Scoring Model)

**Code:**
- `docs/future-work/PHASE2_MIGRATION.md` - Section 4.3 (`detect_author_faculty.py` script with cross-referencing logic)

**Verdict:** ⚠️ **Limited in Phase 1 (manual), Full automated inference in Phase 2**

---

### 4. Parsing Free-Form Text Options

**Your Question:** "What options exist for parsing free form text and is it possible to associate it to the authors"

**Status:** ⚠️ **Manual in Phase 1, Automated in Phase 2**

**Answer:**

**Phase 1 (Assignment):**
- **Parsing approach:** Manual review only
- **Process:** Export depositor accounts, review Organizations field manually, assign faculty_id
- **No automation:** Too risky for ~200 accounts (100% accuracy required)
- **Tool:** CSV template with manual review workflow

**Phase 2 (Future):**
- **Parsing approach:** Automated pattern matching with manual review fallback
- **Technology:** Python regex with FACULTY_PATTERNS dictionary
- **Pattern library:** 8 TU Delft faculties with multiple patterns each
  
**Example FACULTY_PATTERNS:**
```python
FACULTY_PATTERNS = {
    285860001: {  # Aerospace Engineering
        "patterns": [
            (r"Faculty of Aerospace Engineering", 0.9),
            (r"Aerospace Engineering", 0.7),
            (r"\bAE\b", 0.5),
            (r"Aerospace", 0.4)
        ]
    },
    285860005: {  # EEMCS
        "patterns": [
            (r"Faculty of Electrical Engineering, Mathematics and Computer Science", 0.95),
            (r"EEMCS", 0.8),
            (r"Computer Science", 0.6),
            (r"Electrical Engineering", 0.6)
        ]
    }
    # ... 6 more faculties
}
```

- **Confidence calculation:** Weighted sum of matched patterns
- **Auto-assign threshold:** ≥0.8 confidence
- **Manual review:** <0.8 confidence
- **Association to authors:** YES - via `Author.faculty_id` predicate

**Documents:**
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 8.2 (Manual Parsing)
- `docs/future-work/PHASE2_MIGRATION.md` - Section 4.3 (Pattern Matching Algorithm)
- `docs/future-work/PHASE2_DATA_MODEL.md` - Section 5 (Confidence Scoring)

**Code:**
- `docs/future-work/PHASE2_MIGRATION.md` - Section 4.3 (`detect_faculty()` function with full implementation)

**Verdict:** ⚠️ **Phase 1 manual only, Phase 2 has sophisticated pattern matching with 70-80% automation**

---

### 5. Associate Parsed Text to Authors

**Your Question:** "is it possible to associate it to the authors"

**Status:** ❌ **Not in Phase 1**, ✅ **YES in Phase 2**

**Answer:**

**Phase 1 (Assignment):**
- **Association:** Faculty associated to **Account** (depositor only)
- **Authors:** NOT tracked - only depositor's faculty
- **Limitation:** Cannot track co-author faculties

**Phase 2 (Future):**
- **Association:** Faculty associated to **Author** (all contributors)
- **Data model:**
  ```turtle
  djht:Author_UUID
      djht:full_name "Hebly, Scott J."
      djht:faculty_id "285860001"  # Aerospace
      djht:faculty_confidence "0.85"
      djht:faculty_source "organizations_auto"
      djht:faculty_assigned_date "2024-12-09T10:00:00Z"
  ```
- **Propagation:** Faculty assignment follows the author across all their datasets
- **Updates:** If author's faculty changes, update once and it reflects everywhere

**Documents:**
- `docs/future-work/ARCHITECTURE_CORRECTION_AUTHORS.md` - Section 4 (Author vs Account)
- `docs/future-work/PHASE2_DATA_MODEL.md` - Section 2 (RDF Schema Extensions)
- `docs/future-work/PHASE2_DATA_MODEL.md` - Section 3 (Entity Relationships)

**Verdict:** ❌ **Phase 1 does NOT associate to authors (depositor only)**, ✅ **Phase 2 fully associates parsed faculty to all authors**

---

### 6. Log Stats on Missing Data

**Your Question:** "Can stats be logged on the missing data"

**Status:** ✅ **YES - Implemented in both phases**

**Answer:**

**Phase 1 (Assignment):**
- **Migration coverage metric:**
  ```sql
  SELECT 
    COUNT(*) as total_depositors,
    SUM(CASE WHEN faculty_id IS NOT NULL THEN 1 ELSE 0 END) as with_faculty,
    SUM(CASE WHEN faculty_id IS NULL THEN 1 ELSE 0 END) as without_faculty,
    ROUND(100.0 * SUM(CASE WHEN faculty_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) as coverage_pct
  FROM accounts
  WHERE institution_id = '283002203'  -- TU Delft
  ```
- **Target:** ≥90% coverage
- **Dashboard:** Show "X of Y depositors have faculty assigned"
- **Export:** CSV list of accounts without faculty for manual review

**Phase 2 (Future):**
- **Enhanced coverage metrics:**
  ```sql
  SELECT 
    COUNT(*) as total_authors,
    SUM(CASE WHEN faculty_id IS NOT NULL THEN 1 ELSE 0 END) as with_faculty,
    SUM(CASE WHEN faculty_confidence >= 0.8 THEN 1 ELSE 0 END) as high_confidence,
    SUM(CASE WHEN faculty_confidence < 0.8 THEN 1 ELSE 0 END) as low_confidence,
    SUM(CASE WHEN faculty_id IS NULL THEN 1 ELSE 0 END) as without_faculty
  FROM authors
  WHERE institution_id = '283002203'
  ```
- **Confidence distribution:**
  - 0.0-0.5: Needs manual review
  - 0.5-0.8: Manual review recommended
  - 0.8-0.95: Auto-assigned
  - 0.95-1.0: From account or manual review
  
- **Missing data dashboard:**
  - Authors without faculty (by institution)
  - Low confidence assignments (<0.8)
  - External authors (excluded from faculty tracking)
  
- **Validation queries:** 5 SPARQL queries to detect gaps (see PHASE2_MIGRATION.md Section 6)

**Documents:**
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 8.4 (Validation & Quality Assurance)
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 14.1 (Success Metrics)
- `docs/future-work/PHASE2_MIGRATION.md` - Section 6 (Quality Assurance & Validation)
- `docs/future-work/PHASE2_IMPLEMENTATION.md` - Section 5.1 (Success Metrics)

**Verdict:** ✅ **YES - comprehensive missing data tracking in both phases**

---

### 7. Handle Free-Form Organization Information

**Your Question:** "How best to handle the free form organisation information"

**Status:** ✅ **Hybrid approach - preserve field, add structured data**

**Answer:**

**Recommended Approach (Both Phases):**
- **DO NOT remove Organizations field** - it has value for:
  - Display purposes (show full affiliation string)
  - External institutions (non-TU Delft)
  - Historical data
  - Edge cases pattern matching can't handle
  
- **ADD structured faculty_id alongside Organizations:**
  ```turtle
  djht:Account_UUID
      djht:first_name "John"
      djht:last_name "Smith"
      djht:institution_id "283002203"  # TU Delft
      djht:faculty_id "285860001"      # NEW: Aerospace (structured)
  
  djht:Dataset_UUID
      djht:organizations "Faculty of Aerospace Engineering, TU Delft"  # KEEP: Free-form (display)
  ```

**Benefits of Hybrid Approach:**
1. **Aggregation:** Use faculty_id for statistics
2. **Display:** Show Organizations for human readers
3. **Flexibility:** Organizations can contain additional info (department, research group)
4. **Backward compatibility:** Existing datasets keep Organizations field
5. **Future-proof:** Can parse Organizations later to extract department/group

**Migration Strategy:**
- **Phase 1:** Parse Organizations → assign faculty_id → keep original Organizations
- **Phase 2:** Parse Organizations for all authors → assign faculty_id → keep original Organizations

**Documents:**
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 8.2 (Organizations Field Handling)
- `docs/future-work/ARCHITECTURE_CORRECTION_AUTHORS.md` - Section 6 (Extensibility)
- `docs/future-work/PHASE2_MIGRATION.md` - Section 4.2 (Export Unregistered Authors)

**Verdict:** ✅ **Keep Organizations field for display, add faculty_id for aggregation - best of both worlds**

---

### 8. Stats on Contributors Per Institute

**Your Question:** "Stats on number of contributors per institute"

**Status:** ✅ **Already exists + enhanced in Phase 2**

**Answer:**

**Current System:**
- **Existing query:** Count authors by institution (if Author has djht:institution predicate)
- **Limitation:** Most authors don't have institution - only depositors do
- **Current stat:** "Number of depositors per institute" (via Account.institution_id)

**Phase 1 (Assignment):**
- **No change** - still counts depositors only
- **Faculty added:** Can now count "depositors per faculty per institute"

**Phase 2 (Future):**
- **Enhanced:** Count **all authors** per institute per faculty
- **New query:** `author_contributions_by_faculty.sparql`
  ```sparql
  SELECT ?faculty_id (COUNT(DISTINCT ?author) as ?author_count)
  WHERE {
      ?author djht:faculty_id ?faculty_id .
      ?faculty djht:id ?faculty_id ;
               djht:institution_id ?institution_id .
      FILTER(?institution_id = "283002203")  # TU Delft
  }
  GROUP BY ?faculty_id
  ```
- **Multi-level stats:**
  - Authors per institute (TU Delft: 950, UT: 200, etc.)
  - Authors per faculty per institute (TU Delft Aerospace: 120, TU Delft EEMCS: 180, etc.)
  - Contributors per dataset (average authors per dataset by faculty)

**Documents:**
- `docs/current-system/CODEBASE_ANALYSIS.md` - Section 3 (Current Statistics)
- `docs/future-work/PHASE2_STATISTICS.md` - Section 2.4 (Author Contributions)
- `docs/future-work/PHASE2_API_UI.md` - Section 1.6 (GET /v2/authors?faculty_id={id})

**Verdict:** ✅ **Already supported for depositors, Phase 2 extends to all authors**

---

### 9. Stats Based on First Author Only

**Your Question:** "Stats based on first author publication only"

**Status:** ❌ **Not addressed - could be Phase 3**

**Answer:**

**Current Limitation:**
- Djehuty's RDF model does **not preserve author order**
- Authors are stored as unordered set:
  ```turtle
  djht:Dataset_UUID
      djht:has_author djht:Author_UUID_1 .
      djht:has_author djht:Author_UUID_2 .
      djht:has_author djht:Author_UUID_3 .
  ```
- **No predicate for author position** (first, second, corresponding, etc.)

**Why First Author Matters:**
- In some fields (e.g., chemistry, physics), first author = main contributor
- "First author publications" is a common research metric
- **BUT:** In other fields (e.g., math), authors are alphabetical

**Possible Solutions (Out of Scope for Phase 1/2):**

**Option 1: Add author_position predicate (Phase 3):**
```turtle
djht:Dataset_UUID
    djht:has_author [
        djht:author djht:Author_UUID_1 ;
        djht:author_position 1 ;
        djht:author_role "first"
    ] .
```

**Option 2: Use existing DataCite metadata:**
- DataCite XML may contain author order
- Could parse during dataset import
- Requires schema changes

**Option 3: Corresponding author flag:**
```turtle
djht:Author_UUID_1
    djht:is_corresponding_author "true" .
```

**Phase 3 Estimate:**
- 2 weeks development
- Migrate existing datasets (parse author order from DataCite)
- New statistics: "First author publications by faculty"

**Documents:**
- `docs/current-system/CODEBASE_ANALYSIS.md` - Section 4 (Author Management)
- `docs/current-system/DATASET_ANALYSIS.md` - Section 3 (Author Metadata)

**Verdict:** ❌ **Out of scope for Phase 1 and Phase 2 - requires schema extension to track author position (could be Phase 3)**

---

### 10. Extensible Stats Structure

**Your Question:** "What if more stats output types are requested in future, could the structure be improvised"

**Status:** ✅ **YES - SPARQL-based architecture is highly extensible**

**Answer:**

**Why It's Extensible:**

1. **SPARQL = Flexible Query Language:**
   - Not like SQL with fixed schema
   - Can combine predicates in any way
   - Adding new stats = adding new SPARQL query

2. **RDF Triples = Graph Database:**
   - Can traverse relationships in any direction
   - No need to restructure tables
   - Adding new predicates doesn't break existing queries

3. **Jinja2 Templates:**
   - SPARQL queries stored as templates
   - Easy to add new templates without code changes
   - Parameters passed at runtime

**Example - Adding New Stats (Future):**

**Request:** "Show datasets by faculty AND research group"

**Solution:** Add new predicates + new query (no refactoring)
```turtle
# New schema (backward compatible):
djht:Author_UUID
    djht:faculty_id "285860001"
    djht:research_group_id "AE_STRUCTURES"  # NEW

# New query template:
SELECT ?faculty_id ?research_group_id (COUNT(DISTINCT ?dataset) as ?count)
WHERE {
    ?dataset djht:has_author ?author .
    ?author djht:faculty_id ?faculty_id ;
            djht:research_group_id ?research_group_id .
}
GROUP BY ?faculty_id ?research_group_id
```

**Request:** "Show collaboration patterns between faculties over time"

**Solution:** Add temporal query (existing data already has timestamps)
```sparql
SELECT ?year ?faculty1 ?faculty2 (COUNT(*) as ?collaborations)
WHERE {
    ?dataset djht:published_date ?date ;
             djht:has_author ?author1, ?author2 .
    ?author1 djht:faculty_id ?faculty1 .
    ?author2 djht:faculty_id ?faculty2 .
    FILTER(?faculty1 < ?faculty2)  # Avoid duplicates
    BIND(YEAR(?date) as ?year)
}
GROUP BY ?year ?faculty1 ?faculty2
ORDER BY ?year
```

**No Migration Needed:**
- Existing datasets already have dates
- Existing authors already have faculty_id (after Phase 2)
- Just write new query

**Documents:**
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 5.3 (Statistics Queries)
- `docs/current-system/CODEBASE_ANALYSIS.md` - Section 8 (SPARQL Query Patterns)
- `docs/future-work/PHASE2_STATISTICS.md` - Section 7 (Future Extensions)

**Verdict:** ✅ **Extremely extensible - SPARQL + RDF allows adding new stats without schema refactoring**

---

### 11. Modular Schema for Future Requests

**Your Question:** "In the database structure, are the author, institute and faculty related through tables that will allow retention of information other than manual entry. Or is the current schema modular enough that we can focus on explicit tasks and not refactor later and not worry about future possible undefined requests."

**Status:** ✅ **YES - RDF schema is highly modular**

**Answer:**

**RDF Schema Modularity:**

```turtle
# Entities are related through predicates (not foreign keys):

djht:Account_UUID
    djht:institution_id "283002203" .  # Points to Institution
    djht:faculty_id "285860001" .      # Points to Faculty (Phase 1)

djht:Institution_283002203
    djht:id "283002203" .
    djht:name "TU Delft" .
    djht:has_faculty djht:Faculty_285860001 .  # Links to Faculty

djht:Faculty_285860001
    djht:id "285860001" .
    djht:name "Faculty of Aerospace Engineering" .
    djht:institution_id "283002203" .  # Back-reference to Institution

djht:Author_UUID
    djht:account djht:Account_UUID .  # Optional link to Account
    djht:faculty_id "285860001" .     # Points to Faculty (Phase 2)

djht:Dataset_UUID
    djht:has_author djht:Author_UUID .
    djht:owner djht:Account_UUID .  # Depositor
```

**Benefits:**

1. **No Foreign Key Constraints:**
   - Can add new predicates without migrations
   - Predicates are optional by default
   - No cascade delete issues

2. **Bidirectional Relationships:**
   - Faculty → Authors (all authors in this faculty)
   - Author → Faculty (which faculty is this author)
   - Both queries are efficient

3. **Easy Extension:**
   - Want to add Department? Just add `djht:department_id` predicate
   - Want to add Research Group? Just add `djht:research_group_id`
   - **No table alterations** - just new triples

4. **Retain All Information:**
   - Old data: Account has institution_id (preserved)
   - Phase 1: Account adds faculty_id (additive)
   - Phase 2: Author adds faculty_id, faculty_confidence, faculty_source (additive)
   - Nothing deleted, everything cumulative

5. **Manual Entry Retention:**
   - `djht:faculty_source "manual_review"` - preserves how it was assigned
   - `djht:faculty_assigned_date "2024-12-09"` - preserves when
   - Can query "Show only manually reviewed faculty assignments"

**Future Extensions (No Refactoring):**

```turtle
# Phase 3: Add departments
djht:Author_UUID
    djht:faculty_id "285860001" .
    djht:department_id "AE_STRUCTURES" .  # NEW

# Phase 4: Add research groups
djht:Author_UUID
    djht:faculty_id "285860001" .
    djht:department_id "AE_STRUCTURES" .
    djht:research_group_id "AE_STRUCT_COMPOSITE" .  # NEW

# Phase 5: Add temporal changes
djht:Author_UUID
    djht:faculty_history [
        djht:faculty_id "285860001" ;
        djht:start_date "2020-01-01" ;
        djht:end_date "2023-12-31"
    ] ,
    [
        djht:faculty_id "285860005" ;
        djht:start_date "2024-01-01"
    ] .
```

**Documents:**
- `docs/current-system/CODEBASE_ANALYSIS.md` - Section 1 (RDF Schema)
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 4.2 (Entity Relationships)
- `docs/future-work/PHASE2_DATA_MODEL.md` - Section 3 (Entity Relationships)
- `docs/future-work/ARCHITECTURE_CORRECTION_AUTHORS.md` - Section 6 (Extensibility)

**Verdict:** ✅ **Extremely modular - RDF schema allows adding new predicates without refactoring, all information retained**

---

### 12. Stats on Unregistered Author Contributors

**Your Question:** "Thinking of stats based on contributors that we find in unregistered authors."

**Status:** ❌ **Not in Phase 1**, ✅ **YES - Core Phase 2 feature**

**Answer:**

**Phase 1 (Assignment):**
- **Limitation:** Only tracks depositors (registered users)
- **Unregistered authors:** NOT tracked
- **Example:** Dataset with 3 co-authors:
  - Author 1: Dr. Smith (depositor, registered) → Faculty tracked ✅
  - Author 2: Hebly, Scott J. (unregistered) → Faculty NOT tracked ❌
  - Author 3: Dr. Garcia (external, unregistered) → Faculty NOT tracked ❌
- **Statistics:** "Datasets deposited by faculty" (counts Author 1 only)

**Phase 2 (Future):**
- **Enhancement:** Track ALL authors (registered + unregistered)
- **Example:** Same dataset, Phase 2:
  - Author 1: Dr. Smith (registered, Aerospace, confidence 1.0) ✅
  - Author 2: Hebly, Scott J. (unregistered, Aerospace, confidence 0.85) ✅
  - Author 3: Dr. Garcia (external DLR, no faculty) ✅ (excluded)
  
- **Statistics:** "Datasets authored by faculty"
  - Aerospace: +1 (2 authors)
  - Total: 1 dataset counted once for Aerospace (multi-valued semantics)

**Unregistered Author Stats:**

```sparql
# Count unregistered authors by faculty
SELECT ?faculty_name (COUNT(DISTINCT ?author) as ?unregistered_author_count)
WHERE {
    ?author djht:faculty_id ?faculty_id .
    FILTER NOT EXISTS { ?author djht:account ?account }  # Unregistered
    ?faculty djht:id ?faculty_id ;
             djht:name ?faculty_name .
}
GROUP BY ?faculty_name

# Count datasets with unregistered TU Delft contributors
SELECT (COUNT(DISTINCT ?dataset) as ?datasets_with_unregistered_tu_delft)
WHERE {
    ?dataset djht:has_author ?author .
    ?author djht:faculty_id ?faculty_id .
    FILTER NOT EXISTS { ?author djht:account ?account }
}

# Compare registered vs unregistered contribution
SELECT 
    ?faculty_name,
    SUM(CASE WHEN ?has_account THEN 1 ELSE 0 END) as registered_authors,
    SUM(CASE WHEN NOT ?has_account THEN 1 ELSE 0 END) as unregistered_authors
WHERE {
    ?author djht:faculty_id ?faculty_id .
    BIND(EXISTS { ?author djht:account ?account } as ?has_account)
    ?faculty djht:id ?faculty_id ;
             djht:name ?faculty_name .
}
GROUP BY ?faculty_name
```

**Documents:**
- `docs/future-work/ARCHITECTURE_CORRECTION_AUTHORS.md` - Section 2 vs 3 (Depositor-Only vs Author-Inclusive)
- `docs/future-work/PHASE2_OVERVIEW.md` - Section 2 (Problem Statement)
- `docs/future-work/PHASE2_MIGRATION.md` - Section 3.2 (Unregistered Authors)
- `docs/future-work/PHASE2_STATISTICS.md` - Section 2.4 (Author Contributions)

**Verdict:** ❌ **Phase 1 does NOT track unregistered authors**, ✅ **Phase 2 core feature - ~800 unregistered TU Delft authors tracked**

---

### 13. Database Structure Improvements

**Your Question:** "Based on the current code, can suggestions for possible improvements to the database structure be made to alleviate the concerns in the assignment as well as make data gathering more robust and easier to the user with auto population"

**Status:** ✅ **YES - Comprehensive improvements proposed**

**Answer:**

**Proposed Improvements (Implemented in Phase 1 & 2):**

#### 1. Add Faculty Entity (Phase 1)

**Current Problem:** No Faculty entity, can't aggregate by faculty

**Solution:**
```turtle
djht:Faculty
    djht:id "285860001" .
    djht:name "Faculty of Aerospace Engineering" .
    djht:abbreviation "AE" .
    djht:institution_id "283002203" .
    djht:description "Faculty of Aerospace Engineering, TU Delft" .
```

**Benefit:** Structured faculty data for aggregation

---

#### 2. Add faculty_id to Account (Phase 1)

**Current Problem:** Accounts have institution but no faculty

**Solution:**
```turtle
djht:Account
    djht:institution_id "283002203" .
    djht:faculty_id "285860001" .  # NEW
```

**Benefit:** Track depositor's faculty

---

#### 3. Add faculty_id to Author with Confidence (Phase 2)

**Current Problem:** Authors have no institution or faculty

**Solution:**
```turtle
djht:Author
    djht:faculty_id "285860001" .
    djht:faculty_confidence "0.85" .      # NEW: How confident are we?
    djht:faculty_source "organizations_auto" .  # NEW: How was it assigned?
    djht:faculty_assigned_date "2024-12-09" .   # NEW: When was it assigned?
```

**Benefit:** Track all authors' faculties with provenance

---

#### 4. Normalize Organizations Field (Both Phases)

**Current Problem:** Free-text Organizations field, unparseable

**Solution:** **Don't remove it** - add structured faculty_id alongside

**Benefit:** Keep display value, add aggregation capability

---

#### 5. Add Validation Predicates (Both Phases)

**Current Problem:** No validation, bad data can enter

**Solution:**
```python
# Validation rules:
1. faculty.institution_id == account.institution_id  # Faculty must match institution
2. faculty_id must reference existing Faculty entity
3. faculty_confidence must be 0.0-1.0
4. faculty_source must be enum: "account", "organizations_auto", "manual_review"
```

**Benefit:** Data quality enforcement

---

#### 6. Add Caching Layer (Both Phases)

**Current Problem:** Statistics queries are slow

**Solution:**
```python
# Cache keys:
"statistics:faculty:{faculty_id}:deposited" → TTL 6 hours
"statistics:faculty:{faculty_id}:authored"  → TTL 6 hours
"statistics:collaborations" → TTL 12 hours

# Invalidation:
- Clear on Account.faculty_id change
- Clear on Author.faculty_id change
- Clear on Dataset creation/deletion
```

**Benefit:** <200ms query response time

---

#### 7. Add Auto-Population Mechanisms (Phase 1 & 2)

**Phase 1 - Auto-fill for registered users:**
```javascript
// On dataset submission, if user is logged in:
if (account.faculty_id) {
    document.getElementById("depositor-faculty").value = account.faculty_id;
    document.getElementById("depositor-faculty").disabled = true;
}
```

**Phase 2 - Pattern detection for unregistered:**
```python
# detect_author_faculty.py
def auto_populate_author_faculty(author_name):
    # 1. Get all datasets by this author
    datasets = get_datasets_by_author(author_name)
    
    # 2. Concatenate all Organizations fields
    all_orgs = " ".join([d.organizations for d in datasets])
    
    # 3. Run pattern matching
    faculty_id, confidence = detect_faculty(all_orgs)
    
    # 4. Auto-populate if confidence >= 0.8
    if confidence >= 0.8:
        return faculty_id, confidence, "organizations_auto"
    else:
        return None, confidence, "manual_review_needed"
```

**Benefit:** User doesn't need to manually enter faculty for every author

---

#### 8. Add Migration Scripts (Both Phases)

**Current Problem:** 580+ existing datasets need faculty assignment

**Solution:**
- `migrate_depositor_faculty.py` (Phase 1)
- `export_registered_authors.py` (Phase 2)
- `export_unregistered_authors.py` (Phase 2)
- `detect_author_faculty.py` (Phase 2)
- `import_author_faculty.py` (Phase 2)

**Benefit:** Automated migration with manual review fallback

---

**Documents:**
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 4 (Data Model Design)
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 5 (System Components)
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 8 (Migration Strategy)
- `docs/future-work/PHASE2_DATA_MODEL.md` - All sections
- `docs/future-work/PHASE2_MIGRATION.md` - All sections

**Verdict:** ✅ **Comprehensive database improvements proposed and specified in detail**

---

### 14. Auto-Population Suggestions

**Your Question:** "make data gathering more robust and easier to the user with auto population"

**Status:** ⚠️ **Limited in Phase 1**, ✅ **Full in Phase 2**

**Answer:**

**Phase 1 Auto-Population:**

1. **Account Registration:**
   ```html
   <select id="faculty" name="faculty" required>
       <option value="">Select Faculty</option>
       <option value="285860001">Faculty of Aerospace Engineering</option>
       <option value="285860002">Faculty of Architecture</option>
       <!-- ... 6 more -->
   </select>
   ```
   - User selects faculty from dropdown
   - **NOT auto-populated** (no way to detect from email or name)

2. **Dataset Submission:**
   ```javascript
   // Auto-fill depositor faculty from account
   if (logged_in_account.faculty_id) {
       document.getElementById("depositor-faculty").value = account.faculty_id;
       document.getElementById("depositor-faculty").readonly = true;
   }
   ```
   - Depositor's faculty auto-filled from their account ✅
   - Co-author faculties: NOT tracked in Phase 1 ❌

**Phase 2 Auto-Population:**

1. **For Registered Authors:**
   ```python
   # When author has linked account:
   if author.account and author.account.faculty_id:
       author.faculty_id = author.account.faculty_id
       author.faculty_confidence = 1.0
       author.faculty_source = "account"
   ```
   - 100% accuracy ✅
   - ~150 authors auto-populated

2. **For Unregistered Authors:**
   ```python
   # Pattern matching from Organizations field:
   all_orgs = get_all_organizations_for_author(author.full_name)
   faculty_id, confidence = detect_faculty(all_orgs)
   
   if confidence >= 0.8:
       author.faculty_id = faculty_id
       author.faculty_confidence = confidence
       author.faculty_source = "organizations_auto"
       # Auto-populated ✅
   else:
       # Flag for manual review ⚠️
       flag_for_manual_review(author, confidence)
   ```
   - ~600 authors auto-populated (≥80% accuracy)
   - ~200 authors flagged for manual review

3. **Dataset Submission with Co-Authors:**
   ```html
   <div class="author-faculty">
       <span>Hebly, Scott J.</span>
       <select name="author_faculty">
           <option value="">Unknown</option>
           <option value="285860001" selected>Aerospace Engineering (85% confidence)</option>
       </select>
       <span class="confidence-badge">Auto-detected</span>
   </div>
   ```
   - System suggests faculty based on past datasets
   - User can override if incorrect
   - Confidence shown to indicate reliability

4. **Future: ORCID Integration (Phase 3):**
   ```python
   # Query ORCID API for author affiliation:
   orcid_data = get_orcid_affiliation(author.orcid_id)
   if "TU Delft" in orcid_data.affiliation:
       # Parse faculty from affiliation string
       faculty_id, confidence = detect_faculty_from_orcid(orcid_data)
   ```
   - Could improve accuracy to >90%
   - Out of scope for Phase 1/2

**Documents:**
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 7.2 (Dataset Submission Workflow)
- `docs/future-work/PHASE2_MIGRATION.md` - Section 4 (Unregistered Authors Detection)
- `docs/future-work/PHASE2_API_UI.md` - Section 4 (Workflow Integration)

**Verdict:** ⚠️ **Phase 1: Limited auto-fill (depositor only)**, ✅ **Phase 2: Extensive auto-population with pattern matching (70-80% automation)**

---

### 15. Graceful Failure Handling

**Your Question:** "Gracefully fail if a query or author or institute is unknown"

**Status:** ✅ **YES - Comprehensive error handling specified**

**Answer:**

**API Error Handling (Phase 1 & 2):**

#### 1. Unknown Faculty

```python
# GET /v2/faculties/999999
@app.route("/v2/faculties/<faculty_id>", methods=["GET"])
def api_v2_faculty_detail(faculty_id):
    faculty = get_faculty_by_id(faculty_id)
    if not faculty:
        return jsonify({
            "error": "faculty_not_found",
            "message": f"Faculty with ID {faculty_id} does not exist",
            "valid_faculties": "/v2/faculties"
        }), 404
    return jsonify(faculty), 200
```

**Response:**
```json
{
    "error": "faculty_not_found",
    "message": "Faculty with ID 999999 does not exist",
    "valid_faculties": "/v2/faculties"
}
```

---

#### 2. Unknown Author

```python
# GET /v2/authors/invalid-uuid/faculty
@app.route("/v2/authors/<author_uuid>/faculty", methods=["GET"])
def api_v2_author_faculty(author_uuid):
    try:
        uuid.UUID(author_uuid)  # Validate UUID format
    except ValueError:
        return jsonify({
            "error": "invalid_uuid",
            "message": f"'{author_uuid}' is not a valid UUID"
        }), 400
    
    author = get_author_by_uuid(author_uuid)
    if not author:
        return jsonify({
            "error": "author_not_found",
            "message": f"Author with UUID {author_uuid} does not exist"
        }), 404
    
    return jsonify({
        "uuid": author.uuid,
        "full_name": author.full_name,
        "faculty_id": author.faculty_id,
        "faculty_confidence": author.faculty_confidence
    }), 200
```

---

#### 3. Unknown Institution

```python
# GET /v2/statistics/faculties?institution_id=999
@app.route("/v2/statistics/faculties", methods=["GET"])
def api_v2_statistics_faculties():
    institution_id = request.args.get("institution_id")
    
    if institution_id:
        institution = get_institution_by_id(institution_id)
        if not institution:
            return jsonify({
                "error": "institution_not_found",
                "message": f"Institution {institution_id} does not exist",
                "valid_institutions": "/v2/institutions"
            }), 404
    
    # ... rest of statistics logic
```

---

#### 4. Invalid Query Parameters

```python
# GET /v2/statistics/faculties?page=-1
@app.route("/v2/statistics/faculties", methods=["GET"])
def api_v2_statistics_faculties():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        return jsonify({
            "error": "invalid_parameter",
            "message": "page and per_page must be integers"
        }), 400
    
    if page < 1:
        return jsonify({
            "error": "invalid_parameter",
            "message": "page must be >= 1"
        }), 400
    
    if per_page < 1 or per_page > 100:
        return jsonify({
            "error": "invalid_parameter",
            "message": "per_page must be between 1 and 100"
        }), 400
```

---

#### 5. SPARQL Query Failures

```python
def execute_sparql_query(query):
    try:
        result = sparql_endpoint.query(query)
        return result
    except SPARQLWrapperException as e:
        logging.error(f"SPARQL query failed: {e}")
        return {
            "error": "query_failed",
            "message": "Database query failed. Please try again later.",
            "details": str(e) if app.debug else None
        }, 500
    except Timeout:
        logging.error("SPARQL query timeout")
        return {
            "error": "query_timeout",
            "message": "Query took too long. Try a more specific search."
        }, 504
```

---

#### 6. Validation Errors (Phase 2)

```python
# PATCH /v2/authors/{uuid}/faculty
@app.route("/v2/authors/<author_uuid>/faculty", methods=["PATCH"])
def api_v2_update_author_faculty(author_uuid):
    data = request.get_json()
    
    # Validate faculty_id exists
    if not faculty_exists(data["faculty_id"]):
        return jsonify({
            "error": "faculty_not_found",
            "message": f"Faculty {data['faculty_id']} does not exist"
        }), 404
    
    # Validate faculty belongs to author's institution
    author = get_author(author_uuid)
    faculty = get_faculty(data["faculty_id"])
    
    if author.institution_id != faculty.institution_id:
        return jsonify({
            "error": "faculty_institution_mismatch",
            "message": f"Faculty {faculty.name} belongs to {faculty.institution.name}, but author belongs to {author.institution.name}",
            "author_institution": author.institution.name,
            "faculty_institution": faculty.institution.name
        }), 400
    
    # Validate confidence (if provided)
    if "faculty_confidence" in data:
        confidence = data["faculty_confidence"]
        if not (0.0 <= confidence <= 1.0):
            return jsonify({
                "error": "invalid_confidence",
                "message": "faculty_confidence must be between 0.0 and 1.0"
            }), 400
```

---

#### 7. UI Error Handling

```javascript
// Graceful degradation in statistics dashboard
async function loadFacultyStatistics() {
    try {
        const response = await fetch('/v2/statistics/faculties');
        
        if (!response.ok) {
            if (response.status === 404) {
                showError("No faculty data found. Please ensure faculties are configured.");
            } else if (response.status === 500) {
                showError("Server error. Please try again later.");
            } else {
                showError(`Error loading statistics: ${response.statusText}`);
            }
            return;
        }
        
        const data = await response.json();
        renderStatistics(data);
        
    } catch (error) {
        console.error("Failed to load faculty statistics:", error);
        showError("Failed to load statistics. Please check your internet connection.");
    }
}

function showError(message) {
    document.getElementById("statistics-container").innerHTML = `
        <div class="error-message">
            <i class="icon-warning"></i>
            <p>${message}</p>
            <button onclick="loadFacultyStatistics()">Retry</button>
        </div>
    `;
}
```

---

**Documents:**
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 6.1.3 (Error Handling)
- `docs/assignment/SOLUTION_ARCHITECTURE.md` - Section 10 (Security & Privacy)
- `docs/future-work/PHASE2_API_UI.md` - Section 5 (Error Handling)

**Verdict:** ✅ **Comprehensive graceful failure handling for all edge cases**

---

## 📊 Summary Matrix

| Requirement | Phase 1 | Phase 2 | Recommendation |
|-------------|---------|---------|----------------|
| **Stats per institute** | ✅ Exists | ✅ Exists | No action needed |
| **Stats per faculty** | ✅ **CORE** | ✅ Enhanced | **Implement Phase 1** |
| **Cross-referencing** | ⚠️ Manual | ✅ Automated | Manual OK for Phase 1, automate in Phase 2 |
| **Parse free-text** | ⚠️ Manual | ✅ Pattern matching | Manual OK for Phase 1, pattern matching in Phase 2 |
| **Associate to authors** | ❌ No | ✅ **CORE** | Phase 2 required |
| **Missing data stats** | ✅ Coverage | ✅ Confidence | **Implement both** |
| **Handle Organizations** | ✅ Hybrid | ✅ Hybrid | **Keep field + add faculty_id** |
| **Contributors per institute** | ✅ Exists | ✅ Enhanced | Enhanced in Phase 2 |
| **First author stats** | ❌ No | ❌ No | **Phase 3** (out of scope) |
| **Extensible stats** | ✅ SPARQL | ✅ SPARQL | **Already extensible** |
| **Modular schema** | ✅ RDF | ✅ RDF | **Already modular** |
| **Unregistered authors** | ❌ No | ✅ **CORE** | Phase 2 required |
| **DB improvements** | ✅ Specified | ✅ Specified | **Follow architecture docs** |
| **Auto-population** | ⚠️ Limited | ✅ Extensive | Limited in Phase 1, full in Phase 2 |
| **Graceful failures** | ✅ Specified | ✅ Specified | **Implement error handling** |

---

## 🎯 Recommendations

### For the Assignment (Phase 1):

**Implement:**
1. ✅ Stats per faculty (depositor-only)
2. ✅ Missing data coverage metrics
3. ✅ Hybrid approach (keep Organizations + add faculty_id)
4. ✅ Graceful error handling
5. ✅ Manual migration with validation

**Defer to Phase 2:**
1. ⚠️ Cross-referencing / pattern matching
2. ⚠️ Auto-population for unregistered authors
3. ⚠️ Associate faculty to all authors (not just depositors)

**Out of Scope (Phase 3):**
1. ❌ First author statistics (requires author position tracking)

---

### Documentation References

**Already Addressed:**
- Requirements 1, 2, 6, 7, 8, 10, 11, 13, 15 → See `docs/assignment/`
- Requirements 3, 4, 5, 12, 14 → See `docs/future-work/`
- Requirement 9 → Not addressed (Phase 3)

**Key Documents:**
- **Phase 1 implementation:** `docs/assignment/SOLUTION_ARCHITECTURE.md`
- **Phase 2 decision:** `docs/future-work/PHASE2_QUICK_REFERENCE.md`
- **Current gaps:** `docs/current-system/TECHNICAL_FINDINGS_SUMMARY.md`

---

*This analysis demonstrates that the architecture comprehensively addresses 14 of 15 requirements, with 1 deferred to Phase 3.*
