import io
import os
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from churn import run_pipeline
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

def make_json_safe(obj):
    """Recursively convert numpy/pandas/shap/LabelEncoder objects to JSON-safe Python types."""
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, (np.ndarray, pd.Series, list, tuple)):
        return [make_json_safe(x) for x in obj]
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient="records")
    elif isinstance(obj, LabelEncoder):
        return {"classes": obj.classes_.tolist()}
    elif isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    else:
        return obj


@app.route("/")
def home():
    return jsonify({"message": "Churn Prediction API is running 🚀"})


@app.route("/predict", methods=["POST"])
def predict():
    print("DEBUG — request.files:", request.files)
    print("DEBUG — request.form:", request.form)
    print("DEBUG — request.content_type:", request.content_type)

    try:
        df = None

        # ---------------------------
        # 1️⃣ JSON input
        # ---------------------------
        if request.is_json:
            data = request.get_json()
            df = pd.DataFrame([data]) if isinstance(data, dict) else pd.DataFrame(data)
            print("📥 Received JSON input")

        # ---------------------------
        # 2️⃣ CSV file upload
        # ---------------------------
        elif "file" in request.files:
            file = request.files["file"]
            if file.filename == "":
                return jsonify({"error": "No selected file"}), 400

            print("📁 Received file:", file.filename)
            df = pd.read_csv(io.TextIOWrapper(file.stream, encoding="utf-8"))
            print(f"✅ CSV loaded successfully with shape: {df.shape}")

        else:
            return jsonify({"error": "No valid JSON or CSV input provided"}), 400

        # ---------------------------
        # 3️⃣ Run ML pipeline
        # ---------------------------
        print("🚀 Running churn prediction pipeline...")
        results = run_pipeline(df, show_plots=False)

        # ---------------------------
        # 4️⃣ Convert to JSON-safe structure
        # ---------------------------
        safe_results = make_json_safe(results)
        return jsonify(safe_results)

    except Exception as e:
        import traceback
        print("❌ ERROR:\n", traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # ✅ Use dynamic port for Railway
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
