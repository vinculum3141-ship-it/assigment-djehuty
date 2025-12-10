# 📚 Demo Materials Index

**Complete guide to all interview demo materials**

Last updated: $(date +%Y-%m-%d)

---

## 🎯 Quick Start

**First time preparing?** Read in this order:

1. **PROTOTYPE_PLAN.md** - Understand the full strategy
2. **PROGRESS.md** - See what's been accomplished
3. **DEMO_SCRIPT.md** - Learn the 15-minute demo flow
4. **DEMO_DAY_CHECKLIST.md** - Prepare for interview day

**Day of interview?** Use:

1. **DEMO_DAY_CHECKLIST.md** - Complete checklist (2 hours before → follow-up email)
2. **verify_demo.sh** - Automated environment check (30 min before)
3. **DEMO_QUICK_REFERENCE.md** - Essential commands (print and keep visible)
4. **DEMO_TROUBLESHOOTING.md** - Emergency fixes (if something breaks)

---

## 📋 All Documents

### Strategy & Planning

**PROTOTYPE_PLAN.md** (1700+ lines)
- Purpose: Complete 7-day prototype strategy
- Use when: Understanding the full scope and approach
- Key sections:
  * Why prototype approach vs full implementation
  * Three phases (Model, Migration, Visualization)
  * Timeline and estimates
  * Technical architecture
  * Edge cases and limitations
  * Success criteria
- **Read this**: Before starting work, to understand big picture

**PHASE1_FOCUS.md** (400+ lines)
- Purpose: Detailed Phase 1 implementation plan
- Use when: Implementing RDF model and backend
- Key sections:
  * Phase 1 specific tasks
  * RDF schema extension
  * Backend implementation details
  * Testing strategy
- **Read this**: When implementing Phase 1 components

**PROGRESS.md** (300 lines)
- Purpose: What's been accomplished so far
- Use when: Want to know current status
- Key sections:
  * Completed work breakdown
  * Current capabilities (with examples)
  * Interview talking points
  * Timeline update (28.5% complete)
  * Next steps
  * Quality metrics
- **Read this**: Before demo preparation, to understand what works

---

### Demo Preparation

**DEMO_SCRIPT.md** (500+ lines) ⭐ MAIN DEMO GUIDE
- Purpose: Full 15-minute demo walkthrough
- Use when: Learning the demo flow
- Structure:
  * Pre-demo checklist (environment setup)
  * Part 1: Problem & Discovery (2 min)
  * Part 2: RDF Model demo (3 min)
  * Part 3: Backend methods (3 min)
  * Part 4: Two-level comparison (2 min)
  * Part 5: Architecture & next steps (2 min)
  * Q&A preparation (6 common questions with answers)
  * Backup strategy (screenshots, fallback plan)
  * Key messages and one-liners
- Commands: All copy-paste ready with expected outputs
- **Practice with this**: At least twice before interview

**DEMO_QUICK_REFERENCE.md** (200+ lines) ⭐ PRINT THIS
- Purpose: Concise cheat sheet for demo
- Use when: During the actual demo (quick lookup)
- Content:
  * Quick start (2 commands)
  * Demo commands in sequence (numbered steps)
  * Key talking points (one-liners)
  * Q&A quick answers
  * Must-show features checklist
  * Expected outputs
- **Print this**: Keep visible during demo for quick reference

**DEMO_TROUBLESHOOTING.md** (400+ lines) ⭐ EMERGENCY GUIDE
- Purpose: Fixes for common demo problems
- Use when: Something breaks during demo
- Sections:
  * Emergency fixes (30 seconds or less)
  * Common demo problems (with solutions)
  * Graceful failure recovery
  * Must-have screenshots
  * Professional responses for tech difficulties
- **Reference this**: If demo encounters issues

**DEMO_DAY_CHECKLIST.md** (370 lines) ⭐ DAY-OF GUIDE
- Purpose: Complete checklist for interview day
- Use when: Morning of interview through follow-up email
- Timeline:
  * 2 hours before: Physical setup, materials
  * 30 minutes before: Environment setup
  * 10 minutes before: Final check
  * During demo: Flow and engagement tips
  * After demo: Questions to ask, thank-you email
- **Follow this**: Step-by-step on interview day

---

### Automation & Utilities

**verify_demo.sh** (executable script) ⭐ RUN BEFORE DEMO
- Purpose: Automated environment verification
- Use when: 30 minutes before demo
- Checks:
  1. Virtuoso Docker running
  2. Python environment activated
  3. Python imports working
  4. SPARQL endpoint reachable
  5. Sample faculties in store (3 expected)
  6. Cache directory exists
  7. Test suite passing
- Exit code: 0 if all pass, 1 if any fail (with fix instructions)
- **Run this**: 30 min before demo for peace of mind

**insert_sample_faculties.py** (270 lines)
- Purpose: Populate triple store with faculty data
- Use when: Setting up demo environment
- Functions:
  * insert_faculty_entities() - Creates 3 faculties
  * link_datasets_to_faculties() - Updates dataset group_ids
  * verify_faculty_data() - Validates insertion
- **Run this**: Once during setup, or if faculties are missing

**check_data.py** (60 lines)
- Purpose: Inspect triple store contents
- Use when: Debugging data issues
- Queries: Institutions, datasets, faculties
- **Run this**: When troubleshooting data problems

**test_faculty_statistics.py** (145 lines)
- Purpose: Comprehensive backend test suite
- Use when: Validating backend implementation
- Tests:
  1. Get all faculty statistics
  2. Filter by institution_id
  3. Pagination (limit/offset)
  4. JSON serialization
  5. institution_statistics() wrapper
- **Run this**: After any backend changes, during demo

---

### Technical Documentation

**README.md** (280 lines)
- Purpose: Main prototype documentation
- Use when: Understanding project structure
- Sections:
  * Purpose and scope
  * Directory structure
  * Phase 1 details
  * Running instructions
  * Interview talking points
  * Troubleshooting
- **Read this**: For technical overview

**sample_faculties.ttl** (40 lines)
- Purpose: RDF sample data
- Use when: Understanding data model
- Entities: 3 TU Delft faculties
- Format: Turtle (TTL)
- Properties: id, group_id, faculty_name, faculty_short_name, faculty_code, institution_id
- **View this**: To see RDF structure

**statistics_faculty.sparql** (24 lines)
- Purpose: SPARQL aggregation template
- Location: `djehuty/src/djehuty/web/resources/sparql_templates/`
- Use when: Understanding query logic
- Pattern: GROUP BY with OPTIONAL clause
- **View this**: To understand SPARQL query

---

### Screenshots (Optional)

**screenshots/** directory
- Purpose: Backup visuals if demo fails
- Use when: Creating pre-captured demo evidence
- Recommended screenshots:
  1. tests_passing.png - Test suite output
  2. sparql_query.png - SPARQL query results
  3. python_output.png - Python method output
  4. git_history.png - Commit history
- **Create these**: If you want backup evidence (see DEMO_TROUBLESHOOTING.md)

---

## 🎬 Demo Preparation Workflow

### First Time (Week Before Interview)

```
Day 1-2: Implementation
├── Read PROTOTYPE_PLAN.md (understand strategy)
├── Read PHASE1_FOCUS.md (understand Phase 1)
├── Implement RDF model + backend (if not done)
└── Run tests (verify everything works)

Day 3: Demo Learning
├── Read DEMO_SCRIPT.md (learn full demo)
├── Read PROGRESS.md (understand what to showcase)
├── Practice demo flow (without time pressure)
└── Note any confusing parts

Day 4: Practice
├── Practice full demo (time yourself: 10-15 min)
├── Practice Q&A answers (in DEMO_SCRIPT.md)
├── Record yourself (optional, helps with pacing)
└── Fix any rough parts

Day 5-6: Refinement
├── Practice demo 2-3 more times
├── Create screenshots (optional, see DEMO_TROUBLESHOOTING.md)
├── Review DEMO_DAY_CHECKLIST.md
└── Prepare materials (print DEMO_QUICK_REFERENCE.md)

Day 7: Interview Day
└── Follow DEMO_DAY_CHECKLIST.md step-by-step
```

### Interview Day (Timeline)

```
2 hours before:
├── Read DEMO_DAY_CHECKLIST.md (physical setup section)
├── Gather materials (laptop, power, printed docs)
└── Mental preparation

30 minutes before:
├── Run ./prototype/verify_demo.sh
├── Fix any issues (see DEMO_TROUBLESHOOTING.md)
├── Open terminals and VS Code
└── Position windows

10 minutes before:
├── Final check (quick commands)
├── Review DEMO_QUICK_REFERENCE.md
├── Deep breath
└── Clear terminal screen

Demo time:
├── Follow DEMO_SCRIPT.md flow
├── Reference DEMO_QUICK_REFERENCE.md for commands
├── If issues → use DEMO_TROUBLESHOOTING.md
└── Stay calm and confident

After demo:
├── Q&A (answers in DEMO_SCRIPT.md)
├── Your questions for them
├── Thank them
└── Send follow-up email (template in DEMO_DAY_CHECKLIST.md)
```

---

## 🎯 Key Files by Audience

### For Interviewers (What to Share)

If they ask for documentation:
- **README.md** - Technical overview
- **PROTOTYPE_PLAN.md** - Strategy and architecture
- **PROGRESS.md** - Current status
- Git repository link
- Screenshots of working demo (if you made them)

DO NOT share:
- Demo scripts (internal prep materials)
- Troubleshooting guide (shows what could go wrong)
- Checklist (too much detail)

### For Your Preparation

Must read:
- **DEMO_SCRIPT.md** - Main guide
- **DEMO_DAY_CHECKLIST.md** - Day-of workflow

Keep visible during demo:
- **DEMO_QUICK_REFERENCE.md** - Printed on desk

Emergency reference:
- **DEMO_TROUBLESHOOTING.md** - If something breaks

---

## 📊 Document Statistics

| Document | Lines | Purpose | Audience |
|----------|-------|---------|----------|
| PROTOTYPE_PLAN.md | 1700+ | Full strategy | You + Interviewers |
| PHASE1_FOCUS.md | 400+ | Phase 1 plan | You (implementation) |
| PROGRESS.md | 300 | Status update | You + Interviewers |
| DEMO_SCRIPT.md | 500+ | Full demo walkthrough | You (preparation) |
| DEMO_QUICK_REFERENCE.md | 200+ | Essential commands | You (during demo) |
| DEMO_TROUBLESHOOTING.md | 400+ | Emergency fixes | You (backup) |
| DEMO_DAY_CHECKLIST.md | 370 | Day-of checklist | You (interview day) |
| README.md | 280 | Technical overview | You + Interviewers |
| verify_demo.sh | 100 | Automated checks | You (automated) |
| test_faculty_statistics.py | 145 | Test suite | You + Interviewers |
| insert_sample_faculties.py | 270 | Data insertion | You (setup) |
| check_data.py | 60 | Data inspection | You (debugging) |
| sample_faculties.ttl | 40 | RDF sample data | You + Interviewers |
| statistics_faculty.sparql | 24 | SPARQL template | You + Interviewers |

**Total documentation**: ~4,800 lines
**Total code**: ~620 lines (backend + tests + scripts)
**Total**: ~5,400 lines created for this prototype

---

## 🚀 Success Criteria

You're ready to demo when:

- [ ] You can explain the problem and solution in 2 minutes
- [ ] You can run the demo flow in 10-15 minutes without notes
- [ ] You can answer the 6 common Q&A questions confidently
- [ ] You know the key messages by heart
- [ ] `./prototype/verify_demo.sh` passes all checks
- [ ] You've practiced at least twice
- [ ] You have DEMO_QUICK_REFERENCE.md printed
- [ ] You know where DEMO_TROUBLESHOOTING.md is if needed
- [ ] You can gracefully handle demo failures
- [ ] You're excited to show what you've built!

---

## 💡 Pro Tips

### During Demo
1. **Speak slower than normal** - Nerves make you talk fast
2. **Pause for questions** - Engagement > perfect delivery
3. **Explain before typing** - "I'm going to query the SPARQL endpoint..." then type
4. **Show confidence** - You built this, you know it deeply
5. **If stuck, pivot** - Use screenshots or code walkthrough

### Mental Model
Think of demo as telling a story:
1. **Problem** - Users can't see faculty-level stats (Act 1)
2. **Solution** - Extension pattern using RDF (Act 2)
3. **Proof** - Working code with tests (Act 3)
4. **Future** - Next steps and full vision (Epilogue)

### Emergency Mindset
If demo breaks:
- **Don't panic** - Take a breath
- **Stay positive** - "Technical difficulties happen, let me show you the code instead"
- **Demonstrate knowledge** - Walk through code, explain architecture
- **Show preparation** - "I have comprehensive tests and documentation"
- **Remain confident** - You have working code, just demo environment issues

---

## 📧 Questions?

If you're stuck or unsure:

1. **Re-read the relevant doc** - Most answers are in existing docs
2. **Run verify_demo.sh** - Catches most environment issues
3. **Check DEMO_TROUBLESHOOTING.md** - Covers common problems
4. **Practice one more time** - Confidence comes from repetition

---

## 🎓 Final Words

You've built:
- **Working RDF model** (3 faculties in triple store)
- **Backend methods** (faculty_statistics + institution_statistics)
- **Test suite** (5/5 tests passing, 100% coverage)
- **Comprehensive documentation** (~4,800 lines)
- **Complete demo package** (scripts, checklists, troubleshooting)

This is **more than enough** for a 10-15 minute demo. You have:
- Live working code (can run during demo)
- Fallback strategies (screenshots, code walkthrough)
- Deep knowledge (can answer questions confidently)
- Professional presentation (documentation shows thoroughness)

**You're ready. Go show them what you've built!** 🚀

---

**Last updated**: Check git log for latest commit
**Status**: Phase 1 complete (80%), demo-ready
**Next action**: Follow DEMO_DAY_CHECKLIST.md on interview day
