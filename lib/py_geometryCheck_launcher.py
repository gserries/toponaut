# -*- coding: utf-8 -*-
'''
Created on 25 août 2014

@author: serries
'''

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

# Dataset de la géometrie
dataset_geometry="geometry"

# Fichier pour la reference spatiale de la geometrie
file_srid = "D:/ONEMA_GS/04_Produit/controleTopo/file/shape/TRONCON_COURS_EAU.SHP"

''' Nom de la géométrie '''
geometry_name = "Geometrie"

### LANCEMENT DES SCRIPTS ###

# Cr�ation de l'objet objets
geometryTopageCheck = geometryCheck()

# V�rification de la geometrie (continuité du réseau)
geometryTopageCheck.checkGeometry(geometry_name,workspace + geodatabase_topage + "/" + dataset_topology + "/",workspace + geodatabase_topage + "/" + dataset_geometry + "/",csvGeometryFeature_file)
