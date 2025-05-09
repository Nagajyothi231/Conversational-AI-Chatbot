from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List

import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

import csv
import os

class ActionSearchFAISS(Action):
    def name(self) -> Text:
        return "action_search_faiss"

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.read_index("embeddings/faiss_index.index")
        with open("embeddings/metadata.json", "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        query = tracker.latest_message.get("text")
        query_vector = self.model.encode([query])
        D, I = self.index.search(np.array(query_vector).astype("float32"), 3)

        results = [self.metadata[i] for i in I[0] if i < len(self.metadata)]
        answer = "\n\n".join(
            f"📌 **{r['title']}**\n{r['text']}\n🔗 {r['url']}" for r in results
        )

        dispatcher.utter_message(text=answer or "Sorry, I couldn't find any relevant info.")

        return [SlotSet("last_user_query", query), SlotSet("last_bot_response", answer)]


class ActionCollectFeedback(Action):
    def name(self) -> Text:
        return "action_collect_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        feedback = tracker.get_slot("feedback")  # assume "positive" or "negative"
        query = tracker.get_slot("last_user_query")
        response = tracker.get_slot("last_bot_response")

        if feedback and query and response:
            self.save_feedback(query, response, feedback)
            dispatcher.utter_message(text="Thanks for your feedback! 🙏")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't record your feedback.")

        return []

    def save_feedback(self, query, response, feedback):
        file_path = "feedback.csv"
        file_exists = os.path.isfile(file_path)

        with open(file_path, mode="a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Query", "Response", "Feedback"])
            writer.writerow([query, response, feedback])
