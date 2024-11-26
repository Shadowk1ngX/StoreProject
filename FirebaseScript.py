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
    
    DocList = []

    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id
        doc_data['data'] =  doc._data
        DocList.append(doc_data)
    
    for doc_data in DocList:
        print(f"Document ID: {doc_data['id']}")
        print(f"Document Data: {doc_data['data']}")
        print()


#This is a test
GrabAllItems('products')
print("RAN")


def AddItem(CollectionName, data):
    try:
        # Add the document
        doc_ref = db.collection(CollectionName).add(data)
        print(f"Document added with ID: {doc_ref[1].id}")
    except Exception as e:
        print(f"An error occurred: {e}")

def DeleteItem(CollectionName, document_id):
    try:
        # Delete the document
        doc_ref = db.collection(CollectionName).document(document_id)
        doc_ref.delete()
        print(f"Document with ID: {document_id} deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def ModifyItem(CollectionName, document_id, update_data):
    try:
        # Update the document
        doc_ref = db.collection(CollectionName).document(document_id)
        doc_ref.update(update_data)
        print(f"Document with ID: {document_id} updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")








#grab one item function is left to do