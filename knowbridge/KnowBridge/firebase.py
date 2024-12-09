import firebase_admin
from firebase_admin import credentials, initialize_app, firestore

def initialize_firebase():
    try:
        # Attempt to initialize the default Firebase app
        cred = credentials.Certificate(r"C:\Users\hp\knowbridge\education-49071-firebase-adminsdk-rer49-d652087061.json")
        default_app = initialize_app(cred, name='default')
        return firestore.client(default_app)
    except ValueError:
        # If the default app is already initialized, catch the error and return the existing app
        print("Default Firebase app already exists. Using the existing instance.")
        return firestore.client(firebase_admin.get_app('default'))

# Access Firestore client
db = initialize_firebase()
