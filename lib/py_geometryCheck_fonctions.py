# -*- coding: utf-8 -*-
'''
Created on 25 août 2014

@author: serries
'''
import csv
import arcpy

from py_arcpy_geodatabase import geodatabase
from py_arcpy_dataset import dataset  
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
    def checkGeometry(self,geometry_name,topology_folder,geometry_folder,csvGeometryFeature_file):        
        geometryTopage = Geometry()
    
        self.add_geometryFeatureFromTopologyDataset(geometry_name,topology_folder, geometry_folder, csvGeometryFeature_file)
        #geometryTopage.add_feature2ArcGISGeometry(topology_folder,topology_name,feature)      

        
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