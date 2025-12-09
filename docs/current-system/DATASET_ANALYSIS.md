# Dataset Structure Analysis
## Assignment: Faculty-Level Statistics Feature

### Date: December 9, 2025

---

## 1. Sample Datasets Examined

### Dataset 1: Aviation NOx Transport (TU Delft - Aerospace Engineering)
**URL:** https://data.4tu.nl/datasets/31f3537b-4137-4ac4-bde2-e0811105921c

#### Key Metadata Fields Found:
- **Institution:** Delft University of Technology (logo displayed)
- **Organizations Field:** 
  - "TU Delft, Faculty of Aerospace Engineering, Section Aircraft Noise and Climate Effects"
  - "Deutsches Zentrum für Luft- und Raumfahrt, Institut für Physik der Atmosphäre"
- **Categories:** Aerospace Engineering, Atmospheric Sciences
- **Funding:** European Commission grant
- **Multiple Authors:** From different institutions (TU Delft + German DLR)
- **DOI:** 10.4121/16886977.v1

**Key Observations:**
✅ Organizations field contains **structured faculty information** (Faculty of Aerospace Engineering)
✅ Multiple organizations listed (cross-institutional collaboration)
❌ No author-specific affiliation details visible on main page
❌ No ORCID displayed for authors on the dataset page

---

### Dataset 2: Aeolian Deposition Patterns (University of Twente)
**URL:** https://data.4tu.nl/datasets/40731af1-dfcc-46eb-93c2-b4d715676ea6

#### Key Metadata Fields Found:
- **Institution:** University of Twente (logo displayed)
- **Organizations Field:**
  - "University of Twente, Water Engineering and Management"
  - "TU Delft, Faculty of Civil Engineering and Geosciences, Department of Hydraulic Engineering"
- **Categories:** Civil Engineering, Land And Water Management, Physical Geography
- **Funding:** Dutch Research Council + CoastScan
- **Multiple Authors:** Collaboration between Twente and TU Delft

**Key Observations:**
✅ Organizations field contains **faculty-level detail** (Faculty of Civil Engineering and Geosciences)
✅ Department-level granularity also present
✅ Multiple institutions collaborating on single dataset
❌ Still free-text format in Organizations field

---

### Dataset 3: CRK-LRR Receptor Kinases (Wageningen University)
**URL:** https://data.4tu.nl/datasets/ac081516-5311-481e-b7a2-07c5ea9b1991

#### Key Metadata Fields Found:
- **Institution:** Wageningen University and Research (logo displayed)
- **Organizations Field:**
  - "Laboratory of Biochemistry, Wageningen University & Research"
  - "Laboratory of Plant Breeding, Wageningen University & Research"
  - "Department of Cell & Systems Biology, University of Toronto"
- **Categories:** Biochemistry And Cell Biology, Biological Sciences
- **Data Status:** Under embargo until 2030-01-01
- **Multiple Authors:** International collaboration (Netherlands + Canada)

**Key Observations:**
✅ Department/Laboratory level detail
✅ International collaboration visible
❌ **Data under embargo** - cannot see author details currently
❌ Organizations field is free text

---

## 2. ORCID Profile Analysis

### Sample: Gabriela Kuhn (0000-0003-1718-3109)
**Current Employment (visible on ORCID):**
- **Position:** Software Engineer (4TU.ResearchData)
- **Institution:** Delft University of Technology
- **Location:** Delft, South Holland, NL
- **Period:** 2023-11 to present

**Education:**
- Master Student in Applied Computing
- Universidade do Vale do Rio dos Sinos, Brazil
- Period: 2021-01 to 2022-12

**Key Observations:**
✅ ORCID contains **current institutional affiliation**
✅ Employment history with dates
✅ Self-asserted source (not institutionally verified in this case)
❌ **No faculty-level information** in ORCID profile
❌ Affiliation is at institution level only

---

## 3. Current Data Structure Issues

### Problem 1: Free-Text Organizations Field
```
Current format:
"TU Delft, Faculty of Aerospace Engineering, Section Aircraft Noise and Climate Effects"
```
**Issues:**
- No standardized structure
- Unpredictable format variations
- Difficult to parse programmatically
- Inconsistent across datasets
- Multiple formats: "Faculty of X", "Faculty X", "X Faculty", etc.

### Problem 2: Depositor-Centric Statistics
- Statistics are currently grouped by **depositing author's institution only**
- Co-authors from other institutions are **not counted** in statistics
- **Example:** If a TU Delft researcher deposits a dataset with 3 co-authors from Eindhoven, only TU Delft gets credit in the statistics

### Problem 3: Missing ORCID Data
- ORCID IDs are **not mandatory**
- When present, ORCID profiles typically show:
  - Institution-level affiliation only
  - **No faculty/department information**
  - Self-asserted data (not always verified)

### Problem 4: Multi-Author Attribution
```
Dataset with authors from:
- TU Delft (Faculty of Aerospace)
- DLR Germany (Institut für Physik)

Current behavior:
→ Only depositor's institution counted in statistics
→ Other institutions/faculties ignored
```

---

## 4. Data Model Structure (Inferred from Analysis)

### Current RDF/SPARQL Schema
Based on the system architecture:

```turtle
# Dataset entity
<dataset:UUID> a djehuty:Dataset ;
    djehuty:title "Dataset title" ;
    djehuty:depositor <account:UUID> ;
    djehuty:organizations "Free text field" ;  # ← PROBLEM: Unstructured
    djehuty:categories <category:UUID> ;
    ...
    
# Account entity  
<account:UUID> a djehuty:Account ;
    djehuty:email "user@tudelft.nl" ;  # ← Used to determine institution
    djehuty:orcid "0000-0003-1718-3109" ;  # ← Optional
    ...
    
# Institution determined from email domain
# e.g., @tudelft.nl → Delft University of Technology (ID 28586)
```

### Groups/Institutions Configuration
From `djehuty.xml`:
```xml
<group name="4TU.ResearchData" domain="4tu.nl" id="28585" parent_id="0" />
<group name="Delft University of Technology" domain="tudelft.nl" id="28586" parent_id="28585" is_featured="1" />
<group name="Delft University of Technology Students" domain="student.tudelft.nl" id="28628" parent_id="28586" is_featured="1" />
```

**Key Insight:** 
- Groups have hierarchical structure (`parent_id`)
- Matched by email `domain`
- **No faculty-level groups currently exist**

---

## 5. Key Findings Summary

### ✅ What We Have:
1. **Institution-level identification** works well (via email domains)
2. **Organizations field** often contains faculty information (as free text)
3. **ORCID integration** exists (optional field)
4. **Hierarchical group structure** already in place
5. **Multiple authors** per dataset are supported
6. **Category/keyword** system for dataset classification

### ❌ What We're Missing:
1. **Structured faculty/department taxonomy**
2. **Reliable faculty attribution** per author
3. **Multi-author statistics** (only depositor counted)
4. **Mandatory ORCID** for better affiliation tracking
5. **Faculty-level groups** in the system hierarchy
6. **Automated parsing** of Organizations field
7. **Faculty mapping** for existing data

---

## 6. Edge Cases Identified

### Edge Case 1: Multiple Authors, Different Faculties
```
Dataset authors:
- Author 1 (TU Delft, Aerospace) - Depositor
- Author 2 (TU Delft, Civil Engineering)
- Author 3 (University of Twente, Water Management)

Question: Which faculty gets credit?
Currently: Only TU Delft (depositor's institution)
Desired: All three faculties should be counted
```

### Edge Case 2: Free-Text Variations
```
Observed variations:
- "Faculty of Aerospace Engineering"
- "Faculty Aerospace Engineering"  
- "Aerospace Engineering Faculty"
- "Fac. Aerospace Eng."
- "Aerospace Engineering, TU Delft"
- "TU Delft - Aerospace"
```

### Edge Case 3: No Organizations Data
```
Some datasets may have:
- Empty Organizations field
- Only institution name
- Only department (no faculty)
- External/industry affiliations
```

### Edge Case 4: ORCID Missing or Incomplete
```
Scenarios:
- No ORCID provided
- ORCID exists but has no affiliation data
- ORCID has outdated affiliation
- ORCID affiliation at institution level only (no faculty)
```

### Edge Case 5: Historical Data
```
Existing datasets (580+ transactions in logs):
- Were deposited before faculty-level tracking
- Have free-text Organizations field
- May have changed author affiliations since deposit
```

### Edge Case 6: Cross-Institutional Collaborations
```
International/external organizations:
- "Deutsches Zentrum für Luft- und Raumfahrt" (Germany)
- "University of Toronto" (Canada)

Question: How to handle non-4TU institutions?
```

---

## 7. Recommended Next Steps

### Phase 1: Analysis
- [ ] Query existing datasets to analyze Organizations field patterns
- [ ] Determine frequency of ORCID usage
- [ ] Identify most common faculty names/structures
- [ ] Count multi-author datasets

### Phase 2: Design
- [ ] Create faculty taxonomy for 4TU institutions
- [ ] Design data model for faculty entities
- [ ] Plan ORCID integration enhancement
- [ ] Design migration strategy for existing data

### Phase 3: Implementation
- [ ] Extend RDF schema with faculty entities
- [ ] Build faculty mapping/selection UI
- [ ] Implement ORCID affiliation fetching
- [ ] Create statistics aggregation for faculties
- [ ] Build data migration tools

---

## 8. Questions for Stakeholders

1. **Scope:** Should we track faculties for all 4TU institutions or start with one?
2. **ORCID:** Should we make ORCID mandatory for new deposits?
3. **Historical Data:** How important is accurate faculty attribution for old datasets?
4. **External Collaborators:** Should non-4TU institutions be tracked at faculty level?
5. **Maintenance:** Who will maintain the faculty taxonomy as institutions reorganize?
6. **Author Changes:** How to handle researchers who change faculties/institutions?

---

## Appendix: Useful URLs

- **Live Sandbox:** https://next.data.4tu.nl/
- **Production Site:** https://data.4tu.nl/
- **Sample Datasets:**
  - https://data.4tu.nl/datasets/ac081516-5311-481e-b7a2-07c5ea9b1991
  - https://data.4tu.nl/datasets/31f3537b-4137-4ac4-bde2-e0811105921c
  - https://data.4tu.nl/datasets/40731af1-dfcc-46eb-93c2-b4d715676ea6
  - https://data.4tu.nl/datasets/49513019-dc6d-4f6e-9bc5-36bc4d8db1a7
  - https://data.4tu.nl/datasets/342efadc-66f8-4e9b-9d27-da7b28b849d2/5
- **ORCID Example:** https://orcid.org/0000-0003-1718-3109
- **GitHub Repository:** https://github.com/4TUResearchData/djehuty
