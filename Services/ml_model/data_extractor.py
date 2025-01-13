from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from global_logger import global_logger


def extract_features(data):
    text_data = [
        obj.get("description", "")
        for doc in data if isinstance(doc, dict) and "unified_schema" in doc
        for obj in doc["unified_schema"] if isinstance(obj, dict) and obj.get("description")
    ]

    if not text_data:
        raise ValueError("No valid text data found in the documents.")

    vectorizer = TfidfVectorizer(
        min_df=1,
        stop_words=None,
        ngram_range=(1, 2)
    )

    vectorizer.fit(text_data)
    unique_terms = vectorizer.get_feature_names_out()

    max_features = min(100, len(unique_terms))
    vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=(1, 2))
    feature_matrix = vectorizer.fit_transform(text_data).toarray()

    global_logger.info(f"Feature matrix shape: {feature_matrix.shape}")

    return feature_matrix, vectorizer
