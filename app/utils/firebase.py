from firebase import firebase
import cloudinary


from app.utils.configFirebase import firebaseConfig

cloudinary.config(
    cloud_name="dd1tguut1",
    api_key="138692221655426",
    api_secret="nVrgyEMREeq8psKYsD5CAW8155g"
)

firebase_db = firebase.FirebaseApplication(firebaseConfig['databaseURL'], None)