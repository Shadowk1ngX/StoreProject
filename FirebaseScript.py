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

# Function to GrabOneItem
def GrabOneItem(CollectionName, DocumentID):
    try:
        print("Grabbing One Item")
        doc_ref = db.collection(CollectionName).document(DocumentID)
        doc = doc_ref.get()
        if doc.exists:
            print(f"Document data: {doc.to_dict()}")
        else:
            print("No such document!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Testing the function GrabOneItem
print("Testing GrabOneItem")
GrabOneItem('products', 'DOCUMENT_ID')  

# Function to add a new document
def AddItem(CollectionName, data):
    try:
        doc_ref = db.collection(CollectionName).add(data)
        print(f"Document added with ID: {doc_ref[1].id}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Testing Adding a new document
AddItem('products', {'name': 'New Product', 'price': 99.99, 'stock': 20})

# Function to delete a document
def DeleteItem(CollectionName, document_id):
    try:
        doc_ref = db.collection(CollectionName).document(document_id)
        doc_ref.delete()
        print(f"Document with ID: {document_id} deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Testing Deleting a document
DeleteItem('products', 'DOCUMENT_ID')

# Function to modify a document
def ModifyItem(CollectionName, document_id, update_data):
    try:
        doc_ref = db.collection(CollectionName).document(document_id)
        doc_ref.update(update_data)
        print(f"Document with ID: {document_id} updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Testing Modifying an existing document
ModifyItem('products', 'DOCUMENT_ID', {'price': 89.99, 'stock': 15})




#Note: Replace 'DOCUMENT_ID' with the actual ID of the document you want to retrieve, add, delete, mod