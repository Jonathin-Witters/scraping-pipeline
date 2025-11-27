import firebase_admin
from firebase_admin import firestore, credentials

# Initialize Firebase Admin (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate("./newsScraping/firebased-adminsdk.json")
    firebase_admin.initialize_app(cred)

class DatabaseManager:
    def __init__(self):
        self.client = firestore.client()
        # self.collection = self.client.collection('articles') // Previously used as single collection
        self.vrtnws_collection = self.client.collection('vrtnws')
        self.demorgen_collection = self.client.collection('demorgen')
        self.destandaard_collection = self.client.collection('destandaard')
        self.nieuwsblad_collection = self.client.collection('nieuwsblad')
        self.hbvl_collection = self.client.collection('hbvl')

    def save_article(self, json_data):
        # self.collection.document(json_data["title"]).set(json_data) // Previously used as single collection
        match json_data["source"]:
            case "VRT NWS":
                self.vrtnws_collection.document(json_data["title"]).set(json_data)
            case "De Morgen":
                self.demorgen_collection.document(json_data["title"]).set(json_data)
            case "De Standaard":
                self.destandaard_collection.document(json_data["title"]).set(json_data)
            case "Nieuwsblad":
                self.nieuwsblad_collection.document(json_data["title"]).set(json_data)
            case "HBVL":
                self.hbvl_collection.document(json_data["title"]).set(json_data)