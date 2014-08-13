# -*- coding: utf-8 -*-

## Chargement des librairies Pythons
import os
import shutil
import arcpy

class geodatabase:

    ### SCRIPT ###               
        
    ## Création de framework automatique   
    def create(self,folder_geodatabase,geodatabase_name) :
        
        # Suppression des geodatabase si elles existent
        if os.path.exists(folder_geodatabase + geodatabase_name):
            #print u"Suppression de la géodatabase si elle existe"
            shutil.rmtree(folder_geodatabase + geodatabase_name)
        
        # Création des géodatabases
        #print(u"Création de la géodatabase")
        arcpy.CreateFileGDB_management(folder_geodatabase, geodatabase_name)


    def path(self,feature):
        geodatabase_path=""
        geodatabase_bool= 0
        
        for geodatabase_string in feature.split('/'):
            if geodatabase_string[-4:]==".gdb":
                geodatabase_path = geodatabase_path + '/' + geodatabase_string
                geodatabase_bool = 1
            elif geodatabase_bool==0 :
                if geodatabase_path == "":
                    geodatabase_path = geodatabase_string
                else:
                    geodatabase_path = geodatabase_path + "/" + geodatabase_string
        
        return geodatabase_path

        
    def name(self,feature):
        
        for geodatabase_string in feature.split('/'):
            if geodatabase_string[-4:]==".gdb":
                geodatabase_name = geodatabase_string
                break
        
        return geodatabase_name      










