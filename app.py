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


@app.route("/addAccident",methods=["POST"])
@cross_origin()
def index():
    acc_data = request.json
    if len(acc_data) > 1:
        data = acc_data
        query = db.collection('users_patients').where('device_id', '==', acc_data["device_id"])
        docs = query.limit(1).stream()
        for doc in docs:
            patient_id = doc.id
            patient_name = doc.to_dict()["firstname"] +" "+doc.to_dict()["lastname"]
        acc_data["patient_id"] = patient_id
        query = db.collection('accidents').add(acc_data)
        #get responsibles and store data in firestore
        query = db.collection('responsibles').where('patients', 'array_contains', patient_id)
        docs = query.stream()
        resples_ids = []
        resples_emails = []
        resples_phones = []
        resples_notfs = []
        warning_notification = patient_name + " maybe in danger situation ,temperature : "+ str(acc_data["temp"])
        danger_notification = patient_name + " is in danger situation , he fell down ,temperature : "+ str(acc_data["temp"])
        if data["down"] == 1:
            title = "Your Patient Fell Down"
            color = "#df4759"
            notification = danger_notification
        else:
            title = "Check The Situation Of Your Patient"
            color = "	#ffc107"
            notification = warning_notification
        for doc in docs:
            resples_ids.append(doc.id)
            notifications = doc.to_dict()["notifications"]
            notifications.append(notification)
            resples_notfs.append(notifications)
            resples_emails.append(doc.to_dict()["email"])
            resples_phones.append(doc.to_dict()["phone"])
        for re_id, res_notif in zip(resples_ids, resples_notfs):
            query = db.collection('responsibles').document(re_id).update({'notifications':res_notif})
        #notify the responsible in email and phone number
        for email in resples_emails:
            alert(title, notification, email, color)
        return app.response_class(
            response= json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    else:
        return app.response_class(
            response= json.dumps(acc_data),
            status=403,
            mimetype='application/json'
        ) 

@app.route("/login",methods=["POST"])
@cross_origin()
def login():
    data = request.json
    resp_ref = db.collection('responsibles')
    docs = resp_ref.where('email', '==', data["email"]).where('password', '==', data["password"]).stream()
    i = 0
    for doc in docs:
        i +=1
    if i == 0:
        print("NO users")
        data["response"] = "No"
    else:
        print("OK")
        data["response"] = "Ok"
    return app.response_class(
        response= json.dumps(data),
        status=200,
        mimetype='application/json'
    ) 

    

if __name__ == "__main__":
    app.run(debug=True)

