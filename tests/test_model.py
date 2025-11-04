# tests/test_model.py
import joblib
import pandas as pd
import pytest
from sklearn.metrics import accuracy_score

@pytest.fixture(scope="module")
def model():
    return joblib.load("models/model.pkl")

@pytest.fixture(scope="module")
def data():
    return pd.read_csv("data/iris.csv")

def test_model_exists(model):
    assert model is not None

def test_prediction_shape(model, data):
    # Use original column names - do NOT rename
    X = data.iloc[:, :-1]
    preds = model.predict(X)
    assert preds.shape[0] == len(data)

def test_accuracy_threshold(model, data):
    # Use original column names - do NOT rename
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    preds = model.predict(X)
    # Check accuracy is above threshold
    acc = accuracy_score(y, preds)
    assert acc > 0.5, f"Accuracy {acc:.2f} is below threshold 0.5"

def test_no_missing_values(data):
    assert data.isnull().sum().sum() == 0

def test_target_values(data):
    # Label values as per CSV
    y = data.iloc[:, -1]
    assert set(y.unique()) <= set(["setosa", "versicolor", "virginica"])
