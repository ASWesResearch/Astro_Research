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
def File_Num(Fname): #Need to modify to make sure only the number is used. There is a bug where "10new" is used instead of "10"
    Fname_L=Fname.split(".")
    Fname_Number_Str=Fname_L[0]
    Fname_Number_Int=int(Fname_Number_Str) #Some Bug pointed here ! ! ! Seems like a filename I did not consider with the string segment "10new" is casuing an error.
    return Fname_Number_Int
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
    Nearest_Neighbor_Hybrid_Reg_Fpath="/Volumes/xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"+str(ObsID)+"/"+str(ObsID)+"_Nearest_Neighbor_Hybrid.reg"
    Nearest_Neighbor_Hybrid_Reg_File=open(Nearest_Neighbor_Hybrid_Reg_Fpath,"w")
    Nearest_Neighbor_Hybrid_Reg_File.write(Header_String)
    for i in range(0,len(Untraced_Reg_L)):
    #for i in range(0,1): #This is a TEST
        Cur_Min_Distance=100000 #Much larger then any distance expected to be encoutered
        Cur_Min_Index=0
        Untraced_Reg=Untraced_Reg_L[i]
        Cur_Reg_String_L=re.split("[(),]",Untraced_Reg)
        print "Cur_Reg_String_L: ", Cur_Reg_String_L
        Cur_X_Str=Cur_Reg_String_L[1]
        Cur_X=float(Cur_X_Str)
        Cur_Y_Str=Cur_Reg_String_L[2]
        Cur_Y=float(Cur_Y_Str)
        dmcoords(infile=str(Evt2_Filepath),x=float(Cur_X), y=float(Cur_Y), option='sky', verbose=0, celfmt='deg') #Calls dmcoords to get the offaxis angle from the physical coordinates #I should just use the RA and DEC of each X-ray object instead of the SKY coordinate
        Cur_Det_X=dmcoords.detx
        print "Cur_Det_X : ", Cur_Det_X
        Cur_Det_Y=dmcoords.dety
        print "Cur_Det_Y : ", Cur_Det_Y
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
        print "Cur_Min_Distance: ", Cur_Min_Distance
        print "Nearest_Raytraced_Neighbor_Reg: ", Nearest_Raytraced_Neighbor_Reg
        Nearest_Raytraced_Neighbor_Reg_Str_L=re.split("[(),]",Nearest_Raytraced_Neighbor_Reg)
        print "Nearest_Raytraced_Neighbor_Reg_Str_L: ", Nearest_Raytraced_Neighbor_Reg_Str_L
        #Cur_Hybrid_Reg=Cur_Reg_String_L[0]+"("+Nearest_Raytraced_Neighbor_Reg_Str_L[1]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[2]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[3]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[4]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[5]+")\n"
        Cur_Hybrid_Reg=Nearest_Raytraced_Neighbor_Reg_Str_L[0]+"("+Cur_Reg_String_L[1]+","+Cur_Reg_String_L[2]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[3]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[4]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[5]+")"+Nearest_Raytraced_Neighbor_Reg_Str_L[6]+"\n"
        print "Cur_Hybrid_Reg: ", Cur_Hybrid_Reg
        Cur_Hybrid_Reg_Det=Nearest_Raytraced_Neighbor_Reg_Str_L[0]+"("+str(Cur_Det_X)+","+str(Cur_Det_Y)+","+Nearest_Raytraced_Neighbor_Reg_Str_L[3]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[4]+","+Nearest_Raytraced_Neighbor_Reg_Str_L[5]+")"+Nearest_Raytraced_Neighbor_Reg_Str_L[6]+"\n"
        print "Cur_Hybrid_Reg_Det: ", Cur_Hybrid_Reg_Det
        Nearest_Neighbor_Hybrid_Reg_File.write(Cur_Hybrid_Reg) # I don't know if I need to use the X and Y as sky coordinates or detector coordinates if detector coordinates then this must be changed to "Nearest_Neighbor_Hybrid_Reg_File.write(Cur_Hybrid_Reg_Det)", I don't think the shapes of the regions transfered are vaild in detector coodinates so I'm going with sky coordinates now. Also I'm pretty sure calcuationg flux requires sky coords not detector coords
    Raytrace_Reg_File.close()
    Untraced_File.close()
    Nearest_Neighbor_Hybrid_Reg_File.close()

Nearest_Raytraced_Neighbor_Calc(10125)
