# -*- coding:utf-8 -*-
import sys
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo

app = Flask (__name__)
app.config['MONGO_DBNAME'] = 'autobench'
app.config['MONGO_URI'] = 'mongodb://localhost/autobench'
app.debug = True
mongo = PyMongo(app)

@app.route('/cpu', methods = ['POST'])
def all_cpus():
  cpus = mongo.db.cpu.find()
  resp = dumps(cpus)
  return resp

@app.route('/gpu', methods = ['POST'])
def all_cpus():
  gpus = mongo.db.gpu.find()
  resp = dumps(gpus)
  return resp

@app.route('/diskdrive', methods = ['POST'])
def all_cpus():
  diskdrives = mongo.db.diskdrive.find()
  resp = dumps(diskdrives)
  return resp

@app.route('/ram', methods = ['POST'])
def all_cpus():
  rams = mongo.db.ram.find()
  resp = dumps(rams)
  return resp

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=int(sys.argv[1]))
