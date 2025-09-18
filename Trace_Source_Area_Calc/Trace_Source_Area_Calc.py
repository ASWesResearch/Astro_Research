import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import glob
import os
import sys
#from ciao_contrib.runtool import *
#from region import *
dir = os.path.dirname(__file__)
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))
#from File_Query_Code import File_Query_Code_5
#from Coords_Calc import Coords_Calc
from ObsID_From_CSV_Query import ObsID_From_CSV_Query

def Ellipse_Area_Calc(a,b):
    return np.pi*a*b

def Source_Area_Calc(Shape_Str):
    #Finds area of source ellipse
    Cur_Reg_String_L=re.split("[(),]", Shape_Str)
    #print("Cur_Reg_String_L: ", Cur_Reg_String_L)
    Semi_Major_Axis=float(Cur_Reg_String_L[3])
    Semi_Minor_Axis=float(Cur_Reg_String_L[4])
    Area=Ellipse_Area_Calc(Semi_Major_Axis, Semi_Minor_Axis)
    return Area

def Read_Region_File(ObsID):
    Trace_Path="/opt/xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"+str(ObsID)+"/"
    Reg_Path=Trace_Path+"Raytraced_Sources_ObsID_"+str(ObsID)+"_Detector_Coords.reg"
    Trace_File=open(Reg_Path)
    Trace_Str=Trace_File.read()
    #Splits header from .reg file
    header='# Region file format: DS9 version 3.0\nglobal color=blue font="helvetica 10 normal" select=1 edit=1 move=1 delete=1 include=1 fixed=0\n'
    Shape_Str_DF=pd.DataFrame({"Shape_Str_Raw":Trace_Str.split(header)[-1].split("\n")[:-1]})
    Shape_Str_DF["Area"]=Shape_Str_DF["Shape_Str_Raw"].apply(Source_Area_Calc)
    #print("Shape_Str_DF: ", Shape_Str_DF)
    Coords_Path=Trace_Path+"Raytraced_Sources_ObsID_"+str(ObsID)+"_Coords.csv"
    Coords_Data=pd.read_csv(Coords_Path)
    #print("Coords_Data:\n", Coords_Data)
    #Creates new dataframe with needed data
    Data = Coords_Data[["Det_X","Det_Y","Offaxis_Angle"]].join(Shape_Str_DF[["Area"]])
    #Adds ObsID and Source Number Columns
    Data["ObsID"]=ObsID
    Data = Data.reset_index()
    Data["Source_Num"]=Data["index"]+1
    Data = Data.drop(columns=["index"])
    #Rearraging columns
    Key_L=list(Data.keys())
    New_Key_L=Key_L[-2:]+Key_L[:-2]
    #print("New_Key_L:", New_Key_L)
    Data=Data[New_Key_L]
    return Data

def Read_Region_File_Bulk(ObsID_L):
    Fail_L=[]
    for i in range(0,len(ObsID_L)):
        ObsID=ObsID_L[i]
        try:
            Cur_Data=Read_Region_File(ObsID)
        except:
            Fail_L.append(ObsID)
        #print("Cur_Data:\n", Cur_Data)
        if(i==0):
            Data=Cur_Data
        else:
            Data=pd.concat([Data, Cur_Data], ignore_index=True)
    print("Fail_L: ", Fail_L)
    return Data

def Cutoff_Line(x,x0=0,x1=12.5,F0=50.0,F1=9000.0,n=10.0):
    F=F0*(n**(((x-x0)/(x1-x0))*np.log10(F1/F0)))
    return F

def Source_Area_Vs_Offaxis_Angle_Plot(ObsID_L):
    Data=Read_Region_File_Bulk(ObsID_L)
    #plt.plot(Data["Offaxis_Angle"], Data["Area"], ".")
    plt.semilogy(Data["Offaxis_Angle"], Data["Area"], ".")
    Cutoff_Line=Cutoff_Line(Data["Offaxis_Angle"])
    plt.semilogy(Data["Offaxis_Angle"], Cutoff_Line)
    plt.xlabel("Offaxis Angle (arcmin)")
    plt.ylabel("Source Area (pix^2)")
    plt.title("Raytraced Sources Offaxis Angle vs Source Area")
    plt.savefig('Trace_Sources_Offaxis_Angle_vs_Area.pdf')

def Filter_Sources(ObsID_L, Save_Data_Bool=False):
    Data=Read_Region_File_Bulk(ObsID_L)
    Data["Point_Source_Area_Upper_Limit"]=Cutoff_Line(Data["Offaxis_Angle"])
    Data["Extended_Source_Ratio"]=Data["Area"]/Data["Point_Source_Area_Upper_Limit"]
    Data["Extended_Source_Bool"]=Data["Extended_Source_Ratio"]>1.0
    print("Total Sources:", len(Data["Extended_Source_Bool"]))
    print("Number of Extended Sources:", len(Data[Data["Extended_Source_Bool"]]["Extended_Source_Bool"]))
    if(Save_Data_Bool):
        Data.to_csv("Raytraced_Source_Areas.csv")
    return Data

#print(Source_Area_Calc("physical;Ellipse(4194.668904298283,4407.191730705707,5.75915,3.3802,-45.4485) #  "))
#Read_Region_File(404)
#print(Read_Region_File_Bulk([404,10125]))
#Source_Area_Vs_Offaxis_Angle_Plot([404,10125])
ObsID_L=ObsID_From_CSV_Query.Read_ObsIDs(Remove_Unarchived=True)
#Source_Area_Vs_Offaxis_Angle_Plot(ObsID_L)
print(Filter_Sources(ObsID_L, Save_Data_Bool=True))
