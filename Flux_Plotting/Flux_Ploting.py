import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import re
from datetime import datetime

def Morph_Check(Morph_Str):
    if(isinstance(Morph_Str,float)):
        return np.nan
    Morph_L=["S","E","I"]
    for Morph in Morph_L:
        if(Morph in Morph_Str):
            return Morph
"""
def Color_Color_Calc(S,M,H):
    if((H+M==0.0) or (M+S==0.0)):
        print("Error_Flux: ", str((H+M,M+S)))
        return np.nan
    HC_Ratio=(H-M)/((H+M))
    SC_Ratio=(M-S)/((M+S))
    return HC_Ratio, SC_Ratio
"""
def Color_Color_Calc(S,M,H):
    if(H+M==0.0):
        HC_Ratio=np.nan
    else:
        HC_Ratio=(H-M)/((H+M))
    if(M+S==0.0):
        SC_Ratio=np.nan
    else:
        SC_Ratio=(M-S)/((M+S))
    return HC_Ratio, SC_Ratio

def Color_Color_Plot(Data):
    pass

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

#def Find_Source(ObsID,Source_Num,Standard_File_Fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/Source_Flux_All_Modified_3.csv"):
def Find_Source(Data,ObsID,Source_Num):
    #Data=pd.read_csv(Standard_File_Fpath)
    Data_Matched=Data[(Data["ObsID"]==ObsID) & (Data["Source_Num"]==Source_Num)]
    return Data_Matched

def Find_Duplicate(Data,ObsID,Source_Num):
    #Data_Matched=Find_Source(ObsID,Source_Num)
    Data_Matched=Find_Source(Data,ObsID,Source_Num)
    Duplicate_HL=list(Data_Matched["Duplicate_Sources"])
    #print("Duplicate_HL: ", Duplicate_HL)
    Duplicate_L=Parse_List(Duplicate_HL[0])
    if(len(Duplicate_L)==0):
        return np.nan
    #print("Duplicate_L: ", Duplicate_L)
    #return Duplicate_L
    i=0
    #Duplicate_Data
    for Duplicate in Duplicate_L:
        Cur_ObsID=Duplicate[0]
        Cur_Source_Num=Duplicate[1]
        print("Cur_Source_Num: ", Cur_Source_Num)
        #Data_Matched=Find_Source(Cur_ObsID,Cur_Source_Num)
        Data_Matched=Find_Source(Data,Cur_ObsID,Cur_Source_Num)
        if(i==0):
            Duplicate_Data=Data_Matched
        if(i>0):
            Data_Matched=pd.concat([Data_Matched, Duplicate_Data])
        i=i+1
    return Data_Matched

def Duplicate_Table_Calc(Standard_File_Fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/Source_Flux_All_Modified_3.csv"):
    Data=pd.read_csv(Standard_File_Fpath)
    Data=Data[Data["NET_COUNTS_0.3-8.0"]>25.0]
    ObsID_A=Data["ObsID"]
    ObsID_L=list(ObsID_A)
    Src_Num_A=Data["Source_Num"]
    Src_Num_L=list(Src_Num_A)
    Counts_A=Data["NET_COUNTS_0.3-8.0"]
    Counts_L=list(Counts_A)
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Soft_Flux_L=list(Soft_Flux)
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Medium_Flux_L=list(Medium_Flux)
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    Hard_Flux_L=list(Hard_Flux)
    Colors_Tuple_A=np.vectorize(Color_Color_Calc)(Soft_Flux,Medium_Flux,Hard_Flux)
    HC_Ratio_A=Colors_Tuple_A[0]
    HC_Ratio_L=list(HC_Ratio_A)
    SC_Ratio_A=Colors_Tuple_A[1]
    SC_Ratio_L=list(SC_Ratio_A)
    Data["Hard_Color_Flux"]=HC_Ratio_A
    Data["Soft_Color_Flux"]=SC_Ratio_A
    Start_Date_A=Data["Start_Date"]
    Start_Date_L=list(Start_Date_A)

    Soft_Lum=Data["NET_LUM_APER_0.3-1.0"]
    Soft_Lum_L=list(Soft_Lum)
    Medium_Lum=Data["NET_LUM_APER_1.0-2.1"]
    Medium_Lum_L=list(Medium_Lum)
    Hard_Lum=Data["NET_LUM_APER_2.1-7.5"]
    Hard_Lum_L=list(Hard_Lum)
    file=open("Duplicate_Colors.csv","w")
    #file.write("ObsID,Dup_ObsID,Source_Num,Dup_Souce_Num,Counts,Dup_Counts,Hard_Color_Flux,Soft_Color_Flux,Dup_Hard_Color_Flux,Dup_Soft_Color_Flux\n")
    #file.write("ObsID,Dup_ObsID,Source_Num,Dup_Souce_Num,Counts,Dup_Counts,Hard_Color_Flux,Soft_Color_Flux,Dup_Hard_Color_Flux,Dup_Soft_Color_Flux,Soft_Flux,Medium_Flux,Hard_Flux,Dup_Soft_Flux,Dup_Medium_Flux,Dup_Hard_Flux\n")
    ##file.write("ObsID,Dup_ObsID,Source_Num,Dup_Souce_Num,Counts,Dup_Counts,Hard_Color_Flux,Soft_Color_Flux,Dup_Hard_Color_Flux,Dup_Soft_Color_Flux,Soft_Flux,Medium_Flux,Hard_Flux,Dup_Soft_Flux,Dup_Medium_Flux,Dup_Hard_Flux,Start_Date,Dup_Start_Date\n")
    file.write("ObsID,Dup_ObsID,Source_Num,Dup_Souce_Num,Counts,Dup_Counts,Hard_Color_Flux,Soft_Color_Flux,Dup_Hard_Color_Flux,Dup_Soft_Color_Flux,Soft_Flux,Medium_Flux,Hard_Flux,Dup_Soft_Flux,Dup_Medium_Flux,Dup_Hard_Flux,Start_Date,Dup_Start_Date,Soft_Lum,Medium_Lum,Hard_Lum,Dup_Soft_Lum,Dup_Medium_Lum,Dup_Hard_Lum,\n")
    for i in range(0,len(ObsID_L)):
        #for i in range(0,200): #For testing
        Cur_ObsID=ObsID_L[i]
        Cur_Src_Num=Src_Num_L[i]
        Cur_Counts=Counts_L[i]
        Cur_HC_Ratio=HC_Ratio_L[i]
        Cur_SC_Ratio=SC_Ratio_L[i]
        Cur_Soft_Flux=Soft_Flux_L[i]
        Cur_Medium_Flux=Medium_Flux_L[i]
        Cur_Hard_Flux=Hard_Flux_L[i]
        Cur_Start_Date=Start_Date_L[i]

        Cur_Soft_Lum=Soft_Lum_L[i]
        Cur_Medium_Lum=Medium_Lum_L[i]
        Cur_Hard_Lum=Hard_Lum_L[i]
        #Cur_Dup_Data=Find_Duplicate(Cur_ObsID,Cur_Src_Num)
        Cur_Dup_Data=Find_Duplicate(Data,Cur_ObsID,Cur_Src_Num)
        #print("Cur_Dup_Data:\n ", Cur_Dup_Data)
        #if(Cur_Dup_Data==np.nan):
        if((isinstance(Cur_Dup_Data,float)) or (Cur_Dup_Data.empty)):
            print("NaN Found!")
            continue
        print("Cur_Dup_Data: ", Cur_Dup_Data)
        print("type(Cur_Dup_Data): ", type(Cur_Dup_Data))
        Cur_First_Dup_Data=Cur_Dup_Data.head(1)
        ObsID_Dup=Cur_First_Dup_Data.iloc[0]["ObsID"]
        Source_Num_Dup=Cur_First_Dup_Data.iloc[0]["Source_Num"]
        Counts_Dup=Cur_First_Dup_Data.iloc[0]["NET_COUNTS_0.3-8.0"]

        #"""
        Counts_First_Dup_A=Cur_First_Dup_Data["NET_COUNTS_0.3-8.0"]
        Soft_Flux_First_Dup=Cur_First_Dup_Data.iloc[0]["NET_FLUX_APER_0.3-1.0"]
        print("Soft_Flux_First_Dup: ", Soft_Flux_First_Dup)
        Medium_Flux_First_Dup=Cur_First_Dup_Data.iloc[0]["NET_FLUX_APER_1.0-2.1"]
        print("Medium_Flux_First_Dup: ", Medium_Flux_First_Dup)
        Hard_Flux_First_Dup=Cur_First_Dup_Data.iloc[0]["NET_FLUX_APER_2.1-7.5"]
        print("Hard_Flux_First_Dup: ", Hard_Flux_First_Dup)
        #Colors_Tuple_A=np.vectorize(Color_Color_Calc)(Soft_Flux_First_Dup,Medium_Flux_First_Dup,Hard_Flux_First_Dup)
        #"""
        HC_Dup=Cur_Dup_Data.iloc[0]["Hard_Color_Flux"]
        SC_Dup=Cur_Dup_Data.iloc[0]["Soft_Color_Flux"]
        Dup_Start_Date=Cur_Dup_Data.iloc[0]["Start_Date"]

        Soft_Lum_First_Dup=Cur_First_Dup_Data.iloc[0]["NET_LUM_APER_0.3-1.0"]
        print("Soft_Lum_First_Dup: ", Soft_Lum_First_Dup)
        Medium_Lum_First_Dup=Cur_First_Dup_Data.iloc[0]["NET_LUM_APER_1.0-2.1"]
        print("Medium_Lum_First_Dup: ", Medium_Lum_First_Dup)
        Hard_Lum_First_Dup=Cur_First_Dup_Data.iloc[0]["NET_LUM_APER_2.1-7.5"]
        print("Hard_Lum_First_Dup: ", Hard_Lum_First_Dup)

        print("Cur_ObsID: ", Cur_ObsID)
        print("Cur_Src_Num: ", Cur_Src_Num)
        print("Source_Num_Dup: ", Source_Num_Dup)
        print("Cur_Counts: ", Cur_Counts)
        print("Counts_Dup: ", Counts_Dup)
        print("Cur_HC_Ratio: ", Cur_HC_Ratio)
        print("Cur_SC_Ratio: ", Cur_SC_Ratio)
        print("HC_Dup: ", HC_Dup)
        print("SC_Dup: ", SC_Dup)
        #Row_String=str(Cur_ObsID)+","+str(Cur_Src_Num)+","+str(Source_Num_Dup)+","+str(Cur_Counts)+","+str(Counts_Dup)+","+str(Cur_HC_Ratio)+","+str(Cur_SC_Ratio)+","+str(HC_Dup)+","+str(SC_Dup)+"\n"
        ##Row_String=str(int(Cur_ObsID))+","+str(int(ObsID_Dup))+","+str(int(Cur_Src_Num))+","+str(int(Source_Num_Dup))+","+str(float(Cur_Counts))+","+str(float(Counts_Dup))+","+str(float(Cur_HC_Ratio))+","+str(float(Cur_SC_Ratio))+","+str(float(HC_Dup))+","+str(float(SC_Dup))+"\n"
        #Row_String=str(Cur_ObsID)+","+str(ObsID_Dup)+","+str(Cur_Src_Num)+","+str(Source_Num_Dup)+","+str(Cur_Counts)+","+str(Counts_Dup)+","+str(Cur_HC_Ratio)+","+str(Cur_SC_Ratio)+","+str(HC_Dup)+","+str(SC_Dup)+"\n"
        ##Row_String=str(int(Cur_ObsID))+","+str(int(ObsID_Dup))+","+str(int(Cur_Src_Num))+","+str(int(Source_Num_Dup))+","+str(float(Cur_Counts))+","+str(float(Counts_Dup))+","+str(float(Cur_HC_Ratio))+","+str(float(Cur_SC_Ratio))+","+str(float(HC_Dup))+","+str(float(SC_Dup))+","+str(float(Cur_Soft_Flux))+","+str(float(Cur_Medium_Flux))+","+str(float(Cur_Hard_Flux))+","+str(float(Soft_Flux_First_Dup))+","+str(float(Medium_Flux_First_Dup))+","+str(float(Hard_Flux_First_Dup))+"\n"
        ##Row_String=str(int(Cur_ObsID))+","+str(int(ObsID_Dup))+","+str(int(Cur_Src_Num))+","+str(int(Source_Num_Dup))+","+str(float(Cur_Counts))+","+str(float(Counts_Dup))+","+str(float(Cur_HC_Ratio))+","+str(float(Cur_SC_Ratio))+","+str(float(HC_Dup))+","+str(float(SC_Dup))+","+str(float(Cur_Soft_Flux))+","+str(float(Cur_Medium_Flux))+","+str(float(Cur_Hard_Flux))+","+str(float(Soft_Flux_First_Dup))+","+str(float(Medium_Flux_First_Dup))+","+str(float(Hard_Flux_First_Dup))+","+str(Cur_Start_Date)+","+str(Dup_Start_Date)+"\n"
        Row_String=str(int(Cur_ObsID))+","+str(int(ObsID_Dup))+","+str(int(Cur_Src_Num))+","+str(int(Source_Num_Dup))+","+str(float(Cur_Counts))+","+str(float(Counts_Dup))+","+str(float(Cur_HC_Ratio))+","+str(float(Cur_SC_Ratio))+","+str(float(HC_Dup))+","+str(float(SC_Dup))+","+str(float(Cur_Soft_Flux))+","+str(float(Cur_Medium_Flux))+","+str(float(Cur_Hard_Flux))+","+str(float(Soft_Flux_First_Dup))+","+str(float(Medium_Flux_First_Dup))+","+str(float(Hard_Flux_First_Dup))+","+str(Cur_Start_Date)+","+str(Dup_Start_Date)+","+str(float(Cur_Soft_Lum))+","+str(float(Cur_Medium_Lum))+","+str(float(Cur_Hard_Lum))+","+str(float(Soft_Lum_First_Dup))+","+str(float(Medium_Lum_First_Dup))+","+str(float(Hard_Lum_First_Dup))+"\n"

        print("Row_String: ", Row_String)
        file.write(Row_String)
    file.close()

def Exp(X,a,b,c,E):
    return a*((X-b)**E)+c

#def Thermal_SN_Calc(Standard_File_Fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/Source_Flux_All_Modified_4.csv", SN_Fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/Thermal_SNs.csv",Tolerance=0.0005):
#def Thermal_SN_Calc(Data, SN_Fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/Thermal_SNs.csv",Tolerance=0.0005):

def Haversine_Distance(x1,x2,y1,y2):
    dx=x2-x1
    dy=y2-y1
    B=np.sqrt(((np.sin(dy/2.0))**2.0)+((np.cos(y1)*np.cos(y2))*((np.sin(dx/2.0))**2.0)))
    if(y1<0): #Note: This might not work for galaxies on the equator! This needs to be tested! #Note: This works on the equator as well!
        B=-1.0*B
    Have_Dist=2.0*np.arcsin(B)
    return Have_Dist

def HMS_to_Decimal_Deg_Convert(H,M,S):
    H_Decimal=H+(M/60.0)+(S/3600.0)
    Deg_Decimal=H_Decimal*15.0
    return Deg_Decimal

def HMS_Str_to_Decimal_Deg_Convert(HMS_Str):
    #13 36 50.00
    HMS_Str_L=HMS_Str.split(" ")
    H=float(HMS_Str_L[0])
    M=float(HMS_Str_L[1])
    S=float(HMS_Str_L[2])
    Deg_Decimal=HMS_to_Decimal_Deg_Convert(H,M,S)
    return Deg_Decimal

def DMS_to_Decimal_Deg_Convert(D,M,S):
    Negtive_Bool=False
    if(D<0):
        D=-1.0*D
        Negtive_Bool=True
    Deg_Decimal=D+(M/60.0)+(S/3600.0)
    if(Negtive_Bool):
        Deg_Decimal=-1.0*Deg_Decimal
    return Deg_Decimal

def DMS_Str_to_Decimal_Deg_Convert(DMS_Str):
    #-29 52 43.36
    DMS_Str_L=DMS_Str.split(" ")
    D=float(DMS_Str_L[0])
    M=float(DMS_Str_L[1])
    S=float(DMS_Str_L[2])
    Deg_Decimal=DMS_to_Decimal_Deg_Convert(D,M,S)
    return Deg_Decimal

def Thermal_SN_Calc(Data, SN_Fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/Thermal_SNs_V2_Modified.csv",Tolerance=0.0005):
    #Data=pd.read_csv(Standard_File_Fpath)
    SN_Data=pd.read_csv(SN_Fpath)
    #Lum_A=np.vectorize(Luminosity_Calc)(Flux_A,Dist_A)
    SN_Data["RA"]=np.vectorize(HMS_Str_to_Decimal_Deg_Convert)(SN_Data["RA_HMS"])
    SN_Data["Dec"]=np.vectorize(DMS_Str_to_Decimal_Deg_Convert)(SN_Data["Dec_DMS"])
    RA_A=SN_Data["RA"]
    RA_L=list(RA_A)
    Dec_A=SN_Data["Dec"]
    Dec_L=list(Dec_A)
    RA_Test_A=Data["RA"]
    RA_Test_L=list(RA_Test_A)
    Dec_Test_A=Data["Dec"]
    Dec_Test_L=list(Dec_Test_A)
    Matching_Index_L=[]
    for i in range(0,len(RA_L)):
        RA=RA_L[i]
        Dec=Dec_L[i]
        for j in range(0,len(RA_Test_L)):
            RA_Test=RA_Test_L[j]
            Dec_Test=Dec_Test_L[j]

            RA_Diff=np.abs(RA-RA_Test)
            if(RA_Diff>Tolerance):
                continue
            Dec_Diff=np.abs(Dec-Dec_Test)
            if(Dec_Diff>Tolerance):
                continue

            """
            if(Haversine_Distance(RA,RA_Test,Dec,Dec_Test)>Tolerance):
                continue
            """
            #Matching_Index_L.append([i,j])
            ##if((RA_Diff<Tolerance) and (Dec_Diff<Tolerance)):
            #print("Diffs: ", str(RA_Diff)+","+str(Dec_Diff))
            Cur_Index_L=[i,j]
            #if((Cur_Index_L not in Matching_Index_L) and (Cur_Index_L[:-1] not in Matching_Index_L)):
            #if(Cur_Index_L not in Matching_Index_L):
            Matching_Index_L.append([i,j])
    #return Matching_Index_L
    k=0
    for Matching_Index in Matching_Index_L:
        Row_Index=Matching_Index[1]
        #df.iloc[[4]]
        Cur_Row=Data.iloc[[Row_Index]]
        #print("Cur_Row: ", Cur_Row)
        if(k<1):
            Match_Data=Cur_Row
        else:
            Match_Data=pd.concat([Match_Data,Cur_Row])
        k=k+1
    return Match_Data

def Thermal_SNR_Calc(Data, SN_Fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/Thermal_SNs_V2_Modified.csv",Tolerance=0.0005):
    #Data=pd.read_csv(Standard_File_Fpath)
    SN_Data=pd.read_csv(SN_Fpath)
    SN_Data=SN_Data[SN_Data["Color_Color_Classification"]=="Thermal_SNR"]
    #XRB_Data=Thermal_SN_Data[Thermal_SN_Data["Color_Color_Classification"]=="XRB"]
    #Lum_A=np.vectorize(Luminosity_Calc)(Flux_A,Dist_A)
    SN_Data["RA"]=np.vectorize(HMS_Str_to_Decimal_Deg_Convert)(SN_Data["RA_HMS"])
    SN_Data["Dec"]=np.vectorize(DMS_Str_to_Decimal_Deg_Convert)(SN_Data["Dec_DMS"])
    RA_A=SN_Data["RA"]
    RA_L=list(RA_A)
    Dec_A=SN_Data["Dec"]
    Dec_L=list(Dec_A)
    RA_Test_A=Data["RA"]
    RA_Test_L=list(RA_Test_A)
    Dec_Test_A=Data["Dec"]
    Dec_Test_L=list(Dec_Test_A)
    Matching_Index_L=[]
    for i in range(0,len(RA_L)):
        RA=RA_L[i]
        Dec=Dec_L[i]
        for j in range(0,len(RA_Test_L)):
            RA_Test=RA_Test_L[j]
            Dec_Test=Dec_Test_L[j]

            RA_Diff=np.abs(RA-RA_Test)
            if(RA_Diff>Tolerance):
                continue
            Dec_Diff=np.abs(Dec-Dec_Test)
            if(Dec_Diff>Tolerance):
                continue
            """
            if(Haversine_Distance(RA,RA_Test,Dec,Dec_Test)>Tolerance):
                continue
            """
            #Matching_Index_L.append([i,j])
            ##if((RA_Diff<Tolerance) and (Dec_Diff<Tolerance)):
            #print("Diffs: ", str(RA_Diff)+","+str(Dec_Diff))
            Cur_Index_L=[i,j]
            #if((Cur_Index_L not in Matching_Index_L) and (Cur_Index_L[:-1] not in Matching_Index_L)):
            #if(Cur_Index_L not in Matching_Index_L):
            Matching_Index_L.append([i,j])
    #return Matching_Index_L
    k=0
    for Matching_Index in Matching_Index_L:
        Row_Index=Matching_Index[1]
        #df.iloc[[4]]
        Cur_Row=Data.iloc[[Row_Index]]
        #print("Cur_Row: ", Cur_Row)
        if(k<1):
            Match_Data=Cur_Row
        else:
            Match_Data=pd.concat([Match_Data,Cur_Row])
        k=k+1
    return Match_Data

def XRB_Calc(Data, SN_Fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/Thermal_SNs_V2_Modified.csv",Tolerance=0.0005):
    #Data=pd.read_csv(Standard_File_Fpath)
    SN_Data=pd.read_csv(SN_Fpath)
    SN_Data=SN_Data[SN_Data["Color_Color_Classification"]=="XRB"]
    #Lum_A=np.vectorize(Luminosity_Calc)(Flux_A,Dist_A)
    SN_Data["RA"]=np.vectorize(HMS_Str_to_Decimal_Deg_Convert)(SN_Data["RA_HMS"])
    SN_Data["Dec"]=np.vectorize(DMS_Str_to_Decimal_Deg_Convert)(SN_Data["Dec_DMS"])
    RA_A=SN_Data["RA"]
    RA_L=list(RA_A)
    Dec_A=SN_Data["Dec"]
    Dec_L=list(Dec_A)
    RA_Test_A=Data["RA"]
    RA_Test_L=list(RA_Test_A)
    Dec_Test_A=Data["Dec"]
    Dec_Test_L=list(Dec_Test_A)
    Matching_Index_L=[]
    for i in range(0,len(RA_L)):
        RA=RA_L[i]
        Dec=Dec_L[i]
        for j in range(0,len(RA_Test_L)):
            RA_Test=RA_Test_L[j]
            Dec_Test=Dec_Test_L[j]

            RA_Diff=np.abs(RA-RA_Test)
            if(RA_Diff>Tolerance):
                continue
            Dec_Diff=np.abs(Dec-Dec_Test)
            if(Dec_Diff>Tolerance):
                continue
            """
            if(Haversine_Distance(RA,RA_Test,Dec,Dec_Test)>Tolerance):
                continue
            """
            #Matching_Index_L.append([i,j])
            ##if((RA_Diff<Tolerance) and (Dec_Diff<Tolerance)):
            #print("Diffs: ", str(RA_Diff)+","+str(Dec_Diff))
            Cur_Index_L=[i,j]
            #if((Cur_Index_L not in Matching_Index_L) and (Cur_Index_L[:-1] not in Matching_Index_L)):
            #if(Cur_Index_L not in Matching_Index_L):
            Matching_Index_L.append([i,j])
    #return Matching_Index_L
    k=0
    for Matching_Index in Matching_Index_L:
        Row_Index=Matching_Index[1]
        #df.iloc[[4]]
        Cur_Row=Data.iloc[[Row_Index]]
        #print("Cur_Row: ", Cur_Row)
        if(k<1):
            Match_Data=Cur_Row
        else:
            Match_Data=pd.concat([Match_Data,Cur_Row])
        k=k+1
    return Match_Data

def Flux_Plotting(Standard_File_Fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/Source_Flux_All_Modified_6.csv"):
    Data=pd.read_csv(Standard_File_Fpath)
    ##Data=Data[Data["NET_COUNTS_0.3-8.0"]> 25.0]
    Data=Data[Data["Source_Detection_Probability"]> 0.90]
    ##Data=Data[(Data["Soft_Beta_Color"]<-0.25) & (Data["Soft_Beta_Color"]>-0.90)]
    Data_Outside_D25=Data[Data["Outside_D25_Bool"]]
    Data_Inside_D25=Data[Data["Outside_D25_Bool"]==False]
    Data_Outside_Elliptical_D25=Data[Data["Outside_Elliptical_D25_Bool"]]
    Data_Inside_Elliptical_D25=Data[Data["Outside_Elliptical_D25_Bool"]==False]
    Data_Count_Cut=Data[Data["NET_COUNTS_0.3-8.0"]> 25.0]
    #Data=Data[Data["NET_COUNTS_0.3-8.0"]> 25.0]
    Data_Near_Chip_Edge=Data[Data["NEAR_CHIP_EDGE"]]
    Data_Away_Chip_Edge=Data[Data["NEAR_CHIP_EDGE"]==False]
    Data_Spiral_Projected=Data[(Data["Galaxy_Morph_Simple"]=="S") & (Data["Circular_D25_Bool"]==False)]
    #Data_Spiral_Projected=Data[(Data["Galaxy_Morph_Simple"]=="S") & (Data["Circular_D25_Bool"]==False) & ((Data["D25_Min"]/Data["D25_Maj"])<0.5)]
    #Data_Spiral_Projected=Data[(Data["Galaxy_Morph_Simple"]=="S") & (Data["Circular_D25_Bool"]==False) & ((Data["D25_Min"]/Data["D25_Maj"])<0.2)]
    Data_Spiral_Projected_Disk=Data_Spiral_Projected[Data_Spiral_Projected["Outside_Elliptical_D25_Bool"]==False]
    Data_Spiral_Projected_Bulge=Data_Spiral_Projected[(Data_Spiral_Projected["Outside_Elliptical_D25_Bool"]==True) & (Data_Spiral_Projected["Outside_D25_Bool"]==False)]
    print("Data: ", Data)
    ObsID_A=Data["ObsID"]
    ObsID_L_Unique=list(set(list(ObsID_A)))
    ObsID_L_Unique.sort()
    print("ObsID_L_Unique: ", ObsID_L_Unique)
    print("len(ObsID_L_Unique: ", len(ObsID_L_Unique))
    Count_Rate=Data["NET_RATE_0.3-7.5"]
    Backround_Rate=Data["BG_RATE_0.3-7.5"]
    Offaxis_Angle=Data["Offaxis_Angle"]
    Phi=Data["PHI"]
    Psi=Data["Psi"]
    Phi_Rad=Phi*(np.pi/180.0)
    Roll_Angle_A=Data["Roll_Angle"]
    #Source_Roll_A=Phi+Roll_Angle_A
    #Source_Roll_Rad_A=Source_Roll_A*(np.pi/180.0)
    Offaxis_Aera=Data["Offaxis_Angle_Annulus_Area"]
    #Gname_A=Data["Gname_Modifed"] #Note: There is a typo in this key
    #Gname_Modified
    Gname_A=Data["Gname_Modified"]
    Galaxy_Morph_A=Data["Galaxy_Morph"]
    Data["Galaxy_Morph_Simple"]=np.vectorize(Morph_Check)(Galaxy_Morph_A)
    Data_Spiral=Data[Data["Galaxy_Morph_Simple"]=="S"]
    Data_Elliptical=Data[Data["Galaxy_Morph_Simple"]=="E"]
    Data_Irregular=Data[Data["Galaxy_Morph_Simple"]=="I"]
    Area_A=Data["AREA"]
    Gname_L=list(Gname_A)
    Gname_L_Unique =[]
    #'''
    #All
    Soft_Counts=Data["NET_COUNTS_0.3-1.0"]
    Medium_Counts=Data["NET_COUNTS_1.0-2.1"]
    Hard_Counts=Data["NET_COUNTS_2.1-7.5"]
    HC_Ratio=(Hard_Counts-Medium_Counts)/((Hard_Counts+Medium_Counts))
    SC_Ratio=(Medium_Counts-Soft_Counts)/((Medium_Counts+Soft_Counts))
    #Outside D25
    Soft_Counts_Outside_D25=Data_Outside_D25["NET_COUNTS_0.3-1.0"]
    Medium_Counts_Outside_D25=Data_Outside_D25["NET_COUNTS_1.0-2.1"]
    Hard_Counts_Outside_D25=Data_Outside_D25["NET_COUNTS_2.1-7.5"]
    HC_Ratio_Outside_D25=(Hard_Counts_Outside_D25-Medium_Counts_Outside_D25)/((Hard_Counts_Outside_D25+Medium_Counts_Outside_D25))
    SC_Ratio_Outside_D25=(Medium_Counts_Outside_D25-Soft_Counts_Outside_D25)/((Medium_Counts_Outside_D25+Soft_Counts_Outside_D25))
    #Inside D25
    Soft_Counts_Inside_D25=Data_Inside_D25["NET_COUNTS_0.3-1.0"]
    Medium_Counts_Inside_D25=Data_Inside_D25["NET_COUNTS_1.0-2.1"]
    Hard_Counts_Inside_D25=Data_Inside_D25["NET_COUNTS_2.1-7.5"]
    HC_Ratio_Inside_D25=(Hard_Counts_Inside_D25-Medium_Counts_Inside_D25)/((Hard_Counts_Inside_D25+Medium_Counts_Inside_D25))
    SC_Ratio_Inside_D25=(Medium_Counts_Inside_D25-Soft_Counts_Inside_D25)/((Medium_Counts_Inside_D25+Soft_Counts_Inside_D25))
    #Outside Elliptical_D25
    Soft_Counts_Outside_Elliptical_D25=Data_Outside_Elliptical_D25["NET_COUNTS_0.3-1.0"]
    Medium_Counts_Outside_Elliptical_D25=Data_Outside_Elliptical_D25["NET_COUNTS_1.0-2.1"]
    Hard_Counts_Outside_Elliptical_D25=Data_Outside_Elliptical_D25["NET_COUNTS_2.1-7.5"]
    HC_Ratio_Outside_Elliptical_D25=(Hard_Counts_Outside_Elliptical_D25-Medium_Counts_Outside_Elliptical_D25)/((Hard_Counts_Outside_Elliptical_D25+Medium_Counts_Outside_Elliptical_D25))
    SC_Ratio_Outside_Elliptical_D25=(Medium_Counts_Outside_Elliptical_D25-Soft_Counts_Outside_Elliptical_D25)/((Medium_Counts_Outside_Elliptical_D25+Soft_Counts_Outside_Elliptical_D25))
    #Inside D25
    Soft_Counts_Inside_Elliptical_D25=Data_Inside_Elliptical_D25["NET_COUNTS_0.3-1.0"]
    Medium_Counts_Inside_Elliptical_D25=Data_Inside_Elliptical_D25["NET_COUNTS_1.0-2.1"]
    Hard_Counts_Inside_Elliptical_D25=Data_Inside_Elliptical_D25["NET_COUNTS_2.1-7.5"]
    HC_Ratio_Inside_Elliptical_D25=(Hard_Counts_Inside_Elliptical_D25-Medium_Counts_Inside_Elliptical_D25)/((Hard_Counts_Inside_Elliptical_D25+Medium_Counts_Inside_Elliptical_D25))
    SC_Ratio_Inside_Elliptical_D25=(Medium_Counts_Inside_Elliptical_D25-Soft_Counts_Inside_Elliptical_D25)/((Medium_Counts_Inside_Elliptical_D25+Soft_Counts_Inside_Elliptical_D25))
    #Spiral
    Soft_Counts_Spiral=Data_Spiral["NET_COUNTS_0.3-1.0"]
    Medium_Counts_Spiral=Data_Spiral["NET_COUNTS_1.0-2.1"]
    Hard_Counts_Spiral=Data_Spiral["NET_COUNTS_2.1-7.5"]
    HC_Ratio_Spiral=(Hard_Counts_Spiral-Medium_Counts_Spiral)/((Hard_Counts_Spiral+Medium_Counts_Spiral))
    SC_Ratio_Spiral=(Medium_Counts_Spiral-Soft_Counts_Spiral)/((Medium_Counts_Spiral+Soft_Counts_Spiral))
    #Elliptical
    Soft_Counts_Elliptical=Data_Elliptical["NET_COUNTS_0.3-1.0"]
    Medium_Counts_Elliptical=Data_Elliptical["NET_COUNTS_1.0-2.1"]
    Hard_Counts_Elliptical=Data_Elliptical["NET_COUNTS_2.1-7.5"]
    HC_Ratio_Elliptical=(Hard_Counts_Elliptical-Medium_Counts_Elliptical)/((Hard_Counts_Elliptical+Medium_Counts_Elliptical))
    SC_Ratio_Elliptical=(Medium_Counts_Elliptical-Soft_Counts_Elliptical)/((Medium_Counts_Elliptical+Soft_Counts_Elliptical))
    #Irregular
    Soft_Counts_Irregular=Data_Irregular["NET_COUNTS_0.3-1.0"]
    Medium_Counts_Irregular=Data_Irregular["NET_COUNTS_1.0-2.1"]
    Hard_Counts_Irregular=Data_Irregular["NET_COUNTS_2.1-7.5"]
    HC_Ratio_Irregular=(Hard_Counts_Irregular-Medium_Counts_Irregular)/((Hard_Counts_Irregular+Medium_Counts_Irregular))
    SC_Ratio_Irregular=(Medium_Counts_Irregular-Soft_Counts_Irregular)/((Medium_Counts_Irregular+Soft_Counts_Irregular))
    """
    Flux Color-Color Plots
    """
    #All
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    HC_Ratio_Flux=(Hard_Flux-Medium_Flux)/((Hard_Flux+Medium_Flux))
    SC_Ratio_Flux=(Medium_Flux-Soft_Flux)/((Medium_Flux+Soft_Flux))
    #Outside D25
    Soft_Flux_Outside_D25=Data_Outside_D25["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_Outside_D25=Data_Outside_D25["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_Outside_D25=Data_Outside_D25["NET_FLUX_APER_2.1-7.5"]
    HC_Ratio_Flux_Outside_D25=(Hard_Flux_Outside_D25-Medium_Flux_Outside_D25)/((Hard_Flux_Outside_D25+Medium_Flux_Outside_D25))
    SC_Ratio_Flux_Outside_D25=(Medium_Flux_Outside_D25-Soft_Flux_Outside_D25)/((Medium_Flux_Outside_D25+Soft_Flux_Outside_D25))
    #Inside D25
    Soft_Flux_Inside_D25=Data_Inside_D25["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_Inside_D25=Data_Inside_D25["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_Inside_D25=Data_Inside_D25["NET_FLUX_APER_2.1-7.5"]
    HC_Ratio_Flux_Inside_D25=(Hard_Flux_Inside_D25-Medium_Flux_Inside_D25)/((Hard_Flux_Inside_D25+Medium_Flux_Inside_D25))
    SC_Ratio_Flux_Inside_D25=(Medium_Flux_Inside_D25-Soft_Flux_Inside_D25)/((Medium_Flux_Inside_D25+Soft_Flux_Inside_D25))
    #Outside Elliptical_D25
    Soft_Flux_Outside_Elliptical_D25=Data_Outside_Elliptical_D25["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_Outside_Elliptical_D25=Data_Outside_Elliptical_D25["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_Outside_Elliptical_D25=Data_Outside_Elliptical_D25["NET_FLUX_APER_2.1-7.5"]
    HC_Ratio_Flux_Outside_Elliptical_D25=(Hard_Flux_Outside_Elliptical_D25-Medium_Flux_Outside_Elliptical_D25)/((Hard_Flux_Outside_Elliptical_D25+Medium_Flux_Outside_Elliptical_D25))
    SC_Ratio_Flux_Outside_Elliptical_D25=(Medium_Flux_Outside_Elliptical_D25-Soft_Flux_Outside_Elliptical_D25)/((Medium_Flux_Outside_Elliptical_D25+Soft_Flux_Outside_Elliptical_D25))
    #Inside D25
    Soft_Flux_Inside_Elliptical_D25=Data_Inside_Elliptical_D25["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_Inside_Elliptical_D25=Data_Inside_Elliptical_D25["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_Inside_Elliptical_D25=Data_Inside_Elliptical_D25["NET_FLUX_APER_2.1-7.5"]
    HC_Ratio_Flux_Inside_Elliptical_D25=(Hard_Flux_Inside_Elliptical_D25-Medium_Flux_Inside_Elliptical_D25)/((Hard_Flux_Inside_Elliptical_D25+Medium_Flux_Inside_Elliptical_D25))
    SC_Ratio_Flux_Inside_Elliptical_D25=(Medium_Flux_Inside_Elliptical_D25-Soft_Flux_Inside_Elliptical_D25)/((Medium_Flux_Inside_Elliptical_D25+Soft_Flux_Inside_Elliptical_D25))
    #Spiral
    Soft_Flux_Spiral=Data_Spiral["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_Spiral=Data_Spiral["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_Spiral=Data_Spiral["NET_FLUX_APER_2.1-7.5"]
    HC_Ratio_Flux_Spiral=(Hard_Flux_Spiral-Medium_Flux_Spiral)/((Hard_Flux_Spiral+Medium_Flux_Spiral))
    SC_Ratio_Flux_Spiral=(Medium_Flux_Spiral-Soft_Flux_Spiral)/((Medium_Flux_Spiral+Soft_Flux_Spiral))
    #Elliptical
    Soft_Flux_Elliptical=Data_Elliptical["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_Elliptical=Data_Elliptical["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_Elliptical=Data_Elliptical["NET_FLUX_APER_2.1-7.5"]
    HC_Ratio_Flux_Elliptical=(Hard_Flux_Elliptical-Medium_Flux_Elliptical)/((Hard_Flux_Elliptical+Medium_Flux_Elliptical))
    SC_Ratio_Flux_Elliptical=(Medium_Flux_Elliptical-Soft_Flux_Elliptical)/((Medium_Flux_Elliptical+Soft_Flux_Elliptical))
    #Irregular
    Soft_Flux_Irregular=Data_Irregular["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_Irregular=Data_Irregular["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_Irregular=Data_Irregular["NET_FLUX_APER_2.1-7.5"]
    HC_Ratio_Flux_Irregular=(Hard_Flux_Irregular-Medium_Flux_Irregular)/((Hard_Flux_Irregular+Medium_Flux_Irregular))
    SC_Ratio_Flux_Irregular=(Medium_Flux_Irregular-Soft_Flux_Irregular)/((Medium_Flux_Irregular+Soft_Flux_Irregular))
    #High Counts
    Soft_Counts_Count_Cut=Data_Count_Cut["NET_COUNTS_0.3-1.0"]
    Medium_Counts_Count_Cut=Data_Count_Cut["NET_COUNTS_1.0-2.1"]
    Hard_Counts_Count_Cut=Data_Count_Cut["NET_COUNTS_2.1-7.5"]
    HC_Ratio_Count_Cut=(Hard_Counts_Count_Cut-Medium_Counts_Count_Cut)/((Hard_Counts_Count_Cut+Medium_Counts_Count_Cut))
    SC_Ratio_Count_Cut=(Medium_Counts_Count_Cut-Soft_Counts_Count_Cut)/((Medium_Counts_Count_Cut+Soft_Counts_Count_Cut))
    d = {'HC_Ratio_Count_Cut': HC_Ratio_Count_Cut, 'SC_Ratio_Count_Cut': SC_Ratio_Count_Cut}
    Data_Count_Cut = pd.DataFrame(data=d)
    Data_Count_Cut.to_csv("Count_Cut_Colors.csv")
    for Gname in Gname_L:
        if Gname not in Gname_L_Unique:
            Gname_L_Unique.append(Gname)
    print("Gname_L_Unique: ", Gname_L_Unique)
    print("len(Gname_L_Unique): ", len(Gname_L_Unique))
    #"""
    plt.plot(Backround_Rate, Count_Rate, ".")
    plt.ylim(-1, 1)
    plt.xlim(0, 0.2)
    plt.savefig("Count_Rate_VS_Backround_Rate.pdf")
    plt.cla()
    plt.clf()
    plt.plot(Offaxis_Angle,Backround_Rate, ".", alpha=0.1)
    plt.ylim(0, 0.2)
    plt.savefig("Backround_Rate_VS_Offaxis_Angle.pdf")
    plt.cla()
    plt.clf()
    plt.plot(Offaxis_Angle,Count_Rate, ".", alpha=0.1)
    plt.ylim(-0.1, 0.3)
    plt.savefig("Count_Rate_VS_Offaxis_Angle.pdf")
    plt.cla()
    plt.clf()
    ##X_A=np.linspace(0,15,100)
    #Y_A=Exp(X_A,53.33,0)
    #Y_A=Exp(X_A,0.23,0,4)
    #Y_A=Exp(X_A,0.23,100,4)
    #Y_A=Exp(X_A,0.23,-1,100,4)
    #Y_A=Exp(X_A,0.235,-1,100,4)
    #Y_A=Exp(X_A,0.235,-1.6,100,4)
    #Y_A=Exp(X_A,0.23,-1.6,100,4)
    ##Y_A=Exp(X_A,0.23,-1.6,45,4)
    #Y_A=Exp(X_A,0.225,-1.6,45,4)
    #Y_A=Exp(X_A,0.225,-1.8,45,4)
    ##Y_A=Exp(X_A,0.23,-1.6,44,4) #This is a good fit!
    #plt.plot(X_A,Y_A)
    plt.plot(Offaxis_Angle, Area_A, ".")
    ##plt.plot(X_A,Y_A)
    plt.savefig("Source_Area_VS_Offaxis_Angle.pdf")
    #plt.show()
    #return
    plt.cla()
    plt.clf()
    #Data_Near_Chip_Edge
    #plt.plot(Data_Near_Chip_Edge["Offaxis_Angle"], Data_Near_Chip_Edge["AREA"], ".")
    plt.plot(Data_Away_Chip_Edge["Offaxis_Angle"], Data_Away_Chip_Edge["AREA"], ".", label='Away Chip Edge')
    plt.plot(Data_Near_Chip_Edge["Offaxis_Angle"], Data_Near_Chip_Edge["AREA"], ".", label='Near Chip Edge')
    plt.legend(loc="upper right")
    plt.savefig("Source_Area_VS_Offaxis_Angle_Chip_Edge_Info.pdf")
    #plt.show()
    #return
    plt.cla()
    plt.clf()
    plt.hist(Offaxis_Angle,bins=20,range=(0,10))
    plt.savefig("Offaxis_Angle_Hist.pdf")
    plt.cla()
    plt.clf()
    #plt.hist(Offaxis_Aera)
    plt.polar(Phi_Rad,Offaxis_Angle, ".")
    plt.savefig("Source_Polar.pdf")
    plt.cla()
    plt.clf()
    #"""
    #plt.polar(Source_Roll_Rad_A,Offaxis_Angle, ".")
    #plt.polar(Source_Roll_Rad_A,Offaxis_Angle, ".", alpha=0.3)
    plt.polar(Psi,Offaxis_Angle, ".", alpha=0.3)
    #plt.savefig("Source_Roll_Polar.pdf")
    #matplotlib.projections.polar.PolarAxes.set_theta_zero_location("N")
    plt.savefig("Source_Psi_Polar_Alpha.pdf")
    #plt.show()
    plt.cla()
    plt.clf()
    #"""

    #"""
    plt.plot(HC_Ratio,SC_Ratio,".", alpha=0.02) #Note: This plot has some serious artifacts in it
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Weird_Artifacts.pdf")
    plt.cla()
    plt.clf()
    plt.plot(HC_Ratio,SC_Ratio,".", alpha=0.5)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color.pdf")
    plt.cla()
    plt.clf()
    plt.plot(HC_Ratio_Inside_D25,SC_Ratio_Inside_D25,".", alpha=0.5)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Inside_D25.pdf")
    plt.cla()
    plt.clf()
    plt.plot(HC_Ratio_Outside_D25,SC_Ratio_Outside_D25,".", alpha=0.5)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Outside_D25.pdf")
    plt.cla()
    plt.clf()
    plt.plot(HC_Ratio_Inside_D25,SC_Ratio_Inside_D25,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.plot(HC_Ratio_Outside_D25,SC_Ratio_Outside_D25,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Combined_D25.pdf")
    plt.cla()
    plt.clf()

    plt.plot(HC_Ratio_Inside_Elliptical_D25,SC_Ratio_Inside_Elliptical_D25,".", alpha=0.5)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Inside_Elliptical_D25.pdf")
    plt.cla()
    plt.clf()
    plt.plot(HC_Ratio_Outside_Elliptical_D25,SC_Ratio_Outside_Elliptical_D25,".", alpha=0.5)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Outside_Elliptical_D25.pdf")
    plt.cla()
    plt.clf()
    plt.plot(HC_Ratio_Inside_Elliptical_D25,SC_Ratio_Inside_Elliptical_D25,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.plot(HC_Ratio_Outside_Elliptical_D25,SC_Ratio_Outside_Elliptical_D25,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Combined_Elliptical_D25.pdf")
    plt.cla()
    plt.clf()

    plt.plot(HC_Ratio_Spiral,SC_Ratio_Spiral,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.plot(HC_Ratio_Elliptical,SC_Ratio_Elliptical,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.plot(HC_Ratio_Irregular,SC_Ratio_Irregular,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Combined_Morph.pdf")
    plt.cla()
    plt.clf()
    #"""
    """
    Flux Color-Color Plots
    """
    plt.plot(HC_Ratio_Flux,SC_Ratio_Flux,".", alpha=0.02) #Note: This plot has some serious artifacts in it
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Flux_Weird_Artifacts.pdf")
    plt.cla()
    plt.clf()
    plt.plot(HC_Ratio_Flux,SC_Ratio_Flux,".", alpha=0.5)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Flux.pdf")
    plt.cla()
    plt.clf()
    plt.plot(HC_Ratio_Flux_Inside_D25,SC_Ratio_Flux_Inside_D25,".", alpha=0.5)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Flux_Inside_D25.pdf")
    plt.cla()
    plt.clf()
    plt.plot(HC_Ratio_Flux_Outside_D25,SC_Ratio_Flux_Outside_D25,".", alpha=0.5)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Flux_Outside_D25.pdf")
    plt.cla()
    plt.clf()
    plt.plot(HC_Ratio_Flux_Inside_D25,SC_Ratio_Flux_Inside_D25,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.plot(HC_Ratio_Flux_Outside_D25,SC_Ratio_Flux_Outside_D25,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Flux_Combined_D25.pdf")
    plt.cla()
    plt.clf()

    plt.plot(HC_Ratio_Flux_Inside_Elliptical_D25,SC_Ratio_Flux_Inside_Elliptical_D25,".", alpha=0.5)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Flux_Inside_Elliptical_D25.pdf")
    plt.cla()
    plt.clf()
    plt.plot(HC_Ratio_Flux_Outside_Elliptical_D25,SC_Ratio_Flux_Outside_Elliptical_D25,".", alpha=0.5)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Flux_Outside_Elliptical_D25.pdf")
    plt.cla()
    plt.clf()
    plt.plot(HC_Ratio_Flux_Inside_Elliptical_D25,SC_Ratio_Flux_Inside_Elliptical_D25,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.plot(HC_Ratio_Flux_Outside_Elliptical_D25,SC_Ratio_Flux_Outside_Elliptical_D25,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Flux_Combined_Elliptical_D25.pdf")
    plt.cla()
    plt.clf()

    plt.plot(HC_Ratio_Flux_Spiral,SC_Ratio_Flux_Spiral,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.plot(HC_Ratio_Flux_Elliptical,SC_Ratio_Flux_Elliptical,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.plot(HC_Ratio_Flux_Irregular,SC_Ratio_Flux_Irregular,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Flux_Combined_Morph.pdf")
    plt.cla()
    plt.clf()
    #plt.show()
    #Hist=plt.hist(Data["NET_LUM_APER_0.3-7.5"],  bins=100, range=(10E42,10E44), cumulative=-1)
    #Hist=plt.hist(Data["NET_LUM_APER_0.3-7.5"],  bins=100, range=(10E37,10E38), cumulative=-1)
    Hist=plt.hist(Data["NET_LUM_APER_0.3-7.5"],  bins=100, range=(10E37,10E44), cumulative=-1)
    #plt.savefig("XLF.pdf")
    #plt.show()
    plt.cla()
    plt.clf()
    HC_Ratio_Flux_Spiral_Projected_Disk=Data_Spiral_Projected_Disk["Hard_Flux_Color"]
    SC_Ratio_Flux_Spiral_Projected_Disk=Data_Spiral_Projected_Disk["Soft_Flux_Color"]
    HC_Ratio_Flux_Spiral_Projected_Bulge=Data_Spiral_Projected_Bulge["Hard_Flux_Color"]
    SC_Ratio_Flux_Spiral_Projected_Bulge=Data_Spiral_Projected_Bulge["Soft_Flux_Color"]
    plt.plot(HC_Ratio_Flux_Spiral_Projected_Disk,SC_Ratio_Flux_Spiral_Projected_Disk,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.plot(HC_Ratio_Flux_Spiral_Projected_Bulge,SC_Ratio_Flux_Spiral_Projected_Bulge,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Flux_Spiral_Projected.pdf")
    plt.cla()
    plt.clf()
    HC_Ratio_Counts_Spiral_Projected_Disk=Data_Spiral_Projected_Disk["Hard_Counts_Color"]
    SC_Ratio_Counts_Spiral_Projected_Disk=Data_Spiral_Projected_Disk["Soft_Counts_Color"]
    HC_Ratio_Counts_Spiral_Projected_Bulge=Data_Spiral_Projected_Bulge["Hard_Counts_Color"]
    SC_Ratio_Counts_Spiral_Projected_Bulge=Data_Spiral_Projected_Bulge["Soft_Counts_Color"]
    plt.plot(HC_Ratio_Counts_Spiral_Projected_Disk,SC_Ratio_Counts_Spiral_Projected_Disk,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.plot(HC_Ratio_Counts_Spiral_Projected_Bulge,SC_Ratio_Counts_Spiral_Projected_Bulge,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Counts_Spiral_Projected.pdf")
    plt.cla()
    plt.clf()
    HC_Ratio_Flux=Data["Hard_Flux_Color"]
    SC_Ratio_Flux=Data["Soft_Flux_Color"]
    Source_Distance_From_GC_Elliptical_D25=Data["Source_Distance_From_GC_Elliptical_D25"]
    #plt.plot(HC_Ratio_Flux,SC_Ratio_Flux,".", alpha=0.2)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    #ax.scatter3D(HC_Ratio_Flux, SC_Ratio_Flux, Source_Distance_From_GC_Elliptical_D25, c=Source_Distance_From_GC_Elliptical_D25)
    #marker=".", alpha=0.2, vmax=10.0
    ax.scatter3D(HC_Ratio_Flux, SC_Ratio_Flux, Source_Distance_From_GC_Elliptical_D25, c=Source_Distance_From_GC_Elliptical_D25, marker=".", alpha=0.2, vmax=10.0)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    #plt.zlim(1.0, 10)
    ax.axes.set_zlim3d(bottom=0, top=10)
    plt.savefig("Color_Color_Flux_Distance_3D.pdf")
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    HC_Ratio_Counts_Spiral_Projected_Disk=Data_Spiral_Projected_Disk["Hard_Counts_Color"]
    SC_Ratio_Counts_Spiral_Projected_Disk=Data_Spiral_Projected_Disk["Soft_Counts_Color"]
    HC_Ratio_Counts_Spiral_Projected_Bulge=Data_Spiral_Projected_Bulge["Hard_Counts_Color"]
    SC_Ratio_Counts_Spiral_Projected_Bulge=Data_Spiral_Projected_Bulge["Soft_Counts_Color"]
    plt.plot(HC_Ratio_Counts_Spiral_Projected_Disk,SC_Ratio_Counts_Spiral_Projected_Disk,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.plot(HC_Ratio_Counts_Spiral_Projected_Bulge,SC_Ratio_Counts_Spiral_Projected_Bulge,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Counts_Spiral_Projected.pdf")
    plt.cla()
    plt.clf()
    HC_Ratio_Flux=Data["Hard_Flux_Color"]
    SC_Ratio_Flux=Data["Soft_Flux_Color"]
    Source_Distance_From_GC_Elliptical_D25=Data["Source_Distance_From_GC_Elliptical_D25"]
    #plt.plot(HC_Ratio_Flux,SC_Ratio_Flux,".", alpha=0.2)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    #ax.scatter3D(HC_Ratio_Flux, SC_Ratio_Flux, Source_Distance_From_GC_Elliptical_D25, c=Source_Distance_From_GC_Elliptical_D25)
    #marker=".", alpha=0.2, vmax=10.0
    ax.scatter3D(HC_Ratio_Flux, SC_Ratio_Flux, Source_Distance_From_GC_Elliptical_D25, c=Source_Distance_From_GC_Elliptical_D25, marker=".", alpha=0.2, vmax=10.0)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    #plt.zlim(1.0, 10)
    ax.axes.set_zlim3d(bottom=0, top=10)
    #ax.view_init(30, 90)
    ax.view_init(30, 75)
    plt.savefig("Color_Color_Flux_Distance_3D_Side.pdf")
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    HC_Ratio_Counts_Spiral_Projected_Disk=Data_Spiral_Projected_Disk["Hard_Counts_Color"]
    SC_Ratio_Counts_Spiral_Projected_Disk=Data_Spiral_Projected_Disk["Soft_Counts_Color"]
    HC_Ratio_Counts_Spiral_Projected_Bulge=Data_Spiral_Projected_Bulge["Hard_Counts_Color"]
    SC_Ratio_Counts_Spiral_Projected_Bulge=Data_Spiral_Projected_Bulge["Soft_Counts_Color"]
    plt.plot(HC_Ratio_Counts_Spiral_Projected_Disk,SC_Ratio_Counts_Spiral_Projected_Disk,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.plot(HC_Ratio_Counts_Spiral_Projected_Bulge,SC_Ratio_Counts_Spiral_Projected_Bulge,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Counts_Spiral_Projected.pdf")
    plt.cla()
    plt.clf()
    HC_Ratio_Flux=Data["Hard_Flux_Color"]
    SC_Ratio_Flux=Data["Soft_Flux_Color"]
    Source_Distance_From_GC_Elliptical_D25=Data["Source_Distance_From_GC_Elliptical_D25"]
    #plt.plot(HC_Ratio_Flux,SC_Ratio_Flux,".", alpha=0.2)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    #ax.scatter3D(HC_Ratio_Flux, SC_Ratio_Flux, Source_Distance_From_GC_Elliptical_D25, c=Source_Distance_From_GC_Elliptical_D25)
    #marker=".", alpha=0.2, vmax=10.0
    ax.scatter3D(HC_Ratio_Flux, SC_Ratio_Flux, Source_Distance_From_GC_Elliptical_D25, c=Source_Distance_From_GC_Elliptical_D25, marker=".", alpha=0.2, vmax=10.0)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    #plt.zlim(1.0, 10)
    ax.axes.set_zlim3d(bottom=0, top=10)
    ax.view_init(30, 0)
    plt.savefig("Color_Color_Flux_Distance_3D_Front.pdf")
    plt.cla()
    plt.clf()

    HC_Ratio_Flux=Data["Hard_Flux_Color"]
    SC_Ratio_Flux=Data["Soft_Flux_Color"]
    Source_Distance_From_GC_Elliptical_D25=Data["Source_Distance_From_GC_Elliptical_D25"]
    #plt.plot(Source_Distance_From_GC_Elliptical_D25, HC_Ratio_Flux,".", alpha=0.2)
    plt.plot(HC_Ratio_Flux,Source_Distance_From_GC_Elliptical_D25,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(0, 10)
    plt.savefig("HC_vs_Distance.pdf")
    plt.cla()
    plt.clf()
    HC_Ratio_Flux=Data["Hard_Flux_Color"]
    SC_Ratio_Flux=Data["Soft_Flux_Color"]
    Source_Distance_From_GC_Elliptical_D25=Data["Source_Distance_From_GC_Elliptical_D25"]
    #plt.plot(Source_Distance_From_GC_Elliptical_D25, HC_Ratio_Flux,".", alpha=0.2)
    plt.plot(SC_Ratio_Flux,Source_Distance_From_GC_Elliptical_D25,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(0, 10)
    plt.savefig("SC_vs_Distance.pdf")
    plt.cla()
    plt.clf()
    HC_Ratio_Flux=Data["Hard_Flux_Color"]
    SC_Ratio_Flux=Data["Soft_Flux_Color"]
    Source_Distance_From_GC_Elliptical_D25=Data["Source_Distance_From_GC_Elliptical_D25"]
    #plt.plot(HC_Ratio_Flux,SC_Ratio_Flux,".", alpha=0.2)
    fig = plt.figure()
    ax = plt.axes()
    ax.scatter(HC_Ratio_Flux, SC_Ratio_Flux, c=Source_Distance_From_GC_Elliptical_D25, marker=".", alpha=0.2, vmax=10.0)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Flux_Distance.pdf")
    plt.cla()
    plt.clf()


    HC_Ratio_Counts=Data["Hard_Counts_Color"]
    SC_Ratio_Counts=Data["Soft_Counts_Color"]
    Source_Distance_From_GC_Elliptical_D25=Data["Source_Distance_From_GC_Elliptical_D25"]
    #plt.plot(Source_Distance_From_GC_Elliptical_D25, HC_Ratio_Counts,".", alpha=0.2)
    plt.plot(HC_Ratio_Counts,Source_Distance_From_GC_Elliptical_D25,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(0, 10)
    plt.savefig("HC_Counts_vs_Distance.pdf")
    plt.cla()
    plt.clf()
    HC_Ratio_Counts=Data["Hard_Counts_Color"]
    SC_Ratio_Counts=Data["Soft_Counts_Color"]
    Source_Distance_From_GC_Elliptical_D25=Data["Source_Distance_From_GC_Elliptical_D25"]
    #plt.plot(Source_Distance_From_GC_Elliptical_D25, HC_Ratio_Counts,".", alpha=0.2)
    plt.plot(SC_Ratio_Counts,Source_Distance_From_GC_Elliptical_D25,".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(0, 10)
    plt.savefig("SC_Counts_vs_Distance.pdf")
    plt.cla()
    plt.clf()
    HC_Ratio_Counts=Data["Hard_Counts_Color"]
    SC_Ratio_Counts=Data["Soft_Counts_Color"]
    Source_Distance_From_GC_Elliptical_D25=Data["Source_Distance_From_GC_Elliptical_D25"]
    #plt.plot(HC_Ratio_Counts,SC_Ratio_Counts,".", alpha=0.2)
    fig = plt.figure()
    ax = plt.axes()
    ax.scatter(HC_Ratio_Counts, SC_Ratio_Counts, c=Source_Distance_From_GC_Elliptical_D25, marker=".", alpha=0.2, vmax=10.0)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Counts_Distance.pdf")
    plt.cla()
    plt.clf()

    Thermal_SN_Data=Thermal_SN_Calc(Data)
    #Thermal_SNR_Data=Thermal_SN_Data[Thermal_SN_Data["Color_Color_Classification"]=="Thermal_SNR"]
    Thermal_SNR_Data=Thermal_SNR_Calc(Data)
    #XRB_Data=Thermal_SN_Data[Thermal_SN_Data["Color_Color_Classification"]=="XRB"]
    XRB_Data=XRB_Calc(Data)
    HC_Ratio_Flux_SN=Thermal_SN_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_SN=Thermal_SN_Data["Soft_Flux_Color"]
    HC_Ratio_Flux_SNR=Thermal_SNR_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_SNR=Thermal_SNR_Data["Soft_Flux_Color"]
    HC_Ratio_Flux_XRB=XRB_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_XRB=XRB_Data["Soft_Flux_Color"]

    fig = plt.figure()
    ax = plt.axes()
    ax.scatter(HC_Ratio_Flux, SC_Ratio_Flux, c=Source_Distance_From_GC_Elliptical_D25, marker=".", alpha=0.2, vmax=10.0)
    #ax.scatter(HC_Ratio_Flux_SN, SC_Ratio_Flux_SN, c="red", marker="o")
    ax.scatter(HC_Ratio_Flux_SNR, SC_Ratio_Flux_SNR, c="red", marker="o")
    ax.scatter(HC_Ratio_Flux_XRB, SC_Ratio_Flux_XRB, c="blue", marker="o")
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Flux_Distance_with_SN.pdf")
    plt.cla()
    plt.clf()

    #Thermal_SN_Data=Thermal_SN_Calc()
    HC_Ratio_Counts_SN=Thermal_SN_Data["Hard_Counts_Color"]
    SC_Ratio_Counts_SN=Thermal_SN_Data["Soft_Counts_Color"]

    HC_Ratio_Counts_SNR=Thermal_SNR_Data["Hard_Counts_Color"]
    print("HC_Ratio_Counts_SNR:\n", HC_Ratio_Counts_SNR)
    SC_Ratio_Counts_SNR=Thermal_SNR_Data["Soft_Counts_Color"]
    print("SC_Ratio_Counts_SNR:\n", SC_Ratio_Counts_SNR)
    HC_Ratio_Counts_XRB=XRB_Data["Hard_Counts_Color"]
    print("HC_Ratio_Counts_XRB:\n", HC_Ratio_Counts_XRB)
    SC_Ratio_Counts_XRB=XRB_Data["Soft_Counts_Color"]
    print("SC_Ratio_Counts_XRB:\n", SC_Ratio_Counts_XRB)
    #Soft_Counts_Color_Error

    print("Thermal_SNR_Data:\n", Thermal_SNR_Data)
    print("XRB_Data:\n", XRB_Data)

    print('Thermal_SNR_Data["ObsID"]:\n ', Thermal_SNR_Data["ObsID"])
    print('XRB_Data_Data["ObsID"]:\n ', XRB_Data["ObsID"])

    fig = plt.figure()
    ax = plt.axes()
    ax.scatter(HC_Ratio_Counts, SC_Ratio_Counts, c=Source_Distance_From_GC_Elliptical_D25, marker=".", alpha=0.2, vmax=10.0)
    #ax.scatter(HC_Ratio_Counts_SN, SC_Ratio_Counts_SN, c="red", marker="o")
    ax.scatter(HC_Ratio_Counts_SNR, SC_Ratio_Counts_SNR, c="red", marker="o")
    ax.scatter(HC_Ratio_Counts_XRB, SC_Ratio_Counts_XRB, c="blue", marker="o")
    plt.errorbar(HC_Ratio_Counts_SNR, SC_Ratio_Counts_SNR, xerr=Thermal_SNR_Data["Hard_Counts_Color_Error"], yerr=Thermal_SNR_Data["Soft_Counts_Color_Error"], ls='none', c="red")
    plt.errorbar(HC_Ratio_Counts_XRB, SC_Ratio_Counts_XRB, xerr=XRB_Data["Hard_Counts_Color_Error"], yerr=XRB_Data["Soft_Counts_Color_Error"], ls='none', c="blue")
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Counts_Distance_with_SN.pdf")
    plt.cla()
    plt.clf()
    """
    Soft_Counts=Data["NET_COUNTS_0.3-1.0"]
    Medium_Counts=Data["NET_COUNTS_1.0-2.1"]
    Hard_Counts=Data["NET_COUNTS_2.1-7.5"]
    HC_Ratio=(Hard_Counts-Medium_Counts)/((Hard_Counts+Medium_Counts))
    SC_Ratio=(Medium_Counts-Soft_Counts)/((Medium_Counts+Soft_Counts))
    """
    Alt_Soft_Counts=Data["NET_COUNTS_0.3-1.0"]
    Alt_Medium_Counts=Data["NET_COUNTS_1.0-2.0"]
    Alt_Hard_Counts=Data["NET_COUNTS_2.0-8.0"]
    Alt_HC_Ratio=(Hard_Counts-Medium_Counts)/((Hard_Counts+Medium_Counts))
    Alt_SC_Ratio=(Medium_Counts-Soft_Counts)/((Medium_Counts+Soft_Counts))
    fig = plt.figure()
    ax = plt.axes()
    ax.scatter(HC_Ratio_Counts, SC_Ratio_Counts, c=Source_Distance_From_GC_Elliptical_D25, marker=".", alpha=0.2, vmax=10.0)
    ax.scatter(HC_Ratio_Counts_SNR, SC_Ratio_Counts_SNR, c="red", marker="o")
    ax.scatter(HC_Ratio_Counts_XRB, SC_Ratio_Counts_XRB, c="blue", marker="o")
    plt.errorbar(HC_Ratio_Counts_SNR, SC_Ratio_Counts_SNR, xerr=Thermal_SNR_Data["Hard_Counts_Color_Error"], yerr=Thermal_SNR_Data["Soft_Counts_Color_Error"], ls='none', c="red")
    plt.errorbar(HC_Ratio_Counts_XRB, SC_Ratio_Counts_XRB, xerr=XRB_Data["Hard_Counts_Color_Error"], yerr=XRB_Data["Soft_Counts_Color_Error"], ls='none', c="blue")
    ax.scatter(Alt_HC_Ratio, Alt_SC_Ratio, c="black", marker=".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Counts_Distance_with_SN_with_Alt.pdf")
    plt.cla()
    plt.clf()
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate=Data["NET_RATE_0.3-1.0"]
    Medium_Rate=Data["NET_RATE_1.0-2.1"]
    Hard_Rate=Data["NET_RATE_2.1-7.5"]
    #Beta
    Soft_Beta=Soft_Flux/Soft_Rate
    Medium_Beta=Medium_Flux/Medium_Rate
    Hard_Beta=Hard_Flux/Hard_Rate
    fig = plt.figure()
    ax = plt.axes()
    #HC_Ratio_Beta, SC_Ratio_Beta=Color_Color_Calc(Soft_Beta,Medium_Beta,Hard_Beta)
    HC_Ratio_Beta=(Hard_Beta-Medium_Beta)/((Hard_Beta+Medium_Beta))
    SC_Ratio_Beta=(Medium_Beta-Soft_Beta)/((Medium_Beta+Soft_Beta))
    ax.scatter(HC_Ratio_Beta, SC_Ratio_Beta, c=Source_Distance_From_GC_Elliptical_D25, marker=".", alpha=0.2, vmax=10.0)
    #ax.scatter(HC_Ratio_Counts_SNR, SC_Ratio_Counts_SNR, c="red", marker="o")
    #ax.scatter(HC_Ratio_Counts_XRB, SC_Ratio_Counts_XRB, c="blue", marker="o")
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Beta_Distance.pdf")
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate=Data["NET_RATE_0.3-1.0"]
    Medium_Rate=Data["NET_RATE_1.0-2.1"]
    Hard_Rate=Data["NET_RATE_2.1-7.5"]
    #Beta
    Soft_Beta=Soft_Flux/Soft_Rate
    Medium_Beta=Medium_Flux/Medium_Rate
    Hard_Beta=Hard_Flux/Hard_Rate

    Soft_Flux_Thermal_SNR=Thermal_SNR_Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_Thermal_SNR=Thermal_SNR_Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_Thermal_SNR=Thermal_SNR_Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate_Thermal_SNR=Thermal_SNR_Data["NET_RATE_0.3-1.0"]
    Medium_Rate_Thermal_SNR=Thermal_SNR_Data["NET_RATE_1.0-2.1"]
    Hard_Rate_Thermal_SNR=Thermal_SNR_Data["NET_RATE_2.1-7.5"]
    #Beta
    Soft_Beta_Thermal_SNR=Soft_Flux_Thermal_SNR/Soft_Rate_Thermal_SNR
    Medium_Beta_Thermal_SNR=Medium_Flux_Thermal_SNR/Medium_Rate_Thermal_SNR
    Hard_Beta_Thermal_SNR=Hard_Flux/Hard_Rate_Thermal_SNR

    Soft_Flux_XRB=XRB_Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_XRB=XRB_Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_XRB=XRB_Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate_XRB=XRB_Data["NET_RATE_0.3-1.0"]
    Medium_Rate_XRB=XRB_Data["NET_RATE_1.0-2.1"]
    Hard_Rate_XRB=XRB_Data["NET_RATE_2.1-7.5"]
    #Beta
    Soft_Beta_XRB=Soft_Flux_XRB/Soft_Rate_XRB
    Medium_Beta_XRB=Medium_Flux_XRB/Medium_Rate_XRB
    Hard_Beta_XRB=Hard_Flux/Hard_Rate_XRB

    """
    HC_Ratio_Flux_SN=Thermal_SN_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_SN=Thermal_SN_Data["Soft_Flux_Color"]
    HC_Ratio_Flux_SNR=Thermal_SNR_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_SNR=Thermal_SNR_Data["Soft_Flux_Color"]
    HC_Ratio_Flux_XRB=XRB_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_XRB=XRB_Data["Soft_Flux_Color"]

    """
    fig = plt.figure()
    ax = plt.axes()
    #HC_Ratio_Beta, SC_Ratio_Beta=Color_Color_Calc(Soft_Beta,Medium_Beta,Hard_Beta)
    HC_Ratio_Beta_Thermal_SNR=(Hard_Beta_Thermal_SNR-Medium_Beta_Thermal_SNR)/((Hard_Beta_Thermal_SNR+Medium_Beta_Thermal_SNR))
    SC_Ratio_Beta_Thermal_SNR=(Medium_Beta-Soft_Beta_Thermal_SNR)/((Medium_Beta+Soft_Beta_Thermal_SNR))
    HC_Ratio_Beta_Thermal_SNR=(Hard_Beta-Medium_Beta_Thermal_SNR)/((Hard_Beta+Medium_Beta_Thermal_SNR))
    SC_Ratio_Beta_Thermal_SNR=(Medium_Beta-Soft_Beta_Thermal_SNR)/((Medium_Beta+Soft_Beta_Thermal_SNR))
    HC_Ratio_Beta_XRB=(Hard_Beta-Medium_Beta_XRB)/((Hard_Beta+Medium_Beta_XRB))
    SC_Ratio_Beta_XRB=(Medium_Beta-Soft_Beta_XRB)/((Medium_Beta+Soft_Beta_XRB))
    ax.scatter(HC_Ratio_Beta, SC_Ratio_Beta, c=Source_Distance_From_GC_Elliptical_D25, marker=".", alpha=0.2, vmax=10.0)
    ax.scatter(HC_Ratio_Beta_Thermal_SNR, SC_Ratio_Beta_Thermal_SNR, c="red", marker="o")
    ax.scatter(HC_Ratio_Beta_XRB, SC_Ratio_Beta_XRB, c="blue", marker="o")
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Beta_Distance_With_SN.pdf")
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate=Data["NET_RATE_0.3-1.0"]
    Medium_Rate=Data["NET_RATE_1.0-2.1"]
    Hard_Rate=Data["NET_RATE_2.1-7.5"]
    #Effective_Area
    #Effective_Area_0.3-1.0
    Soft_Effective_Area=Data["Effective_Area_0.3-1.0"]
    Medium_Effective_Area=Data["Effective_Area_1.0-2.1"]
    Hard_Effective_Area=Data["Effective_Area_2.1-7.5"]
    #Rate_Effective_Area_Corrected
    Soft_Rate_Effective_Area_Corrected=Soft_Rate/Soft_Effective_Area
    Medium_Rate_Effective_Area_Corrected=Medium_Rate/Medium_Effective_Area
    Hard_Rate_Effective_Area_Corrected=Hard_Rate/Hard_Effective_Area
    #Beta
    Soft_Beta=Soft_Flux/Soft_Rate_Effective_Area_Corrected
    Medium_Beta=Medium_Flux/Medium_Rate_Effective_Area_Corrected
    Hard_Beta=Hard_Flux/Hard_Rate_Effective_Area_Corrected

    Soft_Flux_Thermal_SNR=Thermal_SNR_Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_Thermal_SNR=Thermal_SNR_Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_Thermal_SNR=Thermal_SNR_Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate_Thermal_SNR=Thermal_SNR_Data["NET_RATE_0.3-1.0"]
    Medium_Rate_Thermal_SNR=Thermal_SNR_Data["NET_RATE_1.0-2.1"]
    Hard_Rate_Thermal_SNR=Thermal_SNR_Data["NET_RATE_2.1-7.5"]

    Soft_Effective_Area_Thermal_SNR=Thermal_SNR_Data["Effective_Area_0.3-1.0"]
    Medium_Effective_Area_Thermal_SNR=Thermal_SNR_Data["Effective_Area_1.0-2.1"]
    Hard_Effective_Area_Thermal_SNR=Thermal_SNR_Data["Effective_Area_2.1-7.5"]
    #Rate_Effective_Area_Corrected
    Soft_Rate_Effective_Area_Corrected_Thermal_SNR=Soft_Rate/Soft_Effective_Area_Thermal_SNR
    Medium_Rate_Effective_Area_Corrected_Thermal_SNR=Medium_Rate/Medium_Effective_Area_Thermal_SNR
    Hard_Rate_Effective_Area_Corrected_Thermal_SNR=Hard_Rate/Hard_Effective_Area_Thermal_SNR

    #Beta
    Soft_Beta_Thermal_SNR=Soft_Flux_Thermal_SNR/Soft_Rate_Effective_Area_Corrected
    Medium_Beta_Thermal_SNR=Medium_Flux_Thermal_SNR/Medium_Rate_Effective_Area_Corrected
    Hard_Beta_Thermal_SNR=Hard_Flux_Thermal_SNR/Hard_Rate_Effective_Area_Corrected

    Soft_Flux_XRB=XRB_Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_XRB=XRB_Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_XRB=XRB_Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate_XRB=XRB_Data["NET_RATE_0.3-1.0"]
    Medium_Rate_XRB=XRB_Data["NET_RATE_1.0-2.1"]
    Hard_Rate_XRB=XRB_Data["NET_RATE_2.1-7.5"]

    Soft_Effective_Area_XRB=XRB_Data["Effective_Area_0.3-1.0"]
    Medium_Effective_Area_XRB=XRB_Data["Effective_Area_1.0-2.1"]
    Hard_Effective_Area_XRB=XRB_Data["Effective_Area_2.1-7.5"]
    #Rate_Effective_Area_Corrected
    Soft_Rate_Effective_Area_Corrected_XRB=Soft_Rate_XRB/Soft_Effective_Area_XRB
    Medium_Rate_Effective_Area_Corrected_XRB=Medium_Rate_XRB/Medium_Effective_Area_XRB
    Hard_Rate_Effective_Area_Corrected_XRB=Hard_Rate_XRB/Hard_Effective_Area_XRB

    #Beta
    Soft_Beta_XRB=Soft_Flux_XRB/Soft_Rate_Effective_Area_Corrected_XRB
    Medium_Beta_XRB=Medium_Flux_XRB/Medium_Rate_Effective_Area_Corrected_XRB
    Hard_Beta_XRB=Hard_Flux/Hard_Rate_Effective_Area_Corrected_XRB


    """
    HC_Ratio_Flux_SN=Thermal_SN_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_SN=Thermal_SN_Data["Soft_Flux_Color"]
    HC_Ratio_Flux_SNR=Thermal_SNR_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_SNR=Thermal_SNR_Data["Soft_Flux_Color"]
    HC_Ratio_Flux_XRB=XRB_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_XRB=XRB_Data["Soft_Flux_Color"]

    """
    fig = plt.figure()
    ax = plt.axes()
    #HC_Ratio_Beta, SC_Ratio_Beta=Color_Color_Calc(Soft_Beta,Medium_Beta,Hard_Beta)
    HC_Ratio_Beta=(Hard_Beta-Medium_Beta)/((Hard_Beta+Medium_Beta))
    SC_Ratio_Beta=(Medium_Beta-Soft_Beta)/((Medium_Beta+Soft_Beta))
    HC_Ratio_Beta_Thermal_SNR=(Hard_Beta_Thermal_SNR-Medium_Beta_Thermal_SNR)/((Hard_Beta_Thermal_SNR+Medium_Beta_Thermal_SNR))
    SC_Ratio_Beta_Thermal_SNR=(Medium_Beta-Soft_Beta_Thermal_SNR)/((Medium_Beta+Soft_Beta_Thermal_SNR))
    HC_Ratio_Beta_Thermal_SNR=(Hard_Beta-Medium_Beta_Thermal_SNR)/((Hard_Beta+Medium_Beta_Thermal_SNR))
    SC_Ratio_Beta_Thermal_SNR=(Medium_Beta-Soft_Beta_Thermal_SNR)/((Medium_Beta+Soft_Beta_Thermal_SNR))
    HC_Ratio_Beta_XRB=(Hard_Beta-Medium_Beta_XRB)/((Hard_Beta+Medium_Beta_XRB))
    SC_Ratio_Beta_XRB=(Medium_Beta-Soft_Beta_XRB)/((Medium_Beta+Soft_Beta_XRB))
    ax.scatter(HC_Ratio_Beta, SC_Ratio_Beta, c=Source_Distance_From_GC_Elliptical_D25, marker=".", alpha=0.2, vmax=10.0)
    ax.scatter(HC_Ratio_Beta_Thermal_SNR, SC_Ratio_Beta_Thermal_SNR, c="red", marker="o")
    ax.scatter(HC_Ratio_Beta_XRB, SC_Ratio_Beta_XRB, c="blue", marker="o")
    plt.xlim(0, 1.0)
    #plt.xlim(0.4, 0.8)
    #plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Beta_Distance_With_SN_Effective_Area_Corrected.pdf")
    #plt.savefig("Color_Color_Beta_Distance_With_SN_Zoomed_2.pdf")
    plt.cla()
    plt.clf()
    #ax.scatter(HC_Ratio_Beta, SC_Ratio_Beta, c=Source_Distance_From_GC_Elliptical_D25, marker=".", alpha=0.2, vmax=10.0)
    plt.plot(SC_Ratio_Beta,Source_Distance_From_GC_Elliptical_D25, ".", alpha=0.2)
    plt.xlim(-1.0, 1.0)
    #plt.ylim(0, 20.0)
    plt.ylim(0, 10.0)
    plt.savefig("SC_Ratio_Beta_vs_Distance.pdf")
    plt.cla()
    plt.clf()
    plt.cla()
    plt.clf()
    Soft_Beta=Data["Beta_0.3-1.0"]
    Medium_Beta=Data["Beta_1.0-2.1"]
    Hard_Beta=Data["Beta_2.1-7.5"]
    #Source_Distance_From_GC_Elliptical_D25
    #plt.plot(Source_Distance_From_GC_Elliptical_D25, Soft_Beta, '.', alpha=0.2)
    plt.plot(Soft_Beta, Source_Distance_From_GC_Elliptical_D25, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    plt.xlim(0, 10E-11)
    plt.ylim(0, 10)
    plt.savefig("Soft_Beta_vs_Distance.pdf")
    plt.cla()
    plt.clf()
    Soft_Beta=Data["Beta_0.3-1.0"]
    Medium_Beta=Data["Beta_1.0-2.1"]
    Hard_Beta=Data["Beta_2.1-7.5"]
    #Source_Distance_From_GC_Elliptical_D25
    plt.plot(Medium_Beta, Source_Distance_From_GC_Elliptical_D25, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    plt.xlim(0, 10E-11)
    plt.ylim(0, 10)
    plt.savefig("Medium_Beta_vs_Distance.pdf")
    plt.cla()
    plt.clf()
    plt.clf()
    plt.clf()
    Soft_Beta=Data["Beta_0.3-1.0"]
    Medium_Beta=Data["Beta_1.0-2.1"]
    Hard_Beta=Data["Beta_2.1-7.5"]
    #Source_Distance_From_GC_Elliptical_D25
    plt.plot(Hard_Beta, Source_Distance_From_GC_Elliptical_D25, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    plt.xlim(0, 10E-11)
    plt.ylim(0, 10)
    plt.savefig("Hard_Beta_vs_Distance.pdf")
    plt.cla()
    plt.clf()
    Soft_Beta=Data["Beta_0.3-1.0"]
    Medium_Beta=Data["Beta_1.0-2.1"]
    Hard_Beta=Data["Beta_2.1-7.5"]
    #Source_Distance_From_GC_Elliptical_D25
    #plt.plot(Source_Distance_From_GC_Elliptical_D25, Soft_Beta, '.', alpha=0.2)
    plt.plot(Soft_Beta, Source_Distance_From_GC_Elliptical_D25, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    plt.ylim(0, 4)
    plt.xlim(0, 0.4E-11)
    plt.savefig("Soft_Beta_vs_Distance_Zoomed.pdf")
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Soft_Beta=Data["Beta_0.3-1.0"]
    Medium_Beta=Data["Beta_1.0-2.1"]
    Hard_Beta=Data["Beta_2.1-7.5"]
    #Source_Distance_From_GC_Elliptical_D25
    #plt.plot(Source_Distance_From_GC_Elliptical_D25, Soft_Beta, '.', alpha=0.2)
    plt.plot(Soft_Beta, Source_Distance_From_GC_Elliptical_D25, '.', alpha=0.2)
    plt.plot(Medium_Beta, Source_Distance_From_GC_Elliptical_D25, '.', alpha=0.2)
    plt.plot(Hard_Beta, Source_Distance_From_GC_Elliptical_D25, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    plt.xlim(0, 10E-11)
    plt.ylim(0, 10)
    plt.savefig("All_Beta_vs_Distance.pdf")
    plt.cla()
    plt.clf()


    plt.cla()
    plt.clf()
    Soft_Beta=Data["Beta_0.3-1.0"]
    Medium_Beta=Data["Beta_1.0-2.1"]
    Hard_Beta=Data["Beta_2.1-7.5"]
    #Source_Distance_From_GC_Elliptical_D25
    #plt.plot(Source_Distance_From_GC_Elliptical_D25, Soft_Beta, '.', alpha=0.2)
    plt.hist(Soft_Beta, bins=100, range=(0, 10E-11))
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.savefig("Soft_Beta_Hist.pdf")
    #plt.show()
    plt.cla()
    plt.clf()
    Soft_Beta=Data["Beta_0.3-1.0"]
    Medium_Beta=Data["Beta_1.0-2.1"]
    Hard_Beta=Data["Beta_2.1-7.5"]
    #Source_Distance_From_GC_Elliptical_D25
    #plt.plot(Source_Distance_From_GC_Elliptical_D25, Soft_Beta, '.', alpha=0.2)
    plt.hist(Medium_Beta, bins=100, range=(0, 10E-11))
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.savefig("Medium_Beta_Hist.pdf")
    #plt.show()
    plt.cla()
    plt.clf()
    Soft_Beta=Data["Beta_0.3-1.0"]
    Medium_Beta=Data["Beta_1.0-2.1"]
    Hard_Beta=Data["Beta_2.1-7.5"]
    #Source_Distance_From_GC_Elliptical_D25
    #plt.plot(Source_Distance_From_GC_Elliptical_D25, Soft_Beta, '.', alpha=0.2)
    plt.hist(Hard_Beta, bins=100, range=(0, 10E-11))
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.savefig("Hard_Beta_Hist.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Soft_Beta=Data["Beta_0.3-1.0"]
    Medium_Beta=Data["Beta_1.0-2.1"]
    Hard_Beta=Data["Beta_2.1-7.5"]
    #Source_Distance_From_GC_Elliptical_D25
    #plt.plot(Source_Distance_From_GC_Elliptical_D25, Soft_Beta, '.', alpha=0.2)
    plt.hist(Soft_Beta, bins=100, range=(0, 10E-11), alpha=0.2)
    plt.hist(Medium_Beta, bins=100, range=(0, 10E-11), alpha=0.2)
    plt.hist(Hard_Beta, bins=100, range=(0, 10E-11), alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.savefig("All_Beta_Hist.pdf")
    #plt.show()
    plt.cla()
    plt.clf()


    plt.cla()
    plt.clf()
    Soft_Beta=Data["Beta_0.3-1.0"]
    Medium_Beta=Data["Beta_1.0-2.1"]
    Hard_Beta=Data["Beta_2.1-7.5"]
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Soft_Beta, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.ylim(0, 10E-11)
    plt.savefig("Soft_Beta_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Soft_Beta=Data["Beta_0.3-1.0"]
    Medium_Beta=Data["Beta_1.0-2.1"]
    Hard_Beta=Data["Beta_2.1-7.5"]
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Medium_Beta, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.ylim(0, 10E-11)
    plt.savefig("Medium_Beta_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Soft_Beta=Data["Beta_0.3-1.0"]
    Medium_Beta=Data["Beta_1.0-2.1"]
    Hard_Beta=Data["Beta_2.1-7.5"]
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Hard_Beta, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.ylim(0, 10E-11)
    plt.savefig("Hard_Beta_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate=Data["NET_RATE_0.3-1.0"]
    Medium_Rate=Data["NET_RATE_1.0-2.1"]
    Hard_Rate=Data["NET_RATE_2.1-7.5"]
    #Effective_Area
    #Effective_Area_0.3-1.0
    Soft_Effective_Area=Data["Effective_Area_0.3-1.0"]
    Medium_Effective_Area=Data["Effective_Area_1.0-2.1"]
    Hard_Effective_Area=Data["Effective_Area_2.1-7.5"]
    #Rate_Effective_Area_Corrected
    Soft_Rate_Effective_Area_Corrected=Soft_Rate/Soft_Effective_Area
    Medium_Rate_Effective_Area_Corrected=Medium_Rate/Medium_Effective_Area
    Hard_Rate_Effective_Area_Corrected=Hard_Rate/Hard_Effective_Area
    #Beta
    Soft_Beta=Soft_Flux/Soft_Rate_Effective_Area_Corrected
    Medium_Beta=Medium_Flux/Medium_Rate_Effective_Area_Corrected
    Hard_Beta=Hard_Flux/Hard_Rate_Effective_Area_Corrected
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Soft_Beta, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.ylim(0, 10E-11)
    plt.savefig("Soft_Beta_Effective_Area_Corrected_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate=Data["NET_RATE_0.3-1.0"]
    Medium_Rate=Data["NET_RATE_1.0-2.1"]
    Hard_Rate=Data["NET_RATE_2.1-7.5"]
    #Effective_Area
    #Effective_Area_0.3-1.0
    Soft_Effective_Area=Data["Effective_Area_0.3-1.0"]
    Medium_Effective_Area=Data["Effective_Area_1.0-2.1"]
    Hard_Effective_Area=Data["Effective_Area_2.1-7.5"]
    #Rate_Effective_Area_Corrected
    Soft_Rate_Effective_Area_Corrected=Soft_Rate/Soft_Effective_Area
    Medium_Rate_Effective_Area_Corrected=Medium_Rate/Medium_Effective_Area
    Hard_Rate_Effective_Area_Corrected=Hard_Rate/Hard_Effective_Area
    #Beta
    Soft_Beta=Soft_Flux/Soft_Rate_Effective_Area_Corrected
    Medium_Beta=Medium_Flux/Medium_Rate_Effective_Area_Corrected
    Hard_Beta=Hard_Flux/Hard_Rate_Effective_Area_Corrected
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Medium_Beta, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.ylim(0, 10E-11)
    plt.savefig("Medium_Beta_Effective_Area_Corrected_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate=Data["NET_RATE_0.3-1.0"]
    Medium_Rate=Data["NET_RATE_1.0-2.1"]
    Hard_Rate=Data["NET_RATE_2.1-7.5"]
    #Effective_Area
    #Effective_Area_0.3-1.0
    Soft_Effective_Area=Data["Effective_Area_0.3-1.0"]
    Medium_Effective_Area=Data["Effective_Area_1.0-2.1"]
    Hard_Effective_Area=Data["Effective_Area_2.1-7.5"]
    #Rate_Effective_Area_Corrected
    Soft_Rate_Effective_Area_Corrected=Soft_Rate/Soft_Effective_Area
    Medium_Rate_Effective_Area_Corrected=Medium_Rate/Medium_Effective_Area
    Hard_Rate_Effective_Area_Corrected=Hard_Rate/Hard_Effective_Area
    #Beta
    Soft_Beta=Soft_Flux/Soft_Rate_Effective_Area_Corrected
    Medium_Beta=Medium_Flux/Medium_Rate_Effective_Area_Corrected
    Hard_Beta=Hard_Flux/Hard_Rate_Effective_Area_Corrected
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Hard_Beta, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.ylim(0, 10E-11)
    plt.savefig("Hard_Beta_Effective_Area_Corrected_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    #Soft_Rate_Effective_Area_Corrected
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Soft_Rate, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 0.01)
    plt.ylim(0, 0.002)
    plt.savefig("Soft_Rate_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    #Soft_Rate_Effective_Area_Corrected
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Soft_Rate_Effective_Area_Corrected, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    #plt.ylim(0, 0.01)
    plt.ylim(0, 0.002)
    plt.savefig("Soft_Rate_Effective_Area_Corrected_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    #Medium_Rate_Effective_Area_Corrected
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Medium_Rate, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 0.01)
    plt.ylim(0, 0.002)
    plt.savefig("Medium_Rate_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    #Medium_Rate_Effective_Area_Corrected
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Medium_Rate_Effective_Area_Corrected, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    #plt.ylim(0, 0.01)
    plt.ylim(0, 0.002)
    plt.savefig("Medium_Rate_Effective_Area_Corrected_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    #Hard_Rate_Effective_Area_Corrected
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Hard_Rate, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 0.01)
    plt.ylim(0, 0.002)
    plt.savefig("Hard_Rate_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    #Hard_Rate_Effective_Area_Corrected
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Hard_Rate_Effective_Area_Corrected, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    #plt.ylim(0, 0.01)
    plt.ylim(0, 0.002)
    plt.savefig("Hard_Rate_Effective_Area_Corrected_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()


    plt.cla()
    plt.clf()
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Soft_Flux, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    #plt.ylim(10E-15, 10E-14)
    plt.ylim(10E-16, 10E-13)
    plt.savefig("Soft_Flux_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Medium_Flux, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    #plt.ylim(10E-15, 10E-14)
    plt.ylim(10E-16, 10E-13)
    plt.savefig("Medium_Flux_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Hard_Flux, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    #plt.ylim(10E-15, 10E-14)
    plt.ylim(10E-16, 10E-13)
    plt.savefig("Hard_Flux_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()


    #"""
    plt.cla()
    plt.clf()
    Thermal_SN_Data=Thermal_SN_Calc(Data)
    #Thermal_SNR_Data=Thermal_SN_Data[Thermal_SN_Data["Color_Color_Classification"]=="Thermal_SNR"]
    Thermal_SNR_Data=Thermal_SNR_Calc(Data)
    #XRB_Data=Thermal_SN_Data[Thermal_SN_Data["Color_Color_Classification"]=="XRB"]
    XRB_Data=XRB_Calc(Data)
    HC_Ratio_Flux=Data["Hard_Flux_Color"]
    SC_Ratio_Flux=Data["Soft_Flux_Color"]
    HC_Ratio_Flux_SN=Thermal_SN_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_SN=Thermal_SN_Data["Soft_Flux_Color"]
    HC_Ratio_Flux_SNR=Thermal_SNR_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_SNR=Thermal_SNR_Data["Soft_Flux_Color"]
    HC_Ratio_Flux_XRB=XRB_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_XRB=XRB_Data["Soft_Flux_Color"]

    fig = plt.figure()
    ax = plt.axes()
    ##ax.scatter(HC_Ratio_Flux, SC_Ratio_Flux, c=Start_Date, marker=".", alpha=0.2)
    Start_Date_L=list(Start_Date)
    Start_Timestamp_L=[]
    for Date in Start_Date_L:
        #date_object = datetime.strptime(date_str, '%m-%d-%Y').date()
        #1999-12-05T21:37:28
        #Cur_Date=datetime.strptime(Date, '%Y-%m-%dT%H:%M:%S').date()
        Cur_Date=datetime.strptime(Date, '%Y-%m-%dT%H:%M:%S')
        Cur_Timestamp=Cur_Date.timestamp()
        Start_Timestamp_L.append(Cur_Timestamp)
    ax.scatter(HC_Ratio_Flux, SC_Ratio_Flux, c=Start_Timestamp_L, marker=".", alpha=0.2)
    #ax.scatter(HC_Ratio_Flux_SN, SC_Ratio_Flux_SN, c="red", marker="o")
    ax.scatter(HC_Ratio_Flux_SNR, SC_Ratio_Flux_SNR, c="red", marker="o")
    ax.scatter(HC_Ratio_Flux_XRB, SC_Ratio_Flux_XRB, c="blue", marker="o")
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Flux_Start_Date_with_SN.pdf")
    plt.cla()
    plt.clf()
    #"""

    plt.cla()
    plt.clf()
    Soft_Beta_Color=Data["Soft_Beta_Color"]
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Soft_Beta_Color, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Soft_Beta_Color_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    #Soft_Beta_Color=Data["Soft_Beta_Color"]
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate=Data["NET_RATE_0.3-1.0"]
    Medium_Rate=Data["NET_RATE_1.0-2.1"]
    Hard_Rate=Data["NET_RATE_2.1-7.5"]
    #Effective_Area
    #Effective_Area_0.3-1.0
    Soft_Effective_Area=Data["Effective_Area_0.3-1.0"]
    Medium_Effective_Area=Data["Effective_Area_1.0-2.1"]
    Hard_Effective_Area=Data["Effective_Area_2.1-7.5"]
    #Rate_Effective_Area_Corrected
    Soft_Rate_Effective_Area_Corrected=Soft_Rate/Soft_Effective_Area
    Medium_Rate_Effective_Area_Corrected=Medium_Rate/Medium_Effective_Area
    Hard_Rate_Effective_Area_Corrected=Hard_Rate/Hard_Effective_Area
    #Beta
    Soft_Beta=Soft_Flux/Soft_Rate_Effective_Area_Corrected
    Medium_Beta=Medium_Flux/Medium_Rate_Effective_Area_Corrected
    Hard_Beta=Hard_Flux/Hard_Rate_Effective_Area_Corrected
    #HC_Ratio_Beta=(Hard_Beta-Medium_Beta)/((Hard_Beta+Medium_Beta))
    SC_Ratio_Beta=(Medium_Beta-Soft_Beta)/((Medium_Beta+Soft_Beta))
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, SC_Ratio_Beta, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Soft_Beta_Color_Effective_Area_Corrected_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Hard_Beta_Color=Data["Hard_Beta_Color"]
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Hard_Beta_Color, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Hard_Beta_Color_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    #Soft_Beta_Color=Data["Soft_Beta_Color"]
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate=Data["NET_RATE_0.3-1.0"]
    Medium_Rate=Data["NET_RATE_1.0-2.1"]
    Hard_Rate=Data["NET_RATE_2.1-7.5"]
    #Effective_Area
    #Effective_Area_0.3-1.0
    Soft_Effective_Area=Data["Effective_Area_0.3-1.0"]
    Medium_Effective_Area=Data["Effective_Area_1.0-2.1"]
    Hard_Effective_Area=Data["Effective_Area_2.1-7.5"]
    #Rate_Effective_Area_Corrected
    Soft_Rate_Effective_Area_Corrected=Soft_Rate/Soft_Effective_Area
    Medium_Rate_Effective_Area_Corrected=Medium_Rate/Medium_Effective_Area
    Hard_Rate_Effective_Area_Corrected=Hard_Rate/Hard_Effective_Area
    #Beta
    Soft_Beta=Soft_Flux/Soft_Rate_Effective_Area_Corrected
    Medium_Beta=Medium_Flux/Medium_Rate_Effective_Area_Corrected
    Hard_Beta=Hard_Flux/Hard_Rate_Effective_Area_Corrected
    HC_Ratio_Beta=(Hard_Beta-Medium_Beta)/((Hard_Beta+Medium_Beta))
    #SC_Ratio_Beta=(Medium_Beta-Soft_Beta)/((Medium_Beta+Soft_Beta))
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, HC_Ratio_Beta, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Hard_Beta_Color_Effective_Area_Corrected_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Soft_Flux_Color=Data["Soft_Flux_Color"]
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Soft_Flux_Color, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Soft_Flux_Color_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Hard_Flux_Color=Data["Hard_Flux_Color"]
    Start_Date=Data["Start_Date"]
    plt.plot(Start_Date, Hard_Flux_Color, '.', alpha=0.2)
    #plt.ylim(-0.00001, 0.00001)
    #plt.ylim(-10E-11, 10E-11)
    #plt.xlim(0, 10E-11)
    #plt.ylim(0, 10)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Hard_Flux_Color_vs_Start_Date.pdf")
    #plt.show()
    plt.cla()
    plt.clf()




    plt.cla()
    plt.clf()
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate=Data["NET_RATE_0.3-1.0"]
    Medium_Rate=Data["NET_RATE_1.0-2.1"]
    Hard_Rate=Data["NET_RATE_2.1-7.5"]
    #Beta
    Soft_Beta=Soft_Flux/Soft_Rate
    Medium_Beta=Medium_Flux/Medium_Rate
    Hard_Beta=Hard_Flux/Hard_Rate

    Soft_Flux_Thermal_SNR=Thermal_SNR_Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_Thermal_SNR=Thermal_SNR_Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_Thermal_SNR=Thermal_SNR_Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate_Thermal_SNR=Thermal_SNR_Data["NET_RATE_0.3-1.0"]
    Medium_Rate_Thermal_SNR=Thermal_SNR_Data["NET_RATE_1.0-2.1"]
    Hard_Rate_Thermal_SNR=Thermal_SNR_Data["NET_RATE_2.1-7.5"]
    #Beta
    Soft_Beta_Thermal_SNR=Soft_Flux_Thermal_SNR/Soft_Rate_Thermal_SNR
    Medium_Beta_Thermal_SNR=Medium_Flux_Thermal_SNR/Medium_Rate_Thermal_SNR
    Hard_Beta_Thermal_SNR=Hard_Flux/Hard_Rate_Thermal_SNR

    Soft_Flux_XRB=XRB_Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_XRB=XRB_Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_XRB=XRB_Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate_XRB=XRB_Data["NET_RATE_0.3-1.0"]
    Medium_Rate_XRB=XRB_Data["NET_RATE_1.0-2.1"]
    Hard_Rate_XRB=XRB_Data["NET_RATE_2.1-7.5"]
    #Beta
    Soft_Beta_XRB=Soft_Flux_XRB/Soft_Rate_XRB
    Medium_Beta_XRB=Medium_Flux_XRB/Medium_Rate_XRB
    Hard_Beta_XRB=Hard_Flux/Hard_Rate_XRB

    """
    HC_Ratio_Flux_SN=Thermal_SN_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_SN=Thermal_SN_Data["Soft_Flux_Color"]
    HC_Ratio_Flux_SNR=Thermal_SNR_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_SNR=Thermal_SNR_Data["Soft_Flux_Color"]
    HC_Ratio_Flux_XRB=XRB_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_XRB=XRB_Data["Soft_Flux_Color"]

    """
    fig = plt.figure()
    ax = plt.axes()
    #HC_Ratio_Beta, SC_Ratio_Beta=Color_Color_Calc(Soft_Beta,Medium_Beta,Hard_Beta)
    HC_Ratio_Beta_Thermal_SNR=(Hard_Beta_Thermal_SNR-Medium_Beta_Thermal_SNR)/((Hard_Beta_Thermal_SNR+Medium_Beta_Thermal_SNR))
    SC_Ratio_Beta_Thermal_SNR=(Medium_Beta-Soft_Beta_Thermal_SNR)/((Medium_Beta+Soft_Beta_Thermal_SNR))
    HC_Ratio_Beta_Thermal_SNR=(Hard_Beta-Medium_Beta_Thermal_SNR)/((Hard_Beta+Medium_Beta_Thermal_SNR))
    SC_Ratio_Beta_Thermal_SNR=(Medium_Beta-Soft_Beta_Thermal_SNR)/((Medium_Beta+Soft_Beta_Thermal_SNR))
    HC_Ratio_Beta_XRB=(Hard_Beta-Medium_Beta_XRB)/((Hard_Beta+Medium_Beta_XRB))
    SC_Ratio_Beta_XRB=(Medium_Beta-Soft_Beta_XRB)/((Medium_Beta+Soft_Beta_XRB))
    ax.scatter(HC_Ratio_Beta, SC_Ratio_Beta, c=Start_Timestamp_L, marker=".", alpha=0.2)
    ax.scatter(HC_Ratio_Beta_Thermal_SNR, SC_Ratio_Beta_Thermal_SNR, c="red", marker="o")
    ax.scatter(HC_Ratio_Beta_XRB, SC_Ratio_Beta_XRB, c="blue", marker="o")
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Beta_Start_Date_With_SN.pdf")
    plt.cla()
    plt.clf()

    plt.cla()
    plt.clf()
    Soft_Flux=Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux=Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux=Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate=Data["NET_RATE_0.3-1.0"]
    Medium_Rate=Data["NET_RATE_1.0-2.1"]
    Hard_Rate=Data["NET_RATE_2.1-7.5"]
    #Effective_Area
    #Effective_Area_0.3-1.0
    Soft_Effective_Area=Data["Effective_Area_0.3-1.0"]
    Medium_Effective_Area=Data["Effective_Area_1.0-2.1"]
    Hard_Effective_Area=Data["Effective_Area_2.1-7.5"]
    #Rate_Effective_Area_Corrected
    Soft_Rate_Effective_Area_Corrected=Soft_Rate/Soft_Effective_Area
    Medium_Rate_Effective_Area_Corrected=Medium_Rate/Medium_Effective_Area
    Hard_Rate_Effective_Area_Corrected=Hard_Rate/Hard_Effective_Area
    #Beta
    Soft_Beta=Soft_Flux/Soft_Rate_Effective_Area_Corrected
    Medium_Beta=Medium_Flux/Medium_Rate_Effective_Area_Corrected
    Hard_Beta=Hard_Flux/Hard_Rate_Effective_Area_Corrected

    Soft_Flux_Thermal_SNR=Thermal_SNR_Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_Thermal_SNR=Thermal_SNR_Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_Thermal_SNR=Thermal_SNR_Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate_Thermal_SNR=Thermal_SNR_Data["NET_RATE_0.3-1.0"]
    Medium_Rate_Thermal_SNR=Thermal_SNR_Data["NET_RATE_1.0-2.1"]
    Hard_Rate_Thermal_SNR=Thermal_SNR_Data["NET_RATE_2.1-7.5"]

    Soft_Effective_Area_Thermal_SNR=Thermal_SNR_Data["Effective_Area_0.3-1.0"]
    Medium_Effective_Area_Thermal_SNR=Thermal_SNR_Data["Effective_Area_1.0-2.1"]
    Hard_Effective_Area_Thermal_SNR=Thermal_SNR_Data["Effective_Area_2.1-7.5"]
    #Rate_Effective_Area_Corrected
    Soft_Rate_Effective_Area_Corrected_Thermal_SNR=Soft_Rate/Soft_Effective_Area_Thermal_SNR
    Medium_Rate_Effective_Area_Corrected_Thermal_SNR=Medium_Rate/Medium_Effective_Area_Thermal_SNR
    Hard_Rate_Effective_Area_Corrected_Thermal_SNR=Hard_Rate/Hard_Effective_Area_Thermal_SNR

    #Beta
    Soft_Beta_Thermal_SNR=Soft_Flux_Thermal_SNR/Soft_Rate_Effective_Area_Corrected
    Medium_Beta_Thermal_SNR=Medium_Flux_Thermal_SNR/Medium_Rate_Effective_Area_Corrected
    Hard_Beta_Thermal_SNR=Hard_Flux_Thermal_SNR/Hard_Rate_Effective_Area_Corrected

    Soft_Flux_XRB=XRB_Data["NET_FLUX_APER_0.3-1.0"]
    Medium_Flux_XRB=XRB_Data["NET_FLUX_APER_1.0-2.1"]
    Hard_Flux_XRB=XRB_Data["NET_FLUX_APER_2.1-7.5"]
    #NET_RATE_
    Soft_Rate_XRB=XRB_Data["NET_RATE_0.3-1.0"]
    Medium_Rate_XRB=XRB_Data["NET_RATE_1.0-2.1"]
    Hard_Rate_XRB=XRB_Data["NET_RATE_2.1-7.5"]

    Soft_Effective_Area_XRB=XRB_Data["Effective_Area_0.3-1.0"]
    Medium_Effective_Area_XRB=XRB_Data["Effective_Area_1.0-2.1"]
    Hard_Effective_Area_XRB=XRB_Data["Effective_Area_2.1-7.5"]
    #Rate_Effective_Area_Corrected
    Soft_Rate_Effective_Area_Corrected_XRB=Soft_Rate_XRB/Soft_Effective_Area_XRB
    Medium_Rate_Effective_Area_Corrected_XRB=Medium_Rate_XRB/Medium_Effective_Area_XRB
    Hard_Rate_Effective_Area_Corrected_XRB=Hard_Rate_XRB/Hard_Effective_Area_XRB

    #Beta
    Soft_Beta_XRB=Soft_Flux_XRB/Soft_Rate_Effective_Area_Corrected_XRB
    Medium_Beta_XRB=Medium_Flux_XRB/Medium_Rate_Effective_Area_Corrected_XRB
    Hard_Beta_XRB=Hard_Flux/Hard_Rate_Effective_Area_Corrected_XRB


    """
    HC_Ratio_Flux_SN=Thermal_SN_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_SN=Thermal_SN_Data["Soft_Flux_Color"]
    HC_Ratio_Flux_SNR=Thermal_SNR_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_SNR=Thermal_SNR_Data["Soft_Flux_Color"]
    HC_Ratio_Flux_XRB=XRB_Data["Hard_Flux_Color"]
    SC_Ratio_Flux_XRB=XRB_Data["Soft_Flux_Color"]

    """
    fig = plt.figure()
    ax = plt.axes()
    #HC_Ratio_Beta, SC_Ratio_Beta=Color_Color_Calc(Soft_Beta,Medium_Beta,Hard_Beta)
    HC_Ratio_Beta=(Hard_Beta-Medium_Beta)/((Hard_Beta+Medium_Beta))
    SC_Ratio_Beta=(Medium_Beta-Soft_Beta)/((Medium_Beta+Soft_Beta))
    HC_Ratio_Beta_Thermal_SNR=(Hard_Beta_Thermal_SNR-Medium_Beta_Thermal_SNR)/((Hard_Beta_Thermal_SNR+Medium_Beta_Thermal_SNR))
    SC_Ratio_Beta_Thermal_SNR=(Medium_Beta-Soft_Beta_Thermal_SNR)/((Medium_Beta+Soft_Beta_Thermal_SNR))
    HC_Ratio_Beta_Thermal_SNR=(Hard_Beta-Medium_Beta_Thermal_SNR)/((Hard_Beta+Medium_Beta_Thermal_SNR))
    SC_Ratio_Beta_Thermal_SNR=(Medium_Beta-Soft_Beta_Thermal_SNR)/((Medium_Beta+Soft_Beta_Thermal_SNR))
    HC_Ratio_Beta_XRB=(Hard_Beta-Medium_Beta_XRB)/((Hard_Beta+Medium_Beta_XRB))
    SC_Ratio_Beta_XRB=(Medium_Beta-Soft_Beta_XRB)/((Medium_Beta+Soft_Beta_XRB))
    ax.scatter(HC_Ratio_Beta, SC_Ratio_Beta, c=Start_Timestamp_L, marker=".", alpha=0.2)
    ax.scatter(HC_Ratio_Beta_Thermal_SNR, SC_Ratio_Beta_Thermal_SNR, c="red", marker="o")
    ax.scatter(HC_Ratio_Beta_XRB, SC_Ratio_Beta_XRB, c="blue", marker="o")
    plt.xlim(0, 1.0)
    #plt.xlim(0.4, 0.8)
    #plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Beta_Start_Date_With_SN_Effective_Area_Corrected.pdf")
    #plt.savefig("Color_Color_Beta_Distance_With_SN_Zoomed_2.pdf")
    #'''
    plt.cla()
    plt.clf()
    Limiting_Flux_A=Data["Limiting_Flux"]
    Flux_A=Data["NET_FLUX_APER_0.3-8.0"]
    plt.loglog(Limiting_Flux_A, Flux_A, '.', alpha=0.2)
    plt.loglog(Limiting_Flux_A, Limiting_Flux_A, '.', alpha=0.2)
    plt.xlim(1E-19, 1E-9)
    plt.ylim(1E-19, 1E-9)
    plt.xlabel("Limiting_Flux (erg/s*cm^2)")
    plt.ylabel("Flux (erg/s*cm^2)")
    plt.savefig("Flux_vs_Limiting_Flux.pdf")
    plt.cla()
    plt.clf()
    Galactic_Distance_A=Data["Galactic_Distance"]
    Soft_Counts_Effective_Area_Corrected=Data["NET_COUNTS_AREA_CORRECTED_0.3-1.0"]
    Medium_Counts_Effective_Area_Corrected=Data["NET_COUNTS_AREA_CORRECTED_1.0-2.1"]
    Hard_Counts_Effective_Area_Corrected=Data["NET_COUNTS_AREA_CORRECTED_2.1-7.5"]
    Soft_Counts_Distance_Adjusted=Soft_Counts_Effective_Area_Corrected/(4.0*np.pi*(Galactic_Distance_A**2.0))
    Medium_Counts_Distance_Adjusted=Medium_Counts_Effective_Area_Corrected/(4.0*np.pi*(Galactic_Distance_A**2.0))
    Hard_Counts_Distance_Adjusted=Hard_Counts_Effective_Area_Corrected/(4.0*np.pi*(Galactic_Distance_A**2.0))
    #4.0*np.pi*(Galactic_Distance_A**2.0)
    fig = plt.figure()
    ax = plt.axes()
    #HC_Ratio_Beta, SC_Ratio_Beta=Color_Color_Calc(Soft_Beta,Medium_Beta,Hard_Beta)
    HC_Ratio_Counts_Distance_Adjusted=(Hard_Counts_Distance_Adjusted-Medium_Counts_Distance_Adjusted)/((Hard_Counts_Distance_Adjusted+Medium_Counts_Distance_Adjusted))
    SC_Ratio_Counts_Distance_Adjusted=(Medium_Counts_Distance_Adjusted-Soft_Counts_Distance_Adjusted)/((Medium_Counts_Distance_Adjusted+Soft_Counts_Distance_Adjusted))
    ax.scatter(HC_Ratio_Counts_Distance_Adjusted, SC_Ratio_Counts_Distance_Adjusted, c=Source_Distance_From_GC_Elliptical_D25, marker=".", alpha=0.2, vmax=10.0)
    #ax.scatter(HC_Ratio_Counts_SNR, SC_Ratio_Counts_SNR, c="red", marker="o")
    #ax.scatter(HC_Ratio_Counts_XRB, SC_Ratio_Counts_XRB, c="blue", marker="o")
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    plt.savefig("Color_Color_Counts_Galactic_Distance_Adjusted_Distance.pdf")
    plt.cla()
    plt.clf()

Flux_Plotting()
#print(Morph_Check("SAB(s)bc"))
#print(Morph_Check("E3"))
#print(Find_Duplicate(316,17))
#print(Find_Duplicate(316,31))
#print(Find_Duplicate(1302,54))
#Duplicate_Table_Calc()
#print(Thermal_SN_Calc())
