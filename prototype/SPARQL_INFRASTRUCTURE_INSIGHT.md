# SPARQL Infrastructure Underutilization - A Key Insight

**Discovery**: The RDF/SPARQL infrastructure is **underutilized** for metadata enrichment.

---

## The Problem You Discovered 🔍

When you looked at the institution statistics, you noticed:
- ✅ `group_id` is available (28586, 28598, etc.)
- ❌ `institution_name` is **missing** or empty
- ❓ Why? The data exists in the triple store but isn't being leveraged!

**This is a system weakness you can highlight in the interview!** ✅

---

## Current State: Manual Mapping

### What Happens Now
1. Data steward runs SPARQL query → gets `group_id` values
2. Data steward **manually looks up** or **remembers**:
   - 28586 = "Delft University of Technology"
   - 28598 = "Utrecht University"
   - etc.
3. Data steward types institution names into Excel/CSV
4. Data steward sends report to stakeholder

**Problem**: Manual work, prone to errors, doesn't scale

---

## The RDF Data Actually Exists!

The institution names ARE in the triple store, just not easily accessible:

```sparql
PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>

# Find account with institution info
SELECT ?institution_id ?institution_name
WHERE {
  GRAPH <https://data.4tu.nl> {
    ?account djht:institution_id ?institution_id ;
             djht:institution_user_id ?institution_name .
  }
}
```

**The issue**: `group_id` (28586) ≠ `institution_id` (could be 898 or 28586)
- Two different ID systems
- No reliable join between them
- **Underutilized RDF infrastructure**

---

## How Your Prototype Could Improve This

### Approach 1: Create Proper RDF Entities (IDEAL)

**Add Institution entities to the RDF model**, just like you did for Faculties:

```turtle
@prefix djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/> .

# Institution entity
<https://data.4tu.nl/institutions/28586> a djht:Institution ;
    djht:id "tu-delft" ;
    djht:group_id 28586 ;
    djht:institution_name "Delft University of Technology" ;
    djht:institution_short_name "TU Delft" ;
    djht:country "Netherlands" .

<https://data.4tu.nl/institutions/28598> a djht:Institution ;
    djht:id "utrecht" ;
    djht:group_id 28598 ;
    djht:institution_name "Utrecht University" ;
    djht:institution_short_name "UU" ;
    djht:country "Netherlands" .
```

**Then your SPARQL query becomes simple**:

```sparql
SELECT ?group_id ?institution_name (COUNT(?dataset) AS ?count)
WHERE {
  ?institution djht:group_id ?group_id ;
               djht:institution_name ?institution_name .
  ?dataset djht:group_id ?group_id .
}
GROUP BY ?group_id ?institution_name
```

**Benefits**:
- ✅ Single source of truth for institution metadata
- ✅ No manual mapping needed
- ✅ Scales to thousands of institutions
- ✅ Faculties can reference institutions properly
- ✅ Enables hierarchical queries (institution → faculty)

---

### Approach 2: Lookup Table (PRAGMATIC)

**Create a simple Python mapping** (what your prototype currently does):

```python
# In database.py or a config file
INSTITUTION_NAMES = {
    28586: "Delft University of Technology",
    28598: "Utrecht University",
    28595: "Wageningen University",
    28592: "Eindhoven University of Technology",
    28589: "University of Twente"
}

def institution_statistics(self, ...):
    results = self.dataset_statistics(group_ids=institution_ids, ...)
    
    # Enrich with institution names
    for result in results:
        group_id = result.get('group_id')
        result['institution_name'] = INSTITUTION_NAMES.get(group_id, f"Institution {group_id}")
    
    return results
```

**Benefits**:
- ✅ Works immediately (no RDF changes needed)
- ✅ Simple to implement
- ❌ Manual maintenance required
- ❌ Doesn't leverage SPARQL infrastructure

---

## Interview Talking Points 🎯

### 1. Identifying System Weakness (Gabriela Said This Is Good!)

> "I noticed the institution statistics only return `group_id` without names. This reveals that the **RDF/SPARQL infrastructure is underutilized** for metadata enrichment. The institution names exist in the system but aren't structured as first-class RDF entities, so data stewards manually map IDs to names in their reports."

### 2. Your Prototype Shows the Better Way

> "For faculty-level statistics, I created proper RDF entities with `Faculty` type, `faculty_name`, and `group_id`. This means:
> - No manual mapping needed
> - Single source of truth
> - SPARQL can join datasets → faculties → institutions hierarchically
> - The same pattern could be applied to Institution entities"

### 3. Architecture Improvement Proposal

> "**Recommendation**: Create `Institution` RDF entities (like I did for `Faculty`) to eliminate manual mapping and fully leverage the SPARQL infrastructure. This would:
> - Enable automated reporting for institutions AND faculties
> - Provide hierarchical queries (university → faculty → department)
> - Reduce data steward workload
> - Scale to hundreds of institutions"

### 4. What You've Demonstrated

> "My prototype proves this approach works:
> - `Faculty` entities with proper RDF structure ✅
> - `faculty_statistics()` method that auto-enriches with names ✅
> - Dashboard that shows results without manual mapping ✅
> - The same pattern extends to institutions, departments, labs, etc."

---

## The Dashboard Display Issue You Noticed

You said: **"in the display the institution_name has no data"**

**Why?**
- Your `institution_statistics()` wrapper just calls `dataset_statistics()`
- `dataset_statistics()` only queries `group_id`, not institution names
- There are no `Institution` RDF entities to join with

**Fix Options**:

### Quick Fix (Pragmatic)
Update `generate_dashboard_data.py` to add institution names manually:

```python
INSTITUTION_NAMES = {
    28586: "TU Delft",
    28598: "Utrecht",
    28595: "Wageningen",
    28592: "Eindhoven",
    28589: "Twente"
}

def get_institution_statistics(db):
    stats = db.institution_statistics()
    
    # Add names manually (demo purposes)
    for stat in stats:
        group_id = stat.get('group_id')
        stat['institution_name'] = INSTITUTION_NAMES.get(group_id, f"Institution {group_id}")
    
    return stats
```

### Better Fix (RDF-Proper)
Create `Institution` entities in RDF (like you did for faculties), then update the SPARQL query.

---

## What to Show in the Interview

### Option A: Show the Weakness, Explain the Solution

1. **Show dashboard** with missing institution names
2. **Explain**: "Currently empty because no Institution RDF entities exist"
3. **Point to Faculty entities**: "But I created Faculty entities properly"
4. **Explain the improvement**: "Same pattern could fix institutions too"

**This demonstrates**:
- ✅ You identify system weaknesses
- ✅ You understand RDF/SPARQL architecture
- ✅ You propose scalable solutions
- ✅ Gabriela said this is "welcome and expected"!

### Option B: Quick Fix Before Interview

Add the manual mapping to `generate_dashboard_data.py` so institution names appear.

**This demonstrates**:
- ✅ Pragmatic problem-solving
- ✅ Working demo
- ❌ But less impressive architecturally

---

## Recommendation: Use Option A 🎯

**Show the gap, explain the solution**. This is MORE impressive than hiding it because:

1. **Gabriela explicitly said**: Identifying system weaknesses is "welcome and expected"
2. **Shows deep thinking**: You understand RDF architecture
3. **Shows honesty**: Not hiding limitations
4. **Shows vision**: You can articulate the proper solution
5. **Shows your Faculty work is better**: You DID create proper RDF entities for faculties!

---

## Interview Script for This Point

**When showing the dashboard**:

> "You'll notice the institution names are missing here. That's because the current system doesn't have Institution RDF entities—data stewards manually map `group_id` values like 28586 to 'TU Delft' in their reports. 
>
> This is actually a **system weakness I identified**: the RDF/SPARQL infrastructure is underutilized for metadata enrichment.
>
> For faculty-level statistics, I took a different approach. Look at my Faculty RDF entities [show sample_faculties.ttl]:
> - Proper `djht:Faculty` type
> - `faculty_name` and `faculty_short_name` properties  
> - `group_id` for dataset linking
> - `institution_id` for hierarchy
>
> This means faculty statistics **auto-populate with names**—no manual mapping needed. The same pattern could be applied to Institution entities to fix the manual mapping problem at that level too.
>
> So my prototype not only adds faculty-level granularity, it demonstrates how to properly leverage the SPARQL infrastructure for automated, scalable reporting."

---

## Summary

| Aspect | Current State | Your Prototype | Proposed Improvement |
|--------|--------------|----------------|---------------------|
| **Institution Names** | Manual mapping | Manual mapping (pragmatic) | RDF Institution entities |
| **Faculty Names** | N/A (doesn't exist) | **Auto from RDF** ✅ | Already done! |
| **SPARQL Usage** | Underutilized | Better for faculties | Fully leveraged |
| **Scalability** | Doesn't scale | Scales for faculties | Would scale for all |
| **Data Steward Work** | High (manual) | Low for faculties | Eliminated |

**Key Insight**: Your Faculty implementation is BETTER than the current Institution implementation. This is a strength, not a weakness! 🚀

---

## Bottom Line

**Yes, highlight this!** It shows:
1. ✅ You identified a system weakness (Gabriela wants this)
2. ✅ You understand RDF/SPARQL architecture deeply  
3. ✅ Your Faculty solution is more sophisticated than Institution approach
4. ✅ You can propose scalable improvements
5. ✅ You're honest about limitations (builds trust)

This turns what seems like a "missing feature" into a **demonstration of your architectural thinking**! 💡
