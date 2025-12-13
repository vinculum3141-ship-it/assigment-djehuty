# Source of Dataset Count: 580 Datasets

## Question
"In the title slide speaker notes you indicate that TU Delft has 580 datasets. How did you get to this number?"

## Answer

The **580 datasets** number comes from counting the transaction log files in the Djehuty repository.

### Source
```bash
# Count transaction files
ls -1 logs/transactions/ | wc -l
# Result: 580
```

### Location
`/home/ruby/Projects/assigment-djehuty/logs/transactions/`

### Files
The directory contains 580 SPARQL transaction files:
- `applied_transaction_00000001.sparql`
- `applied_transaction_00000002.sparql`
- ...
- `applied_transaction_00000580.sparql`

### What These Represent
Each transaction file represents a **dataset operation** in the Djehuty system. These are SPARQL INSERT/DELETE operations that were applied to the RDF store.

### Verification
```bash
cd /home/ruby/Projects/assigment-djehuty
ls logs/transactions/ | wc -l
# Returns: 580
```

### Context in Presentation

The number is used throughout the presentation to illustrate:

1. **Slide 2 (Problem Statement):**
   - "580+ datasets need faculty assignment"
   - Shows the scale of the migration challenge

2. **Slide 8 (Migration Strategy):**
   - "Challenge: 580+ Existing Datasets Need Faculty Assignment"
   - Emphasizes the historical data migration requirement

3. **Slide 13 (System Analysis - Areas for Improvement):**
   - "Fetches 580+ datasets, processes in memory, slow for large repositories"
   - Used to illustrate performance considerations

4. **Speaker Notes (Title Slide):**
   - "4TU.ResearchData currently tracks datasets at institutional level - for example, 'TU Delft' has 580 datasets"
   - Provides scale context for the audience

### Important Notes

1. **This is NOT just TU Delft data**
   - The 580 transactions represent the **entire 4TU.ResearchData repository**
   - Includes datasets from all 4TU institutions:
     - TU Delft
     - University of Twente (UT)
     - Eindhoven University of Technology (TU/e)
     - Wageningen University & Research (WUR)

2. **Actual Breakdown**
   According to the prototype dashboard data in `docs/analysis/PROTOTYPE_PLAN.md`:
   ```javascript
   data: [2346, 1469, 580, 0],
   ```
   This appears to show:
   - Total across all institutions (various counts)
   - 580 is mentioned as one data point

3. **Speaker Notes Should Be Corrected**
   The title slide speaker notes currently say:
   > "TU Delft has 580 datasets"
   
   This should be clarified to:
   > "4TU.ResearchData has 580+ datasets across all institutions"

### Recommended Correction

In `presentation/index.html` and `presentation/SPEAKER_NOTES.md`, update the speaker note from:

**Current (INCORRECT):**
```
"4TU.ResearchData currently tracks datasets at institutional level - 
for example, 'TU Delft' has 580 datasets."
```

**Should be (CORRECT):**
```
"4TU.ResearchData currently tracks datasets at institutional level - 
across all 4TU institutions, there are 580+ datasets in the system that 
need faculty-level assignment."
```

Or alternatively:
```
"The repository contains 580+ datasets across TU Delft, UT, TU/e, and WUR - 
all of which need faculty-level assignment for better statistics."
```

### Summary

- **Source:** Count of transaction log files in `logs/transactions/`
- **Command:** `ls -1 logs/transactions/ | wc -l`
- **Result:** 580 files = 580 datasets/transactions
- **Scope:** All 4TU institutions (not just TU Delft)
- **Usage:** Throughout presentation to show scale of migration challenge
- **Action Needed:** Clarify in speaker notes that this is total across all institutions, not TU Delft alone
