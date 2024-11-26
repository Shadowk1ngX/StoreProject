import firebase_admin as fba
from firebase_admin import credentials, firestore

#Variables
cred = credentials.Certificate('Key.json')
if not fba._apps:
    app = fba.initialize_app(cred)
db = firestore.client(app)

def GrabAllItems(CollectionName):
    print("Grabbing All Items")
    docs = (
        db.collection(CollectionName)
        .stream()
    )
    print("Stream Started")
    DocList = []

    print("Insert Data")
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id
        doc_data['data'] =  doc._data
        DocList.append(doc_data)
    
    print("Show Data")
    for doc_data in DocList:
        print(f"Document ID: {doc_data['id']}")
        print(f"Document Data: {doc_data['data']}")
        print()

def GrabAllItems2(CollectionName):
    
    try:
        # Use get() to fetch the documents
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
   
#This is a test
GrabAllItems2('products')
print("RAN")
