import pyrebase


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

        result = self.database.child("circles").child("drones").get()

        self.all_targets = []

        try:
            drone_nr = len(result.val())
            self.drone_nr = drone_nr
        except:
            self.drone_nr = "0"

        self.publish_telemetry(0, 0, 0)
        self.stream = self.database.child("circles").child("targets").stream(self.stream_handler)

    def stream_handler(self, message):
        result = self.database.child("circles").child("targets").get()
        self.all_targets = result.val()
        print("New Target acquired!")

    def publish_telemetry(self, lat, lon, alt):
        data = {
            'altitude': alt,
            'latitude': lat,
            'longitude': lon
        }
        self.database.child("circles").child("drones").child(self.drone_nr).child("telemetry").set(data)

    def update_target(self, index, eliminated):
        self.database.child("circles").child("targets").child(str(index)).child("eliminated").set(eliminated)

    def close(self):
        self.stream.close()

