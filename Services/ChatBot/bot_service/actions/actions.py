# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo

# MongoDB Configuration
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["saas_integration"]

class ActionFetchData(Action):
    def name(self) -> Text:
        return "action_fetch_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        api_name = tracker.get_slot("api_name")
        if not api_name:
            dispatcher.utter_message(text="No API name provided.")
            return []

        data = db.api_responses.find_one({"api_name": str(api_name)})

        if data:
            dispatcher.utter_message(text=f"Here is the data for API: {api_name} : \n {data['response_data'][0]}")
        else:
            dispatcher.utter_message(text=f"I couldn't data found for requested API: {api_name} you looking for.")
        return []

