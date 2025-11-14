import firebase_admin
from firebase_admin import firestore, credentials

# Initialize Firebase Admin (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate("./newsScraping/firebased-adminsdk.json")
    firebase_admin.initialize_app(cred)

class DatabaseManager:
    def __init__(self):
        self.client = firestore.client()
        self.collection = self.client.collection('articles')

    def save_article(self, json_data):
        self.collection.document(json_data["title"]).set(json_data)