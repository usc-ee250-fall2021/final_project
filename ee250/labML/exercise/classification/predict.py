import pickle
from flask import Flask,request
import json

clf = pickle.load(open('model.pickle','rb'))


app = Flask(__name__)

@app.route("/classify")
def hello_world():
    weight = float(request.args.get('w'))
    reflectance = float(request.args.get('r'))

    denomination = int(clf.predict([[reflectance,weight]])[0])
    #print(denomination)
    return json.dumps({"weight":weight, "reflectance":reflectance ,"denomination":denomination})
