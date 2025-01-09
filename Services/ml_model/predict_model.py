import pickle

# Load the model and vectorizer
with open("resolution_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# print("Vectorizer vocabulary:", vectorizer.get_feature_names_out())

# Load the pipeline
# with open("pipeline.pkl", "rb") as pipeline_file:
#     pipeline = pickle.load(pipeline_file)
 

#vectorizer = pipeline.named_steps['vectorizer'] 
print("Model and vectorizer loaded successfully.")

# Print the vectorizer vocabulary
print("Vectorizer vocabulary:")
print(vectorizer.get_feature_names_out())

new_terms = ["bug", "feature", "crypto", "user"]
for term in new_terms:
    print(f"'{term}' in vocabulary: {term in vectorizer.get_feature_names_out()}")


# Example new data
new_data = [
    "This is a bug report",
    "Feature request for the crypto module",
    "User feedback on the latest update"
]

# Transform new data using the loaded vectorizer
new_features = vectorizer.transform(new_data)

# # Print the transformed features array
print("Transformed features array:")
print(new_features.toarray())

# print("New data transformed successfully.")

# # Make predictions on the new data
predictions = model.predict(new_features)

# Predict directly
#predictions = pipeline.predict(new_data)

new_features = vectorizer.transform(new_data)
print("Transformed feature vectors (sparse matrix):")
print(new_features)
print("Transformed feature vectors (dense array):")
print(new_features.toarray())



# Print the numerical predictions
print("Predictions:", predictions)

# Define the mapping from numerical labels to text labels
label_mapping = {
    0: "No match",
    1: "bug",
    2: "Feature",
    3: "User",
    4: "Incident",
    5: "Crypto"
}

# Convert numerical predictions to text labels
text_predictions = [label_mapping[pred] for pred in predictions]

# Print the text predictions
print("Text Predictions:", text_predictions)