import pandas as pd
import numpy as np
import os
from os import system
def Counter(fname):
    #SQL_Data=pd.read_csv("SQL_Standard_File.csv")
    fpath=os.path.realpath('../SQL_Standard_File/'+fname)
    #print "fpath : ", fpath
    SQL_Data=pd.read_csv(fpath)
    #Galaxy_Name_Data=pd.read_csv("Galaxy_List.csv")
    #Galaxy_Name_Data_L=list(Galaxy_Name_Data['queriedName'])
    #print "Galaxy_Name_Data_L : ", Galaxy_Name_Data_L
    #print SQL_Data
    #SQL_Data_L=list(SQL_Data)
    #print (SQL_Data_L)
    #total_rows = (SQL_Data.count)
    #total_rows=total_rows+1
    SQL_Data_Shape=SQL_Data.shape
    #print "SQL_Data_Shape : ", SQL_Data_Shape
    #print "total_rows : ", total_rows
    Num_Rows=SQL_Data_Shape[0]
    #print "Num_Rows : ", Num_Rows
    #print "type(Num_Rows) : ", type(Num_Rows)
    Num_Sources=Num_Rows
    print "Num_Sources : ", Num_Sources
    #obsid
    #Obs_ID_Table=SQL_Data['obsid']
    #OBSID
    Obs_ID_Table=SQL_Data['OBSID']
    #print "Obs_ID_Table : ", Obs_ID_Table
    #Obs_ID_L=list(Obs_ID_Table)
    #print "Obs_ID_L : ", Obs_ID_L
    #for Obs_ID in Obs_ID_L:
    #resolvedObject
    Obs_ID_Table_Grouped=SQL_Data.groupby('OBSID')['resolvedObject'].nunique()
    #print "Obs_ID_Table_Grouped : ", Obs_ID_Table_Grouped
    Obs_ID_Table_Grouped_Shape=Obs_ID_Table_Grouped.shape
    Num_ObsIDs=Obs_ID_Table_Grouped_Shape[0]
    print "Num_ObsIDs : ", Num_ObsIDs
    #print "type(Num_ObsIDs) : ", type(Num_ObsIDs)
    Gname_Table_Grouped=SQL_Data.groupby('resolvedObject')['OBSID'].nunique()
    #print Gname_Table_Grouped
    #Gname_A_Grouped=np.array(Gname_Table_Grouped)
    #print "Gname_A_Grouped : ", Gname_A_Grouped
    Gname_Table_Grouped_Shape=Gname_Table_Grouped.shape
    Num_Gname=Gname_Table_Grouped_Shape[0]
    print "Num_Gname : ", Num_Gname
    #print "type(Num_Gname) : ", type(Num_Gname)
    Name_Table=SQL_Data['resolvedObject']
    #print "Name_Table : \n", Name_Table
    Name_L=list(Name_Table)
    #print "Name_L : ", Name_L
    Name_L_Unique=set(Name_L)
    print "Name_L_Unique : ", Name_L_Unique
    #print "len(Name_L_Unique) : ", len(Name_L_Unique)

Counter("Source_Flux_Table.csv")
