from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Example training data
training_data = [
    "There is a bug in the code.",
    "This feature is working as expected.",
    "The user interface needs improvement.",
    "This incident requires immediate attention.",
    "The project involves cryptocurrency.",
    # Add more training examples as needed
]

# Corresponding labels
training_labels = [1, 2, 3, 4, 5]

# Create and fit the vectorizer
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(training_data)

# Train the model
model = LogisticRegression()
model.fit(X_train, training_labels)

# Save the vectorizer and model
with open("vectorizer.pkl", "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

with open("resolution_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

print("Model and vectorizer retrained and saved successfully.")