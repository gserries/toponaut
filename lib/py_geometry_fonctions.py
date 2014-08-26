# -*- coding: utf-8 -*-
'''
Created on 25 août 2014

@author: serries
'''
## Chargement des librairies Pythons
import arcpy
from py_arcpy_geodatabase import geodatabase  

class Geometry:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    ## Création du dataset   
    def create_ArcGISGeometryEnvironment(self,geometry_folder,geometry_name):

        # Suppression de l'ancienne topologie
        if arcpy.Exists(geometry_folder + geometry_name):
            arcpy.Delete_management(geometry_folder + geometry_name)

        # Suppression des anciens fichiers
        arcpy.env.workspace  = geometry_folder
        oldGeometry = arcpy.ListFeatureClasses()
        for oldGeometryFile in oldGeometry :
            arcpy.Delete_management(geometry_folder + oldGeometryFile)
            
            
    def check(self,geometry_name,geometry_folder,geometryFeature_dictionary,file_laisse=""):
        
        geodatabaseTopage = geodatabase() 
        geodatabasePath = geodatabaseTopage.path(geometry_folder)
        
        arcpy.env.overwriteOutput = True
    
        for feature in geometryFeature_dictionary.itervalues():
            if arcpy.Exists(geodatabasePath + "/" + feature + "_BUILDERR"):
                arcpy.Delete_management(geodatabasePath + "/" + feature + "_BUILDERR")            
    
        # Sélection des entités en jointure avec la laisse ou de celles qui ont l'altitude la plus basse
        print("Création du fichier de l'exutoire")
        arcpy.MakeFeatureLayer_management(geometry_folder + geometryFeature_dictionary['2'], 'lyr')
        
        print geometry_folder + geometryFeature_dictionary['2']
        print file_laisse
        
        if file_laisse!="":
            arcpy.SelectLayerByLocation_management('lyr','INTERSECT',file_laisse,selection_type="NEW_SELECTION")
        
        if file_laisse=="" or arcpy.GetCount_management('lyr')==0:
            print "le compte est : " + arcpy.GetCount_management('lyr').__str__()
            print "merci d'indiquer le fichier des laisses"
            return "" 

        # Création du fichier de l'éxutoire à partir de cette sélection                
        arcpy.FeatureVerticesToPoints_management('lyr',geometry_folder + "/" + geometryFeature_dictionary['2'] + "_Exutoire","END")

        # Suppression du layer
        arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr")  
        
        # Ecriture de la table des sources et des puits
        print("Création de la table des puits et cuvettes")
        arcpy.FeatureVerticesToPoints_management(geometry_folder + "/" + geometryFeature_dictionary['2'], geometry_folder + "/" + geometryFeature_dictionary['2'] + "_summit", "DANGLE")

        # Création du réseau géométrique            
        print("Construction du réseau géométrique")
        arcpy.CreateGeometricNetwork_management(geometry_folder,geometry_name,geometryFeature_dictionary['2'] + " SIMPLE_EDGE NO;" + geometryFeature_dictionary['2'] + "_summit SIMPLE_JUNCTION NO","0.001","#","#","#","PRESERVE_ENABLED")
        
        print("Suppression des éléments non connectés")
        arcpy.gp.TraceGeometricNetwork(geometry_folder + "/" + geometry_name, "lyr" , geometry_folder + "/" + geometryFeature_dictionary['2'] + "_Exutoire", "FIND_DISCONNECTED")
        arcpy.CopyFeatures_management("lyr/" + geometryFeature_dictionary['2'] , geometry_folder + "/" + geometryFeature_dictionary['2'] + "_disconnected")
        arcpy.CopyFeatures_management("lyr/" + geometryFeature_dictionary['2'] + "_summit",geometry_folder + "/" + geometryFeature_dictionary['2'] + "_summit_disconnected")
       
        arcpy.DeleteFeatures_management("lyr/" + geometryFeature_dictionary['2'])
        arcpy.DeleteFeatures_management("lyr/" + geometryFeature_dictionary['2'] + "_summit")
        arcpy.Delete_management("lyr")                
                            
        print("Recréation du réseau géométrique")
        arcpy.Delete_management(geometry_folder + "/" + geometry_name)
        arcpy.CreateGeometricNetwork_management(geometry_folder,geometry_name,geometryFeature_dictionary['2'] + " SIMPLE_EDGE NO;" + geometryFeature_dictionary['2'] + "_summit SIMPLE_JUNCTION YES","0.001","#","#","#","PRESERVE_ENABLED")
        
        print("Ajout de l'exutoire")
        arcpy.MakeFeatureLayer_management(geometry_folder + "/" + geometryFeature_dictionary['2'] + "_summit", 'lyr') 
        arcpy.SelectLayerByLocation_management('lyr', 'INTERSECT', geometry_folder + "/" + geometryFeature_dictionary['2'] + "_Exutoire")
        arcpy.CalculateField_management('lyr','AncillaryRole',"2","PYTHON_9.3","#")
        arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION")
        arcpy.Delete_management("lyr")
        
        print("Calcul du sens d'écoulement")
        arcpy.SetFlowDirection_management(geometry_folder+ "/" + geometry_name, "WITH_DIGITIZED_DIRECTION")
