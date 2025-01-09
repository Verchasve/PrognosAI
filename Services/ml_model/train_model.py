import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import pymongo
from global_logger import global_logger
from data_extractor import extract_features
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline

# Explanation of Model Accuracy
# Accuracy Definition:

# Accuracy is a metric that measures the proportion of correctly predicted instances out of the total instances in the dataset.
# It is calculated as: [ \text{Accuracy} = \frac{\text{Number of Correct Predictions}}{\text{Total Number of Predictions}} ]
# Context in Your Code:

# X_test contains the features of the test dataset.
# y_test contains the true labels of the test dataset.
# model.score(X_test, y_test) evaluates the model's predictions on X_test and compares them to the true labels y_test.
# Interpretation:

# The returned value represents the proportion of test samples that the model correctly classified.
# For example, if the accuracy is 0.85, it means that the model correctly predicted 85% of the test samples.

# MongoDB Configuration
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["saas_integration"]

#  keywords ("bug", "defect", "feature", "user") to classify the tickets
 
#  Loading script
global_logger.info('Loading normalized data')

# Load normalized data 
normalized_data = list(db.normalized_data.find())
print(f"Number of documents: {len(normalized_data)}")
#print(f"Documents: {normalized_data}")

features, vectorizer = extract_features(normalized_data)
print(f"Number of features: {len(features)}")
print(f"Features: {features}") 

# Generate labels for each feature
# Generate labels for each feature
labels = []
for doc in normalized_data:
    if isinstance(doc, dict) and "unified_schema" in doc:
        for obj in doc["unified_schema"]:
            if isinstance(obj, dict):
                description = obj.get("description", "").lower()
                is_bug = "bug" in description or "defect" in description
                is_feature = "feature" in description
                is_user = "user" in description
                is_incident = "incident" in description
                is_crypto = "crypto" in description               
                if is_bug:
                    labels.append(1)
                elif is_feature:
                    labels.append(2)
                elif is_user:
                    labels.append(3)
                elif is_incident:
                    labels.append(4)
                elif is_crypto:
                    labels.append(5)                                        
                else:
                    labels.append(0)

print(f"Number of labels: {len(labels)}")
print(f"Labels: {labels}") 

# Ensure the number of labels matches the number of features
if len(labels) != len(features):
    raise ValueError(f"Inconsistent number of samples: {len(labels)} labels, {len(features)} features")

# Print label distribution
label_distribution = Counter(labels)
print("Label distribution:", label_distribution)

# Check if any class has fewer than 2 instances
min_class_count = min(label_distribution.values())
if min_class_count < 2:
    raise ValueError(f"The least populated class has only {min_class_count} member(s), which is too few for stratified splitting.")

# Ensure stratified split to maintain class distribution
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.5, random_state=42, stratify=labels)

print("Training set label distribution:", Counter(y_train))
print("Test set label distribution:", Counter(y_test))

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Calculate and print model accuracy
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Predict labels for the test set
predicted_labels = model.predict(X_test)

# Print predicted labels and true labels
print("Predicted labels:", predicted_labels)
print("True labels:", y_test)

# Print classification report with zero_division parameter
print("Classification Report: \n" ,classification_report(y_test, predicted_labels, zero_division=0))

pipeline = Pipeline([
    ('vectorizer', vectorizer),
    ('classifier', model)
])

# Save the pipeline
# with open("pipeline.pkl", "wb") as pipeline_file:
#     pickle.dump(pipeline, pipeline_file)
 


# Save model and vectorizer
with open("resolution_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("vectorizer.pkl", "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

print("Model and vectorizer saved successfully.")