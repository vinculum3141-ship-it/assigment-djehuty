# Email Template: Discovery Communication to Stakeholders

**Purpose:** Communicate partial implementation discovery and request feedback/guidance

**Audience:** Hiring manager, technical lead, or assignment evaluator

**Tone:** Professional, transparent, collaborative, shows initiative

---

## Email Template

# Email Template: Discovery Communication for Presentation Assignment

**Purpose:** Communicate partial implementation discovery in context of presentation assignment

**Audience:** Hiring manager, technical lead, or assignment evaluator

**Context:** This is a 15-minute PRESENTATION (conceptual design, technical approach, edge cases), not full design documentation

**Deliverable:** 10-15 minute presentation covering conceptual design, technical approach, data handling, advantages/limitations

**Tone:** Professional, transparent, collaborative, shows architectural thinking

---

## Email Template (Presentation Assignment Context)

**Subject:** Presentation Assignment: Baseline Assumption Question for Faculty Statistics

---

Dear [Hiring Manager / Technical Lead],

I hope this message finds you well. I'm writing to seek clarification on a baseline assumption for the **faculty-level statistics presentation** (10-15 minutes) and how this discovery should be reflected in the conceptual design.

### Discovery Summary

While analyzing the existing system architecture to prepare the presentation, I discovered a **baseline assumption conflict**:

**The Assignment States:**  
*"Institution-level statistics already exist, you need to design faculty-level statistics."*

**The Codebase Reality:**  
Institution-level statistics are **only partially implemented** (infrastructure exists but incomplete).

**Existing Architecture Components:**
- ✅ Institution grouping mechanism (`djht:group_id` predicate in RDF schema)
- ✅ Dataset filtering by institution (`dataset_statistics(group_ids=[...])` method)
- ✅ SPARQL template infrastructure with dynamic query generation
- ❌ Complete aggregation layer for institution statistics (returns lists, not aggregated counts)
- ❌ Full reporting endpoints for institution-level statistics
- ❌ Hierarchical organization infrastructure

### The Design Baseline Question

This discovery creates a fundamental design question about **what baseline to design from**:

**Should I design assuming:**

**A) Assignment Specification as Reality** → "Institution statistics are complete"
- Design only faculty-level additions (per assignment literal reading)
- Assume institution statistics work fully (as assignment states)
- Clean, focused scope on genuinely new capability
- **Demonstrates:** Ability to follow specifications, focused design

**B) Codebase Reality as Baseline** → "Institution statistics are partial"
- Design completion of institution layer + faculty additions
- Address the technical debt discovered in analysis
- More comprehensive scope acknowledging reality
- **Demonstrates:** Code analysis skills, identifying gaps, system improvement

**C) Intent Recognition** → "Partial implementation suggests extension was intended"
- Design leveraging existing patterns (extending what exists)
- Treat partial institution stats as foundation to build on
- Recognize that `djht:group_id` predicate suggests hierarchical extension was planned
- **Demonstrates:** Architectural judgment, pattern recognition, pragmatic design

### Why This Matters

This isn't just about scope—it's about **what world I'm designing for**:

- **Design for stated world (A):** Follow assignment literally, ignore codebase reality
- **Design for actual world (B):** Address what's really there, broader scope
- **Design for intended world (C):** Recognize partial implementation as intentional extension point

Each approach demonstrates different competencies:
- **(A) Specification Compliance:** Tests ability to follow requirements as written
- **(B) Gap Analysis:** Tests ability to identify and address technical debt
- **(C) Architectural Judgment:** Tests ability to recognize patterns and intent in existing code

### Impact on Presentation Approach

This baseline question affects the structure and focus of the 10-15 minute presentation:

| Aspect | Presentation Path A:<br/>Assignment Baseline | Presentation Path B:<br/>Reality Baseline | Presentation Path C:<br/>Intent Recognition |
|--------|----------------------------------------|-------------------------------------|--------------------------------------|
| **Assumption** | "Institution stats complete" | "Institution stats partial" | "Extension intended" |
| **Conceptual Design** | Faculty-only solution | Complete statistics system | Faculty extending institution pattern |
| **Technical Approach** | New faculty components | Institution completion + Faculty | Hierarchical extension pattern |
| **Problem Definition** | "No faculty statistics" | "Incomplete statistics overall" | "Missing hierarchical layer" |
| **Specific Weakness** | "Lack of faculty capability" | "Incomplete system infrastructure" | "Incomplete grouping hierarchy" |
| **Time Allocation** | 100% faculty (~15 min) | 40% institution, 60% faculty (~15 min) | 20% existing, 80% faculty (~15 min) |
| **Existing System** | Not discussed | Analyzed as incomplete | Analyzed as foundation |

### Presentation Content Options

The 10-15 minute presentation must cover:
1. ✅ Conceptual design of solution
2. ✅ Technical approach (data model changes, algorithms, integration strategies)
3. ✅ Handling of existing data and edge cases
4. ✅ Advantages and potential limitations
5. ✅ System strengths/weaknesses and how to address specific weakness

**How each baseline shapes the presentation:**

**Path A: Faculty-Only Presentation (Assignment Baseline)**
- **Assumption:** Institution statistics are complete (per assignment statement)
- **Conceptual Design:** Faculty-level solution as new capability
- **Technical Approach:** Faculty metadata extraction, faculty aggregation algorithms
- **Data Handling:** Strategies for faculty-level existing data (ORCID, affiliations)
- **Edge Cases:** Multiple affiliations, missing ORCID, inconsistent faculty metadata
- **System Weakness Identified:** "Lack of faculty-level statistics capability"
- **Presentation Time:** 100% on faculty-specific solution (~15 minutes)
- **Existing System Context:** Not discussed in detail

**Path B: Comprehensive Presentation (Reality Baseline)**
- **Assumption:** Institution statistics are incomplete (per codebase analysis)
- **Conceptual Design:** Complete statistical hierarchy (both institution and faculty)
- **Technical Approach:** Institution aggregation + faculty aggregation algorithms
- **Data Handling:** Strategies for both institution and faculty existing data
- **Edge Cases:** Both institution-level and faculty-level challenges
- **System Weakness Identified:** "Incomplete statistical infrastructure overall"
- **Presentation Time:** ~40% institution completion, ~60% faculty additions (~15 minutes)
- **Existing System Context:** Analyzed as incomplete, gaps identified

**Path C: Extension Presentation (Intent Recognition)**
- **Assumption:** Partial implementation suggests extension pattern was intended
- **Conceptual Design:** Faculty statistics leveraging and extending existing `djht:group_id` pattern
- **Technical Approach:** Hierarchical extension algorithm (faculty within institution)
- **Data Handling:** Extend existing institution metadata approach to faculty level
- **Edge Cases:** Extension point challenges (hierarchy conflicts, multiple affiliations)
- **System Weakness Identified:** "Missing hierarchical layer in grouping architecture"
- **Presentation Time:** ~20% existing pattern analysis, ~80% faculty extension design (~15 minutes)
- **Existing System Context:** Analyzed as foundation to extend

### Request for Clarity

Before preparing the final presentation, I'd appreciate clarity on which baseline to use:

**The Core Question:**
Which baseline should the presentation assume?

**Option A:** Institution statistics are complete (follow assignment statement literally)
- Presentation focuses entirely on faculty solution
- Existing system context not discussed
- Weakness identified: "Lack of faculty statistics"

**Option B:** Institution statistics are incomplete (acknowledge codebase reality)
- Presentation covers institution completion + faculty additions
- Existing system analyzed as incomplete
- Weakness identified: "Incomplete statistical infrastructure"

**Option C:** Partial implementation is foundation (leverage existing pattern)
- Presentation shows faculty extending existing institution pattern
- Existing system analyzed as foundation to build on
- Weakness identified: "Missing hierarchical layer in grouping"

**Impact on Presentation:**
The baseline choice affects:
- How I define the problem
- Which system weakness I identify and address
- How much time is spent on existing system analysis
- Whether the solution is framed as new capability, completion, or extension

I can prepare the presentation effectively for any of these baselines - I just need clarity on which approach aligns with your expectations for the interview.

### Request for Guidance

Before finalizing the presentation, I need clarity on the **baseline assumption**:

**Question 1: What baseline should the presentation assume?**
- A) Institution statistics are complete (per assignment statement)?
- B) Institution statistics are partial (per codebase reality)?
- C) Partial implementation is foundation to extend (leverage existing pattern)?

**Question 2: How should I structure the 15-minute presentation?**
- Should I include analysis of existing infrastructure as context?
- Or present "clean slate" as if no institution infrastructure exists?
- Should the discovery be part of the presentation narrative?

**Question 3: Which system weakness should I identify and address?**
- Path A frames weakness as: "No faculty-level statistics capability"
- Path B frames weakness as: "Incomplete statistical system overall"
- Path C frames weakness as: "Missing hierarchical layer in grouping architecture"

**Impact on Presentation:**
The baseline choice affects how I define the problem, structure the solution, and identify the system weakness to address.

I can prepare an effective presentation for any of these baselines - I'm simply seeking clarity on which approach you'd like to see for the interview.

### Presentation Deliverables Prepared

Regardless of which path you prefer, I've prepared presentation content for all three approaches:

**Path A Presentation Content (Faculty-Only):**
- Slides covering conceptual design, technical approach, data handling, edge cases
- Focused scope: Faculty metadata extraction and aggregation
- System weakness: "No faculty-level statistics"
- ~12 slides, 15-minute timing

**Path B Presentation Content (Comprehensive):**
- Slides covering complete statistical hierarchy design
- Broad scope: Institution completion + faculty additions
- System weakness: "Incomplete statistical infrastructure overall"
- ~18 slides, 15-minute timing

**Path C Presentation Content (Extension):**
- Slides covering existing pattern analysis + faculty extension design
- Balanced scope: Extension of institution pattern to faculty level
- System weakness: "Missing hierarchical layer in grouping architecture"
- ~15 slides, 15-minute timing
- Includes: Existing `djht:group_id` analysis, hierarchical extension design, integration strategy

**Supporting Materials (All Paths):**
- Technical analysis of existing infrastructure
- Data model diagrams (RDF schema extensions)
- Algorithm pseudocode (metadata extraction, aggregation)
- Edge case analysis documentation
- Code feasibility exploration notes

### My Plan

**If I don't hear back by [DATE]**, I'll prepare the presentation following **Path C** as it balances assignment scope with codebase reality and provides a clear narrative within 15 minutes.

However, I can easily adjust to Path A or Path B based on your guidance.

### My Assumption

**If I don't hear back by [DATE]**, I'll prepare the presentation following **Path C (Extension Presentation - Intent Recognition)** for the following reasons:

**Why Path C for a 15-minute presentation:**
1. **Fits the format:** 15 minutes is perfect for showing analysis (existing system) + solution (faculty extension)
2. **Assignment states "institution stats exist"** - Path C respects this by treating partial implementation as foundation
3. **Addresses required deliverable:** Can clearly identify "missing hierarchical layer" as **specific weakness to address**
4. **Demonstrates architectural thinking:** Shows I can analyze existing systems and propose pragmatic extensions
5. **Balances scope:** Focused on faculty (per assignment) while acknowledging partial implementation reality
6. **Good presentation narrative:** "I found this pattern → I propose extending it → Here's how" is compelling storytelling

**Why NOT Path A (Faculty-only ignoring existing infrastructure):**
- Presenting "as if institution stats are complete" when they're partial feels dishonest
- Can't meaningfully discuss system weaknesses if I ignore discovered gaps
- Misses opportunity to show code analysis skills

**Why NOT Path B (Comprehensive institution + faculty):**
- Too broad for 15-minute presentation (would need to rush)
- May be seen as scope creep beyond assignment
- Assignment explicitly says "institution stats already exist"

**Path C Presentation Structure (15 minutes):**
- **Min 1-3:** Problem + Discovery (faculty stats missing, but institution pattern exists)
- **Min 4-7:** Conceptual Design (extend `djht:group_id` hierarchically to faculties)
- **Min 8-10:** Technical Approach (data model changes, extraction algorithms, aggregation)
- **Min 11-13:** Data Handling + Edge Cases (existing data migration, multiple affiliations, missing ORCID)
- **Min 14-15:** Advantages + System Weakness Addressed (hierarchical layer was missing)

However, I can easily pivot to Path A or Path B if that better serves the evaluation criteria.

### Presentation Deliverables

Regardless of baseline approach, the presentation will cover all required elements:
- ✅ **Conceptual design of solution** (faculty statistics approach)
- ✅ **Technical approach** (data model changes, metadata extraction algorithms, integration strategies)
- ✅ **Handling of existing data and edge cases** (migration strategy, multiple affiliations, missing ORCID, inconsistent metadata)
- ✅ **Advantages and potential limitations** (benefits to stakeholders, technical constraints)
- ✅ **System strengths and weaknesses** (specific weakness identified and how to address it)

The baseline choice affects **which problem I present** and **which weakness I identify**, but not the quality or depth of the presentation.

### Transparency Note

I want to be transparent about this discovery because:

1. **It affects the presentation structure:** The baseline assumption determines how I frame the problem and solution
2. **It demonstrates code analysis:** Finding the partial implementation shows thorough system analysis
3. **It impacts which weakness I address:** Different baselines identify different system weaknesses
4. **Interview context:** I want to ensure the presentation aligns with what you're looking to evaluate

**The Core Question:**
- Assignment says: "Institution statistics exist"
- Codebase shows: "Institution statistics partial"
- Question: Which baseline should the interview presentation assume?

I can deliver an effective presentation for any baseline - I'm simply seeking clarity to ensure alignment with interview expectations.

Please let me know your preference, or feel free to discuss during our next interaction.

Best regards,  
[Your Name]

---

**Attachments (Optional):**
- `PARTIAL_IMPLEMENTATION_ANALYSIS.md` - Existing system analysis
- `PROJECT_OVERVIEW.md` - Complete architectural overview
- `SOLUTION_ARCHITECTURE.md` - Detailed design specification

---

## Alternative: Shorter Version (For Time-Constrained Reviewers)

**Subject:** Interview Presentation: Baseline Clarification for Faculty Statistics

---

Dear [Name],

**Context:** I'm preparing the 10-15 minute **interview presentation** on faculty-level statistics.

**Baseline Question:**

- **Assignment states:** "Institution-level statistics already exist, add faculty-level statistics"
- **Codebase shows:** Institution statistics are only **partially implemented**

**Clarification Needed: Which baseline should the presentation assume?**

**Path A:** Institution stats are complete (faculty-only solution, 15 min)  
**Path B:** Institution stats are incomplete (comprehensive solution, 15 min)  
**Path C:** Partial implementation is foundation (extension solution, 15 min)

**Impact on Presentation:**
- Which problem I define
- Which system weakness I identify and address
- How I structure the solution (new capability vs. completion vs. extension)
- Whether I include existing system analysis

**Presentation will cover (all paths):**
- ✅ Conceptual design, technical approach, data handling, edge cases
- ✅ Advantages/limitations, system strengths/weaknesses

**My plan:** Will prepare Path C by [DATE] unless I hear otherwise, as it balances assignment scope with codebase reality.

Can easily adjust to Path A or B based on your guidance.

Best,  
[Your Name]

---

**Assumption:** Will submit Extension Design (Option A) by [DATE] unless I hear otherwise.

**Attached:** Full architectural analysis for your review.

Best,  
[Your Name]

---

## Alternative: Very Formal/Academic Tone

**Subject:** Presentation Assignment: Baseline Assumption Clarification for Faculty Statistics Presentation

---

Dear [Title] [Last Name],

I am writing to request clarification regarding the **baseline assumption** for the faculty-level statistics presentation (10-15 minutes) prior to final preparation.

### Assignment Context

The assignment deliverable is a **10-15 minute presentation** covering:
1. Conceptual design of solution
2. Technical approach (data model changes, algorithms, integration strategies)
3. Handling of existing data and edge cases
4. Advantages and potential limitations
5. System strengths/weaknesses and how to address a specific weakness

The assignment specification states: *"Institution-level statistics already exist within the 4TU.ResearchData repository. Your task is to design faculty-level statistics."*

### Discovery: Baseline Assumption Conflict

During systematic analysis of the Djehuty codebase to prepare the presentation, I identified a **conflict between the assignment statement and the codebase reality**:

**Assignment Baseline:** "Institution-level statistics already exist"  
**Codebase Reality:** Institution-level statistics are **partially implemented**

**Existing Components:**
1. ✅ Institution grouping mechanism (`djht:group_id` predicate in RDF schema)
2. ✅ Dataset filtering by institution (`dataset_statistics(group_ids=[])` method)
3. ✅ SPARQL template infrastructure with dynamic query generation

**Incomplete Components:**
4. ❌ Aggregation layer for institution statistics (returns datasets, not aggregated counts)
5. ❌ Complete reporting endpoints for institution-level statistics  
6. ❌ Hierarchical organization infrastructure

### Impact on Presentation Structure

This discovery creates three valid presentation approaches with different baseline assumptions:

**Presentation Baseline A: Assignment Specification as Reality**
- **Assumption:** Institution statistics are complete (per assignment statement)
- **Presentation Approach:** Faculty-level solution only
- **Problem Defined:** "Repository lacks faculty-level statistics"
- **System Weakness:** "No faculty statistics capability"
- **Time Allocation:** 100% faculty solution (~15 minutes)
- **Existing System:** Not discussed

**Presentation Baseline B: Codebase Reality as Foundation**
- **Assumption:** Institution statistics are incomplete (per codebase analysis)
- **Presentation Approach:** Complete institution + faculty statistics
- **Problem Defined:** "Statistical infrastructure incomplete overall"
- **System Weakness:** "Incomplete statistical system"
- **Time Allocation:** ~40% institution, ~60% faculty (~15 minutes)
- **Existing System:** Analyzed as incomplete

**Presentation Baseline C: Extension Approach**
- **Assumption:** Partial implementation is foundation for hierarchical extension
- **Presentation Approach:** Faculty statistics extending existing institution pattern
- **Problem Defined:** "Missing hierarchical layer in grouping architecture"
- **System Weakness:** "Incomplete hierarchical organization infrastructure"
- **Time Allocation:** ~20% existing analysis, ~80% faculty extension (~15 minutes)
- **Existing System:** Analyzed as foundation to build on

### Request for Clarification

Which presentation baseline should I use for the interview?

**Primary Question:** Should the presentation assume:
1. Institution statistics are complete (follow assignment statement)?
2. Institution statistics are incomplete (address gaps comprehensively)?
3. Partial implementation is foundation (leverage and extend existing pattern)?

**Secondary Question:** Should the presentation structure include:
- Analysis of existing infrastructure as context?
- "Clean slate" approach with no existing system reference?

**Primary Question:** Should the 15-minute presentation assume:
1. Institution statistics are complete (follow assignment statement, present faculty-only solution)?
2. Institution statistics are incomplete (address gaps, present comprehensive solution)?
3. Partial implementation is intentional foundation (recognize pattern, present extension solution)?

**Secondary Question:** How should the presentation structure "system weakness to address"?
- Baseline A identifies weakness as: "No faculty statistics capability"
- Baseline B identifies weakness as: "Incomplete statistical system overall"
- Baseline C identifies weakness as: "Missing hierarchical layer in grouping architecture"

**Tertiary Question:** Should the presentation include:
- Analysis of existing system as context (supports Baseline C)?
### Presentation Deliverables (Unchanged Regardless of Baseline)

All three baseline approaches include complete 10-15 minute presentation covering:
- Conceptual design of faculty statistics solution
- Technical approach (data model changes, metadata extraction algorithms, aggregation strategies, integration patterns)
- Handling of existing data and edge cases (migration strategy, multiple author affiliations, missing ORCID, inconsistent metadata)
- Advantages and potential limitations (stakeholder benefits, technical constraints)
- System strengths and weaknesses analysis with specific weakness to address

The baseline choice affects **which problem is presented**, **which weakness is identified**, and **how the solution is framed**, but not the quality or depth of the presentation.

### Presentation Plan

I plan to prepare and deliver the presentation by [DATE]. If I do not receive clarification by [EARLIER DATE], I will proceed with **Baseline C** as it balances assignment scope with codebase reality within the 15-minute format.

However, I can readily adjust to Baseline A or B based on your guidance.

### Availability

I am available to discuss this at your convenience if clarification would be helpful.

Respectfully,  
[Your Full Name]  
[Date]

---

## Tips for Customizing

**Choose tone based on recipient:**
- **Informal/Collaborative:** Use first template (conversational, shows discovery process)
- **Formal/Academic:** Use third template (structured, emphasizes methodology)
- **Very Busy Person:** Use second template (short, gets to the point quickly)

**Key Elements to Always Include:**
1. ✅ Clear description of the baseline conflict (assignment vs. codebase)
2. ✅ Three baseline options (complete, incomplete, foundation)
3. ✅ Impact on presentation (problem definition, weakness identification, structure)
4. ✅ Request for clarity (which baseline to use)
5. ✅ Your plan (which you'll prepare by default)
6. ✅ Flexibility (can adjust based on feedback)

**What NOT to do:**
- ❌ Don't apologize for the discovery (it shows thorough analysis)
- ❌ Don't speculate about what they're evaluating (just ask for baseline clarity)
- ❌ Don't frame discovery as reducing work (it's about alignment)
- ❌ Don't make assumptions about their intent (simply request guidance)

**Interview Presentation Context:**
- This is for an interview, not a course assignment
- Focus on asking which baseline they want to see
- Avoid statements about "what demonstrates" - let them decide
- Keep it about impact on presentation structure, not evaluation criteria

**Timing:**
- **Best:** Send as soon as you discover the conflict
- **Good:** Send before you invest significant time in slides
- **Necessary:** Send before finalizing presentation approach

---

## Response Scenarios & How to Handle

### Scenario 1: "Follow the assignment - assume institution stats are complete."
**Response:**
> "Understood - thank you for clarifying. I'll prepare the presentation following Baseline A, designing faculty-level statistics assuming complete institution foundation. The presentation will focus exclusively on faculty-specific components per the assignment specification."

### Scenario 2: "Address the gaps - present both institution completion and faculty."
**Response:**
> "Thank you for the guidance. I'll prepare the presentation following Baseline B, covering comprehensive institution statistics completion plus faculty additions. This broader scope will include both institution and faculty solutions within the 15-minute format."

### Scenario 3: "Leverage what exists - present faculty extending the institution pattern."
**Response:**
> "Perfect - thank you for confirming. I'll prepare the presentation following Baseline C, showing faculty statistics as hierarchical extension of the existing institution pattern. The presentation will show how the `djht:group_id` pattern extends naturally to faculty level."

### Scenario 4: "Present all three approaches comparatively."
**Response:**
> "Excellent idea. I'll create a comparative presentation showing all three baseline approaches (Faculty-Only, Comprehensive, Extension) with trade-off analysis. This will demonstrate how baseline assumptions affect problem definition and solution structure within the 15-minute format."

### Scenario 5: "Let's discuss in our next meeting."
**Response:**
> "Perfect. I'll prepare a brief overview covering:
> 1. The baseline assumption conflict (assignment vs. codebase)
> 2. Analysis of existing institution infrastructure
> 3. Three presentation baseline options with different framings
> 4. Impact on presentation structure and weakness identification
> Looking forward to the discussion."

### Scenario 6: "How confident are you in this partial implementation assessment?"
**Response:**
> "Very confident - I've done thorough code analysis:
> - Traced `dataset_statistics()` execution flow showing list return (not aggregated counts)
> - Reviewed SPARQL templates confirming infrastructure exists but aggregation incomplete
> - Analyzed `djht:group_id` predicate usage showing hierarchical pattern foundation
> - Verified it's production-deployed and actively maintained
> I've documented all findings in `PARTIAL_IMPLEMENTATION_ANALYSIS.md` with code references. Happy to walk through the analysis together if helpful."

### Scenario 7: "Just follow the assignment as stated."
**Response:**
> "Understood completely. I'll prepare the presentation following Baseline A (assignment specification), presenting only faculty-level components and assuming institution statistics are fully functional as stated. This removes any ambiguity about scope."

### Scenario 8: No response received
**Follow-up after 2-3 days:**
> "Quick follow-up on my email from [DATE] regarding the baseline question for the faculty statistics interview presentation.
>
> **Core question:** Should the presentation assume institution stats are complete (per assignment) or partial (per codebase)?
>
> I'm planning to prepare **Baseline C** starting [DATE] unless I hear otherwise, as it balances assignment scope with codebase reality within 15 minutes.
>
> Please let me know if you prefer Baseline A or B instead, or would like to discuss further."

---

**Save this template as:** `docs/meta/STAKEHOLDER_COMMUNICATION_EMAIL.md`
