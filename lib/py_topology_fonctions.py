# -*- coding: utf-8 -*-
## Chargement des librairies Pythons

import arcpy

from py_topology_GSRules import topologyGSRules
 
class topology:

    ### SCRIPT ###   
                
    ## Création du dataset   
    def create_ArcGISTopology(self,topology_folder,topology_name):

        # Suppression de l'ancienne topologie
        if arcpy.Exists(topology_folder + topology_name):
            arcpy.Delete_management(topology_folder + topology_name)
        
        # Suppression des anciens fichiers
        #arcpy.env.workspace  = topology_folder
        #oldTopo = arcpy.ListFeatureClasses()
        #for oldTopoFile in oldTopo :
        #    arcpy.Delete_management(topology_folder + oldTopoFile)
            
        # Création de la topologie
        arcpy.CreateTopology_management(topology_folder,topology_name,"1")

   
    def add_feature2ArcGISTopology(self,topology_folder,topology_name,feature):
        arcpy.AddFeatureClassToTopology_management(topology_folder + topology_name,topology_folder + feature, "1", "1")

    # Ajout de règle topologiques à la topologie        
    def add_topologyRule(self,ruleGS_dictionnary,feature_dictionary,topology_folder,topology_name,feature,ruleBDtopage,rule):
        # Chargement de la bilbiothèque externe
        
          
        topologyGSRules_object = topologyGSRules()#@UnusedVariable        
        #print str(feature_dictionary[feature['id_heritage']]) + ":" + str(feature_dictionary[feature['id_heritage']]['fileBool'])    
        if rule['arcgisBool'] == "true" and rule['fonction']<>"" and rule['feature2Bool'] == "false" :
            #print ruleBDtopage['topologyTexte'] + " => " + rule['fonction']
            # Ajout de la règle...
            arcpy.AddRuleToTopology_management(topology_folder + topology_name,rule['fonction'],topology_folder + feature['name'],"","","")
            ruleGS_dictionnary[ruleBDtopage['topologyTexte']] = " voir le fichier " + topology_name + " dans ARCGIS"

        # Règle ARCGIS sur 2 objets                               
        if rule['arcgisBool'] == "true" and rule['fonction'] <> "" and rule['feature2Bool'] == "true" and feature_dictionary[ruleBDtopage['feature2Id']]['fileBool'] == 'True':
            #print ruleBDtopage['topologyTexte'] + " => " + rule['fonction']
            # Ajout de la règle...
            arcpy.AddRuleToTopology_management(topology_folder + topology_name,rule['fonction'],topology_folder + feature['name'],"",topology_folder + feature_dictionary[ruleBDtopage['feature2Id']]['name'],"")
            ruleGS_dictionnary[ruleBDtopage['topologyTexte']] = " voir le fichier " + topology_name + " dans ARCGIS"
            
        # Règle non ArcGIS sur un objet
        if rule['arcgisBool'] == "false" and rule['fonction']<>"" and rule['feature2Bool'] == "false":
            #print ruleBDtopage['topologyTexte'] + " => " + rule['fonction']
            # Appel à la fonction dans la classe des fonctions
            topologie_return = eval("topologyGSRules_object." + rule['fonction'] + "('" + topology_folder + feature['name'] + "')")
            # Ajout de la règle dans le dictionnaire des vérifications...
            ruleGS_dictionnary[ruleBDtopage['topologyTexte']] = topologie_return  

        # Règle non ArcGIS sur plus d'un objet
        if rule['arcgisBool'] == "false" and rule['fonction']<>"" and rule['feature2Bool'] == "true" and feature_dictionary[ruleBDtopage['feature2Id']]['fileBool'] == 'True':
            #print ruleBDtopage['topologyTexte'] + " => " + rule['fonction']
            # Appel à la fonction dans la classe des fonctions
            # fonction sans attribut
            if rule['attributBool']=="false":
                topologie_return = eval("topologyGSRules_object." + rule['fonction'] + "('" + topology_folder + feature['name'] + "','" + topology_folder + feature_dictionary[ruleBDtopage['feature2Id']]['name'] + "')")
            # fonction avec attribut
            else:
                topologie_return = eval("topologyGSRules_object." + rule['fonction'] + "('" + topology_folder + feature['name'] + "','" + topology_folder + feature_dictionary[ruleBDtopage['feature2Id']]['name'] + "','" + ruleBDtopage['field'] + "','" + ruleBDtopage['fieldValue'] + "')")
            # Ajout dans le dictionnaire de la liste des vérifications...
            ruleGS_dictionnary[ruleBDtopage['topologyTexte']] = topologie_return

        # Sinon, ...
        else:
            rien = ""#@UnusedVariable
            #print "--------" + ruleBDtopage['topologyTexte']
        
        return ruleGS_dictionnary


    def check(self,topology_folder,topology_name):
        # Validation de la topologie
        arcpy.ValidateTopology_management(topology_folder + "/" + topology_name)
  



