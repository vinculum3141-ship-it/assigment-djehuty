#!/bin/bash
# Demo environment verification script
# Run this 5 minutes before your interview demo

set -e  # Exit on error

echo "═══════════════════════════════════════"
echo "  Demo Environment Verification"
echo "═══════════════════════════════════════"
echo ""

# Change to correct directory
cd "$(dirname "$0")/.."

# Check 1: Docker
echo -n "✓ Checking Virtuoso Docker... "
if docker-compose -f djehuty/docker-compose.yaml ps 2>/dev/null | grep -q "sparql.*Up"; then
    echo "RUNNING ✓"
else
    echo "NOT RUNNING ✗"
    echo ""
    echo "  Fix: cd djehuty && docker-compose up -d && cd .."
    exit 1
fi

# Check 2: Python environment
echo -n "✓ Checking Python environment... "
if [[ "$VIRTUAL_ENV" == *"djehuty-env"* ]]; then
    echo "ACTIVATED ✓"
else
    echo "NOT ACTIVATED ✗"
    echo ""
    echo "  Fix: source djehuty-env/bin/activate"
    exit 1
fi

# Check 3: Python imports
echo -n "✓ Checking Python imports... "
if python -c "import sys; sys.path.insert(0, 'djehuty/src'); from djehuty.web.database import SparqlInterface" 2>/dev/null; then
    echo "OK ✓"
else
    echo "FAILED ✗"
    echo ""
    echo "  Fix: Check Python environment and djehuty installation"
    exit 1
fi

# Check 4: SPARQL endpoint
echo -n "✓ Checking SPARQL endpoint... "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8890/sparql | grep -q "200"; then
    echo "REACHABLE ✓"
else
    echo "UNREACHABLE ✗"
    echo ""
    echo "  Fix: Check Virtuoso is running and port 8890 is open"
    exit 1
fi

# Check 5: Sample faculties in store
echo -n "✓ Checking sample faculties... "
FACULTY_COUNT=$(python -c "
import sys, os
sys.path.insert(0, 'djehuty/src')
from djehuty.web.database import SparqlInterface
db = SparqlInterface()
os.makedirs('data/cache', exist_ok=True)
db.cache.storage = 'data/cache'
db.setup_sparql_endpoint()
try:
    results = db.faculty_statistics()
    print(len(results))
except Exception as e:
    print(0)
" 2>/dev/null)

if [ "$FACULTY_COUNT" = "3" ]; then
    echo "3 FOUND ✓"
elif [ "$FACULTY_COUNT" = "0" ]; then
    echo "0 FOUND ✗"
    echo ""
    echo "  Fix: python prototype/insert_sample_faculties.py"
    exit 1
else
    echo "$FACULTY_COUNT FOUND (expected 3) ⚠"
fi

# Check 6: Cache directory
echo -n "✓ Checking cache directory... "
if [ -d "data/cache" ]; then
    echo "EXISTS ✓"
else
    echo "MISSING ✗"
    echo ""
    echo "  Fix: mkdir -p data/cache"
    exit 1
fi

# Check 7: Test suite
echo -n "✓ Running test suite... "
if python prototype/test_faculty_statistics.py 2>&1 | grep -q "✅ ALL TESTS PASSED"; then
    echo "ALL PASSING ✓"
else
    echo "SOME FAILING ✗"
    echo ""
    echo "  Fix: python prototype/test_faculty_statistics.py"
    echo "        (Review test output for details)"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════"
echo "  ✓ ALL CHECKS PASSED"
echo "  🚀 Ready for demo!"
echo "═══════════════════════════════════════"
echo ""
echo "Quick tips:"
echo "  • Have DEMO_QUICK_REFERENCE.md open"
echo "  • Increase terminal font size (Ctrl+Shift++)"
echo "  • Clear screen before starting (clear)"
echo "  • Take a deep breath 😊"
echo ""
