from flask import Flask, jsonify, request, send_file, send_from_directory, abort
from mimetypes import MimeTypes
import os
import sys
import json

sys.path.append('./solver') #Permet aux scripts dans /solver d'utiliser les scripts du repertoire parent et inversement

from distribution import assignment_desire
from penality import assignment_penalty
from solver_parser import parseJSON
from solver_encoder import encodeResult

UPLOAD_DIRECTORY = "solver/uploads/"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = Flask(__name__)
app.config.from_pyfile('settings.py')

@app.route('/')
def index():
    return "Welcome to Cyrovini's Solver !"

@app.route('/key/')
def getKey():
    return f'API_KEY = {app.config.get("API_KEY")}'

@app.route('/solve/repartition/', methods=['POST'])
def solveRepartition():
    [result,code] = assignment_desire(request.data)
    if code == -1:
        return jsonify(result),400
    return result
        
@app.route('/solve/penality/', methods=['POST'])
def solvePenality():
    [result,code] =  assignment_penalty(request.data)
    if code == -1:
        return jsonify(result),400
    return result

@app.route('/download/<id_problem>/')
def download_file_pb(id_problem):
    problem_file = f'prob_{str(id_problem)}.lp'
    if os.path.isfile(os.path.join(UPLOAD_DIRECTORY,problem_file)):
        return send_from_directory(UPLOAD_DIRECTORY,problem_file,as_attachment=True)
    else:
        return {"prob_" + str(id_problem):"This file doesn't exist"}

if __name__ == "__main__":
    app.run(debug=True)