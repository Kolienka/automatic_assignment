def generate_stats(topic_per_student,result,matrice,students_list,topics_list,model,mode):

    cpt_array = [0,0,0,0] #Contient respectivement, le nombre d'étudiants avec leur premier, deuxième, troisième, n-ème choix (avec n>=4)
    selected_topics = [] #Contient tous les sujets assignés
    unselected_topics = [] #Contient tous les sujets non assignés

    if topic_per_student == 1: #format sujet:[étudiants assignés]
        for key,value in result.items(): 
            for student in value: #Pour chaque étudiant affécté au sujet...
                choices_vector = list(matrice[students_list.index(student)]) #On récupère le vecteur choix de l'étudiant
                sorted_vector = sorted(choices_vector)#trié pour avoir les minimums à gauche/maximums à droite
                for i in range(3):
                    #On regarde si l'index du sujet attribué à l'étudiant est égal à l'index du sujet avec la moins/plus grosse pénalité
                    if mode == "penalty":
                        if topics_list.index(key) == choices_vector.index(sorted_vector[i]): 
                            cpt_array[i] += 1
                    elif mode == "repartition":
                        if topics_list.index(key) == choices_vector.index(sorted_vector[-1-i]):
                            cpt_array[i] += 1
        for key,value in result.items():
            #Si le tableau d'étudiants pour le sujet n'est pas vide
            if(value):
                selected_topics.append(key)
            else:
                unselected_topics.append(key)
    else: #format étudiant:[sujets assignés]
        for key,value in result.items():
            choices_vector = list(matrice[students_list.index(key)])
            sorted_vector = sorted(choices_vector)
            for i in range(3):
                for topic in value: #Pour chaque sujet de l'étudiant...
                    if mode == "penalty":
                        if topics_list.index(topic) == choices_vector.index(sorted_vector[i]):
                            cpt_array[i] += 1
                    elif mode == "repartition":
                        if topics_list.index(topic) == choices_vector.index(sorted_vector[-1-i]):
                            cpt_array[i] += 1
        for key,value in result.items():
            if(key):
                for topic in value:
                    selected_topics.append(topic)
            selected_topics = list(set(selected_topics))
            unselected_topics = list(set(topics_list) - set(selected_topics))
    
    cpt_array[3] = topic_per_student*len(students_list) - sum(cpt_array)
    
    stats = {
        "cpt_first_choice" : cpt_array[0],
        "cpt_second_choice" : cpt_array[1],
        "cpt_third_choice" : cpt_array[2],
        "cpt_other_choice" : cpt_array[3],
        "selected_topics" : selected_topics,
        "unselected_topics" : unselected_topics
    }

    if mode == "penalty":
        stats["global_penalty"] = model.objective.value()
    elif mode == "distribution":
        stats["global_satisfaction"] = model.objective.value()
    return stats