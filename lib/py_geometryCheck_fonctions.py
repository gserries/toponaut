# -*- coding: utf-8 -*-
'''
Created on 25 août 2014

@author: serries
'''
import csv
import arcpy

from py_arcpy_feature import feature
from py_geometry_fonctions import Geometry 


class geometryCheck:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    ## MERGE D'UNE LISTE DE FICHIERS DANS UN REPERTOIRE SOURCE
    def feature_dictionary(self,csvGeometryFeature_file,geometry_folder):
        
        featureTopage = feature()
        
        # Ajout des tables
        geometryFeature_list = open(csvGeometryFeature_file, "rb")
        try:
            feature_dictionary = {}
            # Liste des fichiers shape
            feature_reader = csv.reader(geometryFeature_list,delimiter=';')
            # Ajout des fichiers dans le featureclasse de la topologie
            for feature_row in feature_reader:
                # Non prise en compte la première ligne de titre
                if feature_reader.line_num<>1:
                    if featureTopage.checkPresence(geometry_folder + feature_row[1]) == "True":
                        feature_dictionary[feature_row[0]] = feature_row[1]
        finally:
            geometryFeature_list.close() 
            
        return feature_dictionary        

        
    def add_geometryFeatureFromTopologyDataset(self,geometry_name,topology_folder,geometry_folder,csvGeometryFeature_file):
            
        print u"\n########## Création des fichiers géométrique à partir des fichiers réseaux de la BD Topage##########\n"

        featureTopage = feature()  
        geometryTopage = Geometry()
         
        # remise à zéro des règles topologiques
        geometryTopage.create_ArcGISGeometryEnvironment(geometry_folder,geometry_name)
        
        # Ajout des tables
        geometryFeature_list = open(csvGeometryFeature_file, "rb")
        geometryFeature_reader = csv.reader(geometryFeature_list,delimiter=';')
        for feature_row in geometryFeature_reader:
            if geometryFeature_reader.line_num<>1:
                if feature_row[2] <> '':
                    if feature_row[1] == "Network_point" and arcpy.Exists(topology_folder + feature_row[2]):
                        featureTopage.copy(topology_folder + feature_row[2],geometry_folder + feature_row[1])
                    if feature_row[1] == "Network_line" and arcpy.Exists(topology_folder + feature_row[2]):
                        featureTopage.copy(topology_folder + feature_row[2],geometry_folder + feature_row[1])
                    if feature_row[1] == "NetworkSeparetedCrossing_line":
                        if arcpy.Exists(geometry_folder + "Network_line") and arcpy.Exists(topology_folder + feature_row[2]):
                            arcpy.Append_management(topology_folder + feature_row[2],geometry_folder + "Network_line","NO_TEST","#","#")                    
        geometryFeature_list.close()
      
        
    def checkGeometry(self,geometry_name,geometry_folder,csvGeometryFeature_file,file_laisse):      
        geometryTopage = Geometry()
          
        geometryFeature_dictionary = self.feature_dictionary(csvGeometryFeature_file, geometry_folder)
    
        geometryTopage.check(geometry_name,geometry_folder,geometryFeature_dictionary,file_laisse)    