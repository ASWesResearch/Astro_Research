import pandas as pd
import os
import sys
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))
from Observation_Status_Query import Observation_Status_Query
def Read_ObsIDs(Fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv",Remove_Dups=True,Raw=False, Remove_Unarchived=False):
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
    if(Remove_Unarchived==True):
        ObsID_L_Archived=[]
        Observation_Status_Query_L=Observation_Status_Query.Observation_Status_Query_Big_Input(ObsID_L)
        print("Observation_Status_Query_L: ", Observation_Status_Query_L)
        ObsID_Status_L=Observation_Status_Query_L[0]
        for Cur_ObsID_Status in ObsID_Status_L:
            Data_Availability_Bool=Cur_ObsID_Status[1]
            Cur_ObsID=Cur_ObsID_Status[0]
            if(Data_Availability_Bool==True):
                ObsID_L_Archived.append(int(Cur_ObsID))
        return ObsID_L_Archived
    return ObsID_L

#ObsID_L=Read_ObsIDs(Remove_Unarchived=True)
#print(ObsID_L)
#print("len(ObsID_L): ", len(ObsID_L))
