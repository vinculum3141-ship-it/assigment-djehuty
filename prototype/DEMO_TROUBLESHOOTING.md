# Demo Troubleshooting Guide

Quick fixes for common issues during the live demo.

---

## 🔥 Emergency Fixes (30 seconds or less)

### Issue: Virtuoso not running

**Symptom**: `curl http://localhost:8890/sparql` fails

**Fix**:
```bash
cd ~/Projects/assigment-djehuty/djehuty
docker-compose up -d
# Wait 10 seconds
docker-compose ps  # Should show sparql_1 running
```

**Say to audience**: "Let me restart the database service quickly..."

---

### Issue: Python environment not activated

**Symptom**: `ImportError: No module named 'djehuty'`

**Fix**:
```bash
source ~/Projects/assigment-djehuty/djehuty-env/bin/activate
```

**Say to audience**: "Let me activate the Python environment..."

---

### Issue: No faculties in triple store

**Symptom**: SPARQL query returns empty results

**Fix**:
```bash
python prototype/insert_sample_faculties.py
```

**Say to audience**: "Let me quickly insert the sample data..."

---

### Issue: Cache directory missing

**Symptom**: `TypeError: expected str, bytes or os.PathLike object, not NoneType`

**Fix**:
```bash
mkdir -p data/cache
```

Or in Python:
```python
db.cache.storage = 'data/cache'
```

**Say to audience**: "Let me set up the cache directory..."

---

### Issue: Tests fail

**Symptom**: Test script shows failures

**Fallback**:
> "Let me show you the code instead of running tests live..."

**Action**: Show code in editor, explain what it does, show screenshot of tests passing

---

### Issue: SPARQL query hangs

**Symptom**: curl command doesn't return

**Fix**: Ctrl+C and use backup

**Say to audience**: "Let me show you a pre-captured result instead..."

**Action**: Show screenshot or use Python method instead

---

## 🐛 Common Demo Problems

### Problem: Terminal output too small

**Fix**:
```bash
# Increase font size
Ctrl+Shift++  # or Ctrl+=

# Clear screen
clear
```

---

### Problem: JSON output not pretty

**Fix**: Use jq for formatting
```bash
# If jq not installed
sudo apt-get install jq

# Or in Python
import json
print(json.dumps(results, indent=2, default=str))
```

---

### Problem: Network connectivity issues

**Fallback**: Use local Python REPL instead of SPARQL endpoint

```python
# Skip SPARQL curl, go straight to Python
python
>>> import sys
>>> sys.path.insert(0, 'djehuty/src')
>>> from djehuty.web.database import SparqlInterface
>>> # ... continue with demo
```

---

### Problem: Forgot commands

**Solution**: Have DEMO_QUICK_REFERENCE.md printed and visible

**Say**: "Let me reference my notes quickly..."

---

## 📋 Pre-Demo Verification

Run this 5 minutes before demo:

```bash
#!/bin/bash
# Save as: prototype/verify_demo.sh

echo "=== Demo Environment Check ==="

# Check 1: Docker
echo -n "Virtuoso Docker: "
if docker-compose ps | grep -q "sparql_1.*Up"; then
    echo "✓ Running"
else
    echo "✗ NOT RUNNING - Run: docker-compose up -d"
    exit 1
fi

# Check 2: Python environment
echo -n "Python environment: "
if [[ "$VIRTUAL_ENV" == *"djehuty-env"* ]]; then
    echo "✓ Activated"
else
    echo "✗ NOT ACTIVATED - Run: source djehuty-env/bin/activate"
    exit 1
fi

# Check 3: Faculties in store
echo -n "Sample faculties: "
COUNT=$(python -c "
import sys
sys.path.insert(0, 'djehuty/src')
from djehuty.web.database import SparqlInterface
db = SparqlInterface()
db.cache.storage = 'data/cache'
db.setup_sparql_endpoint()
results = db.faculty_statistics()
print(len(results))
" 2>/dev/null)

if [ "$COUNT" = "3" ]; then
    echo "✓ 3 faculties found"
else
    echo "✗ Expected 3, found $COUNT - Run: python prototype/insert_sample_faculties.py"
    exit 1
fi

# Check 4: Tests passing
echo -n "Test suite: "
if python prototype/test_faculty_statistics.py 2>&1 | grep -q "ALL TESTS PASSED"; then
    echo "✓ All passing"
else
    echo "✗ TESTS FAILING - Debug before demo"
    exit 1
fi

echo ""
echo "=== ✓ All checks passed - Ready for demo! ==="
```

---

## 🔄 Reset Demo Environment

If demo gets corrupted, reset quickly:

```bash
# 1. Restart Virtuoso
cd djehuty
docker-compose down
docker-compose up -d

# 2. Re-insert sample data
cd ..
python prototype/insert_sample_faculties.py

# 3. Verify
python prototype/test_faculty_statistics.py
```

**Time**: ~60 seconds

---

## 🎯 Graceful Failure Recovery

### If Live Demo Completely Fails

**Stay calm and pivot**:

> "Technical difficulties happen. Let me show you what I've built through the code and documentation instead."

**Backup Presentation (No Live Demo)**:

1. **Show Code in Editor** (3 min)
   - Open `statistics_faculty.sparql`
   - Open `database.py` with `faculty_statistics()`
   - Explain the logic

2. **Show Test Results Screenshot** (1 min)
   - Pre-captured image of all tests passing
   - Proves code worked before

3. **Show SPARQL Screenshot** (1 min)
   - Pre-captured SPARQL query result
   - Proves data structure

4. **Walk Through Documentation** (3 min)
   - `PROGRESS.md` - What's done
   - `PROTOTYPE_PLAN.md` - Full strategy
   - Commit history - Detailed work

5. **Architecture Discussion** (3 min)
   - Whiteboard diagram
   - Explain extension pattern
   - Benefits and trade-offs

**Key message**:
> "Even though the live demo isn't working right now, I've built comprehensive documentation and tests that prove the prototype is functional. All the code is committed to git with detailed messages."

---

## 📸 Must-Have Screenshots

Create these BEFORE the interview:

### 1. Tests Passing
```bash
python prototype/test_faculty_statistics.py > /tmp/tests.txt 2>&1
# Screenshot the output
```

### 2. SPARQL Query Result
```bash
curl -X POST http://localhost:8890/sparql \
  -H "Content-Type: application/sparql-query" \
  -d "PREFIX djht: <https://ontologies.data.4tu.nl/djehuty/0.0.1/>
      SELECT ?faculty_name WHERE { ?f a djht:Faculty ; djht:faculty_name ?faculty_name . }" \
  | jq > /tmp/sparql.json
# Screenshot the output
```

### 3. Python Method Output
```bash
python -c "
import sys, json
sys.path.insert(0, 'djehuty/src')
from djehuty.web.database import SparqlInterface
db = SparqlInterface()
db.cache.storage = 'data/cache'
db.setup_sparql_endpoint()
results = db.faculty_statistics(limit=2)
print(json.dumps(results, indent=2, default=str))
" > /tmp/python.json
# Screenshot the output
```

### 4. Git Commit History
```bash
git log --oneline --graph --decorate | head -10
# Screenshot
```

Save these in `prototype/screenshots/` directory.

---

## 💡 Pro Tips

### Tip 1: Have Backup Terminal Ready
- Terminal 1: Live demo
- Terminal 2: Backup commands ready to paste

### Tip 2: Test Everything Twice
- Run full demo flow at least twice before interview
- Note any flaky commands

### Tip 3: Know Your Exit Points
- Each demo section should be self-contained
- Can skip to next section if one fails

### Tip 4: Time Buffer
- Plan for 10 minutes, have 15 minutes worth of material
- Can compress if running short

### Tip 5: Audience Engagement
- If demo is boring (just watching commands), explain as you type
- Ask "Does this make sense?" periodically
- Invite questions during demo, not just at end

---

## ⚡ Quick Command Reference

### Reset Terminal
```bash
reset  # or Ctrl+L for clear
cd ~/Projects/assigment-djehuty
source djehuty-env/bin/activate
```

### Check Everything
```bash
docker-compose ps && \
python -c "from djehuty.web.database import SparqlInterface; print('✓')" && \
curl -s http://localhost:8890/sparql > /dev/null && echo "✓ All good"
```

### Restart Virtuoso (if hung)
```bash
cd djehuty && docker-compose restart && cd ..
```

---

## 🆘 Contact Information

**If demo fails completely**:
- Apologize professionally
- Offer to reschedule or send recordings
- Emphasize the documentation and git history
- Remain confident - you have working code, just technical difficulties

**Professional Response**:
> "I apologize for the technical difficulties. I have working code with comprehensive tests and documentation. Would you prefer I walk through the code and documentation instead, or would you like me to send you a recording of the working demo along with the git repository?"

---

**Remember**: Even senior developers have demos that fail. How you handle failure matters more than the failure itself.

Stay calm. Have backups. Know your code.

You've got this! 🚀
