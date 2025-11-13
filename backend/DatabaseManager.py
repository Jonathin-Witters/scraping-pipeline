import firebase_admin
from firebase_admin import firestore, credentials
from Article import Document

cred = credentials.Certificate("firebased-adminsdk.json")
firebase_admin.initialize_app(cred)


if not firebase_admin._apps:
    firebase_admin.initialize_app()

class DatabaseManager:
    def __init__(self):
        self.db = firestore.client()
        self.collection = self.db.collection("articles")

    def add_article(self, article: Document):
        data = article.to_json()
        doc_id = article.title

        # Upload to Firestore
        self.collection.document(doc_id).set(data)

        print(f"Article '{article.title}' uploaded successfully")

    def get_article(self, title: str) -> Document | None:
        doc_id = title.replace("/", "_")
        doc = self.collection.document(doc_id).get()

        if doc.exists:
            return Document.from_json(doc.to_dict())
        else:
            print(f"Article '{title}' not found")
            return None