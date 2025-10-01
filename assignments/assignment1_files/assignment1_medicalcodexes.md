# Medical Codex Data Pipeline Assignment

## Real-World Context

This assignment simulates actual work you'd do as a data engineer or data scientist in healthcare technology. Companies like Epic, Cerner, or health insurance providers maintain exactly these types of data pipelines to ensure their systems have current medical coding standards.

The skills you'll develop:
- Healthcare data domain knowledge
- ETL pipeline development
- Data quality validation
- File format optimization
- Production-ready code practices

## Scenario
You are a data scientist at a healthcare software company. Your team maintains updated reference lists of medical codexes that are critical for the company's products. These codexes change regularly, so you need to build a robust data pipeline to keep them current.

## Assignment Overview
Create Python scripts that can process each medical codex listed below into standardized CSV format. Your pipeline should handle data cleaning, validation, and format conversion for production use.

## Target Medical Codexes
Based on your company's `about.md` reference document:

1. **SNOMED CT (US)** - Clinical terminology
2. **ICD-10-CM (US)** - Diagnosis codes  
3. **ICD-10 (WHO)** - International diagnosis codes
4. **HCPCS (US)** - Healthcare procedure codes
5. **LOINC (US)** - Laboratory test codes
6. **RxNorm (US)** - Medication codes
7. **NPI (US)** - Healthcare provider identifiers

## Repository Setup
1. Create a **public** GitHub repository named `medical-codex-pipeline`
2. **Important**: Repository must be public for submission
3. Structure:
   ```
   medical-codex-pipeline/
   ├── input/
   ├── scripts/
   │   ├── snomed_processor.py
   │   ├── icd10cm_processor.py
   │   ├── icd10who_processor.py
   │   ├── hcpcs_processor.py
   │   ├── loinc_processor.py
   │   ├── rxnorm_processor.py
   │   └── npi_processor.py
   ├── output/
   │   ├── csv/
   ├── utils/
   │   └── common_functions.py
   ├── requirements.txt
   └── README.md
   ```

4. **Important**: Create `.gitignore` to exclude raw data files:
   ```gitignore
   # Raw data files (exclude from repo)
   input/
   *.txt
   *.xml
   *.zip
   raw_downloads/
   
   # Processed files are OK to commit
   # output/ - keep these
   
   # Python
   __pycache__/
   *.pyc
   .env
   venv/
   
   # IDE
   .vscode/
   .idea/
   ```

---

## Core Requirements

### 1. Data Processing Scripts
For **each** of the 7 medical codexes, create a Python script that:

#### Data Loading & Validation
- Read the raw data file(s) in their native format
- Validate data integrity (check for required fields, detect corruption)
- Log any data quality issues found
- Which data files? 
    - Based on what I have provided in my example scripts, only load the example fize that I have referenced in my python file. Some of the medical codexes like RXnorm and SnowMed contains dozens of files. You have the option of either just working with the one that I have identified, or you can identify your own. 

#### Data Cleaning & Standardization
- Handle missing or null values appropriately
- Standardize text fields (trim whitespace, normalize case)
- Validate code formats according to each standard's rules
- Remove or flag invalid/retired codes

#### Output Generation
- **CSV Export**: Clean, standardized CSV with consistent column names


#### Expected Output Format
Standardize column names across all codexes:
- `code`: The primary identifier
- `description`: Human-readable description
- `last_updated`: Processing timestamp

### 2. Common Utilities Module
Create `utils/common_functions.py` with one reusable function:
- `save_to_formats(df, base_filename)`: Save DataFrame to CSV 

This function will be used across all processing scripts to ensure consistent output formatting.

### 3. Documentation & Testing
- **README.md**: Setup instructions, usage examples, data source links
- **Docstrings**: All functions must have clear documentation
- **Error Handling**: Robust exception handling with informative messages
- **Logging**: Use Python logging module to track processing steps

---

## Optional Extensions

### Level 1: Web Download Automation (Bonus)
Add download functionality to each script:
- Automatically fetch latest files from official sources
- Handle authentication where required (API keys, login)
- Implement retry logic for network failures
- Validate downloaded files before processing

### Level 2: GitHub Actions Pipeline (Bonus)
*Save this for later implementation*
- Set up automated workflow to check for updates
- Run processing scripts on schedule
- Commit updated files to repository
- Send notifications on processing failures

---

## Sample Code Structure

```python
# icd10cm_processor.py
import pandas as pd
import logging
from pathlib import Path
from utils.common_functions import validate_code_format, save_to_formats

def load_icd10cm_data(filepath):
    """Load raw ICD-10-CM data file"""
    pass

def clean_icd10cm_data(raw_data):
    """Clean and standardize ICD-10-CM codes"""
    pass

def main():
    logging.basicConfig(level=logging.INFO)
    
    # Load raw data
    raw_data = load_icd10cm_data("input/icd10cm_codes_2024.txt")
    
    # Clean and process
    clean_data = clean_icd10cm_data(raw_data)
    
    # Save outputs
    save_to_formats(clean_data, "output/icd10cm_2024")
    
    logging.info("ICD-10-CM processing completed")

if __name__ == "__main__":
    main()
```

---

## Deliverables

### Required Files
- 7 processing scripts (one per codex)
- Common utilities module
- requirements.txt with all dependencies
- README.md with complete documentation
- Sample output files for each codex (CSV)

### Expected Libraries
- `pandas` - Data manipulation
- `requests` - HTTP downloads (optional extension)
- `logging` - Process logging
- Standard library: `pathlib`, `json`, `datetime`

## Submission

**Submit your public GitHub repository URL through Brightspace.**

Make sure your repository:
- Is **public** and accessible
- Contains all required files and scripts
- Includes sample output files for demonstration
- Has a complete README with setup and usage instructions