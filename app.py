from flask import Flask, request, abort, jsonify, json
#from models import *
##this package to enable cros
from config import Config
from flask_cors import CORS, cross_origin
import json
#firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from alert import alert

app = Flask(__name__)
app.config.from_object(Config)
##configure flask to use cros model
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# Use a service account
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


@app.route("/temp",methods=["POST"])
#@cross_origin()
def index():
    acc_data = request.json
    query = db.collection('users_patients').where('device_id', '==', acc_data["device_id"])
    docs = query.limit(1).stream()
    for doc in docs:
        patient_id = doc.id
        patient_name = doc.to_dict()["firstname"] +" "+doc.to_dict()["lastname"]
        #print(doc.to_dict())
    acc_data["patient_id"] = patient_id
    query = db.collection('accidents').add(acc_data)
    #get responsibles
    query = db.collection('responsibles').where('patients', 'array_contains', patient_id)
    docs = query.stream()
    resples_ids = []
    resples_emails = []
    resples_phones = []
    for doc in docs:
        print(doc.to_dict())
        resples_ids.append(doc.id)
        resples_emails.append(doc.to_dict()["email"])
        resples_phones.append(doc.to_dict()["phone"])
    notification = ""
    return app.response_class(
        response= json.dumps(acc_data),
        status=200,
        mimetype='application/json'
    ) 

if __name__ == "__main__":
    app.run(debug=True)

