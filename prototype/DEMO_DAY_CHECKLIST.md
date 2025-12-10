# Demo Day Checklist

**Use this checklist on the day of your interview.**

---

## 🌅 Morning of Interview (2 hours before)

### Physical Setup
- [ ] Laptop fully charged (100%)
- [ ] Power adapter in bag
- [ ] Backup laptop/tablet with screenshots ready
- [ ] USB drive with repository backup
- [ ] Phone silenced (notifications off)
- [ ] Water bottle filled
- [ ] Notebook and pen for notes

### Materials Printed
- [ ] DEMO_QUICK_REFERENCE.md (2 copies)
- [ ] PROTOTYPE_PLAN.md (1 copy, optional)
- [ ] Your resume/CV (2 copies)
- [ ] List of questions to ask them

### Digital Prep
- [ ] All browser tabs closed except documentation
- [ ] Desktop cleaned (hide personal files)
- [ ] Terminal font size readable from distance
- [ ] Color scheme high contrast (light background)
- [ ] No embarrassing shell history (clear if needed)
- [ ] Notification Center disabled
- [ ] Screen brightness at max

---

## 💻 30 Minutes Before Interview

### Environment Setup
```bash
# 1. Navigate to project
cd ~/Projects/assigment-djehuty

# 2. Activate Python environment
source djehuty-env/bin/activate

# 3. Run verification script
./prototype/verify_demo.sh

# Expected output: "✓ ALL CHECKS PASSED - Ready for demo!"
```

### If Verification Fails

**Virtuoso not running?**
```bash
cd djehuty
docker-compose up -d
sleep 15  # Wait for startup
cd ..
```

**Faculties missing?**
```bash
python prototype/insert_sample_faculties.py
```

**Tests failing?**
```bash
python prototype/test_faculty_statistics.py
# Read errors, fix if simple, otherwise use screenshots
```

### Open These Windows

1. **Terminal 1** (Main Demo)
   ```bash
   cd ~/Projects/assigment-djehuty
   source djehuty-env/bin/activate
   clear
   # Position: Left half of screen
   ```

2. **Terminal 2** (Backup Commands)
   - Have DEMO_QUICK_REFERENCE.md open here
   - Ready to copy-paste if Terminal 1 fails
   - Position: Right half of screen (minimize for now)

3. **VS Code** (Code Walkthrough)
   - Open workspace: `~/Projects/assigment-djehuty`
   - Files ready in tabs:
     * `prototype/sample_faculties.ttl`
     * `djehuty/src/djehuty/web/resources/sparql_templates/statistics_faculty.sparql`
     * `djehuty/src/djehuty/web/database.py` (scroll to line 607)
     * `prototype/test_faculty_statistics.py`
   - Font size: Zoom in (Ctrl+=) until readable
   - Minimap: Disable (View → Show Minimap)

4. **Browser** (Documentation)
   - Tab 1: `prototype/DEMO_SCRIPT.md` (GitHub or local)
   - Tab 2: `prototype/DEMO_QUICK_REFERENCE.md`
   - Tab 3: `prototype/DEMO_TROUBLESHOOTING.md`
   - Tab 4: `prototype/screenshots/` directory (if you made screenshots)
   - All other tabs closed

### Screenshots Ready? (Optional but Recommended)

Create these now if you haven't:

```bash
# 1. Tests passing
python prototype/test_faculty_statistics.py > /tmp/tests.txt 2>&1
# Screenshot this output → save as screenshots/tests_passing.png

# 2. SPARQL query
curl -X POST http://localhost:8890/sparql \
  -H "Content-Type: application/sparql-query" \
  -H "Accept: application/sparql-results+json" \
  -d "PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
      SELECT ?faculty_name ?faculty_short_name 
      WHERE { ?f a djht:Faculty ; 
                 djht:faculty_name ?faculty_name ;
                 djht:faculty_short_name ?faculty_short_name . }" | jq
# Screenshot this → save as screenshots/sparql_query.png

# 3. Python output
python -c "
import sys, json
sys.path.insert(0, 'djehuty/src')
from djehuty.web.database import SparqlInterface
db = SparqlInterface()
db.cache.storage = 'data/cache'
db.setup_sparql_endpoint()
results = db.faculty_statistics(limit=2)
print(json.dumps(results, indent=2, default=str))
"
# Screenshot this → save as screenshots/python_output.png

# 4. Git commits
git log --oneline --graph --decorate | head -10
# Screenshot this → save as screenshots/git_history.png
```

---

## ⏰ 10 Minutes Before (Final Check)

### Mental Prep
- [ ] Read your key message: "Extension not replacement, working prototype in 2 days, same pattern/finer granularity"
- [ ] Review Q&A answers (in DEMO_SCRIPT.md)
- [ ] Deep breath, you know this material cold
- [ ] Remember: Even if demo fails, you have working code + documentation

### Technical Final Check
```bash
# Quick verification (should be instant if ran 30min check)
docker-compose -f djehuty/docker-compose.yaml ps | grep sparql  # Should see "Up"
python -c "from djehuty.web.database import SparqlInterface; print('✓')"  # Should print ✓
curl -s http://localhost:8890/sparql > /dev/null && echo "✓ SPARQL OK"
```

### Position Everything
- [ ] Terminal 1 maximized, cleared, prompt ready
- [ ] VS Code behind terminal (Alt+Tab ready)
- [ ] Browser with docs minimized (easy access)
- [ ] DEMO_QUICK_REFERENCE.md printed on desk in front of you
- [ ] Water within reach (not near laptop!)

---

## 🎬 Demo Time Checklist

### Start Strong
- [ ] Introduce yourself briefly (name, background - 30 sec)
- [ ] State your agenda: "I'll show you a working prototype in 10-15 minutes, then Q&A"
- [ ] Ask: "How much time do we have?" (adjust pacing if needed)

### During Demo
- [ ] Speak clearly, slower than normal
- [ ] Explain what you're typing BEFORE you type it
- [ ] Pause after each section: "Does this make sense so far?"
- [ ] If command fails → stay calm, reference troubleshooting guide
- [ ] If complete failure → pivot to code walkthrough gracefully

### Engagement
- [ ] Make eye contact (not just staring at screen)
- [ ] Read the room (are they following? Adjust pace)
- [ ] Invite questions during demo, not just at end
- [ ] If they interrupt with questions → good sign! Engage deeply

---

## 🎯 Demo Flow (Quick Reference)

**Part 1: Context** (2 min)
```
Show: Assignment PDF, explain problem
```

**Part 2: RDF Model** (3 min)
```bash
curl -X POST http://localhost:8890/sparql ...  # Query faculties
cat prototype/sample_faculties.ttl | head -20  # Show data structure
```

**Part 3: Backend** (3 min)
```bash
python  # Enter REPL
>>> # Import and run faculty_statistics()
python prototype/test_faculty_statistics.py  # Show tests
```

**Part 4: Comparison** (2 min)
```bash
# Show institution vs faculty (hierarchy)
# Explain extension pattern
```

**Part 5: Architecture** (2 min)
```
VS Code: Show code in database.py
Explain: Next steps (API, migration, dashboard)
```

**Q&A** (3 min)
```
Reference answers in DEMO_SCRIPT.md
```

---

## ⚠️ Emergency Protocols

### If Terminal Freezes
- [ ] Have Terminal 2 ready (switch with Alt+Tab)
- [ ] Or use screenshots from browser

### If Virtuoso Crashes
- [ ] Apologize calmly: "Let me use pre-captured results..."
- [ ] Show screenshots of working demo
- [ ] Focus on code walkthrough in VS Code

### If Complete Technical Failure
- [ ] DO NOT PANIC (deep breath)
- [ ] Say: "Technical difficulties happen. Let me show you the code and documentation instead."
- [ ] Open VS Code, walk through:
  1. `statistics_faculty.sparql` - explain query
  2. `database.py` - explain methods
  3. `test_faculty_statistics.py` - explain tests
  4. Git history - show commits
  5. Documentation - show PROTOTYPE_PLAN.md
- [ ] Emphasize: "All code is working and tested, just having demo environment issues right now"

---

## 💬 Key Messages (Memorize These)

### Opening
> "I built a working prototype in 2 days that demonstrates faculty-level statistics alongside the existing institution-level statistics. It's an extension, not a replacement."

### RDF Model
> "I extended the existing InstitutionGroup pattern by reusing the group_id field. This means faculties integrate seamlessly with existing institution aggregations."

### Backend Methods
> "The faculty_statistics() method follows the exact same pattern as dataset_statistics() - same caching, same filtering, same pagination. This consistency makes the codebase maintainable."

### Hierarchy
> "We go from 4 institution groups to 47 faculty groups. Same aggregation pattern, just finer granularity. Users can see both levels depending on their needs."

### Testing
> "100% test coverage for the new methods. All 5 tests passing. I can run them live right now." (then actually run them)

### Next Steps
> "The remaining work is API endpoints, data migration scripting, and visualization dashboard. The hard part - the data model and backend - is proven and working."

---

## 🎓 Post-Demo

### After Demo Completes
- [ ] Ask: "Any questions about what I showed?"
- [ ] Ask: "Would you like me to go deeper into any part?"
- [ ] Offer to send: Git repository link, documentation

### Your Questions for Them
- [ ] "What are the biggest technical challenges the team faces?"
- [ ] "How does the team approach new feature development?"
- [ ] "What would success look like for this role in 6 months?"
- [ ] "What's the timeline for a decision on this role?"

### Thank Them
- [ ] Thank them for their time
- [ ] Express enthusiasm for the role/project
- [ ] Ask about next steps in the process
- [ ] Get contact information for follow-up

---

## 📧 Follow-Up (Same Day)

Send thank-you email within 4 hours:

**Subject**: Thank you - Senior Software Developer Interview - [Your Name]

**Body**:
```
Dear [Interviewer Names],

Thank you for taking the time to speak with me today about the Senior Software 
Developer role at 4TU.ResearchData. I enjoyed demonstrating the faculty-level 
statistics prototype and discussing the technical challenges of the repository 
platform.

[If demo worked]:
As demonstrated, the prototype shows a working extension of the institution 
statistics using faculty-level granularity. All code and documentation are 
available in the git repository.

[If demo had issues]:
Despite the technical difficulties during the live demo, the prototype is 
fully functional with comprehensive tests and documentation. I'd be happy to 
provide a screen recording or schedule a follow-up demo if that would be helpful.

Key deliverables completed:
• RDF data model extension (3 sample faculties)
• SPARQL aggregation template
• Python backend methods (faculty_statistics, institution_statistics)
• Comprehensive test suite (5/5 tests passing)
• Detailed documentation and demo scripts

I'm excited about the opportunity to contribute to the Djehuty platform and 
would welcome the chance to discuss how my experience with [mention something 
specific they discussed] could benefit the team.

Please let me know if you need any additional information.

Best regards,
[Your Name]
[Your Email]
[Your Phone]
[GitHub Profile]
```

Attach (if appropriate):
- Git repository link
- PDF of prototype documentation
- Screenshot of tests passing

---

## 🎉 You're Ready!

**Remember**:
- You've built working code in 2 days
- You have comprehensive documentation
- You know the material deeply
- Technical issues happen to everyone
- Confidence comes from preparation - you're prepared!

**Final Thought**:
Even senior developers have demos that fail. How you handle challenges matters 
more than avoiding them entirely. You have multiple backup strategies, you know 
the code, and you can articulate the architecture clearly.

**Go show them what you've built!** 🚀

---

**Checklist last updated**: Before interview
**Verification script last run**: [Run `./prototype/verify_demo.sh` and note time here]
**Screenshots captured**: Yes / No / Not doing screenshots
**Mental state**: Confident and ready! 😊
