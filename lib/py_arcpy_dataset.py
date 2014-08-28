# -*- coding: utf-8 -*-

## Chargement des librairies Pythons
import arcpy

class dataset:

    ### SCRIPT ###   

    ## Création du dataset   
    def create(self,geodatabase_path,dataset_name,srid):

        # Récupérations du système de coordonnées pour les datasets
        
        #dsc = arcpy.Describe(file_srid)
        #coord_sys = dsc.spatialReference
        coord_sys = arcpy.SpatialReference(srid)
        
        # Création du dataset
        #print(u"Création du dataset " + dataset_name)
        if arcpy.Exists(geodatabase_path + "/" + dataset_name):
            arcpy.env.workspace  = geodatabase_path + "/" + dataset_name
            feature_list = arcpy.ListFeatureClasses()
            for feature in feature_list :
                arcpy.Delete_management(feature)
            arcpy.Delete_management(geodatabase_path + "/" + dataset_name)
        
        arcpy.CreateFeatureDataset_management(geodatabase_path, dataset_name,coord_sys)   

        
    def name(self,feature):
        dataset=""#@UnusedVariable
        dataset_bool= 0
        
        for dataset_string in feature.split('/'):
            if dataset_string[-4:]==".gdb":
                dataset_bool = 1
            elif dataset_bool==1 :
                dataset_name = dataset_string
                break

        return dataset_name

        
    def path(self,feature):
        dataset_path=""
        dataset_bool= 0
        
        for dataset_string in feature.split('/'):
            if dataset_string[-4:]==".gdb":
                dataset_path = dataset_path + '/' + dataset_string
                dataset_bool = 1
            elif dataset_bool==1 :
                dataset_path = dataset_path + '/' + dataset_string
                break
            elif dataset_bool==0 :
                if dataset_path == "":
                    dataset_path = dataset_string
                else:
                    dataset_path = dataset_path + "/" + dataset_string
                
        return dataset_path
        
    def feature_list(self,dataset_path):
        feature_dict = {}
        
        arcpy.env.workspace  = dataset_path
        feature_list = arcpy.ListFeatureClasses()
        
        for feature in feature_list:
            feature_dict[str(feature)] = ""
        
        return feature_dict