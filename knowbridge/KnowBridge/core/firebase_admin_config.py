import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate("C:\\Users\\kshra\\knowbridge\\knowbridge\\education-49071-firebase-adminsdk-rer49-e12e4b2c29.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
