# Solution Architecture: Faculty-Level Statistics for 4TU.ResearchData

**⚠️ IMPORTANT: PARTIAL IMPLEMENTATION DISCOVERED - READ THIS FIRST**

**Version History:**
- **v1.0 (archived):** Original design (build from scratch) - [See archive/SOLUTION_ARCHITECTURE_v1.md](./archive/SOLUTION_ARCHITECTURE_v1.md)
- **v2.0 (current):** Updated December 9, 2024 after partial implementation discovery

**Critical Discovery (December 9, 2024):**

During code analysis, discovered that **institution-level statistics infrastructure is 50% implemented** in current Djehuty codebase:

- ✅ **FOUND:** `dataset_statistics(group_ids=[...])` - Filters datasets by institution (already works!)
- ✅ **FOUND:** `djht:group_id` predicate in RDF schema - Institution tracking (already exists!)
- ✅ **FOUND:** SPARQL templates with filtering support - Dynamic filters (already built!)
- ❌ **MISSING:** Aggregation layer - Need to sum results instead of returning list (4-6 hours to add)

**Impact on This Document:**

| Section | Status | Note |
|---------|--------|------|
| **Institution Sections** | ⚠️ Read with context | Infrastructure exists; design shows what to build if starting from scratch |
| **Faculty Sections** | ✅ 100% Valid | This is genuinely new work - all design is applicable |
| **Implementation Timeline** | ⚠️ Updated | 5 weeks → 2.5 weeks (50% reduction) |
| **Approach** | ⚠️ Changed | Build from scratch → Leverage existing + extend |

**How to Use This Document:**

1. **For Faculty Implementation:** Use this document as-is (faculty design is 100% valid)
2. **For Institution Understanding:** Read knowing that filtering infrastructure already exists
3. **For Discovery Details:** See [PARTIAL_IMPLEMENTATION_ANALYSIS.md](../PARTIAL_IMPLEMENTATION_ANALYSIS.md) (30 pages)
4. **For Quick Reference:** See [PHASE1_IMPACT_SUMMARY.md](../PHASE1_IMPACT_SUMMARY.md) (12 pages)
5. **For Original Context:** See [archive/SOLUTION_ARCHITECTURE_v1.md](./archive/SOLUTION_ARCHITECTURE_v1.md)

**What Changed:**
- **Timeline:** ~~5 weeks~~ → **2.5 weeks** (50% faster)
- **Effort:** ~~100 hours~~ → **50 hours** (50% reduction)
- **Institution Work:** ~~Build from scratch~~ → **Wrap existing method** (4-6 hours instead of 2 weeks)
- **Faculty Work:** **Same as designed** (this part doesn't exist, design is valid)

**Key Insight:**
The majority of this document (faculty tracking, migration, UI, testing) remains completely valid and applicable. Institution sections show what would be needed if building from scratch, but in practice we'll leverage the existing infrastructure discovered during analysis.

---

**Original Document Headers:**

**Version:** 1.0  
**Date:** December 9, 2025  
**Author:** Solution Architecture for Senior Software Developer Assignment  
**Target System:** Djehuty v25.6+ (RDF/SPARQL Repository)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Requirements Analysis](#2-requirements-analysis)
3. [Architectural Principles](#3-architectural-principles)
4. [Data Model Design](#4-data-model-design)
5. [System Components](#5-system-components)
6. [API Design](#6-api-design)
7. [User Interface Design](#7-user-interface-design)
8. [Migration Strategy](#8-migration-strategy)
9. [Implementation Phases](#9-implementation-phases)
10. [Security & Privacy Considerations](#10-security--privacy-considerations)
11. [Performance & Scalability](#11-performance--scalability)
12. [Testing Strategy](#12-testing-strategy)
13. [Risks & Mitigation](#13-risks--mitigation)
14. [Success Metrics](#14-success-metrics)

---

## 1. Executive Summary

**⚠️ NOTE:** This summary reflects the original "build from scratch" approach. For revised timeline and approach leveraging existing infrastructure, see [ROADMAP_EXECUTIVE_SUMMARY.md](./ROADMAP_EXECUTIVE_SUMMARY.md).

### 1.1 Problem Statement

4TU.ResearchData needs to generate **faculty-level statistics** for datasets deposited by researchers. Currently, the system only tracks institutional affiliation (e.g., "TU Delft") without distinguishing between faculties (e.g., "Faculty of Aerospace Engineering" vs. "Faculty of Applied Sciences").

### 1.2 Current State

- ❌ No faculty entity in RDF schema
- ❌ No faculty field in user accounts or datasets
- ❌ "Organizations" field is free-text (unusable for aggregation)
- ❌ Statistics only aggregate at institution or repository level
- ✅ InstitutionGroup hierarchy exists and is extensible
- ✅ SPARQL template system is modular
- ✅ Caching infrastructure ready

### 1.3 Proposed Solution

Extend the Djehuty RDF data model with a **Faculty entity** that sits between Institution and individual researchers. Add structured faculty selection to user registration and dataset deposit workflows. Implement SPARQL-based statistics aggregation by faculty.

### 1.4 Key Benefits

1. **Accurate attribution**: Faculty-level dataset counts and usage metrics
2. **Better insights**: Faculties can track research output and impact
3. **Multi-faculty support**: Handle datasets with authors from multiple faculties
4. **Future-proof**: Extensible to departments, research groups, etc.
5. **Backward compatible**: Existing datasets continue to work (with migration)

### 1.5 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │ Registration   │  │ Dataset Form │  │ Statistics      │ │
│  │ (Faculty Select)│  │(Faculty Meta)│  │ Dashboard       │ │
│  └────────────────┘  └──────────────┘  └─────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │ REST API
┌───────────────────────────┼─────────────────────────────────┐
│                    Application Layer                         │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │ Account        │  │ Dataset      │  │ Statistics      │ │
│  │ Management     │  │ Management   │  │ Aggregation     │ │
│  └────────────────┘  └──────────────┘  └─────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │ SPARQL Queries
┌───────────────────────────┼─────────────────────────────────┐
│                      Data Layer (RDF)                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Account ──faculty_id──→ Faculty ──institution_id──→   │ │
│  │                            ↓                            │ │
│  │  Dataset ──faculty_id──→ (aggregation point)           │ │
│  │                            ↓                            │ │
│  │  Author  ──faculty_id──→ (optional attribution)        │ │
│  └────────────────────────────────────────────────────────┘ │
│                   Virtuoso Triple Store                      │
└─────────────────────────────────────────────────────────────┘
```

### 1.6 Success Criteria

- ✅ Faculty statistics endpoint returns accurate counts
- ✅ New users can select faculty during registration
- ✅ Existing datasets migrated with ≥90% accuracy
- ✅ Statistics page shows faculty breakdown for TU Delft
- ✅ No breaking changes to existing API endpoints
- ✅ Query performance < 100ms for faculty statistics

---

## 2. Requirements Analysis

### 2.1 Functional Requirements

| ID | Requirement | Priority | Complexity |
|----|-------------|----------|------------|
| FR-1 | Store faculty affiliation for user accounts | Critical | Medium |
| FR-2 | Store faculty affiliation for datasets | Critical | Medium |
| FR-3 | Display faculty selection dropdown during registration | High | Low |
| FR-4 | Auto-populate faculty field in dataset form from account | High | Low |
| FR-5 | Allow override of faculty per dataset | Medium | Low |
| FR-6 | Aggregate dataset counts by faculty | Critical | Medium |
| FR-7 | Aggregate download/view metrics by faculty | High | Medium |
| FR-8 | Support multiple faculty attribution per dataset | Low | High |
| FR-9 | Display faculty statistics on institution dashboard | High | Medium |
| FR-10 | Export faculty statistics to CSV/JSON | Medium | Low |
| FR-11 | Migrate existing datasets to have faculty_id | Critical | High |
| FR-12 | Admin UI to manage faculty taxonomy | Medium | Medium |

### 2.2 Non-Functional Requirements

| ID | Requirement | Target | Measure |
|----|-------------|--------|---------|
| NFR-1 | Query performance | < 100ms | Response time for faculty stats |
| NFR-2 | API backward compatibility | 100% | No breaking changes |
| NFR-3 | Data migration accuracy | ≥ 90% | Correctly assigned faculty_id |
| NFR-4 | System availability during migration | ≥ 99% | Downtime |
| NFR-5 | User experience (faculty selection) | < 3 clicks | Registration flow |
| NFR-6 | Cache hit rate | ≥ 80% | Statistics queries |
| NFR-7 | Scalability | 10,000 datasets | Performance maintained |

### 2.3 Constraints

1. **Technical Constraints**:
   - Must use existing RDF/SPARQL infrastructure (Virtuoso)
   - Cannot break existing API contracts
   - Must integrate with current XML configuration system
   - Must support existing SAML2 authentication

2. **Data Constraints**:
   - 580+ existing datasets need migration
   - Organizations field has inconsistent formatting
   - Some authors lack institutional affiliation
   - Email domains don't distinguish faculties

3. **Organizational Constraints**:
   - Faculty taxonomy must be validated by institutions
   - Changes require approval from 4TU partners
   - Must align with institutional reporting needs

### 2.4 Assumptions

1. Faculty taxonomy is relatively stable (changes infrequently)
2. Users know their faculty affiliation
3. TU Delft will be the pilot institution
4. Other 4TU institutions will follow similar structure
5. Historical data migration is acceptable with some manual review

---

## 3. Architectural Principles

### 3.1 Design Principles

1. **Additive Changes Only**
   - Add new RDF predicates without removing existing ones
   - Maintain backward compatibility with existing queries
   - Use OPTIONAL clauses in SPARQL for faculty fields

2. **Separation of Concerns**
   - Faculty configuration separate from code (XML-based)
   - Statistics logic isolated in query templates
   - Migration scripts independent of production code

3. **Data Integrity**
   - Validate faculty_id against configured taxonomy
   - Prevent orphaned references (foreign key equivalent)
   - Log all data migrations for audit trail

4. **Progressive Enhancement**
   - Faculty field optional initially (gradual rollout)
   - Existing statistics continue to work
   - New statistics additive, not replacement

5. **Performance First**
   - Index faculty_id in Virtuoso
   - Cache statistics aggressively
   - Use COUNT queries for aggregation (not client-side)

### 3.2 Technology Choices

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Data Storage | RDF (Virtuoso) | Existing infrastructure, flexible schema |
| Query Language | SPARQL | Native support, powerful aggregation |
| Configuration | XML | Existing pattern, version-controllable |
| API Layer | Python (Werkzeug) | Current implementation, well-tested |
| Templates | Jinja2 | SPARQL template generation |
| Validation | Python validators | Existing validation framework |
| Migration | Python scripts | Access to RDF store, logging |

### 3.3 Patterns & Standards

1. **Repository Pattern**: Faculty data access through `SparqlInterface`
2. **Template Method**: SPARQL queries generated from Jinja2 templates
3. **Cache-Aside**: Statistics cached with invalidation on writes
4. **Factory Pattern**: Faculty entity creation from configuration
5. **Strategy Pattern**: Multiple migration strategies (auto/manual/hybrid)

---

## 4. Data Model Design

### 4.1 RDF Schema Extensions

#### 4.1.1 New Entity: Faculty

```turtle
@prefix djht: <https://ontologies.data.4tu.nl/djehuty#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# Faculty Entity Type
djht:Faculty rdf:type owl:Class ;
    rdfs:label "Faculty"@en ;
    rdfs:comment "An academic faculty within a research institution"@en .

# Faculty Properties
djht:faculty_id rdf:type owl:DatatypeProperty ;
    rdfs:label "Faculty ID"@en ;
    rdfs:domain [ owl:unionOf (djht:Account djht:Dataset djht:Author) ] ;
    rdfs:range xsd:integer ;
    rdfs:comment "Unique identifier for a faculty within an institution"@en .

djht:faculty_name rdf:type owl:DatatypeProperty ;
    rdfs:label "Faculty Name"@en ;
    rdfs:domain djht:Faculty ;
    rdfs:range xsd:string ;
    rdfs:comment "Official name of the faculty"@en .

djht:faculty_short_name rdf:type owl:DatatypeProperty ;
    rdfs:label "Faculty Short Name"@en ;
    rdfs:domain djht:Faculty ;
    rdfs:range xsd:string ;
    rdfs:comment "Abbreviated name or acronym for the faculty"@en .

djht:faculty_code rdf:type owl:DatatypeProperty ;
    rdfs:label "Faculty Code"@en ;
    rdfs:domain djht:Faculty ;
    rdfs:range xsd:string ;
    rdfs:comment "Official institutional code for the faculty"@en .

djht:faculty_url rdf:type owl:DatatypeProperty ;
    rdfs:label "Faculty URL"@en ;
    rdfs:domain djht:Faculty ;
    rdfs:range xsd:anyURI ;
    rdfs:comment "Official website of the faculty"@en .
```

#### 4.1.2 Entity Relationships

```turtle
# Faculty belongs to Institution
djht:Faculty rdfs:subClassOf [
    rdf:type owl:Restriction ;
    owl:onProperty djht:institution_id ;
    owl:cardinality 1
] .

# Account has optional Faculty
djht:Account rdfs:subClassOf [
    rdf:type owl:Restriction ;
    owl:onProperty djht:faculty_id ;
    owl:maxCardinality 1
] .

# Dataset has optional Faculty
djht:Dataset rdfs:subClassOf [
    rdf:type owl:Restriction ;
    owl:onProperty djht:faculty_id ;
    owl:maxCardinality 1
] .

# Author has optional Faculty
djht:Author rdfs:subClassOf [
    rdf:type owl:Restriction ;
    owl:onProperty djht:faculty_id ;
    owl:maxCardinality 1
] .
```

### 4.2 RDF Instance Examples

#### 4.2.1 Faculty Instance

```turtle
@prefix row: <https://data.4tu.nl/info/row/> .

row:faculty_285860001 
    rdf:type djht:Faculty ;
    djht:id "285860001"^^xsd:integer ;
    djht:faculty_name "Faculty of Aerospace Engineering"@en ;
    djht:faculty_short_name "AE"@en ;
    djht:faculty_code "AE" ;
    djht:institution_id "28586"^^xsd:integer ;
    djht:faculty_url <https://www.tudelft.nl/lr> .

row:faculty_285860002
    rdf:type djht:Faculty ;
    djht:id "285860002"^^xsd:integer ;
    djht:faculty_name "Faculty of Architecture and the Built Environment"@en ;
    djht:faculty_short_name "A+BE"@en ;
    djht:faculty_code "BK" ;
    djht:institution_id "28586"^^xsd:integer ;
    djht:faculty_url <https://www.tudelft.nl/bk> .
```

#### 4.2.2 Account with Faculty

```turtle
row:account_abc123
    rdf:type djht:Account ;
    djht:uuid "abc123-def456-ghi789" ;
    djht:email "john.doe@tudelft.nl" ;
    djht:institution_id "28586"^^xsd:integer ;
    djht:faculty_id "285860001"^^xsd:integer ;  # NEW
    djht:first_name "John" ;
    djht:last_name "Doe" .
```

#### 4.2.3 Dataset with Faculty

```turtle
row:dataset_xyz789
    rdf:type djht:Dataset ;
    djht:uuid "xyz789-abc123" ;
    djht:title "Study on Wing Aerodynamics" ;
    djht:institution_id "28586"^^xsd:integer ;
    djht:faculty_id "285860001"^^xsd:integer ;  # NEW
    djht:authors (
        row:author_001
        row:author_002
    ) ;
    djht:is_public "true"^^xsd:boolean .
```

### 4.3 Faculty Taxonomy (TU Delft Example)

```
Institution: TU Delft (ID: 28586)
├── Faculty of Aerospace Engineering (ID: 285860001)
│   ├── Code: AE / LR
│   └── URL: https://www.tudelft.nl/lr
├── Faculty of Architecture and the Built Environment (ID: 285860002)
│   ├── Code: A+BE / BK
│   └── URL: https://www.tudelft.nl/bk
├── Faculty of Applied Sciences (ID: 285860003)
│   ├── Code: AS / TNW
│   └── URL: https://www.tudelft.nl/tnw
├── Faculty of Civil Engineering and Geosciences (ID: 285860004)
│   ├── Code: CEG / CiTG
│   └── URL: https://www.tudelft.nl/citg
├── Faculty of Electrical Engineering, Mathematics and Computer Science (ID: 285860005)
│   ├── Code: EEMCS / EWI
│   └── URL: https://www.tudelft.nl/ewi
├── Faculty of Industrial Design Engineering (ID: 285860006)
│   ├── Code: IDE / IO
│   └── URL: https://www.tudelft.nl/io
├── Faculty of Mechanical Engineering (ID: 285860007)
│   ├── Code: ME / 3mE
│   └── URL: https://www.tudelft.nl/3me
├── Faculty of Technology, Policy and Management (ID: 285860008)
│   ├── Code: TPM
│   └── URL: https://www.tudelft.nl/tbm
└── Other / Unspecified (ID: 285860999)
    └── For administrative units, cross-faculty work
```

### 4.4 Database Schema Changes

#### 4.4.1 Python RDF Store Interface

**File:** `djehuty/src/djehuty/backup/database.py`

```python
def insert_faculty (self, record):
    """Procedure to insert a faculty record."""
    
    faculty_id = value_or_none (record, "id")
    if faculty_id is None:
        logging.error ("Invalid faculty record: %s", record)
        return None
    
    uri = self.record_uri ("Faculty", "id", faculty_id)
    if uri is not None:
        return uri  # Already exists
    
    uri = rdf.unique_node ("faculty")
    
    self.store.add ((uri, RDF.type, rdf.DJHT["Faculty"]))
    
    rdf.add (self.store, uri, rdf.DJHT["id"], faculty_id, XSD.integer)
    rdf.add (self.store, uri, rdf.DJHT["faculty_name"], 
             value_or (record, "name", None), XSD.string)
    rdf.add (self.store, uri, rdf.DJHT["faculty_short_name"],
             value_or (record, "short_name", None), XSD.string)
    rdf.add (self.store, uri, rdf.DJHT["faculty_code"],
             value_or (record, "code", None), XSD.string)
    rdf.add (self.store, uri, rdf.DJHT["institution_id"],
             value_or (record, "institution_id", None), XSD.integer)
    rdf.add (self.store, uri, rdf.DJHT["faculty_url"],
             value_or (record, "url", None), XSD.anyURI)
    
    return uri

def insert_account (self, record):
    """Modified to include faculty_id."""
    # ... existing code ...
    
    # ADD THIS:
    rdf.add (self.store, uri, rdf.DJHT["faculty_id"],
             value_or (record, "faculty_id", None), XSD.integer)
    
    return uri

def insert_dataset (self, record):
    """Modified to include faculty_id."""
    # ... existing code ...
    
    # ADD THIS:
    rdf.add (self.store, uri, rdf.DJHT["faculty_id"],
             value_or_none (record, "faculty_id"), XSD.integer)
    
    return uri

def insert_author (self, record):
    """Modified to include optional faculty_id."""
    # ... existing code ...
    
    # ADD THIS (optional for authors):
    rdf.add (self.store, uri, rdf.DJHT["faculty_id"],
             value_or (record, "faculty_id", None), XSD.integer)
    
    return uri
```

#### 4.4.2 Data Validation

**File:** `djehuty/src/djehuty/web/validator.py`

```python
def faculty_id (value, institution_id=None, required=False):
    """Validation procedure for the faculty_id parameter."""
    
    if value is None and not required:
        return None
    
    faculty_id = integer_value (value, "faculty_id", required=required)
    
    if faculty_id is None:
        return None
    
    # Validate faculty exists for this institution
    from djehuty.web.config import config
    if institution_id is not None:
        valid_faculties = config.get_faculties_for_institution (institution_id)
        if faculty_id not in [f["id"] for f in valid_faculties]:
            raise ValueError (f"Faculty {faculty_id} not valid for institution {institution_id}")
    
    return faculty_id
```

### 4.5 Configuration Format

#### 4.5.1 XML Configuration Extension

**File:** `djehuty/djehuty.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<djehuty>
  <groups>
    <group id="28586" name="TU Delft">
      <domain>tudelft.nl</domain>
      <parent>root</parent>
      
      <!-- NEW: Faculty definitions -->
      <faculties>
        <faculty id="285860001" code="AE">
          <name>Faculty of Aerospace Engineering</name>
          <short-name>AE</short-name>
          <url>https://www.tudelft.nl/lr</url>
        </faculty>
        
        <faculty id="285860002" code="BK">
          <name>Faculty of Architecture and the Built Environment</name>
          <short-name>A+BE</short-name>
          <url>https://www.tudelft.nl/bk</url>
        </faculty>
        
        <faculty id="285860003" code="TNW">
          <name>Faculty of Applied Sciences</name>
          <short-name>AS</short-name>
          <url>https://www.tudelft.nl/tnw</url>
        </faculty>
        
        <!-- ... more faculties ... -->
        
        <faculty id="285860999" code="OTHER">
          <name>Other / Unspecified</name>
          <short-name>Other</short-name>
        </faculty>
      </faculties>
      
      <group id="28696" name="TU Delft Students">
        <domain>student.tudelft.nl</domain>
      </group>
    </group>
    
    <!-- Other institutions ... -->
  </groups>
</djehuty>
```

#### 4.5.2 JSON Configuration Alternative

For institutions that prefer JSON:

```json
{
  "institutions": [
    {
      "id": 28586,
      "name": "TU Delft",
      "faculties": [
        {
          "id": 285860001,
          "name": "Faculty of Aerospace Engineering",
          "short_name": "AE",
          "code": "AE",
          "url": "https://www.tudelft.nl/lr"
        },
        {
          "id": 285860002,
          "name": "Faculty of Architecture and the Built Environment",
          "short_name": "A+BE",
          "code": "BK",
          "url": "https://www.tudelft.nl/bk"
        }
      ]
    }
  ]
}
```

### 4.6 Data Migration Mapping

#### 4.6.1 Organizations Field → Faculty Mapping

**Strategy:** Pattern matching with confidence scores

```python
FACULTY_PATTERNS = {
    285860001: {  # Faculty of Aerospace Engineering
        "patterns": [
            r"Faculty of Aerospace Engineering",
            r"Aerospace Engineering",
            r"\bAE\b",
            r"\bLR\b",
            r"Luchtvaart en Ruimtevaart"
        ],
        "exclude": []  # Patterns that should NOT match
    },
    285860002: {  # Faculty of Architecture
        "patterns": [
            r"Faculty of Architecture",
            r"Architecture and the Built Environment",
            r"\bA\+BE\b",
            r"\bBK\b",
            r"Bouwkunde"
        ],
        "exclude": []
    },
    # ... more faculties ...
}

def extract_faculty_from_organizations (org_text, institution_id):
    """
    Parse organizations field to extract faculty_id.
    Returns: (faculty_id, confidence_score)
    """
    if org_text is None or institution_id != 28586:
        return (None, 0.0)
    
    matches = []
    for faculty_id, config in FACULTY_PATTERNS.items():
        score = 0.0
        for pattern in config["patterns"]:
            if re.search(pattern, org_text, re.IGNORECASE):
                score += 1.0
        
        for exclude_pattern in config["exclude"]:
            if re.search(exclude_pattern, org_text, re.IGNORECASE):
                score = 0.0
                break
        
        if score > 0:
            matches.append((faculty_id, score))
    
    if not matches:
        return (None, 0.0)
    
    # Return highest scoring match
    matches.sort(key=lambda x: x[1], reverse=True)
    faculty_id, score = matches[0]
    
    # Normalize confidence (0-1 scale)
    confidence = min(score / 3.0, 1.0)
    
    return (faculty_id, confidence)
```

---

## 5. System Components

### 5.1 Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Presentation Layer                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐│
│  │ Registration │  │ Dataset Form │  │ Statistics Dashboard   ││
│  │   UI         │  │      UI      │  │        UI              ││
│  │              │  │              │  │                        ││
│  │ - Faculty    │  │ - Faculty    │  │ - Faculty filter       ││
│  │   Dropdown   │  │   Override   │  │ - Charts/tables        ││
│  └──────────────┘  └──────────────┘  └────────────────────────┘│
└────────────┬────────────────┬────────────────────┬──────────────┘
             │ HTTP REST API  │                    │
┌────────────┴────────────────┴────────────────────┴──────────────┐
│                     Application Layer                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Faculty Management Service                   │  │
│  │  - get_faculties_for_institution()                        │  │
│  │  - validate_faculty_id()                                  │  │
│  │  - load_faculty_taxonomy()                                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │               Statistics Service                          │  │
│  │  - faculty_statistics(institution_id, faculty_id)         │  │
│  │  - faculty_dataset_counts()                               │  │
│  │  - faculty_usage_metrics()                                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │               Migration Service                           │  │
│  │  - parse_organizations_field()                            │  │
│  │  - bulk_assign_faculty_ids()                              │  │
│  │  - generate_migration_report()                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────┬────────────────────────────────────────────────────┘
             │ SPARQL Interface
┌────────────┴─────────────────────────────────────────────────────┐
│                       Data Access Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              SparqlInterface (Extended)                   │  │
│  │                                                            │  │
│  │  Queries:                    Mutations:                   │  │
│  │  - faculties()               - insert_faculty()           │  │
│  │  - faculty_by_id()           - update_account_faculty()   │  │
│  │  - faculty_statistics()      - update_dataset_faculty()   │  │
│  │  - datasets_by_faculty()     - delete_faculty()           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              SPARQL Templates (Jinja2)                    │  │
│  │                                                            │  │
│  │  - faculties.sparql                                       │  │
│  │  - faculty_by_id.sparql                                   │  │
│  │  - statistics_faculty.sparql                              │  │
│  │  - datasets_by_faculty.sparql                             │  │
│  │  - update_faculty.sparql                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────┬─────────────────────────────────────────────────────┘
             │ SPARQL Protocol
┌────────────┴─────────────────────────────────────────────────────┐
│                      Storage Layer                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Virtuoso Triple Store                        │  │
│  │                                                            │  │
│  │  Graph: <https://data.4tu.nl/graph/state>                │  │
│  │                                                            │  │
│  │  ┌────────┐  ┌─────────┐  ┌────────┐  ┌────────────┐    │  │
│  │  │Account │  │ Faculty │  │Dataset │  │ Statistics │    │  │
│  │  │Triples │  │ Triples │  │Triples │  │   Cache    │    │  │
│  │  └────────┘  └─────────┘  └────────┘  └────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Component Details

#### 5.2.1 Faculty Management Service

**Purpose:** Centralized faculty taxonomy management

**Responsibilities:**
- Load faculty configuration from XML/JSON
- Validate faculty_id against institution
- Provide faculty list for dropdowns
- Cache faculty taxonomy in memory

**Interface:**

```python
class FacultyManager:
    """Service for managing faculty taxonomy."""
    
    def __init__(self, config_file):
        self.faculties = {}  # institution_id -> [faculty objects]
        self.load_taxonomy(config_file)
    
    def load_taxonomy(self, config_file):
        """Load faculty definitions from XML config."""
        pass
    
    def get_faculties_for_institution(self, institution_id):
        """Return list of faculties for an institution."""
        return self.faculties.get(institution_id, [])
    
    def get_faculty_by_id(self, faculty_id):
        """Return faculty object by ID."""
        pass
    
    def validate_faculty_id(self, faculty_id, institution_id):
        """Check if faculty belongs to institution."""
        pass
    
    def get_faculty_name(self, faculty_id):
        """Get display name for faculty."""
        pass
```

**Configuration Loading:**

```python
def load_taxonomy(self, config_file):
    """Parse XML and build faculty taxonomy."""
    import xml.etree.ElementTree as ET
    
    tree = ET.parse(config_file)
    root = tree.getroot()
    
    for group in root.findall(".//group"):
        institution_id = int(group.get("id"))
        faculties_elem = group.find("faculties")
        
        if faculties_elem is None:
            continue
        
        self.faculties[institution_id] = []
        
        for faculty_elem in faculties_elem.findall("faculty"):
            faculty = {
                "id": int(faculty_elem.get("id")),
                "code": faculty_elem.get("code"),
                "name": faculty_elem.find("name").text,
                "short_name": faculty_elem.find("short-name").text,
                "url": faculty_elem.find("url").text if faculty_elem.find("url") is not None else None,
                "institution_id": institution_id
            }
            self.faculties[institution_id].append(faculty)
    
    logging.info("Loaded %d institutions with faculty data", 
                 len(self.faculties))
```

#### 5.2.2 Statistics Service

**Purpose:** Aggregate faculty-level statistics

**Responsibilities:**
- Query RDF store for faculty metrics
- Cache results for performance
- Invalidate cache on data changes
- Format results for API responses

**Interface:**

```python
class FacultyStatisticsService:
    """Service for faculty-level statistics."""
    
    def __init__(self, db):
        self.db = db  # SparqlInterface instance
        self.cache_ttl = 3600  # 1 hour
    
    def get_faculty_statistics(self, institution_id=None, 
                                     faculty_id=None,
                                     start_date=None,
                                     end_date=None):
        """
        Get aggregated statistics by faculty.
        
        Returns:
        [
            {
                "faculty_id": 285860001,
                "faculty_name": "Faculty of Aerospace Engineering",
                "datasets": 42,
                "total_views": 15000,
                "total_downloads": 3500,
                "total_cites": 120,
                "total_shares": 45
            },
            ...
        ]
        """
        pass
    
    def get_faculty_dataset_list(self, faculty_id, limit=10, offset=0):
        """Get list of datasets for a faculty."""
        pass
    
    def get_faculty_top_datasets(self, faculty_id, metric="downloads", limit=10):
        """Get top N datasets by metric for a faculty."""
        pass
    
    def get_faculty_timeline(self, faculty_id, granularity="month"):
        """Get dataset publication timeline for a faculty."""
        pass
```

**SPARQL Query Example:**

```python
def get_faculty_statistics(self, institution_id=None, faculty_id=None):
    """Execute SPARQL query for faculty statistics."""
    
    query = self.db.__query_from_template("statistics_faculty", {
        "institution_id": institution_id,
        "faculty_id": faculty_id
    })
    
    cache_key = f"faculty_stats_{institution_id}_{faculty_id}"
    results = self.db.__run_query(query, cache_key, "faculty_statistics")
    
    # Enrich with faculty names
    for row in results:
        faculty = faculty_manager.get_faculty_by_id(row["faculty_id"])
        if faculty:
            row["faculty_name"] = faculty["name"]
            row["faculty_short_name"] = faculty["short_name"]
    
    return results
```

#### 5.2.3 Migration Service

**Purpose:** Migrate existing datasets to have faculty_id

**Responsibilities:**
- Parse Organizations field
- Calculate confidence scores
- Bulk update RDF triples
- Generate migration reports
- Handle manual overrides

**Interface:**

```python
class FacultyMigrationService:
    """Service for migrating existing datasets to faculty taxonomy."""
    
    def __init__(self, db, faculty_manager):
        self.db = db
        self.faculty_manager = faculty_manager
        self.migration_log = []
    
    def parse_organizations_field(self, org_text, institution_id):
        """
        Extract faculty_id from organizations text.
        
        Returns: (faculty_id, confidence_score)
        """
        pass
    
    def migrate_dataset(self, dataset_uuid, faculty_id, confidence=1.0):
        """Assign faculty_id to a single dataset."""
        pass
    
    def bulk_migrate(self, institution_id, min_confidence=0.7, 
                     dry_run=True):
        """
        Migrate all datasets for an institution.
        
        Args:
            institution_id: Institution to migrate
            min_confidence: Minimum confidence score to auto-assign
            dry_run: If True, only report, don't update
        
        Returns:
            {
                "total": 580,
                "auto_assigned": 450,
                "manual_review": 130,
                "failed": 0
            }
        """
        pass
    
    def generate_migration_report(self, results):
        """Create CSV report of migration results."""
        pass
    
    def export_manual_review_cases(self, institution_id):
        """
        Export datasets needing manual review.
        
        Returns CSV with:
        - dataset_uuid
        - title
        - organizations_field
        - suggested_faculty_id
        - confidence_score
        """
        pass
```

**Migration Workflow:**

```python
def bulk_migrate(self, institution_id, min_confidence=0.7, dry_run=True):
    """Bulk migration implementation."""
    
    # Get all datasets for institution
    datasets = self.db.datasets(
        institution_id=institution_id,
        is_published=True,
        limit=None
    )
    
    stats = {
        "total": len(datasets),
        "auto_assigned": 0,
        "manual_review": 0,
        "failed": 0
    }
    
    manual_review_cases = []
    
    for dataset in datasets:
        org_text = dataset.get("organizations")
        
        if not org_text:
            stats["manual_review"] += 1
            manual_review_cases.append({
                "uuid": dataset["uuid"],
                "title": dataset["title"],
                "reason": "No organizations field"
            })
            continue
        
        faculty_id, confidence = self.parse_organizations_field(
            org_text, institution_id
        )
        
        if faculty_id and confidence >= min_confidence:
            if not dry_run:
                self.migrate_dataset(dataset["uuid"], faculty_id, confidence)
            stats["auto_assigned"] += 1
            
            self.migration_log.append({
                "dataset_uuid": dataset["uuid"],
                "faculty_id": faculty_id,
                "confidence": confidence,
                "status": "auto_assigned" if not dry_run else "dry_run"
            })
        else:
            stats["manual_review"] += 1
            manual_review_cases.append({
                "uuid": dataset["uuid"],
                "title": dataset["title"],
                "organizations": org_text,
                "suggested_faculty": faculty_id,
                "confidence": confidence,
                "reason": "Low confidence" if faculty_id else "No match"
            })
    
    # Save manual review cases to CSV
    if manual_review_cases:
        self.export_manual_review_cases_to_csv(manual_review_cases)
    
    return stats, manual_review_cases
```

### 5.3 SPARQL Query Templates

#### 5.3.1 faculties.sparql

**Purpose:** List all faculties for an institution

```sparql
{% extends "prefixes.sparql" %}
{% block query %}
SELECT DISTINCT ?faculty_id ?faculty_name ?faculty_short_name 
                ?faculty_code ?faculty_url ?institution_id
WHERE {
  GRAPH <{{state_graph}}> {
    ?faculty        rdf:type                djht:Faculty .
    ?faculty        djht:id                 ?faculty_id .
    ?faculty        djht:faculty_name       ?faculty_name .
    
    {%- if institution_id is not none %}
    ?faculty        djht:institution_id     {{institution_id}} .
    {%- endif %}
    
    OPTIONAL { ?faculty djht:faculty_short_name ?faculty_short_name . }
    OPTIONAL { ?faculty djht:faculty_code       ?faculty_code . }
    OPTIONAL { ?faculty djht:faculty_url        ?faculty_url . }
    OPTIONAL { ?faculty djht:institution_id     ?institution_id . }
  }
}
ORDER BY ?faculty_name
{% endblock %}
```

#### 5.3.2 statistics_faculty.sparql

**Purpose:** Aggregate statistics by faculty

```sparql
{% extends "prefixes.sparql" %}
{% block query %}
SELECT ?faculty_id 
       (COUNT(DISTINCT ?container) AS ?datasets)
       (SUM(?total_views) AS ?total_views)
       (SUM(?total_downloads) AS ?total_downloads)
       (SUM(?total_cites) AS ?total_cites)
       (SUM(?total_shares) AS ?total_shares)
WHERE {
  GRAPH <{{state_graph}}> {
    ?container      rdf:type                      djht:DatasetContainer ;
                    djht:latest_published_version ?dataset .
    
    ?dataset        rdf:type                      djht:Dataset ;
                    djht:is_public                "true"^^xsd:boolean ;
                    djht:faculty_id               ?faculty_id .
    
    {%- if institution_id is not none %}
    ?dataset        djht:institution_id           {{institution_id}} .
    {%- endif %}
    
    {%- if faculty_id is not none %}
    FILTER (?faculty_id = {{faculty_id}})
    {%- endif %}
    
    {%- if start_date is not none %}
    ?dataset        djht:published_date           ?pub_date .
    FILTER (?pub_date >= "{{start_date}}"^^xsd:dateTime)
    {%- endif %}
    
    {%- if end_date is not none %}
    ?dataset        djht:published_date           ?pub_date .
    FILTER (?pub_date <= "{{end_date}}"^^xsd:dateTime)
    {%- endif %}
    
    OPTIONAL { ?container djht:total_views      ?total_views . }
    OPTIONAL { ?container djht:total_downloads  ?total_downloads . }
    OPTIONAL { ?container djht:total_cites      ?total_cites . }
    OPTIONAL { ?container djht:total_shares     ?total_shares . }
  }
}
GROUP BY ?faculty_id
ORDER BY DESC(?datasets)
{% endblock %}
```

#### 5.3.3 datasets_by_faculty.sparql

**Purpose:** List datasets for a specific faculty

```sparql
{% extends "prefixes.sparql" %}
{% block query %}
SELECT DISTINCT ?uuid ?dataset_id ?title ?doi ?published_date 
                ?total_views ?total_downloads ?faculty_id
WHERE {
  GRAPH <{{state_graph}}> {
    ?container      rdf:type                      djht:DatasetContainer ;
                    djht:dataset_id               ?dataset_id ;
                    djht:latest_published_version ?dataset .
    
    ?dataset        rdf:type                      djht:Dataset ;
                    djht:is_public                "true"^^xsd:boolean ;
                    djht:faculty_id               {{faculty_id}} ;
                    djht:title                    ?title .
    
    BIND(STRAFTER(STR(?container), "container:") AS ?uuid)
    
    OPTIONAL { ?dataset   djht:doi               ?doi . }
    OPTIONAL { ?dataset   djht:published_date    ?published_date . }
    OPTIONAL { ?container djht:total_views       ?total_views . }
    OPTIONAL { ?container djht:total_downloads   ?total_downloads . }
  }
}
ORDER BY DESC(?published_date)
LIMIT {{limit}}
OFFSET {{offset}}
{% endblock %}
```

#### 5.3.4 update_account_faculty.sparql

**Purpose:** Update faculty_id for an account

```sparql
{% extends "prefixes.sparql" %}
{% block query %}
DELETE {
  GRAPH <{{state_graph}}> {
    ?account djht:faculty_id ?old_faculty_id .
  }
}
INSERT {
  GRAPH <{{state_graph}}> {
    ?account djht:faculty_id {{faculty_id}} .
  }
}
WHERE {
  GRAPH <{{state_graph}}> {
    ?account    rdf:type    djht:Account ;
                djht:uuid   "{{account_uuid}}" .
    OPTIONAL { ?account djht:faculty_id ?old_faculty_id . }
  }
}
{% endblock %}
```

---

## 6. API Design

### 6.1 REST API Endpoints

#### 6.1.1 Faculty Endpoints

**GET /v2/institutions/{institution_id}/faculties**

List all faculties for an institution.

```http
GET /v2/institutions/28586/faculties HTTP/1.1
Host: data.4tu.nl
Accept: application/json

Response 200 OK:
{
  "faculties": [
    {
      "id": 285860001,
      "name": "Faculty of Aerospace Engineering",
      "short_name": "AE",
      "code": "AE",
      "url": "https://www.tudelft.nl/lr",
      "institution_id": 28586
    },
    {
      "id": 285860002,
      "name": "Faculty of Architecture and the Built Environment",
      "short_name": "A+BE",
      "code": "BK",
      "url": "https://www.tudelft.nl/bk",
      "institution_id": 28586
    }
  ]
}
```

**GET /v2/faculties/{faculty_id}**

Get details for a specific faculty.

```http
GET /v2/faculties/285860001 HTTP/1.1
Host: data.4tu.nl
Accept: application/json

Response 200 OK:
{
  "id": 285860001,
  "name": "Faculty of Aerospace Engineering",
  "short_name": "AE",
  "code": "AE",
  "url": "https://www.tudelft.nl/lr",
  "institution_id": 28586,
  "institution_name": "TU Delft"
}
```

#### 6.1.2 Statistics Endpoints

**GET /v2/statistics/faculties**

Get statistics aggregated by faculty.

```http
GET /v2/statistics/faculties?institution=28586 HTTP/1.1
Host: data.4tu.nl
Accept: application/json

Response 200 OK:
{
  "statistics": [
    {
      "faculty_id": 285860001,
      "faculty_name": "Faculty of Aerospace Engineering",
      "datasets": 42,
      "total_views": 15000,
      "total_downloads": 3500,
      "total_cites": 120,
      "total_shares": 45
    },
    {
      "faculty_id": 285860004,
      "faculty_name": "Faculty of Civil Engineering and Geosciences",
      "datasets": 38,
      "total_views": 12000,
      "total_downloads": 2800,
      "total_cites": 95,
      "total_shares": 32
    }
  ],
  "total_datasets": 580,
  "generated_at": "2025-12-09T10:30:00Z"
}
```

**Query Parameters:**
- `institution` (integer, required): Institution ID
- `faculty` (integer, optional): Filter by specific faculty
- `start_date` (ISO 8601, optional): Filter by publication date
- `end_date` (ISO 8601, optional): Filter by publication date
- `format` (string, optional): Response format (json, csv)

**GET /v2/statistics/faculties/{faculty_id}/datasets**

Get top datasets for a faculty.

```http
GET /v2/statistics/faculties/285860001/datasets?metric=downloads&limit=10 HTTP/1.1
Host: data.4tu.nl
Accept: application/json

Response 200 OK:
{
  "faculty_id": 285860001,
  "faculty_name": "Faculty of Aerospace Engineering",
  "datasets": [
    {
      "uuid": "abc123-def456",
      "dataset_id": 12345,
      "title": "Study on Wing Aerodynamics",
      "doi": "10.4121/12345678",
      "published_date": "2024-03-15T00:00:00Z",
      "total_views": 5000,
      "total_downloads": 1200,
      "total_cites": 45
    }
  ],
  "total": 42
}
```

**Query Parameters:**
- `metric` (string): Ranking metric (downloads, views, cites, shares)
- `limit` (integer): Number of results (default: 10, max: 100)
- `offset` (integer): Pagination offset
- `order` (string): Sort order (asc, desc)

#### 6.1.3 Account Endpoints (Extended)

**PATCH /v2/account**

Update account faculty affiliation.

```http
PATCH /v2/account HTTP/1.1
Host: data.4tu.nl
Authorization: Bearer {token}
Content-Type: application/json

{
  "faculty_id": 285860001
}

Response 200 OK:
{
  "uuid": "user-uuid-123",
  "email": "john.doe@tudelft.nl",
  "institution_id": 28586,
  "faculty_id": 285860001,
  "faculty_name": "Faculty of Aerospace Engineering"
}
```

**GET /v2/account**

Get account details (includes faculty).

```http
GET /v2/account HTTP/1.1
Host: data.4tu.nl
Authorization: Bearer {token}

Response 200 OK:
{
  "uuid": "user-uuid-123",
  "email": "john.doe@tudelft.nl",
  "first_name": "John",
  "last_name": "Doe",
  "institution_id": 28586,
  "institution_name": "TU Delft",
  "faculty_id": 285860001,
  "faculty_name": "Faculty of Aerospace Engineering"
}
```

#### 6.1.4 Dataset Endpoints (Extended)

**POST /v2/account/datasets**

Create dataset with faculty (backward compatible).

```http
POST /v2/account/datasets HTTP/1.1
Host: data.4tu.nl
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "New Dataset",
  "description": "Dataset description",
  "faculty_id": 285860001,  // NEW - optional
  // ... other fields ...
}

Response 201 Created:
{
  "uuid": "dataset-uuid-456",
  "title": "New Dataset",
  "institution_id": 28586,
  "faculty_id": 285860001,
  // ... other fields ...
}
```

**PATCH /v2/account/datasets/{uuid}**

Update dataset faculty.

```http
PATCH /v2/account/datasets/dataset-uuid-456 HTTP/1.1
Host: data.4tu.nl
Authorization: Bearer {token}
Content-Type: application/json

{
  "faculty_id": 285860002
}

Response 200 OK:
{
  "uuid": "dataset-uuid-456",
  "faculty_id": 285860002,
  "faculty_name": "Faculty of Architecture and the Built Environment"
}
```

### 6.2 API Implementation

#### 6.2.1 Python Route Handlers

**File:** `djehuty/src/djehuty/web/wsgi.py`

```python
# Faculty listing endpoint
@self.app.route("/v2/institutions/<int:institution_id>/faculties", methods=["GET"])
def api_faculties_list (self, institution_id):
    """List all faculties for an institution."""
    
    try:
        faculties = self.faculty_manager.get_faculties_for_institution(institution_id)
        return self.response(json.dumps({"faculties": faculties}))
    
    except Exception as error:
        logging.error("Failed to retrieve faculties: %s", error)
        return self.error_500("faculties", "list", str(error))

# Faculty statistics endpoint
@self.app.route("/v2/statistics/faculties", methods=["GET"])
def api_faculty_statistics (self):
    """Get statistics aggregated by faculty."""
    
    handler = self.default_error_handling (
        self.__faculty_statistics, "faculties", "statistics"
    )
    return handler()

def __faculty_statistics (self):
    """Internal handler for faculty statistics."""
    
    institution_id = validator.integer_value(request.args, "institution", required=True)
    faculty_id = validator.integer_value(request.args, "faculty", required=False)
    start_date = validator.date_value(request.args, "start_date", required=False)
    end_date = validator.date_value(request.args, "end_date", required=False)
    format_type = validator.string_value(request.args, "format", required=False) or "json"
    
    # Get statistics from service
    stats = self.statistics_service.get_faculty_statistics(
        institution_id=institution_id,
        faculty_id=faculty_id,
        start_date=start_date,
        end_date=end_date
    )
    
    if format_type == "csv":
        return self.response_csv(stats, "faculty_statistics.csv")
    else:
        return self.response(json.dumps({
            "statistics": stats,
            "total_datasets": sum(s["datasets"] for s in stats),
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }))

# Faculty datasets endpoint
@self.app.route("/v2/statistics/faculties/<int:faculty_id>/datasets", methods=["GET"])
def api_faculty_datasets (self, faculty_id):
    """Get datasets for a specific faculty."""
    
    metric = validator.string_value(request.args, "metric") or "downloads"
    limit = validator.integer_value(request.args, "limit") or 10
    offset = validator.integer_value(request.args, "offset") or 0
    
    datasets = self.statistics_service.get_faculty_dataset_list(
        faculty_id=faculty_id,
        metric=metric,
        limit=min(limit, 100),
        offset=offset
    )
    
    faculty = self.faculty_manager.get_faculty_by_id(faculty_id)
    
    return self.response(json.dumps({
        "faculty_id": faculty_id,
        "faculty_name": faculty["name"] if faculty else None,
        "datasets": datasets,
        "total": len(datasets)
    }))

# Update account faculty
@self.app.route("/v2/account", methods=["PATCH"])
@login_required
def api_account_update (self):
    """Update account details including faculty."""
    
    handler = self.default_error_handling(
        self.__account_update, "account", "update", output_json
    )
    return handler(account_uuid=self.account_uuid)

def __account_update (self, account_uuid):
    """Internal handler for account update."""
    
    record = request.get_json()
    
    # Validate faculty_id if provided
    if "faculty_id" in record:
        account = self.db.accounts(account_uuid=account_uuid, limit=1)[0]
        faculty_id = validator.faculty_id(
            record["faculty_id"],
            institution_id=account["institution_id"],
            required=False
        )
        
        if faculty_id is not None:
            success = self.db.update_account_faculty(account_uuid, faculty_id)
            if not success:
                return self.error_500("account", "update", "Failed to update faculty")
    
    # Return updated account
    account = self.db.accounts(account_uuid=account_uuid, limit=1)[0]
    return formatter.format_account_details_record(account)
```

#### 6.2.2 Database Layer Methods

**File:** `djehuty/src/djehuty/web/database.py`

```python
def faculties (self, institution_id=None, faculty_id=None):
    """Retrieve faculty records."""
    
    query = self.__query_from_template("faculties", {
        "institution_id": institution_id,
        "faculty_id": faculty_id
    })
    
    cache_key = f"faculties_{institution_id}_{faculty_id}"
    return self.__run_query(query, cache_key, "faculties")

def faculty_statistics (self, institution_id=None, faculty_id=None,
                              start_date=None, end_date=None):
    """Retrieve faculty-level statistics."""
    
    query = self.__query_from_template("statistics_faculty", {
        "institution_id": institution_id,
        "faculty_id": faculty_id,
        "start_date": start_date,
        "end_date": end_date
    })
    
    cache_key = f"faculty_stats_{institution_id}_{faculty_id}_{start_date}_{end_date}"
    return self.__run_query(query, cache_key, "faculty_statistics")

def datasets_by_faculty (self, faculty_id, limit=10, offset=0,
                               metric="downloads", order="desc"):
    """Retrieve datasets for a specific faculty."""
    
    query = self.__query_from_template("datasets_by_faculty", {
        "faculty_id": faculty_id,
        "limit": limit,
        "offset": offset
    })
    
    query += rdf.sparql_suffix(metric, order, limit, offset)
    
    return self.__run_query(query)

def update_account_faculty (self, account_uuid, faculty_id):
    """Update faculty_id for an account."""
    
    query = self.__query_from_template("update_account_faculty", {
        "account_uuid": account_uuid,
        "faculty_id": faculty_id
    })
    
    # Invalidate cache
    self.cache.invalidate_by_prefix(f"accounts_{account_uuid}")
    self.cache.invalidate_by_prefix("faculty_statistics")
    
    return self.__run_logged_query(query)

def update_dataset_faculty (self, dataset_uuid, faculty_id):
    """Update faculty_id for a dataset."""
    
    query = self.__query_from_template("update_dataset_faculty", {
        "dataset_uuid": dataset_uuid,
        "faculty_id": faculty_id
    })
    
    # Invalidate cache
    self.cache.invalidate_by_prefix(f"datasets_{dataset_uuid}")
    self.cache.invalidate_by_prefix("faculty_statistics")
    
    return self.__run_logged_query(query)
```

### 6.3 Response Formats

#### 6.3.1 JSON Format (Default)

Standard JSON responses with consistent structure:

```json
{
  "statistics": [...],
  "metadata": {
    "generated_at": "2025-12-09T10:30:00Z",
    "cache_hit": true,
    "query_time_ms": 45
  }
}
```

#### 6.3.2 CSV Format

For data export and reporting:

```csv
faculty_id,faculty_name,datasets,total_views,total_downloads,total_cites,total_shares
285860001,"Faculty of Aerospace Engineering",42,15000,3500,120,45
285860002,"Faculty of Architecture and the Built Environment",38,12000,2800,95,32
```

**Implementation:**

```python
def response_csv (self, data, filename):
    """Generate CSV response from statistics data."""
    
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    
    response = self.response(output.getvalue())
    response.headers["Content-Type"] = "text/csv"
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    
    return response
```

---

## 7. User Interface Design

### 7.1 Faculty Selection in Registration

**Location:** Account registration/profile setup page

**Design:**

```
┌──────────────────────────────────────────────────────────┐
│  Complete Your Profile                                   │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Email: john.doe@tudelft.nl ✓                           │
│  Institution: TU Delft (auto-detected)                   │
│                                                           │
│  Faculty *                                                │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Faculty of Aerospace Engineering              ▼   │  │
│  └────────────────────────────────────────────────────┘  │
│    ↓ Dropdown options:                                   │
│    - Faculty of Aerospace Engineering                    │
│    - Faculty of Architecture and the Built Environment   │
│    - Faculty of Applied Sciences                         │
│    - Faculty of Civil Engineering and Geosciences        │
│    - ...                                                  │
│    - Other / Unspecified                                 │
│                                                           │
│  ℹ️ Your faculty helps us provide relevant statistics    │
│     and can be changed later in your profile settings.   │
│                                                           │
│  [ Cancel ]                          [ Save & Continue ] │
└──────────────────────────────────────────────────────────┘
```

**JavaScript Implementation:**

```javascript
// Auto-load faculties based on detected institution
function loadFaculties(institutionId) {
    fetch(`/v2/institutions/${institutionId}/faculties`)
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('faculty-select');
            select.innerHTML = '<option value="">-- Select Faculty --</option>';
            
            data.faculties.forEach(faculty => {
                const option = document.createElement('option');
                option.value = faculty.id;
                option.textContent = faculty.name;
                select.appendChild(option);
            });
            
            // Add "Other" option
            const otherOption = document.createElement('option');
            otherOption.value = 999;
            otherOption.textContent = 'Other / Unspecified';
            select.appendChild(otherOption);
        });
}

// Validate on submit
function validateProfileForm() {
    const facultyId = document.getElementById('faculty-select').value;
    if (!facultyId) {
        alert('Please select your faculty');
        return false;
    }
    return true;
}
```

### 7.2 Faculty Field in Dataset Form

**Location:** Dataset deposit/edit form

**Design:**

```
┌──────────────────────────────────────────────────────────┐
│  Dataset Metadata                                        │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Title *                                                  │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Study on Wing Aerodynamics                        │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  Description *                                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │ This dataset contains...                          │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  Faculty                                                  │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Faculty of Aerospace Engineering (from profile) ▼ │  │
│  └────────────────────────────────────────────────────┘  │
│  ☐ This dataset involves multiple faculties              │
│                                                           │
│  ℹ️ Faculty is auto-filled from your profile. Change if  │
│     this dataset belongs to a different faculty.         │
│                                                           │
│  [ Save as Draft ]                           [ Publish ] │
└──────────────────────────────────────────────────────────┘
```

**Auto-fill Logic:**

```javascript
// Pre-fill faculty from user's account
function initializeDatasetForm() {
    fetch('/v2/account')
        .then(response => response.json())
        .then(account => {
            if (account.faculty_id) {
                document.getElementById('faculty-select').value = account.faculty_id;
            }
        });
}

// Allow override
document.getElementById('faculty-select').addEventListener('change', function() {
    const selectedFacultyId = this.value;
    // Mark as manually overridden
    document.getElementById('faculty-override-flag').value = 'true';
});
```

### 7.3 Faculty Statistics Dashboard

**Location:** Institution dashboard / statistics page

**Design:**

```
┌──────────────────────────────────────────────────────────────┐
│  TU Delft - Research Data Statistics                         │
├──────────────────────────────────────────────────────────────┤
│  View by: [ Institution ] [ Faculty ▼ ] [ Category ]         │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Faculty Statistics (2025)                             │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │  Faculty                        │ Datasets │ Downloads │  │
│  ├─────────────────────────────────┼──────────┼───────────┤  │
│  │  Aerospace Engineering          │    42    │   3,500   │  │
│  │  Civil Eng. and Geosciences     │    38    │   2,800   │  │
│  │  Applied Sciences               │    35    │   2,100   │  │
│  │  EEMCS                          │    32    │   1,900   │  │
│  │  Architecture                   │    28    │   1,500   │  │
│  │  Other faculties...             │   ...    │   ...     │  │
│  ├─────────────────────────────────┼──────────┼───────────┤  │
│  │  Total                          │   580    │  28,500   │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Datasets by Faculty (Chart)                           │  │
│  │                                                         │  │
│  │  █████████████████████ Aerospace Eng. (42)            │  │
│  │  ██████████████████ Civil Eng. (38)                   │  │
│  │  █████████████████ Applied Sciences (35)              │  │
│  │  ████████████████ EEMCS (32)                          │  │
│  │  ██████████████ Architecture (28)                     │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  [ Export CSV ] [ Export JSON ] [ Print Report ]              │
└──────────────────────────────────────────────────────────────┘
```

**Chart.js Implementation:**

```javascript
// Fetch faculty statistics and render chart
fetch('/v2/statistics/faculties?institution=28586')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('faculty-chart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.statistics.map(s => s.faculty_short_name || s.faculty_name),
                datasets: [{
                    label: 'Datasets',
                    data: data.statistics.map(s => s.datasets),
                    backgroundColor: 'rgba(0, 166, 214, 0.7)',  // TU Delft cyan
                    borderColor: 'rgba(0, 166, 214, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
```

---

## 8. Migration Strategy

### 8.1 Migration Overview

**Goal:** Assign faculty_id to 580+ existing datasets with ≥90% accuracy

**Approach:** Hybrid strategy combining automated parsing with manual review

**Timeline:** 2-3 weeks for complete migration

### 8.2 Migration Phases

#### Phase 1: Analysis & Preparation (Days 1-3)

**Tasks:**
1. Export all datasets for TU Delft (institution_id = 28586)
2. Analyze Organizations field patterns
3. Build faculty detection patterns
4. Test patterns on sample datasets
5. Calculate expected confidence scores

**Deliverables:**
- Pattern configuration file
- Sample migration results (100 datasets)
- Confidence score distribution analysis

#### Phase 2: Automated Migration (Days 4-7)

**Tasks:**
1. Run automated faculty detection on all datasets
2. Auto-assign high-confidence matches (≥0.8)
3. Flag medium-confidence for manual review (0.5-0.8)
4. Flag low-confidence / no-match for manual assignment (<0.5)
5. Generate migration reports

**Deliverables:**
- Migration statistics report
- CSV file of manual review cases
- Backup of original data

#### Phase 3: Manual Review (Days 8-14)

**Tasks:**
1. Review medium-confidence cases
2. Manually assign faculty to flagged datasets
3. Validate auto-assigned cases (spot checks)
4. Handle edge cases (multi-faculty, international, etc.)

**Deliverables:**
- Manual review CSV (completed)
- Quality assurance report
- Edge case documentation

#### Phase 4: Bulk Import (Days 15-17)

**Tasks:**
1. Import manually reviewed assignments
2. Validate referential integrity
3. Update RDF store with faculty_id triples
4. Invalidate statistics cache
5. Verify statistics correctness

**Deliverables:**
- Updated RDF database
- Migration completion report
- Statistics validation results

#### Phase 5: Validation & Rollout (Days 18-21)

**Tasks:**
1. Compare before/after statistics
2. User acceptance testing
3. Train institutional staff
4. Communicate changes to users
5. Monitor for issues

**Deliverables:**
- UAT sign-off
- Training documentation
- Release notes

### 8.3 Migration Scripts

#### 8.3.1 Export Script

**File:** `scripts/export_datasets_for_migration.py`

```python
#!/usr/bin/env python3
"""
Export datasets for faculty migration analysis.
"""

import csv
import sys
from djehuty.web.database import SparqlInterface
from djehuty.web.config import config

def export_datasets(institution_id, output_file):
    """Export all datasets for an institution."""
    
    db = SparqlInterface()
    db.setup_sparql_endpoint()
    
    datasets = db.datasets(
        institution_id=institution_id,
        is_published=True,
        limit=None
    )
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'uuid', 'dataset_id', 'title', 'doi', 'organizations',
            'published_date', 'institution_id'
        ])
        writer.writeheader()
        
        for dataset in datasets:
            writer.writerow({
                'uuid': dataset.get('uuid'),
                'dataset_id': dataset.get('dataset_id'),
                'title': dataset.get('title'),
                'doi': dataset.get('doi'),
                'organizations': dataset.get('organizations', ''),
                'published_date': dataset.get('published_date'),
                'institution_id': dataset.get('institution_id')
            })
    
    print(f"Exported {len(datasets)} datasets to {output_file}")

if __name__ == "__main__":
    export_datasets(28586, "tudelft_datasets_for_migration.csv")
```

#### 8.3.2 Pattern Detection Script

**File:** `scripts/detect_faculty_patterns.py`

```python
#!/usr/bin/env python3
"""
Detect faculty from Organizations field using pattern matching.
"""

import re
import csv
import json

# Faculty detection patterns
FACULTY_PATTERNS = {
    285860001: {  # Aerospace Engineering
        "name": "Faculty of Aerospace Engineering",
        "patterns": [
            r"Faculty of Aerospace Engineering",
            r"Aerospace Engineering",
            r"\bAE\b.*Faculty",
            r"Luchtvaart",
            r"\bLR\b"
        ],
        "weight": 1.0
    },
    285860002: {  # Architecture
        "name": "Faculty of Architecture and the Built Environment",
        "patterns": [
            r"Faculty of Architecture",
            r"Architecture and the Built Environment",
            r"\bA\+BE\b",
            r"Bouwkunde",
            r"\bBK\b.*Faculty"
        ],
        "weight": 1.0
    },
    285860003: {  # Applied Sciences
        "name": "Faculty of Applied Sciences",
        "patterns": [
            r"Faculty of Applied Sciences",
            r"Applied Sciences",
            r"\bAS\b.*Faculty",
            r"Technische Natuurwetenschappen",
            r"\bTNW\b"
        ],
        "weight": 1.0
    },
    285860004: {  # Civil Engineering
        "name": "Faculty of Civil Engineering and Geosciences",
        "patterns": [
            r"Faculty of Civil Engineering",
            r"Civil Engineering and Geosciences",
            r"\bCEG\b",
            r"Civiele Techniek",
            r"\bCiTG\b"
        ],
        "weight": 1.0
    },
    285860005: {  # EEMCS
        "name": "Faculty of Electrical Engineering, Mathematics and Computer Science",
        "patterns": [
            r"Faculty of Electrical Engineering",
            r"EEMCS",
            r"Elektrotechniek",
            r"\bEWI\b",
            r"Computer Science.*TU Delft",
            r"Mathematics.*TU Delft"
        ],
        "weight": 1.0
    },
    285860006: {  # Industrial Design
        "name": "Faculty of Industrial Design Engineering",
        "patterns": [
            r"Faculty of Industrial Design",
            r"Industrial Design Engineering",
            r"\bIDE\b",
            r"Industrieel Ontwerpen",
            r"\bIO\b.*Faculty"
        ],
        "weight": 1.0
    },
    285860007: {  # Mechanical Engineering
        "name": "Faculty of Mechanical Engineering",
        "patterns": [
            r"Faculty of Mechanical Engineering",
            r"Mechanical.*Engineering",
            r"\b3mE\b",
            r"Werktuigbouwkunde",
            r"\bME\b.*Faculty"
        ],
        "weight": 1.0
    },
    285860008: {  # TPM
        "name": "Faculty of Technology, Policy and Management",
        "patterns": [
            r"Faculty of Technology, Policy",
            r"Technology, Policy and Management",
            r"\bTPM\b",
            r"\bTBM\b"
        ],
        "weight": 1.0
    }
}

def detect_faculty(organizations_text):
    """
    Detect faculty from organizations text.
    
    Returns: (faculty_id, confidence, matched_pattern)
    """
    if not organizations_text:
        return (None, 0.0, None)
    
    matches = []
    
    for faculty_id, config in FACULTY_PATTERNS.items():
        score = 0
        matched_patterns = []
        
        for pattern in config["patterns"]:
            if re.search(pattern, organizations_text, re.IGNORECASE):
                score += config["weight"]
                matched_patterns.append(pattern)
        
        if score > 0:
            matches.append({
                "faculty_id": faculty_id,
                "faculty_name": config["name"],
                "score": score,
                "patterns": matched_patterns
            })
    
    if not matches:
        return (None, 0.0, None)
    
    # Sort by score, take highest
    matches.sort(key=lambda x: x["score"], reverse=True)
    best_match = matches[0]
    
    # Calculate confidence (normalize by number of possible patterns)
    num_patterns = len(FACULTY_PATTERNS[best_match["faculty_id"]]["patterns"])
    confidence = min(best_match["score"] / num_patterns, 1.0)
    
    # Boost confidence if multiple patterns matched
    if len(best_match["patterns"]) >= 2:
        confidence = min(confidence * 1.2, 1.0)
    
    return (
        best_match["faculty_id"],
        round(confidence, 2),
        ", ".join(best_match["patterns"])
    )

def process_datasets(input_csv, output_csv):
    """Process all datasets and detect faculties."""
    
    results = {
        "total": 0,
        "matched": 0,
        "high_confidence": 0,  # ≥ 0.8
        "medium_confidence": 0,  # 0.5 - 0.8
        "low_confidence": 0,  # < 0.5
        "no_match": 0
    }
    
    with open(input_csv, 'r', encoding='utf-8') as infile:
        with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.DictReader(infile)
            
            fieldnames = reader.fieldnames + [
                'detected_faculty_id',
                'detected_faculty_name',
                'confidence',
                'matched_pattern',
                'action'
            ]
            
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                results["total"] += 1
                
                faculty_id, confidence, pattern = detect_faculty(row['organizations'])
                
                # Determine action
                if faculty_id is None:
                    action = "MANUAL_REVIEW"
                    results["no_match"] += 1
                elif confidence >= 0.8:
                    action = "AUTO_ASSIGN"
                    results["high_confidence"] += 1
                    results["matched"] += 1
                elif confidence >= 0.5:
                    action = "MANUAL_REVIEW"
                    results["medium_confidence"] += 1
                    results["matched"] += 1
                else:
                    action = "MANUAL_REVIEW"
                    results["low_confidence"] += 1
                    results["matched"] += 1
                
                row['detected_faculty_id'] = faculty_id or ''
                row['detected_faculty_name'] = FACULTY_PATTERNS.get(faculty_id, {}).get('name', '') if faculty_id else ''
                row['confidence'] = confidence
                row['matched_pattern'] = pattern or ''
                row['action'] = action
                
                writer.writerow(row)
    
    # Print summary
    print("\n=== Migration Detection Summary ===")
    print(f"Total datasets: {results['total']}")
    print(f"Matched: {results['matched']} ({results['matched']/results['total']*100:.1f}%)")
    print(f"  - High confidence (≥0.8): {results['high_confidence']} - AUTO_ASSIGN")
    print(f"  - Medium confidence (0.5-0.8): {results['medium_confidence']} - MANUAL_REVIEW")
    print(f"  - Low confidence (<0.5): {results['low_confidence']} - MANUAL_REVIEW")
    print(f"No match: {results['no_match']} - MANUAL_REVIEW")
    print(f"\nTotal requiring manual review: {results['medium_confidence'] + results['low_confidence'] + results['no_match']}")
    print(f"Output written to: {output_csv}")

if __name__ == "__main__":
    process_datasets(
        "tudelft_datasets_for_migration.csv",
        "tudelft_datasets_with_faculty_detection.csv"
    )
```

#### 8.3.3 Bulk Import Script

**File:** `scripts/import_faculty_assignments.py`

```python
#!/usr/bin/env python3
"""
Bulk import faculty assignments to RDF store.
"""

import csv
import logging
from djehuty.web.database import SparqlInterface
from djehuty.web.config import config

logging.basicConfig(level=logging.INFO)

def import_faculty_assignments(input_csv, min_confidence=0.8, dry_run=True):
    """
    Import faculty assignments from CSV.
    
    Args:
        input_csv: CSV file with columns: uuid, detected_faculty_id, confidence, action
        min_confidence: Minimum confidence for auto-assignment
        dry_run: If True, don't actually update database
    """
    
    db = SparqlInterface()
    db.setup_sparql_endpoint()
    
    stats = {
        "total": 0,
        "auto_assigned": 0,
        "skipped": 0,
        "failed": 0
    }
    
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            stats["total"] += 1
            
            uuid = row['uuid']
            faculty_id = row['detected_faculty_id']
            confidence = float(row['confidence']) if row['confidence'] else 0.0
            action = row['action']
            
            # Skip if no faculty detected or below threshold
            if not faculty_id or confidence < min_confidence or action != "AUTO_ASSIGN":
                stats["skipped"] += 1
                logging.info(f"Skipping {uuid}: confidence={confidence}, action={action}")
                continue
            
            # Update dataset
            try:
                if not dry_run:
                    success = db.update_dataset_faculty(uuid, int(faculty_id))
                    if not success:
                        stats["failed"] += 1
                        logging.error(f"Failed to update {uuid}")
                        continue
                
                stats["auto_assigned"] += 1
                logging.info(f"Assigned faculty {faculty_id} to dataset {uuid} (confidence={confidence})")
            
            except Exception as e:
                stats["failed"] += 1
                logging.error(f"Error updating {uuid}: {e}")
    
    # Print summary
    print("\n=== Import Summary ===")
    print(f"Total datasets processed: {stats['total']}")
    print(f"Auto-assigned: {stats['auto_assigned']}")
    print(f"Skipped: {stats['skipped']}")
    print(f"Failed: {stats['failed']}")
    
    if dry_run:
        print("\n⚠️  DRY RUN - No changes were made to the database")
    else:
        print("\n✅ Import complete - Database updated")

if __name__ == "__main__":
    import sys
    
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    
    import_faculty_assignments(
        "tudelft_datasets_with_faculty_detection.csv",
        min_confidence=0.8,
        dry_run=dry_run
    )
```

### 8.4 Manual Review Workflow

**Tool:** Web-based review interface (optional) or CSV editing

#### CSV Review Format

```csv
uuid,dataset_id,title,organizations,detected_faculty_id,detected_faculty_name,confidence,manual_faculty_id,notes
abc123,12345,"Wing Study","TU Delft, Aerospace...",285860001,"Faculty of Aerospace",0.95,285860001,"Confirmed"
def456,12346,"Building Materials","TU Delft",,,0.0,285860002,"Based on title"
...
```

**Review Instructions:**
1. Check `detected_faculty_id` and `confidence`
2. If confidence < 0.8, review Organizations field and title
3. Fill in `manual_faculty_id` if different or if detection failed
4. Add notes for future reference
5. Submit reviewed CSV for import

#### Web Interface (Future Enhancement)

```
┌──────────────────────────────────────────────────────────┐
│  Faculty Migration Review                                │
├──────────────────────────────────────────────────────────┤
│  Dataset 130 of 580                          [ ← ] [ → ] │
│                                                           │
│  Title: "Building Materials Study"                       │
│  DOI: 10.4121/12345678                                   │
│                                                           │
│  Organizations Field:                                     │
│  "TU Delft, Section Materials and Environment"           │
│                                                           │
│  Detected Faculty: None (confidence: 0.0)                │
│                                                           │
│  Assign Faculty: *                                        │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Faculty of Architecture and Built Environment  ▼  │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  Notes (optional):                                        │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Based on "Materials and Environment" section      │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  [ Skip ]           [ Save & Next ]      [ Save & Prev ] │
└──────────────────────────────────────────────────────────┘
```

### 8.5 Quality Assurance

#### 8.5.1 Validation Checks

1. **Referential Integrity**
   - All faculty_id values exist in faculty taxonomy
   - All datasets have valid institution_id

2. **Consistency Checks**
   - Faculty belongs to correct institution
   - No orphaned faculty_id references

3. **Statistics Validation**
   - Sum of faculty datasets equals total datasets
   - No datasets counted multiple times

#### 8.5.2 Sample Validation Query

```python
def validate_migration():
    """Run validation checks on migrated data."""
    
    db = SparqlInterface()
    
    # Check 1: Orphaned faculty_id references
    query = """
    PREFIX djht: <https://ontologies.data.4tu.nl/djehuty#>
    SELECT ?dataset ?faculty_id
    WHERE {
        ?dataset djht:faculty_id ?faculty_id .
        FILTER NOT EXISTS {
            ?faculty djht:id ?faculty_id ;
                     rdf:type djht:Faculty .
        }
    }
    """
    orphaned = db.__run_query(query)
    if orphaned:
        print(f"❌ Found {len(orphaned)} orphaned faculty_id references")
    else:
        print("✅ No orphaned faculty_id references")
    
    # Check 2: Faculty-institution mismatch
    query = """
    PREFIX djht: <https://ontologies.data.4tu.nl/djehuty#>
    SELECT ?dataset ?dataset_inst ?faculty_inst
    WHERE {
        ?dataset djht:institution_id ?dataset_inst ;
                 djht:faculty_id ?faculty_id .
        ?faculty djht:id ?faculty_id ;
                 djht:institution_id ?faculty_inst .
        FILTER (?dataset_inst != ?faculty_inst)
    }
    """
    mismatches = db.__run_query(query)
    if mismatches:
        print(f"❌ Found {len(mismatches)} institution-faculty mismatches")
    else:
        print("✅ No institution-faculty mismatches")
    
    # Check 3: Statistics consistency
    total_datasets = db.repository_statistics()["datasets"]
    faculty_stats = db.faculty_statistics(institution_id=28586)
    faculty_total = sum(s["datasets"] for s in faculty_stats)
    
    if faculty_total <= total_datasets:
        print(f"✅ Faculty statistics consistent (faculty: {faculty_total}, total: {total_datasets})")
    else:
        print(f"❌ Faculty statistics inconsistent!")
    
    print("\nValidation complete.")
```

---

## 9. Implementation Phases

### Phase 1: Foundation (Weeks 1-2)

**Objective:** Establish data model and configuration

**Tasks:**
1. Design and document RDF schema extensions
2. Create faculty taxonomy for TU Delft (validate with stakeholders)
3. Extend XML configuration with faculty definitions
4. Update `database.py` with faculty insertion methods
5. Create SPARQL templates for faculty queries
6. Unit tests for faculty data operations

**Deliverables:**
- [ ] Updated RDF schema documentation
- [ ] `djehuty.xml` with TU Delft faculties
- [ ] `insert_faculty()`, `update_account_faculty()`, `update_dataset_faculty()` methods
- [ ] SPARQL templates: `faculties.sparql`, `statistics_faculty.sparql`
- [ ] Unit test suite (≥80% coverage)

**Success Criteria:**
- ✅ Faculty entities can be inserted into RDF store
- ✅ Faculty validation works correctly
- ✅ All tests pass

### Phase 2: API & Services (Weeks 2-3)

**Objective:** Implement backend services and API endpoints

**Tasks:**
1. Implement `FacultyManager` service
2. Implement `FacultyStatisticsService`
3. Create API endpoints for faculties
4. Create API endpoints for faculty statistics
5. Add faculty field to account/dataset endpoints
6. Implement response formatting (JSON, CSV)
7. Integration tests for API endpoints

**Deliverables:**
- [ ] `FacultyManager` class with configuration loading
- [ ] `FacultyStatisticsService` with aggregation methods
- [ ] API routes: `/v2/institutions/{id}/faculties`, `/v2/statistics/faculties`
- [ ] Extended account/dataset endpoints with faculty support
- [ ] Integration test suite

**Success Criteria:**
- ✅ API endpoints return correct data
- ✅ Statistics aggregation is accurate
- ✅ Response time < 100ms for faculty stats
- ✅ All integration tests pass

### Phase 3: Migration (Weeks 3-4)

**Objective:** Migrate existing datasets to have faculty_id

**Tasks:**
1. Implement `FacultyMigrationService`
2. Develop faculty detection patterns
3. Export datasets for analysis
4. Run automated detection (dry run)
5. Manual review of flagged cases
6. Bulk import faculty assignments
7. Validation and QA

**Deliverables:**
- [ ] Migration scripts (export, detect, import)
- [ ] Faculty detection pattern configuration
- [ ] Migration report (statistics, confidence distribution)
- [ ] Manually reviewed CSV file
- [ ] Updated RDF database with faculty_id triples

**Success Criteria:**
- ✅ ≥90% of datasets have faculty_id assigned
- ✅ All validation checks pass
- ✅ No data loss or corruption
- ✅ Statistics match expected values

### Phase 4: UI Development (Weeks 4-5)

**Objective:** Build user-facing interfaces

**Tasks:**
1. Faculty dropdown in registration form
2. Faculty field in dataset deposit form
3. Faculty statistics dashboard
4. Chart.js visualizations
5. CSV export functionality
6. Responsive design for mobile
7. UI/UX testing

**Deliverables:**
- [ ] Updated registration page with faculty selection
- [ ] Updated dataset form with faculty field
- [ ] Statistics dashboard with faculty breakdown
- [ ] Charts and visualizations
- [ ] Mobile-friendly responsive design

**Success Criteria:**
- ✅ Users can select faculty during registration
- ✅ Faculty auto-fills in dataset form
- ✅ Statistics dashboard displays correctly
- ✅ UI works on desktop and mobile

### Phase 5: Testing & Deployment (Week 5)

**Objective:** Final testing and production deployment

**Tasks:**
1. End-to-end testing
2. Performance testing (load, stress)
3. User acceptance testing (UAT)
4. Training documentation
5. Release notes
6. Production deployment
7. Monitoring and support

**Deliverables:**
- [ ] E2E test results
- [ ] Performance test report
- [ ] UAT sign-off
- [ ] User documentation
- [ ] Admin documentation
- [ ] Release notes
- [ ] Deployed to production

**Success Criteria:**
- ✅ All tests pass
- ✅ Performance meets requirements
- ✅ UAT approved by stakeholders
- ✅ Zero critical bugs in production
- ✅ Users successfully using faculty features

---

## 10. Security & Privacy Considerations

### 10.1 Data Privacy

**Faculty Information:**
- Faculty affiliation is considered public metadata
- No GDPR concerns (institutional data, not personal)
- Users can change faculty in profile settings

**Access Control:**
- Faculty statistics visible to all authenticated users
- No faculty-level permissions required (additive feature)
- Admin can manage faculty taxonomy via XML config

### 10.2 Input Validation

```python
def validate_faculty_input(faculty_id, institution_id):
    """Validate faculty_id to prevent injection attacks."""
    
    # Type validation
    if not isinstance(faculty_id, int):
        raise ValueError("faculty_id must be integer")
    
    # Range validation
    if faculty_id < 1 or faculty_id > 999999999:
        raise ValueError("faculty_id out of valid range")
    
    # Referential integrity
    valid_faculties = config.get_faculties_for_institution(institution_id)
    if faculty_id not in [f["id"] for f in valid_faculties]:
        raise ValueError(f"Faculty {faculty_id} not found for institution {institution_id}")
    
    return faculty_id
```

### 10.3 SPARQL Injection Prevention

All faculty_id values are parameterized in SPARQL queries:

```python
# SAFE - Using template parameters
query = self.__query_from_template("statistics_faculty", {
    "faculty_id": faculty_id  # Integer, validated
})

# UNSAFE - String concatenation (NEVER DO THIS)
query = f"SELECT * WHERE {{ ?dataset djht:faculty_id {faculty_id} }}"
```

### 10.4 Audit Logging

Log all faculty assignments for audit trail:

```python
logging.info("Faculty assignment: dataset=%s, faculty_id=%s, user=%s, confidence=%s",
             dataset_uuid, faculty_id, account_uuid, confidence)
```

---

## 11. Performance & Scalability

### 11.1 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Faculty list query | < 50ms | Response time |
| Faculty statistics | < 100ms | Response time (cached) |
| Dataset list by faculty | < 150ms | Response time (10 items) |
| Account update (faculty) | < 200ms | Total request time |
| Statistics cache hit rate | ≥ 80% | Cache effectiveness |

### 11.2 Caching Strategy

**Cache Layers:**

1. **Faculty Taxonomy Cache**
   - In-memory cache of faculty configuration
   - TTL: Infinity (reload on config change)
   - Size: < 1 MB

2. **Statistics Cache**
   - File-based cache (existing mechanism)
   - TTL: 1 hour
   - Invalidation: On dataset/account faculty update

3. **Query Result Cache**
   - RDFlib query cache
   - TTL: 5 minutes
   - Size: 100 MB

**Cache Invalidation:**

```python
def update_dataset_faculty(self, dataset_uuid, faculty_id):
    """Update faculty_id with cache invalidation."""
    
    # Update RDF
    success = self.__run_logged_query(update_query)
    
    if success:
        # Invalidate caches
        self.cache.invalidate_by_prefix(f"datasets_{dataset_uuid}")
        self.cache.invalidate_by_prefix("faculty_statistics")
        self.cache.invalidate_by_prefix("repository_statistics")
    
    return success
```

### 11.3 Database Indexing

**Virtuoso Indexes:**

```sql
-- Create index on faculty_id for faster filtering
CREATE INDEX faculty_idx ON DB.DBA.RDF_QUAD (
    O  -- Object (the faculty_id value)
) WHERE P = <https://ontologies.data.4tu.nl/djehuty#faculty_id>;
```

### 11.4 Query Optimization

**Optimized SPARQL:**

```sparql
-- GOOD: Use specific predicates
SELECT ?faculty_id (COUNT(?dataset) AS ?count)
WHERE {
    ?dataset djht:faculty_id ?faculty_id ;
             djht:is_public "true"^^xsd:boolean .
}
GROUP BY ?faculty_id

-- BAD: Broad pattern matching
SELECT ?faculty_id (COUNT(?dataset) AS ?count)
WHERE {
    ?dataset ?p ?o ;
             djht:faculty_id ?faculty_id .
}
GROUP BY ?faculty_id
```

### 11.5 Scalability Considerations

**Current Scale:**
- 580 datasets (TU Delft)
- 8 faculties per institution
- 4 institutions (4TU)

**Projected Scale (5 years):**
- 5,000 datasets
- 10 faculties per institution
- 10 institutions

**Scaling Strategy:**
- Virtuoso can handle 1M+ triples (currently ~50K)
- Statistics pre-aggregation for large datasets
- Pagination for all list endpoints
- Consider materialized views for complex aggregations

---

## 12. Testing Strategy

### 12.1 Unit Tests

**Coverage:** ≥80% of new code

**Test Cases:**

```python
class TestFacultyManager(unittest.TestCase):
    """Unit tests for FacultyManager."""
    
    def test_load_taxonomy(self):
        """Test loading faculty taxonomy from XML."""
        manager = FacultyManager("test_config.xml")
        faculties = manager.get_faculties_for_institution(28586)
        self.assertEqual(len(faculties), 8)
    
    def test_validate_faculty_id(self):
        """Test faculty validation."""
        manager = FacultyManager("test_config.xml")
        # Valid faculty
        self.assertTrue(manager.validate_faculty_id(285860001, 28586))
        # Invalid faculty
        with self.assertRaises(ValueError):
            manager.validate_faculty_id(999999, 28586)
    
    def test_get_faculty_name(self):
        """Test faculty name retrieval."""
        manager = FacultyManager("test_config.xml")
        name = manager.get_faculty_name(285860001)
        self.assertEqual(name, "Faculty of Aerospace Engineering")

class TestFacultyMigration(unittest.TestCase):
    """Unit tests for migration service."""
    
    def test_pattern_detection(self):
        """Test faculty detection from organizations field."""
        service = FacultyMigrationService(db, faculty_manager)
        
        # High confidence match
        faculty_id, conf = service.parse_organizations_field(
            "TU Delft, Faculty of Aerospace Engineering", 28586
        )
        self.assertEqual(faculty_id, 285860001)
        self.assertGreater(conf, 0.8)
        
        # No match
        faculty_id, conf = service.parse_organizations_field(
            "External organization", 28586
        )
        self.assertIsNone(faculty_id)
        self.assertEqual(conf, 0.0)
```

### 12.2 Integration Tests

**Test API Endpoints:**

```python
class TestFacultyAPI(unittest.TestCase):
    """Integration tests for faculty API."""
    
    def test_list_faculties(self):
        """Test GET /v2/institutions/28586/faculties."""
        response = self.client.get('/v2/institutions/28586/faculties')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('faculties', data)
        self.assertGreater(len(data['faculties']), 0)
    
    def test_faculty_statistics(self):
        """Test GET /v2/statistics/faculties."""
        response = self.client.get('/v2/statistics/faculties?institution=28586')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('statistics', data)
        # Verify structure
        for stat in data['statistics']:
            self.assertIn('faculty_id', stat)
            self.assertIn('datasets', stat)
            self.assertIn('total_downloads', stat)
```

### 12.3 Performance Tests

**Load Testing:**

```python
import time
import statistics as stats

def test_faculty_statistics_performance():
    """Test response time for faculty statistics."""
    
    times = []
    for i in range(100):
        start = time.time()
        response = client.get('/v2/statistics/faculties?institution=28586')
        end = time.time()
        times.append((end - start) * 1000)  # ms
    
    avg_time = stats.mean(times)
    p95_time = stats.quantiles(times, n=20)[18]  # 95th percentile
    
    print(f"Average response time: {avg_time:.2f}ms")
    print(f"95th percentile: {p95_time:.2f}ms")
    
    assert avg_time < 100, "Average response time exceeds 100ms"
    assert p95_time < 200, "95th percentile exceeds 200ms"
```

### 12.4 User Acceptance Testing

**Test Scenarios:**

1. **New User Registration**
   - User creates account with TU Delft email
   - Faculty dropdown appears
   - User selects "Faculty of Aerospace Engineering"
   - Account saved with faculty_id

2. **Dataset Deposit**
   - User creates new dataset
   - Faculty pre-filled from account
   - User can override if needed
   - Dataset published with correct faculty_id

3. **Statistics Viewing**
   - Admin views statistics dashboard
   - Faculty breakdown displayed correctly
   - Numbers match manual count
   - Export to CSV works

---

## 13. Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Data Migration Errors** | Medium | High | • Dry-run testing<br>• Manual review of low-confidence<br>• Backup before import<br>• Rollback plan |
| **Performance Degradation** | Low | Medium | • Performance testing before deploy<br>• Query optimization<br>• Caching strategy<br>• Virtuoso tuning |
| **User Confusion** | Medium | Low | • Clear UI labels<br>• Help text and tooltips<br>• Training documentation<br>• Support channel |
| **Faculty Taxonomy Changes** | Medium | Low | • Version-controlled XML<br>• Migration script for changes<br>• Clear change process |
| **API Breaking Changes** | Low | High | • Backward compatibility<br>• Optional fields<br>• Versioned API endpoints |
| **Stakeholder Disagreement** | Medium | Medium | • Early validation of taxonomy<br>• Iterative feedback<br>• Pilot with one institution |
| **Scope Creep** | High | Medium | • Fixed feature set<br>• Document future enhancements<br>• Phase 2 roadmap |

---

## 14. Success Metrics

### 14.1 Technical Metrics

- ✅ Faculty statistics endpoint response time < 100ms
- ✅ Migration accuracy ≥ 90%
- ✅ Test coverage ≥ 80%
- ✅ Zero production incidents in first month
- ✅ API backward compatibility maintained

### 14.2 User Metrics

- ✅ ≥ 80% of new users select faculty during registration
- ✅ ≥ 90% of new datasets have faculty_id
- ✅ User satisfaction score ≥ 4/5
- ✅ < 5% support tickets related to faculty feature

### 14.3 Business Metrics

- ✅ Faculty statistics available for all 4TU institutions
- ✅ Institutional dashboards show faculty breakdown
- ✅ Reports can be exported and shared
- ✅ Feature adopted by at least 3 of 4 institutions

---

## 15. Conclusion

This solution architecture provides a comprehensive plan for implementing faculty-level statistics in the Djehuty repository system. The approach is:

- **Technically Sound**: Extends existing RDF model without breaking changes
- **Scalable**: Designed for growth from 580 to 5000+ datasets
- **User-Friendly**: Intuitive UI with minimal clicks
- **Accurate**: Hybrid migration strategy achieving ≥90% accuracy
- **Maintainable**: Configuration-driven taxonomy, clear documentation

**Key Innovations:**
1. Hybrid migration strategy (automated + manual review)
2. Confidence-based assignment with thresholds
3. Backward-compatible API extensions
4. Flexible faculty taxonomy (XML/JSON)

**Next Steps:**
1. Stakeholder validation of faculty taxonomy
2. Approval of implementation timeline
3. Resource allocation (1 developer, 5 weeks)
4. Kick-off Phase 1 (Foundation)

---

*End of Solution Architecture Document*
