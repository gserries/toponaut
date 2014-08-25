# -*- coding: utf-8 -*-
'''
Created on 25 août 2014

@author: serries
'''
## Chargement des librairies Pythons
import arcpy

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
            

    def add_feature2ArcGISGeometry(self,topology_folder,topology_name,feature):
        
        Network_point="HydroNode_point"
        Network_line="WatercourseLink_line"
        NetworkSeparetedCrossing_line="WatercourseSeparetedCrossing_line"
        
        

        arcpy.AddFeatureClassToTopology_management(topology_folder + topology_name,topology_folder + feature, "1", "1")
    
    def check(self,database,dataset_topology,dataset_geometry,file_name,geometry_name,file_laisse=""):
        arcpy.env.overwriteOutput = True
        
        folder_topology = database + "/" + dataset_topology
        folder_geometry= database + "/" + dataset_geometry
        
        # Suppression de la géometrie si elle existe
        if arcpy.Exists(folder_geometry + "/" + geometry_name):
            arcpy.Delete_management(folder_geometry + "/" + geometry_name)
        if arcpy.Exists(database + "/" + file_name + "_BUILDERR"):
            arcpy.Delete_management(database + "/" + file_name + "_BUILDERR")
            
        # Copie des fichiers de topologie
        print("Copie et fusion des fichiers de topologie sources")
        arcpy.CopyFeatures_management(folder_topology + "/" + file_name + "_topo", folder_geometry + "/" + file_name + "_geometry")   
    
        # Sélection des entités en jointure avec la laisse ou de celles qui ont l'altitude la plus basse
        print("Création du fichier de l'exutoire")    
        arcpy.MakeFeatureLayer_management(folder_geometry + "/" + file_name + "_geometry", 'lyr')
        if file_laisse!="":
            arcpy.SelectLayerByLocation_management('lyr','INTERSECT',file_laisse,selection_type="NEW_SELECTION")
        
        if file_laisse=="" or arcpy.GetCount_management('lyr')==0:
            print "le compte est : " + arcpy.GetCount_management('lyr')
            #minZ = [row[0] for row in arcpy.da.SearchCursor ('lyr', ["Z_FIN"])]
            #sqlExp = "Z_FIN = " + str(min(minZ))
            #arcpy.SelectLayerByAttribute_management('lyr', "NEW_SELECTION", sqlExp)
            # Suppression du curseur pour éviter le lock des tables
            #del row
    
        # Création du fichier de l'éxutoire à partir de cette sélection                
        arcpy.FeatureVerticesToPoints_management('lyr',folder_geometry + "/" + file_name + "_geometry_Exutoire","END")
        
        # Suppression du layer
        arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr")   
        
        # Ajout des ponts et des tunnels sur le fichier topologiquement correct
        arcpy.Append_management(folder_topology + "/" + file_name + "_topo_Tunnel",folder_geometry + "/" + file_name + "_geometry","TEST","#","#")   
        arcpy.Append_management(folder_topology + "/" + file_name + "_topo_pontCanal",folder_geometry + "/" + file_name + "_geometry","TEST","#","#")   
        
        # Ecriture de la table des sources et des puits
        print("Création de la table des puits et cuvettes")
        arcpy.FeatureVerticesToPoints_management(folder_geometry + "/" + file_name + "_geometry", folder_geometry + "/" + file_name + "_geometry" + "_summit", "DANGLE")
    
        print("Construction du réseau géométrique")
        # Création du réseau géométrique
        arcpy.CreateGeometricNetwork_management(folder_geometry,geometry_name,file_name + "_geometry" + " SIMPLE_EDGE NO;" + file_name + "_geometry" + "_summit SIMPLE_JUNCTION NO","0.001","#","#","#","PRESERVE_ENABLED")
        
        print("Suppression des éléments non connectés")
        arcpy.gp.TraceGeometricNetwork(folder_geometry + "/" + geometry_name, "lyr" , folder_geometry + "/" + file_name + "_geometry_Exutoire", "FIND_DISCONNECTED")
        arcpy.CopyFeatures_management("lyr/" + file_name + "_geometry",folder_geometry + "/" + file_name + "_geometry_disconnected")
        arcpy.CopyFeatures_management("lyr/" + file_name + "_geometry_summit",folder_geometry + "/" + file_name + "_geometry_summit_disconnected")
       
        arcpy.DeleteFeatures_management("lyr/" + file_name + "_geometry")
        arcpy.DeleteFeatures_management("lyr/" + file_name + "_geometry_summit")
        arcpy.Delete_management("lyr")
        
        print("Recréation du réseau géométrique")
        arcpy.Delete_management(folder_geometry + "/" + geometry_name)
        arcpy.CreateGeometricNetwork_management(folder_geometry,geometry_name,file_name + "_geometry" + " SIMPLE_EDGE NO;" + file_name + "_geometry" + "_summit SIMPLE_JUNCTION YES","0.001","#","#","#","PRESERVE_ENABLED")
        
        print("Ajout de l'exutoire")
        arcpy.MakeFeatureLayer_management(folder_geometry + "/" + file_name + "_geometry_summit", 'lyr') 
        arcpy.SelectLayerByLocation_management('lyr', 'INTERSECT', folder_geometry + "/" + file_name + "_geometry_Exutoire")
        arcpy.CalculateField_management('lyr','AncillaryRole',"2","PYTHON_9.3","#")
        arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION")
        arcpy.Delete_management("lyr")
        
        print("Calcul du sens d'écoulement")
        arcpy.SetFlowDirection_management(folder_geometry+ "/" + geometry_name, "WITH_DIGITIZED_DIRECTION")
        