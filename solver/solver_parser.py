import json

def parseJSON(my_json):

    data = json.loads(my_json)

    #obtaining the different subsets
    id_problem = data['id_problem']
    students_json = data['students']
    topics = data['topics']
    global_constraints = data['global_constraints']
    
    students = [] #Tableau de tuples avec des tuples de forme: ('étudiant',[vecteur des choix/pénalités])

    #remplissage du tableau
    for key in students_json:
        students.append((key,students_json[key])) 

    return [id_problem,students, topics, global_constraints]