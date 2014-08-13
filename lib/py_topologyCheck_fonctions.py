# -*- coding: utf-8 -*-
## Chargement des librairies Pythons

import csv
import arcpy

from py_arcpy_geodatabase import geodatabase
from py_arcpy_dataset import dataset  
from py_arcpy_feature import feature
from py_topology_fonctions import topology 
 
class topologyCheck:
      
    ### SCRIPT ###   
                
    ## MERGE D'UNE LISTE DE FICHIERS DANS UN REPERTOIRE SOURCE
    def createFramework(self,destination_folder,geodatabase_topage,dataset_source,dataset_topo,file_srid):
  
        geodatabaseTopage = geodatabase() 
        datasetTopage = dataset()   
        featureTopage = feature()
        
        print u"\n########## Création de l'environnement de vérification topologique ##########\n"
        
        geodatabaseTopage.create(destination_folder,geodatabase_topage)
        
        datasetTopage.create(destination_folder + geodatabase_topage,dataset_source,file_srid)
        datasetTopage.create(destination_folder + geodatabase_topage,dataset_topo,file_srid)
        datasetTopage.create(destination_folder + geodatabase_topage,dataset_topo + "_error",file_srid)
        
        featureTopage.create(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error","topo_point_error","POINT",file_srid)
        featureTopage.create(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error","topo_multipoint_error","MULTIPOINT",file_srid)
        featureTopage.create(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error","topo_line_error","POLYLINE",file_srid)
        featureTopage.create(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error","topo_polygon_error","POLYGON",file_srid)
        
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_point_error","OriginObjectClassName","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_point_error","OriginObjectID","LONG")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_point_error","DestinationObjectClassName","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_point_error","DestinationObjectID","LONG")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_point_error","RuleType","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_point_error","RuleDescription","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_point_error","isExeption","LONG")
         
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_multipoint_error","OriginObjectClassName","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_multipoint_error","OriginObjectID","LONG")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_multipoint_error","DestinationObjectClassName","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_multipoint_error","DestinationObjectID","LONG")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_multipoint_error","RuleType","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_multipoint_error","RuleDescription","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_multipoint_error","isExeption","LONG")
               
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_line_error","OriginObjectClassName","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_line_error","OriginObjectID","LONG")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_line_error","DestinationObjectClassName","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_line_error","DestinationObjectID","LONG")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_line_error","RuleType","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_line_error","RuleDescription","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_line_error","isExeption","LONG")
        
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_polygon_error","OriginObjectClassName","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_polygon_error","OriginObjectID","LONG")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_polygon_error","DestinationObjectClassName","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_polygon_error","DestinationObjectID","LONG")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_polygon_error","RuleType","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_polygon_error","RuleDescription","TEXT")
        featureTopage.addField(destination_folder + geodatabase_topage + "/" + dataset_topo + "_error/topo_polygon_error","isExeption","LONG")

        
    ## MERGE D'UNE LISTE DE FICHIERS DANS UN REPERTOIRE SOURCE
    def feature_dictionary(self,csvFeature_file,source_folder):
        
        featureTopage = feature()
        
        # Ajout des tables
        feature_list = open(csvFeature_file, "rb")
        try:
            feature_dictionary = {}
            # Liste des fichiers shape
            feature_reader = csv.reader(feature_list,delimiter=';')
            # Ajout des fichiers dans le featureclasse de la topologie
            for feature_row in feature_reader:
                # Non prise en compte la première ligne de titre
                if feature_reader.line_num<>1:
                    # Ecriture du dictionnaire des entités présentes dans la topologie
                    feature_dictionary[feature_row[0]] = {}
                    feature_dictionary[feature_row[0]]['id'] = feature_row[0]       
                    feature_dictionary[feature_row[0]]['name'] = feature_row[1]
                    feature_dictionary[feature_row[0]]['id_heritage'] = feature_row[6]
                    if featureTopage.checkPresence(source_folder + feature_row[1]) == "True":
                        feature_dictionary[feature_row[0]]['fileBool'] = "True"
                        #print feature_dictionary[feature_row[0]]['name'] + " : ok"
                    else :
                        feature_dictionary[feature_row[0]]['fileBool'] = "False"
                        #print feature_dictionary[feature_row[0]]['name'] + " : pas ok"
        
        finally:
            feature_list.close() 
            
        return feature_dictionary

        
    # Fonction pour vérifier la topologie la topology. Cette fonction appelle les fonction interne de la classe
    def checkTopology(self,topology_name,topology_folder,csvFeature_file,csvRule_file,csvRuleBDTopage):
    
        feature_dictionary = self.feature_dictionary(csvFeature_file,topology_folder)
        self.add_topologyFeature2Topology(topology_folder,topology_name,feature_dictionary,csvRule_file,csvRuleBDTopage)

        
    ## MERGE D'UNE LISTE DE FICHIERS DANS UN REPERTOIRE SOURCE
    def add_sourceFeatureFromCSV(self,destination_folder,csvFeature_file,file_srid):

        featureTopage = feature()
        
        #feature_dictionary = {}
        
        print u"\n########## Ajout des fichiers sources dans le vérificateur ##########\n"
        
        # Ajout des tables
        feature_list = open(csvFeature_file, "rb")
        
        feature_reader = csv.reader(feature_list,delimiter=';')
        for feature_row in feature_reader:
            if feature_reader.line_num<>1:
                if feature_row[3] <> '':
                    feature_name = feature_row[3].split('\\')
                    feature_name = feature_name[len(feature_name)-1]
                    feature_name = feature_name.replace(".shp", "")
                    feature_name = feature_name.replace(".SHP", "")
                    
                    print feature_name
                    
                    featureTopage.copy(feature_row[3], destination_folder + feature_name)

        feature_list.close()    
 
 
    def add_topologyFeatureFromSourceDataset(self,topology_name,source_folder,destination_folder,csvFeature_file):
            
        print u"\n########## Création des fichiers Topage depuis les sources ##########\n"

   
        datasetTopage = dataset()   
        featureTopage = feature()  
        topologyTopage = topology()
         
        # remise à zéro des règles topologiques
        topologyTopage.create_ArcGISTopology(destination_folder,topology_name)
        
        # Ajout des tables
        featureSourceDataset_dictionary = datasetTopage.feature_list(source_folder)
        feature_list = open(csvFeature_file, "rb")
        
        feature_reader = csv.reader(feature_list,delimiter=';')
        for feature_row in feature_reader:
            if feature_reader.line_num<>1:
                if feature_row[3] <> '':
                    file_name = feature_row[3].split('\\')
                    file_name = file_name[len(file_name)-1]
                    file_name = file_name.replace(".shp", "")
                    file_name = file_name.replace(".SHP", "")
                    if featureSourceDataset_dictionary.has_key(file_name) == True : 
                        print feature_row[1]
                        featureTopage.copy(source_folder + file_name,destination_folder + feature_row[1])
                        
        feature_list.close()    
        
        # Ajout des fichiers parents...
        feature_dictionary = self.feature_dictionary(csvFeature_file,destination_folder)
        self.add_topologyParentFeature(destination_folder,feature_dictionary)
  
        
    def add_topologyParentFeature(self,topology_folder,feature_dictionary):
                 
        print u"\n########## Création des fichiers topage parents ##########\n"
        self.i_heritage = int()
        featureTopage = feature()
        
        oldFile_dictionary = {}
        for i_heritage in range(0,5):#@UnusedVariable
            newFile_dictionary = {}
            for feature_element in feature_dictionary.values() :
                if feature_element['id_heritage']<>'' and feature_element['fileBool'] == "True" and oldFile_dictionary.has_key(feature_element['id']) == False:
                    if newFile_dictionary.has_key(feature_element['id_heritage']) == False :
                        newFile_dictionary[feature_element['id_heritage']]=[]
                    
                    newFile_dictionary[feature_element['id_heritage']].append(topology_folder + feature_element['name'])
                    oldFile_dictionary[feature_element['id']] = ""
                        
            if len(newFile_dictionary) == 0 :
                break

            for id_featureElement,feature_element in newFile_dictionary.items() :
                if featureTopage.checkPresence(topology_folder + feature_dictionary[id_featureElement]['name']) == "True" :
                    featureTopage.copy(topology_folder + feature_dictionary[id]['name'],topology_folder + feature_dictionary[id_featureElement]['name'] + "_temp")
                    feature_element.append(topology_folder + feature_dictionary[id_featureElement]['name'] + "_temp")
                
                featureTopage.merge(feature_element, topology_folder + feature_dictionary[id_featureElement]['name'])
                feature_dictionary[id_featureElement]['fileBool'] = "True"
                
                print feature_dictionary[id_featureElement]['name']
                
                featureTopage.delete(topology_folder + feature_dictionary[id_featureElement]['name'] + "_temp")
        
        return feature_dictionary

        
    def add_topologyFeature2Topology(self,topology_folder,topology_name,feature_dictionary,csvRule_file,csvRuleBDTopage):
        
        ruleGS_dictionnary = {}

        datasetTopage = dataset()
        featureTopage = feature()
        topologyTopage = topology()

        rule_list = open(csvRule_file, "rb")
        rule_reader = csv.reader(rule_list,delimiter=';')
        
        ruleBDTopage_list = open(csvRuleBDTopage, "rb")
        ruleBDTopage_reader = csv.reader(ruleBDTopage_list,delimiter=';')

        # Création de la topology ArcGIS
        topologyTopage.create_ArcGISTopology(topology_folder,topology_name)
 
        try :
            # Ajout des feature dans le gestionnaire topo
            for id_featureTopo,featureTopo in feature_dictionary.items():#@UnusedVariable
                if featureTopo['fileBool']=='True':                  
                    topologyTopage.add_feature2ArcGISTopology(topology_folder,topology_name,featureTopo['name'])  
                    
            # Check de toutes les vérifications ajoutées dans le dictionnaire
            #print u"\n########## Règles topologiques à tester ##########\n"       
            
            for id_featureTopo,featureTopo in feature_dictionary.items():#@UnusedVariable
                if featureTopo['fileBool']=='True':                        
                    # Remise à zéro du csv des règles topologiques de la BD Topage
                    ruleBDTopage_list.seek(0)
                    # Recherche de la présence de règle topologique concernant le fichier en question
                    for ruleBDTopage_row in ruleBDTopage_reader:
                        
                        # Paramétrage de la règle BD Topage
                        ruleBDtopage = {'topologyId':ruleBDTopage_row[13]}
                        ruleBDtopage['topologyTexte'] = ruleBDTopage_row[2]
                        ruleBDtopage['feature1Id'] = ruleBDTopage_row[4]
                        ruleBDtopage['feature2Id'] = ruleBDTopage_row[7]
                        ruleBDtopage['feature3Id'] = ruleBDTopage_row[10]
                        ruleBDtopage['field'] = ruleBDTopage_row[14]
                        ruleBDtopage['fieldValue'] = ruleBDTopage_row[15]  
                        
                        # Si la règle topologique concerne l'objet recherché
                        if ruleBDTopage_reader.line_num<>1 and ruleBDtopage['feature1Id'] == featureTopo['id']:
                            # Recherche de la règle topologique dans les règles génériques ESRI
                            rule_list.seek(0)
                            for rule_row in rule_reader:
                            
                                # Paramètre de la règle topologique
                                rule = {'id':rule_row[0]}
                                rule['feature2Bool'] = rule_row[6]
                                rule['attributBool'] = rule_row[8]
                                rule['arcgisBool'] = rule_row[12]
                                rule['fonction'] = rule_row[13]
                                
                                # Si le numéro de la règle générique correspond au numéro de la règle indiqué dans les règles de la BD Topage
                                if rule_reader.line_num<>1 and rule['id'] == ruleBDtopage['topologyId']:
                                    # Appel de la fonction d'ajout des règles à la topologie
                                    ruleGS_dictionnary = topologyTopage.add_topologyRule(ruleGS_dictionnary,feature_dictionary,topology_folder,topology_name,featureTopo,ruleBDtopage,rule)

        finally:
            ruleBDTopage_list.close()
            rule_list.close()
        
        # Validation de la topologie
        print(u"\n########## Vérification de la topologie ArcGIS ##########\n")
        topologyTopage.check(topology_folder,topology_name)       
        
        #Export des erreurs Arcgis
        featureTopage.delete(topology_folder[0:-1] + "_error" + "/" + topology_name + "_point")
        featureTopage.delete(topology_folder[0:-1] + "_error" + "/" + topology_name + "_line")
        featureTopage.delete(topology_folder[0:-1] + "_error" + "/" + topology_name + "_poly")
        
        arcpy.ExportTopologyErrors_management(topology_folder + topology_name,datasetTopage.path(topology_folder) + "_error",topology_name)
        
        # Check de toutes les vérifications ajoutées dans le dictionnaire
        print u"\n########## Résultat de la vérifications des règles de topologies ##########\n"

        for ruleGS_dictionnary_key in ruleGS_dictionnary.keys():
            print ruleGS_dictionnary_key + " : " + ruleGS_dictionnary[ruleGS_dictionnary_key]        
        
        return ruleGS_dictionnary
