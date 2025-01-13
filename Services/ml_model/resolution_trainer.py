from sklearn.model_selection import train_test_split , GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import pandas as pd
import pickle
from scipy.sparse import hstack
from mongo_client import get_mongo_client, get_database
from global_logger import global_logger

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

global_logger.info('Training model started...')

# MongoDB Configuration
client = get_mongo_client()
db = get_database(client)


# Load normalized data
normalized_data = list(db["sanitized_data"].find()) 
global_logger.info(f"Sanitized collection documents: {len(normalized_data)}")


# Convert to DataFrame
df = pd.DataFrame(normalized_data)

# Handle missing values
df.fillna("", inplace=True)

# Preprocess text features
vectorizer = TfidfVectorizer(max_features=1000)
text_features = vectorizer.fit_transform(df["description"])

# Encode categorical features
le_priority = LabelEncoder()
df["priority"] = le_priority.fit_transform(df["priority"])

le_status = LabelEncoder()
df["status"] = le_status.fit_transform(df["status"])

le_type = LabelEncoder()
df["type"] = le_type.fit_transform(df["type"])

# Combine all features
numerical_features = df[["priority", "time_to_resolve"]].values
categorical_features = df[["type"]].values


features = hstack([numerical_features, categorical_features, text_features])
labels = df["status"]

global_logger.info(f"Features: {features}") 
global_logger.info(f"Labels: {labels}")  

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.5, random_state=42, stratify=labels)

# Hyperparameter tuning for RandomForestClassifier
# param_grid = {
#     'n_estimators': [100, 200, 300],
#     'max_depth': [None, 10, 20, 30],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4]
# }

# grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, n_jobs=-1, verbose=2)
# grid_search.fit(X_train, y_train)


# # Best model from grid search
# model = grid_search.best_estimator_

# Train RandomForest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Calculate and print model accuracy
accuracy = model.score(X_test, y_test) 
global_logger.info(f"Model Accuracy: {accuracy * 100:.2f}%") 


# Predict labels for the test set
predicted_labels = model.predict(X_test)

# Print predicted labels and true labels

global_logger.info(f"Predicted labels: {predicted_labels}")  
global_logger.info(f"True labels: {y_test}")  


# Print classification report with zero_division parameter
global_logger.info(f"Classification Report: \n {classification_report(y_test, predicted_labels, zero_division=0)}")   
 

# Save the model and vectorizer
with open("trained_model/resolution_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("trained_model/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

global_logger.info(f"Model and vectorizer saved successfully.")
