from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

MODEL_PATH = os.environ.get("MODEL_PATH", "models/model.pkl")
model = joblib.load(MODEL_PATH)

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json()
    # expect payload: {"instances": [[...], [...]]}
    instances = payload.get("instances", [])
    df = pd.DataFrame(instances)
    preds = model.predict(df).tolist()
    return jsonify({"predictions": preds})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
