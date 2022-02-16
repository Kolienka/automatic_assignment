from collections import defaultdict
from flask import jsonify
import json

def encodeResult(dic,stats):
    if "error" not in dic:
        affectations = dic
        affectations['stats'] = stats
        return json.dumps(affectations),1
    return json.dumps(dic),-1