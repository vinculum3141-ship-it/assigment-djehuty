# ORCID Data Investigation

## Question
"You make this statement in the speaker notes of slide 9: 'ORCID records currently only contain institution-level affiliation anyway, not faculty-level detail.' How sure are you of that statement, what evidence do you have of this?"

## Answer
**I am NOT sure of that statement - it was an assumption without proper verification.**

## What I Actually Know

### From Djehuty Codebase:

1. **ORCID Integration Exists:**
   - `djehuty/src/djehuty/web/wsgi.py` has ORCID OAuth2 authentication
   - Uses `/read-public` scope to read public ORCID profiles
   - Stores `orcid_id` in user accounts

2. **What Djehuty Actually Uses:**
   - Only the ORCID identifier itself (`orcid_id`)
   - Does NOT appear to fetch employment/affiliation data from ORCID API
   - No code found that parses ORCID employment records

### What ORCID Actually Provides (from ORCID API Documentation):

**ORCID records CAN contain:**
- **Employment records** with:
  - Organization name
  - Organization identifier (ROR, GRID, etc.)
  - Department name
  - Role title
  - Start/end dates
  
- **Education records** with similar structure

- **Affiliation details** that MAY include department-level information

**Example ORCID Employment Record Structure:**
```json
{
  "employment-summary": {
    "organization": {
      "name": "Delft University of Technology",
      "address": {
        "city": "Delft",
        "country": "NL"
      },
      "disambiguated-organization": {
        "disambiguated-organization-identifier": "grid.5292.c",
        "disambiguation-source": "GRID"
      }
    },
    "department-name": "Faculty of Aerospace Engineering",
    "role-title": "Assistant Professor"
  }
}
```

## The Problem with My Statement

### What I Claimed:
> "ORCID records currently only contain institution-level affiliation anyway, not faculty-level detail."

### Why This Is Likely WRONG:

1. **ORCID DOES support department names** - the `department-name` field exists
2. **Some ORCID profiles DO include faculty information** - if users add it
3. **Whether Djehuty USES this data is different from whether ORCID HAS it**

### What I Should Have Said:

**Option 1 - Honest about uncertainty:**
> "Based on the Djehuty codebase, it appears the system only stores the ORCID identifier itself, not employment or affiliation details from ORCID profiles. I haven't verified whether ORCID profiles actually contain faculty-level information, or whether Djehuty could be enhanced to fetch that data."

**Option 2 - Focus on what Djehuty actually does:**
> "Currently, Djehuty only stores the ORCID identifier from user authentication. It doesn't fetch employment or affiliation records from the ORCID API, even though that data may be available in users' ORCID profiles. This means we can't rely on ORCID as a source for faculty information without enhancing the integration."

**Option 3 - Make it about data quality, not ORCID capabilities:**
> "Even if ORCID profiles contain faculty information, we can't rely on it as our primary data source for two reasons: First, not all users have ORCID accounts. Second, even users with ORCID may not have kept their employment records current, or may not have included department-level details. Therefore, we need users to explicitly select their faculty during registration."

## Recommendations

### For the Speaker Notes:

**Replace the problematic statement in Slide 8 (Edge Case 2 - Missing ORCID):**

**Current (INCORRECT):**
```markdown
**Not a Blocker:**
- "This turns out not to be a blocker for our solution."
- "ORCID records currently only contain institution-level affiliation anyway, not faculty-level detail."
- "So even if we had ORCID data for everyone, it wouldn't help us determine faculty."
```

**Proposed (ACCURATE):**
```markdown
**Not a Blocker:**
- "This turns out not to be a blocker for our solution."
- "Currently, Djehuty only stores the ORCID identifier itself - it doesn't fetch employment or affiliation records from ORCID profiles."
- "Even if we enhanced the integration to fetch that data, we couldn't rely on it as the primary source because: (1) Not all users have ORCID accounts, and (2) Even users with ORCID may not keep their employment records current or include department details."
- "Therefore, capturing faculty during registration remains the most reliable approach."
```

### Possible Enhancement (Out of Scope for This Assignment):

Djehuty COULD be enhanced to:
1. Fetch employment records from ORCID API during authentication
2. Parse the `department-name` field
3. Use pattern matching to map department names to faculty_id values
4. Auto-populate the faculty field with confidence scoring

This would be a Phase 2+ enhancement, not something to build now.

## Conclusion

**I was wrong to state categorically that ORCID only contains institution-level data.**

The truth is more nuanced:
- ORCID CAN contain faculty/department information (if users add it)
- Djehuty currently doesn't fetch or use that data
- Even if available, ORCID data has reliability issues (not all users, not always current)
- The proposed solution (capture during registration) is still the right approach

**Thank you for questioning this - it's exactly the kind of scrutiny that improves the quality of technical presentations.**
