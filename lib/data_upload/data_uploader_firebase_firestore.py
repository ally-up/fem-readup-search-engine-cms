import inspect
import json
import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore
from tqdm import tqdm
from tracking_decorator import TrackingDecorator


def load_private_key(script_path, firebase_private_key_file):
    cert_path = os.path.join(script_path, firebase_private_key_file)
    cred = credentials.Certificate(cert_path)
    return cred


def open_database_connection(cred, firebase_database_url, firebase_collection_name):
    firebase_admin.initialize_app(cred, {"databaseURL": firebase_database_url})
    db = firestore.client()
    coll_ref = db.collection(firebase_collection_name)
    return coll_ref


def delete_collection(logger, coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        logger.log_line(f'Deleting document {doc.id}')
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(logger, coll_ref, batch_size)


def upload_data(results_path):
    """Uploads data to Firebase Firestore"""

    # Iterate over markdown files
    for file_path in tqdm(iterable=list(Path(results_path).rglob("*.json")), unit="file", desc="Upload json files"):
        file_name = os.path.basename(file_path)
        file_base_name = file_name.replace(".json", "")

        with open(file_path, "r") as json_file:
            db = firestore.client()
            db.collection(u'fundings').document(file_base_name).set(json.load(json_file))


#
# Main
#

class FirebaseFirestoreUploader:

    @TrackingDecorator.track_time
    def run(self, logger, results_path, clean=False):
        # Set script path
        script_path = os.path.dirname(__file__)

        # Make results path
        os.makedirs(results_path, exist_ok=True)

        # Set project specific parameters
        firebase_database_url = "https://klubtalent-5da84.firebaseio.com/"
        firebase_private_key_file = "klubtalent-5da84-firebase-adminsdk-dgd6r-54031355fe.json"
        firebase_collection_name = "fundings"

        # Load connection credentials
        cred = load_private_key(script_path, firebase_private_key_file)

        # Retrieve collection reference
        coll_ref = open_database_connection(cred, firebase_database_url, firebase_collection_name)

        # Clean results path
        if clean:
            delete_collection(logger, coll_ref, 128)

        # Upload data
        upload_data(results_path)

        class_name = self.__class__.__name__
        function_name = inspect.currentframe().f_code.co_name

        logger.log_line(class_name + "." + function_name + " finished")
