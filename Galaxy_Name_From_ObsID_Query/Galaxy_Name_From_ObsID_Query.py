import numpy as np
import pandas as pd
import glob

def Gname_Query(ObsID, Data_Path="/opt/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv", Key="Gname"):
    """
    ObsID:-int  Observation ID, The integer ObsID
    Data_Path:-str Data Path, The path to the standard SQL queried CSV file. The standard SQL queried CSV initally defined the sample.
    Key:-str, Key, The key that matches the galaxy name column in the standard SQL queried CSV file

    Output: Gname:-str, Galaxy Name, The name of the galaxy associated with the ObsID

    This function takes an ObsID as an input and returns the associated galaxy observed in that observation.
    """
    #query_path='/Volumes/xray/simon/all_chandra_observations/'+str(ObsID)+'/primary/*evt2*'
    Glob_L=glob.glob(Data_Path)
    if(len(Glob_L)!=1):
        raise Exception("Data_Path has "+str(len(Glob_L))+" Matching Files ! ! !")
    Data_Path=Glob_L[0]
    Data=pd.read_csv(Data_Path)
    #print("Data: ", Data)
    ##Data_Reduced=Data[Data["Obs ID"].isin([ObsID])]
    Data_Reduced=Data[Data["Obs ID"] == ObsID]
    Data_Reduced=Data_Reduced.reset_index(drop=True)
    #print("Data_Reduced: ", Data_Reduced)
    Gname=Data_Reduced[Key].loc[0]
    #print("Gname: ", Gname)
    return Gname

def Gname_Homogenized_Query(ObsID, Data_Path="/opt/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified_2.csv", Key="Galaxy_Name_Homogenized"):
    """
    ObsID:-int  Observation ID, The integer ObsID
    Data_Path:-str Data Path, The path to the standard SQL queried CSV file. The standard SQL queried CSV initally defined the sample.
    Key:-str, Key, The key that matches the galaxy name column in the standard SQL queried CSV file

    Output: Gname:-str, Galaxy Name, The name of the galaxy associated with the ObsID

    This function takes an ObsID as an input and returns the associated galaxy observed in that observation.
    """
    #query_path='/Volumes/xray/simon/all_chandra_observations/'+str(ObsID)+'/primary/*evt2*'
    Glob_L=glob.glob(Data_Path)
    if(len(Glob_L)!=1):
        raise Exception("Data_Path has "+str(len(Glob_L))+" Matching Files ! ! !")
    Data_Path=Glob_L[0]
    Data=pd.read_csv(Data_Path)
    #print("Data: ", Data)
    ##Data_Reduced=Data[Data["Obs ID"].isin([ObsID])]
    Data_Reduced=Data[Data["Obs ID"] == ObsID]
    Data_Reduced=Data_Reduced.reset_index(drop=True)
    #print("Data_Reduced: ", Data_Reduced)
    Gname=Data_Reduced[Key].loc[0]
    #print("Gname: ", Gname)
    return Gname

#print(Gname_Query(10125))
#print(Gname_Homogenized_Query(10125))
