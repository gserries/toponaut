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
    def create_arcGISGeometryEnvironment(self,geometry_folder,geometry_name):

        # Suppression de l'ancienne topologie
        if arcpy.Exists(geometry_folder + geometry_name):
            arcpy.Delete_management(geometry_folder + geometry_name)

        # Suppression des anciens fichiers
        arcpy.env.workspace  = geometry_folder
        oldGeometry = arcpy.ListFeatureClasses()
        for oldGeometryFile in oldGeometry :
            arcpy.Delete_management(geometry_folder + oldGeometryFile)
            
            
    def check_orientation(self,geometry_name,geometry_folder,networkLine,file_laisse=""):
        
        geodatabaseTopage = geodatabase() 
        geodatabasePath = geodatabaseTopage.path(geometry_folder)
        
        arcpy.env.overwriteOutput = True
    
        if arcpy.Exists(geodatabasePath + "/" + networkLine + "_BUILDERR"):
            arcpy.Delete_management(geodatabasePath + "/" + networkLine + "_BUILDERR")            
    
        # Sélection des entités en jointure avec la laisse ou de celles qui ont l'altitude la plus basse
        print("Création du fichier de l'exutoire")
        arcpy.MakeFeatureLayer_management(geometry_folder + networkLine, 'lyr')
        
        print file_laisse
        
        if file_laisse!="":
            arcpy.SelectLayerByLocation_management('lyr','INTERSECT',file_laisse,selection_type="NEW_SELECTION")
        
        if file_laisse=="" or arcpy.GetCount_management('lyr')==0:
            print "le compte est : " + arcpy.GetCount_management('lyr').__str__()
            print "merci d'indiquer le fichier des laisses"
            return "" 

        # Création du fichier de l'éxutoire à partir de cette sélection                
        arcpy.FeatureVerticesToPoints_management('lyr',geometry_folder + networkLine + "_Exutoire","END")

        # Suppression du layer
        arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr")  
        
        # Ecriture de la table des sources et des puits
        print("Création de la table des puits et cuvettes")
        arcpy.FeatureVerticesToPoints_management(geometry_folder + networkLine, geometry_folder + networkLine + "_summit", "DANGLE")

        # Création du réseau géométrique            
        print("Construction du réseau géométrique")
        arcpy.CreateGeometricNetwork_management(geometry_folder,geometry_name,networkLine + " SIMPLE_EDGE NO;" + networkLine + "_summit SIMPLE_JUNCTION NO","0.001","#","#","#","PRESERVE_ENABLED")
        
        print("Suppression des éléments non connectés")
        arcpy.gp.TraceGeometricNetwork(geometry_folder + geometry_name, "lyr" , geometry_folder + networkLine + "_Exutoire", "FIND_DISCONNECTED")
        arcpy.CopyFeatures_management("lyr/" + networkLine , geometry_folder + networkLine + "_disconnected")
        arcpy.CopyFeatures_management("lyr/" + networkLine + "_summit",geometry_folder + networkLine + "_summit_disconnected")
       
        arcpy.DeleteFeatures_management("lyr/" + networkLine)
        arcpy.DeleteFeatures_management("lyr/" + networkLine + "_summit")
        arcpy.Delete_management("lyr")                
                            
        print("Recréation du réseau géométrique")
        arcpy.Delete_management(geometry_folder  + geometry_name)
        arcpy.CreateGeometricNetwork_management(geometry_folder,geometry_name,networkLine + " SIMPLE_EDGE NO;" + networkLine + "_summit SIMPLE_JUNCTION YES","0.001","#","#","#","PRESERVE_ENABLED")
        
        print("Ajout de l'exutoire")
        arcpy.MakeFeatureLayer_management(geometry_folder + networkLine + "_summit", 'lyr') 
        arcpy.SelectLayerByLocation_management('lyr', 'INTERSECT', geometry_folder + networkLine + "_Exutoire")
        arcpy.CalculateField_management('lyr','AncillaryRole',"2","PYTHON_9.3","#")
        arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION")
        arcpy.Delete_management("lyr")
        
        print("Calcul du sens d'écoulement")
        arcpy.SetFlowDirection_management(geometry_folder+ "/" + geometry_name, "WITH_DIGITIZED_DIRECTION")
        
        
    def correct_orientation(self,geometry_name,geometry_folder,networkLine):       
        arcpy.env.overwriteOutput = True
        
        print("Création du fichier du réseau avec le bon sens d'écoulement")
        arcpy.gp.TraceGeometricNetwork(geometry_folder + geometry_name, "lyr" , geometry_folder + networkLine + "_Exutoire", "TRACE_UPSTREAM")
        
        arcpy.CopyFeatures_management("lyr/" + networkLine,geometry_folder + networkLine + "_Upstream")
    
        print("Création du fichier des réseaux avec le mauvais sens d'écoulement")
        arcpy.SelectLayerByAttribute_management("lyr/" + networkLine, "SWITCH_SELECTION")
        arcpy.CopyFeatures_management("lyr/" + networkLine,geometry_folder + networkLine + "_notUpstream")
        arcpy.SelectLayerByAttribute_management('lyr/' + networkLine, "CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management('lyr/' + networkLine + "_summit", "CLEAR_SELECTION")
        arcpy.Delete_management("lyr")
        
        print("Sélection des entités avec un mauvais sens de digitalisation et qui ne sont pas intermitent")
        arcpy.MakeFeatureLayer_management(geometry_folder + networkLine + "_notUpstream", 'lyr') 
        arcpy.SelectLayerByLocation_management('lyr',"BOUNDARY_TOUCHES",geometry_folder + networkLine + "_Upstream","#","NEW_SELECTION")
        
        #arcpy.SelectLayerByAttribute_management('lyr',"SUBSET_SELECTION",flowField + " = '" + flowAttribut + "'")
        
        print("Correction du sens de digitalisation")
        arcpy.FlipLine_edit('lyr')
        arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION")
        # arcpy.Delete_management("lyr")
        
        print("Assemblage des données du nouveau réseau")
        arcpy.Delete_management(geometry_folder + "/" + geometry_name)
        arcpy.Delete_management(geometry_folder + networkLine)
        arcpy.Merge_management(geometry_folder + networkLine + "_Upstream;" + geometry_folder + networkLine + "_notUpstream",geometry_folder + networkLine)
        
        #Appel de la fonction de recréation du réseau géométrique"
        #self.recheck_orientation(geometry_name,geometry_folder,networkLine)
        
        
    def recheck_orientation(self,geometry_name,geometry_folder,networkLine):
        arcpy.env.overwriteOutput = True   

        geodatabaseTopage = geodatabase() 
        geodatabasePath = geodatabaseTopage.path(geometry_folder)
        
        print("Recréation du réseau géométrique")
        if arcpy.Exists(geodatabasePath + "/" + networkLine + "_BUILDERR"):
            arcpy.Delete_management(geodatabasePath + "/" + networkLine + "_BUILDERR")
            
        arcpy.Delete_management(geometry_folder + geometry_name)
        arcpy.CreateGeometricNetwork_management(geometry_folder,geometry_name,networkLine + " SIMPLE_EDGE NO;" + networkLine + "_summit SIMPLE_JUNCTION YES","0.001","#","#","#","PRESERVE_ENABLED")
        
        print("Ajout de l'exutoire")
        arcpy.MakeFeatureLayer_management(geometry_folder + networkLine + "_summit", 'lyr') 
        arcpy.SelectLayerByLocation_management('lyr', 'INTERSECT', geometry_folder + networkLine + "_Exutoire")
        arcpy.CalculateField_management('lyr','AncillaryRole',"2","PYTHON_9.3","#")
        arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION")
        arcpy.Delete_management("lyr")
        
        print("Calcul du sens d'écoulement")
        arcpy.SetFlowDirection_management(geometry_folder + geometry_name, "WITH_DIGITIZED_DIRECTION")
        
        arcpy.TraceGeometricNetwork_management(geometry_folder + "/" + geometry_name, geometry_name, geometry_folder + networkLine + "_Exutoire", "TRACE_UPSTREAM")
        
        arcpy.MakeFeatureLayer_management(geometry_folder + networkLine + "_notUpstream", 'lyr_notUpstream') 
        
        return arcpy.GetCount_management('lyr_notUpstream').__str__()
        

