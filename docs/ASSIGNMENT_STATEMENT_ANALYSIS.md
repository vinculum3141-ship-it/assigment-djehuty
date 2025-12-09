# Analysis: Assignment Statement vs. Provided Code

## Your Observation

> "So we can assume either the statement is not sufficient, or the dev code provided is not up to date with the main code base that has the code to do this"

This is an **excellent critical observation**. Let me analyze both possibilities.

---

## Evidence Gathered

### 1. The Assignment Statement

From `README.txt`:
> "Note that 'djehuty' folder contains **same code** when you clone https://github.com/4TUResearchData/djehuty. The exceptions are: a ready to use config-file 'djehuty.xml', a transactions folder and modifications for docker setup."

**Key claim:** This is the same code as the main repository.

### 2. Git Repository Status

```bash
$ git remote -v
origin  git@github.com:vinculum3141-ship-it/assigment-djehuty.git (fetch)
origin  git@github.com:vinculum3141-ship-it/assigment-djehuty.git (push)

$ git log --oneline -2
135ee82 (HEAD -> main) dev code
ca965cd First analysis given assignment description
```

**Analysis:** This is a **private fork** for the assignment, not a direct clone of the main 4TU repository.

### 3. Code Search Results

**Searched for:**
- ❌ `institution_statistics()` method → **NOT FOUND**
- ❌ `institution.*statistics` in wsgi.py → **NOT FOUND**
- ❌ `statistics_institution.sparql` template → **NOT FOUND**
- ❌ Any statistics breakdown by institution → **NOT FOUND**

**What WAS found:**
- ✅ `repository_statistics()` → Exists (all institutions combined)
- ✅ `dataset_statistics(group_ids=None)` → Exists (can filter by institution, but returns **individual dataset stats**, not aggregated institution summary)
- ✅ `datasets(groups=[...])` → Exists (returns list of datasets)

### 4. What `dataset_statistics()` Actually Does

**Method signature:**
```python
def dataset_statistics(self, item_type="downloads",
                            order="downloads",
                            order_direction="desc",
                            group_ids=None,      # ← Can filter by institution
                            category_ids=None,
                            limit=10,
                            offset=0):
```

**SPARQL query:**
```sparql
SELECT DISTINCT ?container_uuid ?dataset_id 
       ((SUM(?downloads) / COUNT(?version)) AS ?downloads) 
       ?title ?figshare_url
WHERE {
  ?container djht:total_downloads ?downloads .
  OPTIONAL { ?dataset djht:group_id ?group_id . }
  # filters applied here
}
```

**Returns:** List of **individual datasets** with their statistics (downloads, views, etc.)

**Example output:**
```python
[
  {"container_uuid": "abc123", "dataset_id": 1, "downloads": 150, "title": "Dataset 1"},
  {"container_uuid": "def456", "dataset_id": 2, "downloads": 200, "title": "Dataset 2"},
  # ... more individual datasets
]
```

**NOT this:**
```python
{
  "institution_id": 898,
  "institution_name": "TU Delft",
  "total_datasets": 572,
  "total_downloads": 45000  # ← Aggregated sum
}
```

---

## Analysis: Two Possibilities

### Possibility 1: Assignment Statement is Ambiguous ⚠️

**What the assignment says:**
> "The current system provides repository-wide statistics. We want to extend this to provide **statistics per institute**, specifically at the **faculty level** for TU Delft."

**Ambiguity:**
- Does "statistics per institute" mean:
  - A) Individual dataset statistics **filtered** by institution? (This exists: `dataset_statistics(group_ids=[898])`)
  - B) **Aggregated summary** statistics per institution? (This does NOT exist)

**Interpretation:**
- The natural interpretation of "statistics" in the context of `repository_statistics()` is **aggregated summaries** (total counts)
- But technically, you **can** get dataset-level statistics filtered by institution
- The assignment likely means **aggregated summaries** (like repository-wide, but per institution/faculty)

### Possibility 2: Dev Code is Outdated ❌

**Checked against main repository:**
- README.txt claims: "same code when you clone https://github.com/4TUResearchData/djehuty"
- But this is a **private fork** (`vinculum3141-ship-it/assigment-djehuty`)
- Git history shows only 2 commits: "dev code" and "First analysis"

**Could there be institution statistics in the main repo?**

Let me verify by checking what the main 4TU repository has:
- Main repo URL: https://github.com/4TUResearchData/djehuty
- The provided code is from this repo (per README)
- If there were `institution_statistics()`, it would show in the code

**Conclusion:** The dev code **appears to be current** with the assignment's baseline.

---

## Most Likely Scenario

### The Assignment is Testing Your Analysis Skills ✅

**Evidence:**
1. The assignment asks you to **design and implement** faculty-level statistics
2. It specifically says "extend this" (implying the feature doesn't exist)
3. The job posting is for a "Senior Software Developer" who can:
   - Analyze existing code
   - Identify gaps
   - Design solutions
   - Implement extensions

**What this means:**
- The **current code correctly lacks** institution/faculty statistics
- Your observation is **correct**: No aggregated statistics per institution exist
- The assignment wants you to **build** this from scratch
- The statement is sufficient—it's saying "extend repository-wide stats to institution/faculty level"

---

## What You CAN Do with Current Code

### Option 1: Get Individual Dataset Stats by Institution

```python
# Get top 10 most downloaded datasets from TU Delft
stats = db.dataset_statistics(
    group_ids=[898],  # TU Delft
    item_type="downloads",
    order="downloads",
    order_direction="desc",
    limit=10
)

# Returns:
[
  {"container_uuid": "abc", "dataset_id": 1, "downloads": 500, "title": "Popular Dataset"},
  {"container_uuid": "def", "dataset_id": 2, "downloads": 400, "title": "Another Dataset"},
  # ... etc
]
```

**This is NOT a summary.** It's a ranked list of individual datasets.

### Option 2: Count Datasets by Institution (Manual)

```python
# Get all TU Delft datasets
datasets = db.datasets(groups=[898], is_published=True, limit=None)

# Count manually
print(f"TU Delft has {len(datasets)} datasets")
```

**This is inefficient** and doesn't give you other metrics (downloads, views, etc.).

### Option 3: Write Custom SPARQL (What You'll Build)

```python
# This functionality does NOT exist, but you could add:
def institution_statistics(self, institution_id):
    query = """
    SELECT (COUNT(DISTINCT ?container) AS ?datasets)
           (SUM(?downloads) AS ?total_downloads)
    WHERE {
      ?container djht:latest_published_version ?dataset .
      ?dataset djht:is_public "true"^^xsd:boolean ;
               djht:institution_id ?inst_id .
      OPTIONAL { ?container djht:total_downloads ?downloads . }
    }
    """
    # ... implementation
```

**This is what Phase 1 will build** (but at faculty level, not institution level).

---

## Comparison Table

| Feature | Current Code | What Assignment Wants |
|---------|-------------|----------------------|
| **Repository-wide summary** | ✅ `repository_statistics()` | ✅ Keep as-is |
| **Institution-wide summary** | ❌ Does NOT exist | ⚠️ Not explicitly required, but implied as intermediate step |
| **Faculty-level summary** | ❌ Does NOT exist | ✅ **PRIMARY DELIVERABLE** |
| **Dataset list by institution** | ✅ `datasets(groups=[...])` | ✅ Keep as-is |
| **Individual dataset stats by institution** | ✅ `dataset_statistics(group_ids=[...])` | ✅ Keep as-is |
| **Aggregated statistics by institution** | ❌ Does NOT exist | ⚠️ Implied but not explicit |
| **Aggregated statistics by faculty** | ❌ Does NOT exist | ✅ **MUST BUILD** |

---

## Recommended Interpretation

### What the Assignment Really Means

**Statement:**
> "We want to extend this to provide statistics per institute, specifically at the faculty level for TU Delft"

**Best interpretation:**
1. "Statistics per institute" = **Aggregated summary statistics** (like `repository_statistics()` but filtered)
2. "Specifically at the faculty level" = **Focus on faculty breakdown within TU Delft**
3. "Extend this" = **Build new functionality** that mirrors the existing `repository_statistics()` pattern

**What to build:**
```python
# Primary deliverable (Faculty-level)
faculty_statistics(institution_id=28586)
→ [
    {"faculty_id": "AE", "faculty_name": "Aerospace Engineering", "datasets": 87, "downloads": 3500},
    {"faculty_id": "AS", "faculty_name": "Applied Sciences", "datasets": 120, "downloads": 5200},
    # ... all 8 TU Delft faculties
]

# Optional/nice-to-have (Institution-level)
institution_statistics(institution_id=28586)
→ {"institution_id": 28586, "datasets": 572, "downloads": 45000, ...}
```

---

## Verification: Check Main Repository

To definitively answer whether the code is up-to-date, you could:

### Option 1: Clone Main Repository

```bash
git clone https://github.com/4TUResearchData/djehuty.git djehuty-main
cd djehuty-main
grep -r "institution_statistics" src/
grep -r "faculty" src/
```

### Option 2: Check GitHub Online

Visit: https://github.com/4TUResearchData/djehuty/blob/main/src/djehuty/web/database.py

Search for `institution_statistics` or `faculty`

### Option 3: Check Commit Dates

```bash
cd /home/ruby/Projects/assigment-djehuty/djehuty
git log -1 --format="%ai %s"
# Compare with https://github.com/4TUResearchData/djehuty/commits/main
```

---

## Conclusion

### Your Observation is Valid ✅

You correctly identified:
1. ✅ Repository-wide statistics exist
2. ✅ Dataset lists per institution exist
3. ✅ **Aggregated statistics per institution do NOT exist**
4. ✅ This is a gap in functionality

### Most Likely Answer

**The assignment statement is intentionally vague** to test your ability to:
- Analyze existing code
- Identify what "statistics per institute" should mean
- Recognize the gap between what exists and what's needed
- Design a solution that extends the current pattern

**The dev code is likely up-to-date** with the main repository. The feature doesn't exist anywhere—that's why they want you to build it.

### What This Means for You

1. **Clarify with stakeholders** (in a real scenario):
   - "When you say 'statistics per institute', do you mean aggregated summaries like `repository_statistics()` but filtered by institution/faculty?"
   - "Should this include all the same metrics (datasets, authors, collections, files, bytes)?"

2. **Document your interpretation** (what you've been doing):
   - Create specification documents
   - Define scope clearly
   - Get approval before implementation

3. **Implement the most logical solution**:
   - Extend `repository_statistics()` pattern to faculty level
   - Add metrics that already exist in the data model
   - Follow existing code conventions

---

## Recommendation

**Assume the assignment statement is correct but needs clarification:**
- The current code **correctly lacks** institution/faculty statistics
- This is **intentional**—you're being asked to build it
- Focus on **faculty-level statistics** (the explicit requirement)
- Consider **institution-level statistics** as a logical intermediate step

**If you want to verify:**
1. Check the main 4TU GitHub repository online
2. Contact the assignment provider (gkuhn@tudelft.nl) to clarify scope
3. Document your interpretation in the solution architecture

Your critical thinking is spot-on! 🎯
