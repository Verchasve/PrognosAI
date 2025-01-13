import pickle
from global_logger import global_logger
# Define the mapping from numerical labels to text labels
label_mapping = {
    0: "No match",
    1: "Bug/Defect",
    2: "Feature",
    3: "User",
    4: "Incident",
    5: "Crypto"
}

 

# Example new data
new_data = [
    "Can you fix this bug in the code?",
    "I need a new feature in the app.",
    "The user interface is not user-friendly.",
    "This incident is critical.",
    "The project involves cryptocurrency.",
]

def load_pickle_file(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)

def log_vectorizer_info(vectorizer, terms):
    global_logger.info("Vectorizer vocabulary:")
    global_logger.info(vectorizer.get_feature_names_out())
    for term in terms:
        global_logger.info(f"'{term}' in vocabulary: {term.lower()  in vectorizer.get_feature_names_out()}")

def transform_and_predict(model, vectorizer, data):
    transformed_data = vectorizer.transform(data)
    global_logger.info("Transformed feature vectors (sparse matrix):")
    global_logger.info(transformed_data)
    global_logger.info("Transformed feature vectors (dense array):")
    global_logger.info(transformed_data.toarray())
    predictions = model.predict(transformed_data)
    return predictions

def main():
    model = load_pickle_file("resolution_model.pkl")
    vectorizer = load_pickle_file("vectorizer.pkl")
    global_logger.info("Model and vectorizer loaded successfully.")
    
    new_terms = [ "Bug", "Defect", "Feature", "Incident", "Crypto"]
    log_vectorizer_info(vectorizer, new_terms)
    
    predictions = transform_and_predict(model, vectorizer, new_data)
    global_logger.info(f"Predictions: {predictions}")
    
    text_predictions = [label_mapping[pred] for pred in predictions]
    for text, label in zip(new_data, text_predictions):
        print(f"Text: {text}\nPredicted Label: {label}\n")

if __name__ == "__main__":
    main()
