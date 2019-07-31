import os
from os import system
import sys
import numpy as np
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
def Distance_Calc(x,y):
    Distance=np.sqrt((x**2.0)+(y**2.0))
    return Distance
def Nearest_Raytraced_Neighbor_Calc(ObsID):
    #For Accessing the Raytraced Region Files:
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
    #For Accessing the Unraytraced Region Files:
    Obervations_Path="/Volumes/xray/simon/all_chandra_observations/"
    Untraced_Path=Obervations_Path+str(ObsID)+"/primary/"+str(ObsID)+"_reg.reg"
    Untraced_File=open(Untraced_Path)
    Untraced_Str=Untraced_File.read()
    print "Untraced_Str: \n", Untraced_Str




Nearest_Raytraced_Neighbor_Calc(10125)
