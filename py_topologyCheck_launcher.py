# -*- coding: utf-8 -*-
### ENVIRONNEMENT DE TRAVAIL ###

## Chargement des librairies Pythons personnelles

from lib.py_topologyCheck_fonctions import topologyCheck

##Variables

# R�pertoire de l'environnement de travail"
workspace = "C:/Users/serries/Desktop/testControle_cours/"

# CSV
# Dossier du CSV
csv_folder = workspace + "csv/"
# Nom des CSV
csvObjet_file = csv_folder + "listObjet.csv"
csvFeature_file = csv_folder + "listFeature.csv"
csvRule_file = csv_folder + "listRule.csv"
csvRuleBDTopage = csv_folder + "listRuleBDTopage.csv"
csvGeometryFeature_file = csv_folder + "listGeometryFeature.csv"

# G�odatabase topologie
localisation = "0"
geodatabase_topage="Controle_Topage_" + localisation + ".gdb"

# Dataset source
dataset_source = "source"

# Dataset de la topo
dataset_topology="topology"

# Dataset de la géometrie
dataset_geometry="geometry"

# Fichier pour la reference spatiale de la geometrie
file_srid = "D:/ONEMA_GS/04_Produit/controleTopo/file/shape/TRONCON_COURS_EAU.SHP"

# Nom de la topologie
topology_name = "Topologie"
geometry_name = "Geometrie"


### LANCEMENT DES SCRIPTS ###

# Cr�ation de l'objet objets
topologyTopageCheck = topologyCheck()

# Cr�ation de la g�odatabase de traitement
#topologyTopageCheck.createFramework(workspace,geodatabase_topage,dataset_source,dataset_topology,dataset_geometry,file_srid)

# Ajout des fichiers � traiter dans le dataset source
#topologyTopageCheck.add_sourceFeatureFromCSV(workspace + geodatabase_topage + "/" + dataset_source + "/",csvFeature_file,file_srid)

# Ajout des donn�es � traiter dans le dataset topology
#topologyTopageCheck.add_topologyFeatureFromSourceDataset(topology_name,workspace + geodatabase_topage + "/" + dataset_source + "/",workspace + geodatabase_topage + "/" + dataset_topology + "/",csvFeature_file)

# V�rification de la topologie
#topologyTopageCheck.checkTopology(topology_name,workspace + geodatabase_topage + "/" + dataset_topology + "/",csvFeature_file,csvRule_file,csvRuleBDTopage)

# V�rification de la geometrie (continuité du réseau)
topologyTopageCheck.checkGeometry(geometry_name,workspace + geodatabase_topage + "/" + dataset_topology + "/",workspace + geodatabase_topage + "/" + dataset_geometry + "/",csvGeometryFeature_file)

#raw_input()
