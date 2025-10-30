# Inferential Statistics Test Examples

This directory contains comprehensive examples of inferential statistical tests using clinical datasets. Each script demonstrates a specific test type with detailed explanations, interpretations, and visualizations.

## Overview

All examples use real-world clinical data from:
- `patient_data.csv` - Patient demographics and characteristics
- `claims_data.csv` - Healthcare claims and billing information

## Test Examples

### 1. ANOVA (Analysis of Variance)

#### `anova_patient_data.py`
**Research Question:** Does the mean risk score differ significantly across different insurance types?

- **Variables:**
  - Dependent: risk_score (continuous)
  - Independent: insurance_type (categorical - 4 groups)
- **Use Case:** Comparing means across multiple groups (3+)
- **Key Outputs:** F-statistic, p-value, Tukey HSD post-hoc tests, eta-squared effect size
- **Visualizations:** Boxplots, violin plots, mean comparisons

**Run:**
```bash
python anova_patient_data.py
```

#### `anova_claims_data.py`
**Research Question:** Do mean claim amounts differ significantly across different service types?

- **Variables:**
  - Dependent: claim_amount (continuous)
  - Independent: service_type (categorical - multiple groups)
- **Use Case:** Comparing healthcare costs across service lines
- **Key Outputs:** F-statistic, p-value, Tukey HSD, variance homogeneity tests
- **Visualizations:** Boxplots, violin plots, strip plots with means

**Run:**
```bash
python anova_claims_data.py
```

---

### 2. Chi-Square Test of Independence

#### `chisquare_patient_data.py`
**Research Question:** Is there an association between chronic condition status and Stonybrook patient enrollment?

- **Variables:**
  - Variable 1: chronic_condition (categorical)
  - Variable 2: stonybrook_patient (categorical - enrolled vs not)
- **Use Case:** Testing association between two categorical variables
- **Key Outputs:** Chi-square statistic, p-value, Cramér's V effect size, contingency tables
- **Visualizations:** Stacked bar charts, heatmaps of proportions

**Run:**
```bash
python chisquare_patient_data.py
```

#### `chisquare_claims_data.py`
**Research Question:** Is there an association between claim status and Stonybrook patient enrollment?

- **Variables:**
  - Variable 1: claim_status (categorical - Paid/Denied/Pending)
  - Variable 2: stonybrook_patient (categorical)
- **Use Case:** Examining claim approval patterns across patient groups
- **Key Outputs:** Chi-square, p-value, Cramér's V, standardized residuals
- **Visualizations:** Multiple bar charts, heatmaps, grouped comparisons

**Run:**
```bash
python chisquare_claims_data.py
```

---

### 3. Linear Regression

#### `regression_claims_data.py`
**Research Question:** Can we predict the paid amount of a claim based on the claim amount?

- **Variables:**
  - Dependent (Y): paid_amount (continuous)
  - Independent (X): claim_amount (continuous)
- **Use Case:** Predicting continuous outcomes, examining relationships
- **Key Outputs:** R-squared, regression coefficients, p-values, confidence intervals
- **Visualizations:** Scatter plots with regression line, residual plots, Q-Q plots, diagnostic plots

**Run:**
```bash
python regression_claims_data.py
```

---

### 4. Independent Samples t-Test

#### `ttest_patient_data.py`
**Research Question:** Is there a significant difference in average risk scores between male and female patients?

- **Variables:**
  - Dependent: risk_score (continuous)
  - Independent: gender (categorical - 2 groups)
- **Use Case:** Comparing means between two independent groups
- **Key Outputs:** t-statistic, p-value, Cohen's d effect size, confidence intervals
- **Visualizations:** Boxplots, violin plots, histograms with means, error bars

**Run:**
```bash
python ttest_patient_data.py
```

#### `ttest_claims_data.py`
**Research Question:** Is there a significant difference in average claim amounts between Stonybrook and non-Stonybrook patients?

- **Variables:**
  - Dependent: claim_amount (continuous)
  - Independent: stonybrook_patient (categorical - 2 groups)
- **Use Case:** Comparing healthcare costs between patient groups
- **Key Outputs:** t-statistic, p-value, Cohen's d, Welch's test, normality tests
- **Visualizations:** Multiple comparison plots, distributions, mean comparisons

**Run:**
```bash
python ttest_claims_data.py
```

---

## Common Features Across All Examples

Each script includes:

1. **Detailed Documentation**
   - Research question clearly stated
   - Hypotheses (null and alternative)
   - When to use the test
   - Interpretation guidelines

2. **Comprehensive Analysis**
   - Descriptive statistics
   - Assumption checking
   - Main statistical test
   - Effect size calculations
   - Post-hoc tests (when applicable)

3. **Professional Visualizations**
   - Multiple plot types for data exploration
   - High-quality PNG outputs (300 DPI)
   - Clear labels and titles
   - Saved to the tests directory

4. **Detailed Interpretation**
   - Statistical significance explained
   - Practical/clinical significance discussed
   - Effect size interpretation
   - Business/healthcare implications

5. **Educational Content**
   - Step-by-step explanations
   - Statistical concepts explained
   - Assumption violations addressed
   - Alternative tests suggested when appropriate

## How to Interpret Results

### Statistical Significance
- **p-value < 0.05**: Statistically significant (reject null hypothesis)
- **p-value ≥ 0.05**: Not statistically significant (fail to reject null hypothesis)

### Effect Sizes

**Cohen's d (t-tests):**
- Small: 0.2
- Medium: 0.5
- Large: 0.8

**Eta-squared (ANOVA):**
- Small: 0.01
- Medium: 0.06
- Large: 0.14

**Cramér's V (Chi-square):**
- Small: 0.1
- Medium: 0.3
- Large: 0.5

**R-squared (Regression):**
- Small: 0.01-0.09
- Medium: 0.09-0.25
- Large: 0.25+

## Requirements

All scripts require the following Python packages:

```bash
pip install pandas numpy scipy statsmodels matplotlib seaborn
```

## Output Files

Each script generates:
- Console output with detailed statistics and interpretations
- High-quality visualization PNG files

### Generated Visualization Files:
- `anova_patient_boxplot.png`
- `anova_claims_visualization.png`
- `chisquare_patient_visualization.png`
- `chisquare_claims_visualization.png`
- `regression_claims_analysis.png`
- `ttest_patient_visualization.png`
- `ttest_claims_visualization.png`

## Dataset Information

### patient_data.csv
Contains patient-level information:
- `patient_id`: Unique patient identifier
- `age`: Patient age
- `gender`: M/F
- `risk_score`: Health risk score (continuous)
- `chronic_condition`: Type of chronic condition or "None"
- `insurance_type`: Commercial, Medicare, Medicaid
- `stonybrook_patient`: 0 = not enrolled, 1 = enrolled

### claims_data.csv
Contains claims-level information:
- `claim_id`: Unique claim identifier
- `patient_id`: Links to patient data
- `claim_amount`: Amount billed
- `paid_amount`: Amount paid by payer
- `service_type`: Type of healthcare service
- `claim_status`: Paid, Denied, or Pending
- `stonybrook_patient`: 0 = not enrolled, 1 = enrolled

## Tips for Using These Examples

1. **Start with descriptive statistics** - Understand your data before running tests
2. **Check assumptions** - Each test has specific requirements
3. **Consider effect size** - Statistical significance ≠ practical significance
4. **Visualize your data** - Plots reveal patterns statistics might miss
5. **Interpret in context** - Consider clinical/business implications

## Quick Reference: Which Test to Use?

| Research Goal | Variables | Test to Use |
|--------------|-----------|-------------|
| Compare 2 group means | 1 continuous + 1 binary categorical | Independent t-test |
| Compare 3+ group means | 1 continuous + 1 categorical (3+ groups) | ANOVA |
| Association between categories | 2 categorical variables | Chi-square test |
| Predict continuous outcome | 1+ continuous predictors + 1 continuous outcome | Linear regression |

## Additional Resources

- For paired comparisons (same subjects), use paired t-test
- For non-normal data, consider non-parametric alternatives:
  - Mann-Whitney U (instead of t-test)
  - Kruskal-Wallis (instead of ANOVA)
  - Fisher's Exact Test (instead of Chi-square for small samples)

## Questions or Issues?

Each script is heavily commented and includes detailed explanations. If you have questions about:
- Statistical concepts
- Interpretation of results
- Choosing the appropriate test
- Assumption violations

Refer to the extensive comments within each script or consult a statistics textbook/resource.

---

**Last Updated:** 2025
**Author:** HHA 507 Course Materials
