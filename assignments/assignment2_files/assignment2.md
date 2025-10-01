# Assignment 2 (Lite, Split) — Single-Table Patient Roster in SQLite
*Two-step workflow: (1) create DB with Python, (2) load CSV with Pandas/SQLAlchemy; then run simple queries.*

## Learning goals
- Create a **stand-alone `.sql` schema** for a single table.  
- Use **Python (sqlite3)** to create an SQLite database from a schema file.  
- Load a CSV into SQLite with **Pandas + SQLAlchemy**.  
- Write and run **single-table SELECT** queries in DB Browser for SQLite.

---

## What you will build

### Repo scaffold
```
health-sqlite-lite/
├─ data/
│  └─ patients.csv
├─ sql/
│  ├─ schema.sql
│  └─ analysis.sql
├─ src/
│  ├─ create_db.py         
│  └─ import_csv.py        
├─ clinic_simple.db        
├─ requirements.txt
└─ README.md
```

### 1) Define the schema (single table) — `sql/schema.sql`
> Minimal example; no indexes, no foreign keys.

```sql
-- sql/schema.sql
DROP TABLE IF EXISTS patients;

CREATE TABLE patients (
  patient_id     TEXT PRIMARY KEY,         -- e.g., P0001
  birth_date     DATE NOT NULL,            -- ISO: YYYY-MM-DD
  primary_icd10  TEXT NOT NULL,            -- e.g., E11.9
  last_cpt       TEXT NOT NULL,            -- e.g., 99213
  last_visit_dt  DATE NOT NULL             -- ISO date
);
```

### 2) Review the CSV and put it into the proper location — `patients.csv`
It looks like this: 

```csv
patient_id,birth_date,primary_icd10,last_cpt,last_visit_dt
P0001,1980-05-03,E11.9,99213,2025-08-14
P0002,1972-11-19,I10,93000,2025-07-30
P0003,1995-02-07,J45.909,99214,2025-06-21
P0004,1968-09-12,M54.5,72100,2025-04-09
P0005,1988-01-25,N18.3,80053,2025-03-18
P0006,2001-12-03,F41.9,99213,2025-05-02
P0007,1977-07-28,K21.9,43235,2025-02-10
P0008,1960-03-15,E78.5,83036,2025-08-02
```

### 3) Step 1 — Create the database with Python (`src/create_db.py`)
This script uses Python’s **sqlite3** to create `clinic_simple.db` and apply `sql/schema.sql`.


### 4) Step 2 — Load the CSV with Pandas/SQLAlchemy (`src/import_csv.py`)
This script appends `patients.csv` rows into the `patients` table.


### 5) Simple queries — `sql/analysis.sql`
All queries are single-table.

```sql
-- A) Row count
SELECT COUNT(*) AS n_patients FROM patients;

-- B) Top primary diagnoses by count
SELECT primary_icd10, COUNT(*) AS n
FROM patients
GROUP BY primary_icd10
ORDER BY n DESC;

-- C) Office-visit CPTs since Jan 1, 2025 (CPT codes starting with 992)
SELECT patient_id, last_cpt, last_visit_dt
FROM patients
WHERE last_cpt LIKE '992%' AND last_visit_dt >= '2025-01-01'
ORDER BY last_visit_dt DESC;

-- D) Age (approx) at last visit for the 5 oldest patients
SELECT
  patient_id,
  birth_date,
  last_visit_dt,
  CAST((julianday(date('now')) - julianday(birth_date)) / 365.25 AS INT) AS age_years
FROM patients
ORDER BY age_years DESC
LIMIT 5;

-- E) Quick data quality check: any blank codes?
SELECT *
FROM patients
WHERE primary_icd10 = '' OR last_cpt = '';
```

---

## How to run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. **Step 1:** Create the database
   ```bash
   python src/create_db.py
   ```
3. **Step 2:** Load the CSV
   ```bash
   python src/import_csv.py
   ```
4. Open `clinic_simple.db` in **DB Browser for SQLite** and run `sql/analysis.sql`.

**`requirements.txt`**
```
pandas
SQLAlchemy
```

---

## Deliverables (GitHub URL) submitted to brightspace called `sqlite_pandas_dbs`
1. `sql/schema.sql`
2. `data/patients.csv` (≥25 rows)
3. `src/create_db.py` and `src/import_csv.py`
4. `sql/analysis.sql`
5. `clinic_simple.db` (checked in)
6. `README.md` with:
   - Brief overview of the project (2-3 sentences)
   - Run steps (how to recreate the database)
   - **Query results section**: For each query (A-E) in `analysis.sql`, include:
     - The query description
     - A screenshot or text output of the results from DB Browser
     - 1-2 sentence explanation of what the results show

---
