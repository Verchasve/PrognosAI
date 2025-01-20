import pickle
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pymongo
# Load your pretrained model and vectorizer
with open("../models/resolution_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("../models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

MONGO_URI = "mongodb://localhost:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["saas_integration"]
normalized_data = list(db["sanitized_data"].find())
ticket_ids = [doc["eid"] for doc in normalized_data]
resolutions = [doc["resolution"] for doc in normalized_data]
description_vectors = vectorizer.transform([doc["description"] for doc in normalized_data])

class ActionPredictTicket(Action):
    def name(self) -> str:
        return "action_predict_ticket"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> list:
        # Extract the user's message
        user_message = tracker.latest_message.get("text")

        # Vectorize the user's message
        user_vector = vectorizer.transform([user_message])

        # Predict status
        numerical_features = np.array([[2, 5.0]])  # Placeholder for priority and time_to_resolve
        categorical_features = np.array([[0]])  # Placeholder for type
        X_new = np.hstack([numerical_features, categorical_features, user_vector.toarray()])

        predicted_status = model.predict(X_new)
        status = "Resolved" if predicted_status[0] == 1 else "Unresolved"  # Example mapping

        # Find similar tickets
        similarities = cosine_similarity(user_vector, description_vectors).flatten()
        top_indices = np.argsort(similarities)[::-1][:3]

        similar_tickets = [
            {
                "ticket_id": ticket_ids[i],
                "similarity_score": similarities[i],
                "resolution": resolutions[i],
            }
            for i in top_indices
        ]

        # Respond with the prediction and suggestions
        response = f"The predicted status is: {status}\n\nSimilar tickets and resolutions:\n"
        for ticket in similar_tickets:
            response += (
                f"- Ticket ID: {ticket['ticket_id']}, Similarity: {ticket['similarity_score']:.2f}\n"
                f"  Resolution: {ticket['resolution']}\n"
            )

        dispatcher.utter_message(response)
        return []


def predict_and_suggest(new_ticket):
    # Preprocess the new ticket
    new_ticket_vector = vectorizer.transform([new_ticket["description"]])
    
    try:
        # Convert the priority to numerical value using the mapping
        priority_mapping = {
            "Low": 1,
            "Medium": 2,
            "High": 3,
            "Critical": 4
        }
        priority_value = priority_mapping[new_ticket["priority"]]
        numerical_features = np.array([[priority_value, new_ticket["time_to_resolve"]]])
        categorical_features = np.array([[le_type.transform([new_ticket["type"]])[0]]])
    except ValueError as e:
        print(f"Error transforming new ticket values: {e}")
        return None, None
    
    X_new = hstack([numerical_features, categorical_features, new_ticket_vector])

    # Predict the status
    try:
        predicted_status = model.predict(X_new)
        predicted_status_label = le_status.inverse_transform(predicted_status)[0]
    except ValueError as e:
        print(f"Error predicting status: {e}")
        return None, None

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