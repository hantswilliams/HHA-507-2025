import joblib
import numpy as np

# -------------------------------------------------
# 1. Load the trained model
# -------------------------------------------------

model = joblib.load('Module9/p0_models/models/regression_diabetes_xgb.model')


# -------------------------------------------------
# 2. Define your input values
# -------------------------------------------------
# Edit these values to make predictions for different patients
# All values should be in real-world clinical units

# Patient demographics and physical measurements
age = 50              # Age in years (range: 20-80)
sex = 0               # Sex: 0 = Male, 1 = Female
bmi = 25.0            # Body Mass Index in kg/m� (range: 15-45)
bp = 90               # Average blood pressure in mmHg (range: 60-130)

# Cholesterol and lipid values
s1_total_cholesterol = 200    # Total cholesterol in mg/dL (range: 100-350)
s2_ldl = 120                  # LDL cholesterol in mg/dL (range: 50-250)
s3_hdl = 50                   # HDL cholesterol in mg/dL (range: 20-100)
s4_tch_ratio = 4.5            # Total cholesterol / HDL ratio (range: 2-10)

# Other blood markers
s5_triglycerides = 4.5        # Log of triglycerides (range: 3.0-6.5)
s6_blood_sugar = 90           # Blood glucose in mg/dL (range: 60-150)


# -------------------------------------------------
# 3. Scale raw values to standardized space
# -------------------------------------------------
# The model was trained on standardized data, so we need to convert
# our real-world values to the standardized scale

def scale_raw_to_standardized(raw_values, feature_scaling):
    """Convert raw clinical values to standardized values."""
    scaled = []
    for name, raw_val in raw_values.items():
        scale = feature_scaling[name]
        raw_range = scale['raw_max'] - scale['raw_min']
        std_range = scale['std_max'] - scale['std_min']
        normalized = (raw_val - scale['raw_min']) / raw_range
        std_val = scale['std_min'] + (normalized * std_range)
        scaled.append(std_val)
    return scaled

# Scaling parameters (maps raw ranges to standardized ranges)
FEATURE_SCALING = {
    'age': {'raw_min': 20, 'raw_max': 80, 'std_min': -0.107, 'std_max': 0.107},
    'sex': {'raw_min': 0, 'raw_max': 1, 'std_min': -0.044, 'std_max': 0.044},
    'bmi': {'raw_min': 15, 'raw_max': 45, 'std_min': -0.090, 'std_max': 0.170},
    'bp': {'raw_min': 60, 'raw_max': 130, 'std_min': -0.112, 'std_max': 0.132},
    's1': {'raw_min': 100, 'raw_max': 350, 'std_min': -0.127, 'std_max': 0.154},
    's2': {'raw_min': 50, 'raw_max': 250, 'std_min': -0.116, 'std_max': 0.199},
    's3': {'raw_min': 20, 'raw_max': 100, 'std_min': -0.102, 'std_max': 0.181},
    's4': {'raw_min': 2, 'raw_max': 10, 'std_min': -0.076, 'std_max': 0.185},
    's5': {'raw_min': 3.0, 'raw_max': 6.5, 'std_min': -0.126, 'std_max': 0.133},
    's6': {'raw_min': 60, 'raw_max': 150, 'std_min': -0.138, 'std_max': 0.135},
}

# Organize input values
raw_input = {
    'age': age,
    'sex': sex,
    'bmi': bmi,
    'bp': bp,
    's1': s1_total_cholesterol,
    's2': s2_ldl,
    's3': s3_hdl,
    's4': s4_tch_ratio,
    's5': s5_triglycerides,
    's6': s6_blood_sugar,
}

# -------------------------------------------------
# 4. Make prediction
# -------------------------------------------------

# Scale the raw values
scaled_values = scale_raw_to_standardized(raw_input, FEATURE_SCALING)

# Create feature array for model
X = np.array([scaled_values])

# Get prediction
prediction = model.predict(X)[0]

print(f"Disease Progression Score: {prediction:.1f}")

print("\n  Interpretation:")
print("    - Lower values indicate less disease progression")
print("    - Higher values indicate more disease progression")
print("    - Typical range: 25 - 346")



# -------------------------------------------------
# 6. Example: Try different patients
# -------------------------------------------------
#
# patients = [
#     {'age': 30, 'sex': 0, 'bmi': 22, 'bp': 80, 's1': 180, 's2': 100, 's3': 60, 's4': 3.0, 's5': 4.0, 's6': 80},
#     {'age': 55, 'sex': 1, 'bmi': 30, 'bp': 100, 's1': 240, 's2': 150, 's3': 40, 's4': 6.0, 's5': 5.0, 's6': 110},
#     {'age': 70, 'sex': 0, 'bmi': 35, 'bp': 120, 's1': 280, 's2': 180, 's3': 35, 's4': 8.0, 's5': 5.5, 's6': 130},
# ]
#
# for i, patient in enumerate(patients, 1):
#     scaled = scale_raw_to_standardized(patient, FEATURE_SCALING)
#     X = np.array([scaled])
#     pred = model.predict(X)[0]
#     print(f"  Patient {i}: Age={patient['age']}, BMI={patient['bmi']}, BP={patient['bp']} -> Score: {pred:.1f}")
