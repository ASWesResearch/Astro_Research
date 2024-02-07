import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import re

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



def Flux_Plotting(Standard_File_Fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/Source_Flux_All_Modified_3.csv"):
    Data=pd.read_csv(Standard_File_Fpath)
    Data_Outside_D25=Data[Data["Outside_D25_Bool"]]
    Data_Inside_D25=Data[Data["Outside_D25_Bool"]==False]
    Data_Outside_Elliptical_D25=Data[Data["Outside_Elliptical_D25_Bool"]]
    Data_Inside_Elliptical_D25=Data[Data["Outside_Elliptical_D25_Bool"]==False]
    Data_Count_Cut=Data[Data["NET_COUNTS_0.3-8.0"]> 25.0]
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
    Gname_A=Data["Gname_Modifed"]
    Galaxy_Morph_A=Data["Galaxy_Morph"]
    Data["Galaxy_Morph_Simple"]=np.vectorize(Morph_Check)(Galaxy_Morph_A)
    Data_Spiral=Data[Data["Galaxy_Morph_Simple"]=="S"]
    Data_Elliptical=Data[Data["Galaxy_Morph_Simple"]=="E"]
    Data_Irregular=Data[Data["Galaxy_Morph_Simple"]=="I"]
    Area_A=Data["AREA"]
    Gname_L=list(Gname_A)
    Gname_L_Unique =[]
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
    """
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
    plt.plot(Offaxis_Angle, Area_A, ".")
    plt.savefig("Source_Area_VS_Offaxis_Angle.pdf")
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
    """
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

#Flux_Plotting()
#print(Morph_Check("SAB(s)bc"))
#print(Morph_Check("E3"))
#print(Find_Duplicate(316,17))
#print(Find_Duplicate(316,31))
#print(Find_Duplicate(1302,54))
Duplicate_Table_Calc()
