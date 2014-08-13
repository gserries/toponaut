# -*- coding: utf-8 -*-

### ENVIRONNEMENT DE TRAVAIL ###

## Chargement des librairies Pythons
import arcpy

from py_arcpy_geodatabase import geodatabase
from py_arcpy_dataset import dataset
from py_arcpy_feature import feature 

geodatabaseTopage = geodatabase()  
datasetTopage = dataset()
     
class topologyGSRules:
                                
    ### SCRIPT ###               

 
    def addEntityToRuleError(self,file_topologyError,entity,feature1,feature2,RuleType):
        feature_row = entity[0],feature1,entity[1],feature2,RuleType
        cursor = arcpy.da.InsertCursor(file_topologyError, ["SHAPE@","OriginObjectClassName","OriginObjectId","DestinationObjectClassName","RuleType"])#@UndefinedVariable
        cursor.insertRow(feature_row)
        del cursor
 
 
    def addLyrToRuleError(self,file_topologyError,lyr,feature1,feature2,RuleType):
        
        for feature_row in arcpy.da.SearchCursor(lyr,["SHAPE@","OBJECTID"]):#@UndefinedVariable
            feature_row = feature_row[0],feature1,feature_row[1],feature2,RuleType
            cursor = arcpy.da.InsertCursor(file_topologyError, ["SHAPE@","OriginObjectClassName","OriginObjectId","DestinationObjectClassName","RuleType"])#@UndefinedVariable
            cursor.insertRow(feature_row)
            del cursor
 
 
    def mustBeSinglePart_Point(self,feature):
        feature_description = arcpy.Describe(feature)
        if feature_description.shapeType == "Point":
            return "true"
        else:
            return "false"

            
    def mustBeSinglePart_Area(self,feature):

        # Géodatabase courante            
        #geodatabaseTopage = geodatabase()      
        
        # Géodatabase courante
        geodatabase_path = geodatabaseTopage.path(feature)
        
        # Création du fichier des points extrèmes pour chaque ligne
        if arcpy.Exists(geodatabase_path + "/feature_checking"):
            arcpy.Delete_management(geodatabase_path + "/feature_checking")
        arcpy.MultipartToSinglepart_management(feature,geodatabase_path + "/feature_checking")
        
        # Compte des features disloquées et des feature originel
        compte_feature = arcpy.GetCount_management(feature).getOutput(0)
        compte_featureTest = arcpy.GetCount_management(geodatabase_path + "/feature_checking").getOutput(0)
        
        # Suppression du fichier des points créé pour le traitement
        arcpy.Delete_management(geodatabase_path + "/feature_checking")     
        
        if int(compte_feature) == int(compte_featureTest) :
            return "true"
        else:
            return "false"
 
 
    def mustBeDisjoint_Point(self,feature1,feature2):
        for feature1_row in arcpy.da.SearchCursor(feature1, ["SHAPE@WKB"]):#@UndefinedVariable
            for feature2_row in arcpy.da.SearchCursor(feature2, ["SHAPE@WKB"]):#@UndefinedVariable
                if feature1_row == feature2_row:
                    return "false"
        
        return "true"

        
    def mustBeInside_PointArea(self,feature1,feature2):
 
        arcpy.MakeFeatureLayer_management(feature1, 'lyr') 
        compte1 = arcpy.GetCount_management('lyr').getOutput(0)
        arcpy.SelectLayerByLocation_management('lyr', 'WITHIN', feature2)
        compte2 = arcpy.GetCount_management('lyr').getOutput(0)

        if compte1 == compte2 :
            arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION")
            arcpy.Delete_management("lyr")
            return "true"
        else :
            arcpy.SelectLayerByAttribute_management('lyr', "SWITCH_SELECTION")
            dataset_topologyError = datasetTopage.path(feature1)
            self.addLyrToRuleError(dataset_topologyError + "/topo_point_error",'lyr',feature1,feature2,"mustBeInside_PointArea")            
            arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION")
            arcpy.Delete_management("lyr")
        
            return "false"

            
    def mustCoincideWith_LineLine(self,feature1,feature2):
    
        arcpy.MakeFeatureLayer_management(feature1, 'lyr') 
        compte1 = arcpy.GetCount_management('lyr').getOutput(0)
        arcpy.SelectLayerByLocation_management('lyr', 'ARE_IDENTICAL_TO', feature2)
        compte2 = arcpy.GetCount_management('lyr').getOutput(0)

        if compte1 == compte2 :
            arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION")
            arcpy.Delete_management("lyr")
            return "true"
        else :
            arcpy.SelectLayerByAttribute_management('lyr', "SWITCH_SELECTION")   
            dataset_topologyError = datasetTopage.path(feature1)                         
            self.addLyrToRuleError(dataset_topologyError + "/topo_line_error",'lyr',feature1,feature2,"mustBeInside_PointArea")
            #for feature_row in arcpy.da.SearchCursor('lyr',["SHAPE@WKB","OBJECTID"]):
            #    feature_row = feature_row[0],feature1,feature_row[1],feature2,"mustCoincideWith_LineLine"
            #    cursor = arcpy.da.InsertCursor(dataset_topologyError + "/topo_line_error", ["SHAPE@WKB","OriginObjectClassName","OriginObjectId","DestinationObjectClassName","RuleType"])
            #    cursor.insertRow(feature_row)
            #    del cursor
            arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION")
            arcpy.Delete_management("lyr")
        
            return "false"

            
    def mustNotCrossedByTheOutlineOf_LineArea(self,feature1,feature2):

        arcpy.MakeFeatureLayer_management(feature1, 'lyr') 
        arcpy.SelectLayerByLocation_management('lyr', 'CROSSED_BY_THE_OUTLINE_OF', feature2)
        compte = arcpy.GetCount_management('lyr').getOutput(0)

        if compte == "0" :
            arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION")
            arcpy.Delete_management("lyr")
            return "true"
        else :                
            dataset_topologyError = datasetTopage.path(feature1)            
            self.addLyrToRuleError(dataset_topologyError + "/topo_line_error",'lyr',feature1,feature2,"mustNotCrossedByTheOutlineOf_LineArea")
            arcpy.SelectLayerByAttribute_management('lyr', "CLEAR_SELECTION")
            arcpy.Delete_management("lyr")
            return "false"    

    def mustBeTransverse_LineArea(self,feature1,feature2):
    
        result=1  
        
        # Géodatabase courante
        geodatabase_path = geodatabaseTopage.path(feature1)
        
        # Sélection des lignes qui sont à l'intérieur des polygones
        arcpy.MakeFeatureLayer_management(feature2, 'lyr_lines')
        arcpy.SelectLayerByLocation_management('lyr_lines', 'WITHIN', feature1)
        
        # Sélection des polygones qui contiennent les lignes
        arcpy.MakeFeatureLayer_management(feature1, 'lyr_areas') 
        arcpy.SelectLayerByLocation_management('lyr_areas', 'CONTAINS', 'lyr_lines')    
        
        #On stoppe le traitement si il y a des polygones sans ligne traversante...
        if arcpy.GetCount_management(feature1).getOutput(0) <> arcpy.GetCount_management('lyr_areas').getOutput(0):
            # Remise à zéro de la sélection du polygones et des lignes à l'interieur de ce polygone
            arcpy.SelectLayerByAttribute_management('lyr_areas', "SWITCH_SELECTION")   
            dataset_topologyError = datasetTopage.path(feature1)                         
            self.addLyrToRuleError(dataset_topologyError + "/topo_polygon_error",'lyr_areas',feature1,feature2,"mustBeTransverse_LineArea")
            
            arcpy.SelectLayerByAttribute_management('lyr_areas', "SWITCH_SELECTION")  
            #arcpy.SelectLayerByAttribute_management('lyr_areas', "CLEAR_SELECTION")
            #arcpy.SelectLayerByAttribute_management('lyr_lines', "CLEAR_SELECTION")
            #arcpy.Delete_management("lyr_areas")  
            #arcpy.Delete_management("lyr_lines")
            
            result = 0
            #return "false"
        
        # Liste des polygones
        #areaList = arcpy.Geometry()
        #areaList = arcpy.CopyFeatures_management('lyr_areas',areaList)

        #for area in areaList:
        for entity in arcpy.da.SearchCursor('lyr_areas',["SHAPE@","OBJECTID"]):#@UndefinedVariable
            area = entity[0]
            # Paramétrage initial du resultat final
            resultEntity=0
            
            # Sélection des lignes contenu dans chaques polygone
            arcpy.SelectLayerByLocation_management('lyr_lines', 'WITHIN', area)
            
            # Création du fichier des points extrèmes pour chaque ligne
            if arcpy.Exists(geodatabase_path + "/pointBothEnds"):
                arcpy.Delete_management(geodatabase_path + "/pointBothEnds")
            arcpy.FeatureVerticesToPoints_management('lyr_lines',geodatabase_path + "/pointBothEnds","BOTH_ENDS")
            
            # Création du layer des points extrèmes
            arcpy.MakeFeatureLayer_management(geodatabase_path + "/pointBothEnds", 'lyr_pointBothEnds')
            
            # Création du layer des points qui touches le contour du polygone
            arcpy.SelectLayerByLocation_management('lyr_pointBothEnds', 'BOUNDARY_TOUCHES', area)
            arcpy.MakeFeatureLayer_management('lyr_pointBothEnds', 'lyr_pointsContour')  
            arcpy.SelectLayerByAttribute_management('lyr_pointBothEnds', "CLEAR_SELECTION")
            arcpy.Delete_management("lyr_pointBothEnds")
            
            # Création des layer des lignes du polygone déjà traitées et des lignes séléctionnées pour le traitement. Au départ, aucune sélection n'est faite dans ces layers.
            arcpy.MakeFeatureLayer_management('lyr_lines', 'lyr_selectedLines')
            arcpy.MakeFeatureLayer_management('lyr_lines', 'lyr_doneLines')
            
            # Nombre de lignes contenues dans le polygone
            compteLines = arcpy.GetCount_management('lyr_selectedLines').getOutput(0)
            
            # Sélection d'une première ligne dans le layer des lignes à traiter
            for feature_row in arcpy.SearchCursor('lyr_selectedLines'):
                OBJECTID_value = feature_row.getValue('OBJECTID')
                break
            arcpy.SelectLayerByAttribute_management('lyr_selectedLines', "NEW_SELECTION" , ' "OBJECTID" = ' + str(OBJECTID_value))            
            
            # Compteur des lignes sélectionnées à traiter
            compte_selectedLines=0
            
            # Boucle qui analyse au maximum toutes les lignes du polygone
            for i_compteLines in range(0,int(compteLines)) :#@UnusedVariable
                # Ajout de lignes qui touchent la ligne sélectionnée dans le layer des lignes à traiter
                arcpy.SelectLayerByLocation_management('lyr_selectedLines', 'BOUNDARY_TOUCHES', 'lyr_selectedLines','','ADD_TO_SELECTION')
                # Ajout de lignes des lignes à traiter dans le layer des lignes déjà traiter
                arcpy.SelectLayerByLocation_management('lyr_doneLines', 'ARE_IDENTICAL_TO', 'lyr_selectedLines','','ADD_TO_SELECTION')
                # Sélection des points de contours qui intersectent les lignes à traiter
                arcpy.SelectLayerByLocation_management('lyr_pointsContour', 'INTERSECT', 'lyr_selectedLines')       
                
                # Traitement : Si 2 points de contours sont positionnées sur les lignes sélectionnées, alors c'est ok !!! ... On quitte la boucle.
                if int(arcpy.GetCount_management('lyr_pointsContour').getOutput(0)) >= 2:
                    resultEntity = 1
                    break
                
                # Si ce n'est pas ok et que le nombre de lignes sélectionnées pour le traitement n'augmente pas par rapport au dernier passage de la boucle, alors on change la sélection des lignes à traiter. On prend d'autres lignes qui n'ont pas encore été traitées.
                elif compte_selectedLines == int(arcpy.GetCount_management('lyr_selectedLines').getOutput(0)) :
                    # Remise à zéro du compte des lignes séléctionnées à traiter
                    compte_selectedLines=0
                    # Ajout dans le layer des lignes traitées de la sélection des lignes traitées par la boucle précédente
                    arcpy.SelectLayerByLocation_management('lyr_doneLines', 'ARE_IDENTICAL_TO', 'lyr_selectedLines','','ADD_TO_SELECTION')

                    #On stoppe le traitement si on a analyser toutes les lignes...
                    if compteLines == arcpy.GetCount_management('lyr_doneLines').getOutput(0):
                        break
                        
                    # Sélection dans les lignes à traiter des lignes qui n'ont pas encore été traitées
                    arcpy.SelectLayerByLocation_management('lyr_selectedLines', 'ARE_IDENTICAL_TO', 'lyr_doneLines')
                    arcpy.SelectLayerByAttribute_management('lyr_selectedLines', "SWITCH_SELECTION")
                
                    # Sélection d'une des lignes qui n'ont pas encore été traitées
                    for feature_row in arcpy.SearchCursor('lyr_selectedLines'):
                        OBJECTID_value = feature_row.getValue('OBJECTID')
                        break
                    arcpy.SelectLayerByAttribute_management('lyr_selectedLines', "NEW_SELECTION" , ' "OBJECTID" = ' + str(OBJECTID_value))
                
                # Mise à jour du compteur des lignes sélectionnées dans la boucle
                compte_selectedLines = int(arcpy.GetCount_management('lyr_selectedLines').getOutput(0))            
            # Suppression des layers crées au cours du traitement
            arcpy.SelectLayerByAttribute_management('lyr_doneLines', "CLEAR_SELECTION")               
            arcpy.Delete_management("lyr_doneLines")             
            arcpy.SelectLayerByAttribute_management('lyr_selectedLines', "CLEAR_SELECTION")               
            arcpy.Delete_management("lyr_selectedLines")
            arcpy.SelectLayerByAttribute_management('lyr_pointsContour', "CLEAR_SELECTION") 
            arcpy.Delete_management("lyr_pointsContour")
            
            # Remise à zéro de la sélection du polygones et des lignes à l'interieur de ce polygone
            arcpy.SelectLayerByAttribute_management('lyr_areas', "CLEAR_SELECTION")
            arcpy.SelectLayerByAttribute_management('lyr_lines', "CLEAR_SELECTION")   
            
            # Suppression du fichier des points créé pour le traitement
            arcpy.Delete_management(geodatabase_path + "/pointBothEnds")
            
            # S'il n'y a pas de chaine de lignes débutant et finissant sur le polygone et qui le traverse complètement, alors c'est indiqué et on stoppe le traitement...
            if resultEntity == 0:
                # Ajout du polygone dans le listing des erreurs              
                dataset_topologyError = datasetTopage.path(feature1)           
                self.addEntityToRuleError(dataset_topologyError + "/topo_polygon_error",entity,feature1,feature2,"mustBeTransverse_LineArea")
                result = 0
                #break

        arcpy.Delete_management("lyr_areas")  
        arcpy.Delete_management("lyr_lines")
        
        if result == 0:
            return "false"
        else :
            return "true"


    def coincidePointMustHaveAttribute_PointPoint(self,feature1,feature2,field,attribut): 
   
        featureTopage = feature()      
           
        dataset_topologyError = datasetTopage.path(feature1) 
        result = featureTopage.fieldCheck(feature1,field)
          
        if result == 0 :         
            self.addLyrToRuleError(dataset_topologyError + "/topo_point_error",feature1,feature1,feature2,"coincidePointMustHaveAttribute_PointPoint")
            return "erreur -> il n'existe pas de champs " + field + " dans la couche " + feature1
            
        # Sélection des points qui doivent avoir des attributs précis
        arcpy.MakeFeatureLayer_management(feature1, 'lyr_point2check')
        arcpy.SelectLayerByLocation_management('lyr_point2check', 'ARE_IDENTICAL_TO', feature2)
        
        # dictionnaire des attributs
        attribut_dictionary = attribut.split(",")
        
        # Sélection d'une des lignes qui n'ont pas encore été traitées
        for entity in arcpy.da.SearchCursor('lyr_point2check',["SHAPE@","OBJECTID",field]) :#@UndefinedVariable
            #field_value = entity.getValue(field)
            for attribut in attribut_dictionary :
                if entity[2] == attribut :
                    resultEntity = 1
                    break
                else :
                    resultEntity = 0          
                    
            if resultEntity == 0 :
                result=0
                self.addEntityToRuleError(dataset_topologyError + "/topo_point_error",entity,feature1,feature2,"coincidePointMustHaveAttribute_PointPoint")
        
        # Remise à zéro du layer
        arcpy.SelectLayerByAttribute_management('lyr_point2check', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr_point2check")
        
        # Retour de la fonction
        if result == 0:
            return "false"
        else :
            return "true"        
         

    def pointOnLineMustHaveAttribute_PointLine(self,feature1,feature2,field,attribut): 
        
    
        featureTopage = feature()          
           
        dataset_topologyError = datasetTopage.path(feature1)  
        result = featureTopage.fieldCheck(feature1,field)
          
        if result == 0 :         
            self.addLyrToRuleError(dataset_topologyError + "/topo_point_error",feature1,feature1,feature2,"pointOnLineMustHaveAttribute_PointLine")
            return "erreur -> il n'existe pas de champs " + field + " dans la couche " + feature1
            
        # Sélection des points qui doivent avoir des attributs précis
        arcpy.MakeFeatureLayer_management(feature1, 'lyr_point2check')
        arcpy.SelectLayerByLocation_management('lyr_point2check', 'INTERSECT', feature2)
        
        # dictionnaire des attributs
        attribut_dictionary = attribut.split(",")
        
        # Sélection d'une des lignes qui n'ont pas encore été traitées
        for entity in arcpy.da.SearchCursor('lyr_point2check',["SHAPE@","OBJECTID",field]) :#@UndefinedVariable
            #field_value = entity.getValue(field)
            for attribut in attribut_dictionary :
                if entity[2] == attribut :
                    resultEntity = 1
                    break
                else :
                    resultEntity = 0          
                    
            if resultEntity == 0 :
                result=0
                self.addEntityToRuleError(dataset_topologyError + "/topo_point_error",entity,feature1,feature2,"coincidePointMustHaveAttribute_PointPoint")

        
        # Remise à zéro du layer
        arcpy.SelectLayerByAttribute_management('lyr_point2check', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr_point2check")
        
        # Retour de la fonction
        if result == 0:
            return "false"
        else :
            return "true"   

    def pointInAreaMustHaveAttribute_PointArea(self,feature1,feature2,field,attribut): 
          
        featureTopage = feature()      
           
        dataset_topologyError = datasetTopage.path(feature1) 
        result = featureTopage.fieldCheck(feature1,field)
          
        if result == 0 :         
            self.addLyrToRuleError(dataset_topologyError + "/topo_point_error",feature1,feature1,feature2,"coincidePointMustHaveAttribute_PointPoint")
            return "erreur -> il n'existe pas de champs " + field + " dans la couche " + feature1
        
        # Sélection des points qui doivent avoir des attributs précis
        arcpy.MakeFeatureLayer_management(feature1, 'lyr_point2check')
        arcpy.SelectLayerByLocation_management('lyr_point2check', 'INTERSECT', feature2)
        
        # dictionnaire des attributs
        attribut_dictionary = attribut.split(",")
        
        # Sélection d'une des lignes qui n'ont pas encore été traitées
        for entity in arcpy.da.SearchCursor('lyr_point2check',["SHAPE@","OBJECTID",field]) :#@UndefinedVariable
            #field_value = entity.getValue(field)
            for attribut in attribut_dictionary :
                if entity[2] == attribut :
                    resultEntity = 1
                    break
                else :
                    resultEntity = 0          
                    
            if resultEntity == 0 :
                result=0
                self.addEntityToRuleError(dataset_topologyError + "/topo_point_error",entity,feature1,feature2,"coincidePointMustHaveAttribute_PointPoint")
        
        # Remise à zéro du layer
        arcpy.SelectLayerByAttribute_management('lyr_point2check', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr_point2check")
        
        # Retour de la fonction
        if result == 0:
            return "false"
        else :
            return "true"   

    def pointOnPerimetreMustHaveAttribute_PointArea(self,feature1,feature2,field,attribut): 
          
        featureTopage = feature()      
           
        dataset_topologyError = datasetTopage.path(feature1) 
        result = featureTopage.fieldCheck(feature1,field)
          
        if result == 0 :         
            self.addLyrToRuleError(dataset_topologyError + "/topo_point_error",feature1,feature1,feature2,"coincidePointMustHaveAttribute_PointPoint")
            return "erreur -> il n'existe pas de champs " + field + " dans la couche " + feature1
        
        # Sélection des points qui doivent avoir des attributs précis
        arcpy.MakeFeatureLayer_management(feature1, 'lyr_point2check')
        arcpy.SelectLayerByLocation_management('lyr_point2check', 'BOUNDARY_TOUCHES', feature2)
        
        # dictionnaire des attributs
        attribut_dictionary = attribut.split(",")
        
        # Sélection d'une des lignes qui n'ont pas encore été traitées
        for entity in arcpy.da.SearchCursor('lyr_point2check',["SHAPE@","OBJECTID",field]) :#@UndefinedVariable
            #field_value = entity.getValue(field)
            for attribut in attribut_dictionary :
                if entity[2] == attribut :
                    resultEntity = 1
                    break
                else :
                    resultEntity = 0          
                    
            if resultEntity == 0 :
                result=0
                self.addEntityToRuleError(dataset_topologyError + "/topo_point_error",entity,feature1,feature2,"coincidePointMustHaveAttribute_PointPoint")
            
        # Remise à zéro du layer
        arcpy.SelectLayerByAttribute_management('lyr_point2check', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr_point2check")
        
        # Retour de la fonction
        if result == 0:
            return "false"
        else :
            return "true"              

    def pointOn3LineConnectionMustHaveAttribute_PointLine(self,feature1,feature2,field,attribut): 
          
        featureTopage = feature()      
           
        dataset_topologyError = datasetTopage.path(feature1) 
        result = featureTopage.fieldCheck(feature1,field)
          
        if result == 0 :         
            self.addLyrToRuleError(dataset_topologyError + "/topo_point_error",feature1,feature1,feature2,"coincidePointMustHaveAttribute_PointPoint")
            return "erreur -> il n'existe pas de champs " + field + " dans la couche " + feature1
                
        # Layer des lignes
        arcpy.MakeFeatureLayer_management(feature2, 'lyr_lines')
        
        # Sélection des points qui sont sur les lignes
        arcpy.MakeFeatureLayer_management(feature1, 'lyr_point')
        arcpy.SelectLayerByLocation_management('lyr_point', 'INTERSECT', feature2)
        arcpy.MakeFeatureLayer_management('lyr_point', 'lyr_point2check')
        
        # dictionnaire des attributs
        attribut_dictionary = attribut.split(",")

        #shapeName = arcpy.Describe('lyr_point2check').shapeFieldName
        # Boucle sur tous les points hydroNode du réseau
        for entity in arcpy.da.SearchCursor('lyr_point2check',["SHAPE@","OBJECTID",field]):#@UndefinedVariable
            #print entity
            # Sélection des links qui touches les noeuds
            arcpy.SelectLayerByLocation_management('lyr_lines', 'INTERSECT', entity[0])
            # Si plus de 3 lignes touchent le noeud, alors on vérifie la valeur du champs
            if int(arcpy.GetCount_management('lyr_lines').getOutput(0)) >= 3 :

                # Récupération de la valeur du champs
                #field_value = entity[2]
                # Vérification pour voir si la valeur du champs est compris dans le dictionnaire des valeurs autorisées

                for attribut in attribut_dictionary :
                    if entity[2] == attribut :
                        resultEntity = 1
                        break
                    else :
                        resultEntity = 0          
                        
                if resultEntity == 0 :
                    result=0
                    self.addEntityToRuleError(dataset_topologyError + "/topo_point_error",entity,feature1,feature2,"coincidePointMustHaveAttribute_PointPoint")
            
            # Remise à zéro de la sélection des lignes
            arcpy.SelectLayerByAttribute_management('lyr_lines', "CLEAR_SELECTION") 
            
        # Remise à zéro des layers
        arcpy.SelectLayerByAttribute_management('lyr_point2check', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr_point2check")
        arcpy.SelectLayerByAttribute_management('lyr_point', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr_point")
        arcpy.SelectLayerByAttribute_management('lyr_lines', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr_lines")  
        
        # Retour de la fonction
        if result == 0:
            return "false"
        else :
            return "true"   

        
    def mustBeOutside_LineArea(self,feature1,feature2)  :
        # Paramétrage initial du resultat final
        result=1
           
        dataset_topologyError = datasetTopage.path(feature1) 
                
        # Layer des lignes
        arcpy.MakeFeatureLayer_management(feature1, 'lyr_lines')

        arcpy.SelectLayerByLocation_management('lyr_lines', 'INTERSECT', feature2)
        arcpy.MakeFeatureLayer_management('lyr_lines', 'lyr_lines_intersect')
        
        arcpy.SelectLayerByLocation_management('lyr_lines_intersect', 'WITHIN', feature2)
        if int(arcpy.GetCount_management('lyr_lines_intersect').getOutput(0)) > 0 :         
            self.addLyrToRuleError(dataset_topologyError + "/topo_line_error",'lyr_lines_intersect',feature1,feature2,"mustBeOutside_LineArea")
            result = 0

        arcpy.SelectLayerByLocation_management('lyr_lines_intersect', 'BOUNDARY_TOUCHES', feature2)
        if int(arcpy.GetCount_management('lyr_lines_intersect').getOutput(0)) <> int(arcpy.GetCount_management('lyr_lines').getOutput(0)) :
            arcpy.SelectLayerByLocation_management('lyr_lines_intersect', 'ARE_IDENTICAL_TO', 'lyr_lines',"","REMOVE_FROM_SELECTION")         
            self.addLyrToRuleError(dataset_topologyError + "/topo_line_error",'lyr_lines_intersect',feature1,feature2,"mustBeOutside_LineArea")
            result = 0

        arcpy.SelectLayerByAttribute_management('lyr_lines', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr_lines")  
        arcpy.SelectLayerByAttribute_management('lyr_lines_intersect', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr_lines_intersect")  
        
        # Retour de la fonction
        if result == 0 :
            return "false"
        else :
            return "true"   

    def mustBeOutside_PointLine(self,feature1,feature2):
        # Paramétrage initial du resultat final
        result=1
        
        dataset_topologyError = datasetTopage.path(feature1) 
        
        # Layer des lignes
        arcpy.MakeFeatureLayer_management(feature1, 'lyr_points')

        arcpy.SelectLayerByLocation_management('lyr_points', 'INTERSECT', feature2)
        arcpy.MakeFeatureLayer_management('lyr_points', 'lyr_points_intersect')
        
        arcpy.SelectLayerByLocation_management('lyr_points_intersect', 'BOUNDARY_TOUCHES', feature2)
        
        if int(arcpy.GetCount_management('lyr_points_intersect').getOutput(0)) <> int(arcpy.GetCount_management('lyr_points').getOutput(0)) :
            arcpy.SelectLayerByLocation_management('lyr_points_intersect', 'ARE_IDENTICAL_TO', 'lyr_points',"","REMOVE_FROM_SELECTION")   
            self.addLyrToRuleError(dataset_topologyError + "/topo_point_error",'lyr_points_intersect',feature1,feature2,"mustBeOutside_PointLine")
            result = 0

        arcpy.SelectLayerByAttribute_management('lyr_points', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr_points")  
        arcpy.SelectLayerByAttribute_management('lyr_points_intersect', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr_points_intersect")  
        
        # Retour de la fonction
        if result == 0 :
            return "false"
        else :
            return "true"   

    def mustBeOutside_PointArea(self,feature1,feature2):
        # Paramétrage initial du resultat final
        result=1
        
        dataset_topologyError = datasetTopage.path(feature1) 
        
        # Layer des lignes
        arcpy.MakeFeatureLayer_management(feature1, 'lyr_points')

        arcpy.SelectLayerByLocation_management('lyr_points', 'INTERSECT', feature2)        
        if int(arcpy.GetCount_management('lyr_points').getOutput(0)) > 0 :
            self.addLyrToRuleError(dataset_topologyError + "/topo_point_error",'lyr_points',feature1,feature2,"mustBeOutside_PointArea")
            result = 0

        arcpy.SelectLayerByAttribute_management('lyr_points', "CLEAR_SELECTION") 
        arcpy.Delete_management("lyr_points")  
        
        # Retour de la fonction
        if result == 0 :
            return "false"
        else :
            return "true"  
