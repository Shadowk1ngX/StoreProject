import firebase_admin as fba
from firebase_admin import firestore

# Initialize Firebase Admin SDK with default credentials
if not fba._apps:
    app = fba.initialize_app()  # Automatically uses Google Cloud default credentials

# Firestore client
db = firestore.client(app)

# Function to grab all items from a Firestore collection
def GrabAllItems(CollectionName):
    print("Grabbing All Items")
    docs = db.collection(CollectionName).stream()
    print("Stream Started")
    DocList = []

    print("Insert Data")
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id
        doc_data["data"] = doc._data
        DocList.append(doc_data)

    print("Show Data")
    for doc_data in DocList:
        print(f"Document ID: {doc_data['id']}")
        print(f"Document Data: {doc_data['data']}")
        print()

# Function to grab all items using the `.get()` method
def GrabAllItems2(CollectionName):
    try:
        print("Grabbing All Items")
        docs = db.collection(CollectionName).get()
        print("Documents Retrieved")
        DocList = []

        print("Insert Data")
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data["id"] = doc.id
            DocList.append(doc_data)

        print("Show Data")
        for doc_data in DocList:
            print(f"Document ID: {doc_data['id']}")
            print(f"Document Data: {doc_data}")
            print()

    except Exception as e:
        print(f"An error occurred: {e}")

# Test function
GrabAllItems2("products")
print("RAN")
