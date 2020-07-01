import os
from os import system
import sys
import numpy as np
import re
from ciao_contrib.runtool import *
#import time
dir = os.path.dirname(__file__)
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))
from File_Query_Code import File_Query_Code_5
from Coords_Calc import Coords_Calc
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
    Raytrace_Reg_Fpath="/Volumes/xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/Detector_Coord_All_Soruces.reg"
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
    path_Coords="/Volumes/xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"
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
    Obervations_Path="/Volumes/xray/simon/all_chandra_observations/"
    ObsID_Filepath=Obervations_Path+str(ObsID)+"/primary/"
    Evt2_LS_String=os.popen("ls " +ObsID_Filepath+"| grep 'evt2.fit'").read()
    #print "Evt2_LS_String: ", Evt2_LS_String
    Evt2_LS_String_L=Evt2_LS_String.split("\n")
    #print "Evt2_LS_String_L: ", Evt2_LS_String_L
    Evt2_Fname=Evt2_LS_String_L[0]
    #print "Evt2_Fname: ", Evt2_Fname
    Evt2_Filepath=ObsID_Filepath+Evt2_Fname
    print "Evt2_Filepath: ", Evt2_Filepath
    Untraced_Path=Obervations_Path+str(ObsID)+"/primary/"+str(ObsID)+"_reg.reg" #This needs to be converted to detector coordinates
    Untraced_File=open(Untraced_Path)
    Untraced_Str=Untraced_File.read() # Note: The order of the sources may not be enfored here. It is totaly possible that the soruce are saved in the order of first number how simon did it (For example 1.reg, 10.reg, 11.reg, 2.reg) rather then the way I do it (1.reg, 2.reg...n.reg), Note_Update: Nevermind these are not from trace but wavedect sources the order has no meaning
    #print "Untraced_Str: \n", Untraced_Str
    Untraced_Reg_L=Untraced_Str.split("\n")
    #print "Untraced_Reg_L Before Pop: ", Untraced_Reg_L
    Untraced_Reg_L.pop(len(Untraced_Reg_L)-1)
    #print "Untraced_Reg_L After Pop: ", Untraced_Reg_L
    #for Untraced_Reg in Untraced_Reg_L:
    #Nearest_Neighbor_Hybrid_Reg_Fpath="/Volumes/xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
    Nearest_Neighbor_Hybrid_Reg_Fpath="/Volumes/xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
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
    for Cur_Hybrid_Reg in Nearest_Neighbor_Hybrid_Reg_L:
        #print "Cur_Hybrid_Reg: ", Cur_Hybrid_Reg
        #print "type(Cur_Hybrid_Reg): ", type(Cur_Hybrid_Reg)
        Nearest_Neighbor_Hybrid_Reg_File.write(Cur_Hybrid_Reg) # I don't know if I need to use the X and Y as sky coordinates or detector coordinates if detector coordinates then this must be changed to "Nearest_Neighbor_Hybrid_Reg_File.write(Cur_Hybrid_Reg_Det)", I don't think the shapes of the regions transfered are vaild in detector coodinates so I'm going with sky coordinates now. Also I'm pretty sure calcuationg flux requires sky coords not detector coords
    Raytrace_Reg_File.close()
    Untraced_File.close()
    Nearest_Neighbor_Hybrid_Reg_File.close()

    """
    This creates the Nearest_Neighbor_Hybrid_Sources_Coords.csv Files
    """
    Source_C_L=Coords_Calc.Coords_Calc(Evt2_Filepath,Nearest_Neighbor_Hybrid_Reg_Fpath)
    #print "Source_C_L:\n", Source_C_L
    Nearest_Neighbor_Hybrid_Coord_Outpath="/Volumes/xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/Nearest_Neighbor_Hybrid_Sources_ObsID_"+str(ObsID)+"_Coords.csv"
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
    Nearest_Neighbor_Hybrid_Reg_Fpath="/Volumes/xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
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
    Nearest_Neighbor_Hybrid_BG_Reg_Fpath="/Volumes/xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid_Background.reg"
    Nearest_Neighbor_Hybrid_BG_Reg_File=open(Nearest_Neighbor_Hybrid_BG_Reg_Fpath,"w")
    Nearest_Neighbor_Hybrid_BG_Reg_File.write(Header_String)
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
    Nearest_Neighbor_Hybrid_BG_Reg_File.close()

#Background_Reg_Generator(10125)

def Nearest_Raytraced_Neighbor_Calc_Big_Input(ObsID_L,Generate_Bool=False):
    Header_String='# Region file format: DS9 version 3.0\nglobal color=blue font="helvetica 10 normal" select=1 edit=1 move=1 delete=1 include=1 fixed=0\n'
    Raytrace_Files_Path="/Volumes/xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"
    #Nearest_Neighbor_Hybrid_All_Soruces_File=open(Raytrace_Files_Path+"Nearest_Neighbor_Hybrid_All_Soruces.reg","w")
    Nearest_Raytraced_Neighbor_FPath="/Volumes/xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"
    Nearest_Neighbor_Hybrid_All_Soruces_File=open(Nearest_Raytraced_Neighbor_FPath+"Nearest_Neighbor_Hybrid_All_Soruces.reg","w")
    Nearest_Neighbor_Hybrid_All_Soruces_File.write(Header_String)
    Nearest_Neighbor_Hybrid_All_Soruces_L=[]
    for ObsID in ObsID_L:
        if(Generate_Bool):
            Nearest_Raytraced_Neighbor_Calc(ObsID)
            Background_Reg_Generator(ObsID)
        #Nearest_Raytraced_Neighbor_Reg_FPath="/Volumes/xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
        Nearest_Raytraced_Neighbor_Reg_FPath="/Volumes/xray/anthony/Research_Git/Nearest_Raytraced_Neighbor_Calc/Hybrid_Regions/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
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
Nearest_Raytraced_Neighbor_Calc_Big_Input([6096, 1971, 1972, 768, 952, 11674, 13255, 13253, 13246, 12952, 12953, 13247, 12951, 2025, 9548, 2149, 2197, 9510, 6131, 5908, 803, 14342, 12995, 2064, 16024, 12992, 14332, 13202, 793, 2933, 11104, 379, 2056, 2055, 2922, 9506, 11344, 766, 4688, 6869, 6872, 3554, 2057, 2058, 8041, 9121, 9546, 7252, 7060, 9553, 5930, 5931, 5929, 2079, 5905, 9527, 4689, 3947, 1563, 9507, 4613, 794, 11775, 11271, 3951, 2062, 2027, 2060, 2061, 2070, 2032, 7154, 7153, 11779, 5932, 2976, 4613, 794, 1043, 4632, 4631, 4633, 4404, 2059, 12095, 2040, 2915, 4372, 2069, 11229, 7848, 15383, 10125, 2031, 10875, 12889, 12888, 321, 322, 9551, 9550, 3954, 2020, 2068, 4742, 2039, 3150, 2030, 4743, 5197, 11784, 9552],Generate_Bool=True)
