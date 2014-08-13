# -*- coding: utf-8 -*-

## Chargement des librairies Pythons
import arcpy

class feature:

    ### SCRIPT ###   
    ## MERGE D'UNE LISTE DE FICHIERS DANS UN REPERTOIRE SOURCE
    def create(self,destination_folder,file_name,geometry_type,srid=""):
        try:   
            if arcpy.Exists(destination_folder + "/" + file_name):
                arcpy.Delete_management(destination_folder + "/" + file_name)             

            arcpy.CreateFeatureclass_management(destination_folder,file_name,geometry_type)

        except Exception as e:
            print e.message
            arcpy.AddError(e.message)   
        
    ## MERGE D'UNE LISTE DE FICHIERS DANS UN REPERTOIRE SOURCE
    def copy(self,source_file,destination_file):
        try:
           
            if arcpy.Exists(destination_file):
                arcpy.Delete_management(destination_file)             
                
            arcpy.CopyFeatures_management(source_file,destination_file)
            
        except Exception as e:
            print e.message
            arcpy.AddError(e.message)

    
    ## MERGE D'UNE LISTE DE FICHIERS DANS UN REPERTOIRE SOURCE
    def merge(self,featureList,destination_file):
        try:
           
            if arcpy.Exists(destination_file):
                arcpy.Delete_management(destination_file)             
                
            arcpy.Merge_management(featureList,destination_file)
            
        except Exception as e:
            print e.message
            arcpy.AddError(e.message)


    ## MERGE D'UNE LISTE DE FICHIERS DANS UN REPERTOIRE SOURCE
    def checkPresence(self,feature_path):
        if arcpy.Exists(feature_path):
            return "True"
        else :
            return "False"

            
    def delete(self,feature):
        if arcpy.Exists(feature):
            arcpy.Delete_management(feature)        

            
    def fieldCheck(self,feature,field):
        result = 0
        
        fieldList = arcpy.ListFields(feature)
        for field_test in fieldList :
            if field_test.name ==  field : 
                result = 1

        return result
        
    def addField(self,feature,field,fieldType):
        try:   
            fieldList = arcpy.ListFields(feature)
            for field_test in fieldList :
                if field_test.name ==  field : 
                    arcpy.DeleteField_management(feature,[field])
            
            arcpy.AddField_management(feature, field, fieldType)
            
        except Exception as e:
            print e.message
            arcpy.AddError(e.message)         