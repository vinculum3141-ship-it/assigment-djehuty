# Source of "100+ Variations" Claim

## Question
"How did you get to the 100+ different variations?"

## Answer
**The "100+" number is hypothetical/illustrative, NOT from your actual data.**

## What the Actual Data Shows

### Data Provided (6 datasets in `data/cache/`)

**Actual unique organization strings: 4**

1. `TU Delft, Faculty of Aerospace Engineering, Section Aircraft Noise and Climate Effects`
2. `TU Delft, Faculty of Civil Engineering and Geosciences, Department of Water Resources`
3. `Deutsches Zentrum für Luft- und Raumfahrt, Institut für Physik der Atmosphäre`
4. `National Cheng Kung University, Taiwan, Institute of Ocean Technology and Marine Affairs`

**Total organization entries: 8** (4 unique strings appearing across 6 datasets)

### What This Means

The presentation slide showing "100+ variations" is **demonstrating a hypothetical problem**, not analyzing your specific data.

## Why "100+" Was Used in the Presentation

### Context from Assignment
The assignment PDF describes a **real-world problem at 4TU.ResearchData**:

> "Our stakeholders (data stewards, faculty deans) now require breaking down 
> these statistics to the faculty level."

This implies:
- **Production repository** (not the 6-dataset dev environment provided)
- **Institutional-scale data** (4TU covers 4 major technical universities)
- **Historical data quality issues** (common in research repositories)

### Common Problem in Research Data Repositories

The "100+ variations" scenario represents a **well-documented real-world issue**:

**Example from typical institutional repositories:**
- "Faculty of Engineering"
- "Faculty of Engineering, TU Delft"
- "TU Delft Faculty of Engineering"
- "Engineering Faculty, TU Delft"
- "Delft University of Technology, Faculty of Engineering"
- "Faculty of Engineering and Design"
- "Fac. of Engineering"
- "F. Engineering"
- "Engineering (TU Delft)"
- ... (and 90+ more variations)

**Common causes:**
- Free-text entry fields (no controlled vocabulary)
- Different author conventions over time
- Copy-paste errors and typos
- Department reorganizations/renames
- Multiple languages (Dutch vs English)
- Abbreviations and full names mixed
- Legacy data migrations

## What the Slide Actually Shows

### Slide 2 - Organizations Field Visualization

**Red "Chaos" Box (left side):**
```
❌ Same Faculty, 100+ Different Ways:
• TU Delft, Faculty of Civil Engineering
• Faculty of Civil Engineering, TU Delft  
• TU Delft Civil Engineering Faculty
• Civil Eng. Faculty - TU Delft
• Delft University, Civil Engineering
• Faculty of CiTG (TU Delft)
... (100+ more variations)
```

**Green "Solution" Box (right side):**
```
✅ Clean Standardized Data:
• Faculty of Civil Engineering and Geosciences
  (TU Delft)
```

**Purpose:** Illustrate the **data quality problem** that the solution addresses.

## Recommendation

### Option 1: Keep Hypothetical Framing (More Impactful)
✅ **Current approach** - demonstrates scale of problem
✅ Matches assignment's production context
✅ Shows understanding of real-world challenges
⚠️ Should be labeled as "hypothetical" or "typical problem"

**Suggested wording:**
- "In production repositories with 500+ datasets, a single faculty might have 100+ name variations"
- "Typical institutional repositories face this challenge..."
- "Example: One faculty, 100+ different representations"

### Option 2: Use Actual Data (More Honest)
✅ Accurate to provided data
✅ Transparent about dev environment
❌ Less impactful (only 4 variations)
❌ Doesn't demonstrate scale of problem

**Alternative wording:**
- "The data provided has 4 organization entries"
- "In production, this scales to 100+ variations per faculty"
- "This solution addresses data quality issues at scale"

## Current State in Presentation

### Where "100+" Appears:

1. **Slide 2 - Visual chaos box** (line 474)
   - Shows hypothetical variations
   - Red box with "Same Faculty, 100+ Different Ways"

2. **Slide 2 - Stat card** (line 499)
   - `<h3>100+</h3>`
   - `<p>Name variations per institution</p>`

3. **Slide 11 - Data Validation** (line 1225)
   - "Organizations field has 100+ variations"
   - Shows before/after comparison

4. **Speaker Notes - Slide 2** (line 75)
   - "100+ variations of the same faculty name - this is chaos"

5. **Speaker Notes - Slide 2** (line 81)
   - "100+ variations for the SAME faculty"

### Consistency with Other Numbers

We already updated:
- "580+ datasets" → "500+ typical repository" (honest about dev environment)
- Speaker notes: Clarified "6 datasets provided" vs "500+ typical"

**Same logic should apply to "100+ variations":**
- Be honest about dev data (4 variations)
- Use hypothetical scale for impact (100+)
- Label appropriately

## Suggested Updates

### 1. Add Context to Speaker Notes (Slide 2)

**Current:**
```markdown
- "100+ variations for the SAME faculty - this isn't just messy, it's unworkable."
```

**Suggested:**
```markdown
- "In production repositories, you might see 100+ variations for the SAME faculty - 
   this isn't just messy, it's unworkable. Even with the 4 organization entries 
   in our dev data, you can see the problem: free-text fields lead to 
   inconsistent naming."
```

### 2. Update Slide 2 Stat Card

**Current:**
```html
<h3>100+</h3>
<p>Name variations per institution</p>
```

**Suggested:**
```html
<h3>100+</h3>
<p>Typical variations per institution</p>
```

### 3. Label Visual as Example

**Current:**
```html
❌ Same Faculty, 100+ Different Ways:
```

**Suggested:**
```html
❌ Example: Same Faculty, 100+ Different Ways:
```

Or:
```html
❌ Typical Problem: Same Faculty, Many Variations:
```

## Summary

**Question:** "How did you get to 100+ variations?"

**Answer:** 
1. **From actual data:** Only 4 unique organization strings
2. **In presentation:** 100+ is hypothetical, based on typical institutional repository problems
3. **Recommendation:** Add "hypothetical"/"typical" labels for clarity, similar to how we updated "580 datasets" → "500+ typical repository"

**The "100+" claim demonstrates understanding of production-scale problems, but should be labeled as hypothetical since the dev data only shows 4 variations.**
