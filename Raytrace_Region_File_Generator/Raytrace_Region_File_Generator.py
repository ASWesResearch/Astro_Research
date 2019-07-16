from astropy.io import ascii
import os
from os import system
import sys
import numpy
import pyregion
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))
from Coords_Calc import Coords_Calc
def File_Num(Fname):
    Fname_L=Fname.split(".")
    Fname_Number_Str=Fname_L[0]
    Fname_Number_Int=int(Fname_Number_Str)
    return Fname_Number_Int
def Raytrace_Region_File_Generator(ObsID):
    Header_String='# Region file format: DS9 version 3.0\nglobal color=blue font="helvetica 10 normal" select=1 edit=1 move=1 delete=1 include=1 fixed=0\n'
    path_Coords="/Volumes/xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"
    path_Obs=path_Coords+str(ObsID)+'/'
    directory_Obs=os.path.dirname(path_Obs)
    if not os.path.exists(directory_Obs):
        os.makedirs(directory_Obs)
    Raytrace_Reg_Fname="ObsID_"+str(ObsID)+"_Raytraced_Source_Regions.reg"
    Raytrace_Reg_Fpath=path_Obs+Raytrace_Reg_Fname
    print "Raytrace_Reg_Fpath: ", Raytrace_Reg_Fpath
    ObsID_Reg_File=open(Raytrace_Reg_Fpath,"w")
    ObsID_Reg_File.write(Header_String)
    #f=open(ObsID_Reg_File,"w")
    Trace_Path="/Volumes/xray/spirals/trace/"+"/"+str(ObsID)+"/"
    Trace_LS_String=os.popen("ls " +Trace_Path+"| grep '.reg' | grep -v 'bkg' | grep -v '.fits'").read()
    Trace_LS_String_L=Trace_LS_String.split("\n")
    #print "Trace_LS_String_L Before Pop: ", Trace_LS_String_L
    #print "len(Trace_LS_String_L) Before Pop: ", len(Trace_LS_String_L)
    Trace_LS_String_L.pop(len(Trace_LS_String_L)-1)
    #print "Trace_LS_String_L After Pop:", Trace_LS_String_L
    Trace_LS_String_L.sort(key=File_Num)
    #print "Trace_LS_String_L After Sort:", Trace_LS_String_L
    #print "len(Trace_LS_String_L) After Pop:", len(Trace_LS_String_L)
    for Cur_reg_fname in Trace_LS_String_L:
        Cur_reg_fpath=Trace_Path+Cur_reg_fname
        #print "Cur_reg_fpath: ", Cur_reg_fpath
        Cur_Reg_File=open(Cur_reg_fpath)
        #print "Cur_Reg_File: ", Cur_Reg_File
        Cur_Reg_Str=Cur_Reg_File.read()
        #print "Cur_Reg_Str: ", Cur_Reg_Str
        Cur_Reg_Str_L=Cur_Reg_Str.split("\n")
        #print "Cur_Reg_Str_L: ", Cur_Reg_Str_L
        #Cur_Header=Cur_Reg_Str_L[0]+"\n"+Cur_Reg_Str_L[1]+"\n"
        #print "Cur_Header:\n", Cur_Header
        Cur_Shape_Str=Cur_Reg_Str_L[2]
        #print "Cur_Shape_Str: ", Cur_Shape_Str
        #Cur_Shape_Str_L=Cur_Shape_Str.split(";")
        #Cur_Shape_Str_Reduced=Cur_Shape_Str_L[1]
        #ObsID_Reg_File.write(Cur_Shape_Str_Reduced+"\n")
        ObsID_Reg_File.write(Cur_Shape_Str+"\n")
    ObsID_Reg_File.close()
    #return Raytrace_Reg_Fpath
    #/Volumes/xray/simon/all_chandra_observations/10025/primary
    ObsID_Filepath="/Volumes/xray/simon/all_chandra_observations/"+str(ObsID)+"/primary/"
    Evt2_LS_String=os.popen("ls " +ObsID_Filepath+"| grep 'evt2.fit'").read()
    #print "Evt2_LS_String: ", Evt2_LS_String
    Evt2_LS_String_L=Evt2_LS_String.split("\n")
    #print "Evt2_LS_String_L: ", Evt2_LS_String_L
    Evt2_Fname=Evt2_LS_String_L[0]
    #print "Evt2_Fname: ", Evt2_Fname
    Evt2_Filepath=ObsID_Filepath+Evt2_Fname
    print "Evt2_Filepath: ", Evt2_Filepath
    #Reg_Fpath=Raytrace_Region_File_Generator(ObsID)
    #ObsID_Coords_Calc(ObsID,Evt2_Filepath,Raytrace_Reg_Fpath)
    #print "Raytrace_Reg_Fpath Test: ", Raytrace_Reg_Fpath
    #Source_C_L=Coords_Calc.Coords_Calc(Evt2_Filepath,Raytrace_Reg_Fpath,header=Header_String)
    Source_C_L=Coords_Calc.Coords_Calc(Evt2_Filepath,Raytrace_Reg_Fpath)
    #print "Source_C_L:\n", Source_C_L
    Raytraced_Coord_Outpath=path_Obs+"Raytraced_Sources_ObsID_"+str(ObsID)+"_Coords.csv"
    print "Raytraced_Coord_Outpath: ", Raytraced_Coord_Outpath
    file2=open(Raytraced_Coord_Outpath,"w")
    #[Cur_X,Cur_Y,Cur_Chip_X,Cur_Chip_Y,Cur_Chip_ID,Cur_RA,Cur_DEC,Cur_Theta]
    file2.write("Phys_X,Phys_Y,Chip_X,Chip_Y,Chip_ID,RA,DEC,Det_X,Det_Y,Offaxis_Angle"+"\n")
    for Source_C in Source_C_L:
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
#Raytrace_Region_File_Generator(140)
Raytrace_Region_File_Generator(10125)
