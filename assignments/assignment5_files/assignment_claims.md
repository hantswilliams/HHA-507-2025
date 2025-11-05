# Healthcare Claims Data Analysis Assignment

## Real-World Context

This assignment simulates the type of analysis performed daily by healthcare data analysts, medical billing specialists, and health informaticians. Understanding claims data is essential for:
- Revenue cycle management
- Coding accuracy audits
- Payer contract analysis
- Clinical quality reporting
- Healthcare operations optimization

The skills you'll develop:
- Working with relational healthcare data
- Understanding claims data structure (HEADER, LINE, CODE files)
- Performing multi-table joins and aggregations
- Analyzing provider billing patterns
- Identifying common diagnosis-procedure combinations

## Scenario

You are a data analyst at Stony Brook University Hospital. The compliance and revenue cycle teams have provided you with a sample of prospective claims data from May 2024. They need your help analyzing billing patterns, identifying the most common diagnoses and procedures, and understanding payer mix to support operational decision-making.

## Assignment Overview

You will analyze three interconnected claims files to answer key questions about provider billing patterns, common diagnoses, procedures, and payer relationships. This assignment focuses on relational data analysis using Python and pandas.

## Dataset Description

The claims data consists of three CSV files that form a relational database structure:

### 1. HEADER File (`STONYBRK_20240531_HEADER.csv`)
Contains one row per claim with high-level information:
- **ProspectiveClaimId**: Unique claim identifier
- **Provider NPIs**: Billing, Attending, Rendering, Referring, Operating providers
- **ServiceFromDate/ServiceToDate**: Service dates
- **PrimaryPayerName/PrimaryPayerCode**: Primary insurance payer
- **PlaceOfService**: Where services were rendered
- **WorkQueName**: Audit/review queue assignment

### 2. LINE File (`STONYBRK_20240531_LINE.csv`)
Contains one row per service line (procedures/services):
- **ProspectiveClaimId**: Links to HEADER file
- **LinePos**: Line number on the claim
- **HCPCS**: CPT/HCPCS procedure code
- **Modifier1-4**: Procedure modifiers
- **DxMapDelim**: Shows which diagnosis codes justify this procedure
- **Charges**: Dollar amount billed for this line
- **Units**: Quantity of service

### 3. CODE File (`STONYBRK_20240531_CODE.csv`)
Contains diagnosis codes (ICD-10):
- **ProspectiveClaimId**: Links to HEADER file
- **CodePos**: Position/order of diagnosis on claim
- **CodeValue**: ICD-10 diagnosis code
- **CodeQualifier**: Code type (ABF, ABK, etc.)

## Data Location

The data files are located in:
```
Module6_claims/clean/example_2/
    STONYBRK_20240531_HEADER.csv
    STONYBRK_20240531_LINE.csv
    STONYBRK_20240531_CODE.csv
```

## Repository Setup

1. Create a **public** GitHub repository named `claims-analysis`
2. Structure your repository:
   ```
    .venv
    data/
       *.csv 
    notebooks/
        claims_analysis.ipynb
    requirements.txt
    README.md
   ```

3. **Important**: Create `.gitignore` to exclude data files:
   ```gitignore
   # Data files (too large for GitHub)
   data/*.csv
   data/*.txt

   # Python
   __pycache__/
   *.pyc
   .env
   venv/

   # Jupyter
   .ipynb_checkpoints/

   # Environment
   .venv

   # IDE
   .vscode/
   .idea/
   ```

---

## Instructions

### Part 1: Data Loading and Exploration 
Complete the following tasks in a Google Colab or Jupyter notebook:

1. **Load the three CSV files** into pandas DataFrames
   - Use appropriate variable names: `df_header`, `df_line`, `df_code`

2. **Explore each file** by displaying:
   - Shape (number of rows and columns)
   - First 5 rows
   - Column names and data types
   - Missing value counts
   - Basic descriptive statistics for numeric columns

3. **Document your observations** about:
   - How many unique claims are in the dataset?
   - What is the date range of the claims?
   - How many service lines are there on average per claim?
   - How many diagnosis codes are there on average per claim?

### Part 2: Relational Data Analysis 
Answer the following questions using pandas operations (merge, groupby, value_counts, etc.):

**Question 1: Provider Analysis**
- Who are the top 5 billing providers by number of claims?
- Display: Provider name, NPI, and claim count
- Create a simple bar chart showing the top 5 providers

**Question 2: Payer Mix Analysis**
- What are the top 5 primary payers by claim volume?
- Calculate the percentage of total claims for each payer
- Create a bar chart or pie chart showing payer distribution

**Question 3: Common Diagnoses**
- What are the 10 most frequently appearing diagnosis codes (CodeValue)?
- Display: ICD-10 code and frequency count
- Note: You may want to look up what these codes mean online (icd10data.com)

**Question 4: Common Procedures**
- What are the 10 most frequently billed procedure codes (HCPCS)?
- Display: HCPCS code, description (if available in data), and frequency
- Create a bar chart showing the top 10 procedures

**Question 5: Service Location Analysis**
- How many claims were submitted for each PlaceOfService?
- What percentage of claims are for "INPATIENT" vs "DOCTOR'S OFFICE"?

### Part 3: Advanced Analysis with Joins 

**Question 6: Claims with High Service Line Counts**
- Merge the HEADER and LINE files
- Calculate the total number of service lines per claim
- Identify claims with 5 or more service lines
- Display: ClaimId, Provider name, number of lines, and total charges

**Question 7: Diagnosis-Procedure Combinations**
- Create a merged dataset linking claims to both procedures and diagnoses
- Find the most common diagnosis code (CodeValue) associated with CPT code 99291
- Hint: You'll need to merge all three files together

**Question 8: Charges by Payer**
- Merge HEADER and LINE files
- Calculate total charges (sum of all line charges) per claim
- Group by PrimaryPayerName and calculate:
  - Total charges
  - Average charges per claim
  - Number of claims
- Sort by total charges descending and display top 10 payers

### Part 4: Creative Analysis  

**Question 9: Your Own Analysis**
Develop and answer your own analytical question using the claims data. Your question should:
- Require merging at least two of the three files
- Use groupby or aggregation
- Provide meaningful insight about the data
- Include at least one visualization

Examples of questions you could explore:
- Which providers bill for the most complex cases (highest number of diagnosis codes)?
- What is the relationship between place of service and average charges?
- Are there seasonal patterns in claim submissions?
- Which diagnosis codes are most commonly paired together?

---

## Deliverables

1. **Google Colab or Jupyter Notebook** (`.ipynb` file) containing:
   - All code for loading and analyzing data
   - Clear markdown cells explaining each analysis step
   - Visualizations for key findings
   - Written interpretations of your results
   - Comments in your code explaining complex operations

2. **README.md** in your GitHub repository with:
   - Brief project description
   - Data source information
   - How to run the notebook
   - Summary of key findings (3-5 bullet points)
   - Required libraries

3. **requirements.txt** with necessary Python packages:
   ```
   pandas>=1.3.0
   matplotlib>=3.4.0
   seaborn>=0.11.0
   ```



## REMEMBER!!!! 

1. **Multiple rows per claim**: Remember that LINE and CODE files have multiple rows per ProspectiveClaimId
2. **Aggregation**: When calculating totals, make sure you're not double-counting
3. **Data types**: Service dates may need to be converted to datetime format

