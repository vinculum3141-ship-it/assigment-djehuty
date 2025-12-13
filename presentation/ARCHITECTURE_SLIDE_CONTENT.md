# Technical Architecture - Faculty-Level Statistics

## System Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  ┌──────────────────┐  ┌──────────────────────────────────┐ │
│  │  Registration    │  │  Statistics Dashboard            │ │
│  │  (Faculty        │  │  (Faculty breakdown charts)      │ │
│  │   Dropdown)      │  │  • Export to CSV                 │ │
│  └──────────────────┘  └──────────────────────────────────┘ │
└─────────────┬───────────────────────────────────────────────┘
              │ REST API (JSON)
┌─────────────┴───────────────────────────────────────────────┐
│                  APPLICATION LAYER                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ FacultyManager | StatisticsService | MigrationService │ │
│  │ ─────────────────────────────────────────────────────  │ │
│  │ • faculty_list()          → Get all faculties         │ │
│  │ • faculty_by_id()         → Get faculty details       │ │
│  │ • statistics_for_faculty() → Aggregated counts        │ │
│  │ • migrate_dataset()       → Pattern matching          │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────┬───────────────────────────────────────────────┘
              │ SPARQL Queries
┌─────────────┴───────────────────────────────────────────────┐
│                   DATA LAYER (RDF Store)                    │
│                                                             │
│  Account ──faculty_id──→ Faculty ←─faculty_id── Dataset    │
│      ↓                       ↓                      ↓       │
│  faculty_id             institution_id          faculty_id  │
│  (optional)             (required)              (optional)  │
│                                                             │
│  Cache: Redis (statistics) + In-memory (faculty lists)     │
└─────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. Presentation Layer
- **Registration Forms**: Faculty dropdown for account creation
- **Statistics Dashboard**: Visual faculty-level reports with charts
- **REST API**: JSON endpoints for all operations

### 2. Application Layer
Three main services:

| Service | Purpose | Key Methods |
|---------|---------|-------------|
| **FacultyManager** | Faculty CRUD operations | `faculty_list()`, `faculty_by_id()` |
| **StatisticsService** | Dataset aggregation | `statistics_for_faculty()`, `export_csv()` |
| **MigrationService** | Historical data cleanup | `migrate_dataset()`, `pattern_match()` |

### 3. Data Layer (RDF Store)
- **Entities**: Faculty, Account, Dataset, Institution
- **Optional Links**: Account/Dataset → Faculty (backward compatible)
- **Caching**: Redis for stats (1hr TTL), in-memory for faculty lists

## RDF Schema Extension

```turtle
# NEW Entity
djht:Faculty rdf:type owl:Class .

# NEW Predicates
djht:faculty_id        → Links Account/Dataset to Faculty
djht:faculty_name      → Faculty display name
djht:faculty_short_name → Abbreviation (e.g., "AE")
djht:institution_id    → Faculty belongs to Institution
```

## Data Relationships

```
Institution (e.g., TU Delft)
    ↓
Faculty (e.g., Faculty of Aerospace Engineering)
    ↓
Account (has faculty_id="tu-delft-ae")
    ↓
Dataset (inherits faculty_id from Account)
```

## Example RDF Triples

```turtle
# Define a Faculty
<faculty/tu-delft-ae> rdf:type djht:Faculty ;
                      djht:faculty_id "tu-delft-ae" ;
                      djht:faculty_name "Faculty of Aerospace Engineering" ;
                      djht:faculty_short_name "AE" ;
                      djht:institution_id "tu-delft" .

# Link Account to Faculty
<account/123> djht:faculty_id "tu-delft-ae" .

# Link Dataset to Faculty
<dataset/456> djht:faculty_id "tu-delft-ae" .
```

## Data Flow: New Dataset Deposit

1. **User logs in** → Account has `faculty_id="tu-delft-ae"`
2. **User deposits dataset** → `faculty_id` copied from Account to Dataset
3. **Dataset saved** to RDF store with faculty triple
4. **Statistics cache invalidated** (Redis)
5. **Next query** → SPARQL aggregates by `faculty_id` → Updated count

## Caching Strategy

| Cache Type | Content | TTL | Invalidation |
|------------|---------|-----|--------------|
| **Redis** | Statistics results | 1 hour | On new dataset |
| **In-memory** | Faculty lists | Indefinite | On config change |

## Key Architectural Decisions

### ✓ 3-Tier Architecture
**Why**: Clean separation of concerns, testable, maintainable

### ✓ Optional faculty_id (Backward Compatible)
**Why**: Existing datasets continue working, no breaking changes

### ✓ Configuration-Driven
**Why**: Each 4TU institution defines own faculty structure

### ✓ SPARQL-Based Statistics
**Why**: Leverages existing RDF infrastructure, no new database

### ✓ Multi-Layer Caching
**Why**: Performance - statistics expensive, faculty lists rarely change

### ✓ Additive Approach (Not Replacement)
**Why**: Risk mitigation - Organizations field still works, new field added

## Performance Characteristics

- **Faculty list retrieval**: <10ms (in-memory cache)
- **Statistics query**: <100ms (with Redis cache)
- **Dataset deposit**: +5ms overhead (one extra triple write)
- **Migration**: ~50 datasets/second (pattern matching bottleneck)

## Technology Stack

| Layer | Technology |
|-------|----------|
| **RDF Store** | Existing Djehuty RDF infrastructure |
| **Cache** | Redis + Python dict |
| **Query Language** | SPARQL 1.1 |
| **API** | REST (JSON) |
| **Configuration** | YAML files (per institution) |
