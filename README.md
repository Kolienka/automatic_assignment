# Welcome to Cyrovini's solver !

Voici la partie du projet permettant d'affecter les étudiants d'une manière **automatique** à des sujets par le biai de l'optimisation linéaire

# Flask API

## Pour le moment, 5 requêtes sont disponibles quand le serveur est lancé

### `http://localhost:1234/` 
Il s'agit de la requête "indexe", elle retourne `Welcome to Cyrovini's solver !`

### `http://localhost:1234/key` 
Cette requête permet de récupérer la clé de l'API

### `http://localhost:1234/solve/penality`
Il s'agit d'une requête "Post" permettant d'appeller les scripts utilisant Pulp et faisant appel au solveur tout en envoyant les données nécéssaires à la génération du modèle et à la résolution du problème. Les données sont envoyer sous format JSON et expriment les étudiants ainsi que les pénalités qu'ils ont pour chaque projet, l'ensemble des projets et des contraintes associées et enfin les contraintes globales s'appliquant à chaque étudiant et/ou projet. 

Voici un exemple de donnée en entrée :

```json
{	
	"id_problem": 1,
    	"students":{
		"Romain":[0,1,2,4],
		"Nicolas":[1,0,2,4],
		"Remi":[1,2,0,4],
		"Guillaume":[1,2,2,0],
		"Sylvain":[1,2,2,0],
		"Lucas":[1,2,2,0],
		"Tanguy":[1,2,2,0],
		"Miguel":[2,0,4,1],
		"Geoffrey":[4,1,0,2],
		"George":[0,1,4,2]
    	},
    	"topics": {
      		"Affectations": {
			"grp_min" : 0,
			"grp_max" : 2,
			"grp_size_min" : 2,
			"grp_size_max" : 3
        	},
		"GreenIT": {
		  "grp_min" : 0,
		  "grp_max" : 2,
		  "grp_size_min" : 2,
		  "grp_size_max" : 3
		},
	      "iPhone" :{
		"grp_min" : 0,
		"grp_max" : 2,
		"grp_size_min" : 2,
		"grp_size_max" : 3
		},
	      "Alumni": {
		"grp_min" : 0,
		"grp_max" : 2,
		"grp_size_min" : 2,
		"grp_size_max" : 3}
		},
    "global_constraints":{
      "topic_per_student" : 2,
      "team_size" : 1,
      "different_topics_min" : 3,
      "different_topics_max" : 4
      }
}
```
La section "students" donne des pairs noms (ou id) / tableau, les tableaux expriment les pénalités de l'étudiant pour chaque sujet.
Pour exemple, l'étudiant "Romain" n'a pas de pénalité pour le sujet "Affectations" a une pénalité de 1 pour "GreenIT", de 2 pour "iPhone" etc... Le but est ici est de réaliser une affectation automatique tout en minimisant la pénalité globale.

la section "topics" donne le nom des sujets et exprime toutes les contraintes qui y sont associées.
Par exemple pour le sujet "Affectation", il peut y avoir entre 0 et 2 groupes et chaque groupe peut avoir entre 2 et 3 membres.

Pour finir, la section "global_constraints" exprime des contraintes générales à appliquer sur tous les étudiants et/ou sujets, pour le moment les contraintes globales sont le nombre de sujets que doit avoir un étudiant après la résolution, la taille des équipes, et le nombre minimum et maximum de sujets différents devant être assignés.

Si la résolution est possible et que le nombre de sujets assigné à chaque étudiant est plus grand que 1, alors en retour les scripts renveront des données sous format JSON donnant chaque étudiant et chaque sujets auxquels il est affécté ainsi que quelques statistiques associées à la résolution. Voici un exemple de données sortantes avec l'entrée précédente : 

```json
{
  "Romain": [
    "Affectations",
    "GreenIT"
  ],
  "Nicolas": [
    "Affectations",
    "GreenIT"
  ],
  "Remi": [
    "Affectations",
    "GreenIT"
  ],
  "Guillaume": [
    "Affectations",
    "Alumni"
  ],
  "Sylvain": [
    "Affectations",
    "Alumni"
  ],
  "Lucas": [
    "Affectations",
    "Alumni"
  ],
  "Tanguy": [
    "Affectations",
    "Alumni"
  ],
  "Miguel": [
    "GreenIT",
    "Alumni"
  ],
  "Geoffrey": [
    "GreenIT",
    "Alumni"
  ],
  "George": [
    "Affectations",
    "GreenIT"
  ],
  "stats": {
    "cpt_first_choice": 8,
    "cpt_second_choice": 10,
    "cpt_third_choice": 2,
    "cpt_other_choice": 0,
    "selected_topics": [
      "Alumni",
      "Affectations",
      "GreenIT"
    ],
    "unselected_topics": [
      "iPhone"
    ],
    "global_penalty": 14.0
  }
}
```
Sinon, si le nombre de sujets devant être assignés à chaque étudiant vaut 1, alors le format de sortie sera un peu différent et présentera les résultats sous format : sujet/étudiants afféctés :

```json
{
  "Affectations": [
    "George",
    "Romain",
    "Remi"
  ],
  "GreenIT": [
    "Nicolas",
    "Miguel",
    "Geoffrey"
  ],
  "iPhone": [],
  "Alumni": [
    "Guillaume",
    "Sylvain",
    "Lucas",
    "Tanguy"
  ],
  "stats": {
    "cpt_first_choice": 8,
    "cpt_second_choice": 2,
    "cpt_third_choice": 0,
    "cpt_other_choice": 0,
    "selected_topics": [
      "Affectations",
      "GreenIT",
      "Alumni"
    ],
    "unselected_topics": [
      "iPhone"
    ],
    "global_penalty": 2.0
  }
}
```

### `http://localhost:1234/solve/repartition/`
Il s'agit également d'une requête "Post". La requête fonctionne comme la précédente, cependant ici, les étudiants ne sont plus associés à des tableaux de pénalités mais à des tableaux de "satisfaction", le but est donc ici de réaliser l'affectation automatique en maximisant la satisfaction des étudiants. 

Voici un exemple de données en entrée:
```json
{	
	"id_problem":2,
    "students":{
       	"Romain":[3,2,1,0],
        "Nicolas":[2,3,1,0],
        "Remi":[2,1,3,0],
        "Guillaume":[1,0,0,3],
        "Sylvain":[1,0,0,3],
        "Lucas:":[1,0,0,3],
        "Tanguy":[1,0,0,3],
        "Miguel":[4,8,0,2],
        "Geoffrey":[4,1,0,2],
        "George":[0,1,4,2]
			},
      "topics": {
        "Affectations": {
          "grp_min" : 0,
          "grp_max" : 2,
          "grp_size_min" : 2,
          "grp_size_max" : 3
         },
         "GreenIT": {
          "grp_min" : 0,
          "grp_max" : 2,
          "grp_size_min" : 2,
          "grp_size_max" : 3
			},
      "iPhone" :{
        "grp_min" : 0,
        "grp_max" : 2,
        "grp_size_min" : 2,
        "grp_size_max" : 3
        },
      "Alumni": {
        "grp_min" : 0,
        "grp_max" : 2,
        "grp_size_min" : 2,
        "grp_size_max" : 3}
		},
    "global_constraints":{
      "topic_per_student" : 1,
      "team_size" : 1,
      "different_topics_min" : 3,
      "different_topics_max" : 4
     }
}
```
Voici les données en sortie: 

```json
{
  "Affectations": [
    "Romain",
    "Geoffrey"
  ],
  "GreenIT": [
    "Nicolas",
    "Miguel"
  ],
  "iPhone": [
    "George",
    "Remi"
  ],
  "Alumni": [
    "Guillaume",
    "Sylvain",
    "Lucas:",
    "Tanguy"
  ],
  "stats": {
    "cpt_first_choice": 0,
    "cpt_second_choice": 0,
    "cpt_third_choice": 0,
    "cpt_other_choice": 10,
    "selected_topics": [
      "Affectations",
      "GreenIT",
      "iPhone",
      "Alumni"
    ],
    "unselected_topics": [],
    "global_satisfaction": 37.0
  }
}
```

Dans les cas où la résolution n'est pas possible (suite à des incohérences dans les contraintes par exemple) les scripts python retournent un message d'erreur
```json
{
  "error": "Solving is not possible with input data, check constraints and input values."
}
```

### `http://localhost:1234/download/<id_problem>`

Cette dernière requête permet à l'aide d'un identifiant de problème de télécharger le fichier .lp du problème, ce fichier permet d'exprimer toutes les caractéristiques du problème.
