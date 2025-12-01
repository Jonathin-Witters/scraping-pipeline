import firebase_admin
from firebase_admin import firestore, credentials
import datetime
import os

# Initialize Firebase Admin (only once)
if not firebase_admin._apps:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "firebased-adminsdk.json")
    cred = credentials.Certificate(path)

    firebase_admin.initialize_app(cred)

class DatabaseManager:

    class NoSuccessfulUpdatesError(Exception):
        """No available job was claimed."""
        pass

    def __init__(self):
        self.client = firestore.client()
        # self.collection = self.client.collection('articles') // Previously used as single collection
        self.vrtnws_collection = self.client.collection('vrtnws')
        self.demorgen_collection = self.client.collection('demorgen')
        self.destandaard_collection = self.client.collection('destandaard')
        self.nieuwsblad_collection = self.client.collection('nieuwsblad')
        self.hbvl_collection = self.client.collection('hbvl')
        self.telegraaf_collection = self.client.collection('telegraaf')
        self.gva_collection = self.client.collection('gva')
        self.devolkskrant_collection = self.client.collection('devolkskrant')
        self.jobs_collection = self.client.collection('jobs')

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
            case "Telegraaf":
                self.telegraaf_collection.document(json_data["title"]).set(json_data)
            case "GVA":
                self.gva_collection.document(json_data["title"]).set(json_data)
            case "De Volkskrant":
                self.devolkskrant_collection.document(json_data["title"]).set(json_data)

    def get_work_batch(self, size):
        jobs = self.jobs_collection
        current_time = datetime.datetime.utcnow()
        # jobs that have NOT been updated in the last 1 hour
        cutoff = current_time - datetime.timedelta(hours=1)
        query = jobs.where("lastUpdate", "<=", cutoff).limit(size)
        docs = query.get()

        if not docs:
            return []

        results = []
        for doc in docs:
            try:
                # Update the job's lastUpdate to the current time so it's marked as worked on now
                doc.reference.update({"lastUpdate": current_time})
            except Exception:
                continue

            results.append(doc.id)

        # If there were available jobs but nothing is claimed
        if not results:
            raise DatabaseManager.NoSuccessfulUpdatesError(
                "Found jobs but none could be updated"
            )

        return results