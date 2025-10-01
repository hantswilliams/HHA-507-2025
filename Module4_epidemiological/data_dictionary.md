# Data Dictionary - Simulated Lung Cancer Study

**Dataset:** simulated_data.csv
**Study:** Association between smoking and lung cancer
**Location:** Small rural town (Millbrook, NY)
**Sample Size:** (n) participants - variable

---

## Variables

| Variable Name | Type | Description | Values/Range |
|--------------|------|-------------|--------------|
| `id` | Integer | Unique participant identifier | 1-1000 |
| `name` | String | Participant name (simulated) | Text |
| `age` | Integer | Age in years | 18-85 |
| `gender` | String | Biological sex | Male, Female |
| `address` | String | Street address (simulated) | Text (all in Millbrook, NY) |
| `is_smoker` | Boolean | Current smoking status | True, False |
| `at_risk` | Boolean | Flag indicating if participant is in at-risk population | True, False |
| `has_cancer` | Boolean | Lung cancer diagnosis status | True, False |
| `is_new_case` | Boolean | Indicates if cancer diagnosis is new | True, False | 

---

## Data Generation Rules

### Cancer Probability by Smoking Status
- **Smokers:** 20% probability of having lung cancer
- **Non-smokers:** 2% probability of having lung cancer



