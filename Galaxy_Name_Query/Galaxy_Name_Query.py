import numpy as np
import pandas as pd
from astroquery.ned import Ned
"""
import astropy.units as u
import os
from os import system
import sys
dir = os.path.dirname(__file__)
path=os.path.realpath('../')
sys.path.append(os.path.abspath(path))
from Galaxy_Name_Reducer import Galaxy_Name_Reducer
from D25_Finder import D25_Finder
"""
def Galaxy_Name_Query(Gname):
    Galaxy_Bool=True
    try:
        result_table = Ned.query_object(Gname)
    except:
        return False
    #print "result_table\n", result_table
    #print result_table['Object Name']
    #print result_table['Type']
    Object_Type=result_table['Type']
    #print "Object_Type: ", Object_Type
    if((Object_Type!="G") and (Object_Type!="GPair")):
        #print str(Gname)+" is not a Galaxy"
        Galaxy_Bool=False
        #D25=D25_Finder.D25_Finder(Gname)
        #print "D25: ", D25
        #result_table_distance = Ned.query_region(Gname, radius=10.0*0.166666 * u.deg)
        #print result_table_distance
    Gname_Queried_Table=result_table['Object Name']
    Gname_Queried=list(Gname_Queried_Table)[0]
    #print "Gname_Queried: ", Gname_Queried
    #print "Object_Type: ", Object_Type
    #print "Galaxy_Bool: ", Galaxy_Bool
    return Gname_Queried, Galaxy_Bool

def Galaxy_Name_Query_Big_Input(Remove_Duplicates=True):
    #"""
    Gname_Queried_File=open("Gname_Queried.csv", "w")
    Gname_Queried_Only_Galaxies_File=open("Gname_Queried_Only_Galaxies.csv", "w")
    Header="Object_Name,Queried_Gname\n"
    Gname_Queried_File.write(Header)
    Gname_Queried_Only_Galaxies_File.write(Header)
    New_A=pd.read_csv("/Volumes/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv")
    ##New_A=New_A[New_A["Exposure "]>9.0]
    Gname_A=New_A["Target Name"]
    Gname_L=list(Gname_A)
    #"""
    if(Remove_Duplicates):
        Gname_L=list(set(Gname_L))
    #Gname_Queried_A=np.vectorize(Galaxy_Name_Query)(Gname_A)
    Gname_Error_L=[]
    Non_Galaxy_L=[]
    Gname_Queried_L=[]
    for Gname in Gname_L:
        try:
            Galaxy_Data=Galaxy_Name_Query(Gname)
            Gname_Queried=Galaxy_Data[0]
            Galaxy_Bool=Galaxy_Data[1]
            Gname_Queried_L.append(Gname_Queried)
            Gname_Queried_File.write(Gname+','+Gname_Queried+'\n')
            if(Galaxy_Bool==False):
                Non_Galaxy_L.append(Gname_Queried)
            if(Galaxy_Bool==True):
                Gname_Queried_Only_Galaxies_File.write(Gname+','+Gname_Queried+'\n')
        except:
            Gname_Error_L.append(Gname)
    #print "Gname_Error_L: ", Gname_Error_L
    if(Remove_Duplicates):
        Gname_Queried_L=list(set(Gname_Queried_L))
    print "Gname_Error_L:/n", Gname_Error_L
    print "Non_Galaxy_L:/n", Non_Galaxy_L
    Gname_Queried_File.close()
    Gname_Queried_Only_Galaxies_File.close()
    return Gname_Queried_L
"""
def Radius_Test(Gname):
    #result_table_distance = Ned.query_region(Gname, radius=10.0*0.166666 * u.deg)
    result_table_distance = Ned.query_region("3c 273", radius=10.0*0.166666 * u.deg)
    return result_table_distance
"""
#print Galaxy_Name_Query("NGC 224")
#print Galaxy_Name_Query("Centaurus A")
#print Galaxy_Name_Query("NGC 7741")
#print Radius_Test("NGC 224")
print Galaxy_Name_Query_Big_Input()
