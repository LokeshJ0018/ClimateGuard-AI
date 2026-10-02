import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

print("🔥 CLIMATEGUARD AI - MODEL TRAINING")
print("=" * 50)

# ---------------------------------------
# 1. Load ML dataset
# ---------------------------------------

data_file = "data/processed/climateguard_training_data.csv"

print("\nLoading training dataset...")

data = pd.read_csv(data_file)

print(f"Total samples: {len(data):,}")

# ---------------------------------------
# 2. Select ML features
# ---------------------------------------

features = [
    "temperature_c",
    "relative_humidity",
    "precipitation_mm",
    "wind_speed_ms",
    "latitude_grid",
    "longitude_grid",
    "month",
    "day_of_year"
]

X = data[features]
y = data["fire"]

print("\nFeatures:")
for feature in features:
    print("-", feature)

print("\nClass distribution:")
print(y.value_counts())

# ---------------------------------------
# 3. Train/test split
# ---------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"\nTraining samples: {len(X_train):,}")
print(f"Testing samples: {len(X_test):,}")

# ---------------------------------------
# 4. Train Random Forest
# ---------------------------------------

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=20,
    min_samples_leaf=2,
    n_jobs=-1,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

print("Training completed! ✅")

# ---------------------------------------
# 5. Evaluate
# ---------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)

print("\n📊 MODEL PERFORMANCE")
print("=" * 40)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# ---------------------------------------
# 6. Feature importance
# ---------------------------------------

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
}).sort_values(
    "importance",
    ascending=False
)

print("\n🔥 FEATURE IMPORTANCE")
print(importance.to_string(index=False))

# ---------------------------------------
# 7. Save model
# ---------------------------------------

os.makedirs("models", exist_ok=True)

model_file = "models/climateguard_random_forest.pkl"

joblib.dump(
    {
        "model": model,
        "features": features
    },
    model_file
)

print("\n✅ MODEL SAVED")
print("Saved to:", model_file)