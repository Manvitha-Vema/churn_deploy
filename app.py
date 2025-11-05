from flask import Flask, request, jsonify
import joblib
import pandas as pd
from churn import run_pipeline, fit_xgb, prepare_data

app = Flask(__name__)

@app.route('/')
def home():
    return "Churn Prediction API is running 🚀"

@app.route('/train', methods=['POST'])
def train_model():
    file = request.files['file']
    df = pd.read_csv(file)
    results = run_pipeline(df, show_plots=False)
    joblib.dump(results['final_metrics'], "final_metrics.joblib")
    return jsonify({"message": "Model trained successfully", "metrics": results['final_metrics']})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    model = joblib.load("xgb_churn_model.joblib")
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return jsonify({"prediction": int(prediction)})

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
