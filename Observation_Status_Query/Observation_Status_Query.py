import os
from os import system
import sys
from ciao_contrib.runtool import * #Imports ciao tools into python
import re
import pandas as pd
def Observation_Status_Query(ObsID,Threshold=22480):
    #Query_Str=os.popen('find_chandra_obsid '+str(ObsID)+' verbose=3').read()
    #print("Query_Str:\n", Query_Str)
    print("ObsID: "+str(ObsID))
    ObsID_Int=int(ObsID)
    if(ObsID_Int<Threshold):
        print("Observed_Status_Str_Reduced: ", "archived")
        return [ObsID, True, "archived"]
    Observed_Status_Str=os.popen("find_chandra_obsid "+str(ObsID)+" verbose=2 | grep 'status'").read()
    #print("Observed_Status_Str: ", Observed_Status_Str)
    Observed_Status_Str_Reduced=re.split(r"\s+", Observed_Status_Str)[2].split("=")[1]
    print("Observed_Status_Str_Reduced: ", Observed_Status_Str_Reduced)
    if(Observed_Status_Str_Reduced=="archived"):
        Data_Availability_Bool=True
    else:
        Data_Availability_Bool=False
    return [ObsID, Data_Availability_Bool, Observed_Status_Str_Reduced]
    """
    #find_chandra_obsid 22481 verbose=3 | grep  "PUBLIC_AVAIL"
    Availability_Status_Header_Str=os.popen("find_chandra_obsid "+str(ObsID)+" verbose=3 | grep  'PUBLIC_AVAIL'").read()
    print("Availability_Status_Header_Str:\n", Availability_Status_Header_Str)
    Availability_Status_Header_Str_L=re.split(r"\s+", Availability_Status_Header_Str)
    print("Availability_Status_Header_Str_L:\n", Availability_Status_Header_Str_L)
    # find_chandra_obsid 22481 verbose=3 | grep -A2 "PUBLIC_AVAIL" | tail -n 1
    Availability_Status_Data_Str=os.popen("find_chandra_obsid "+str(ObsID)+" verbose=3 | grep -A2 'PUBLIC_AVAIL' | tail -n 1").read()
    print("Availability_Status_Data_Str:\n", Availability_Status_Data_Str)
    Availability_Status_Data_Str_L=re.split(r"\s+", Availability_Status_Data_Str)
    print("Availability_Status_Data_Str_L:\n", Availability_Status_Data_Str_L)
    """
def Observation_Status_Query_Big_Input(ObsID_L, Outpath="", Outfile_Bool=False):
    ObsID_Status_L=[]
    ObsID_Status_Dict={}
    for ObsID in ObsID_L:
        Cur_ObsID_Status=Observation_Status_Query(ObsID)
        ObsID_Status_L.append(Cur_ObsID_Status)
        ObsID_Status_Dict[ObsID]=Cur_ObsID_Status[1:]
    if(Outfile_Bool):
        f=open(Outpath+"Observation_Status.csv","w")
        Header="ObsID,Data_Availability_Bool,Observation_Status"+"\n"
        f.write(Header)
        for Cur_ObsID_Status in ObsID_Status_L:
            Cur_Line=str(Cur_ObsID_Status[0])+","+str(Cur_ObsID_Status[1])+","+str(Cur_ObsID_Status[2])+"\n"
            f.write(Cur_Line)
        f.close()
    return ObsID_Status_L, ObsID_Status_Dict
#/opt/xray/anthony/Research_Git/SQL_Standard_File

def Read_ObsIDs(Fpath,Remove_Dups=True,Raw=False):
    if(Raw):
        #pass
        File = open(Fpath, "r")
        #for line in range(1,File):
        ObsID_L_With_Head=[]
        for Line in File:
            #print(Line)
            ObsID_Str_With_Head=Line.split(",")[1]
            #print(ObsID_Str_With_Head)
            ObsID_L_With_Head.append(ObsID_Str_With_Head)
        ObsID_Str_L=ObsID_L_With_Head[1:]
        ObsID_L=[]
        for ObsID_Str in ObsID_Str_L:
            ObsID=int(ObsID_Str)
            ObsID_L.append(ObsID)
        #print(ObsID_L)
    else:
        Data=pd.read_csv(Fpath)
        ObsID_A=Data["Obs ID"]
        ObsID_L=list(ObsID_A)
    if(Remove_Dups):
        ObsID_L_With_Dups=ObsID_L
        ObsID_L=list(set(ObsID_L))
        print("Number of Duplicates: ",len(ObsID_L_With_Dups)-len(ObsID_L))
    return ObsID_L

#Observation_Status_Query(22481)
#Observation_Status_Query(253)
#print(Observation_Status_Query_Big_Input([22481, 253]))

def Main():
    pass
    #"/opt/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv"
    #ObsID_L=Read_ObsIDs("/opt/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv",Remove_Dups=False,Raw=True)
    #ObsID_L=Read_ObsIDs("/opt/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv",Remove_Dups=False,Raw=False)
    #print("ObsID_L: ", ObsID_L)
    #print(Observation_Status_Query_Big_Input(ObsID_L,Outfile_Bool=True))
    #print(Observation_Status_Query_Big_Input(ObsID_L,Outfile_Bool=False))

#Main()
