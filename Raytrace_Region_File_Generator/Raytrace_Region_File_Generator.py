from astropy.io import ascii
import os
from os import system
import sys
import numpy
#import pyregion
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))
from Coords_Calc import Coords_Calc
def File_Num(Fname): #Need to modify to make sure only the number is used. There is a bug where "10new" is used instead of "10"
    Fname_L=Fname.split(".")
    Fname_Number_Str=Fname_L[0]
    Fname_Number_Int=int(Fname_Number_Str) #Some Bug pointed here ! ! ! Seems like a filename I did not consider with the string segment "10new" is casuing an error.
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
    Trace_LS_String=os.popen("ls " +Trace_Path+"| grep '.reg' | grep -v 'bkg' | grep -v '.fits' | grep -v 'new' | grep -v 'sky'").read()
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
        Cur_Reg_File.close()
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
    Det_Coords_Reg_Outpath=path_Obs+"Raytraced_Sources_ObsID_"+str(ObsID)+"_Detector_Coords.reg"
    Det_Coords_Reg_File=open(Det_Coords_Reg_Outpath,"w")
    Det_Coords_Reg_File.write(Header_String)
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
        ##Cur_Reg_Str="detector;Ellipse("4095.41,3893.44,4.12171,3.24946,2.0637) #"
        Cur_Reg_Str="detector;Circle("+str(Det_X)+","+str(Det_Y)+","+str(10)+") #\n" #This needs to be updated to preserve the region shape
        Det_Coords_Reg_File.write(Cur_Reg_Str)
    file2.close()
    Det_Coords_Reg_File.close()
#Raytrace_Region_File_Generator(140)
#Raytrace_Region_File_Generator(10125)

def Raytrace_All_Soucres_Region_File_Generator(ObsID_L,Generate_Bool=False):
    Header_String='# Region file format: DS9 version 3.0\nglobal color=blue font="helvetica 10 normal" select=1 edit=1 move=1 delete=1 include=1 fixed=0\n'
    Raytrace_Files_Path="/Volumes/xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"
    Sky_Coord_All_Soruces_File=open(Raytrace_Files_Path+"Sky_Coord_All_Soruces.reg","w")
    Sky_Coord_All_Soruces_File.write(Header_String)
    Detector_Coord_All_Soruces_File=open(Raytrace_Files_Path+"Detector_Coord_All_Soruces.reg","w")
    Detector_Coord_All_Soruces_File.write(Header_String)
    for ObsID in ObsID_L:
        if(Generate_Bool):
            Raytrace_Region_File_Generator(ObsID)
        Cur_Raytrace_Sky_Path=Raytrace_Files_Path+str(ObsID)+"/ObsID_"+str(ObsID)+"_Raytraced_Source_Regions.reg"
        Cur_Raytrace_Detector_Path=Raytrace_Files_Path+str(ObsID)+"/Raytraced_Sources_ObsID_"+str(ObsID)+"_Detector_Coords.reg"
        Cur_Raytrace_Sky_File=open(Cur_Raytrace_Sky_Path)
        Cur_Raytrace_Sky_Str=Cur_Raytrace_Sky_File.read()
        #print "Cur_Raytrace_Sky_Str: ", Cur_Raytrace_Sky_Str
        Cur_Raytrace_Sky_Str_L=Cur_Raytrace_Sky_Str.split("fixed=0\n")
        #print "Cur_Raytrace_Sky_Str_L: ", Cur_Raytrace_Sky_Str_L
        Cur_Raytrace_Sky_Str_Reduced=Cur_Raytrace_Sky_Str_L[1]
        #print "Cur_Raytrace_Sky_Str_Reduced:\n", Cur_Raytrace_Sky_Str_Reduced
        #print "Cur_Raytrace_Sky_Str_Reduced Sum:\n",Header_String+Cur_Raytrace_Sky_Str_Reduced+Cur_Raytrace_Sky_Str_Reduced
        Sky_Coord_All_Soruces_File.write(Cur_Raytrace_Sky_Str_Reduced)
        Cur_Raytrace_Detector_File=open(Cur_Raytrace_Detector_Path)
        Cur_Raytrace_Detector_Str=Cur_Raytrace_Detector_File.read()
        #print "Cur_Raytrace_Detector_Str: ", Cur_Raytrace_Detector_Str
        Cur_Raytrace_Detector_Str_L=Cur_Raytrace_Detector_Str.split("fixed=0\n")
        #print "Cur_Raytrace_Detector_Str_L: ", Cur_Raytrace_Detector_Str_L
        Cur_Raytrace_Detector_Str_Reduced=Cur_Raytrace_Detector_Str_L[1]
        #print "Cur_Raytrace_Detector_Str_Reduced:\n", Cur_Raytrace_Detector_Str_Reduced
        #print "Cur_Raytrace_Detector_Str_Reduced Sum:\n",Header_String+Cur_Raytrace_Detector_Str_Reduced+Cur_Raytrace_Detector_Str_Reduced
        Detector_Coord_All_Soruces_File.write(Cur_Raytrace_Detector_Str_Reduced)
    Sky_Coord_All_Soruces_File.close()
    Detector_Coord_All_Soruces_File.close()

Raytrace_All_Soucres_Region_File_Generator([10125])
#Raytrace_All_Soucres_Region_File_Generator([6096, 1971, 1972, 768, 952, 11674, 13255, 13253, 13246, 12952, 12953, 13247, 12951, 2025, 9548, 2149, 2197, 9510, 6131, 5908, 803, 14342, 12995, 2064, 16024, 12992, 14332, 13202, 793, 2933, 11104, 379, 2056, 2055, 2922, 9506, 11344, 766, 4688, 6869, 6872, 3554, 2057, 2058, 8041, 9121, 9546, 7252, 7060, 9553, 5930, 5931, 5929, 2079, 5905, 9527, 4689, 3947, 1563, 9507, 4613, 794, 11775, 11271, 3951, 2062, 2027, 2060, 2061, 2070, 2032, 7154, 7153, 11779, 5932, 2976, 4613, 794, 1043, 4632, 4631, 4633, 4404, 2059, 12095, 2040, 2915, 4372, 2069, 11229, 7848, 15383, 10125, 2031, 10875, 12889, 12888, 321, 322, 9551, 9550, 3954, 2020, 2068, 4742, 2039, 3150, 2030, 4743, 5197, 11784, 9552],Generate_Bool=True)
