# -*- coding:utf-8 -*-
import sys
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = Flask (__name__)
CORS(app)
# CORS(app, resources={r'*': {'origins': 'http://autobench-web.run.goorm.io/'}})
app.config['MONGO_DBNAME'] = 'autobench'
app.config['MONGO_URI'] = 'mongodb://localhost/autobench'
app.debug = True
mongo = PyMongo(app)

@app.route('/login', methods = ['POST'])
def login():
    _email = request.json['email']
    _password = request.json['password']
    if mongo.db.user.find_one({'email':_email}) == None:
        return jsonify(error='no user')
    else:
        data = mongo.db.user.find_one({'email':_email,'password':_password})
        if data == None:
            return jsonify(error='wrong password')
        else:
            data = {"username":data['username'],"email":data['email']}
            return jsonify(data)
    return jsonify(hello='world')

@app.route('/cpu')
def all_cpus():
    cpus = mongo.db.cpu.find()
    resp = dumps(cpus)
    return resp

@app.route('/cpu/<modelName>')
def cpu_model(modelName):
    cpu = mongo.db.cpu.find_one({'model_name': modelName})
    resp = dumps(cpu)
    return resp
        
@app.route('/gpu')
def all_gpus():
    gpus = mongo.db.gpu.find()
    resp = dumps(gpus)
    return resp

@app.route('/gpu/<modelName>')
def gpu_model(modelName):
    gpu = mongo.db.gpu.find_one({'model_name': modelName})
    resp = dumps(gpu)
    return resp

@app.route('/diskdrive')
def all_diskdrives():
    diskdrives = mongo.db.diskdrive.find()
    resp = dumps(diskdrives)
    return resp

@app.route('/diskdrive/<modelName>')
def drive_model(modelName):
    diskdrive = mongo.db.diskdrive.find_one({'model_name': modelName})
    resp = dumps(diskdrive)
    return resp

@app.route('/ram')
def all_rams():
    rams = mongo.db.ram.find()
    resp = dumps(rams)
    return resp

@app.route('/ram/<modelName>')
def ram_model(modelName):
    ram = mongo.db.ram.find_one({'model_name': modelName})
    resp = dumps(ram)
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(sys.argv[1]))
