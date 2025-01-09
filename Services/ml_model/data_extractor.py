from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def extract_features(data):
    text_data = []
    for doc in data:
        if isinstance(doc, dict) and "unified_schema" in doc:
            for obj in doc["unified_schema"]:
                if isinstance(obj, dict):
                    description = obj.get("description", "")
                    if description:  # Ensure description is not empty
                        text_data.append(description)

    # Filter out None values from text_data
    text_data = [text for text in text_data if text is not None]
    #print(f"Filtered text data: {text_data}")

    if not text_data:
        raise ValueError("No valid text data found in the documents.")

    # Print unique terms
    # vectorizer = TfidfVectorizer(
    #     min_df=1,              # Include terms appearing at least once
    #     stop_words=None,       # Avoid removing stopwords like "feature", "user"
    #     ngram_range=(1, 2)     # Capture single words and bi-grams
    # )

    vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 1))

    vectorizer.fit(text_data)
    unique_terms = vectorizer.get_feature_names_out()
    #print(f"Unique terms: {unique_terms}")
    #print(f"Number of unique terms: {len(unique_terms)}")

    # Adjust max_features based on the number of unique terms
    max_features = min(100, len(unique_terms))
    vectorizer = TfidfVectorizer(max_features=max_features)
    feature_matrix = vectorizer.fit_transform(text_data)
    feature_matrix = feature_matrix.toarray()
    print(f"Feature matrix shape: {feature_matrix.shape}")

    return feature_matrix, vectorizer