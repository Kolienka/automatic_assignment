import os
import re
import numpy as np
import pulp as pl

from solver_parser import parseJSON
from results_management import generate_results
from stats_management import generate_stats
from solver_parser import parseJSON
from solver_encoder import encodeResult

UPLOAD_DIRECTORY = "solver/uploads/"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def assignment_desire(data):
    
    #Récupération des données en provenance du JSON
    [id_problem,students,topics,constraints] = parseJSON(data)

    #parametres
    grp_min = [] #Nombre de groupe minimal pour chaque projet
    grp_max = [] #Nombre de groupe maximal pour chaque projet
    grp_size_min = [] #Taille minimal d'un groupe pour chaque projet
    grp_size_max = [] #Taille maximal d'un groupe pour chaque projet
    team_size = constraints["team_size"] #Taille des équipes (1 = travail seul, 2 = binôme etc...)
    different_topics_min = constraints["different_topics_min"] #Nombre minimum de topics DIFFERENTS devant être assignés
    different_topics_max = constraints["different_topics_max"] #Nombre maximum de topics DIFFERENTS devant être assignés
    topics_list = [key for key in topics] #Liste des noms de sujets 
    students_list = [students[i][0] for i in range(len(students))] #Liste des étudiants
    n_students = len(students) #Nombre d'étudiants pour l'affectation
    n_topics = len(topics) #Nombre de sujets 
    topic_per_student = constraints['topic_per_student'] #Nombre de sujets auxquels chaque étudiant doit être affécté
    desire_matrice = [students[i][1] for i in range(n_students)] #Matrice des désires

    #Remplissage des vecteurs de paramètres de projets
    for key in topics:
        grp_min.append(topics[key]['grp_min'])
        grp_max.append(topics[key]['grp_max'])
        grp_size_min.append(topics[key]['grp_size_min'])
        grp_size_max.append(topics[key]['grp_size_max'])

    #Gestion des variables

    #Matrice des allocations (binaire)
    variables_names = ["e_" + str(i) + "_s_" + str(j) for i in range(1,n_students + 1) for j in range(1,n_topics + 1)]
    DV_variables = pl.LpVariable.matrix("X",variables_names,cat="Binary")
    isAllocated = np.array(DV_variables).reshape(n_students,n_topics)

    variables_names = [str(j) for j in range(1,n_topics + 1)]

    #Vecteur du nombre de groupe pour le sujet j
    nbGrp = pl.LpVariable.matrix("nGrp_s",variables_names,cat="Integer")
    #Vecteur du nombre d'équipes pour le sujet j
    nbTeam = pl.LpVariable.matrix("nTeam_s",variables_names,cat="Integer")
    #Nombre d'équipe en tout
    nbTeam_total = pl.LpVariable("nbTeam_total",cat="Integer")
    #Matrice (binaire) permettant de savoir si le sujet j est prit ou non
    pris = pl.LpVariable.matrix("pris",topics_list,cat="Binary")

    #Définition du modèle
    model = pl.LpProblem("Affectation-penalty-problem",pl.LpMaximize)

    #Fonction objective, on cherche à maximiser la satisfaction globale
    obj_func = pl.lpSum(desire_matrice*isAllocated)
    model += obj_func

    #Gestion des contraintes

    #Pour chaque étudiant i
    for i in range(n_students):
        #Le nombre de sujets assigné doit être égal à topic_per_student
        model += pl.lpSum(isAllocated[i][j] for j in range(n_topics)) == topic_per_student

    for j in range(n_topics):
        #Le nombre de groupes doit être supérieur au nombre minimum de groupe pour le projet
        model += pl.lpSum(nbGrp[j]) >= grp_min[j]
        #Le nombre de groupes doit être inférieur au nombre maximum de groupe pour le projet
        model += pl.lpSum(nbGrp[j]) <= grp_max[j]
        #Le nombre d'étudiants doit être inférieur au nombre de groupes pour le projet multiplié par
        #La taille maximale des groupes pour le projet
        model += pl.lpSum(isAllocated[i][j] for i in range(n_students)) <= nbGrp[j] * grp_size_max[j]
        #Le nombre d'étudiants doit être supérieur au nombre de groupes pour le projet multiplié par
        #La taille minimale des groupes pour le projet
        model += pl.lpSum(isAllocated[i][j] for i in range(n_students)) >= nbGrp[j] * grp_size_min[j]
        #Le nombre d'étudiants doit être égal au nombre d'équipes pour le projet multiplié par la taille des équipes
        model += pl.lpSum(isAllocated[i][j] for i in range(n_students)) == nbTeam[j] * team_size
        #Le nombre d'étudiants doit être égal au nombre total d'équipes multiplié par la taille des équipes
        model += n_students == nbTeam_total*team_size
        #Un projet est pris que si il a au moins un groupe
        model += pris[j] <= nbGrp[j]
        #Le nombre de groupe pour le projet est inférieur au nombre de groupes max pour le projet multiplié par 1 si le sujet est prit, 0 sinon
        model += pris[j] * grp_max[j] >= nbGrp[j]
        #Un projet est pris que si il a au moins une équipe
        model += pris[j] <= nbTeam[j]

    #Le nombre de sujet prit doit être plus petit que different_topics_min
    model += pl.lpSum(pris[j] for j in range(n_topics)) >= different_topics_min
    #Le nombre de sujet prit doit être plus grand que different_topics_max
    model += pl.lpSum(pris[j] for j in range(n_topics)) <= different_topics_max

#Write LP file
    model.writeLP(os.path.join(UPLOAD_DIRECTORY,"prob_" + str(id_problem) + ".lp"))

    #processing of results
    flag = model.solve(pl.PULP_CBC_CMD()) #Recupération du code de retour de la résolution, une valeur différente de 1 est le résultat d'un soucis lors de la résolution

    if flag != 1:
        return ({"error" : "Solving is not possible with input data, check constraints and input values."},flag)

    status = pl.LpStatus[model.status]

    #Récupératin des résultats
    results = generate_results(topic_per_student,students_list,topics_list,model)
    #Récupération des stats
    stats = generate_stats(topic_per_student,results,desire_matrice,students_list,topics_list,model,"distribution")

    #Mise des résultats sous bon format

    results = encodeResult(results,stats)

    return results