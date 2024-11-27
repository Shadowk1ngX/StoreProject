import firebase_admin as fba
from firebase_admin import credentials, firestore

#Variables
cred = credentials.Certificate('Key.json')

if not fba._apps:
    app = fba.initialize_app(cred)
db = firestore.client(app)

def GetAllItems(CollectionName):
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
        DocList.append(doc_data['data'])
    
    #for doc_data in DocList:
    #    print(f"Document ID: {doc_data['id']}")
     #   print(f"Document Data: {doc_data['data']}")
    #    print()
    
    return DocList

def GetSingleItem(CollectionName,DocumentID):
    print("Grabbing Item")
    try:
        doc_ref = db.collection(CollectionName).document(DocumentID)
        doc = doc_ref.get()
        if doc.exists:
            print(f"Document data: {doc.to_dict()}")
            return doc.to_dict()  # Return the document data as a dictionary
        else:
            print(f"No document found with ID: {DocumentID}")
    except Exception as e:
        print(f"An error occurred: {e}")

def GetItemsByKey(CollectionName, Field, Value):
    """
    Retrieve all documents from a Firestore collection where a specific field equals a given value.

    :param CollectionName: The name of the Firestore collection.
    :param Field: The field name to filter by.
    :param Value: The value to match for the specified field.
    :return: A list of documents with their ID and data.
    """
    try:
        print(f"Querying collection '{CollectionName}' where '{Field}' == '{Value}'")
        query = db.collection(CollectionName).where(Field, "==", Value).stream()
        
        results = []
        for doc in query:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id  # Include document ID for reference
            results.append(doc_data)
            print(f"Document ID: {doc.id}, Data: {doc_data}")
        
        if not results:
            print(f"No documents found in '{CollectionName}' where '{Field}' equals '{Value}'")
        
        return results
    except Exception as e:
        print(f"An error occurred: {e}")
        return []



def AddItem(CollectionName, data: list):
    try:
        doc_ref = db.collection(CollectionName).add(data)
        print(f"Document added with ID: {doc_ref[1].id}")
    except Exception as e:
        print(f"Doc not created! An error occurred: {e}")

def DeleteItem(CollectionName, document_id):
    try:
        doc_ref = db.collection(CollectionName).document(document_id)
        doc_ref.delete()
        print(f"Document with ID: {document_id} deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to modify a document
def ModifyItem(CollectionName, document_id, update_data):
    try:
        doc_ref = db.collection(CollectionName).document(document_id)
        doc_ref.update(update_data)
        print(f"Document with ID: {document_id} updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


#This is a test
#GrabAllItems('products')
data = {
    "name" : "King",
    "age" : 18,
    "salary" : 30000
}

#AddItem("products", data)
#ModifyItem("products","sia4VT8h8W01X3AiNtT5",data)
#DeleteItem("products","sia4VT8h8W01X3AiNtT5")
#GetSingleItem("products","2Jr8e8jmTNWriQ0OubC6")
#GetItemsByKey("products","category","Electronics")

#grab one item function is left to do



