from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def extract_features(data):
    text_data = []
    for doc in data:
        if isinstance(doc, dict) and "unified_schema" in doc:
            for obj in doc["unified_schema"]:
                if isinstance(obj, dict):
                    description = obj.get("description", "")
                    if description:
                        text_data.append(description)

    # Filter out None values from text_data
    text_data = [text for text in text_data if text is not None]
    print(f"Filtered text data: {text_data}")

    if not text_data:
        raise ValueError("No valid text data found in the documents.")

    vectorizer = TfidfVectorizer(max_features=100)
    feature_matrix = vectorizer.fit_transform(text_data)
    feature_matrix = feature_matrix.toarray()
    print(f"Feature matrix shape: {feature_matrix.shape}")

    return feature_matrix, vectorizer
