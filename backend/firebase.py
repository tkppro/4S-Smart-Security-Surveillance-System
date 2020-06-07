import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("./sproject-3697d-firebase-adminsdk-smiiq-ea6aea6b5c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sproject-3697d.firebaseio.com/'
})

def uploadRecord(recordObject):
    ref = db.reference('actions')
    ref.push(recordObject)
    return "Pushed data to firebase"
