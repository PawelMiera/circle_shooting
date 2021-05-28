import pyrebase
import os


class FirebaseConnection:
    def __init__(self):
        config = {
            "apiKey": "AIzaSyAglFX49k28WWJqS33SQEpct3kE_d3JDZs",
            "authDomain": "droniada-f604a.firebaseapp.com",
            "databaseURL": "https://droniada-f604a-default-rtdb.firebaseio.com",
            "projectId": "droniada-f604a",
            "storageBucket": "droniada-f604a.appspot.com",
            "messagingSenderId": "65160484994",
            "appId": "1:65160484994:web:f38e43420da263ba44bc9b"
        }

        self.firebase = pyrebase.initialize_app(config)

        self.storage = self.firebase.storage()

        self.database = self.firebase.database()

    def publish_target(self, lat, lon):
        result = self.database.child("circles").child("targets").get()

        try:
            number_id = len(result.val())
        except:
            number_id = "0"

        data = {
            'latitude': lat,
            'longitude': lon,
            'eliminated': 0,
        }
        self.database.child("circles").child("targets").child(number_id).set(data)

    def close(self):
        self.stream.close()


firebase = FirebaseConnection()

firebase.publish_target(51, 11)