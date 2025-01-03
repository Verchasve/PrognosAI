from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from data_extractor import extract_features
import pymongo
import json

# MongoDB Configuration
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["saas_integration"]

# Example training data
normalized_data = list(db.normalized_data.find())
print(f"Number of documents: {len(normalized_data)}")
print(f"Documents: {normalized_data}")

features, vectorizer = extract_features(normalized_data)
print(f"Number of features: {len(features)}")
print(f"Features: {features}")

# Generate labels for each feature
labels = [
    1 if isinstance(doc, dict) and "unified_schema" in doc and any("bug" in obj.get("description", "").lower() for obj in doc["unified_schema"] if isinstance(obj, dict)) else 0
    for doc in normalized_data for _ in doc["unified_schema"]
]
print(f"Number of labels: {len(labels)}")
print(f"Labels: {labels}")

# Ensure the number of labels matches the number of features
if len(labels) != len(features):
    raise ValueError(f"Inconsistent number of samples: {len(labels)} labels, {len(features)} features")

# Convert features to a list of strings for JSON serialization
features_list = [" ".join(map(str, feature)) for feature in features]

# Convert to Rasa NLU training data format
rasa_nlu_data = {
    "rasa_nlu_data": {
        "common_examples": [
            {
                "text": description,
                "intent": "report_bug" if label == 1 else "other",
                "entities": []
            }
            for description, label in zip(features_list, labels)
        ]
    }
}

# Save Rasa NLU training data to a file
with open('../data/nlu.json', 'w') as f:
    json.dump(rasa_nlu_data, f)

print("Rasa NLU training data generated and saved to data/nlu.json")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

print(f"Model Accuracy: {model.score(X_test, y_test)}")