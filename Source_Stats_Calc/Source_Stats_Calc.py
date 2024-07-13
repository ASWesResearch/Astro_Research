import numpy as np
import pandas as pd
import re
def Parse_List(L):
    if(len(L)==2):
        return []
    Element_L=re.split("[\[\],]", L)
    #print("Element_L: ", Element_L)
    Element_L_Whitespace_Removed=[]
    for Element in Element_L:
        #Element_L_Whitespace_Removed.append(Element.strip())
        Element_L_Whitespace_Removed.append(Element.replace(" ", ""))
    Element_L=Element_L_Whitespace_Removed
    #print("Element_L: ", Element_L)
    HL=[]
    for i in range(0,len(Element_L)-1, 2):
        j=i+1
        #print("i: ", i)
        #print("j: ", j)
        ObsID=Element_L[i]
        if(ObsID==""):
            continue
        ObsID=int(ObsID)
        Src_Num=int(Element_L[j])
        Cur_L=[ObsID,Src_Num]
        HL.append(Cur_L)
    return HL

def Duplicate_Source_Count(Fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/Source_Flux_All_Modified_3.csv",Keys=["ObsID","Source_Num","Duplicate_Sources"]):
    Data=pd.read_csv(Fpath)
    ObsID_A=Data[Keys[0]]
    ObsID_L=list(ObsID_A)
    Src_Num_A=Data[Keys[1]]
    Src_Num_L=list(Src_Num_A)
    Duplicate_Sources_A=Data[Keys[2]]
    Duplicate_Sources_L=list(Duplicate_Sources_A)
    #print("ObsID_A:\n", ObsID_A)
    #print("Src_Num_A:\n", Src_Num_A)
    #print("Duplicate_Sources_A:\n", Duplicate_Sources_A)
    Duplicate_L=[]
    for i in range(0,len(Duplicate_Sources_L)):
        Cur_ObsID=ObsID_L[i]
        Cur_Source=Src_Num_L[i]
        Cur_Group=[Cur_ObsID, Cur_Source]
        if(Cur_Group in Duplicate_L):
            continue
        Cur_Dup_Source_Str=Duplicate_Sources_L[i]
        Cur_Dup_Source_L=Parse_List(Cur_Dup_Source_Str)
        for Cur_Dup in Cur_Dup_Source_L:
            if Cur_Dup not in Duplicate_L:
                Duplicate_L.append(Cur_Dup)
        #print("Cur_Dup_Source_L: ", Cur_Dup_Source_L)
        #print("type(Cur_Dup_Source_L): ", type(Cur_Dup_Source_L))
    print("Duplicate_L:\n", Duplicate_L)
    print("len(Duplicate_L): ", len(Duplicate_L))

Duplicate_Source_Count()
