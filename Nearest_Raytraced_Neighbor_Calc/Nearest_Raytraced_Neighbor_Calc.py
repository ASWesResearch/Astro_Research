import os
from os import system
import sys
import numpy as np
import re
from ciao_contrib.runtool import *
import glob
import matplotlib.pyplot as plt
#import time
dir = os.path.dirname(__file__)
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))
from File_Query_Code import File_Query_Code_5
from Coords_Calc import Coords_Calc
#Constants:
#Root_Path="/Volumes/"
Root_Path="/opt/"
def Reg_Org(Reg_Str):
    Reg_L=re.split("[(),]",Reg_Str)
    #print "Cur_Raytrace_Reg_L: ", Cur_Raytrace_Reg_L
    X_Str=Reg_L[1]
    X=float(X_Str)
    Y_Str=Reg_L[2]
    Y=float(Y_Str)
    return X
def Distance_Calc(x1,y1,x2,y2):
    Distance=np.sqrt(((x2-x1)**2.0)+((y2-y1)**2.0))
    return Distance
def Nearest_Raytraced_Neighbor_Calc(ObsID):
    #For Accessing the Raytraced Region Files:
    #THIS STILL NEEDS TO BE CHECKED FOR BUGS ! ! !
    Header_String='# Region file format: DS9 version 3.0\nglobal color=blue font="helvetica 10 normal" select=1 edit=1 move=1 delete=1 include=1 fixed=0\n'
    Raytrace_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/Detector_Coord_All_Soruces.reg"
    Raytrace_Reg_File=open(Raytrace_Reg_Fpath)
    Raytrace_Reg_Str=Raytrace_Reg_File.read()
    #print "Raytrace_Reg_Str:\n", Raytrace_Reg_Str
    Raytrace_Reg_Str_L=Raytrace_Reg_Str.split(Header_String)
    #print "Raytrace_Reg_Str_L: ", Raytrace_Reg_Str_L
    Raytrace_Reg_Str_Reduced=Raytrace_Reg_Str_L[1]
    #print "Raytrace_Reg_Str_Reduced:\n", Raytrace_Reg_Str_Reduced
    Raytrace_Reg_Str_Reduced_L=Raytrace_Reg_Str_Reduced.split("\n")
    #print "Raytrace_Reg_Str_Reduced_L: ", Raytrace_Reg_Str_Reduced_L
    #print "len(Raytrace_Reg_Str_Reduced_L) Before Pop: ", len(Raytrace_Reg_Str_Reduced_L)
    Raytrace_Reg_Str_Reduced_L.pop(len(Raytrace_Reg_Str_Reduced_L)-1)
    #print "Raytrace_Reg_Str_Reduced_L After Pop: ", Raytrace_Reg_Str_Reduced_L
    #print "len(Raytrace_Reg_Str_Reduced_L) After Pop: ", len(Raytrace_Reg_Str_Reduced_L)
    #print "len(Source_C_L): ", len(Source_C_L)
    """
    path_Coords=Root_Path+"xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"
    path_Obs=path_Coords+str(ObsID)+'/'
    #directory_Obs=os.path.dirname(path_Obs)
    #if not os.path.exists(directory_Obs):
        #os.makedirs(directory_Obs)
    Raytrace_Reg_Fname="ObsID_"+str(ObsID)+"_Raytraced_Source_Regions.reg"
    Raytrace_Reg_Fpath=path_Obs+Raytrace_Reg_Fname
    print "Raytrace_Reg_Fpath: ", Raytrace_Reg_Fpath
    ObsID_Reg_File=open(Raytrace_Reg_Fpath)
    ObsID_Reg_Str=ObsID_Reg_File.read()
    print "ObsID_Reg_Str: ", ObsID_Reg_Str
    """
    #For Accessing the Unraytraced Region Files:
    ##Obervations_Path=Root_Path+"xray/simon/all_chandra_observations/" #This is an the path for Vetinari
    #/Volumes/expansion/ObsIDs/10125/new/exposure_correction/10125_src.reg
    Obervations_Path="/Volumes/expansion/ObsIDs/" #This is an the path for Mando
    ##ObsID_Filepath=Obervations_Path+str(ObsID)+"/primary/" #This is an the path for Vetinari
    ObsID_Filepath=Obervations_Path+str(ObsID)+"/new/" #This is an the path for Mando
    Evt2_LS_String=os.popen("ls " +ObsID_Filepath+"| grep 'evt2.fit'").read()
    #print "Evt2_LS_String: ", Evt2_LS_String
    Evt2_LS_String_L=Evt2_LS_String.split("\n")
    #print "Evt2_LS_String_L: ", Evt2_LS_String_L
    Evt2_Fname=Evt2_LS_String_L[0]
    #print "Evt2_Fname: ", Evt2_Fname
    Evt2_Filepath=ObsID_Filepath+Evt2_Fname
    print("Evt2_Filepath: ", Evt2_Filepath)
    ##Untraced_Path=Obervations_Path+str(ObsID)+"/primary/"+str(ObsID)+"_reg.reg" #This needs to be converted to detector coordinates #This is an the path for Vetinari
    Untraced_Path=Obervations_Path+str(ObsID)+"/new/exposure_correction/"+str(ObsID)+"_src.reg" #This needs to be converted to detector coordinates #This is an the path for Mando
    Untraced_File=open(Untraced_Path)
    Untraced_Str=Untraced_File.read() # Note: The order of the sources may not be enfored here. It is totaly possible that the soruce are saved in the order of first number how simon did it (For example 1.reg, 10.reg, 11.reg, 2.reg) rather then the way I do it (1.reg, 2.reg...n.reg), Note_Update: Nevermind these are not from trace but wavedect sources the order has no meaning
    #print "Untraced_Str: \n", Untraced_Str
    Untraced_Reg_L=Untraced_Str.split("\n")
    #print "Untraced_Reg_L Before Pop: ", Untraced_Reg_L
    Untraced_Reg_L.pop(len(Untraced_Reg_L)-1)
    #print "Untraced_Reg_L After Pop: ", Untraced_Reg_L
    #for Untraced_Reg in Untraced_Reg_L:
    #Nearest_Neighbor_Hybrid_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
    Nearest_Neighbor_Hybrid_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
    directory_Obs=os.path.dirname(Nearest_Neighbor_Hybrid_Reg_Fpath)
    if not os.path.exists(directory_Obs):
        os.makedirs(directory_Obs)
    Nearest_Neighbor_Hybrid_Reg_File=open(Nearest_Neighbor_Hybrid_Reg_Fpath,"w")
    Nearest_Neighbor_Hybrid_Reg_File.write(Header_String)
    Nearest_Neighbor_Hybrid_Reg_L=[]
    for i in range(0,len(Untraced_Reg_L)):
    #for i in range(0,1): #This is a TEST
        Cur_Min_Distance=100000 #Much larger then any distance expected to be encoutered
        Cur_Min_Index=0
        Untraced_Reg=Untraced_Reg_L[i]
        Cur_Reg_String_L=re.split("[(),]",Untraced_Reg)
        #print "Cur_Reg_String_L: ", Cur_Reg_String_L
        Cur_X_Str=Cur_Reg_String_L[1]
        Cur_X=float(Cur_X_Str)
        Cur_Y_Str=Cur_Reg_String_L[2]
        Cur_Y=float(Cur_Y_Str)
        dmcoords(infile=str(Evt2_Filepath),x=float(Cur_X), y=float(Cur_Y), option='sky', verbose=0, celfmt='deg') #Calls dmcoords to get the offaxis angle from the physical coordinates #I should just use the RA and DEC of each X-ray object instead of the SKY coordinate
        Cur_Det_X=dmcoords.detx
        #print "Cur_Det_X : ", Cur_Det_X
        Cur_Det_Y=dmcoords.dety
        #print "Cur_Det_Y : ", Cur_Det_Y
        #print "Raytrace_Reg_Str_Reduced_L: ", Raytrace_Reg_Str_Reduced_L
        for j in range(0,len(Raytrace_Reg_Str_Reduced_L)):
            Cur_Raytrace_Reg=Raytrace_Reg_Str_Reduced_L[j]
            Cur_Raytrace_Reg_L=re.split("[(),]",Cur_Raytrace_Reg)
            #print "Cur_Raytrace_Reg_L: ", Cur_Raytrace_Reg_L
            Cur_Det_Trace_X_Str=Cur_Raytrace_Reg_L[1]
            Cur_Det_Trace_X=float(Cur_Det_Trace_X_Str)
            Cur_Det_Trace_Y_Str=Cur_Raytrace_Reg_L[2]
            Cur_Det_Trace_Y=float(Cur_Det_Trace_Y_Str)
            Distance=Distance_Calc(Cur_Det_X,Cur_Det_Y,Cur_Det_Trace_X,Cur_Det_Trace_Y)
            #print "Distance: ", Distance
            #if((Distance<Cur_Min_Distance) and (Distance>1.0)): #The Distance>1.0 is the wrong way to do this. I need to decide if I am keeping all sources or only the untraced ones, I need to add a condition that if a indendical source is found in both lists it keeps the original trace version if it does not already
            if(Distance<Cur_Min_Distance): #The Distance>1.0 is the wrong way to do this. I need to decide if I am keeping all sources or only the untraced ones, I need to add a condition that if a indendical source is found in both lists it keeps the original trace version if it does not already
                Cur_Min_Distance=Distance
                Cur_Min_Index=j
        Nearest_Raytraced_Neighbor_Reg=Raytrace_Reg_Str_Reduced_L[Cur_Min_Index]
        #print "Cur_Min_Distance: ", Cur_Min_Distance
        #print "Nearest_Raytraced_Neighbor_Reg: ", Nearest_Raytraced_Neighbor_Reg
        Nearest_Raytraced_Neighbor_Reg_Str_L=re.split("[(),]",Nearest_Raytraced_Neighbor_Reg)
        #print "Nearest_Raytraced_Neighbor_Reg_Str_L: ", Nearest_Raytraced_Neighbor_Reg_Str_L
        #Cur_Hybrid_Reg=Cur_Reg_String_L[0]+"("+Nearest_Raytraced_Neighbor_Reg_Str_L[1]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[2]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[3]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[4]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[5]+")\n"
        Cur_Hybrid_Reg=Nearest_Raytraced_Neighbor_Reg_Str_L[0]+"("+Cur_Reg_String_L[1]+","+Cur_Reg_String_L[2]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[3]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[4]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[5]+")"+Nearest_Raytraced_Neighbor_Reg_Str_L[6]+"\n"
        #print "Cur_Hybrid_Reg: ", Cur_Hybrid_Reg
        Cur_Hybrid_Reg_Det=Nearest_Raytraced_Neighbor_Reg_Str_L[0]+"("+str(Cur_Det_X)+","+str(Cur_Det_Y)+","+Nearest_Raytraced_Neighbor_Reg_Str_L[3]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[4]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[5]+")"+Nearest_Raytraced_Neighbor_Reg_Str_L[6]+"\n"
        #print "Cur_Hybrid_Reg_Det: ", Cur_Hybrid_Reg_Det
        #Nearest_Neighbor_Hybrid_Reg_File.write(Cur_Hybrid_Reg) # I don't know if I need to use the X and Y as sky coordinates or detector coordinates if detector coordinates then this must be changed to "Nearest_Neighbor_Hybrid_Reg_File.write(Cur_Hybrid_Reg_Det)", I don't think the shapes of the regions transfered are vaild in detector coodinates so I'm going with sky coordinates now. Also I'm pretty sure calcuationg flux requires sky coords not detector coords
        Nearest_Neighbor_Hybrid_Reg_L.append(Cur_Hybrid_Reg)
    #print "Nearest_Neighbor_Hybrid_Reg_L Before: ", Nearest_Neighbor_Hybrid_Reg_L
    #print type(Nearest_Neighbor_Hybrid_Reg_L[0])
    #Nearest_Neighbor_Hybrid_Reg_L.sort(key=Reg_Org(Nearest_Neighbor_Hybrid_Reg_L,Evt2_Filepath))
    Nearest_Neighbor_Hybrid_Reg_L.sort(key=Reg_Org,reverse=True)
    #Nearest_Neighbor_Hybrid_Reg_L=Reg_Sort(Nearest_Neighbor_Hybrid_Reg_L,Evt2_Filepath)
    #print "Nearest_Neighbor_Hybrid_Reg_L After: ", Nearest_Neighbor_Hybrid_Reg_L
    #Nearest_Neighbor_Hybrid_Reg_L.sort(key=Reg_Org(self,Evt2_Filepath))
    Source_Num=1
    for Cur_Hybrid_Reg in Nearest_Neighbor_Hybrid_Reg_L:
        #print "Cur_Hybrid_Reg: ", Cur_Hybrid_Reg
        #print "type(Cur_Hybrid_Reg): ", type(Cur_Hybrid_Reg)
        Nearest_Neighbor_Hybrid_Reg_File.write(Cur_Hybrid_Reg) # I don't know if I need to use the X and Y as sky coordinates or detector coordinates if detector coordinates then this must be changed to "Nearest_Neighbor_Hybrid_Reg_File.write(Cur_Hybrid_Reg_Det)", I don't think the shapes of the regions transfered are vaild in detector coodinates so I'm going with sky coordinates now. Also I'm pretty sure calcuationg flux requires sky coords not detector coords
        Cur_Source_Nearest_Neighbor_Hybrid_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/Individual_Source_Regions/"+"Source_"+str(Source_Num)+"_ObsID_"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
        directory_Obs=os.path.dirname(Cur_Source_Nearest_Neighbor_Hybrid_Reg_Fpath)
        if not os.path.exists(directory_Obs):
            os.makedirs(directory_Obs)
        Cur_Source_Nearest_Neighbor_Hybrid_Reg_File=open(Cur_Source_Nearest_Neighbor_Hybrid_Reg_Fpath,"w")
        Cur_Source_Nearest_Neighbor_Hybrid_Reg_File.write(Header_String)
        Cur_Source_Nearest_Neighbor_Hybrid_Reg_File.write(Cur_Hybrid_Reg)
        Cur_Source_Nearest_Neighbor_Hybrid_Reg_File.close()
        Source_Num=Source_Num+1
    Raytrace_Reg_File.close()
    Untraced_File.close()
    Nearest_Neighbor_Hybrid_Reg_File.close()

    """
    This creates the Nearest_Neighbor_Hybrid_Sources_Coords.csv Files
    """
    Source_C_L=Coords_Calc.Coords_Calc(Evt2_Filepath,Nearest_Neighbor_Hybrid_Reg_Fpath)
    #print "Source_C_L:\n", Source_C_L
    Nearest_Neighbor_Hybrid_Coord_Outpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/Nearest_Neighbor_Hybrid_Sources_ObsID_"+str(ObsID)+"_Coords.csv"
    #print "Nearest_Neighbor_Hybrid_Coord_Outpath: ", Nearest_Neighbor_Hybrid_Coord_Outpath
    file2=open(Nearest_Neighbor_Hybrid_Coord_Outpath,"w")
    #[Cur_X,Cur_Y,Cur_Chip_X,Cur_Chip_Y,Cur_Chip_ID,Cur_RA,Cur_DEC,Cur_Theta]
    file2.write("Phys_X,Phys_Y,Chip_X,Chip_Y,Chip_ID,RA,DEC,Det_X,Det_Y,Offaxis_Angle"+"\n")
    Nearest_Neighbor_Hybrid_Reg_File=open(Nearest_Neighbor_Hybrid_Reg_Fpath)
    Nearest_Neighbor_Hybrid_Reg_Str=Nearest_Neighbor_Hybrid_Reg_File.read()
    #print "Nearest_Neighbor_Hybrid_Reg_Str:\n", Nearest_Neighbor_Hybrid_Reg_Str
    Nearest_Neighbor_Hybrid_Reg_Str_L=Nearest_Neighbor_Hybrid_Reg_Str.split(Header_String)
    #print "Nearest_Neighbor_Hybrid_Reg_Str_L: ", Nearest_Neighbor_Hybrid_Reg_Str_L
    Nearest_Neighbor_Hybrid_Reg_Str_Reduced=Nearest_Neighbor_Hybrid_Reg_Str_L[1]
    #print "Nearest_Neighbor_Hybrid_Reg_Str_Reduced:\n", Nearest_Neighbor_Hybrid_Reg_Str_Reduced
    Nearest_Neighbor_Hybrid_Reg_Str_Reduced_L=Nearest_Neighbor_Hybrid_Reg_Str_Reduced.split("\n")
    #print "Nearest_Neighbor_Hybrid_Reg_Str_Reduced_L: ", Nearest_Neighbor_Hybrid_Reg_Str_Reduced_L
    #print "len(Nearest_Neighbor_Hybrid_Reg_Str_Reduced_L) Before Pop: ", len(Nearest_Neighbor_Hybrid_Reg_Str_Reduced_L)
    Nearest_Neighbor_Hybrid_Reg_Str_Reduced_L.pop(len(Nearest_Neighbor_Hybrid_Reg_Str_Reduced_L)-1)
    #print "Nearest_Neighbor_Hybrid_Reg_Str_Reduced_L After Pop: ", Nearest_Neighbor_Hybrid_Reg_Str_Reduced_L
    #print "len(Nearest_Neighbor_Hybrid_Reg_Str_Reduced_L) After Pop: ", len(Nearest_Neighbor_Hybrid_Reg_Str_Reduced_L)
    #print "len(Source_C_L): ", len(Source_C_L)
    #for Source_C in Source_C_L:
    for i in range(0,len(Source_C_L)):
        Source_C=Source_C_L[i]
        #print "Source_C: ", Source_C
        Cur_Reg=Nearest_Neighbor_Hybrid_Reg_Str_Reduced_L[i]
        #print "Cur_Reg: ", Cur_Reg
        Phys_X=Source_C[0]
        Phys_Y=Source_C[1]
        Chip_X=Source_C[2]
        Chip_Y=Source_C[3]
        Chip_ID=Source_C[4]
        RA=Source_C[5]
        DEC=Source_C[6]
        Det_X=Source_C[7]
        Det_Y=Source_C[8]
        Offaxis_Angle=Source_C[9]
        file2.write(str(Phys_X)+","+str(Phys_Y)+","+str(Chip_X)+","+str(Chip_Y)+","+str(Chip_ID)+","+str(RA)+","+str(DEC)+","+str(Det_X)+","+str(Det_Y)+","+str(Offaxis_Angle)+"\n")
        #Cur_Reg_Str="detector;Ellipse("4095.41,3893.44,4.12171,3.24946,2.0637) #"
        Cur_Reg_String_L=re.split("[(),]",Cur_Reg)
        #print "Cur_Reg_String_L: ", Cur_Reg_String_L
        #Cur_Reg_Str="detector;Circle("+str(Det_X)+","+str(Det_Y)+","+str(10)+") #\n" #This needs to be updated to preserve the region shape
        Cur_Reg_Str=Cur_Reg_String_L[0]+"("+str(Det_X)+","+str(Det_Y)+","+Cur_Reg_String_L[3]+","+Cur_Reg_String_L[4]+","+Cur_Reg_String_L[5]+")"+Cur_Reg_String_L[6]+"\n"
        #print "Cur_Reg_Str: ", Cur_Reg_Str
    file2.close()
    Nearest_Neighbor_Hybrid_Reg_File.close()

#Nearest_Raytraced_Neighbor_Calc(10125)
def Background_Reg_Generator(ObsID):
    Header_String='# Region file format: DS9 version 3.0\nglobal color=blue font="helvetica 10 normal" select=1 edit=1 move=1 delete=1 include=1 fixed=0\n'
    Nearest_Neighbor_Hybrid_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
    Nearest_Neighbor_Reg_File=open(Nearest_Neighbor_Hybrid_Reg_Fpath)
    Nearest_Neighbor_Reg_Str=Nearest_Neighbor_Reg_File.read()
    #print "Nearest_Neighbor_Reg_Str:\n", Nearest_Neighbor_Reg_Str
    Nearest_Neighbor_Reg_Str_L=Nearest_Neighbor_Reg_Str.split(Header_String)
    #print "Nearest_Neighbor_Reg_Str_L: ", Nearest_Neighbor_Reg_Str_L
    Nearest_Neighbor_Reg_Str_Reduced=Nearest_Neighbor_Reg_Str_L[1]
    #print "Nearest_Neighbor_Reg_Str_Reduced:\n", Nearest_Neighbor_Reg_Str_Reduced
    Nearest_Neighbor_Reg_Str_Reduced_L=Nearest_Neighbor_Reg_Str_Reduced.split("\n")
    #print "Nearest_Neighbor_Reg_Str_Reduced_L: ", Nearest_Neighbor_Reg_Str_Reduced_L
    #print "len(Nearest_Neighbor_Reg_Str_Reduced_L) Before Pop: ", len(Nearest_Neighbor_Reg_Str_Reduced_L)
    Nearest_Neighbor_Reg_Str_Reduced_L.pop(len(Nearest_Neighbor_Reg_Str_Reduced_L)-1)
    Nearest_Neighbor_Hybrid_BG_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid_Background.reg"
    Nearest_Neighbor_Hybrid_BG_Reg_File=open(Nearest_Neighbor_Hybrid_BG_Reg_Fpath,"w")
    Nearest_Neighbor_Hybrid_BG_Reg_File.write(Header_String)
    Source_Num=1
    for Nearest_Neighbor_Reg_Str_Reduced in Nearest_Neighbor_Reg_Str_Reduced_L:
        Nearest_Neighbor_Reg_Str_Reduced_Split_L=re.split("[(),]", Nearest_Neighbor_Reg_Str_Reduced)
        #print "Nearest_Neighbor_Reg_Str_Reduced_Split_L: ", Nearest_Neighbor_Reg_Str_Reduced_Split_L
        X_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[1]
        #print "X_Str: ", X_Str
        X=float(X_Str)
        Y_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[2]
        Y=float(Y_Str)
        Maj_Ax_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[3]
        Maj_Ax=float(Maj_Ax_Str)
        Min_Ax_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[4]
        Min_Ax=float(Min_Ax_Str)
        Angle_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[5]
        Angle=float(Angle_Str)
        Reg_Front_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[0]
        Reg_Front_Str_L=Reg_Front_Str.split(";")
        Units_Str=Reg_Front_Str_L[0]
        Shape_Str=Reg_Front_Str_L[1]
        Reg_Back_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[len(Nearest_Neighbor_Reg_Str_Reduced_Split_L)-1]
        BG_Maj=2.0*Maj_Ax
        BG_Min=2.0*Min_Ax
        Cur_BG_Reg=Units_Str+";"+Shape_Str+"("+str(X)+","+str(Y)+","+str(BG_Maj)+","+str(BG_Min)+","+str(Angle)+")"+Reg_Back_Str+"\n"
        Cur_Reg=Units_Str+";-"+Shape_Str+"("+str(X)+","+str(Y)+","+str(Maj_Ax)+","+str(Min_Ax)+","+str(Angle)+")"+Reg_Back_Str+"\n"
        #print "Cur_BG_Reg: ", Cur_BG_Reg
        #print "Cur_Reg: ", Cur_Reg
        Nearest_Neighbor_Hybrid_BG_Reg_File.write(Cur_BG_Reg)
        Nearest_Neighbor_Hybrid_BG_Reg_File.write(Cur_Reg)
        Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/Individual_Source_Regions/"+"Source_"+str(Source_Num)+"_ObsID_"+str(ObsID)+"_Nearest_Neighbor_Hybrid_Background.reg"
        directory_Obs=os.path.dirname(Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_Fpath)
        if not os.path.exists(directory_Obs):
            os.makedirs(directory_Obs)
        Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_File=open(Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_Fpath,"w")
        Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_File.write(Header_String)
        Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_File.write(Cur_BG_Reg)
        Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_File.write(Cur_Reg)
        Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_File.close()
        Source_Num=Source_Num+1
    Nearest_Neighbor_Hybrid_BG_Reg_File.close()

#Background_Reg_Generator(10125)

def Deg_to_Rad(Angle):
    Angle=(np.pi/180.0)*Angle
    return Angle

def Rad_to_Deg(Angle):
    Angle=(180.0/np.pi)*Angle
    return Angle

def Angle_Convert(Angle):
    """
    Angle:-float, an anlge in radians

    Converts angles to be in the range of 0 rad<New_Angle<2pi rad
    """
    Full_Cricle=2.0*np.pi
    if(Angle<0):
        New_Angle=Angle+Full_Cricle
    if(Angle>Full_Cricle):
        New_Angle=Angle-Full_Cricle
    else:
        New_Angle=Angle
    return New_Angle

def Ellipse_Radius_Calc(a,b,Ang_Rel):
    """
    a:-float, Semi-major axis of source ellipse
    b:-float, Semi-minor axis of source ellipse
    Ang_Rel:-float, Polar angle at which the ellipse radius will be calculated in radians

    Calcuates the radius of an ellipse at a given polar angle
    """
    r=(a*b)/(np.sqrt(((b*np.cos(Ang_Rel))**2.0)+((a*np.sin(Ang_Rel))**2.0)))
    return r

def Source_Overlap_Calc(x1,x2,y1,y2,a1,a2,b1,b2,rot1,rot2,M=2.0):
    """
    x1:-float, X Postion of First source ellipse
    x2:-float, X Postion of Second source ellipse
    y1:-float, Y Postion of First source ellipse
    y2:-float, Y Postion of Second source ellipse
    a1:-float, Semi-major axis of First source ellipse
    a2:-float, Semi-major axis of Second source ellipse
    b1:-float, Semi-minor axis of First source ellipse
    b2:-float, Semi-minor axis of Second source ellipse
    rot1:-float, rotation angle of First source ellipse
    rot2:-float, rotation angle of Second source ellipse

    This function takes the coordinates for two source ellipse region shapes as an input and then returns a list of booleans where
    the first element bool is True when the first source has the second source in its backgournd area and the second element bool is True
    when the first soruce area is overlapping with the second source area.
    """
    dx=x2-x1
    dy=y2-y1
    if((dx==0) and (dy==0)):
        #print "Same_Source"
        return [False,False]
    Position_Angle_1=np.arctan2(dy,dx)
    Position_Angle_1=Angle_Convert(Position_Angle_1)
    Position_Angle_2=Position_Angle_1+np.pi
    Position_Angle_2=Angle_Convert(Position_Angle_2)
    Dist=np.sqrt((dx**2.0)+(dy**2.0))
    rot1_Rad=Deg_to_Rad(rot1)
    rot1_Rad=Angle_Convert(rot1_Rad)
    rot2_Rad=Deg_to_Rad(rot2)
    rot2_Rad=Angle_Convert(rot2_Rad)
    Relative_Angle_1=Position_Angle_1-rot1_Rad #Need to make sure rot1 is in radians
    Relative_Angle_2=Position_Angle_2-rot2_Rad #Need to make sure rot2 is in radians
    Relative_Angle_1=Angle_Convert(Relative_Angle_1)
    Relative_Angle_2=Angle_Convert(Relative_Angle_2)
    r1=Ellipse_Radius_Calc(a1,b1,Relative_Angle_1)
    r1_Background=M*r1
    r2=Ellipse_Radius_Calc(a2,b2,Relative_Angle_2)
    Dgs=Dist-r1-r2
    Dgb=Dist-r1_Background-r2
    #print "Dgb: ", Dgb
    Background_Overlap_Bool=(Dgb<0)
    Source_Overlap_Bool=(Dgs<0)
    Overlap_List=[Background_Overlap_Bool,Source_Overlap_Bool]
    return Overlap_List

def Background_Overlap_Corrected_Reg_Generator(ObsID):
    Header_String='# Region file format: DS9 version 3.0\nglobal color=blue font="helvetica 10 normal" select=1 edit=1 move=1 delete=1 include=1 fixed=0\n'
    Nearest_Neighbor_Hybrid_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
    Nearest_Neighbor_Reg_File=open(Nearest_Neighbor_Hybrid_Reg_Fpath)
    Nearest_Neighbor_Reg_Str=Nearest_Neighbor_Reg_File.read()
    #print "Nearest_Neighbor_Reg_Str:\n", Nearest_Neighbor_Reg_Str
    Nearest_Neighbor_Reg_Str_L=Nearest_Neighbor_Reg_Str.split(Header_String)
    #print "Nearest_Neighbor_Reg_Str_L: ", Nearest_Neighbor_Reg_Str_L
    Nearest_Neighbor_Reg_Str_Reduced=Nearest_Neighbor_Reg_Str_L[1]
    #print "Nearest_Neighbor_Reg_Str_Reduced:\n", Nearest_Neighbor_Reg_Str_Reduced
    Nearest_Neighbor_Reg_Str_Reduced_L=Nearest_Neighbor_Reg_Str_Reduced.split("\n")
    #print "Nearest_Neighbor_Reg_Str_Reduced_L: ", Nearest_Neighbor_Reg_Str_Reduced_L
    #print "len(Nearest_Neighbor_Reg_Str_Reduced_L) Before Pop: ", len(Nearest_Neighbor_Reg_Str_Reduced_L)
    Nearest_Neighbor_Reg_Str_Reduced_L.pop(len(Nearest_Neighbor_Reg_Str_Reduced_L)-1)
    Nearest_Neighbor_Hybrid_BG_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid_Overlap_Corrected_Background.reg"
    Nearest_Neighbor_Hybrid_BG_Reg_File=open(Nearest_Neighbor_Hybrid_BG_Reg_Fpath,"w")
    Nearest_Neighbor_Hybrid_BG_Reg_File.write(Header_String)
    Overlapping_Sources_Fpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Overlapping_Sources.csv"
    Overlapping_Sources_File=open(Overlapping_Sources_Fpath,"w")
    Overlapping_Sources_File.write("Source_Num;Background_Overlap;Source_Overlap\n")
    Source_Num=1
    for Nearest_Neighbor_Reg_Str_Reduced in Nearest_Neighbor_Reg_Str_Reduced_L:
        Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/Individual_Source_Regions/"+"Source_"+str(Source_Num)+"_ObsID_"+str(ObsID)+"_Nearest_Neighbor_Hybrid_Overlap_Corrected_Background.reg"
        directory_Obs=os.path.dirname(Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_Fpath)
        if not os.path.exists(directory_Obs):
            os.makedirs(directory_Obs)
        Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_File=open(Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_Fpath,"w")
        Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_File.write(Header_String)
        Nearest_Neighbor_Reg_Str_Reduced_Split_L=re.split("[(),]", Nearest_Neighbor_Reg_Str_Reduced)
        #print "Nearest_Neighbor_Reg_Str_Reduced_Split_L: ", Nearest_Neighbor_Reg_Str_Reduced_Split_L
        X_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[1]
        #print "X_Str: ", X_Str
        X=float(X_Str)
        Y_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[2]
        Y=float(Y_Str)
        Maj_Ax_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[3]
        Maj_Ax=float(Maj_Ax_Str)
        Min_Ax_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[4]
        Min_Ax=float(Min_Ax_Str)
        Angle_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[5]
        Angle=float(Angle_Str)
        Reg_Front_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[0]
        Reg_Front_Str_L=Reg_Front_Str.split(";")
        Units_Str=Reg_Front_Str_L[0]
        Shape_Str=Reg_Front_Str_L[1]
        Reg_Back_Str=Nearest_Neighbor_Reg_Str_Reduced_Split_L[len(Nearest_Neighbor_Reg_Str_Reduced_Split_L)-1]
        BG_Maj=2.0*Maj_Ax
        BG_Min=2.0*Min_Ax
        Cur_BG_Reg=Units_Str+";"+Shape_Str+"("+str(X)+","+str(Y)+","+str(BG_Maj)+","+str(BG_Min)+","+str(Angle)+")"+Reg_Back_Str+"\n"
        Cur_Reg=Units_Str+";-"+Shape_Str+"("+str(X)+","+str(Y)+","+str(Maj_Ax)+","+str(Min_Ax)+","+str(Angle)+")"+Reg_Back_Str+"\n"
        Nearest_Neighbor_Hybrid_BG_Reg_File.write(Cur_BG_Reg)
        Nearest_Neighbor_Hybrid_BG_Reg_File.write(Cur_Reg)
        Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_File.write(Cur_BG_Reg)
        Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_File.write(Cur_Reg)
        Background_Overlap_List=[]
        Source_Overlap_List=[]
        Source_Num_Test=1
        for Nearest_Neighbor_Reg_Str_Reduced_Test in Nearest_Neighbor_Reg_Str_Reduced_L:
            Nearest_Neighbor_Reg_Str_Reduced_Split_L_Test=re.split("[(),]", Nearest_Neighbor_Reg_Str_Reduced_Test)
            #print "Nearest_Neighbor_Reg_Str_Reduced_Split_L: ", Nearest_Neighbor_Reg_Str_Reduced_Split_L
            X_Str_Test=Nearest_Neighbor_Reg_Str_Reduced_Split_L_Test[1]
            #print "X_Str: ", X_Str
            X_Test=float(X_Str_Test)
            Y_Str_Test=Nearest_Neighbor_Reg_Str_Reduced_Split_L_Test[2]
            Y_Test=float(Y_Str_Test)
            Maj_Ax_Str_Test=Nearest_Neighbor_Reg_Str_Reduced_Split_L_Test[3]
            Maj_Ax_Test=float(Maj_Ax_Str_Test)
            Min_Ax_Str_Test=Nearest_Neighbor_Reg_Str_Reduced_Split_L_Test[4]
            Min_Ax_Test=float(Min_Ax_Str_Test)
            Angle_Str_Test=Nearest_Neighbor_Reg_Str_Reduced_Split_L_Test[5]
            Angle_Test=float(Angle_Str_Test)
            Reg_Front_Str_Test=Nearest_Neighbor_Reg_Str_Reduced_Split_L[0]
            Reg_Front_Str_L_Test=Reg_Front_Str.split(";")
            Units_Str_Test=Reg_Front_Str_L[0]
            Shape_Str_Test=Reg_Front_Str_L[1]
            Reg_Back_Str_Test=Nearest_Neighbor_Reg_Str_Reduced_Split_L[len(Nearest_Neighbor_Reg_Str_Reduced_Split_L)-1]
            Overlap_Bool_L=Source_Overlap_Calc(X,X_Test,Y,Y_Test,Maj_Ax,Maj_Ax_Test,Min_Ax,Min_Ax_Test,Angle,Angle_Test)
            Cur_Reg_Test=Units_Str_Test+";-"+Shape_Str_Test+"("+str(X_Test)+","+str(Y_Test)+","+str(Maj_Ax_Test)+","+str(Min_Ax_Test)+","+str(Angle_Test)+")"+Reg_Back_Str_Test+"\n"
            #print Overlap_Bool_L
            """
            if(True in Overlap_Bool_L):
                print "Overlap! "
                print Overlap_Bool_L
                print "Overlapping Region: ", Cur_Reg_Test
            """
            if(Overlap_Bool_L[0]):
                Cur_Reg_Test=Units_Str_Test+";-"+Shape_Str_Test+"("+str(X_Test)+","+str(Y_Test)+","+str(Maj_Ax_Test)+","+str(Min_Ax_Test)+","+str(Angle_Test)+")"+Reg_Back_Str_Test+"color=yellow"+"\n"
                Nearest_Neighbor_Hybrid_BG_Reg_File.write(Cur_Reg_Test)
                Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_File.write(Cur_Reg_Test)
                Background_Overlap_List.append(Source_Num_Test)
            if(Overlap_Bool_L[1]):
                Source_Overlap_List.append(Source_Num_Test)
            Source_Num_Test=Source_Num_Test+1
            #Cur_Reg_Test=Units_Str_Test+";-"+Shape_Str_Test+"("+str(X_Test)+","+str(Y_Test)+","+str(Maj_Ax_Test)+","+str(Min_Ax_Test)+","+str(Angle_Test)+")"+Reg_Back_Str_Test+"\n"
        #print "Cur_BG_Reg: ", Cur_BG_Reg
        #print "Cur_Reg: ", Cur_Reg
        #Nearest_Neighbor_Hybrid_BG_Reg_File.write(Cur_BG_Reg)
        #Nearest_Neighbor_Hybrid_BG_Reg_File.write(Cur_Reg)
        Source_Overlap_Str=str(Source_Num)+";"+str(Background_Overlap_List)+";"+str(Source_Overlap_List)+"\n"
        Overlapping_Sources_File.write(Source_Overlap_Str)
        Cur_Source_Nearest_Neighbor_Hybrid_BG_Reg_File.close()
        Source_Num=Source_Num+1
    Nearest_Neighbor_Hybrid_BG_Reg_File.close()
    Overlapping_Sources_File.close()

def Source_Overlap_Calc_Testing():
    X_L=[-2,2]
    Y_L=[-2,2]
    a2=0.2
    b2=0.1
    rot2= 0
    for X in X_L:
        for Y in Y_L:
            print("("+str(X)+","+str(Y)+")")
            print(Source_Overlap_Calc(0,X,0,Y,2,a2,1,b2,0,rot2,M=3.0))

def Evt2_File_Query(ObsID):
    ##query_path='/Volumes/xray/simon/all_chandra_observations/'+str(ObsID)+'/primary/*evt2*' #Path for Vetinari
    #/Volumes/expansion/ObsIDs/10125/new/exposure_correction/10125_src.reg
    query_path='/Volumes/expansion/ObsIDs/'+str(ObsID)+'/new/*evt2*' #Fot Mando
    evtfpath_L=glob.glob(query_path)
    if(len(evtfpath_L)!=1):
        #print str(ObsID)+" has "+str(len(evtfpath_L)-1)+"Additional Evt2 Files ! ! !"
        print(str(ObsID)+" has "+str(len(evtfpath_L))+" Evt2 Files ! ! !")
        return "Error"
    evtfpath=evtfpath_L[0]
    return evtfpath

def Postion_Error_Calc(OFF,C):
    """
    OFF:-float, Offaxis Angle of the source in units of arcmin
    C:-float, The number of Counts in the soruce

    returns: Error_Radius:-float, the raduis of the positional error of the source. #I have to check if this is actually a radius rather than a diameter or "Error Box" (From Kim et al. 2004)
    """
    Error_Radius_20_Counts=1-(0.02*(OFF**2.0))+(0.0067*(OFF**3.0)) #OFF is in units of arcmin, Error Radius in units of arcsec
    Error_Radius_100_Counts=1-(0.01*(OFF**2.0))+(0.0025*(OFF**3.0)) #OFF is in units of arcmin, Error Radius in units of arcsec
    Point_1=[20,Error_Radius_20_Counts]
    Point_2=[100,Error_Radius_100_Counts]
    Slope=(Point_2[1]-Point_1[1])/(Point_2[0]-Point_1[0])
    #Solved Point Slope Formula y=m(x-x1)+y1
    Error_Radius=Slope*(C-Point_1[0])+Point_1[1]
    #print "Error_Radius: ", Error_Radius
    #"""
    if(Error_Radius<1.0): #This needs to be implimented to work with numpy #Update: This will now work with numpy
        Error_Radius=1.0
    #"""
    return Error_Radius

def Postion_Error_Simple_Calc(OFF,C="None"):
    if(OFF<2.0):
        return 2.0
    return OFF

def Heat_Map(A):
    #plt.imshow(A, cmap='viridis')
    plt.imshow(A, extent=[0, 10, 0, 100], origin='lower',
                  cmap='viridis')
    plt.colorbar()
    plt.axis(aspect='image')
    plt.show()

def Contour_Map(x,y,f,V_min,V_max):
    X, Y = np.meshgrid(x, y)
    Z=np.zeros((len(X),len(X)))
    for i in range(0,len(X)):
        for j in range(0,len(X)):
            Z[i][j]=f(X[i][j],Y[i][j])
    #Z = f(X, Y)
    #plt.contourf(X, Y, Z, 20, cmap='viridis')
    plt.contourf(X, Y, Z, 500, cmap='viridis',vmin=V_min,vmax=V_max)
    #plt.contourf(X, Y, Z, 20, cmap='Wistia',vmin=V_min,vmax=V_max)
    plt.colorbar(ticks=np.arange(V_min,V_max))
    #plt.show()

def Postion_Error_Plot(F):
    Off_A=np.linspace(0,10,100)
    Counts_A=np.arange(0,100)
    """
    Data=np.zeros((100,100))
    for i in range(0,len(Off_A)):
        Cur_Row=[]
        Off=Off_A[i]
        for j in range(0,len(Counts_A)):
            Counts=Counts_A[j]
            Data[i][j]=Postion_Error_Calc(Off,Counts)
    #print Data
    """
    Contour_Map(Off_A,Counts_A,F,0,10)
    plt.xlabel("Offaxis (arcmin)")
    plt.ylabel("Counts")
    plt.title("Positional Error (arcsec)")
    #Fname=F.__name__+"_Plot.pdf"
    Fname=F.__name__+"_Plot.png"
    print("Fname: ", Fname)
    plt.savefig(Fname)
    ##plt.show()
    plt.close()
    #Heat_Map(Data)


def Duplicate_Source_Remover(ObsID):
    print(ObsID)
    Header_String='# Region file format: DS9 version 3.0\nglobal color=blue font="helvetica 10 normal" select=1 edit=1 move=1 delete=1 include=1 fixed=0\n'
    evtfpath=Evt2_File_Query(ObsID)
    Nearest_Neighbor_Hybrid_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
    Nearest_Neighbor_Reg_File=open(Nearest_Neighbor_Hybrid_Reg_Fpath)
    Nearest_Neighbor_Reg_Str=Nearest_Neighbor_Reg_File.read()
    #print "Nearest_Neighbor_Reg_Str:\n", Nearest_Neighbor_Reg_Str
    Nearest_Neighbor_Reg_Str_L=Nearest_Neighbor_Reg_Str.split(Header_String)
    #print "Nearest_Neighbor_Reg_Str_L: ", Nearest_Neighbor_Reg_Str_L
    Nearest_Neighbor_Reg_Str_Reduced=Nearest_Neighbor_Reg_Str_L[1]
    #print "Nearest_Neighbor_Reg_Str_Reduced:\n", Nearest_Neighbor_Reg_Str_Reduced
    Nearest_Neighbor_Reg_Str_Reduced_L=Nearest_Neighbor_Reg_Str_Reduced.split("\n")
    #print "Nearest_Neighbor_Reg_Str_Reduced_L: ", Nearest_Neighbor_Reg_Str_Reduced_L
    #print "len(Nearest_Neighbor_Reg_Str_Reduced_L) Before Pop: ", len(Nearest_Neighbor_Reg_Str_Reduced_L)
    Nearest_Neighbor_Reg_Str_Reduced_L.pop(len(Nearest_Neighbor_Reg_Str_Reduced_L)-1)
    #for Nearest_Neighbor_Reg_Str in Nearest_Neighbor_Reg_Str_Reduced_L:
    Number_Duplicate_Sources=0
    Duplicate_Source_Index_L=[]
    Duplicate_Source_Index_HL=[]
    for i in range(0,len(Nearest_Neighbor_Reg_Str_Reduced_L)):
        Nearest_Neighbor_Reg_Str=Nearest_Neighbor_Reg_Str_Reduced_L[i]
        Nearest_Neighbor_Reg_Str_Split_L=re.split("[(),]", Nearest_Neighbor_Reg_Str)
        #print "Nearest_Neighbor_Reg_Str_Split_L: ", Nearest_Neighbor_Reg_Str_Split_L
        X_Str=Nearest_Neighbor_Reg_Str_Split_L[1]
        #print "X_Str: ", X_Str
        X=float(X_Str)
        Y_Str=Nearest_Neighbor_Reg_Str_Split_L[2]
        Y=float(Y_Str)
        dmcoords(infile=str(evtfpath),x=float(X), y=float(Y), option='sky', verbose=0, celfmt='deg') #Calls dmcoords to get the offaxis angle from the physical coordinates
        Cur_Theta_Arcmin=dmcoords.theta #Cur_Theta:-float, Current Theta, The current offaxis angle of the object in arcmin
        #print "Cur_Theta_Arcmin: ", Cur_Theta_Arcmin
        Nearest_Neighbor_Reg_Str_Reduced=Nearest_Neighbor_Reg_Str.split(";")[1].split(" ")[0]
        Infile_String=evtfpath+"[sky="+Nearest_Neighbor_Reg_Str_Reduced+"]"
        #print "Infile_String: ", Infile_String
        Counts_Output=dmlist(infile=str(Infile_String), opt="counts")
        #print "Counts_Output: ", Counts_Output
        #print "type(Counts_Output): ", type(Counts_Output)
        Counts=float(Counts_Output)
        #print "Counts: ", Counts
        Cur_Source_Radius_Arcsec=Postion_Error_Calc(Cur_Theta_Arcmin,Counts)
        """
        if(Cur_Theta_Arcmin<2.0):
            Cur_Source_Radius_Arcsec=2.0
        else:
            Cur_Source_Radius_Arcsec=Cur_Theta_Arcmin #Source radius in arcsec ~= off-axis angle in arcmin. So 2 min off-axis = 2 arcsec, etc.
        """
        Cur_Source_Radius_Pixels=Cur_Source_Radius_Arcsec*2.03252032520325 #The converstion factor is 2.03252032520325pix/arcsec
        #print "Cur_Source_Radius_Pixels: ", Cur_Source_Radius_Pixels
        #for Nearest_Neighbor_Reg_Str_Test in Nearest_Neighbor_Reg_Str_Reduced_L:
        Cur_Duplicate_Source_Index_L=[]
        for j in range(i+1,len(Nearest_Neighbor_Reg_Str_Reduced_L)): #i+1 to ignore current source. This might not be right
            if(i not in Duplicate_Source_Index_L):
                Nearest_Neighbor_Reg_Str_Test=Nearest_Neighbor_Reg_Str_Reduced_L[j]
                Nearest_Neighbor_Reg_Str_Test_Split_L=re.split("[(),]", Nearest_Neighbor_Reg_Str_Test)
                #print "Nearest_Neighbor_Reg_Str_Split_L: ", Nearest_Neighbor_Reg_Str_Split_L
                X_Str=Nearest_Neighbor_Reg_Str_Test_Split_L[1]
                #print "X_Str: ", X_Str
                X_Test=float(X_Str)
                Y_Str=Nearest_Neighbor_Reg_Str_Test_Split_L[2]
                Y_Test=float(Y_Str)
                Dist=Distance_Calc(X,Y,X_Test,Y_Test)
                #Cur_Theta_Pixels #
                if(Dist<2.0*Cur_Source_Radius_Pixels):
                    print("Matching Cur_Theta_Arcmin: ", Cur_Theta_Arcmin)
                    print("Matching Counts: ", Counts)
                    print("Cur_Source_Radius_Arcsec: ", Cur_Source_Radius_Arcsec)
                    print("Cur_Source_Radius_Pixels: ", Cur_Source_Radius_Pixels)
                    print("Matching Dist: ", Dist)
                    #"""
                    #print "Region: ", Nearest_Neighbor_Reg_Str
                    ##Nearest_Neighbor_Reg_Str_Reduced=Nearest_Neighbor_Reg_Str.split(";")[1].split(" ")[0]
                    #print "Nearest_Neighbor_Reg_Str_Reduced: ", Nearest_Neighbor_Reg_Str_Reduced
                    #print "Test Region: ", Nearest_Neighbor_Reg_Str_Test
                    Nearest_Neighbor_Reg_Str_Test_Reduced=Nearest_Neighbor_Reg_Str_Test.split(";")[1].split(" ")[0]
                    #print "Nearest_Neighbor_Reg_Str_Test_Reduced: ", Nearest_Neighbor_Reg_Str_Test_Reduced
                    #dmcoords(infile=str(evtfpath),x=float(Cur_X), y=float(Cur_Y), option='sky', verbose=0, celfmt='deg') #Calls dmcoords to get the offaxis angle from the physical coordinates #I should just use the RA and DEC of each X-ray object instead of the SKY coordinate #Note: This is only here for symtax
                    #dmlist "acis_evt2.fits[sky=rotbox(4148,4044,8,22,44.5)]" counts
                    ##Infile_String=evtfpath+"[sky="+Nearest_Neighbor_Reg_Str_Reduced+"]"
                    print("Infile_String: ", Infile_String)
                    Infile_String_Test=evtfpath+"[sky="+Nearest_Neighbor_Reg_Str_Test_Reduced+"]"
                    print("Infile_String_Test: ", Infile_String_Test)
                    Cur_Duplicate_Source_Index_L.append(j)
                    #Duplicate_Source_Index_HL.append()
                    if(j not in Duplicate_Source_Index_L):
                        Duplicate_Source_Index_L.append(j)
                        ##Region_Output=dmlist(infile=str(Infile_String), opt="counts")
                        #print "Region_Output: ", Region_Output
                        ##Region_Test_Output=dmlist(infile=str(Infile_String_Test), opt="counts")
                        #print "Region_Test_Output: ", Region_Test_Output
                        #"""
                        Number_Duplicate_Sources=Number_Duplicate_Sources+1
        Cur_Duplicate_Source_Index_HL=[i,Cur_Duplicate_Source_Index_L]
        Duplicate_Source_Index_HL.append(Cur_Duplicate_Source_Index_HL)
    print("Number_Duplicate_Sources: ", Number_Duplicate_Sources)
    Nearest_Neighbor_Reg_File.close()
    print("Duplicate_Source_Index_L: ", Duplicate_Source_Index_L)
    print("Duplicate_Source_Index_HL: ", Duplicate_Source_Index_HL)
    Duplicate_Source_Fpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Duplicate_Sources.csv"
    Duplicate_Source_File=open(Duplicate_Source_Fpath,"w")
    Duplicate_Source_Header_Str="Source_Num;Duplicate_Sources\n"
    Duplicate_Source_File.write(Duplicate_Source_Header_Str)
    for Cur_Duplicate_Source_Index_L in Duplicate_Source_Index_HL:
        Source_Num=Cur_Duplicate_Source_Index_L[0]+1
        Duplicate_Source_Idx_L=Cur_Duplicate_Source_Index_L[1]
        Duplicate_Source_Num_L=[]
        for Duplicate_Source_Idx in Duplicate_Source_Idx_L:
            Duplicate_Source_Num=Duplicate_Source_Idx+1
            Duplicate_Source_Num_L.append(Duplicate_Source_Num)
        Cur_Line_Str=str(Source_Num)+";"+str(Duplicate_Source_Num_L)+"\n"
        Duplicate_Source_File.write(Cur_Line_Str)
    Duplicate_Source_File.close()
    #return Duplicate_Source_Index_L

def Source_Number_Comparer(ObsID):
    #/Volumes/xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/12888/Raytraced_Sources_ObsID_12888_Coords.csv
    #Raytrace_Coords_Fpath=Root_Path+"xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"+str(ObsID)+"/Raytraced_Sources_ObsID_"+str(ObsID)+"_Coords.csv"
    Raytrace_ObsID_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"+str(ObsID)+"/ObsID_"+str(ObsID)+"_Raytraced_Source_Regions.reg"
    Header_String='# Region file format: DS9 version 3.0\nglobal color=blue font="helvetica 10 normal" select=1 edit=1 move=1 delete=1 include=1 fixed=0\n'
    #Raytrace_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/Detector_Coord_All_Soruces.reg"
    Raytrace_ObsID_Reg_File=open(Raytrace_ObsID_Reg_Fpath)
    Raytrace_ObsID_Reg_Str=Raytrace_ObsID_Reg_File.read()
    #print "Raytrace_ObsID_Reg_Str:\n", Raytrace_ObsID_Reg_Str
    Raytrace_ObsID_Reg_Str_L=Raytrace_ObsID_Reg_Str.split(Header_String)
    #print "Raytrace_ObsID_Reg_Str_L: ", Raytrace_ObsID_Reg_Str_L
    Raytrace_ObsID_Reg_Str_Reduced=Raytrace_ObsID_Reg_Str_L[1]
    #print "Raytrace_ObsID_Reg_Str_Reduced:\n", Raytrace_ObsID_Reg_Str_Reduced
    Raytrace_ObsID_Reg_Str_Reduced_L=Raytrace_ObsID_Reg_Str_Reduced.split("\n")
    #print "Raytrace_ObsID_Reg_Str_Reduced_L: ", Raytrace_ObsID_Reg_Str_Reduced_L
    #print "len(Raytrace_ObsID_Reg_Str_Reduced_L) Before Pop: ", len(Raytrace_ObsID_Reg_Str_Reduced_L)
    Raytrace_ObsID_Reg_Str_Reduced_L.pop(len(Raytrace_ObsID_Reg_Str_Reduced_L)-1)
    #Header_String='# Region file format: DS9 version 3.0\nglobal color=blue font="helvetica 10 normal" select=1 edit=1 move=1 delete=1 include=1 fixed=0\n'
    Nearest_Neighbor_Hybrid_Reg_Fpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
    Nearest_Neighbor_Reg_File=open(Nearest_Neighbor_Hybrid_Reg_Fpath)
    Nearest_Neighbor_Reg_Str=Nearest_Neighbor_Reg_File.read()
    #print "Nearest_Neighbor_Reg_Str:\n", Nearest_Neighbor_Reg_Str
    Nearest_Neighbor_Reg_Str_L=Nearest_Neighbor_Reg_Str.split(Header_String)
    #print "Nearest_Neighbor_Reg_Str_L: ", Nearest_Neighbor_Reg_Str_L
    Nearest_Neighbor_Reg_Str_Reduced=Nearest_Neighbor_Reg_Str_L[1]
    #print "Nearest_Neighbor_Reg_Str_Reduced:\n", Nearest_Neighbor_Reg_Str_Reduced
    Nearest_Neighbor_Reg_Str_Reduced_L=Nearest_Neighbor_Reg_Str_Reduced.split("\n")
    #print "Nearest_Neighbor_Reg_Str_Reduced_L: ", Nearest_Neighbor_Reg_Str_Reduced_L
    #print "len(Nearest_Neighbor_Reg_Str_Reduced_L) Before Pop: ", len(Nearest_Neighbor_Reg_Str_Reduced_L)
    Nearest_Neighbor_Reg_Str_Reduced_L.pop(len(Nearest_Neighbor_Reg_Str_Reduced_L)-1)
    Matching_Source_Num_Fpath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Matching_Source_Number.csv"
    Matching_Source_Num_File=open(Matching_Source_Num_Fpath,"w")
    Source_Number_CSV_Header_String="Raytrace_Source_Num,Nearest_Neighbor_Num\n"
    Matching_Source_Num_File.write(Source_Number_CSV_Header_String)
    Raytrace_Source_Num=1
    for Raytrace_Reg_Str in Raytrace_ObsID_Reg_Str_Reduced_L:
        Raytrace_Reg_Str_Split_L=re.split("[(),]", Raytrace_Reg_Str)
        #print "Raytrace_Reg_Str_Split_L: ", Raytrace_Reg_Str_Split_L
        X_Str=Raytrace_Reg_Str_Split_L[1]
        #print "X_Str: ", X_Str
        X=float(X_Str)
        Y_Str=Raytrace_Reg_Str_Split_L[2]
        Y=float(Y_Str)
        Matching_Nearest_Neighbor_Source_Num_L=[]
        Nearest_Neighbor_Source_Num=1
        for Nearest_Neighbor_Reg_Str in Nearest_Neighbor_Reg_Str_Reduced_L:
            Nearest_Neighbor_Reg_Str_Split_L=re.split("[(),]", Nearest_Neighbor_Reg_Str)
            #print "Nearest_Neighbor_Reg_Str_Split_L: ", Nearest_Neighbor_Reg_Str_Split_L
            X_Str=Nearest_Neighbor_Reg_Str_Split_L[1]
            #print "X_Str: ", X_Str
            X_Test=float(X_Str)
            Y_Str=Nearest_Neighbor_Reg_Str_Split_L[2]
            Y_Test=float(Y_Str)
            Dist=Distance_Calc(X,Y,X_Test,Y_Test)
            print("Dist: ", Dist)
            if(Dist<4.0):
                Matching_Nearest_Neighbor_Source_Num_L.append(Nearest_Neighbor_Source_Num)
            Nearest_Neighbor_Source_Num=Nearest_Neighbor_Source_Num+1
        if(len(Matching_Nearest_Neighbor_Source_Num_L)!=1):
            print("Error: ObsID "+str(ObsID)+" Raytrace_Source_Num "+str(Raytrace_Source_Num)+" has "+str(len(Matching_Nearest_Neighbor_Source_Num_L))+" Matching Source Numbers !")
            print("Matching_Nearest_Neighbor_Source_Num_L: ", Matching_Nearest_Neighbor_Source_Num_L)
        if(len(Matching_Nearest_Neighbor_Source_Num_L)==0):
            Matching_Nearest_Neighbor_Source_Num=None
        else:
            Matching_Nearest_Neighbor_Source_Num=Matching_Nearest_Neighbor_Source_Num_L[0]
        Cur_Match_Str=str(Raytrace_Source_Num)+","+str(Matching_Nearest_Neighbor_Source_Num)+"\n"
        Matching_Source_Num_File.write(Cur_Match_Str)
        Raytrace_Source_Num=Raytrace_Source_Num+1
    Raytrace_ObsID_Reg_File.close()
    Nearest_Neighbor_Reg_File.close()
    Matching_Source_Num_File.close()

def Nearest_Raytraced_Neighbor_Calc_Big_Input(ObsID_L,Generate_Bool=False):
    Header_String='# Region file format: DS9 version 3.0\nglobal color=blue font="helvetica 10 normal" select=1 edit=1 move=1 delete=1 include=1 fixed=0\n'
    Raytrace_Files_Path=Root_Path+"xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"
    #Nearest_Neighbor_Hybrid_All_Soruces_File=open(Raytrace_Files_Path+"Nearest_Neighbor_Hybrid_All_Soruces.reg","w")
    Nearest_Raytraced_Neighbor_FPath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"
    Nearest_Neighbor_Hybrid_All_Soruces_File=open(Nearest_Raytraced_Neighbor_FPath+"Nearest_Neighbor_Hybrid_All_Soruces.reg","w")
    Nearest_Neighbor_Hybrid_All_Soruces_File.write(Header_String)
    Nearest_Neighbor_Hybrid_All_Soruces_L=[]
    for ObsID in ObsID_L:
        if(Generate_Bool):
            Nearest_Raytraced_Neighbor_Calc(ObsID)
            Background_Reg_Generator(ObsID)
            Background_Overlap_Corrected_Reg_Generator(ObsID)
            Duplicate_Source_Remover(ObsID)
            Source_Number_Comparer(ObsID)
        #Nearest_Raytraced_Neighbor_Reg_FPath=Root_Path+"xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
        Nearest_Raytraced_Neighbor_Reg_FPath=Root_Path+"xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
        Nearest_Raytraced_Neighbor_Reg_File=open(Nearest_Raytraced_Neighbor_Reg_FPath)
        Nearest_Raytraced_Neighbor_Reg_Str=Nearest_Raytraced_Neighbor_Reg_File.read()
        Nearest_Raytraced_Neighbor_Reg_Str_L=Nearest_Raytraced_Neighbor_Reg_Str.split("fixed=0\n")
        #print "Nearest_Raytraced_Neighbor_Reg_Str_L: ", Nearest_Raytraced_Neighbor_Reg_Str_L
        Nearest_Raytraced_Neighbor_Reg_Str_Reduced=Nearest_Raytraced_Neighbor_Reg_Str_L[1]
        #print "Nearest_Raytraced_Neighbor_Reg_Str_Reduced:\n", Nearest_Raytraced_Neighbor_Reg_Str_Reduced
        Nearest_Raytraced_Neighbor_Reg_Str_Reduced_L=Nearest_Raytraced_Neighbor_Reg_Str_Reduced.split("\n")
        Nearest_Raytraced_Neighbor_Reg_Str_Reduced_L.pop(len(Nearest_Raytraced_Neighbor_Reg_Str_Reduced_L)-1)
        for Nearest_Raytraced_Neighbor_Reg in Nearest_Raytraced_Neighbor_Reg_Str_Reduced_L:
            Nearest_Neighbor_Hybrid_All_Soruces_L.append(Nearest_Raytraced_Neighbor_Reg+"\n")
    Nearest_Neighbor_Hybrid_All_Soruces_L.sort(key=Reg_Org,reverse=True)
    for Nearest_Neighbor_Hybrid_Source in Nearest_Neighbor_Hybrid_All_Soruces_L:
        Nearest_Neighbor_Hybrid_All_Soruces_File.write(Nearest_Neighbor_Hybrid_Source)
    Nearest_Neighbor_Hybrid_All_Soruces_File.close()


#Nearest_Raytraced_Neighbor_Calc_Big_Input([10125],Generate_Bool=True)
#Nearest_Raytraced_Neighbor_Calc_Big_Input([12888],Generate_Bool=True)
#Background_Overlap_Corrected_Reg_Generator(10125)
#Background_Overlap_Corrected_Reg_Generator(12888)
Source_Number_Comparer(10125)
#Source_Number_Comparer(12888)
#Source_Overlap_Calc_Testing()
#Postion_Error_Plot(Postion_Error_Calc)
#Postion_Error_Plot(Postion_Error_Simple_Calc)
#Nearest_Raytraced_Neighbor_Calc_Big_Input([6096, 1971, 1972, 768, 952, 11674, 13255, 13253, 13246, 12952, 12953, 13247, 12951, 2025, 9548, 2149, 2197, 9510, 6131, 5908, 803, 14342, 12995, 2064, 16024, 12992, 14332, 13202, 793, 2933, 11104, 379, 2056, 2055, 2922, 9506, 11344, 766, 4688, 6869, 6872, 3554, 2057, 2058, 8041, 9121, 9546, 7252, 7060, 9553, 5930, 5931, 5929, 2079, 5905, 9527, 4689, 3947, 1563, 9507, 4613, 794, 11775, 11271, 3951, 2062, 2027, 2060, 2061, 2070, 2032, 7154, 7153, 11779, 5932, 2976, 4613, 794, 1043, 4632, 4631, 4633, 4404, 2059, 12095, 2040, 2915, 4372, 2069, 11229, 7848, 15383, 10125, 2031, 10875, 12889, 12888, 321, 322, 9551, 9550, 3954, 2020, 2068, 4742, 2039, 3150, 2030, 4743, 5197, 11784, 9552],Generate_Bool=True)

#Updated List Without the Erroneously Included NGC 4559 (This is the best and most current version of the sample) #(109 ObsIDs in the sample):
##Nearest_Raytraced_Neighbor_Calc_Big_Input([6096, 1971, 1972, 768, 952, 11674, 13255, 13253, 13246, 12952, 12953, 13247, 12951, 2025, 9548, 2149, 2197, 9510, 6131, 5908, 803, 14342, 12995, 2064, 16024, 12992, 14332, 13202, 793, 2933, 11104, 379, 2056, 2055, 2922, 9506, 11344, 766, 4688, 3554, 2057, 2058, 8041, 9121, 9546, 7252, 7060, 9553, 5930, 5931, 5929, 2079, 5905, 9527, 4689, 3947, 1563, 9507, 4613, 794, 11775, 11271, 3951, 2062, 2060, 2061, 2070, 2032, 7154, 7153, 11779, 5932, 2976, 4613, 794, 1043, 4632, 4631, 4633, 4404, 2059, 12095, 2040, 2915, 4372, 2069, 11229, 7848, 15383, 10125, 2031, 10875, 12889, 12888, 321, 322, 9551, 9550, 3954, 2020, 2068, 4742, 2039, 3150, 2030, 4743, 5197, 11784, 9552],Generate_Bool=True)
#List of all ObsIDs NOT in the galaxy sample (There might be two ObsIDs in there that are included but I can't find them)
#Nearest_Raytraced_Neighbor_Calc_Big_Input([10534, 10985, 10986, 11269, 11358, 11781, 11782, 11783, 11978, 11979, 11988, 11989, 12019, 12124, 12130, 12134, 12136, 12437, 12562, 12668, 12988, 12990, 13726, 13727, 13791, 13830, 13831, 13832, 14031, 14412, 15384, 1575, 1576, 1579, 1580, 1581, 1582, 1584, 1586, 1587, 1611, 1618, 1619, 1622, 1730, 1881, 1967, 2014, 2015, 2022, 2023, 2024, 2026, 2027, 2048, 2049, 2050, 2066, 2067, 2073, 2107, 2147, 2196, 2198, 2223, 2241, 2255, 2454, 2686, 2707, 2779, 2894, 2895, 2896, 2897, 2899, 2900, 2901, 2902, 2950, 3008, 3040, 3042, 3043, 3044, 308, 310, 311, 314, 3149, 3217, 3355, 350, 352, 354, 3550, 3551, 3717, 3718, 3810, 383, 390, 3908, 3931, 3933, 3945, 3950, 4017, 404, 4169, 4177, 4360, 4536, 4541, 4628, 4629, 4630, 4725, 4726, 4732, 4736, 4741, 4747, 4748, 4750, 517, 5309, 5935, 5936, 5937, 5938, 5939, 5940, 5941, 5942, 5943, 5944, 5945, 5946, 5947, 5948, 5949, 6114, 6152, 6167, 6376, 6377, 6380, 6381, 6383, 6385, 6386, 6389, 6862, 6868, 6869, 6870, 6871, 6872, 6873, 7073, 7074, 7075, 7076, 7077, 7078, 7079, 7080, 7081, 7196, 7197, 7198, 7199, 735, 7635, 785, 7853, 786, 788, 797, 8047, 805, 8050, 8057, 8063, 8107, 8182, 8210, 8507, 8554, 9100, 9120, 9122, 934, 9530, 9532, 9535, 9540, 9810],Generate_Bool=True]
#Nearest_Raytraced_Neighbor_Calc_Big_Input([10125], Generate_Bool=True) #For Testing
