from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
from mongo_client import get_mongo_client, get_database
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import hstack
from global_logger import global_logger


# Load the model and vectorizer
with open("trained_model/resolution_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("trained_model/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# MongoDB Configuration
client = get_mongo_client()
db = get_database(client)

global_logger.info('Prediction model started...')

# Precompute vectorized descriptions for similarity search
normalized_data = list(db["sanitized_data"].find())
ticket_ids = [doc["eid"] for doc in normalized_data]
resolutions = [doc["resolution"] for doc in normalized_data]
description_vectors = vectorizer.transform([doc["description"] for doc in normalized_data])

# Fit label encoders
le_priority = LabelEncoder()
le_priority.fit([doc["priority"] for doc in normalized_data])

le_type = LabelEncoder()
le_type.fit([doc["type"] for doc in normalized_data])

le_status = LabelEncoder()
le_status.fit([doc["status"] for doc in normalized_data])

# Debugging: Print the classes of the label encoders
global_logger.info(f"Priority classes: {le_priority.classes_}") 
global_logger.info(f"Type classes: {le_type.classes_}") 
global_logger.info(f"Status classes: {le_status.classes_}") 
 

# Create a mapping for priority values
priority_mapping = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4
}

# Predict and suggest resolutions
def predict_and_suggest(new_ticket):
    # Preprocess the new ticket
    new_ticket_vector = vectorizer.transform([new_ticket["description"]])
    
    # the new ticket values 
    global_logger.info(f"New ticket priority: {new_ticket['priority']}")
    global_logger.info(f"New ticket type: {new_ticket['type']}")
    
    try:
        # Convert the priority to numerical value using the mapping
        priority_value = priority_mapping[new_ticket["priority"]]
        numerical_features = np.array([[priority_value, new_ticket["time_to_resolve"]]])
        categorical_features = np.array([[le_type.transform([new_ticket["type"]])[0]]])
    except ValueError as e:
        print("Error transforming new ticket values:", e)
        return None, None
    
    X_new = hstack([numerical_features, categorical_features, new_ticket_vector])

    # Predict the status
    predicted_status = model.predict(X_new)
    predicted_status_label = le_status.inverse_transform(predicted_status)[0]

    # Find similar tickets
    similarities = cosine_similarity(new_ticket_vector, description_vectors).flatten()
    top_indices = np.argsort(similarities)[::-1][:3]
    similar_tickets = [
        {
            "ticket_id": ticket_ids[i],
            "similarity_score": similarities[i],
            "suggested_resolution": resolutions[i]
        }
        for i in top_indices
    ]

    return predicted_status_label, similar_tickets

# Example usage
new_ticket = {
    "description": "There is a big in the dashboard when I try to filter the data.",
    "priority": "High",
    "time_to_resolve": 48,
    "type": "Bug"
}

predicted_status, suggestions = predict_and_suggest(new_ticket)
if predicted_status and suggestions: 
    global_logger.info(f"Predicted Status: {predicted_status}") 
    global_logger.info("Suggestions:")
    for suggestion in suggestions:
        print(suggestion)