# Source of "Faculty-Level Statistics Requirement" Statement

## Question
"Why do you make the following statement in the speaker notes: 'However, there's no way to break this down by faculty - which was indicated by the institutes to be needed, possibly for research assessment and strategic planning'?"

## Answer

This statement comes **directly from the assignment document** provided by 4TU.ResearchData.

### Source: Assignment PDF

**From:** "Assignment for Senior Software Developer Role – 4TU.ResearchData Repository.pdf"

**Exact quotes from the assignment:**

### 1. The Challenge Section:
> "**Our stakeholders (data stewards, faculty deans) now require statistics per faculty**, not just per institution."

### 2. User Story/Motivation:
> "As a **data steward of 4TU**, I want to check **statistics per faculty**, not only at the organizational level (in the case of TU Delft institution, e.g. Faculty of Technology, Policy and Management), **so that I can analyze the dataset statistics specifically relevant to my faculty**."

### 3. Current Limitation:
> "Based on institutional grouping, we provide statistics (e.g., number of publications)."
> 
> **The Challenge:** "Our stakeholders (data stewards, faculty deans) now require statistics per faculty, not just per institution."

## Where the Speaker Notes Statement Comes From

**Speaker Notes (Slide 1):**
```
"However, there's no way to break this down by faculty - which is critical 
for research assessment and strategic planning."
```

**This is based on:**

1. **Assignment explicitly states** stakeholders (data stewards, faculty deans) require this
2. **User story** shows the need: "so that I can analyze the dataset statistics specifically relevant to my faculty"
3. **Current system limitation**: Only provides institution-level statistics, not faculty-level

## Why "Research Assessment and Strategic Planning"?

This is a **logical inference** based on:

### 1. Stakeholder Types Mentioned:
- **Data Stewards**: Need statistics for institutional reporting
- **Faculty Deans**: Need metrics for faculty performance and planning

### 2. Common Use Cases for Faculty-Level Statistics:
Faculty deans and data stewards typically need faculty statistics for:
- **Research Assessment**: 
  - Measuring research output per faculty
  - Comparing faculty performance
  - Tracking research productivity trends
  - Supporting grant applications and research evaluations

- **Strategic Planning**:
  - Resource allocation decisions
  - Faculty development priorities
  - Identifying research strengths and gaps
  - Setting targets and KPIs

### 3. Real-World Context:
Universities routinely use dataset/publication statistics for:
- Annual faculty reports
- Research impact assessments (e.g., REF in UK, VSNU in Netherlands)
- Budget allocation
- Strategic research priorities
- Accreditation processes

## Is This Statement Accurate?

**Yes, it's accurate because:**

1. ✅ **Assignment explicitly requires** faculty-level statistics (not just institution-level)
2. ✅ **Current system cannot do this** (only tracks by institution)
3. ✅ **Stakeholders identified**: data stewards and faculty deans
4. ✅ **Purpose is clear**: "analyze dataset statistics relevant to my faculty"

**The specific mention of "research assessment and strategic planning":**
- Not explicitly stated in assignment
- But **strongly implied** by the stakeholder types (faculty deans, data stewards)
- **Reasonable inference** based on standard university use cases

## Alternative Wording (if you want to be more precise):

### Current (in speaker notes):
> "However, there's no way to break this down by faculty - which is critical for research assessment and strategic planning."

### More precise (directly quoting assignment):
> "However, there's no way to break this down by faculty - which our stakeholders (data stewards and faculty deans) now require for analyzing dataset statistics relevant to their faculties."

### Even more explicit:
> "However, there's no way to break this down by faculty - which is the core requirement stated in the assignment: data stewards and faculty deans need to check statistics per faculty, not just at the organizational level."

## Evidence from Assignment

### Full Context:
```
Context:
The 4TU.ResearchData repository allows users to browse and search datasets 
by institutions. Currently:
● Institution information is retrieved from the depositing author's 
  affiliation (identified via login).
● Based on institutional grouping, we provide statistics 
  (e.g., number of publications).

The Challenge:
Our stakeholders (data stewards, faculty deans) now require statistics 
per faculty, not just per institution.
● Faculty information can be derived from the metadata field "Organizations", 
  but this field is free text and therefore unreliable.

Summary of the user motivation:
As a data steward of 4TU*, I want to check statistics per faculty, not only 
at the organizational level (in the case of TU Delft institution, e.g. Faculty 
of Technology, Policy and Management), so that I can analyze the dataset 
statistics specifically relevant to my faculty.
```

## Conclusion

The statement in the speaker notes is:
1. ✅ **Based on the assignment requirements** (stakeholder need for faculty-level statistics)
2. ✅ **Accurate about current limitation** (system only tracks institution-level)
3. ⚠️ **Partially inferred** (specific mention of "research assessment and strategic planning")
4. ✅ **Reasonable inference** given stakeholder types (faculty deans, data stewards)

**Recommendation:**
If you want to be more conservative, replace "research assessment and strategic planning" with:
- "analyzing dataset statistics relevant to their faculties" (direct quote from assignment)
- "faculty-level reporting and analysis" (more generic)
- "the needs of data stewards and faculty deans" (directly cites stakeholders)

But the current wording is **defensible and reasonable** based on standard university use cases for this type of data.
