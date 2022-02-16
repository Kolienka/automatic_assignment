import pytest
import os
import json

from solver_app import app as flask_app
from solver import solver_parser

def test_parseJSON():
    with open('tests/data_parse.json') as json_file:
        json_data = json.load(json_file)
    [id_test,students_test,topics_test,constraints_test] = solver_parser.parseJSON(json.dumps(json_data))
    #Conservation id
    assert id_test == 1
    #Conservation de tous les étudiants et sujets
    assert len(students_test) == 2
    assert len(topics_test) == 1
    #Conservation des contraintes
    assert constraints_test['topic_per_student'] == 15
    assert constraints_test['team_size'] == 20
    assert constraints_test['different_topics_min'] == 25
    assert constraints_test['different_topics_max'] == 30
    #Conservation des contraintes de projet
    assert topics_test['Affectations']['grp_min'] == 1
    assert topics_test['Affectations']['grp_max'] == 2
    assert topics_test['Affectations']['grp_size_min'] == 3
    assert topics_test['Affectations']['grp_size_max'] == 4
    #Conservation des étudiants et vecteurs désire/pénalité
    assert students_test[0] == ('Romain',[0,1,2,4])
    assert students_test[1] == ('Nicolas',[1,0,2,4])

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(app,client):
    res = client.get('/')
    assert res.status_code == 200
    expected = "Welcome to Cyrovini's Solver !"
    assert expected == res.get_data(as_text=True)

def test_getKey(app,client):
    res = client.get('/key/')
    assert res.status_code == 200
    expected = f'API_KEY = {app.config.get("API_KEY")}'
    assert expected == res.get_data(as_text=True)

def test_penalty_success(app,client):
    my_data = 'tests/data_succes.json'
    with open(my_data,'r') as f:
        res = client.post('/solve/penality/',data=f)
    assert res.status_code == 200
    assert str(type(res.get_data())) == "<class 'bytes'>"

def test_penalty_error(app,client):
    my_data = 'tests/data_error.json'
    with open(my_data,'r') as f:
        res = client.post('/solve/penality/',data=f)
    assert res.status_code == 200
    assert "error" in res.get_data(as_text=True)

def test_distribution_success(app,client):
    my_data = 'tests/data_succes.json'
    with open(my_data,'r') as f:
        res = client.post('/solve/repartition/',data=f)
    assert res.status_code == 200
    assert str(type(res.get_data())) == "<class 'bytes'>"

def test_distribution_error(app,client):
    my_data = 'tests/data_error.json'
    with open(my_data,'r') as f:
        res = client.post('/solve/repartition/',data=f)
    assert res.status_code == 200
    assert "error" in res.get_data(as_text=True)