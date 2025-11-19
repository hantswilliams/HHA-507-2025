# Flask app for Diabetes Disease Progression Prediction
# Loads the trained XGBoost model and provides a web interface for predictions
# To install dependencies:
#   pip install flask joblib xgboost numpy scikit-learn

from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('Module9/p0_models/models/regression_diabetes_xgb.model')

# Define raw value ranges and their mapping to standardized space
# The sklearn diabetes dataset is pre-standardized, so we map realistic
# clinical ranges to the typical standardized range of the dataset
# Format: (raw_min, raw_max, std_min, std_max)
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

# Feature names in order expected by model
FEATURE_NAMES = ['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']


def scale_raw_to_standardized(raw_values):
    """
    Convert raw clinical values to standardized values expected by the model.
    Uses linear interpolation from raw ranges to standardized ranges.
    """
    scaled_values = []

    for i, name in enumerate(FEATURE_NAMES):
        raw_val = raw_values[i]
        scale = FEATURE_SCALING[name]

        # Linear interpolation: map raw range to standardized range
        raw_range = scale['raw_max'] - scale['raw_min']
        std_range = scale['std_max'] - scale['std_min']

        # Normalize to 0-1, then scale to standardized range
        normalized = (raw_val - scale['raw_min']) / raw_range
        std_val = scale['std_min'] + (normalized * std_range)

        scaled_values.append(std_val)

    return scaled_values


@app.route('/', methods=['GET'])
def home():
    """Display the prediction form"""
    return render_template(
        'index.html',
        values={},
        prediction=None
    )


@app.route('/predict', methods=['POST'])
def predict():
    """Handle form submission and make prediction"""
    # Get raw values from form
    raw_values = {}
    feature_values = []

    for name in FEATURE_NAMES:
        value = float(request.form.get(name, 0))
        raw_values[name] = value
        feature_values.append(value)

    # Scale raw values to standardized space
    scaled_values = scale_raw_to_standardized(feature_values)

    # Make prediction
    X = np.array([scaled_values])
    prediction = model.predict(X)[0]

    # Round to 1 decimal place
    prediction = round(prediction, 1)

    return render_template(
        'index.html',
        values=raw_values,
        prediction=prediction
    )


if __name__ == '__main__':
    print("=" * 50)
    print("Diabetes Disease Progression Predictor")
    print("=" * 50)
    print("\nModel loaded successfully!")
    print("\nOpen http://127.0.0.1:5000 in your browser")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, port=5000)
