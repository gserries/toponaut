# -*- coding: utf-8 -*-
### ENVIRONNEMENT DE TRAVAIL ###

## Chargement des librairies Pythons personnelles

from lib.py_geometryCheck_fonctions import geometryCheck

##Variables

# R�pertoire de l'environnement de travail"
workspace = "C:/Users/serries/Desktop/testControle_cours/"

# CSV
# Dossier du CSV
csv_folder = workspace + "csv/"
# Nom des CSV
csvGeometryFeature_file = csv_folder + "listGeometryFeature.csv"

# G�odatabase topologie
localisation = "0"
geodatabase_topage="Controle_Topage_" + localisation + ".gdb"

# Dataset de la topo
dataset_topology="topology"
# Dataset de la geometry
dataset_geometry="geometry"

# Fichier de la laisse
file_laisse = workspace + geodatabase_topage + "/" + dataset_topology + "/LandWaterBoundary_line"

# Nom de la g�om�trie
geometry_name = "Geometrie"


### LANCEMENT DES SCRIPTS ###

# Cr�ation de l'objet objets
geometryTopageCheck = geometryCheck()

# Import des fichiers concern�s par la g�om�trie
geometryTopageCheck.add_geometryFeatureFromTopologyDataset(geometry_name,workspace + geodatabase_topage + "/" + dataset_topology + "/", workspace + geodatabase_topage + "/" + dataset_geometry + "/", csvGeometryFeature_file)

# Cr�ation de la g�om�trie
geometryTopageCheck.create_geometry(geometry_name, workspace + geodatabase_topage + "/" + dataset_geometry + "/", csvGeometryFeature_file,file_laisse)

# Correction de la g�om�trie
geometryTopageCheck.correct_geometry(geometry_name,workspace + geodatabase_topage + "/" + dataset_geometry + "/",csvGeometryFeature_file,file_laisse)

#raw_input()
