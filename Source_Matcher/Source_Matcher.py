import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord

def Deg_to_Rad(Angle):
    Angle=(np.pi/180.0)*Angle
    return Angle

def Rad_to_Deg(Angle):
    Angle=(180.0/np.pi)*Angle
    return Angle

def Haversine_Distance(x1,x2,y1,y2):
    dx=x2-x1
    dy=y2-y1
    B=np.sqrt(((np.sin(dy/2.0))**2.0)+((np.cos(y1)*np.cos(y2))*((np.sin(dx/2.0))**2.0)))
    if(y1<0): #Note: This might not work for galaxies on the equator! This needs to be tested! #Note: This works on the equator as well!
        B=-1.0*B
    Have_Dist=2.0*np.arcsin(B)
    return Have_Dist

def Source_Matcher(Data_Input, RA_Key, Dec_Key, Data_Input_Standard="../SQL_Standard_File/Source_Flux_All_Modified_6.csv", RA_Key_Standard_File="RA", Dec_Key_Standard_File="Dec", Data_Filter_Tuple=None, Coord_Convert_Bool=False, Dist_Threshold=(2.0/3600.0)):
    if(isinstance(Data_Input,str)):
        Data=pd.read_csv(Data_Input)
    else:
        Data=Data_Input
    if(isinstance(Data_Input_Standard,str)):
        Data_Standard_File=pd.read_csv(Data_Input_Standard)
    else:
        Data_Standard_File=Data_Input_Standard
    if(Data_Filter_Tuple!=None):
        Filter_Key=Data_Filter_Tuple[0]
        Filter_Value=Data_Filter_Tuple[1]
        Data_Standard_File=Data_Standard_File[Data_Standard_File[Filter_Key]==Filter_Value]
    RA_L=list(Data[RA_Key])
    Dec_L=list(Data[Dec_Key])
    RA_Test_L=list(Data_Standard_File[RA_Key_Standard_File])
    Dec_Test_L=list(Data_Standard_File[Dec_Key_Standard_File])
    Match_Index_L=[]
    for i in range(0,len(RA_L)):
        RA=RA_L[i]
        Dec=Dec_L[i]
        if(Coord_Convert_Bool):
            Coords = SkyCoord(RA, Dec, frame='icrs', unit=(u.hourangle, u.deg))
            print("Coords: ", Coords)
            RA=float(Coords.ra.degree)
            Dec=float(Coords.dec.degree)
        #print("RA: ", RA)
        #print("type(RA): ", type(RA))
        x1_Rad=Deg_to_Rad(RA)
        y1_Rad=Deg_to_Rad(Dec)
        for j in range(0,len(RA_Test_L)):
            RA_Test=RA_Test_L[j]
            Dec_Test=Dec_Test_L[j]
            x2_Rad=Deg_to_Rad(RA_Test)
            y2_Rad=Deg_to_Rad(Dec_Test)
            Have_Dist=Haversine_Distance(x1_Rad,x2_Rad,y1_Rad,y2_Rad)
            Have_Dist=np.abs(Have_Dist)
            Have_Dist_Deg=Rad_to_Deg(Have_Dist)
            Dist=Have_Dist_Deg
            if(Dist<Dist_Threshold):
                Match_Bool=True
                print("Match_Found!!!")
                #break
                Match_Index_L.append(j)
                break
    Match_Data=Data_Standard_File.iloc[Match_Index_L]
    print(Match_Data)
    #Match_Data.to_csv("Matched_Data.csv")

#Source_Matcher("Test", None, None, None)
#Source_Matcher(True, None, None, None)
#Gname_Homogenized
#MESSIER 101
#Source_Matcher(Data_Input="./Chandra_Missing_Data_ds9.csv", RA_Key="ra", Dec_Key="decl", Data_Filter_Tuple=("Gname_Homogenized","MESSIER 101"), Coord_Convert_Bool=True)
