import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import pyplot
import pandas as pd
import os
from os import system
import sys
from astroquery.ned import Ned
from ciao_contrib.runtool import *
from region import *
import pickle as pl
import re
from scipy import integrate
#from sklearn import datasets
#from scipy import optimize

dir = os.path.dirname(__file__)
##path=os.path.realpath('../')
path=os.path.realpath(dir+'/../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))

from File_Query_Code import File_Query_Code_5
from Galaxy_Name_Reducer import Galaxy_Name_Reducer
from Background_Finder import Background_Finder_10
from D25_Finder import D25_Finder
from Area_Calc import Area_Calc_Frac_B_2_Alt_8
from Galaxy_Name_From_ObsID_Query import Galaxy_Name_From_ObsID_Query
from Log_N_Log_S_Plotting import Log_N_Log_S_Plotting

dir = os.path.dirname(__file__)
##path=os.path.realpath('../')
path=os.path.realpath(dir+'/../Marx_Source_Injection/')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))
from Source_Detection_Analysis import Source_Detection_Analysis

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

def Pickle_Save(Input, Outpath):
    pl.dump(Input, open(Outpath, 'wb'))

def Pickle_Load(Pickle_Path):
    Output = pl.load(open(Pickle_Path, 'rb'))
    return Output

def Pickle_Test():
    Test_Data="Hello_World!!!"
    Pickle_Save(Test_Data, "Hello_World.pickle")
    Unpickled_Data=Pickle_Load("Hello_World.pickle")
    print("Unpickled_Data: ", Unpickled_Data)

"""
def Background_Calc_Galaxy_Name_Input(Gname):
    Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
    Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
    print("Evt2_File_H_L: ", Evt2_File_H_L)
    Fov1_File_H_L=File_Query_Code_5.File_Query(Gname,"fov1")
    print("Fov1_File_H_L: ", Fov1_File_H_L)
    Reg_File_H_L=File_Query_Code_5.File_Query(Gname,"reg")
    print("Reg_File_H_L: ", Reg_File_H_L)
    if((len(Evt2_File_H_L)!=len(Fov1_File_H_L)) or (len(Evt2_File_H_L)!=len(Reg_File_H_L)) or (len(Fov1_File_H_L)!=len(Reg_File_H_L))):
        raise "Missing File!!!"
    Background_HL=[]
    for i in range(0,len(Evt2_File_H_L)):
        Cur_Evt2_File_L=Evt2_File_H_L[i]
        Cur_ObsID=Cur_Evt2_File_L[0]
        Cur_Evt2_Path=Cur_Evt2_File_L[1]
        Cur_Fov1_File_L=Fov1_File_H_L[i]
        Cur_Fov1_ObsID=Cur_Fov1_File_L[0]
        Cur_Fov1_Path=Cur_Fov1_File_L[1]
        Cur_Reg_File_L=Reg_File_H_L[i]
        Cur_Reg_ObsID=Cur_Reg_File_L[0]
        Cur_Reg_Path=Cur_Reg_File_L[1]
        if((Cur_ObsID!=Cur_Fov1_ObsID) or (Cur_ObsID!=Cur_Reg_ObsID) or (Cur_Fov1_ObsID!=Cur_Reg_ObsID)):
            raise "Mismatched File!!!"
        Cur_Background_Ratio_Tuple=Background_Finder_10.Background_Finder_V2(Gname,Cur_Evt2_Path,Cur_Reg_Path,Cur_Fov1_Path)
        #print("Cur_Background_Ratio_Tuple: ", Cur_Background_Ratio_Tuple)
        Cur_Background_L=[Cur_ObsID, Cur_Background_Ratio_Tuple]
        Background_HL.append(Cur_Background_L)
    return Background_HL
"""

def Background_Calc(ObsID):
    Gname=Galaxy_Name_From_ObsID_Query.Gname_Query(ObsID)
    print("Gname: ", Gname)
    Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
    Evt2_Path=File_Query_Code_5.ObsID_File_Query(ObsID,ObsID_Path='/opt/xray/anthony/expansion_backup/ObsIDs/',key="evt2")
    FOV1_Path=File_Query_Code_5.ObsID_File_Query(ObsID,ObsID_Path='/opt/xray/anthony/expansion_backup/ObsIDs/',key="fov1")
    Reg_Path=File_Query_Code_5.ObsID_File_Query(ObsID,ObsID_Path='/opt/xray/anthony/expansion_backup/ObsIDs/',key="reg")
    Background_Ratio_Tuple=Background_Finder_10.Background_Finder_V2(Gname,Evt2_Path,Reg_Path,FOV1_Path)
    #print("Background_Ratio_Tuple: ", Background_Ratio_Tuple)
    #Background_L=[ObsID, Background_Ratio_Tuple]
    #Background_L=[Background_Ratio_Tuple]
    return Background_Ratio_Tuple

'''
def Limiting_Flux_Intersected_Region_Calc_Galaxy_Name_Input(Gname, Data_Input=dir+'/../Marx_Source_Injection/Source_Detection_Analysis/Marx_Source_Detection_Data.csv', Count_Limits_Path=dir+'/../Marx_Source_Injection/Source_Detection_Analysis/Count_Limits.csv', Max_Counts=100):
    Background_HL=Background_Calc(Gname)
    print("Background_HL: ", Background_HL)
    #Counts_L=list(range(0,201,10))
    #Count_Limits_Path=
    ##Counts_L=list(range(0,101,10))
    #Cur_Theta_Intersection_HL_Tuple_HL_HL=[]
    for Background_L in Background_HL:
        #Counts_L=list(range(0,101,10))
        Cur_ObsID=Background_L[0]
        Cur_Evt2_Path=File_Query_Code_5.ObsID_File_Query(Cur_ObsID,ObsID_Path='/opt/xray/anthony/expansion_backup/ObsIDs/',key="evt2")
        Cur_FOV1_Path=File_Query_Code_5.ObsID_File_Query(Cur_ObsID,ObsID_Path='/opt/xray/anthony/expansion_backup/ObsIDs/',key="fov1")
        Cur_Background_Tuple=Background_L[1]
        Cur_Background_Front_Illuminated=Cur_Background_Tuple[0]
        Cur_Background_Back_Illuminated=Cur_Background_Tuple[1]

        Pointing_X,Pointing_Y=Area_Calc_Frac_B_2_Alt_8.Aimpoint_Physical_Coords_Calc(Cur_Evt2_Path)

        G_Data = Ned.query_object(Gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The queryed data of the galaxy from NED in the form of a astropy table
        raGC,decGC=Background_Finder_10.GC_Query(Gname) #raGC:-float, Right Ascension of Galactic Center, The right ascension of the Galactic center of the current galaxy in degrees. #decGC:-float, Declination of Galactic Center, The declination of the Galactic center of the current galaxy in degrees.
        D25_S_Maj_Deg=D25_Finder.D25_Finder(Gname)
        D25_S_Maj=D25_S_Maj_Deg*3600.0 #D25_S_Maj:-float, D25_Semi_Major_Axis, The D25 Semi Major Axis of the current galaxy in arcseconds
        dmcoords(infile=str(Cur_Evt2_Path),ra=str(raGC), dec=str(decGC), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the GC to SKY coodinates in pixels (?)
        X_Phys=dmcoords.x #X_Phys:-float, X_Physical, The sky plane X pixel coordinate in units of pixels of the Galactic center
        Y_Phys=dmcoords.y #Y_Phys:-float, Y_Physical, The sky plane Y pixel coordinate in units of pixels of the Galactic center
        Chip_ID=dmcoords.chip_id #Chip_ID:-int, Chip_ID, The Chip ID number the GC is on
        R_Phys=D25_S_Maj*2.03252032520325 #R_Phys:-numpy.float64, Radius_Physical, The radius of the galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
        D25_Shape_String='circle(' + str(X_Phys) +','+ str(Y_Phys)+','+ str(R_Phys)+')'
        Galaxy_Region=CXCRegion(D25_Shape_String)
        #Galaxy_Region=Galaxy_Region.edit(stretch=10.0) #For Testing
        #print("Galaxy_Region: ", Galaxy_Region)
        FOV_Path_Front_Illuminated_Chips=Cur_FOV1_Path+'[ccd_id=0,1,2,3,4,6,8,9]'
        FOV_Path_Back_Illuminated_Chips=Cur_FOV1_Path+'[ccd_id=5,7]'
        CCD_Regions_Front_Illuminated=CXCRegion(FOV_Path_Front_Illuminated_Chips)
        CCD_Regions_Back_Illuminated=CXCRegion(FOV_Path_Back_Illuminated_Chips)

        Counts_L=list(range(0,Max_Counts+1,10))
        Cur_Theta_Intersection_HL_Tuple_HL=[]
        """ #Quoted Out for Testing. Should be enabled in Final Code!
        for i in range(0,len(Counts_L)-1):
            Limiting_Counts_Low=Counts_L[i]
            Limiting_Counts_High=Counts_L[i+1]
            Theta_Intersection_HL_Front_Illuminated=Source_Detection_Analysis.Limiting_Counts_Annuli_Calc(Limiting_Counts_Low, Limiting_Counts_High, Cur_Background_Front_Illuminated, Data_Input=Data_Input)
            #print("Theta_Intersection_HL_Front_Illuminated: ", Theta_Intersection_HL_Front_Illuminated)
            Theta_Intersection_HL_Back_Illuminated=Source_Detection_Analysis.Limiting_Counts_Annuli_Calc(Limiting_Counts_Low, Limiting_Counts_High, Cur_Background_Back_Illuminated, Data_Input=Data_Input)
            #print("Theta_Intersection_HL_Back_Illuminated: ", Theta_Intersection_HL_Back_Illuminated)
            Cur_Theta_Intersection_HL_Tuple=(Theta_Intersection_HL_Front_Illuminated,Theta_Intersection_HL_Back_Illuminated)
            #print("Cur_Theta_Intersection_HL_Tuple: ", Cur_Theta_Intersection_HL_Tuple)
            Cur_Theta_Intersection_HL_Tuple_HL.append(Cur_Theta_Intersection_HL_Tuple)
        """
        Cur_Theta_Intersection_HL_Tuple_HL=[([[0, 0.737868691680198], [1.4153788224598618, 3.274431247553509]], []), ([[0.737868691680198, 1.4153788224598618], [3.274431247553509, 7.158274470697053]], [[0, 4.788287940088315]]), ([[7.158274470697053, 8]], [[4.788287940088315, 7]])] #This is for Testing!!!
        print("Cur_Theta_Intersection_HL_Tuple_HL: ", Cur_Theta_Intersection_HL_Tuple_HL)
        #print("Cur_Theta_Intersection_HL_Tuple_HL[0]: ", Cur_Theta_Intersection_HL_Tuple_HL[1])
        #for Cur_Theta_Intersection_HL_Tuple in Cur_Theta_Intersection_HL_Tuple_HL:
        Annulus_Region_Front_Illuminated_L=[]
        Annulus_Region_Back_Illuminated_L=[]
        for Flux_Bin_Index in range(0, len(Cur_Theta_Intersection_HL_Tuple_HL)):
            print("Flux_Bin_Index: ", Flux_Bin_Index)
            Cur_Theta_Intersection_HL_Tuple=Cur_Theta_Intersection_HL_Tuple_HL[Flux_Bin_Index]
            Cur_Theta_Intersection_HL_Front_Illuminated=Cur_Theta_Intersection_HL_Tuple[0]
            Cur_Theta_Intersection_HL_Back_Illuminated=Cur_Theta_Intersection_HL_Tuple[1]
            print("Cur_Theta_Intersection_HL_Front_Illuminated: ", Cur_Theta_Intersection_HL_Front_Illuminated)
            print("Cur_Theta_Intersection_HL_Back_Illuminated: ", Cur_Theta_Intersection_HL_Back_Illuminated)
            #for Cur_Annulus in Cur_Theta_Intersection_HL_Front_Illuminated:
            #Annulus_Region_Front_Illuminated_L=[]
            if(len(Cur_Theta_Intersection_HL_Front_Illuminated)>0):
                for i in range(0,len(Cur_Theta_Intersection_HL_Front_Illuminated)):
                    Cur_Annulus_Front_Illuminated=Cur_Theta_Intersection_HL_Front_Illuminated[i]

                    Inner_Radius_Front_Illuminated=Cur_Annulus_Front_Illuminated[0]
                    Inner_Radius_Physical_Front_Illuminated=Inner_Radius_Front_Illuminated*2.03252032520325 #The converstion factor is 2.03252032520325pix/arcsec
                    Outer_Radius_Front_Illuminated=Cur_Annulus_Front_Illuminated[1]
                    Outer_Radius_Physical_Front_Illuminated=Outer_Radius_Front_Illuminated*2.03252032520325 #The converstion factor is 2.03252032520325pix/arcsec


                    #myreg = annulus(x,y,inner,outer)
                    Cur_Annulus_Region_Front_Illuminated = annulus(Pointing_X,Pointing_Y,Inner_Radius_Physical_Front_Illuminated,Outer_Radius_Physical_Front_Illuminated)

                    #print("Cur_Annulus_Region_Front_Illuminated: ", Cur_Annulus_Region_Front_Illuminated)
                    #print("Cur_Annulus_Region_Back_Illuminated: ", Cur_Annulus_Region_Back_Illuminated)
                    #Cur_Annulus_Region = circle(Pointing_X,Pointing_Y,Inner_Radius_Physical) #For Testing

                    if(i==0):
                        Annulus_Region_Front_Illuminated=Cur_Annulus_Region_Front_Illuminated

                    else:
                        #Annulus_Region=Annulus_Region|Cur_Annulus_Region
                        Annulus_Region_Front_Illuminated=Annulus_Region_Front_Illuminated+Cur_Annulus_Region_Front_Illuminated
                Annulus_Region_Front_Illuminated_L.append(Annulus_Region_Front_Illuminated)

            if(len(Cur_Theta_Intersection_HL_Back_Illuminated)>0):
                for i in range(0,len(Cur_Theta_Intersection_HL_Back_Illuminated)):
                    Cur_Annulus_Back_Illuminated=Cur_Theta_Intersection_HL_Back_Illuminated[i]

                    Inner_Radius_Back_Illuminated=Cur_Annulus_Back_Illuminated[0]
                    Inner_Radius_Physical_Back_Illuminated=Inner_Radius_Back_Illuminated*2.03252032520325 #The converstion factor is 2.03252032520325pix/arcsec
                    Outer_Radius_Back_Illuminated=Cur_Annulus_Back_Illuminated[1]
                    Outer_Radius_Physical_Back_Illuminated=Outer_Radius_Back_Illuminated*2.03252032520325 #The converstion factor is 2.03252032520325pix/arcsec

                    #myreg = annulus(x,y,inner,outer)
                    Cur_Annulus_Region_Back_Illuminated = annulus(Pointing_X,Pointing_Y,Inner_Radius_Physical_Back_Illuminated,Outer_Radius_Physical_Back_Illuminated)

                    #print("Cur_Annulus_Region_Front_Illuminated: ", Cur_Annulus_Region_Front_Illuminated)
                    #print("Cur_Annulus_Region_Back_Illuminated: ", Cur_Annulus_Region_Back_Illuminated)
                    #Cur_Annulus_Region = circle(Pointing_X,Pointing_Y,Inner_Radius_Physical) #For Testing

                    if(i==0):
                        Annulus_Region_Back_Illuminated=Cur_Annulus_Region_Back_Illuminated
                    else:
                        #Annulus_Region=Annulus_Region|Cur_Annulus_Region
                        Annulus_Region_Back_Illuminated=Annulus_Region_Back_Illuminated+Cur_Annulus_Region_Back_Illuminated

                Annulus_Region_Back_Illuminated_L.append(Annulus_Region_Back_Illuminated)
    print("Annulus_Region_Front_Illuminated_L: ", Annulus_Region_Front_Illuminated_L)
    print("Annulus_Region_Back_Illuminated_L: ", Annulus_Region_Back_Illuminated_L)
'''
"""
def func(x, a, b):
    y = a*x + b
    return y

def Weighted_Mean(X,Y,Func=func):
    alpha = optimize.curve_fit(func, xdata = x, ydata = y)[0]
    print(alpha)
"""

def Gamma_Calc(ObsID, Data_Input="../SQL_Standard_File/Source_Flux_All_Modified_6.csv", Key="Beta_0.3-8.0"):
    #Theta_Intersection_HL_Front_Illuminated=Source_Detection_Analysis.Limiting_Counts_Annuli_Calc(Limiting_Counts_Low, Limiting_Counts_High,Background_Front_Illuminated, Data_Input=Data_Input)
    Data=pd.read_csv(Data_Input)
    Data_ObsID=Data[Data["ObsID"]==ObsID]
    #print("Data: \n", Data)
    #print("Data_ObsID: \n", Data_ObsID)
    Beta_A=Data_ObsID[Key]
    Beta_A=Beta_A[Beta_A>0]
    pd.set_option('display.max_rows', None)
    print("Beta_A: ", Beta_A)
    Beta_Avg=Beta_A.mean()
    #print("Beta_Avg: ", Beta_Avg)
    Exposure_A=Data_ObsID["EXPOSURE"]
    #print("Exposure_A: ", Exposure_A)
    Exposure=Exposure_A.mean()
    Gamma=float(Exposure)/Beta_Avg
    return Gamma

def Flux_to_Counts_Convert(Flux, ObsID, Data_Input="../SQL_Standard_File/Source_Flux_All_Modified_6.csv", Key="Beta_0.3-8.0", Gamma=None):
    #Theta_Intersection_HL_Front_Illuminated=Source_Detection_Analysis.Limiting_Counts_Annuli_Calc(Limiting_Counts_Low, Limiting_Counts_High,Background_Front_Illuminated, Data_Input=Data_Input)
    """
    Data=pd.read_csv(Data_Input)
    Data_ObsID=Data[Data["ObsID"]==ObsID]
    #print("Data: \n", Data)
    #print("Data_ObsID: \n", Data_ObsID)
    Beta_A=Data_ObsID[Key]
    Beta_Avg=Beta_A.mean()
    #print("Beta_Avg: ", Beta_Avg)
    Exposure_A=Data_ObsID["EXPOSURE"]
    #print("Exposure_A: ", Exposure_A)
    Exposure=Exposure_A.mean()
    Counts=(float(Flux)*float(Exposure))/Beta_Avg
    """
    if(Gamma==None):
        Gamma=Gamma_Calc(ObsID=ObsID, Data_Input=Data_Input, Key=Key)
    Counts=float(Flux)*Gamma
    return Counts

def Flux_Array_Calc(Factor_Low=1, Factor_High=10, Factor_Step=5, Mag_Low=-17, Mag_High=-12, Include_Zero_Bool=False, Custom_Array=None, Append_End=None):
    #a2 = np.arange(1,10,1)
    if(Custom_Array!=None):
        a2=np.array(Custom_Array)
    else:
        a2 = np.arange(Factor_Low,Factor_High,Factor_Step)
    #a1 = 10.**(np.arange(-4,0))
    a1 = 10.**(np.arange(Mag_Low,Mag_High))
    #print("a1: ", a1)
    X=np.outer(a1, a2).flatten()
    #X=np.round(X,4)
    if(Include_Zero_Bool):
        X=np.insert(X, 0, 0.0)
    if(Append_End!=None):
        End_Index=len(list(X))
        X=np.insert(X, End_Index, Append_End)
    #X=np.format_float_positional(X, precision=3)
    return X

def Theta_Intersection_Calc(ObsID, Max_Counts=100, Counts_Step=10, Data_Input=dir+'/../Marx_Source_Injection/Source_Detection_Analysis/Marx_Source_Detection_Data.csv', Flux_Bool=False):
    Background_Tuple=Background_Calc(ObsID)
    Background_Front_Illuminated=Background_Tuple[0]
    Background_Back_Illuminated=Background_Tuple[1]
    Counts_L=list(range(0,Max_Counts+1,Counts_Step))
    if(Flux_Bool):
        Flux_L=Flux_Array_Calc()
        print("Flux_L: ", Flux_L)
        Gamma=Gamma_Calc(ObsID)
        print("Gamma: ", Gamma)
        Counts_L=[]
        for Flux in Flux_L:
            Counts=Flux_to_Counts_Convert(Flux,ObsID,Gamma=Gamma)
            Counts_L.append(Counts)
    print("Counts_L: ", Counts_L)
    Theta_Intersection_HL_Tuple_HL=[]
    for i in range(0,len(Counts_L)-1):
        Limiting_Counts_Low=Counts_L[i]
        Limiting_Counts_High=Counts_L[i+1]
        if((Limiting_Counts_High<3) or (Limiting_Counts_Low>30)):
            Theta_Intersection_HL_Tuple_HL.append(([],[]))
            continue
        Theta_Intersection_HL_Front_Illuminated=Source_Detection_Analysis.Limiting_Counts_Annuli_Calc(Limiting_Counts_Low, Limiting_Counts_High, Background_Front_Illuminated, Data_Input=Data_Input)
        #print("Theta_Intersection_HL_Front_Illuminated: ", Theta_Intersection_HL_Front_Illuminated)
        Theta_Intersection_HL_Back_Illuminated=Source_Detection_Analysis.Limiting_Counts_Annuli_Calc(Limiting_Counts_Low, Limiting_Counts_High, Background_Back_Illuminated, Data_Input=Data_Input)
        #print("Theta_Intersection_HL_Back_Illuminated: ", Theta_Intersection_HL_Back_Illuminated)
        Cur_Theta_Intersection_HL_Tuple=(Theta_Intersection_HL_Front_Illuminated,Theta_Intersection_HL_Back_Illuminated)
        #print("Cur_Theta_Intersection_HL_Tuple: ", Cur_Theta_Intersection_HL_Tuple)
        Theta_Intersection_HL_Tuple_HL.append(Cur_Theta_Intersection_HL_Tuple)
    return Theta_Intersection_HL_Tuple_HL

def Limiting_Flux_Intersected_Region_Calc(ObsID, Data_Input=dir+'/../Marx_Source_Injection/Source_Detection_Analysis/Marx_Source_Detection_Data.csv', Count_Limits_Path=dir+'/../Marx_Source_Injection/Source_Detection_Analysis/Count_Limits.csv', Max_Counts=100, Counts_Step=10, Galactic_Radius_Max=2.0, Galactic_Radius_Step=0.25, Flux_Bool=False):
    Gname=Galaxy_Name_From_ObsID_Query.Gname_Query(ObsID)
    Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
    Background_Tuple=Background_Calc(ObsID)
    Evt2_Path=File_Query_Code_5.ObsID_File_Query(ObsID,ObsID_Path='/opt/xray/anthony/expansion_backup/ObsIDs/',key="evt2")
    FOV1_Path=File_Query_Code_5.ObsID_File_Query(ObsID,ObsID_Path='/opt/xray/anthony/expansion_backup/ObsIDs/',key="fov1")
    Background_Front_Illuminated=Background_Tuple[0]
    Background_Back_Illuminated=Background_Tuple[1]

    Pointing_X,Pointing_Y=Area_Calc_Frac_B_2_Alt_8.Aimpoint_Physical_Coords_Calc(Evt2_Path)

    """
    G_Data = Ned.query_object(Gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The queryed data of the galaxy from NED in the form of a astropy table
    raGC,decGC=Background_Finder_10.GC_Query(Gname) #raGC:-float, Right Ascension of Galactic Center, The right ascension of the Galactic center of the current galaxy in degrees. #decGC:-float, Declination of Galactic Center, The declination of the Galactic center of the current galaxy in degrees.
    D25_S_Maj_Deg=D25_Finder.D25_Finder(Gname)
    D25_S_Maj=D25_S_Maj_Deg*3600.0 #D25_S_Maj:-float, D25_Semi_Major_Axis, The D25 Semi Major Axis of the current galaxy in arcseconds
    dmcoords(infile=str(Evt2_Path),ra=str(raGC), dec=str(decGC), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the GC to SKY coodinates in pixels (?)
    X_Phys=dmcoords.x #X_Phys:-float, X_Physical, The sky plane X pixel coordinate in units of pixels of the Galactic center
    Y_Phys=dmcoords.y #Y_Phys:-float, Y_Physical, The sky plane Y pixel coordinate in units of pixels of the Galactic center
    Chip_ID=dmcoords.chip_id #Chip_ID:-int, Chip_ID, The Chip ID number the GC is on
    R_Phys=D25_S_Maj*2.03252032520325 #R_Phys:-numpy.float64, Radius_Physical, The radius of the galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
    D25_Shape_String='circle(' + str(X_Phys) +','+ str(Y_Phys)+','+ str(R_Phys)+')'
    Galaxy_Region=CXCRegion(D25_Shape_String)
    """
    Circular_D25_Bool=False
    #G_Data = Ned.query_object(Gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The queryed data of the galaxy from NED in the form of a astropy table
    raGC,decGC=Background_Finder_10.GC_Query(Gname) #raGC:-float, Right Ascension of Galactic Center, The right ascension of the Galactic center of the current galaxy in degrees. #decGC:-float, Declination of Galactic Center, The declination of the Galactic center of the current galaxy in degrees.
    #D25_S_Maj_Deg=D25_Finder.D25_Finder(Gname)
    D25_Tuple=D25_Finder.D25_Full_Query(Gname)
    if(isinstance(D25_Tuple[1],np.ma.core.MaskedConstant) or isinstance(D25_Tuple[2],np.ma.core.MaskedConstant)): #In the event that the ellipse is assumed to be a cirlce by RC3
        print(str(ObsID)+" has a circular D25 region")
        Circular_D25_Bool=True
    D25_S_Maj_Arcmin=D25_Tuple[0]
    D25_S_Min_Arcmin=D25_Tuple[1]
    D25_S_Angle=D25_Tuple[2]
    D25_S_Angle_Adjusted=D25_S_Angle+90
    #D25_S_Maj=D25_S_Maj_Deg*3600.0 #D25_S_Maj:-float, D25_Semi_Major_Axis, The D25 Semi Major Axis of the current galaxy in arcseconds
    D25_S_Maj=D25_S_Maj_Arcmin*60.0 #D25_S_Maj:-float, D25_Semi_Major_Axis, The D25 Semi Major Axis of the current galaxy in arcseconds
    D25_S_Min=D25_S_Min_Arcmin*60.0 #D25_S_Maj:-float, D25_Semi_Minor_Axis, The D25 Semi Minor Axis of the current galaxy in arcseconds
    dmcoords(infile=str(Evt2_Path),ra=str(raGC), dec=str(decGC), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the GC to SKY coodinates in pixels (?)
    X_Phys=dmcoords.x #X_Phys:-float, X_Physical, The sky plane X pixel coordinate in units of pixels of the Galactic center
    Y_Phys=dmcoords.y #Y_Phys:-float, Y_Physical, The sky plane Y pixel coordinate in units of pixels of the Galactic center
    Chip_ID=dmcoords.chip_id #Chip_ID:-int, Chip_ID, The Chip ID number the GC is on
    #R_Phys=D25_S_Maj*2.03252032520325 #R_Phys:-numpy.float64, Radius_Physical, The radius of the galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
    D25_S_Maj_Phys=D25_S_Maj*2.03252032520325 #D25_S_Maj_Phys:-numpy.float64, D25_Semi_Major_Axis_Physical, D25 Semi Major Axis of the current galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
    D25_S_Min_Phys=D25_S_Min*2.03252032520325 #D25_S_Min_Phys:-numpy.float64, D25_Semi_Minor_Axis_Physical, D25 Semi Minor Axis of the current galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
    #D25_Shape_String='circle(' + str(X_Phys) +','+ str(Y_Phys)+','+ str(R_Phys)+')'
    #Galaxy_Region=CXCRegion(D25_Shape_String)
    if(Circular_D25_Bool==False):
        Galaxy_Region=ellipse(X_Phys,Y_Phys,D25_S_Maj_Phys,D25_S_Min_Phys,D25_S_Angle_Adjusted) #Need to add circular case!
    else:
        Galaxy_Region=circle(X_Phys,Y_Phys,D25_S_Maj_Phys)
    #Galaxy_Region=Galaxy_Region.edit(stretch=10.0) #For Testing
    print("Galaxy_Region: ", Galaxy_Region)
    FOV_Path_Front_Illuminated_Chips=FOV1_Path+'[ccd_id=0,1,2,3,4,6,8,9]'
    #FOV_Path_Front_Illuminated_Chips=FOV1_Path #For Testing
    FOV_Path_Back_Illuminated_Chips=FOV1_Path+'[ccd_id=5,7]'
    #FOV_Path_Front_Illuminated_Chips=FOV_Path_Back_Illuminated_Chips #For Testing
    CCD_Regions_Front_Illuminated=CXCRegion(FOV_Path_Front_Illuminated_Chips)
    CCD_Regions_Back_Illuminated=CXCRegion(FOV_Path_Back_Illuminated_Chips)

    Counts_L=list(range(0,Max_Counts+1,Counts_Step))
    Theta_Intersection_HL_Tuple_HL=[]
    """ #Quoted Out for Testing. Should be enabled in Final Code!
    for i in range(0,len(Counts_L)-1):
        Limiting_Counts_Low=Counts_L[i]
        Limiting_Counts_High=Counts_L[i+1]
        Theta_Intersection_HL_Front_Illuminated=Source_Detection_Analysis.Limiting_Counts_Annuli_Calc(Limiting_Counts_Low, Limiting_Counts_High,Background_Front_Illuminated, Data_Input=Data_Input)
        #print("Theta_Intersection_HL_Front_Illuminated: ", Theta_Intersection_HL_Front_Illuminated)
        Theta_Intersection_HL_Back_Illuminated=Source_Detection_Analysis.Limiting_Counts_Annuli_Calc(Limiting_Counts_Low, Limiting_Counts_High, Background_Back_Illuminated, Data_Input=Data_Input)
        #print("Theta_Intersection_HL_Back_Illuminated: ", Theta_Intersection_HL_Back_Illuminated)
        Cur_Theta_Intersection_HL_Tuple=(Theta_Intersection_HL_Front_Illuminated,Theta_Intersection_HL_Back_Illuminated)
        #print("Cur_Theta_Intersection_HL_Tuple: ", Cur_Theta_Intersection_HL_Tuple)
        Theta_Intersection_HL_Tuple_HL.append(Cur_Theta_Intersection_HL_Tuple)
    """
    Theta_Intersection_HL_Tuple_HL=Theta_Intersection_Calc(ObsID, Max_Counts=Max_Counts, Counts_Step=Counts_Step, Data_Input=Data_Input, Flux_Bool=Flux_Bool)
    print("Theta_Intersection_HL_Tuple_HL: ", Theta_Intersection_HL_Tuple_HL)

    #Theta_Intersection_HL_Tuple_HL=[([[0, 0.737868691680198], [1.4153788224598618, 3.274431247553509]], []), ([[0.737868691680198, 1.4153788224598618], [3.274431247553509, 7.158274470697053]], [[0, 4.788287940088315]]), ([[7.158274470697053, 8]], [[4.788287940088315, 7]])] #This is for Testing!!!
    #Theta_Intersection_HL_Tuple_HL:  [([[0, 0.7507228926455718], [1.3990741619884763, 3.2611711019159664]], []), ([[0.7507228926455718, 1.3990741619884763], [3.2611711019159664, 7.137313541613234]], [[0, 4.7966724803737115]]), ([[7.137313541613234, 8]], [[4.7966724803737115, 7]]), ([], []), ([], []), ([], []), ([], []), ([], []), ([], []), ([], [])] #This is for Testing!!!
    #Theta_Intersection_HL_Tuple_HL=[([[0, 2.299848281922187]], []), ([[2.299848281922187, 6.309420622311873]], [[0, 3.3233922414396715]]), ([[6.309420622311873, 8]], [[3.3233922414396715, 5.101172444098994]]), ([], [[5.101172444098994, 6]]), ([], []), ([], []), ([], []), ([], []), ([], []), ([], [])]
    #print("Theta_Intersection_HL_Tuple_HL: ", Theta_Intersection_HL_Tuple_HL)
    #print("len(Theta_Intersection_HL_Tuple_HL): ", len(Theta_Intersection_HL_Tuple_HL))
    #print("Theta_Intersection_HL_Tuple_HL[0]: ", Theta_Intersection_HL_Tuple_HL[1])
    #for Theta_Intersection_HL_Tuple in Theta_Intersection_HL_Tuple_HL:
    Annulus_Region_Front_Illuminated_L=[]
    Annulus_Region_Back_Illuminated_L=[]
    for Flux_Bin_Index in range(0, len(Theta_Intersection_HL_Tuple_HL)):
        #print("Flux_Bin_Index: ", Flux_Bin_Index)
        Cur_Theta_Intersection_HL_Tuple=Theta_Intersection_HL_Tuple_HL[Flux_Bin_Index]
        Cur_Theta_Intersection_HL_Front_Illuminated=Cur_Theta_Intersection_HL_Tuple[0]
        Cur_Theta_Intersection_HL_Back_Illuminated=Cur_Theta_Intersection_HL_Tuple[1]
        #print("Cur_Theta_Intersection_HL_Front_Illuminated: ", Cur_Theta_Intersection_HL_Front_Illuminated)
        #print("Cur_Theta_Intersection_HL_Back_Illuminated: ", Cur_Theta_Intersection_HL_Back_Illuminated)
        #for Cur_Annulus in Cur_Theta_Intersection_HL_Front_Illuminated:
        #Annulus_Region_Front_Illuminated_L=[]
        #print("Cur_Theta_Intersection_HL_Front_Illuminated: ", Cur_Theta_Intersection_HL_Front_Illuminated)
        if(len(Cur_Theta_Intersection_HL_Front_Illuminated)>0):
            for i in range(0,len(Cur_Theta_Intersection_HL_Front_Illuminated)):
                Cur_Annulus_Front_Illuminated=Cur_Theta_Intersection_HL_Front_Illuminated[i]
                Inner_Radius_Front_Illuminated=Cur_Annulus_Front_Illuminated[0]
                Inner_Radius_Physical_Front_Illuminated=Inner_Radius_Front_Illuminated*2.03252032520325*60 #The converstion factor is 2.03252032520325pix/arcsec
                Outer_Radius_Front_Illuminated=Cur_Annulus_Front_Illuminated[1]
                Outer_Radius_Physical_Front_Illuminated=Outer_Radius_Front_Illuminated*2.03252032520325*60 #The converstion factor is 2.03252032520325pix/arcsec
                #myreg = annulus(x,y,inner,outer)
                Cur_Annulus_Region_Front_Illuminated = annulus(Pointing_X,Pointing_Y,Inner_Radius_Physical_Front_Illuminated,Outer_Radius_Physical_Front_Illuminated)
                if(i==0):
                    Annulus_Region_Front_Illuminated=Cur_Annulus_Region_Front_Illuminated
                else:
                    Annulus_Region_Front_Illuminated=Annulus_Region_Front_Illuminated+Cur_Annulus_Region_Front_Illuminated
            Annulus_Region_Front_Illuminated_L.append(Annulus_Region_Front_Illuminated)
        else:
            Annulus_Region_Front_Illuminated_L.append(CXCRegion())
        if(len(Cur_Theta_Intersection_HL_Back_Illuminated)>0):
            for i in range(0,len(Cur_Theta_Intersection_HL_Back_Illuminated)):
                Cur_Annulus_Back_Illuminated=Cur_Theta_Intersection_HL_Back_Illuminated[i]
                Inner_Radius_Back_Illuminated=Cur_Annulus_Back_Illuminated[0]
                Inner_Radius_Physical_Back_Illuminated=Inner_Radius_Back_Illuminated*2.03252032520325*60 #The converstion factor is 2.03252032520325pix/arcsec
                Outer_Radius_Back_Illuminated=Cur_Annulus_Back_Illuminated[1]
                Outer_Radius_Physical_Back_Illuminated=Outer_Radius_Back_Illuminated*2.03252032520325*60 #The converstion factor is 2.03252032520325pix/arcsec
                #myreg = annulus(x,y,inner,outer)
                Cur_Annulus_Region_Back_Illuminated = annulus(Pointing_X,Pointing_Y,Inner_Radius_Physical_Back_Illuminated,Outer_Radius_Physical_Back_Illuminated)
                if(i==0):
                    Annulus_Region_Back_Illuminated=Cur_Annulus_Region_Back_Illuminated
                else:
                    Annulus_Region_Back_Illuminated=Annulus_Region_Back_Illuminated+Cur_Annulus_Region_Back_Illuminated
            Annulus_Region_Back_Illuminated_L.append(Annulus_Region_Back_Illuminated)
        else:
            Annulus_Region_Back_Illuminated_L.append(CXCRegion())
    #print("Annulus_Region_Front_Illuminated_L: ", Annulus_Region_Front_Illuminated_L)
    #print("Annulus_Region_Back_Illuminated_L: ", Annulus_Region_Back_Illuminated_L)
    """
    Intersecting Front_Illuminated CCD Regions with Front_Illuminated Limiting Flux Annulus Regions
    """
    #print("len(Annulus_Region_Front_Illuminated_L): ", len(Annulus_Region_Front_Illuminated_L))
    Annulus_Region_Front_Illuminated_FOV_Intersected_L=[]
    for Annulus_Region_Front_Illuminated in Annulus_Region_Front_Illuminated_L:
        #print("Current Annulus_Region_Front_Illuminated: ", Annulus_Region_Front_Illuminated)
        #print("CCD_Regions_Front_Illuminated: ", CCD_Regions_Front_Illuminated)
        Annulus_Region_Front_Illuminated_FOV_Intersected=CCD_Regions_Front_Illuminated*Annulus_Region_Front_Illuminated
        #Annulus_Region_Front_Illuminated_FOV_Intersected=Annulus_Region_Front_Illuminated*Annulus_Region_Front_Illuminated
        #print("Annulus_Region_Front_Illuminated_FOV_Intersected.shapes: ", Annulus_Region_Front_Illuminated_FOV_Intersected.shapes)
        Annulus_Region_Front_Illuminated_FOV_Intersected_L.append(Annulus_Region_Front_Illuminated_FOV_Intersected)
        #Annulus_Region_Front_Illuminated_FOV_Intersected_L.append(Annulus_Region_Front_Illuminated_FOV_Intersected.area())
    #print("Annulus_Region_Front_Illuminated_FOV_Intersected_L: ", Annulus_Region_Front_Illuminated_FOV_Intersected_L)
    """
    Intersecting Back_Illuminated CCD Regions with Back_Illuminated Limiting Flux Annulus Regions
    """
    Annulus_Region_Back_Illuminated_FOV_Intersected_L=[]
    for Annulus_Region_Back_Illuminated in Annulus_Region_Back_Illuminated_L:
        #print("Current Annulus_Region_Back_Illuminated: ", Annulus_Region_Back_Illuminated)
        #print("CCD_Regions_Back_Illuminated: ", CCD_Regions_Back_Illuminated)
        Annulus_Region_Back_Illuminated_FOV_Intersected=CCD_Regions_Back_Illuminated*Annulus_Region_Back_Illuminated
        #Annulus_Region_Back_Illuminated_FOV_Intersected=Annulus_Region_Back_Illuminated*Annulus_Region_Back_Illuminated
        #print("Annulus_Region_Back_Illuminated_FOV_Intersected.shapes: ", Annulus_Region_Back_Illuminated_FOV_Intersected.shapes)
        Annulus_Region_Back_Illuminated_FOV_Intersected_L.append(Annulus_Region_Back_Illuminated_FOV_Intersected)
        #Annulus_Region_Back_Illuminated_FOV_Intersected_L.append(Annulus_Region_Back_Illuminated_FOV_Intersected.area())
    #print("Annulus_Region_Back_Illuminated_FOV_Intersected_L: ", Annulus_Region_Back_Illuminated_FOV_Intersected_L)
    #Galaxy_Size_Scalers_L=list(np.arange(0, 2+Galactic_Radius_Step, Galactic_Radius_Step))
    Galaxy_Size_Scalers_L=list(np.arange(0, float(Galactic_Radius_Max)+Galactic_Radius_Step, Galactic_Radius_Step))
    #print("Galaxy_Size_Scalers_L: ", Galaxy_Size_Scalers_L)
    Galactic_Annulus_Region_L=[]
    for i in range(0,len(Galaxy_Size_Scalers_L)-1):
        Cur_Inner_Scaler=Galaxy_Size_Scalers_L[i]
        #print("Cur_Inner_Scaler: ", Cur_Inner_Scaler)
        Cur_Outer_Scaler=Galaxy_Size_Scalers_L[i+1]
        #print("Cur_Outer_Scaler: ", Cur_Outer_Scaler)
        if(Cur_Inner_Scaler!=1):
            Inner_Galactic_Radius_Region=Galaxy_Region.edit(stretch=Cur_Inner_Scaler)
        else:
            Inner_Galactic_Radius_Region=Galaxy_Region
        #print("Inner_Galactic_Radius_Region: ", Inner_Galactic_Radius_Region)
        if(Cur_Outer_Scaler!=1):
            Outer_Galactic_Radius_Region=Galaxy_Region.edit(stretch=Cur_Outer_Scaler)
        else:
            Outer_Galactic_Radius_Region=Galaxy_Region
        #print("Outer_Galactic_Radius_Region: ", Outer_Galactic_Radius_Region)
        if(i==0):
            Cur_Galactic_Annulus_Region=Outer_Galactic_Radius_Region
        else:
            Cur_Galactic_Annulus_Region=Outer_Galactic_Radius_Region-Inner_Galactic_Radius_Region
        #print("Cur_Galactic_Annulus_Region: ", Cur_Galactic_Annulus_Region)
        Galactic_Annulus_Region_L.append(Cur_Galactic_Annulus_Region)
    #print("Galactic_Annulus_Region_L: ", Galactic_Annulus_Region_L)


    Region_Galactic_Intersected_HL_Front_Illuminated=[]
    #print("len(Annulus_Region_Front_Illuminated_FOV_Intersected_L): ", len(Annulus_Region_Front_Illuminated_FOV_Intersected_L))
    for Annulus_Region_Front_Illuminated_FOV_Intersected in Annulus_Region_Front_Illuminated_FOV_Intersected_L:
        Region_Galactic_Intersected_L_Front_Illuminated=[]
        for Galactic_Annulus_Region in Galactic_Annulus_Region_L:
            Region_Galactic_Intersected_Front_Illuminated=Annulus_Region_Front_Illuminated_FOV_Intersected*Galactic_Annulus_Region
            #Region_Galactic_Intersected=Galactic_Annulus_Region_L*Annulus_Region_Front_Illuminated_FOV_Intersected
            #print("Region_Galactic_Intersected: ", Region_Galactic_Intersected)
            Region_Galactic_Intersected_L_Front_Illuminated.append(Region_Galactic_Intersected_Front_Illuminated)
            #print("Region_Galactic_Intersected_L: ", Region_Galactic_Intersected_L)
        Region_Galactic_Intersected_HL_Front_Illuminated.append(Region_Galactic_Intersected_L_Front_Illuminated)
    #print("Region_Galactic_Intersected_HL: ", Region_Galactic_Intersected_HL)
    #print("Region_Galactic_Intersected_HL[0]: ", Region_Galactic_Intersected_HL[0])
    #print("Region_Galactic_Intersected_HL[0][0]: ", Region_Galactic_Intersected_HL[0][0])
    """
    Intersected_Area_HL_Front_Illuminated=[]
    Count=0
    for Region_Galactic_Intersected_L_Front_Illuminated in Region_Galactic_Intersected_HL_Front_Illuminated:
        Intersected_Area_L_Front_Illuminated=[]
        for Region_Galactic_Intersected_Front_Illuminated in Region_Galactic_Intersected_L_Front_Illuminated:
            Count=Count+1
            #print("Count: ", Count)
            #print("Region_Galactic_Intersected: ", Region_Galactic_Intersected)
            #Cur_Region_Galactic_Intersected_Area=Region_Galactic_Intersected.area(pixel=True,bin=0.01)
            Cur_Region_Galactic_Intersected_Area_Front_Illuminated=Region_Galactic_Intersected_Front_Illuminated.area(pixel=True,bin=1)
            #Cur_Region_Galactic_Intersected_Area=Cur_Region_Galactic_Intersected_Area/(Galaxy_Region.area()) #For Testing!
            if(Cur_Region_Galactic_Intersected_Area_Front_Illuminated<1.0):
                Cur_Region_Galactic_Intersected_Area_Front_Illuminated=0.0
            Intersected_Area_L_Front_Illuminated.append(Cur_Region_Galactic_Intersected_Area_Front_Illuminated)
        Intersected_Area_HL_Front_Illuminated.append(Intersected_Area_L_Front_Illuminated)
    print("Intersected_Area_HL_Front_Illuminated: ", Intersected_Area_HL_Front_Illuminated)
    """
    Region_Galactic_Intersected_HL_Back_Illuminated=[]
    for Annulus_Region_Back_Illuminated_FOV_Intersected in Annulus_Region_Back_Illuminated_FOV_Intersected_L:
        Region_Galactic_Intersected_L_Back_Illuminated=[]
        for Galactic_Annulus_Region in Galactic_Annulus_Region_L:
            Region_Galactic_Intersected_Back_Illuminated=Annulus_Region_Back_Illuminated_FOV_Intersected*Galactic_Annulus_Region
            #Region_Galactic_Intersected=Galactic_Annulus_Region_L*Annulus_Region_Back_Illuminated_FOV_Intersected
            #print("Region_Galactic_Intersected: ", Region_Galactic_Intersected)
            Region_Galactic_Intersected_L_Back_Illuminated.append(Region_Galactic_Intersected_Back_Illuminated)
            #print("Region_Galactic_Intersected_L: ", Region_Galactic_Intersected_L)
        Region_Galactic_Intersected_HL_Back_Illuminated.append(Region_Galactic_Intersected_L_Back_Illuminated)
    #print("Region_Galactic_Intersected_HL: ", Region_Galactic_Intersected_HL)
    #print("Region_Galactic_Intersected_HL[0]: ", Region_Galactic_Intersected_HL[0])
    #print("Region_Galactic_Intersected_HL[0][0]: ", Region_Galactic_Intersected_HL[0][0])
    """
    Intersected_Area_HL_Back_Illuminated=[]
    Count=0
    for Region_Galactic_Intersected_L_Back_Illuminated in Region_Galactic_Intersected_HL_Back_Illuminated:
        Intersected_Area_L_Back_Illuminated=[]
        for Region_Galactic_Intersected_Back_Illuminated in Region_Galactic_Intersected_L_Back_Illuminated:
            Count=Count+1
            #print("Count: ", Count)
            #print("Region_Galactic_Intersected: ", Region_Galactic_Intersected)
            #Cur_Region_Galactic_Intersected_Area=Region_Galactic_Intersected.area(pixel=True,bin=0.01)
            Cur_Region_Galactic_Intersected_Area_Back_Illuminated=Region_Galactic_Intersected_Back_Illuminated.area(pixel=True,bin=1)
            #Cur_Region_Galactic_Intersected_Area=Cur_Region_Galactic_Intersected_Area/(Galaxy_Region.area()) #For Testing!
            if(Cur_Region_Galactic_Intersected_Area_Back_Illuminated<1.0):
                Cur_Region_Galactic_Intersected_Area_Back_Illuminated=0.0
            Intersected_Area_L_Back_Illuminated.append(Cur_Region_Galactic_Intersected_Area_Back_Illuminated)
        Intersected_Area_HL_Back_Illuminated.append(Intersected_Area_L_Back_Illuminated)
    print("Intersected_Area_HL_Back_Illuminated: ", Intersected_Area_HL_Back_Illuminated)
    """
    return Region_Galactic_Intersected_HL_Front_Illuminated, Region_Galactic_Intersected_HL_Back_Illuminated

def Region_Test():
    Ellipse_Region=ellipse(0,0,100,50,20)
    Circle_Region=circle(0,0,100)
    Circle_Region_2=circle(200,0,100)
    Circle_Region_3=circle(0,0,50)
    Annulus_Region=annulus(0,0,50,100)
    Box=box(0,0,1000,1000)
    Box_2=box(1000,0,1000,1000)
    Box_3=box(1000,0,1000,1000,45)

    #Ellipse_Region_Modified=Ellipse_Region.edit(stretch=0)
    #Circle_Region_Modified=Circle_Region.edit(stretch=0)
    #Ellipse_Region_Modified=Ellipse_Region.edit(pad=-100)
    #Circle_Region_Modified=Circle_Region.edit(pad=-100)
    #Ellipse_Region_Modified=Ellipse_Region.edit(pad=-100)
    Ellipse_Region_Modified=Ellipse_Region.edit(stretch=1)
    Circle_Region_Modified=Circle_Region.edit(stretch=1)
    #Circle_Intersection_Region=Circle_Region*Circle_Region_2
    #print("Ellipse_Region_Modified: ", Ellipse_Region_Modified)
    #print("Circle_Region_Modified: ", Circle_Region_Modified)
    Circle_Intersection_Region=Circle_Region*Circle_Region_2
    """
    print("Circle_Intersection_Region.area(): ", Circle_Intersection_Region.area())
    print("Circle_Intersection_Region.area(pixel=True): ", Circle_Intersection_Region.area(pixel=True))
    print("Circle_Intersection_Region.area(pixel=True,bin=0.1): ", Circle_Intersection_Region.area(pixel=True,bin=0.1))
    print("Circle_Intersection_Region.area(pixel=True,bin=0.01): ", Circle_Intersection_Region.area(pixel=True,bin=0.01))
    print("Circle_Intersection_Region.area(pixel=True,bin=0.01): ", Circle_Intersection_Region.area(pixel=True,bin=0.0001))

    print("Circle_Intersection_Region.area(pixel=False): ", Circle_Intersection_Region.area(pixel=False))
    """
    Diff_Circle_Region=Circle_Region-Circle_Region_3
    """
    print("Annulus_Region==Diff_Circle_Region: ", Annulus_Region==Diff_Circle_Region)
    print("Diff_Circle_Region.area(): ", Diff_Circle_Region.area())
    print("Annulus_Region.area(): ", Annulus_Region.area())
    """
    Diff_Region=Diff_Circle_Region*Box
    Non_Diff_Region=Annulus_Region*Box
    """
    print("Diff_Region: ", Diff_Region)
    print("Non_Diff_Region: ", Non_Diff_Region)
    print("Diff_Region.area(): ", Diff_Region.area())
    print("Non_Diff_Region.area(): ", Non_Diff_Region.area())
    """
    Box_Parallel=Box+Box_2
    Box_Parallel_Intersection=Box*Box_2
    print("Box_Parallel.area(): ", Box_Parallel.area())
    Box_Non_Parallel=Box+Box_3
    Box_Non_Parallel_Intersection=Box*Box_3
    #print("Box_Non_Parallel.area(): ", Box_Non_Parallel.area())
    Box_Parallel_Rotated=Box_Parallel.edit(rotate=45)
    print("Box_Parallel_Rotated.area(): ", Box_Parallel_Rotated.area())
    Box_Parallel_Rotated.write("Box_Parallel_Rotated_Test.reg", clobber=True)
    Region_L=[Ellipse_Region, Circle_Region]
    Region_L.edit(dx=354)
    print("Region_L: ", Region_L)


def Close_ObsIDs_Query(ObsID, Data_Path=dir+"/../SQL_Standard_File/Source_Flux_All_Modified_6.csv"):
    Data=pd.read_csv(Data_Path)
    #print("Data:\n", Data)
    Data_Unique_ObsIDs=Data.drop_duplicates(subset=['ObsID'])
    #print("Data_Unique_ObsIDs:\n", Data_Unique_ObsIDs)
    Data_ObsID=Data_Unique_ObsIDs[Data_Unique_ObsIDs["ObsID"]==ObsID]
    #print("Data_ObsID:\n", Data_ObsID)
    Close_ObsIDs_Str=Data_ObsID["Close_ObsIDs"].values[0]
    #print("Close_ObsIDs_Str: ", Close_ObsIDs_Str)
    #print("type(Close_ObsIDs_Str): ", type(Close_ObsIDs_Str))
    Close_ObsIDs_Str_L=Close_ObsIDs_Str.split(";")
    Close_ObsID_L=[]
    for Close_ObsIDs_Str_Seg in Close_ObsIDs_Str_L:
        if("[" in Close_ObsIDs_Str_Seg):
            Close_ObsIDs_Str_Seg=Close_ObsIDs_Str_Seg[1:]
        if("]" in Close_ObsIDs_Str_Seg):
            Close_ObsIDs_Str_Seg=Close_ObsIDs_Str_Seg[:len(Close_ObsIDs_Str_Seg)-1]
        #print("Close_ObsIDs_Str_Seg: ", Close_ObsIDs_Str_Seg)
        Cur_Close_ObsID=int(Close_ObsIDs_Str_Seg)
        Close_ObsID_L.append(Cur_Close_ObsID)
    #print("Close_ObsID_L: ", Close_ObsID_L)
    return Close_ObsID_L

def Aimpoint_Distance_Calc(ObsID_1, ObsID_2, Data_Path=dir+"/../SQL_Standard_File/Source_Flux_All_Modified_6.csv"):
    Data=pd.read_csv(Data_Path)
    #print("Data:\n", Data)
    Data_Unique_ObsIDs=Data.drop_duplicates(subset=['ObsID'])
    #print("Data_Unique_ObsIDs:\n", Data_Unique_ObsIDs)
    Data_ObsID_1=Data_Unique_ObsIDs[Data_Unique_ObsIDs["ObsID"]==ObsID_1]
    RA_Aimpoint_1=Data_ObsID_1["RA_Aimpoint"].values[0]
    DEC_Aimpoint_1=Data_ObsID_1["DEC_Aimpoint"].values[0]

    Data_ObsID_2=Data_Unique_ObsIDs[Data_Unique_ObsIDs["ObsID"]==ObsID_2]
    RA_Aimpoint_2=Data_ObsID_2["RA_Aimpoint"].values[0]
    DEC_Aimpoint_2=Data_ObsID_2["DEC_Aimpoint"].values[0]
    #print("Aimpont_2 ("+str(ObsID_2)+"): ", (RA_Aimpoint_2, DEC_Aimpoint_2))
    x1_Rad=Deg_to_Rad(RA_Aimpoint_1)
    x2_Rad=Deg_to_Rad(RA_Aimpoint_2)
    y1_Rad=Deg_to_Rad(DEC_Aimpoint_1)
    y2_Rad=Deg_to_Rad(DEC_Aimpoint_2)
    Have_Dist=Haversine_Distance(x1_Rad,x2_Rad,y1_Rad,y2_Rad)
    Have_Dist=np.abs(Have_Dist)
    Have_Dist_Deg=Rad_to_Deg(Have_Dist)
    Have_Dist_Arcmin=Have_Dist_Deg*60.0
    return Have_Dist_Arcmin

def Aimpoint_Offset_Calc(ObsID_1, ObsID_2, Data_Path=dir+"/../SQL_Standard_File/Source_Flux_All_Modified_6.csv"):
    Data=pd.read_csv(Data_Path)
    #print("Data:\n", Data)
    Data_Unique_ObsIDs=Data.drop_duplicates(subset=['ObsID'])
    #print("Data_Unique_ObsIDs:\n", Data_Unique_ObsIDs)
    Data_ObsID_1=Data_Unique_ObsIDs[Data_Unique_ObsIDs["ObsID"]==ObsID_1]
    RA_Aimpoint_1=Data_ObsID_1["RA_Aimpoint"].values[0]
    DEC_Aimpoint_1=Data_ObsID_1["DEC_Aimpoint"].values[0]

    Data_ObsID_2=Data_Unique_ObsIDs[Data_Unique_ObsIDs["ObsID"]==ObsID_2]
    RA_Aimpoint_2=Data_ObsID_2["RA_Aimpoint"].values[0]
    DEC_Aimpoint_2=Data_ObsID_2["DEC_Aimpoint"].values[0]
    #print("Aimpont_2 ("+str(ObsID_2)+"): ", (RA_Aimpoint_2, DEC_Aimpoint_2))
    Evt2_Path=File_Query_Code_5.ObsID_File_Query(ObsID_1,ObsID_Path='/opt/xray/anthony/expansion_backup/ObsIDs/',key="evt2")
    dmcoords(infile=str(Evt2_Path),ra=str(RA_Aimpoint_1), dec=str(DEC_Aimpoint_1), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the aimpont to SKY coodinates in pixels (?)
    X_Phys_1=dmcoords.x #X_Phys:-float, X_Physical, The sky plane X pixel coordinate in units of pixels of the aimpont
    Y_Phys_1=dmcoords.y #Y_Phys:-float, Y_Physical, The sky plane Y pixel coordinate in units of pixels of the aimpont
    dmcoords(infile=str(Evt2_Path),ra=str(RA_Aimpoint_2), dec=str(DEC_Aimpoint_2), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the GC to SKY coodinates in pixels (?)
    X_Phys_2=dmcoords.x #X_Phys:-float, X_Physical, The sky plane X pixel coordinate in units of pixels of the aimpont
    Y_Phys_2=dmcoords.y #Y_Phys:-float, Y_Physical, The sky plane Y pixel coordinate in units of pixels of the aimpont
    #print("X_Phys_1,Y_Phys_1: ", (X_Phys_1,Y_Phys_1))
    #print("X_Phys_2,Y_Phys_2: ", (X_Phys_2,Y_Phys_2))
    X_Offset=X_Phys_2-X_Phys_1
    Y_Offset=Y_Phys_2-Y_Phys_1
    return X_Offset, Y_Offset

def Overlapping_ObsIDs_Calc(ObsID, Data_Path=dir+"/../SQL_Standard_File/Source_Flux_All_Modified_6.csv"):
    Data=pd.read_csv(Data_Path)
    #print("Data:\n", Data)
    Data_Unique_ObsIDs=Data.drop_duplicates(subset=['ObsID'])
    #print("Data_Unique_ObsIDs:\n", Data_Unique_ObsIDs)
    Data_ObsID=Data_Unique_ObsIDs[Data_Unique_ObsIDs["ObsID"]==ObsID]
    RA_Aimpoint=Data_ObsID["RA_Aimpoint"].values[0]
    DEC_Aimpoint=Data_ObsID["DEC_Aimpoint"].values[0]
    #print("Aimpont: ", (RA_Aimpoint, DEC_Aimpoint))
    Close_ObsID_L=Close_ObsIDs_Query(ObsID, Data_Path=Data_Path)
    Overlapping_ObsID_L=[]
    for Close_ObsID in Close_ObsID_L:
        Data_Close_ObsID=Data_Unique_ObsIDs[Data_Unique_ObsIDs["ObsID"]==Close_ObsID]
        RA_Aimpoint_Close_ObsID=Data_Close_ObsID["RA_Aimpoint"].values[0]
        DEC_Aimpoint_Close_ObsID=Data_Close_ObsID["DEC_Aimpoint"].values[0]
        #print("Aimpont_Close_ObsID ("+str(Close_ObsID)+"): ", (RA_Aimpoint_Close_ObsID, DEC_Aimpoint_Close_ObsID))
        x1_Rad=Deg_to_Rad(RA_Aimpoint)
        x2_Rad=Deg_to_Rad(RA_Aimpoint_Close_ObsID)
        y1_Rad=Deg_to_Rad(DEC_Aimpoint)
        y2_Rad=Deg_to_Rad(DEC_Aimpoint_Close_ObsID)
        Have_Dist=Haversine_Distance(x1_Rad,x2_Rad,y1_Rad,y2_Rad)
        Have_Dist=np.abs(Have_Dist)
        Have_Dist_Deg=Rad_to_Deg(Have_Dist)
        Have_Dist_Arcmin=Have_Dist_Deg*60.0
        #print("Have_Dist_Arcmin: ", Have_Dist_Arcmin)
        if(Have_Dist_Arcmin<=20.0):
            Overlapping_ObsID_L.append(Close_ObsID)
    return Overlapping_ObsID_L

def Galactic_Limiting_Flux_Intersected_Region_Calc(Gname, Pickle_Save_Bool=False, Max_Counts=100, Counts_Step=10, Galactic_Radius_Max=2.0, Galactic_Radius_Step=0.25, Flux_Bool=False):
    Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
    Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
    #print("Evt2_File_H_L: ", Evt2_File_H_L)
    #Fov1_File_H_L=File_Query_Code_5.File_Query(Gname,"fov1")
    #print("Fov1_File_H_L: ", Fov1_File_H_L)
    #Exp_Max_B=False
    Evt2_File_H_L_Max_Exposure=File_Query_Code_5.File_Query(Gname,"evt2", Exp_Max_B=True)
    print("Evt2_File_H_L: ", Evt2_File_H_L)
    if(Evt2_File_H_L==False):
        raise Exception("No valid observations for "+str(Gname)+"!!!")
    print("Evt2_File_H_L_Max_Exposure: ", Evt2_File_H_L_Max_Exposure)
    ObsID_Max_Exposure=Evt2_File_H_L_Max_Exposure[0][0]
    Region_Galactic_Intersected_HL_Front_Illuminated_Max_Exposure, Region_Galactic_Intersected_HL_Back_Illuminated_Max_Exposure=Limiting_Flux_Intersected_Region_Calc(ObsID_Max_Exposure, Max_Counts=Max_Counts, Counts_Step=Counts_Step, Galactic_Radius_Max=Galactic_Radius_Max, Galactic_Radius_Step=Galactic_Radius_Step, Flux_Bool=Flux_Bool)
    #print("Region_Galactic_Intersected_HL_Front_Illuminated_Max_Exposure: ", Region_Galactic_Intersected_HL_Front_Illuminated_Max_Exposure)
    #return
    Region_Galactic_Intersected_HL_Front_Illuminated_Merged=Region_Galactic_Intersected_HL_Front_Illuminated_Max_Exposure
    Region_Galactic_Intersected_HL_Back_Illuminated_Merged=Region_Galactic_Intersected_HL_Back_Illuminated_Max_Exposure
    for i in range(0,len(Evt2_File_H_L)):
        Cur_Overlapping_Evt2_File_L=Evt2_File_H_L[i]
        #Cur_Overlapping_Fov1_File_L=Fov1_File_H_L[i]
        Cur_Overlapping_ObsID=Cur_Overlapping_Evt2_File_L[0]
        #Cur_Overlapping_Evt2_Path=Cur_Overlapping_Evt2_File_L[1]
        #Cur_Overlapping_Fov1_Path=Cur_Overlapping_Fov1_File_L[1]
        if(Cur_Overlapping_ObsID==ObsID_Max_Exposure):
            continue
        else:
            Cur_Overlapping_Region_Galactic_Intersected_HL_Front_Illuminated, Cur_Overlapping_Region_Galactic_Intersected_HL_Back_Illuminated=Limiting_Flux_Intersected_Region_Calc(Cur_Overlapping_ObsID,  Max_Counts=Max_Counts, Counts_Step=Counts_Step, Galactic_Radius_Max=Galactic_Radius_Max, Galactic_Radius_Step=Galactic_Radius_Step, Flux_Bool=Flux_Bool)
            X_Offset, Y_Offset = Aimpoint_Offset_Calc(ObsID_Max_Exposure, Cur_Overlapping_ObsID)
            #for Cur_Overlapping_Region_Galactic_Intersected_L_Front_Illuminated in Cur_Overlapping_Region_Galactic_Intersected_HL_Front_Illuminated:
            for j in range(0,len(Cur_Overlapping_Region_Galactic_Intersected_HL_Front_Illuminated)):
                Cur_Overlapping_Region_Galactic_Intersected_L_Front_Illuminated=Cur_Overlapping_Region_Galactic_Intersected_HL_Front_Illuminated[j]
                #for Cur_Overlapping_Region_Galactic_Intersected_Front_Illuminated in Cur_Overlapping_Region_Galactic_Intersected_L_Front_Illuminated:
                for k in range(0,len(Cur_Overlapping_Region_Galactic_Intersected_L_Front_Illuminated)):
                    Cur_Overlapping_Region_Galactic_Intersected_Front_Illuminated=Cur_Overlapping_Region_Galactic_Intersected_L_Front_Illuminated[k]
                    #Region_Galactic_Intersected_HL_Front_Illuminated_Merged[j][k]=Region_Galactic_Intersected_HL_Front_Illuminated_Merged[j][k]*Cur_Overlapping_Region_Galactic_Intersected_Front_Illuminated
                    """
                    SHIFT REGIONS FIRST!!!
                    """
                    Cur_Overlapping_Region_Galactic_Intersected_Front_Illuminated=Cur_Overlapping_Region_Galactic_Intersected_Front_Illuminated.edit(dx=X_Offset)
                    Cur_Overlapping_Region_Galactic_Intersected_Front_Illuminated=Cur_Overlapping_Region_Galactic_Intersected_Front_Illuminated.edit(dy=Y_Offset)
                    Region_Galactic_Intersected_HL_Front_Illuminated_Merged[j][k]=Region_Galactic_Intersected_HL_Front_Illuminated_Merged[j][k]+Cur_Overlapping_Region_Galactic_Intersected_Front_Illuminated

            for j in range(0,len(Cur_Overlapping_Region_Galactic_Intersected_HL_Back_Illuminated)):
                Cur_Overlapping_Region_Galactic_Intersected_L_Back_Illuminated=Cur_Overlapping_Region_Galactic_Intersected_HL_Back_Illuminated[j]
                #for Cur_Overlapping_Region_Galactic_Intersected_Back_Illuminated in Cur_Overlapping_Region_Galactic_Intersected_L_Back_Illuminated:
                for k in range(0,len(Cur_Overlapping_Region_Galactic_Intersected_L_Back_Illuminated)):
                    Cur_Overlapping_Region_Galactic_Intersected_Back_Illuminated=Cur_Overlapping_Region_Galactic_Intersected_L_Back_Illuminated[k]
                    #Region_Galactic_Intersected_HL_Back_Illuminated_Merged[j][k]=Region_Galactic_Intersected_HL_Back_Illuminated_Merged[j][k]*Cur_Overlapping_Region_Galactic_Intersected_Back_Illuminated
                    """
                    SHIFT REGIONS FIRST!!!
                    """
                    Cur_Overlapping_Region_Galactic_Intersected_Back_Illuminated=Cur_Overlapping_Region_Galactic_Intersected_Back_Illuminated.edit(dx=X_Offset)
                    Cur_Overlapping_Region_Galactic_Intersected_Back_Illuminated=Cur_Overlapping_Region_Galactic_Intersected_Back_Illuminated.edit(dy=Y_Offset)
                    Region_Galactic_Intersected_HL_Back_Illuminated_Merged[j][k]=Region_Galactic_Intersected_HL_Back_Illuminated_Merged[j][k]+Cur_Overlapping_Region_Galactic_Intersected_Back_Illuminated
    """
    if(Pickle_Save_Bool):
        Pickle_Save((Region_Galactic_Intersected_HL_Front_Illuminated_Merged, Region_Galactic_Intersected_HL_Back_Illuminated_Merged), str(Gname_Modifed)+"_Merged_Region.pickle")
    """
    return Region_Galactic_Intersected_HL_Front_Illuminated_Merged, Region_Galactic_Intersected_HL_Back_Illuminated_Merged

def Merged_Area_Calc(Gname, Max_Counts=100, Counts_Step=10, Galactic_Radius_Max=2.0, Galactic_Radius_Step=0.25, D25_Area_Bool=False, Flux_Bool=False):
    Region_Galactic_Intersected_HL_Front_Illuminated_Merged, Region_Galactic_Intersected_HL_Back_Illuminated_Merged=Galactic_Limiting_Flux_Intersected_Region_Calc(Gname, Pickle_Save_Bool=False, Max_Counts=Max_Counts, Counts_Step=Counts_Step, Galactic_Radius_Max=Galactic_Radius_Max, Galactic_Radius_Step=Galactic_Radius_Step, Flux_Bool=Flux_Bool)
    if(D25_Area_Bool):
        Circular_D25_Bool=False
        D25_Tuple=D25_Finder.D25_Full_Query(Gname)
        if(isinstance(D25_Tuple[1],np.ma.core.MaskedConstant) or isinstance(D25_Tuple[2],np.ma.core.MaskedConstant)): #In the event that the ellipse is assumed to be a cirlce by RC3
            #print(str(ObsID)+" has a circular D25 region")
            Circular_D25_Bool=True
        D25_S_Maj_Arcmin=D25_Tuple[0]
        D25_S_Min_Arcmin=D25_Tuple[1]
        D25_S_Maj=D25_S_Maj_Arcmin*60.0 #D25_S_Maj:-float, D25_Semi_Major_Axis, The D25 Semi Major Axis of the current galaxy in arcseconds
        D25_S_Min=D25_S_Min_Arcmin*60.0 #D25_S_Maj:-float, D25_Semi_Minor_Axis, The D25 Semi Minor Axis of the current galaxy in arcseconds
        D25_S_Maj_Phys=D25_S_Maj*2.03252032520325 #D25_S_Maj_Phys:-numpy.float64, D25_Semi_Major_Axis_Physical, D25 Semi Major Axis of the current galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
        D25_S_Min_Phys=D25_S_Min*2.03252032520325 #D25_S_Min_Phys:-numpy.float64, D25_Semi_Minor_Axis_Physical, D25 Semi Minor Axis of the current galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
        """
        if(Circular_D25_Bool==False):
            Galaxy_Region=ellipse(0,0,D25_S_Maj_Phys,D25_S_Min_Phys,0) #Need to add circular case!
        else:
            Galaxy_Region=circle(0,0,D25_S_Maj_Phys)
        #Galaxy_Region=Galaxy_Region.edit(stretch=10.0) #For Testing
        print("Galaxy_Region: ", Galaxy_Region)
        Galaxy_Area_Physical=Galaxy_Region.area(pixel=True,bin=1)
        """
        Galaxy_Area_Physical=D25_S_Maj_Phys**2.0
    #print("TEST")
    #Area_Front_Illuminated_Merged_HL=Region_Galactic_Intersected_HL_Front_Illuminated_Merged
    #Area_Back_Illuminated_Merged_HL=Region_Galactic_Intersected_HL_Back_Illuminated_Merged
    Area_Front_Illuminated_Merged_HL=[]
    for j in range(0,len(Region_Galactic_Intersected_HL_Front_Illuminated_Merged)):
        Area_Front_Illuminated_Merged_L=[]
        #for k in range(0,len(Region_Galactic_Intersected_HL_Front_Illuminated_Merged)): #This may be a bug
        for k in range(0,len(Region_Galactic_Intersected_HL_Front_Illuminated_Merged[j])):
            #Area_Front_Illuminated_Merged_HL[j][k]=Region_Galactic_Intersected_HL_Front_Illuminated_Merged[j][k].area(pixel=True,bin=1)
            #Area_Front_Illuminated_Merged_HL[j][k]=(Area_Front_Illuminated_Merged_HL[j][k].area(pixel=True,bin=1))
            #Area_Front_Illuminated_Merged_HL[j][k]=(Area_Front_Illuminated_Merged_HL[j][k].area(pixel=True,bin=1))
            #print("Region_Galactic_Intersected_HL_Front_Illuminated_Merged[j][k]: ", Region_Galactic_Intersected_HL_Front_Illuminated_Merged[j][k])
            Current_Area_Front_Illuminated=(Region_Galactic_Intersected_HL_Front_Illuminated_Merged[j][k].area(pixel=True,bin=1))
            #print("Current_Area_Front_Illuminated: ", Current_Area_Front_Illuminated)
            #Area_Front_Illuminated_Merged_HL[j][k]=Current_Area_Front_Illuminated
            if(Current_Area_Front_Illuminated<1.0):
                Current_Area_Front_Illuminated=0.0
            if(D25_Area_Bool):
                Current_Area_Front_Illuminated=Current_Area_Front_Illuminated/Galaxy_Area_Physical
            Area_Front_Illuminated_Merged_L.append(Current_Area_Front_Illuminated)
        Area_Front_Illuminated_Merged_HL.append(Area_Front_Illuminated_Merged_L)
    #print("TEST 2")
    Area_Back_Illuminated_Merged_HL=[]
    for j in range(0,len(Region_Galactic_Intersected_HL_Back_Illuminated_Merged)):
        Area_Back_Illuminated_Merged_L=[]
        #for k in range(0,len(Region_Galactic_Intersected_HL_Back_Illuminated_Merged)):
        for k in range(0,len(Region_Galactic_Intersected_HL_Back_Illuminated_Merged[j])):
            #Area_Back_Illuminated_Merged_HL[j][k]=Region_Galactic_Intersected_HL_Back_Illuminated_Merged[j][k].area(pixel=True,bin=1)
            #Area_Back_Illuminated_Merged_HL[j][k]=(Area_Back_Illuminated_Merged_HL[j][k].area(pixel=True,bin=1))
            #Area_Back_Illuminated_Merged_HL[j][k]=(Area_Back_Illuminated_Merged_HL[j][k].area(pixel=True,bin=1))
            #print("Region_Galactic_Intersected_HL_Back_Illuminated_Merged[j][k]: ", Region_Galactic_Intersected_HL_Back_Illuminated_Merged[j][k])
            Current_Area_Back_Illuminated=(Region_Galactic_Intersected_HL_Back_Illuminated_Merged[j][k].area(pixel=True,bin=1))
            #print("Current_Area_Back_Illuminated: ", Current_Area_Back_Illuminated)
            #Area_Back_Illuminated_Merged_HL[j][k]=Current_Area_Back_Illuminated
            if(Current_Area_Back_Illuminated<1.0):
                Current_Area_Back_Illuminated=0.0
            if(D25_Area_Bool):
                Current_Area_Back_Illuminated=Current_Area_Back_Illuminated/Galaxy_Area_Physical
            Area_Back_Illuminated_Merged_L.append(Current_Area_Back_Illuminated)
        Area_Back_Illuminated_Merged_HL.append(Area_Back_Illuminated_Merged_L)

    return Area_Front_Illuminated_Merged_HL, Area_Back_Illuminated_Merged_HL


def Save_FOV1_Region(ObsID_1,ObsID_2=None):
    if(ObsID_2!=None):
        FOV1_Path=File_Query_Code_5.ObsID_File_Query(ObsID_2,ObsID_Path='/opt/xray/anthony/expansion_backup/ObsIDs/',key="fov1")
        CCD_Regions=CXCRegion(FOV1_Path)
        X_Offset, Y_Offset = Aimpoint_Offset_Calc(ObsID_1, ObsID_2)
        CCD_Regions=CCD_Regions.edit(dx=X_Offset)
        CCD_Regions=CCD_Regions.edit(dy=Y_Offset)
        CCD_Regions.write(str(ObsID_2)+"_FOV1_Shifted.reg", clobber=True, newline=True)
    else:
        FOV1_Path=File_Query_Code_5.ObsID_File_Query(ObsID_1,ObsID_Path='/opt/xray/anthony/expansion_backup/ObsIDs/',key="fov1")
        FOV_Path_Front_Illuminated_Chips=FOV1_Path+'[ccd_id=0,1,2,3,4,6,8,9]'
        #FOV_Path_Front_Illuminated_Chips=FOV1_Path #For Testing
        FOV_Path_Back_Illuminated_Chips=FOV1_Path+'[ccd_id=5,7]'
        #FOV1_Path=FOV_Path_Front_Illuminated_Chips
        #FOV1_Path=FOV_Path_Back_Illuminated_Chips
        CCD_Regions=CXCRegion(FOV1_Path)
        CCD_Regions.write(str(ObsID_1)+"_FOV1.reg", clobber=True, newline=True)


def Merged_Area_Calc_Galaxy_L(Gname_L, Max_Counts=100, Counts_Step=10, Galactic_Radius_Max=2.0, Galactic_Radius_Step=0.25, D25_Area_Bool=False, Flux_Bool=False):
    Area_Merged_HHL=[]
    Gname_Fail_L=[]
    for Gname in Gname_L:
        try:
            print("Gname: ", Gname)
            ##Cur_Area_Front_Illuminated_Merged_HL, Cur_Area_Back_Illuminated_Merged_HL=Merged_Area_Calc(Gname)
            ###Cur_Area_Front_Illuminated_Merged_HL, Cur_Area_Back_Illuminated_Merged_HL=Merged_Area_Calc(Gname, Max_Counts=Max_Counts, Counts_Step=Counts_Step, Galactic_Radius_Max=Galactic_Radius_Max, Galactic_Radius_Step=Galactic_Radius_Step)
            Cur_Area_Front_Illuminated_Merged_HL, Cur_Area_Back_Illuminated_Merged_HL=Merged_Area_Calc(Gname, Max_Counts=Max_Counts, Counts_Step=Counts_Step, Galactic_Radius_Max=Galactic_Radius_Max, Galactic_Radius_Step=Galactic_Radius_Step, D25_Area_Bool=D25_Area_Bool, Flux_Bool=Flux_Bool)
            Area_Merged_HHL.append(Cur_Area_Front_Illuminated_Merged_HL)
            Area_Merged_HHL.append(Cur_Area_Back_Illuminated_Merged_HL)
        except:
            Gname_Fail_L.append(Gname)
    ##print("Gname_Fail_L: ", Gname_Fail_L)
    #print("Area_Merged_HHL: ", Area_Merged_HHL)
    """
    for Area_Merged_HL in Area_Merged_HHL:
        print("Current Area_Merged_HL: ", Area_Merged_HL)
    """
    Area_Merged_All_A=np.sum(Area_Merged_HHL, axis=0)
    #print(len(list(Area_Merged_All_A)))
    if(D25_Area_Bool==False):
        Area_Merged_All_A_Deg=Area_Merged_All_A*((0.4920/3600.0)**2.0)
        Area_Merged_All_DF_Deg=pd.DataFrame(Area_Merged_All_A_Deg)
        Area_Merged_All_DF_Deg.to_csv('Limiting_Flux_Areas.csv', index=False)
        Area_Merged_All_DF=Area_Merged_All_DF_Deg
    else:
        Area_Merged_All_DF=pd.DataFrame(Area_Merged_All_A)
        Area_Merged_All_DF.to_csv('Limiting_Flux_D25_Areas.csv', index=False)
    print("Gname_Fail_L: ", Gname_Fail_L)
    return Area_Merged_All_DF


"""
def Theta_Intersection_Calc(ObsID, Max_Counts=100, Counts_Step=10, Data_Input=dir+'/../Marx_Source_Injection/Source_Detection_Analysis/Marx_Source_Detection_Data.csv', Flux_Bool=False):
    Background_Tuple=Background_Calc(ObsID)
    Background_Front_Illuminated=Background_Tuple[0]
    Background_Back_Illuminated=Background_Tuple[1]
    Counts_L=list(range(0,Max_Counts+1,Counts_Step))
    if(Flux_Bool):
        Flux_L=Flux_Array_Calc()
        Gamma=Gamma_Calc(ObsID)
        Counts_L=[]
        for Flux in Flux_L:
            Counts=Flux_to_Counts_Convert(Flux,ObsID,Gamma=Gamma)
            Counts_L.append(Counts)
    print("Counts_L: ", Counts_L)
    Theta_Intersection_HL_Tuple_HL=[]
    for i in range(0,len(Counts_L)-1):
        Limiting_Counts_Low=Counts_L[i]
        Limiting_Counts_High=Counts_L[i+1]
        if((Limiting_Counts_High<3) or (Limiting_Counts_Low>30)):
            Theta_Intersection_HL_Tuple_HL.append(([],[]))
            continue
        Theta_Intersection_HL_Front_Illuminated=Source_Detection_Analysis.Limiting_Counts_Annuli_Calc(Limiting_Counts_Low, Limiting_Counts_High, Background_Front_Illuminated, Data_Input=Data_Input)
        #print("Theta_Intersection_HL_Front_Illuminated: ", Theta_Intersection_HL_Front_Illuminated)
        Theta_Intersection_HL_Back_Illuminated=Source_Detection_Analysis.Limiting_Counts_Annuli_Calc(Limiting_Counts_Low, Limiting_Counts_High, Background_Back_Illuminated, Data_Input=Data_Input)
        #print("Theta_Intersection_HL_Back_Illuminated: ", Theta_Intersection_HL_Back_Illuminated)
        Cur_Theta_Intersection_HL_Tuple=(Theta_Intersection_HL_Front_Illuminated,Theta_Intersection_HL_Back_Illuminated)
        #print("Cur_Theta_Intersection_HL_Tuple: ", Cur_Theta_Intersection_HL_Tuple)
        Theta_Intersection_HL_Tuple_HL.append(Cur_Theta_Intersection_HL_Tuple)
    return Theta_Intersection_HL_Tuple_HL
"""

def Source_Flux_Area_Calc(ObsID, Source_Num, Max_Counts=100, Counts_Step=10, Galactic_Radius_Max=2.0, Galactic_Radius_Step=0.25, Theta_Intersection_HL_Tuple_HL=None, Background_Tuple=None, Data_Input=dir+"/../SQL_Standard_File/Source_Flux_All_Modified_6.csv", Limiting_Flux_Area_Path=dir+"/Limiting_Flux_Areas.csv", Source_Detection_Data_Input=dir+'/../Marx_Source_Injection/Source_Detection_Analysis/Marx_Source_Detection_Data.csv', Flux_Bool=False):
    if(isinstance(Data_Input,str)):
        Data=pd.read_csv(Data_Input)
    else:
        Data=Data_Input
    if(isinstance(Source_Detection_Data_Input,str)):
        Data_Source_Detection, Data_Grouped, Data_Grouped_Mean, Data_Grouped_Sum=Source_Detection_Analysis.Process_Data(Source_Detection_Data_Input)
        Source_Detection_Data_Input=Data_Grouped_Mean
    """
    Need to filter data of duplicate sources!!!
    """
    Data_Source=Data[(Data["ObsID"]==ObsID) & (Data["Source_Num"]==Source_Num)]
    #print("Data_Source: ", Data_Source)
    #CHIP_ID, THETA, Source_Distance_From_GC_Elliptical_D25, COUNTS_0.3-8.0, NET_COUNTS_0.3-8.0
    Chip_ID=Data_Source["CHIP_ID"].values[0]
    #print("type(Chip_ID): ", type(Chip_ID))
    Theta=Data_Source["THETA"].values[0]
    Counts=Data_Source["COUNTS_0.3-8.0"].values[0]
    Source_Distance_From_GC_Elliptical_D25=Data_Source["Source_Distance_From_GC_Elliptical_D25"].values[0]
    #Source_Detection_Analysis.Limiting_Counts_Annuli_Calc(Limiting_Counts_Low, Limiting_Counts_High, Background_Front_Illuminated, Data_Input=Data_Input)
    if(Background_Tuple==None):
        Background_Tuple=Background_Calc(ObsID)
    Chip_ID_Front_Illuminated_L=[0,1,2,3,4,6,8,9]
    Chip_ID_Back_Illuminated_L=[5,7]
    if(Chip_ID in Chip_ID_Front_Illuminated_L):
        Back_Illuminated_Bool=False
    if(Chip_ID in Chip_ID_Back_Illuminated_L):
        Back_Illuminated_Bool=True
    Background=Background_Tuple[int(Back_Illuminated_Bool)]
    #Source_Detection_Bool=Source_Detection_Analysis.Limiting_Count_Cut(Counts, Theta, Background, Data_Input=Data_Input)
    ##Source_Detection_Bool=Source_Detection_Analysis.Limiting_Count_Cut(Counts, Theta, Background, Data_Input=dir+'/../Marx_Source_Injection/Source_Detection_Analysis/Marx_Source_Detection_Data.csv')
    Source_Detection_Bool=Source_Detection_Analysis.Limiting_Count_Cut(Counts, Theta, Background, Data_Input=Source_Detection_Data_Input)
    if(Source_Detection_Bool==False):
        return None,None
    if(Theta_Intersection_HL_Tuple_HL==None):
        ##Theta_Intersection_HL_Tuple_HL=Theta_Intersection_Calc(ObsID, Max_Counts=Max_Counts, Counts_Step=Counts_Step, Data_Input=dir+'/../Marx_Source_Injection/Source_Detection_Analysis/Marx_Source_Detection_Data.csv')
        Theta_Intersection_HL_Tuple_HL=Theta_Intersection_Calc(ObsID, Max_Counts=Max_Counts, Counts_Step=Counts_Step, Data_Input=Source_Detection_Data_Input, Flux_Bool=Flux_Bool)
    """
    Chip_ID_Front_Illuminated_L=[0,1,2,3,4,6,8,9]
    Chip_ID_Back_Illuminated_L=[5,7]
    if(Chip_ID in Chip_ID_Front_Illuminated_L):
        Back_Illuminated_Bool=False
    if(Chip_ID in Chip_ID_Back_Illuminated_L):
        Back_Illuminated_Bool=True
    """
    Theta_Intersection_HL=[]
    for Theta_Intersection_HL_Tuple in Theta_Intersection_HL_Tuple_HL:
        Theta_Intersection_HL.append(Theta_Intersection_HL_Tuple[int(Back_Illuminated_Bool)])
    print("Theta_Intersection_HL: ", Theta_Intersection_HL)
    Matching_Flux_Bin_Index=None
    for i in range(0,len(Theta_Intersection_HL)):
        Cur_Theta_Intersection_L=Theta_Intersection_HL[i]
        #for Cur_Theta_Intersection_Group in Cur_Theta_Intersection_L:
        for j in range(0,len(Cur_Theta_Intersection_L)):
            Cur_Theta_Intersection_Group=Cur_Theta_Intersection_L[j]
            #print("Cur_Theta_Intersection_Group: ", Cur_Theta_Intersection_Group)
            Cur_Theta_Low=Cur_Theta_Intersection_Group[0]
            Cur_Theta_High=Cur_Theta_Intersection_Group[1]
            if((Theta>=Cur_Theta_Low) and (Theta<Cur_Theta_High)):
                ##Matching_Flux_Bin_Index=j
                Matching_Flux_Bin_Index=i
                break
            #break #This might be a bug
    #print("Matching_Flux_Bin_Index: ", Matching_Flux_Bin_Index)
    Galaxy_Size_Scalers_L=list(np.arange(0, float(Galactic_Radius_Max)+Galactic_Radius_Step, Galactic_Radius_Step))
    Matching_D25_Bin_Index=None
    #print("Source_Distance_From_GC_Elliptical_D25: ", Source_Distance_From_GC_Elliptical_D25)
    for i in range(0,len(Galaxy_Size_Scalers_L)-1):
        Cur_Inner_Scaler=Galaxy_Size_Scalers_L[i]
        #print("Cur_Inner_Scaler: ", Cur_Inner_Scaler)
        Cur_Outer_Scaler=Galaxy_Size_Scalers_L[i+1]
        #print("Cur_Outer_Scaler: ", Cur_Outer_Scaler)
        if((Source_Distance_From_GC_Elliptical_D25>=Cur_Inner_Scaler) and (Source_Distance_From_GC_Elliptical_D25<Cur_Outer_Scaler)):
            Matching_D25_Bin_Index=i
            break
    #print("Matching_D25_Bin_Index: ", Matching_D25_Bin_Index)
    return Matching_Flux_Bin_Index, Matching_D25_Bin_Index

def Source_Flux_Area_Calc_Bulk(ObsID, Max_Counts=100, Counts_Step=10, Galactic_Radius_Max=2.0, Galactic_Radius_Step=0.25, Theta_Intersection_HL_Tuple_HL=None, Background_Tuple=None, Data_Input=dir+"/../SQL_Standard_File/Source_Flux_All_Modified_6.csv", Limiting_Flux_Area_Path=dir+"/Limiting_Flux_Areas.csv", Source_Detection_Data_Input=dir+'/../Marx_Source_Injection/Source_Detection_Analysis/Marx_Source_Detection_Data.csv', Flux_Bool=False):
    if(isinstance(Data_Input,str)):
        Data=pd.read_csv(Data_Input)
    else:
        Data=Data_Input
    if(isinstance(Source_Detection_Data_Input,str)):
        Data_Source_Detection, Data_Grouped, Data_Grouped_Mean, Data_Grouped_Sum=Source_Detection_Analysis.Process_Data(Source_Detection_Data_Input)
        Source_Detection_Data_Input=Data_Grouped_Mean
    Data_ObsID=Data[(Data["ObsID"]==ObsID)]
    Theta_A=Data_ObsID["THETA"]
    Theta_L=list(Theta_A)
    #Theta_Intersection_HL_Tuple_HL=Theta_Intersection_Calc(ObsID, Max_Counts=Max_Counts, Counts_Step=Counts_Step, Data_Input=Data)
    ##Theta_Intersection_HL_Tuple_HL=Theta_Intersection_Calc(ObsID, Max_Counts=Max_Counts, Counts_Step=Counts_Step)
    Theta_Intersection_HL_Tuple_HL=Theta_Intersection_Calc(ObsID, Max_Counts=Max_Counts, Counts_Step=Counts_Step, Data_Input=Source_Detection_Data_Input, Flux_Bool=Flux_Bool)
    if(Background_Tuple==None):
        Background_Tuple=Background_Calc(ObsID)
    Match_Index_Tuple_L=[]
    for i in range(0,len(Theta_A)):
        Source_Num=i+1
        ##Matching_Flux_Bin_Index, Matching_D25_Bin_Index = Source_Flux_Area_Calc(ObsID, Source_Num,  Max_Counts=Max_Counts, Counts_Step=Counts_Step, Galactic_Radius_Max=Galactic_Radius_Max, Galactic_Radius_Step=Galactic_Radius_Step, Theta_Intersection_HL_Tuple_HL=Theta_Intersection_HL_Tuple_HL, Data_Input=Data_ObsID, Limiting_Flux_Area_Path=dir+"/Limiting_Flux_Areas.csv")
        Matching_Flux_Bin_Index, Matching_D25_Bin_Index = Source_Flux_Area_Calc(ObsID, Source_Num,  Max_Counts=Max_Counts, Counts_Step=Counts_Step, Galactic_Radius_Max=Galactic_Radius_Max, Galactic_Radius_Step=Galactic_Radius_Step, Theta_Intersection_HL_Tuple_HL=Theta_Intersection_HL_Tuple_HL, Background_Tuple=Background_Tuple, Data_Input=Data_ObsID, Limiting_Flux_Area_Path=dir+"/Limiting_Flux_Areas.csv", Source_Detection_Data_Input=Source_Detection_Data_Input, Flux_Bool=Flux_Bool)
        Match_Index_Tuple_L.append((Matching_Flux_Bin_Index,Matching_D25_Bin_Index))
    return Match_Index_Tuple_L

def Parse_List(L):
    if(len(L)==2):
        return []
    #Element_L=re.split("[\[\],]", L)
    Element_L=re.split("[\[\];]", L)
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
        #print("Element_L[i]: ", Element_L[i])
        ObsID=Element_L[i]
        if(ObsID==""):
            continue
        ObsID=int(ObsID)
        Src_Num=int(Element_L[j])
        Cur_L=[ObsID,Src_Num]
        HL.append(Cur_L)
    return HL

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
    Duplicate_Source_L=[]
    for Duplicate in Duplicate_L:
        Cur_ObsID=Duplicate[0]
        Cur_Source_Num=Duplicate[1]
        Duplicate_Source_L.append([Cur_ObsID,Cur_Source_Num])
    return Duplicate_Source_L

def Find_Duplicate_Data(Data,ObsID,Source_Num):
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
        #print("Cur_Source_Num: ", Cur_Source_Num)
        #Data_Matched=Find_Source(Cur_ObsID,Cur_Source_Num)
        Data_Matched=Find_Source(Data,Cur_ObsID,Cur_Source_Num)
        if(i==0):
            Duplicate_Data=Data_Matched
        if(i>0):
            Data_Matched=pd.concat([Data_Matched, Duplicate_Data])
        i=i+1
    return Data_Matched

def Remove_Duplicate_Souces(Source_Flux_Area_HL, Data_Input=dir+"/../SQL_Standard_File/Source_Flux_All_Modified_6.csv"):
    Source_Flux_Area_HL_Modified=Source_Flux_Area_HL
    if(isinstance(Data_Input,str)):
        Data=pd.read_csv(Data_Input)
    else:
        Data=Data_Input
    #for Gname_HL in Source_Flux_Area_HL:
    for i in range(0,len(Source_Flux_Area_HL)):
        Gname_HL=Source_Flux_Area_HL[i]
        Gname=Gname_HL[0]
        ObsID_HHL=Gname_HL[1]
        Data_Gname=Data[(Data["Gname_Homogenized"]==Gname)]
        #for ObsID_HL in ObsID_HHL:
        for j in range(0,len(ObsID_HHL)):
            ObsID_HL=ObsID_HHL[j]
            ObsID=ObsID_HL[0]
            Miniumn_ObsID_Bool=True
            for ObsID_HL_Test in ObsID_HHL:
                ObsID_Test=ObsID_HL_Test[0]
                if(ObsID_Test<ObsID):
                    Miniumn_ObsID_Bool=False
            Source_L=ObsID_HL[1]
            for k in range(0,len(Source_L)):
                Source_Num=k+1
                Cur_Source_Tuple=Source_L[k]
                if(None in Cur_Source_Tuple):
                    continue
                Duplicate_Source_HL=Find_Duplicate(Data_Gname,ObsID,Source_Num)
                if(isinstance(Duplicate_Source_HL,list)==False):
                    continue
                #print(str(ObsID)+" : "+str(Source_Num)+" Duplicate_Source_HL: ", Duplicate_Source_HL)
                Matching_Source_Tuple_L=[]
                for Duplicate_Source_L in Duplicate_Source_HL:
                    Duplicate_ObsID=Duplicate_Source_L[0]
                    Duplicate_Source_Num=Duplicate_Source_L[1]
                    #ObsID_HHL.index(Duplicate_ObsID)
                    for ObsID_HL_Test in ObsID_HHL:
                        if(ObsID_HL_Test[0]==Duplicate_ObsID):
                            Matching_Source_Tuple=ObsID_HL_Test[1][Duplicate_Source_Num-1]
                            Matching_Source_Tuple_L.append(Matching_Source_Tuple)
                #print("Matching_Source_Tuple_L: ", Matching_Source_Tuple_L)
                Source_Tuple_Max_Flux_Bin=Cur_Source_Tuple
                #Source_Tuple_Max_Equal_Bin_L=[]
                Duplicate_Found_Bool=False
                for Matching_Source_Tuple in Matching_Source_Tuple_L:
                    if(None in Matching_Source_Tuple):
                        continue
                    #print("Matching_Source_Tuple: ", Matching_Source_Tuple)
                    if(Source_Tuple_Max_Flux_Bin[0]>Matching_Source_Tuple[0]):
                        #print("Duplicate Found!!!")
                        Duplicate_Found_Bool=True
                        Source_Tuple_Max_Flux_Bin=Matching_Source_Tuple
                        Source_Flux_Area_HL_Modified[i][1][j][1][k]=(None,None)
                        break
                if((Duplicate_Found_Bool==False) and (Miniumn_ObsID_Bool==False)):
                    Source_Flux_Area_HL_Modified[i][1][j][1][k]=(None,None)
        return Source_Flux_Area_HL_Modified



def Source_Flux_Area_Calc_Galaxy_Bulk(Gname_L, Max_Counts=100, Counts_Step=10, Galactic_Radius_Max=2.0, Galactic_Radius_Step=0.25, Theta_Intersection_HL_Tuple_HL=None, Data_Input=dir+"/../SQL_Standard_File/Source_Flux_All_Modified_6.csv", Limiting_Flux_Area_Path=dir+"/Limiting_Flux_Areas.csv", Flux_Bool=False):
    if(isinstance(Data_Input,str)):
        Data=pd.read_csv(Data_Input)
    else:
        Data=Data_Input
    Fail_L=[]
    Source_Flux_Area_HL=[]
    for Gname in Gname_L:
        try:
            Data_Gname=Data[(Data["Gname_Homogenized"]==Gname)]
            Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
            Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
            Cur_Source_Flux_Area_L=[]
            for Evt2_File_L in Evt2_File_H_L:
                Cur_ObsID=Evt2_File_L[0]
                Cur_Match_Index_Tuple_L=Source_Flux_Area_Calc_Bulk(Cur_ObsID, Max_Counts=Max_Counts, Counts_Step=Counts_Step, Galactic_Radius_Max=Galactic_Radius_Max, Galactic_Radius_Step=Galactic_Radius_Step, Theta_Intersection_HL_Tuple_HL=None, Data_Input=Data_Gname, Limiting_Flux_Area_Path=dir+"/Limiting_Flux_Areas.csv", Flux_Bool=Flux_Bool)
                Cur_Source_Flux_Area_L.append([Cur_ObsID,Cur_Match_Index_Tuple_L])
            ##Source_Flux_Area_HL.append(Cur_Source_Flux_Area_L)
            Source_Flux_Area_HL.append([Gname,Cur_Source_Flux_Area_L])
        except:
            Fail_L.append(Gname)
    print("Fail_L: ", Fail_L)
    Source_Flux_Area_HL=Remove_Duplicate_Souces(Source_Flux_Area_HL,Data_Input=Data_Input)
    return Source_Flux_Area_HL

def Source_Count_Matrix_Calc(Gname_L, Max_Counts=100, Counts_Step=10, Galactic_Radius_Max=2.0, Galactic_Radius_Step=0.25, Theta_Intersection_HL_Tuple_HL=None, Data_Input=dir+"/../SQL_Standard_File/Source_Flux_All_Modified_6.csv", Limiting_Flux_Area_Path=dir+"/Limiting_Flux_Areas.csv", Flux_Bool=False):
    Counts_L=list(range(0,Max_Counts+1,Counts_Step))
    Galaxy_Size_Scalers_L=list(np.arange(0, float(Galactic_Radius_Max)+Galactic_Radius_Step, Galactic_Radius_Step))
    Source_Flux_Area_HL=Source_Flux_Area_Calc_Galaxy_Bulk(Gname_L, Max_Counts=Max_Counts, Counts_Step=Counts_Step, Galactic_Radius_Max=Galactic_Radius_Max, Galactic_Radius_Step=Galactic_Radius_Step, Theta_Intersection_HL_Tuple_HL=None, Data_Input=dir+"/../SQL_Standard_File/Source_Flux_All_Modified_6.csv", Limiting_Flux_Area_Path=dir+"/Limiting_Flux_Areas.csv", Flux_Bool=Flux_Bool)
    #Source_Count_Matrix=np.zeros((len(Counts_L), len(Galaxy_Size_Scalers_L)))
    Source_Count_Matrix=np.zeros((len(Counts_L)-1, len(Galaxy_Size_Scalers_L)-1))
    Fail_L=[]
    for Cur_Galaxy_HL in Source_Flux_Area_HL:
        try:
            Gname=Cur_Galaxy_HL[0]
            Cur_Galaxy_Source_Flux_Area_HL=Cur_Galaxy_HL[1]
            for Cur_ObsID_HL in Cur_Galaxy_Source_Flux_Area_HL:
                ObsID=Cur_ObsID_HL[0]
                Cur_ObsID_Source_Flux_Area_HL=Cur_ObsID_HL[1]
                for Cur_Source_Bin_Tuple in Cur_ObsID_Source_Flux_Area_HL:
                    if None in Cur_Source_Bin_Tuple:
                        continue
                    Limting_Flux_Bin_Index=Cur_Source_Bin_Tuple[0]
                    Galactic_Radius_Bin_Index=Cur_Source_Bin_Tuple[1]
                    Source_Count_Matrix[Limting_Flux_Bin_Index][Galactic_Radius_Bin_Index]=Source_Count_Matrix[Limting_Flux_Bin_Index][Galactic_Radius_Bin_Index]+1
        except:
            Fail_L.append(Cur_Galaxy_HL)
    print("Fail_L: ", Fail_L)
    Source_Count_Matrix_DF=pd.DataFrame(Source_Count_Matrix)
    Source_Count_Matrix_DF.to_csv('Source_Count_Matrix.csv', index=False)
    return Source_Count_Matrix

def Differential_LogN_LogC_Calc(Source_Count_Matrix_Path='Source_Count_Matrix.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas.csv', Counts_Step=10):
    Source_Count_Matrix_A=pd.read_csv(Source_Count_Matrix_Path)
    print("Source_Count_Matrix_A:\n", Source_Count_Matrix_A)
    Limiting_Flux_Areas_A=pd.read_csv(Limiting_Flux_Areas_Path)
    print("Limiting_Flux_Areas_A:\n", Limiting_Flux_Areas_A)
    Differential_LogN_LogC_Matrix=Source_Count_Matrix_A/Limiting_Flux_Areas_A
    Differential_LogN_LogC_Matrix=Differential_LogN_LogC_Matrix/Counts_Step
    print("Differential_LogN_LogC_Matrix:\n", Differential_LogN_LogC_Matrix)
    Differential_LogN_LogC_Matrix.to_csv('Differential_LogN_LogC_Matrix.csv', index=False)
    return Differential_LogN_LogC_Matrix

def LogN_LogC_Calc(Source_Count_Matrix_Path='Source_Count_Matrix.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas.csv', Counts_Step=10):
    Differential_LogN_LogC_Matrix=Differential_LogN_LogC_Calc(Source_Count_Matrix_Path=Source_Count_Matrix_Path, Limiting_Flux_Areas_Path=Limiting_Flux_Areas_Path, Counts_Step=Counts_Step)
    Differential_LogN_LogC_Matrix_Count_Integrated=Differential_LogN_LogC_Matrix*Counts_Step
    #Differential_LogN_LogC_Matrix_Count_Integrated=Differential_LogN_LogC_Matrix_Count_Integrated.to_numpy()
    #print("Differential_LogN_LogC_Matrix_Count_Integrated:\n", Differential_LogN_LogC_Matrix_Count_Integrated)
    LogN_LogC_Matrix=Differential_LogN_LogC_Matrix_Count_Integrated.iloc[::-1].cumsum().iloc[::-1]
    print("LogN_LogC_Matrix:\n", LogN_LogC_Matrix)
    Source_Count_Matrix_A=pd.read_csv(Source_Count_Matrix_Path)
    print("Source_Count_Matrix_A:\n", Source_Count_Matrix_A)
    Source_Count_Matrix_Integrated_A=Source_Count_Matrix_A.iloc[::-1].cumsum().iloc[::-1]
    Error_Matrix=LogN_LogC_Matrix/(Source_Count_Matrix_Integrated_A.apply(np.sqrt))
    print("Error_Matrix\n:", Error_Matrix)
    LogN_LogC_Matrix.to_csv('Integral_LogN_LogC_Matrix.csv', index=False)
    return LogN_LogC_Matrix, Error_Matrix

def Log_N_Log_C_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas.csv', Counts_Step=10, Galactic_Radius_Max=2.0, Galactic_Radius_Step=0.25):
    LogN_LogC_Tuple=LogN_LogC_Calc(Source_Count_Matrix_Path=Source_Count_Matrix_Path, Limiting_Flux_Areas_Path=Limiting_Flux_Areas_Path, Counts_Step=Counts_Step)
    LogN_LogC_Matrix=LogN_LogC_Tuple[0]
    LogN_LogC_Error_Matrix=LogN_LogC_Tuple[1]
    Matrix_Shape=LogN_LogC_Matrix.shape
    ##LogN_LogC_Matrix_Background=LogN_LogC_Matrix.iloc[:, [2, :]]
    #Counts_L=list(range(0,Max_Counts+1,Counts_Step))
    #Galaxy_Size_Scalers_L=list(np.arange(0, float(Galactic_Radius_Max)+Galactic_Radius_Step, Galactic_Radius_Step))
    Flux_Bins=list(np.array(list(range(0,Matrix_Shape[0])))*Counts_Step)
    print("Flux_Bins: ", Flux_Bins)
    #Color_L=["red","orange","yellow","green","lime","cyan","blue","purple"]
    #Color_L=["red","orange","yellow","lime","green","cyan","blue","purple"]
    Color_L=["red","orange","yellow","greenyellow","green","deepskyblue","blue","purple"]
    Galaxy_Size_Scalers_L=list(np.arange(0, float(Galactic_Radius_Max)+Galactic_Radius_Step, Galactic_Radius_Step))
    i=0
    for column_name in LogN_LogC_Matrix.columns:
        #print(LogN_LogC_Matrix[column_name])
        #plt.step(Flux_Bins, LogN_LogC_Matrix[column_name], color="darkorange", where="post")
        #plt.plot(Flux_Bins, LogN_LogC_Matrix[column_name])
        #plt.plot(Flux_Bins, LogN_LogC_Matrix[column_name], color=Color_L[i])
        plt.plot(Flux_Bins, LogN_LogC_Matrix[column_name], color=Color_L[i], marker=".", label=Galaxy_Size_Scalers_L[i+1])
        plt.errorbar(Flux_Bins, LogN_LogC_Matrix[column_name], yerr=LogN_LogC_Error_Matrix[column_name], color=Color_L[i], linestyle='', alpha=0.5)
        #plt.plot(Flux_Bins, LogN_LogC_Matrix[column_name], marker=".", label=Galaxy_Size_Scalers_L[i+1])
        #plt.errorbar(Flux_Bins, LogN_LogC_Matrix[column_name], yerr=LogN_LogC_Error_Matrix[column_name], linestyle='', alpha=0.5)
        i=i+1
    #pyplot.yscale('log')
    plt.yscale('log')
    plt.xlim(0,30)
    plt.xlabel("Counts")
    plt.ylabel("N(>C)")
    plt.legend(title="D25 bin", loc='upper right')
    plt.title("Log(N)-Log(C)")
    #plt.savefig("Integrated_LogN_LogC_Test_Plot.pdf")
    plt.savefig("Integrated_LogN_LogC_Plot.pdf")

def Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas.csv', Alternative_Limiting_Flux_Areas_Path=None, Counts_Step=10, Galactic_Radius_Max=2.0, Galactic_Radius_Step=0.25, D25_Area_Bool=False, Flux_Bool=False):
    LogN_LogC_Tuple=LogN_LogC_Calc(Source_Count_Matrix_Path=Source_Count_Matrix_Path, Limiting_Flux_Areas_Path=Limiting_Flux_Areas_Path, Counts_Step=Counts_Step)
    if(D25_Area_Bool):
        LogN_LogC_Tuple_Standard=LogN_LogC_Calc(Source_Count_Matrix_Path=Source_Count_Matrix_Path, Limiting_Flux_Areas_Path=Alternative_Limiting_Flux_Areas_Path, Counts_Step=Counts_Step)
        Limiting_Flux_Areas_DF=pd.read_csv(Limiting_Flux_Areas_Path)
        Limiting_Flux_Areas_DF=Limiting_Flux_Areas_DF.iloc[::-1].cumsum().iloc[::-1]
        Alternative_Limiting_Flux_Areas_DF=pd.read_csv(Alternative_Limiting_Flux_Areas_Path)
        Alternative_Limiting_Flux_Areas_DF=Alternative_Limiting_Flux_Areas_DF.iloc[::-1].cumsum().iloc[::-1]
    LogN_LogC_Matrix=LogN_LogC_Tuple[0]
    #print("LogN_LogC_Matrix:\n", LogN_LogC_Matrix)
    LogN_LogC_Error_Matrix=LogN_LogC_Tuple[1]
    Matrix_Shape=LogN_LogC_Matrix.shape
    #Counts_L=list(range(0,Max_Counts+1,Counts_Step))
    #Galaxy_Size_Scalers_L=list(np.arange(0, float(Galactic_Radius_Max)+Galactic_Radius_Step, Galactic_Radius_Step))
    Flux_Bins=list(np.array(list(range(0,Matrix_Shape[0])))*Counts_Step)
    if(Flux_Bool):
        Flux_Bins=Flux_Array_Calc()
    print("Flux_Bins: ", Flux_Bins)
    #Color_L=["red","orange","yellow","green","lime","cyan","blue","purple"]
    #Color_L=["red","orange","yellow","lime","green","cyan","blue","purple"]
    ###Color_L=["red","orange","yellow","greenyellow","green","deepskyblue","blue","purple"]
    Color_L=["red","orange","yellow","greenyellow","red","orange","blue","purple"]
    Galaxy_Size_Scalers_L=list(np.arange(0, float(Galactic_Radius_Max)+Galactic_Radius_Step, Galactic_Radius_Step))
    Galaxy_Size_Scalers_L=Galaxy_Size_Scalers_L[1:]
    #Galaxy_Size_Scalers_L=Galaxy_Size_Scalers_L[:-1]
    print("Galaxy_Size_Scalers_L: ", Galaxy_Size_Scalers_L)
    LogN_LogC_Matrix_Transposed=LogN_LogC_Matrix.T
    print("LogN_LogC_Matrix_Transposed:\n", LogN_LogC_Matrix_Transposed)
    LogN_LogC_Error_Matrix_Transposed=LogN_LogC_Error_Matrix.T
    ###Cutoff_Index=int(2.0/Galactic_Radius_Step)
    Cutoff_Index=int(2.75/Galactic_Radius_Step)
    print("Cutoff_Index: ", Cutoff_Index)
    if(D25_Area_Bool):
        #LogN_LogC_Tuple_Standard[0]
        LogN_LogC_Matrix_Transposed_Background=LogN_LogC_Tuple_Standard[0].T.iloc[Cutoff_Index:]
    else:
        LogN_LogC_Matrix_Transposed_Background=LogN_LogC_Matrix_Transposed.iloc[Cutoff_Index:]
    print("LogN_LogC_Matrix_Transposed_Background: ", LogN_LogC_Matrix_Transposed_Background)
    i=0
    #i=2
    for column_name in LogN_LogC_Matrix_Transposed.columns:
        if(i>7):
            continue
        if((i>3) and (i<6)):
            #print(LogN_LogC_Matrix[column_name])
            #plt.step(Flux_Bins, LogN_LogC_Matrix[column_name], color="darkorange", where="post")
            #plt.plot(Flux_Bins, LogN_LogC_Matrix[column_name])
            #plt.plot(Flux_Bins, LogN_LogC_Matrix[column_name], color=Color_L[i])
            #plt.plot(Galaxy_Size_Scalers_L, LogN_LogC_Matrix_Transposed[column_name], color=Color_L[i], marker=".", label=Flux_Bins[i])
            ##plt.plot(Galaxy_Size_Scalers_L, LogN_LogC_Matrix_Transposed[column_name], marker=".", label=str(Flux_Bins[i])+"-"+str(Flux_Bins[i+1]))
            print("i: ", i)
            Format_String="{:." + str(0) + "e}"
            if(Flux_Bool):
                plt.plot(Galaxy_Size_Scalers_L, LogN_LogC_Matrix_Transposed[column_name], marker=".", color=Color_L[i], label=str(Format_String.format(Flux_Bins[i]))+" - "+str(Format_String.format(Flux_Bins[i+1])))
            else:
                plt.plot(Galaxy_Size_Scalers_L, LogN_LogC_Matrix_Transposed[column_name], marker=".", color=Color_L[i], label=str(Flux_Bins[i])+" - "+str(Flux_Bins[i+1]))
            #plt.plot(Galaxy_Size_Scalers_L, LogN_LogC_Matrix_Transposed[column_name], marker=".", label=str(Flux_Bins[i])+"-"+str(Flux_Bins[i+1]))
            #plt.plot(Galaxy_Size_Scalers_L, LogN_LogC_Matrix_Transposed[column_name]/((np.pi)*(1.0**2.0)), marker=".", color=Color_L[i], label=str(Flux_Bins[i])+"-"+str(Flux_Bins[i+1])) #For Testing
            #plt.step(Galaxy_Size_Scalers_L, LogN_LogC_Matrix_Transposed[column_name], marker=".", where="pre", label=Flux_Bins[i])
            ##plt.step(Galaxy_Size_Scalers_L, LogN_LogC_Matrix_Transposed[column_name], marker=".", where="post", label=Flux_Bins[i])
            #plt.errorbar(Galaxy_Size_Scalers_L, LogN_LogC_Matrix_Transposed[column_name], yerr=LogN_LogC_Error_Matrix_Transposed[column_name], color=Color_L[i], linestyle='', alpha=0.5)
            ###plt.errorbar(Galaxy_Size_Scalers_L, LogN_LogC_Matrix_Transposed[column_name], yerr=LogN_LogC_Error_Matrix_Transposed[column_name], linestyle='', alpha=0.5)
            ####plt.errorbar(Galaxy_Size_Scalers_L, LogN_LogC_Matrix_Transposed[column_name], yerr=LogN_LogC_Error_Matrix_Transposed[column_name], color=Color_L[i], linestyle='', alpha=0.5)
            #plt.errorbar(Galaxy_Size_Scalers_L, LogN_LogC_Matrix_Transposed[column_name], yerr=LogN_LogC_Error_Matrix_Transposed[column_name], alpha=1.0, label=Flux_Bins[i])
            Background_Density=LogN_LogC_Matrix_Transposed_Background[column_name].mean()
            Background_Density_Error=LogN_LogC_Matrix_Transposed_Background[column_name].std()
            if(D25_Area_Bool):
                print("Limiting_Flux_Areas_DF.T[column_name]:\n", Limiting_Flux_Areas_DF.T[column_name])
                ##Background_Density_A=Background_Density/(Limiting_Flux_Areas_DF.T[column_name])
                Background_Density_A=Background_Density*((Alternative_Limiting_Flux_Areas_DF.T[column_name])/(Limiting_Flux_Areas_DF.T[column_name]))
                #Background_Density_A=Background_Density_A*((np.pi)*((Galaxy_Size_Scalers_L[0])**2.0)) #For Testing
                #Background_Density_A=Background_Density_A/((np.pi)*(1.0**2.0)) #For Testing
                Background_Density_Error_A=Background_Density_Error*((Alternative_Limiting_Flux_Areas_DF.T[column_name])/(Limiting_Flux_Areas_DF.T[column_name]))
                #Background_Density_Error_A=Background_Density_Error_A/((np.pi)*(1.0**2.0)) #For Testing
                print("Background_Density_A: ", Background_Density_A)
                ##plt.plot(Galaxy_Size_Scalers_L, Background_Density_A, color=Color_L[i], linestyle='--')
                ##plt.errorbar(Galaxy_Size_Scalers_L, Background_Density_A, yerr=Background_Density_Error_A, color=Color_L[i], linestyle='', alpha=0.5)
                ##plt.errorbar(Galaxy_Size_Scalers_L, Background_Density_A, yerr=3.0*Background_Density_Error_A, color=Color_L[i], linestyle='', alpha=0.5)
                ##plt.errorbar(Galaxy_Size_Scalers_L, Background_Density_A, yerr=3.0*Background_Density_Error_A, color=Color_L[i], linestyle='-', alpha=0.5)
                plt.plot(Galaxy_Size_Scalers_L, Background_Density_A+(3.0*Background_Density_Error_A), color=Color_L[i], linestyle='--', alpha=0.5)
            else:
                plt.axhline(y=Background_Density, color=Color_L[i], linestyle='-.')
                plt.axhline(y=Background_Density+(3.0*Background_Density_Error), color=Color_L[i], linestyle='--', alpha=0.5)
                #plt.axhline(y=Background_Density-(3.0*Background_Density_Error), color=Color_L[i], linestyle='--', alpha=0.3)
                if(Flux_Bool):
                    pass
                    #Mean_Bin_Flux=(Flux_Bins[i]+Flux_Bins[i+1])
                    #Mean_Bin_Flux=(Flux_Bins[i+1]-Flux_Bins[i])/2.0
                    #Mean_Bin_Flux = 10.0**((np.log10(Flux_Bins[i+1])+np.log10(Flux_Bins[i]))/2)
                    #print(str(Flux_Bins[i])+" - "+str(Flux_Bins[i+1]))
                    #print("Mean_Bin_Flux: ", Mean_Bin_Flux)
                    #plt.axhline(y=Log_N_Log_S_Plotting.Key_Based_Integral_Form(Mean_Bin_Flux, "AGN", "H"), color=Color_L[i], linestyle=':')
                    #plt.axhline(y=Log_N_Log_S_Plotting.Key_Based_Integral_Form(Flux_Bins[i], "AGN", "H"), color=Color_L[i], linestyle=':')
                    Mean_Bin_Value=((integrate.quad(Log_N_Log_S_Plotting.Key_Based_Integral_Form, Flux_Bins[i], Flux_Bins[i+1], args=("AGN", "H")))/(Flux_Bins[i+1]-Flux_Bins[i]))[0]
                    print("Mean_Bin_Value: ", Mean_Bin_Value)
                    plt.axhline(y=Mean_Bin_Value, color=Color_L[i], linestyle=':', alpha=0.5)


        i=i+1
    #pyplot.yscale('log')
    plt.yscale('log')
    #plt.xlim(0,2)
    #plt.xticks(Galaxy_Size_Scalers_L[::2])
    ##plt.xticks(Galaxy_Size_Scalers_L[1::2])
    plt.xticks(Galaxy_Size_Scalers_L[1:])
    ##plt.xticks(Galaxy_Size_Scalers_L[1::2])
    plt.xlim(0.25,4)
    ##plt.xlim(0.125,4)
    #plt.xlim(0.125,3)
    ##plt.xlim(0.25,3)
    ##plt.xlim(0.25,2)
    #plt.xlim(1,4)
    #plt.ylim(900,3100)
    #plt.ylim(4,10**3.0)
    #plt.ylim(2,10**3.0)
    #plt.ylim(2,600)
    #plt.xlim(0.5,4)
    #plt.figure(figsize=(7, 4.8))
    #plt.xlim(Galaxy_Size_Scalers_L[0],Galaxy_Size_Scalers_L[-2])
    #plt.rcParams.update({"text.usetex": True, "font.family": "Helvetica"})
    ##plt.xlabel("Elliptical Radius (D25)")
    plt.xlabel("Elliptical Radius "+r"($D25$)")
    if(D25_Area_Bool):
        #plt.ylabel("N(>C) (D25^-2)")
        #plt.ylabel("N(>C) ($D25^{-2}$)")
        #plt.ylabel(r'$\sum_{i=0}^\infty x_i$')
        ##plt.ylabel("N(>C) "+r"($D25^{-2}$)")
        if(Flux_Bool):
            plt.ylabel("N(>S"+r"$_j$"+") "+r"($D25^{-2}$)")
        else:
            plt.ylabel("N(>C"+r"$_j$"+") "+r"($D25^{-2}$)")
        #plt.ylabel(r"$N(>C_j)$"+" "+r"$(D25^{-2})$")
    else:
        ##plt.ylabel("N(>C) (Deg^-2)")
        #plt.ylabel("N(>C) ($Deg^{-2}$)")
        ##plt.ylabel("N(>C) "+r"($Deg^{-2}$)")
        if(Flux_Bool):
            plt.ylabel("N(>S"+r"$_j$"+") "+r"($Deg^{-2}$)")
        else:
            plt.ylabel("N(>C"+r"$_j$"+") "+r"($Deg^{-2}$)")
    if(Flux_Bool):
        plt.legend(title="Limiting Flux "+r"($erg/s*cm^{-2}$)", loc='upper right')
    else:
        plt.legend(title="Count bin", loc='upper right')
    #plt.title("Log(N)-Log(R)")
    plt.title("Log(N)-r")
    #plt.savefig("Integrated_LogN_LogC_Test_Plot.pdf")
    #plt.savefig("Integrated_LogN_LogR_Plot.pdf")
    plt.savefig("Integrated_LogN_vs_R_Plot.pdf")
    plt.savefig("Integrated_LogN_vs_R_Plot.png")

def Main():
    Galaxy_List_Path=dir+"/../Galaxy_List/Galaxy_Names_Reduced_Homogeneous_Resolved_Unique_with_10ks_Exposure_Cut.csv"
    Galaxy_List_DF=pd.read_csv(Galaxy_List_Path)
    #print("Galaxy_List_DF:\n", Galaxy_List_DF)
    #Galaxy_Name_Reduced
    Galaxy_List_A=Galaxy_List_DF["Galaxy_Name_Reduced"]
    #print("Galaxy_List_A:\n", Galaxy_List_A)
    Gname_L=list(Galaxy_List_A)
    #MESSIER 051
    print("len(Gname_L): ", len(Gname_L))
    Gname_L.remove("MESSIER 051") #Note: This needs to be removed because it has no D25 value!!!
    Bad_List=['NGC 4485','MESSIER 105','NGC 3377','NGC 4565','NGC 4473','MESSIER 090','NGC 2841','NGC 3998','Holmberg IX','NGC 4625','NGC 2903','NGC 2683','NGC 3384','NGC 7457','NGC 4861','NGC 4088','NGC 4417','MRK 0750','NGC 3344','NGC 4550','NGC 4551','NGC 1404','MESSIER 049','NGC 4302','NGC 3287','MESSIER 096']
    print("len(Bad_List): ", len(Bad_List))
    ##Very_Bad_List=['NGC 4485','MESSIER 105','NGC 3377','MESSIER 090','NGC 3998','Holmberg IX','NGC 4625','NGC 3384','NGC 4550','NGC 4551','NGC 4302']
    Gname_L_First_Reduced=[]
    for Gname in Gname_L:
        if(Gname not in Bad_List):
            Gname_L_First_Reduced.append(Gname)
    Gname_L=Gname_L_First_Reduced
    print("Gname_L: ", Gname_L)
    print("len(Gname_L): ", len(Gname_L))
    """
    Data=pd.read_csv(dir+"/../SQL_Standard_File/Source_Flux_All_Modified_6.csv")
    Data_Galaxies=Data.drop_duplicates(subset=['Gname_Homogenized'])
    print("Data_Galaxies: ", Data_Galaxies)
    #Data_Galaxies_Filtered=Data_Galaxies[Data_Galaxies['D25']<=5.0]
    #Data_Galaxies_Filtered=Data_Galaxies[Data_Galaxies['D25']<=6.666666]
    #Data_Galaxies_Filtered=Data_Galaxies[Data_Galaxies['D25']>=10.0]
    #print("Data_Galaxies_Filtered: ", Data_Galaxies_Filtered)
    #Area_Merged_All_A_Deg=Merged_Area_Calc_Galaxy_L(Gname_L)
    """
    ##print(Merged_Area_Calc_Galaxy_L(Gname_L))
    #Galactic_Radius_Max=4.0
    ##print(Merged_Area_Calc_Galaxy_L(Gname_L, Galactic_Radius_Max=4.0, Galactic_Radius_Step=0.125))
    ###print(Merged_Area_Calc_Galaxy_L(Gname_L, Galactic_Radius_Max=4.0))
    ##print(Merged_Area_Calc_Galaxy_L(Gname_L, Max_Counts=30, Galactic_Radius_Max=4.0, Galactic_Radius_Step=0.5))
    #D25_Area_Bool=True
    ###print(Merged_Area_Calc_Galaxy_L(Gname_L, Galactic_Radius_Max=4.0, D25_Area_Bool=True))
    #print(Merged_Area_Calc_Galaxy_L(Gname_L, Max_Counts=30, Counts_Step=5, Galactic_Radius_Max=4.0))
    ##print(Merged_Area_Calc_Galaxy_L(Gname_L, Max_Counts=30, Counts_Step=1, Galactic_Radius_Max=4.0))
    ##print(Merged_Area_Calc_Galaxy_L(Gname_L, Galactic_Radius_Max=4.0, Flux_Bool=True))

    Fail_List=["NGC 4945", "UGC 06456", "NGC 4395", "NGC 4111", "NGC 4559", "NGC 4051", "NGC 7331", "MESSIER 102", "NGC 5204", "MESSIER 100", "NGC 4026", "NGC 3621", "MESSIER 081 DWARF A", "NGC 5408", "NGC 4178", "WISEA J024656.39-003305.0"]
    #Fail_List_D25=["NGC 4945", "UGC 06456", "NGC 4395", "NGC 4111", "NGC 4559", "NGC 4051", "NGC 7331", "MESSIER 102", "NGC 5204", "MESSIER 100", "NGC 4026", "NGC 3621", "MESSIER 081 DWARF A", "NGC 5408", "NGC 4178", "WISEA J024656.39-003305.0"]
    #print(Merged_Area_Calc_Galaxy_L(Fail_List))
    #print(Merged_Area_Calc_Galaxy_L(["NGC 4945"])) #Note: Background outside of simulation range!
    #print(Merged_Area_Calc_Galaxy_L(["UGC 06456"])) #Note: There are no valid observations for UGC 06456. It should not be in the sample.
    #print(Merged_Area_Calc_Galaxy_L(["NGC 4395"])) #Note: There are no valid observations for NGC 4395. It should not be in the sample.
    #print(Merged_Area_Calc_Galaxy_L(["NGC 4111"])) #Note: There are no valid observations for NGC 4111. It should not be in the sample.
    #print(Merged_Area_Calc_Galaxy_L(["NGC 4559"])) #Note: There are no valid observations for NGC 4559. It should not be in the sample.
    #print(Merged_Area_Calc_Galaxy_L(["NGC 4051"])) #Note: There are no valid observations for NGC 4051. It should not be in the sample.
    #print(Merged_Area_Calc_Galaxy_L(["NGC 7331"])) #Note: There are no valid observations for NGC 7331. It should not be in the sample.
    #print(Merged_Area_Calc_Galaxy_L(["MESSIER 102"])) #Note: There are no valid observations for MESSIER 102. It should not be in the sample.
    #print(Merged_Area_Calc_Galaxy_L(["NGC 5204"])) #Note: There are no valid observations for NGC 5204. It should not be in the sample.
    #print(Merged_Area_Calc_Galaxy_L(["MESSIER 100"])) #Note: There are no valid observations for MESSIER 100. It should not be in the sample.
    #print(Merged_Area_Calc_Galaxy_L(["NGC 4026"])) #Note: There are no valid observations for NGC 4026. It should not be in the sample.
    #print(Merged_Area_Calc_Galaxy_L(["NGC 3621"])) #Note: There are no valid observations for NGC 3621. It should not be in the sample.
    #print(Merged_Area_Calc_Galaxy_L(["MESSIER 081 DWARF A"])) #Note: Astroquery Failure
    #print(Merged_Area_Calc_Galaxy_L(["NGC 5408"])) #Note: There are no valid observations for NGC 5408. It should not be in the sample.
    #print(Merged_Area_Calc_Galaxy_L(["NGC 4178"])) #Note: There are no valid observations for NGC 4178. It should not be in the sample.
    ##print(Merged_Area_Calc_Galaxy_L(["WISEA J024656.39-003305.0"]))

    #"""
    Gname_L_Reduced=[]
    for Gname in Gname_L:
        if(Gname not in Fail_List):
            Gname_L_Reduced.append(Gname)
    print("Gname_L_Reduced: ", Gname_L_Reduced)
    print("len(Gname_L_Reduced): ", len(Gname_L_Reduced))
    #"""
    ###print(Source_Count_Matrix_Calc(Gname_L_Reduced))
    ##print(Source_Count_Matrix_Calc(Gname_L_Reduced, Galactic_Radius_Max=4.0, Galactic_Radius_Step=0.125))
    ###print(Source_Count_Matrix_Calc(Gname_L_Reduced, Galactic_Radius_Max=4.0))
    #print(Source_Count_Matrix_Calc(Gname_L_Reduced, Max_Counts=30, Galactic_Radius_Max=4.0, Galactic_Radius_Step=0.5))
    ##print(Source_Count_Matrix_Calc(Gname_L_Reduced, Max_Counts=30, Counts_Step=5, Galactic_Radius_Max=4.0))
    ##print(Source_Count_Matrix_Calc(Gname_L_Reduced, Max_Counts=30, Counts_Step=1, Galactic_Radius_Max=4.0))
    ##print(Source_Count_Matrix_Calc(Gname_L_Reduced, Galactic_Radius_Max=4.0, Flux_Bool=True))



#print(Background_Calc('NGC 3077'))
#print(Limiting_Flux_Intersected_Region_Calc('NGC 3077', Max_Counts=30))
#print(Limiting_Flux_Intersected_Region_Calc(2076, Max_Counts=30))
#print(Limiting_Flux_Intersected_Region_Calc(2076, Max_Counts=100))
#print(len(Limiting_Flux_Intersected_Region_Calc(2076, Max_Counts=100)[0]))
#Region_Test()
#print(Close_ObsIDs_Query(2076))
#print(Overlapping_ObsIDs_Calc(2076))
#print(Overlapping_ObsIDs_Calc(10125))
#print(Galactic_Limiting_Flux_Intersected_Region_Calc("NGC 4449"))
#print(Aimpoint_Distance_Calc(10125, 2031))
#print(Aimpoint_Offset_Calc(10125, 2031))
#Pickle_Test()
#print(Merged_Area_Calc("NGC 4449"))
#print(Merged_Area_Calc("NGC 4449", D25_Area_Bool=True))
#Save_FOV1_Region(10125,2031)
#print(Merged_Area_Calc("NGC 3077"))
#print(Merged_Area_Calc_Galaxy_L(["NGC 4449","NGC 3077"]))
##print(Merged_Area_Calc_Galaxy_L(["NGC 4449","NGC 3077"], D25_Area_Bool=True))
#print(Merged_Area_Calc_Galaxy_L(["NGC 4449"], D25_Area_Bool=True))
#print(Merged_Area_Calc_Galaxy_L(["NGC 4449","NGC 3077"], Galactic_Radius_Max=4.0))
##print(Merged_Area_Calc_Galaxy_L(["NGC 4449","NGC 3077"], Galactic_Radius_Max=4.0, Flux_Bool=True))
#print(Theta_Intersection_Calc(10125))
#print(Source_Flux_Area_Calc(10125,1))
#print(Source_Flux_Area_Calc(10125,2))
#print(Source_Flux_Area_Calc(10125,15))
#print(Source_Flux_Area_Calc_Bulk(10125))
#print(Source_Flux_Area_Calc_Galaxy_Bulk(["NGC 4449","NGC 3077"]))
#print(Source_Flux_Area_Calc_Galaxy_Bulk(["NGC 4449","NGC 3077"], Flux_Bool=True))
#NGC 5128
#print(Source_Flux_Area_Calc_Galaxy_Bulk(["NGC 5128"]))

#Source_Flux_Area_HL=[['NGC 5128', [[316, [(None, 3), (None, 3), (None, 3), (2, 2), (None, 1), (2, 2), (None, 3), (2, 1), (None, None), (2, 1), (None, 1), (None, 1), (1, 1), (2, 1), (None, 2), (1, 1), (None, None), (None, 2), (1, 1), (1, 2), (1, 2), (None, None), (None, 2), (None, None), (2, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 2), (2, 1), (1, 1), (2, 1), (1, 0), (1, 0), (1, 1), (1, 0), (None, 3), (2, 0), (1, 1), (1, 0), (1, 2), (1, 0), (1, 0), (1, 1), (1, 2), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (0, 0), (2, 1), (0, 0), (0, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 3), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 0), (1, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 0), (1, 3), (1, 2), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 1), (2, 1), (2, 1), (1, 0), (2, 1), (2, 1), (1, 0), (None, 1), (None, 1), (1, 0), (1, 0), (None, 1), (None, 1), (1, 0), (1, 0), (0, 0), (1, 0), (None, None), (1, 0), (1, 0), (0, 1), (2, 1), (1, 3), (1, 0), (1, 0), (0, 0), (1, 0), (None, 1), (1, 0), (1, 0), (None, None), (0, 0), (None, None), (0, 1), (0, 0), (1, 0), (1, 2), (0, 0), (0, 0), (0, 0), (1, 0), (0, 0), (0, 0), (2, 1), (1, 1), (0, 0), (1, 0), (1, 1), (0, 0), (0, 1), (0, 0), (0, 1), (1, 3), (1, 0), (2, 1), (1, 0), (1, 1), (0, 0), (0, 1), (1, 3), (None, None), (0, 1), (0, 1), (None, None), (0, 1), (0, 2), (None, None), (None, 3), (None, None), (None, None), (1, 2), (1, 1), (0, 1), (1, 1), (1, 3), (1, 1), (1, 3), (None, None), (1, 2), (2, 2), (None, None), (0, 1), (0, 1), (1, 1), (1, 1), (2, 2), (0, 2), (None, None), (1, 2), (0, 2), (2, 2), (None, 4), (2, 3), (None, None), (None, None), (1, 2), (None, 4), (1, 3), (2, 3), (1, 3), (2, 3), (None, None), (2, 3), (1, 3), (1, 3), (None, None), (None, 3), (2, 3), (None, 3), (None, None), (None, 4), (None, 3)]], [962, [(None, 3), (None, 3), (2, 2), (None, 3), (None, 3), (None, 4), (1, 2), (None, 4), (1, 1), (None, 3), (1, 2), (1, 1), (None, 4), (None, 3), (1, 1), (None, None), (1, 1), (1, 1), (1, 2), (1, 1), (1, 2), (1, 2), (None, None), (1, 3), (1, 1), (None, 5), (1, 1), (1, 1), (1, 1), (2, 1), (2, 1), (1, 0), (1, 2), (2, 1), (1, 1), (1, 0), (2, 1), (1, 1), (1, 1), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 0), (None, 1), (1, 0), (1, 0), (1, 0), (0, 0), (1, 0), (0, 1), (1, 1), (1, 0), (1, 0), (1, 0), (0, 0), (2, 1), (0, 0), (0, 0), (0, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 0), (0, 0), (0, 1), (0, 0), (0, 0), (0, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 0), (1, 3), (0, 0), (0, 0), (0, 0), (0, 1), (0, 0), (0, 1), (0, 0), (0, 0), (1, 0), (1, 2), (0, 0), (0, 0), (0, 0), (0, 0), (1, 0), (1, 0), (0, 0), (1, 0), (1, 3), (0, 0), (None, 3), (1, 2), (1, 0), (1, 0), (0, 0), (1, 0), (1, 0), (0, 0), (1, 0), (1, 0), (None, None), (0, 0), (0, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 1), (0, 0), (None, None), (1, 2), (1, 0), (0, 0), (1, 0), (1, 0), (1, 0), (None, 4), (1, 0), (None, None), (1, 0), (1, 0), (1, 3), (None, None), (1, 0), (1, 0), (1, 0), (1, 0), (None, None), (None, None), (1, 0), (1, 0), (None, None), (1, 0), (None, None), (1, 0), (0, 0), (1, 0), (0, 1), (0, 1), (0, 0), (1, 0), (0, 1), (0, 1), (1, 1), (0, 1), (None, 4), (1, 0), (0, 0), (2, 1), (None, None), (1, 0), (None, None), (None, None), (0, 1), (None, None)]], [2978, [(None, 3), (1, 2), (None, 3), (None, 3), (None, 3), (1, 2), (1, 1), (None, 2), (None, None), (2, 2), (1, 1), (1, 2), (1, 2), (1, 1), (1, 1), (2, 2), (1, 2), (1, 1), (0, 1), (1, 2), (1, 1), (1, 2), (None, 2), (1, 2), (None, 2), (2, 2), (0, 1), (1, 1), (1, 1), (1, 1), (0, 1), (2, 2), (1, 2), (1, 1), (0, 1), (1, 1), (None, None), (1, 1), (1, 1), (None, None), (1, 1), (1, 1), (0, 0), (1, 1), (0, 1), (1, 1), (0, 0), (1, 0), (0, 0), (1, 0), (1, 0), (0, 0), (1, 0), (1, 0), (0, 0), (0, 0), (0, 0), (1, 0), (0, 0), (1, 0), (0, 0), (None, 3), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 1), (0, 0), (0, 0), (0, 0), (1, 1), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 1), (0, 0), (0, 0), (1, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 0), (1, 1), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (None, 3), (1, 1), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 0), (0, 0), (0, 0), (0, 0), (1, 1), (0, 0), (0, 0), (1, 0), (1, 0), (0, 0), (0, 0), (0, 0), (1, 1), (0, 0), (1, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 1), (1, 1), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 0), (0, 0), (0, 0), (None, None), (1, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 1), (0, 0), (0, 0), (1, 1), (0, 0), (None, 3), (0, 0), (0, 0), (1, 0), (0, 0), (0, 0), (None, None), (1, 0), (0, 0), (1, 0), (0, 0), (1, 0), (1, 0), (0, 0), (1, 1), (1, 0), (0, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 1), (0, 0), (1, 0), (1, 0), (1, 1), (1, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, 1), (1, 0), (1, 0), (1, 1), (1, 1), (1, 0), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 0), (1, 1), (1, 0), (1, 0), (1, 1), (1, 1), (1, 1), (None, None), (1, 1), (None, None), (1, 1), (1, 1), (1, 1), (1, 1), (None, 2), (1, 1), (1, 1), (1, 1), (None, None), (None, None), (None, None), (1, 1), (1, 1), (1, 1), (None, 2), (None, None), (None, None), (None, 3)]], [3965, [(None, 3), (None, 3), (None, 3), (1, 2), (None, 3), (2, 2), (1, 1), (None, 2), (1, 1), (1, 2), (1, 1), (1, 1), (1, 1), (1, 1), (1, 2), (1, 1), (1, 2), (1, 2), (2, 2), (1, 2), (2, 2), (0, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (0, 1), (1, 1), (1, 1), (1, 2), (2, 2), (1, 1), (1, 0), (0, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (0, 0), (1, 1), (1, 1), (1, 1), (0, 1), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (None, 3), (0, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, 3), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (None, 3), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, None), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 1), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, 1), (1, 0), (1, 0), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 0), (1, 1), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (None, 2), (1, 1), (1, 1), (1, 1), (1, 1), (None, 2), (1, 1), (1, 1), (1, 1), (None, 2), (1, 1), (2, 1), (1, 1), (None, None), (None, None), (2, 1), (2, 2), (None, 2), (2, 2), (None, None), (None, None)]], [7797, [(None, 3), (None, 3), (None, 3), (None, 3), (None, 3), (None, 4), (None, 4), (2, 3), (2, 3), (None, 3), (2, 3), (2, 2), (None, 4), (1, 2), (None, 3), (1, 2), (2, 3), (None, 3), (None, 3), (2, 3), (1, 1), (None, None), (None, 4), (2, 2), (None, 3), (None, 4), (1, 2), (1, 1), (2, 3), (None, 3), (1, 1), (1, 2), (1, 2), (1, 2), (1, 1), (1, 1), (2, 3), (1, 2), (1, 1), (None, 4), (None, 3), (1, 1), (1, 1), (1, 1), (2, 2), (1, 2), (1, 1), (1, 1), (1, 2), (1, 1), (2, 3), (1, 2), (None, 2), (1, 2), (1, 1), (1, 1), (2, 2), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (None, 2), (1, 2), (1, 0), (1, 1), (1, 1), (1, 0), (1, 1), (1, 1), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, 1), (1, 1), (1, 1), (1, 0), (1, 0), (2, 1), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, 5), (None, 3), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (None, 4), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, 3), (1, 0), (1, 0), (None, None), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (None, None), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, 3), (1, 0), (1, 0), (None, 3), (1, 2), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (1, 1), (1, 0), (None, 3), (1, 0), (2, 2), (1, 0), (1, 0), (1, 0), (None, 4), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (None, 3), (1, 0), (None, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (None, 4), (1, 0), (1, 0), (2, 1), (2, 1), (1, 0), (2, 1), (None, 3), (2, 2), (1, 0), (1, 1), (2, 2), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (None, 3), (None, None), (1, 1), (2, 1), (2, 1), (None, 3), (2, 2), (2, 2), (2, 1), (2, 1), (1, 1), (None, 2), (None, 2), (2, 1), (1, 1), (2, 1), (None, 3), (None, 2), (1, 1), (None, 3), (2, 2), (None, 1), (2, 2), (2, 1), (1, 1), (2, 1), (None, 1), (2, 1), (1, 1), (None, 2), (2, 1), (2, 2), (2, 1), (2, 2), (2, 1), (2, 1), (2, 2), (None, 1), (None, 4), (None, 1), (None, 1), (None, 1), (2, 1), (None, 1), (2, 1), (None, 2), (None, 2), (None, 3), (None, 2), (None, 2), (None, None), (None, 2), (None, 4), (None, 3), (None, 4), (None, 2), (None, None), (None, None), (None, None), (None, 4)]], [7798, [(None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 0), (None, 0), (None, 1), (None, 1), (2, 0), (2, 0), (2, 0), (None, 1), (None, 1), (2, 0), (2, 1), (2, 0), (2, 1), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (None, 1), (2, 1), (2, 0), (2, 0), (2, 1), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 1), (2, 0), (2, 0), (2, 0), (1, 0), (2, 0), (1, 0), (2, 0), (2, 0), (None, 2), (1, 0), (None, 1), (1, 0), (1, 0), (None, 1), (2, 1), (2, 0), (2, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (None, 3), (1, 0), (1, 0), (None, 2), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (2, 1), (1, 0), (1, 0), (None, 2), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, 4), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (2, 1), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (None, None)]], [7799, [(None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 0), (None, 0), (None, 1), (None, 1), (2, 0), (2, 0), (None, 1), (None, 1), (2, 1), (2, 1), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (None, 1), (2, 0), (2, 1), (2, 0), (2, 0), (2, 1), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 1), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (1, 0), (2, 0), (2, 0), (2, 0), (1, 0), (1, 0), (None, 1), (None, 1), (2, 1), (2, 0), (2, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, 3), (1, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (2, 1), (1, 0), (None, 2), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (2, 1), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, None), (2, 1), (1, 0), (None, 4), (1, 0), (1, 0), (1, 1), (1, 1), (1, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 1), (None, 2), (2, 1), (1, 0), (1, 1), (1, 0), (None, 2), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (None, 3), (1, 0), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (2, 2), (None, 3), (None, 2), (1, 1), (1, 1), (2, 1), (None, 3), (1, 1), (2, 2), (1, 1), (None, None), (1, 1), (1, 1), (None, 3), (2, 2), (1, 1), (1, 1), (None, 3), (None, None), (1, 1), (2, 2), (None, None), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (None, 3), (1, 1), (1, 1), (1, 1), (1, 2), (1, 1), (1, 2), (1, 1), (1, 1), (2, 2), (1, 1), (None, None), (1, 1), (1, 1), (1, 1), (2, 2), (None, None), (None, 4), (1, 1), (1, 2), (1, 1), (1, 1), (1, 1), (1, 2), (1, 2), (1, 2), (None, None), (2, 3), (1, 2), (1, 2), (None, None), (None, 4), (2, 3), (None, 3), (None, 4), (None, 4), (1, 2), (1, 2), (1, 2), (None, 4), (1, 2), (1, 2), (None, 3), (None, 3), (None, None), (1, 3), (None, 4), (1, 3), (2, 3), (2, 3), (1, 3), (1, 3), (None, 5), (2, 3), (1, 3), (None, 5), (None, 3), (None, 4), (2, 3), (None, 4), (2, 3), (None, 3), (None, 3), (2, 3), (None, None), (2, 3), (2, 4), (2, 3), (2, 3), (None, 4), (None, 4), (None, 4), (None, 4), (None, 5), (None, 5), (None, 5)]], [7800, [(None, 1), (None, 2), (None, 1), (None, 1), (None, 1), (None, 1), (None, 2), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (2, 1), (None, 1), (None, 1), (None, 2), (None, 1), (None, 2), (None, 2), (None, 1), (None, 2), (None, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (None, 2), (2, 0), (2, 1), (2, 0), (2, 0), (2, 1), (None, 1), (2, 0), (2, 0), (None, 1), (2, 0), (None, 1), (2, 1), (2, 1), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 1), (2, 0), (2, 0), (2, 2), (2, 0), (2, 0), (None, 1), (2, 0), (2, 0), (2, 1), (2, 2), (None, 3), (2, 0), (2, 0), (2, 0), (2, 0), (1, 1), (2, 0), (2, 0), (2, 0), (2, 0), (1, 0), (2, 0), (None, 1), (2, 0), (2, 0), (2, 0), (2, 0), (1, 0), (None, 3), (1, 0), (None, None), (2, 0), (2, 0), (None, 1), (1, 0), (1, 0), (2, 0), (2, 0), (2, 0), (1, 0), (1, 0), (None, 3), (1, 0), (None, None), (2, 2), (None, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (2, 0), (1, 1), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (2, 1), (1, 0), (None, 3), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (2, 0), (None, 1), (1, 0), (None, None), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 1), (2, 1), (2, 2), (2, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, None), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (None, 1), (1, 0), (1, 0), (1, 1), (1, 1), (1, 0), (1, 0), (1, 1), (1, 1), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (None, None), (None, None), (1, 0), (1, 1), (1, 1), (1, 0), (2, 2), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (None, 2), (2, 3), (1, 1), (1, 1), (1, 2), (1, 1), (1, 1), (1, 1), (1, 2), (2, 1), (1, 1), (None, 2), (2, 2), (1, 1), (None, 2), (1, 1), (1, 1), (1, 1), (1, 1), (None, None), (2, 3), (2, 1), (2, 3), (1, 2), (2, 2), (2, 2), (None, 3), (1, 2), (1, 1), (None, 2), (1, 1), (1, 2), (1, 1), (1, 1), (1, 2), (1, 1), (None, None), (1, 1), (None, None), (1, 2), (2, 2), (1, 2), (2, 2), (None, 3), (1, 2), (2, 2), (None, 3), (2, 2), (1, 2), (1, 2), (None, 4), (1, 2), (None, None), (None, 3), (None, None), (1, 2), (2, 3), (None, None), (2, 3), (2, 3), (None, 3), (None, None), (2, 3), (2, 3), (None, 5), (2, 3), (2, 3), (None, 3), (None, 5), (None, None), (None, None), (2, 3), (None, 3), (None, 4), (2, 3), (None, 3), (2, 3), (2, 3), (None, 4), (None, 3), (None, 4), (None, 4), (None, 4), (None, 4)]], [8489, [(None, 4), (None, 3), (None, 3), (None, 2), (None, 2), (None, 2), (2, 2), (None, 2), (None, 3), (None, 2), (None, 3), (None, 1), (2, 1), (None, 2), (None, 4), (None, 2), (None, 2), (2, 1), (None, 3), (2, 1), (None, 1), (None, 1), (2, 1), (2, 2), (None, 1), (2, 1), (2, 1), (None, 4), (2, 1), (2, 2), (2, 1), (2, 1), (None, 2), (2, 2), (2, 1), (2, 2), (2, 1), (2, 1), (2, 1), (None, 1), (2, 1), (2, 2), (2, 1), (2, 1), (2, 1), (None, 3), (2, 1), (2, 2), (1, 1), (None, 1), (None, 2), (2, 1), (2, 1), (2, 2), (2, 1), (None, 2), (1, 1), (2, 2), (2, 1), (1, 1), (1, 1), (2, 1), (2, 1), (1, 1), (2, 1), (2, 2), (1, 0), (1, 1), (2, 1), (1, 1), (1, 0), (1, 0), (2, 1), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (None, None), (1, 0), (1, 1), (2, 1), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (None, 2), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (2, 1), (None, None), (1, 0), (None, 2), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (None, 4), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, 3), (1, 0), (1, 0), (1, 0), (None, None), (1, 0), (None, None), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (2, 2), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, 4), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, 3), (1, 0), (2, 2), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 1), (1, 0), (1, 0), (2, 2), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, 4), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (None, 3), (2, 1), (1, 0), (2, 1), (1, 1), (1, 0), (1, 0), (None, None), (1, 0), (1, 1), (1, 0), (None, None), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, None), (1, 0), (1, 0), (1, 1), (None, 4), (1, 0), (1, 0), (2, 1), (1, 1), (1, 0), (1, 1), (1, 1), (2, 1), (None, 3), (2, 2), (1, 1), (None, None), (1, 1), (2, 2), (1, 0), (1, 1), (1, 0), (1, 1), (None, 3), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (2, 2), (None, 3), (2, 2), (1, 1), (None, 3), (1, 1), (1, 1), (None, 3), (1, 1), (2, 1), (None, 3), (2, 1), (2, 2), (1, 1), (1, 1), (1, 1), (1, 1), (None, 3), (1, 2), (None, None), (None, 3), (2, 2), (None, None), (1, 1), (1, 1), (None, 3), (1, 1), (2, 2), (2, 3), (2, 2), (None, 3), (2, 3), (None, 3), (None, None), (None, None), (None, None), (None, 4), (None, 4), (None, 5), (None, 6)]], [8490, [(None, 3), (None, 4), (None, None), (None, 3), (None, 3), (None, 3), (None, 2), (2, 3), (None, 2), (None, 4), (None, 4), (None, 4), (None, 4), (None, None), (2, 3), (2, 3), (2, 2), (2, 3), (None, 4), (None, 4), (2, 2), (2, 2), (None, 2), (2, 2), (None, None), (2, 2), (1, 2), (2, 3), (1, 2), (2, 3), (None, 2), (None, 3), (1, 2), (2, 2), (2, 3), (2, 3), (1, 2), (2, 1), (None, 4), (2, 2), (None, 4), (1, 2), (1, 1), (None, None), (None, 2), (2, 3), (2, 1), (None, 2), (2, 3), (1, 1), (1, 1), (1, 2), (1, 1), (1, 2), (None, 4), (1, 2), (1, 1), (None, 3), (1, 1), (1, 1), (2, 2), (1, 2), (1, 1), (1, 1), (None, 1), (1, 2), (1, 2), (None, None), (2, 2), (2, 1), (None, None), (2, 3), (1, 2), (1, 2), (None, 1), (1, 2), (2, 2), (1, 1), (1, 2), (2, 1), (1, 1), (1, 1), (2, 1), (2, 1), (1, 1), (None, None), (1, 2), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (1, 1), (1, 1), (2, 2), (1, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, 1), (1, 0), (None, 2), (1, 0), (1, 0), (None, 1), (2, 1), (1, 0), (1, 0), (None, 1), (1, 0), (None, 1), (1, 0), (1, 0), (1, 0), (None, 1), (1, 0), (None, 1), (1, 0), (2, 1), (1, 0), (2, 1), (1, 0), (2, 1), (1, 0), (2, 1), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (2, 1), (2, 1), (2, 1), (None, 2), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (2, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (2, 0), (2, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (None, None), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (2, 3), (1, 0), (1, 0), (1, 1), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (None, None), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, 3), (2, 2), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (2, 0), (1, 0), (1, 0), (1, 0), (None, 1), (1, 1), (1, 0), (1, 0), (2, 2), (1, 0), (2, 0), (1, 0), (1, 0), (1, 0), (1, 1), (2, 0), (2, 0), (None, 3), (1, 0), (None, 1), (1, 0), (1, 1), (2, 0), (1, 1), (None, None), (1, 0), (1, 0), (1, 0), (2, 0), (2, 0), (1, 1), (1, 0), (2, 0), (None, 1), (2, 1), (1, 1), (None, None), (None, 1), (None, 3), (1, 1), (1, 0), (2, 2), (1, 1), (2, 0), (None, 3), (2, 1), (2, 2), (2, 2), (2, 1), (None, 3), (None, 1), (2, 1), (None, 3), (None, 2), (2, 1), (None, 3), (None, 1), (None, 1), (2, 2), (2, 1), (None, 1), (None, 1), (None, None), (2, 1), (None, 2), (2, 2), (None, None), (None, None), (2, 2), (None, 1), (2, 1), (None, 3), (None, 1), (None, 2), (None, 3), (None, 2), (None, None), (None, 4), (None, 3), (None, 4), (None, 4)]], [10722, [(None, 4), (1, 2), (1, 2), (None, 3), (None, 3), (None, 3), (2, 2), (1, 1), (1, 1), (1, 2), (1, 1), (1, 1), (2, 2), (1, 1), (1, 1), (1, 2), (2, 1), (None, None), (1, 2), (1, 2), (2, 2), (1, 1), (1, 1), (1, 1), (None, None), (2, 1), (1, 1), (2, 1), (None, None), (2, 1), (2, 2), (2, 1), (1, 1), (2, 1), (1, 1), (1, 1), (0, 0), (1, 1), (2, 1), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 1), (1, 0), (1, 0), (1, 0), (None, None), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, None), (1, 0), (1, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, None), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (2, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (None, 2), (1, 0), (1, 0), (1, 1), (1, 1), (1, 0), (1, 1), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (2, 1), (1, 1), (2, 1), (1, 0), (1, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (1, 0), (2, 1), (1, 1), (2, 1), (1, 0), (1, 1), (2, 1), (1, 1), (2, 1), (2, 1), (2, 1), (None, None), (None, 2), (2, 1), (3, 1), (2, 1), (None, 2), (2, 1), (None, None), (None, None), (None, None), (None, 2), (2, 1), (None, 2), (3, 1), (3, 1), (None, None), (None, None), (None, None), (None, None), (None, 4)]], [15200, [(None, None), (1, None), (None, None), (None, None), (None, None), (1, None), (None, None), (None, None), (None, None), (None, None), (0, None), (0, None), (None, None), (None, None), (1, None), (None, None), (None, None), (None, None), (1, None), (None, None), (None, None), (None, None), (None, None), (0, None), (0, None), (None, None), (None, None), (None, None), (None, None), (None, None), (1, None), (None, None), (None, None), (1, None), (None, None), (1, None), (1, None), (None, None), (1, None), (1, None), (2, None), (None, None), (None, None)]], [19521, [(None, 3), (None, 2), (None, 1), (0, 1), (0, 1), (None, 1), (0, 1), (1, 1), (None, 2), (0, 1), (1, 1), (0, 1), (0, 1), (0, 1), (1, 1), (0, 1), (None, None), (0, 0), (None, None), (1, 0), (0, 0), (1, 0), (None, None), (1, 0), (None, None), (0, 0), (None, None), (1, 1), (None, None), (0, 0), (0, 0), (0, 0), (0, 0), (None, None), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (None, None), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (None, None), (0, 0), (0, 0), (1, 0), (0, 0), (0, 0), (None, None), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (None, None), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (None, None), (0, 0), (1, 0), (0, 0), (1, 0), (1, 0), (None, None), (None, None), (0, 0), (0, 0), (1, 1), (0, 0), (0, 0), (1, 1), (0, 0), (0, 0), (None, None), (0, 0), (None, None), (None, None), (1, 0), (1, 0), (1, 1), (None, None), (None, None), (None, None), (1, 0), (1, 1), (1, 1), (1, 1), (None, None), (1, 1), (None, None), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (None, None), (1, 1), (None, None), (1, 1), (None, 3)]], [20585, [(None, 3), (None, 3), (None, 4), (None, 1), (None, 4), (None, 1), (None, 3), (None, 1), (None, 1), (None, 1), (None, 1), (2, 2), (None, 1), (None, 1), (None, 1), (None, 1), (2, 1), (2, 2), (2, 2), (2, 2), (2, 2), (2, 1), (2, 0), (2, 1), (2, 0), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 0), (2, 1), (2, 1), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (None, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (None, None), (2, 0), (2, 1), (2, 0), (2, 1), (2, 0), (None, 0), (2, 0), (None, None), (None, None), (None, 0), (2, 0), (2, 0), (1, 2), (2, 0), (None, None), (2, 0), (2, 0), (2, 0), (1, 1), (2, 0), (2, 0), (1, 1), (2, 0), (1, 2), (2, 0), (1, 0), (1, 1), (2, 0), (2, 0), (2, 0), (2, 4), (1, 1), (1, 0), (1, 2), (1, 1), (1, 2), (2, 0), (1, 1), (1, 1), (1, 2), (1, 2), (1, 3), (1, 1), (1, 1), (1, 3), (1, 2), (1, 1), (1, 2), (1, 2), (1, 2), (None, None), (1, 3), (1, 2), (None, None), (1, 2), (None, None), (0, 3), (1, 4), (1, 3), (None, None), (1, 3), (1, 4), (None, None), (None, None), (1, 3), (1, 4), (2, 5), (None, 5)]], [20794, [(2, 2), (None, 3), (2, 1), (None, 2), (1, 1), (1, 1), (1, 1), (2, 2), (2, 2), (1, 1), (2, 2), (2, 2), (1, 1), (None, 2), (1, 1), (1, 1), (1, 1), (2, 2), (None, 2), (None, 1), (2, 2), (2, 2), (None, 2), (1, 1), (2, 2), (None, 1), (1, 1), (None, 1), (1, 1), (2, 2), (1, 0), (1, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (1, 0), (None, 1), (None, 1), (1, 1), (None, 1), (None, None), (None, 1), (None, 0), (None, None), (None, None), (None, 1), (None, 1), (1, 1), (None, 0), (None, 0), (None, 0), (None, 0), (1, 0), (None, None), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (1, 1), (None, 0), (None, 0), (None, None), (None, 0), (None, 1), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 1), (None, 0), (None, 0), (None, 0), (None, 0), (1, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, None), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, None), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, None), (1, 1), (None, 0), (1, 1), (None, 0), (None, 0)]], [22189, [(None, 4), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (None, 1), (2, 2), (2, 1), (2, 1), (2, 0), (2, 1), (1, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (1, 1), (2, 0), (1, 0), (1, 0), (1, 0), (None, 0), (2, 0), (None, 0), (2, 0), (2, 0), (1, 2), (2, 0), (1, 0), (2, 0), (None, None), (2, 0), (None, None)]]]]]

#print(Remove_Duplicate_Souces(Source_Flux_Area_HL, Data_Input=dir+"/../SQL_Standard_File/Source_Flux_All_Modified_6.csv"))

#print(Source_Flux_Area_Calc_Galaxy_Bulk(["NGC 4449","NGC 3077"],  Max_Counts=50, Counts_Step=5))
#print(Source_Count_Matrix_Calc(["NGC 4449","NGC 3077"]))
#print(Background_Calc(316))
#print(Limiting_Flux_Intersected_Region_Calc(316))
#print(Merged_Area_Calc_Galaxy_L(["NGC 5128"]))
#MESSIER 106
#print(Background_Calc(354))
#print(Merged_Area_Calc_Galaxy_L(["MESSIER 106"]))
#print(Background_Calc(18047))
#Save_FOV1_Region(18047)
#print(Background_Calc(864))
#print(Limiting_Flux_Intersected_Region_Calc(864))
#print(Differential_LogN_LogC_Calc())
#print(LogN_LogC_Calc())
#Log_N_Log_C_Plotting()
#Log_N_Log_R_Plotting()
#Log_N_Log_C_Plotting(Galactic_Radius_Max=4.0, Galactic_Radius_Step=0.125)
#Log_N_Log_R_Plotting(Galactic_Radius_Max=4.0, Galactic_Radius_Step=0.125)
#Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_Backup.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas_Backup.csv')
#Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_Modified.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas_Backup.csv')
#Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_Modified_2.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas_Modified.csv')
#Log_N_Log_R_Plotting(Galactic_Radius_Max=4.0)
#Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_Big_Radius_Modified.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas_Big_Radius_Modified.csv', Galactic_Radius_Max=4.0)
###Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_Big_Radius_Modified_2.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas_Big_Radius_Modified_2.csv', Galactic_Radius_Max=4.0)
#Log_N_Log_R_Plotting(Galactic_Radius_Max=4.0, Galactic_Radius_Step=0.5)
#MESSIER 083
#print(Merged_Area_Calc_Galaxy_L(["MESSIER 083"], Galactic_Radius_Max=4.0, D25_Area_Bool=True))
#print(Merged_Area_Calc_Galaxy_L(["NGC 4449"], Galactic_Radius_Max=4.0, D25_Area_Bool=True))
#Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_Big_Radius.csv', Limiting_Flux_Areas_Path='Limiting_Flux_D25_Areas.csv', Galactic_Radius_Max=4.0)
##Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_Big_Radius_Modified_2.csv', Limiting_Flux_Areas_Path='Limiting_Flux_D25_Areas_Modified.csv', Galactic_Radius_Max=4.0)
##Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_Big_Radius_Modified_2.csv', Limiting_Flux_Areas_Path='Limiting_Flux_D25_Areas_Modified.csv', Alternative_Limiting_Flux_Areas_Path='Limiting_Flux_Areas_Big_Radius_Modified_2.csv', Galactic_Radius_Max=4.0, D25_Area_Bool=True)
#Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_Very_Coarse.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas_Very_Coarse.csv', Galactic_Radius_Max=4.0, Galactic_Radius_Step=0.5)
###Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_Big_Radius_Modified_2.csv', Limiting_Flux_Areas_Path='Limiting_Flux_D25_Areas_Square_Modified.csv', Alternative_Limiting_Flux_Areas_Path='Limiting_Flux_Areas_Big_Radius_Modified_2.csv', Galactic_Radius_Max=4.0, D25_Area_Bool=True)
#Save_FOV1_Region(2076)
#print(Background_Calc(2076))
##Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_5_Counts_Bins.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas_5_Count_Bins.csv', Counts_Step=5, Galactic_Radius_Max=4.0)
##Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_5_Counts_Bins_Modified.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas_5_Count_Bins_Modified.csv', Counts_Step=5, Galactic_Radius_Max=4.0)
#print(Flux_to_Counts_Convert(1E-15,10125))
#print(Flux_to_Counts_Convert(2.7720248100903852e-14,10125)) #28.374297078590043 counts #2.7720248100903852e-14 erg/s*cm^2
#print(Flux_to_Counts_Convert(2E-14,10125))
#print(Flux_Array_Calc())
#print(Theta_Intersection_Calc(10125,Flux_Bool=True))
#print(Theta_Intersection_Calc(10125,Flux_Bool=False))
#print(Limiting_Flux_Intersected_Region_Calc(2076, Flux_Bool=True))
#print(Theta_Intersection_Calc(16024,Flux_Bool=True))
#print(Gamma_Calc(16024))
#Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_Flux_Bins.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas_Flux_Bins.csv', Galactic_Radius_Max=4.0, Flux_Bool=True)
Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_Flux_Bins_Modified.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas_Flux_Bins_Modified.csv', Galactic_Radius_Max=4.0, Flux_Bool=True)
#Log_N_Log_R_Plotting(Source_Count_Matrix_Path='Source_Count_Matrix_Flux_Bins_Big_Cut_Modified.csv', Limiting_Flux_Areas_Path='Limiting_Flux_Areas_Flux_Bins_Big_Cut_Modified.csv', Galactic_Radius_Max=4.0, Flux_Bool=True)





###Main()
