# -*- coding: utf-8 -*-
### ENVIRONNEMENT DE TRAVAIL ###

## Chargement des librairies Pythons personnelles

from lib.py_topologyCheck_fonctions import topologyCheck

##Variables

# Répertoire de l'environnement de travail"
workspace = "C:/Users/serries/Desktop/testControle_cours/"

# CSV
# Dossier du CSV
csv_folder = workspace + "csv/"
# Nom des CSV
csvObjet_file = csv_folder + "listObjet.csv"
csvFeature_file = csv_folder + "listFeature.csv"
csvRule_file = csv_folder + "listRule.csv"
csvRuleBDTopage = csv_folder + "listRuleBDTopage.csv"

# Géodatabase topologie
localisation = "0"
geodatabase_topage="Controle_Topage_" + localisation + ".gdb"

# Dataset source
dataset_source = "source"
# Dataset de la topo
dataset_topology="topology"
# Dataset de la geometry
dataset_geometry="geometry"

# Fichier pour la reference spatiale de la geometrie
srid = 2154

# Nom de la topologie
topology_name = "Topologie"


### LANCEMENT DES SCRIPTS ###

# Création de l'objet objets
topologyTopageCheck = topologyCheck()

# Création de la géodatabase de traitement
topologyTopageCheck.createFramework(workspace,geodatabase_topage,dataset_source,dataset_topology,dataset_geometry,srid)

# Ajout des fichiers à traiter dans le dataset source
topologyTopageCheck.add_sourceFeatureFromCSV(workspace + geodatabase_topage + "/" + dataset_source + "/",csvFeature_file)

# Ajout des données à traiter dans le dataset topology
topologyTopageCheck.add_topologyFeatureFromSourceDataset(topology_name,workspace + geodatabase_topage + "/" + dataset_source + "/",workspace + geodatabase_topage + "/" + dataset_topology + "/",csvFeature_file)

# Vérification de la topologie
topologyTopageCheck.checkTopology(topology_name,workspace + geodatabase_topage + "/" + dataset_topology + "/",csvFeature_file,csvRule_file,csvRuleBDTopage)

#raw_input()
