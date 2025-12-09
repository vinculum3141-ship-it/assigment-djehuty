# CRITICAL CORRECTION: Author vs Account Entities

**Date:** December 9, 2025  
**Issue:** Original architecture incorrectly assumed all authors have accounts  
**Impact:** Faculty assignment strategy needs revision

---

## The Problem You Identified

**Your Question:**
> "Are you assuming all authors have logins to the system (have registered on the system)? What if someone contributed but is not registered?"

**Answer:** You're absolutely correct - I made a false assumption. The original architecture only addressed faculty assignment for **registered users** (those with `djht:Account` entities), but **most authors don't have accounts**.

---

## How the System Actually Works

### Two Separate Entities

```sparql
# Account entity (REGISTERED users only)
?account rdf:type djht:Account
?account djht:email "researcher@tudelft.nl"
?account djht:institution_id 28586

# Author entity (ALL contributors, registered or not)
?author rdf:type djht:Author
?author djht:full_name "Dr. Jane Smith"
?author djht:orcid_id "0000-0003-1234-5678"
?author djht:institution_id 28586        # OPTIONAL - often null
?author djht:account ?account            # OPTIONAL - only if registered!
```

### The Optional Link

From `src/djehuty/web/database.py` line 1575:

```python
def insert_author(self, ..., account_uuid=None):
    """Procedure to add an author to the state graph."""
    # ...
    if account_uuid is not None:
        account_uri = URIRef(rdf.uuid_to_uri(account_uuid, "account"))
        rdf.add(graph, author_uri, rdf.DJHT["account"], account_uri, "uri")
    # ^^^ This is OPTIONAL - most authors don't have accounts!
```

From `accounts.sparql` lines 33-38:

```sparql
OPTIONAL {
  ?author            rdf:type                   djht:Author ;
                     djht:account               ?account .
  OPTIONAL { ?author djht:orcid_id              ?orcid . }
  OPTIONAL { ?author djht:full_name             ?full_name . }
}
```

**The `OPTIONAL` clause means most queries return authors WITHOUT linked accounts.**

---

## Real-World Scenario

### Dataset Example: Aviation NOx Emissions

From `DATASET_ANALYSIS.md`, the dataset has **3 authors**:

1. **Hebly, Scott J.** - Listed contributor (probably no account)
2. **Hoekstra, Joris M.** - Listed contributor (probably no account)  
3. **Depositor** - The registered user who uploaded the dataset (HAS account)

**Current State:**
- Dataset `djht:institution_id` = 28586 (TU Delft) ← from depositor's account
- Dataset `djht:organizations` = "TU Delft, Faculty of Aerospace Engineering..." ← free text
- Authors: NO institution_id, NO faculty_id ← unregistered contributors

---

## Impact on Faculty Statistics

### What We Need to Track

**Use Case from Assignment:**
> "Count datasets published by **Faculty of Aerospace Engineering**"

**The Problem:**
- Depositor has account → can set `faculty_id` at registration ✅
- But co-authors (Hebly, Hoekstra) are **unregistered** ❌
- Their faculty affiliation is only in the free-text `Organizations` field
- Statistics would only count depositor's faculty, **not co-authors' faculties**

### Example Counts (Hypothetical)

**Scenario:** Dataset with 3 authors from different faculties:
- Depositor: Faculty of Aerospace (account with `faculty_id=285860001`)
- Co-author 1: Faculty of EEMCS (no account, only in Organizations text)
- Co-author 2: External institution DLR Germany (no account)

**Original Architecture Would Count:**
- ✅ 1 dataset for "Faculty of Aerospace" (depositor's faculty)
- ❌ 0 datasets for "Faculty of EEMCS" (co-author has no account)

**This is incorrect** if we want to count all faculty contributions!

---

## Two Possible Interpretations

### Interpretation 1: Depositor-Only Statistics (Simpler)

**Assumption:** Faculty statistics track **depositing faculty**, not authorship contributions.

**Justification:**
- Administrative view: "Which faculty is **managing** datasets?"
- Easier implementation: Only need `faculty_id` on Account
- Aligns with current `institution_id` behavior (only tracks depositor)

**Query:**
```sparql
SELECT ?faculty_name (COUNT(?dataset) AS ?count)
WHERE {
  ?dataset djht:container/djht:account ?account .
  ?account djht:faculty_id ?faculty_id .
  ?faculty djht:id ?faculty_id ;
           djht:name ?faculty_name .
}
GROUP BY ?faculty_name
```

**Pros:**
- ✅ Simple, matches existing institution_id logic
- ✅ No migration of unregistered author data needed
- ✅ Clear ownership: 1 dataset = 1 faculty

**Cons:**
- ❌ Doesn't track co-author faculty affiliations
- ❌ Multi-faculty collaboration invisible

---

### Interpretation 2: Author-Inclusive Statistics (Complex)

**Assumption:** Faculty statistics should count **all author contributions**, registered or not.

**Justification:**
- Research view: "Which faculty's researchers are contributing?"
- More accurate representation of faculty research output
- Aligns with bibliometric standards (count all affiliations)

**Requires:**
1. Add `faculty_id` to **Author** entity (not just Account)
2. Parse Organizations field to extract faculty for unregistered authors
3. Multi-valued statistics (1 dataset can count for multiple faculties)

**Query:**
```sparql
SELECT ?faculty_name (COUNT(DISTINCT ?dataset) AS ?count)
WHERE {
  ?dataset djht:authors/rdf:rest*/rdf:first ?author .
  ?author djht:faculty_id ?faculty_id .
  ?faculty djht:id ?faculty_id ;
           djht:name ?faculty_name .
}
GROUP BY ?faculty_name
```

**Pros:**
- ✅ Accurate representation of faculty contributions
- ✅ Captures multi-faculty collaboration
- ✅ Aligns with research metrics standards

**Cons:**
- ❌ Complex migration (need to extract faculty from Organizations text for unregistered authors)
- ❌ One dataset counted multiple times (double-counting concern)
- ❌ Harder to validate

---

## Recommended Solution: Hybrid Approach

### Phase 1: Depositor-Only (Match Assignment Scope)

**For the assignment**, implement **Interpretation 1**:

1. Add `faculty_id` to `djht:Account` only
2. Display faculty dropdown at registration
3. Auto-populate faculty in dataset form (from account)
4. Statistics count datasets by **depositor's faculty**

**Reasoning:**
- Assignment says "faculty-level statistics" without specifying author contributions
- Current `institution_id` only tracks depositor institution (we extend same pattern)
- Minimal scope, achievable in 5 weeks
- Clear semantics: "Which faculty is depositing data?"

### Phase 2: Author Contributions (Future Enhancement)

**Post-assignment**, extend to **Interpretation 2**:

1. Add `faculty_id` to `djht:Author` entity
2. For **registered authors**: copy from their account's `faculty_id`
3. For **unregistered authors**: extract from Organizations field during migration
4. Provide separate statistics:
   - "Datasets deposited by faculty" (depositor-based)
   - "Datasets authored by faculty" (author-based)
   - "Multi-faculty collaborations" (datasets with authors from ≥2 faculties)

---

## Updated Architecture: Depositor-Only Approach

### Data Model Changes

**No changes to Author entity** (keeps it simple):

```turtle
# Account entity (REGISTERED users)
djht:Account a rdfs:Class ;
    rdfs:label "Account" .

djht:faculty_id a rdf:Property ;
    rdfs:domain djht:Account ;
    rdfs:range xsd:integer ;
    rdfs:label "Faculty ID" .

# Author entity remains unchanged
djht:Author a rdfs:Class ;
    rdfs:label "Author" .
# NO faculty_id predicate on Author (for now)
```

### Statistics Query (Corrected)

**Count datasets by depositor's faculty:**

```sparql
PREFIX djht: <https://data.4tu.nl/ontology/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?faculty_id ?faculty_name (COUNT(DISTINCT ?dataset) AS ?dataset_count)
WHERE {
  GRAPH <https://data.4tu.nl> {
    # Get datasets
    ?container djht:account ?account .
    ?container djht:published_dataset ?dataset .
    
    # Get faculty from depositor's account
    ?account djht:faculty_id ?faculty_id .
    
    # Get faculty name
    ?faculty rdf:type djht:Faculty ;
             djht:id ?faculty_id ;
             djht:name ?faculty_name .
  }
}
GROUP BY ?faculty_id ?faculty_name
ORDER BY DESC(?dataset_count)
```

**This query:**
- ✅ Only counts registered depositors (those with accounts)
- ✅ Ignores unregistered co-authors (avoids the problem you identified)
- ✅ Clear semantics: "Datasets deposited by each faculty"
- ✅ No double-counting (each dataset counted once)

---

## Migration Strategy (Simplified)

### What Gets Migrated

**Target:** 580 existing TU Delft datasets

**Strategy:** Extract faculty from **depositor's account**, not from author list.

### Migration Script (Revised)

**detect_faculty_patterns.py** (simplified version):

```python
import re
import csv

# TU Delft faculty patterns
FACULTY_PATTERNS = {
    285860001: [  # Aerospace Engineering
        r'Faculty of Aerospace Engineering',
        r'Aerospace Engineering',
        r'\bAE\b',
        r'Delft University of Technology, Flight Performance and Propulsion',
        r'Section Aircraft Noise'
    ],
    285860002: [  # Architecture
        r'Faculty of Architecture',
        r'Architecture and the Built Environment',
        r'\bA\+BE\b',
        r'\bBK\b'
    ],
    # ... other faculties
}

def detect_faculty_from_organizations(organizations_text):
    """
    Extract faculty from Organizations field.
    Returns: (faculty_id, confidence_score)
    """
    if not organizations_text:
        return None, 0.0
    
    for faculty_id, patterns in FACULTY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, organizations_text, re.IGNORECASE):
                confidence = 0.9 if 'Faculty of' in pattern else 0.7
                return faculty_id, confidence
    
    return None, 0.0

def process_datasets(input_csv):
    """
    Read datasets and detect faculty from Organizations field.
    Note: This assigns faculty based on DEPOSITOR context, not all authors.
    """
    with open(input_csv) as f:
        reader = csv.DictReader(f)
        results = []
        
        for row in reader:
            dataset_uuid = row['dataset_uuid']
            account_uuid = row['account_uuid']  # Depositor's account
            organizations = row['organizations']
            
            faculty_id, confidence = detect_faculty_from_organizations(organizations)
            
            results.append({
                'account_uuid': account_uuid,  # NOT dataset_uuid!
                'faculty_id': faculty_id,
                'confidence': confidence,
                'matched_text': organizations,
                'action': 'AUTO_ASSIGN' if confidence >= 0.8 else 'MANUAL_REVIEW'
            })
        
        return results
```

**Key Change:** We assign `faculty_id` to the **depositor's account**, not to the dataset or individual authors.

### Import Script (Revised)

**import_faculty_assignments.py**:

```python
def import_faculty_assignments(csv_file, dry_run=True):
    """
    Import faculty assignments to DEPOSITOR accounts.
    """
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            account_uuid = row['account_uuid']
            faculty_id = row['faculty_id']
            
            if not dry_run:
                # Update the Account entity (not Dataset or Author)
                sparql_query = f"""
                PREFIX djht: <https://data.4tu.nl/ontology/>
                INSERT {{
                  GRAPH <https://data.4tu.nl> {{
                    <account:{account_uuid}> djht:faculty_id {faculty_id} .
                  }}
                }}
                WHERE {{
                  GRAPH <https://data.4tu.nl> {{
                    <account:{account_uuid}> rdf:type djht:Account .
                  }}
                }}
                """
                execute_sparql(sparql_query)
            
            print(f"{'[DRY RUN] ' if dry_run else ''}Assigned faculty {faculty_id} to account {account_uuid}")
```

---

## Validation: Who Gets Faculty Assignment?

### Scope of Assignment

**Who gets `faculty_id`:**
- ✅ Registered users (those with `djht:Account`)
- ✅ Only during migration if they are depositors of TU Delft datasets
- ✅ Only if Organizations field contains detectable faculty pattern

**Who does NOT get `faculty_id`:**
- ❌ Unregistered co-authors (no Account entity)
- ❌ Authors who never deposited datasets
- ❌ External collaborators from other institutions

**Why this is acceptable:**
- Faculty statistics = "Datasets deposited by our faculty"
- Matches current institution_id semantics (only tracks depositor)
- Co-author contributions can be added in Phase 2

---

## Updated Success Metrics

### Technical Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| Account migration | ≥90% | Assign faculty to depositor accounts based on Organizations field |
| Faculty assignment accuracy | ≥90% | Correct faculty for migrated accounts |
| Datasets with faculty_id | ≥80% | Via depositor's account (indirect) |
| Unregistered authors | 0% | Explicitly NOT migrated (depositor-only approach) |

### Expected Outcomes

**For 580 TU Delft datasets:**
- ~450 depositor accounts assigned faculty automatically (high confidence)
- ~80 depositor accounts flagged for manual review (medium confidence)
- ~50 depositor accounts left without faculty (no pattern match)

**Statistics will show:**
- Faculty X deposited Y datasets
- Does NOT show: Faculty X authored Z datasets (co-authors ignored)

---

## Addressing Your Concern: Future-Proofing

### Extensibility to Author-Level Faculty

**The good news:** The RDF schema can easily support both approaches:

```turtle
# Current implementation (Phase 1)
<account:12345> djht:faculty_id 285860001 .

# Future extension (Phase 2)
<author:67890> djht:faculty_id 285860002 .  # Add this later
<author:67890> djht:account <account:12345> .

# Both can coexist!
```

**Migration path to author-level statistics:**
1. Add `faculty_id` predicate to Author entity in RDF schema
2. For registered authors: SPARQL query to copy from their account
3. For unregistered authors: run Organizations parser again
4. Create separate statistics views:
   - `statistics_faculty_deposited.sparql` (current, depositor-only)
   - `statistics_faculty_authored.sparql` (new, all authors)

---

## Revised Presentation Talking Points

### Slide 2: Problem Statement

**OLD (incorrect):**
> "Current system tracks institution-level only. Authors don't have faculty granularity."

**NEW (corrected):**
> "Current system tracks depositor's institution only. We need depositor's faculty for finer-grained statistics."

### Slide 7: Migration Strategy

**OLD (incomplete):**
> "Migrate 580 datasets to assign faculty based on Organizations field."

**NEW (accurate):**
> "Migrate ~200 depositor accounts to assign faculty based on their datasets' Organizations field. Statistics will count datasets by depositor's faculty (not co-author contributions)."

### Slide 10: Trade-offs

**Add this limitation:**

**Limitation:** Co-author faculty affiliations not tracked
- Current approach: Statistics count **depositor's faculty** only
- Unregistered co-authors: Faculty info remains in Organizations text field
- **Rationale:** Matches existing institution_id semantics (depositor-only)
- **Mitigation:** Future enhancement can add author-level faculty tracking

---

## Action Items

### Immediate (Assignment Scope)

1. ✅ **Clarify with stakeholders:** Confirm depositor-only statistics are acceptable
2. ✅ **Update SOLUTION_ARCHITECTURE.md:** 
   - Remove `faculty_id` from Author entity
   - Keep only on Account entity
   - Update migration scripts to target accounts, not datasets
   - Update statistics queries to use `djht:container/djht:account/djht:faculty_id`
3. ✅ **Update presentation:** Add "Limitations & Future Work" slide explaining co-author scope

### Future (Phase 2)

4. ⏳ **Author-level faculty tracking:** Add `faculty_id` to Author entity
5. ⏳ **Multi-faculty statistics:** Count author contributions, not just depositors
6. ⏳ **Organizations field cleanup:** Migrate free text to structured data

---

## Conclusion

**Thank you for catching this critical assumption!** 

The revised architecture:
- ✅ Correctly handles unregistered authors (by ignoring them for faculty stats)
- ✅ Maintains clear semantics (depositor-based statistics)
- ✅ Reduces migration complexity (only ~200 accounts vs 580 datasets)
- ✅ Remains extensible (can add author-level tracking later)
- ✅ Matches existing system behavior (institution_id is also depositor-only)

**Key insight:** The assignment asks for "faculty-level statistics" but doesn't specify whether this means depositor's faculty or all authors' faculties. The depositor-only interpretation is:
- More conservative (smaller scope)
- More consistent with current system (matches institution_id)
- More feasible for 5-week timeline
- Still valuable for institutional reporting

---

**Next Steps:**
1. Validate with stakeholders: Is "depositor-based faculty statistics" acceptable?
2. If yes: Update architecture documents with corrected approach
3. If no: Extend scope to author-level faculty (requires more time/resources)

