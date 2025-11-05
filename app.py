# app.py
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os
import time

MODEL_PATH = os.environ.get("MODEL_PATH", "models/model.pkl")
# load model once per container
model = joblib.load(MODEL_PATH)

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200

@app.route("/predict", methods=["POST"])
def predict():
    # Expect: {"instances": [[...], [...]]}
    payload = request.get_json(force=True, silent=True) or {}
    instances = payload.get("instances", [])

    if not instances:
        return {"error": "no instances"}, 400

    try:
        df = pd.DataFrame(instances)
        start = time.time()
        preds = model.predict(df).tolist()
        latency_ms = (time.time() - start) * 1000.0
        return {"predictions": preds, "latency_ms": latency_ms}, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

