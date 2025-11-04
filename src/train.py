import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib # Using joblib for model serialization

# Configuration
DATA_PATH = "data/iris.csv"
MODEL_PATH = "models/model.pkl"

def load_data(path):
  df = pd.read_csv(path)
  # Ensure standard IRIS column names if using original format
  if len(df.columns) == 5:
    df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
  return df

def train_model(df):
  X = df.drop('species', axis=1)
  y = df['species']

  # Simple train-test split (optional, as DVC focuses on full dataset tracking)
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  model = RandomForestClassifier(n_estimators=100, random_state=42)
  model.fit(X_train, y_train)

  # Evaluate
  y_pred = model.predict(X_test)
  accuracy = accuracy_score(y_test, y_pred)
  print(f"Model trained. Accuracy: {accuracy:.4f}")

  return model

def save_model(model, path):
  joblib.dump(model, path)
  print(f"Model saved to {path}")

if __name__ == "__main__":
  df = load_data(DATA_PATH)
  model = train_model(df)
  save_model(model, MODEL_PATH)
