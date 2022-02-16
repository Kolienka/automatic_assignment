import re

def generate_results(topic_per_student,students_list,topics_list,model):

    result = {} #Dictionnaire contenant les résultats

    if topic_per_student > 1:
        for student in students_list: #Données de sortie sous la forme étudiant: liste de sujets
            result[student] = []
    else: 
        for topic in topics_list: #Données de sortie sous la forme sujet: étudiants afféctés
            result[topic] = []

    for v in model.variables():
        try:
            if v.value() != 0 and re.compile('X_e_\d+_s_\d+').match(v.name): #Expression régulière correspondant au format X_élève_numéroEtudiant_s_numeroDeSujet
                res = v.name.split("_")
                if topic_per_student == 1: #Format groupe:[étudiants dans le groupe]
                    result[topics_list[int(res[4])-1]].append(students_list[int(res[2])-1])
                else: #Format étudiant:[sujet assignés]
                    result[students_list[int(res[2])-1]].append(topics_list[int(res[4])-1])
        except:
            print("error, couldnt find value")

    return result