import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate("C:\\Users\\kshra\\knowbridge\\knowbridge\\education-49071-firebase-adminsdk-rer49-d652087061.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
