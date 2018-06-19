import subprocess
import threading
from threading import Thread
import os
from os import system
import sys
import gzip
#import time
dir = os.path.dirname(__file__)
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))
from Histogram_Code import Galaxy_Histogram_Code_3
from File_Query_Code import File_Query_Code_5
from XPA_DS9_Region_Generator import XPA_DS9_Region_Generator_3
#from CCD_Region_Testing import Simple_Region_Generator_8
from Simple_Region_Generator import Simple_Region_Generator_9
from Area_Calc import Area_Calc_Frac_B_2_Alt_8
from Galaxy_Name_Reducer import Galaxy_Name_Reducer
#from File_Query_Code import File_Query_Code_5
from Source_Region_Generator import Source_Region_Generator_Radius_Modifed_V3
from Background_Finder import Background_Finder_10
from Detection_Probablity_Calc import Detection_Probability_Calc_7
from Known_Flux_Finder import Known_Flux_Finder
from Counts_To_Flux_Converter import Counts_To_Flux_Converter_3
#from Galaxy_Name_Reducer import Galaxy_Name_Reducer
from Coords_Calc import Coords_Calc
def Pipeline_A(Gname_L):
    """
    #Imports alaxy_Histogram_Code_2
    #os.system('python Hello_World.py')
    #dir = os.path.dirname(__file__)
    #path=os.path.realpath('../GitHub/Galaxy_Histogram_Code.py') #Need to modify so it is possible to input Gname to the Galaxy_Histogram_Code
    #print "Path=",path
    #system('pwd')
    #os.system('python '+path) #Runs Galaxy_Histogram_Code.py
    #os.system('python Hello_World.py')
    dir = os.path.dirname(__file__)
    #path=os.path.realpath('../GitHub/Galaxy_Histogram_Code_2.py')
    path=os.path.realpath('../')
    #print "Path=",path
    #system('pwd')
    #os.system('python '+path) #This works when inputs are not used
    #import Galaxy_Histogram_Code_2
    #Driver_Code('NGC4258')
    sys.path.append(os.path.abspath(path))
    #print sys.path
    #from Galaxy_Histogram_Code_2 import *
    #import Galaxy_Histogram_Code_2
    from Histogram_Code import Galaxy_Histogram_Code_3
    """
    for Gname in Gname_L:
        #Pipeline_A Code
        print "Gname A: ", Gname
        Galaxy_Histogram_Code_3.Driver_Code(Gname) #This runs the histrogram code and creates the histrograms and the directories with the histrograms in them

# Pipelines are quoted until they are finished

def Pipeline_B(Gname_L):
    """
    dir = os.path.dirname(__file__)
    path=os.path.realpath('../')
    #print "Path=",path
    #system('pwd')
    sys.path.append(os.path.abspath(path))
    #print sys.path
    from File_Query_Code import File_Query_Code_5
    from XPA_DS9_Region_Generator import XPA_DS9_Region_Generator_3
    #from CCD_Region_Testing import Simple_Region_Generator_8
    from Simple_Region_Generator import Simple_Region_Generator_9
    from Area_Calc import Area_Calc_Frac_B_2_Alt_8
    from Galaxy_Name_Reducer import Galaxy_Name_Reducer
    """
    for Gname in Gname_L:
        #Pipeline_B Code
        print "Gname B: ", Gname
        """
        Gname_List=Gname.split(" ")
        print "Gname_List: ", Gname_List
        if(len(Gname_List)>1):
            Gname_Modifed=Gname_List[0]+"_"+Gname_List[1] #Adds underscore to remove space from "NGC #" to change to "NGC_#" if there is a space in the name
        else:
            Gname_Modifed=Gname # Does nothing if the galaxy name has no space, ie. NGC#, For example NGC253 instead of NGC 253 or NGC_253
        """
        Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
        #print "Gname_Modifed ", Gname_Modifed
        path_2=os.path.realpath('../Master_Code/Master_Output/')
        path_3=path_2+'/'+Gname_Modifed+'/'
        directory = os.path.dirname(path_3)
        if not os.path.exists(directory):
            os.makedirs(directory)
        #os.chdir(path_3) #Goes to Current Galaxies Folder
        path_Area=path_3+'Area_Lists/'
        directory_Area=os.path.dirname(path_Area)
        if not os.path.exists(directory_Area):
            os.makedirs(directory_Area)
        #print "path_Area=",path_Area
        #os.chdir(path_Area)
        """
        Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
        Reg_File_H_L=File_Query_Code_5.File_Query(Gname,"reg",".reg")
        print "Evt2_File_H_L ", Evt2_File_H_L
        print "Reg_File_H_L ", Reg_File_H_L
        for Evt2_File_L in Evt2_File_H_L:
            Cur_Evt2_ObsID=Evt2_File_L[0]
            Cur_Evt2_Filepath=Evt2_File_L[1]
            for Reg_File_L in Reg_File_H_L:
                Cur_Reg_ObsID=Reg_File_L[0]
                Cur_Reg_Filepath=Reg_File_L[1]
                if(Cur_Evt2_ObsID==Cur_Reg_ObsID):
                    #print "Test"
                    path_Obs=path_Area+'/'+str(Cur_Evt2_ObsID)+'/'
                    directory_Obs=os.path.dirname(path_Obs)
                    if not os.path.exists(directory_Obs):
                        os.makedirs(directory_Obs)
                    os.chdir(path_Obs)
                    print "THE PWD AT END IS :"
                    system('pwd')
                    XPA_DS9_Region_Generator_3.XPA_DS9_Region_Generator(Cur_Evt2_Filepath,Cur_Reg_Filepath)
                    #Simple_Region_Generator_8.Simple_Region_Generator('foo2','acisf03931_repro_evt2.fits')
        path_5=os.path.realpath('../../../../')
        os.chdir(path_5)
        #print "THE PWD AT END IS :"
        #system('pwd')
        #Need to add the rest of Pipeline B after XPA_DS9_Region_Generator
        """
        Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
        #Reg_File_H_L=File_Query_Code_5.File_Query(Gname,"reg",".reg")
        Fov_File_H_L=File_Query_Code_5.File_Query(Gname,"fov1")
        #print "Evt2_File_H_L ", Evt2_File_H_L
        #print "Fov_File_H_L ", Fov_File_H_L
        for Evt2_File_L in Evt2_File_H_L:
            Cur_Evt2_ObsID=Evt2_File_L[0]
            Cur_Evt2_Filepath=Evt2_File_L[1]
            for Fov_File_L in Fov_File_H_L:
                Cur_Fov_ObsID=Fov_File_L[0]
                Cur_Fov_Filepath=Fov_File_L[1]
                if(Cur_Evt2_ObsID==Cur_Fov_ObsID):
                    #print "Test"
                    #path_Obs=path_Area+'/'+str(Cur_Evt2_ObsID)+'/'
                    path_Obs=path_Area+str(Cur_Evt2_ObsID)+'/'
                    directory_Obs=os.path.dirname(path_Obs)
                    if not os.path.exists(directory_Obs):
                        os.makedirs(directory_Obs)
                    #os.chdir(path_Obs) #This os.chdir actullay effects the outcome of the code
                    #print "path_Obs : ", path_Obs
                    #print "THE PWD AT END IS :"
                    #system('pwd')
                    #print "CURRENT FOV FILEPATH IS :", Cur_Fov_Filepath
                    Cur_Fov_Filename_L=Cur_Fov_Filepath.split("/")
                    #print "Cur_FOV_Filename_L : ",Cur_Fov_Filename_L
                    Cur_Fov_Filepath_No_Fname_L=Cur_Fov_Filepath.rsplit("/",1)
                    #print "Cur_Fov_Filepath_No_Fname_L : ",Cur_Fov_Filepath_No_Fname_L
                    Cur_Fov_Filepath_No_Fname=Cur_Fov_Filepath_No_Fname_L[0]
                    #print "Cur_Fov_Filepath_No_Fname : ",Cur_Fov_Filepath_No_Fname
                    Cur_Fov_Filename=Cur_Fov_Filename_L[len(Cur_Fov_Filename_L)-1]
                    #print "Cur_Fov_Filename : ",Cur_Fov_Filename
                    Cur_Fov_Filename_Ext_L=Cur_Fov_Filename.split(".")
                    #print "Cur_Fov_Filename_Ext_L : ",Cur_Fov_Filename_Ext_L
                    Cur_Fov_Filename_Ext=Cur_Fov_Filename_Ext_L[len(Cur_Fov_Filename_Ext_L)-1]
                    #print "Cur_Fov_Filename_Ext : ", Cur_Fov_Filename_Ext
                    if(Cur_Fov_Filename_Ext=="gz"): #Need to test this later with a compressed fits file
                        Output_Fov_Filename=Cur_Fov_Filename_Ext_L[0]+"."+Cur_Fov_Filename_Ext_L[1]
                        #os.chdir(path_Obs)
                        #Cur_Fov_Filepath
                        #os.chdir(Cur_Fov_Filepath_No_Fname)
                        #system('pwd')
                        Output_Fov_Filepath=Cur_Fov_Filepath_No_Fname+"/"+Output_Fov_Filename
                        #print "Output_Fov_Filepath : ",Output_Fov_Filepath
                        #inF = gzip.open(Cur_Fov_Filename, 'rb')
                        #outF = open(Output_Fov_Filename, 'wb')
                        inF = gzip.open(Cur_Fov_Filepath, 'rb')
                        outF = open(Output_Fov_Filepath, 'wb')
                        outF.write( inF.read() )
                        inF.close()
                        outF.close()
                        #os.chdir(path_Obs)
                        Cur_Fov_Filepath=Output_Fov_Filepath
                    #print "Cur_Evt2_Filepath : ", Cur_Evt2_Filepath
                    #print "Cur_Fov_Filepath : ", Cur_Fov_Filepath
                    XPA_DS9_Region_Generator_3.XPA_DS9_Region_Generator(Cur_Evt2_Filepath,Cur_Fov_Filepath,path_Obs) #Need to update file output location
                    #print "The Filepath Before End is : "
                    #system('pwd')
                    #time.sleep(10.0)
                    Region_File_LS= os.popen("ls "+path_Obs).read()
                    #print "Region_File_LS : ", Region_File_LS
                    Region_File_LS_L=Region_File_LS.split("\n")
                    #print "Region_File_LS_L : ",Region_File_LS_L
                    for Region_Filename_Test in Region_File_LS_L:
                        Region_Filename_Test_L=Region_Filename_Test.split("_")
                        #print "Region_Filename_Test_L : ",Region_Filename_Test_L
                        #if(len(Region_Filename_Test_L)==4):
                            #Region_Filename=Region_Filename_Test
                        if(("modifed" not in Region_Filename_Test) and ("CCD" in Region_Filename_Test)):
                            Region_Filename=Region_Filename_Test
                    #print "Region_Filename : ",Region_Filename
                    #This_is_Ment_To_Break_The_Code
                    Simple_Region_Generator_9.Simple_Region_Generator(Region_Filename,Cur_Evt2_Filepath,path_Obs) #Need to update file output location
                    #print "Cur_Evt2_Filepath: ", Cur_Evt2_Filepath
                    #Area_Calc_Frac_B_2_Alt_2("NGC 253","/Network/Servers/vimes.astro.wesleyan.edu/Volumes/vvodata/home/asantini/Desktop/CCD_Incompleteness_Correction/Area_Calc/acisf13830_repro_evt2.fits","acisf13830_repro_CCD_Regions_simple_region_modifed_Code.txt")
                    #print "The Filepath Before LS Delay"
                    #system('pwd')
                    #time.sleep(10.0)
                    Simple_Region_File_LS= os.popen("ls "+path_Obs).read()
                    #print "Simple_Region_File_LS : ", Simple_Region_File_LS
                    #print "The Filepath Before LS Delay"
                    #system('pwd')
                    Simple_Region_File_LS_L=Simple_Region_File_LS.split("\n")
                    #print "Simple_Region_File_LS_L : ",Simple_Region_File_LS_L
                    for Simple_Region_Filename_Test in Simple_Region_File_LS_L:
                        Simple_Region_Filename_Test_L=Simple_Region_Filename_Test.split("_")
                        #print "Simple_Region_Filename_Test_L : ",Simple_Region_Filename_Test_L
                        #if(len(Simple_Region_Filename_Test_L)==8):
                            #Simple_Region_Filename=Simple_Region_Filename_Test
                        if(("modifed" in Simple_Region_Filename_Test_L) and ("no" not in Simple_Region_Filename_Test_L)):
                            Simple_Region_Filename=Simple_Region_Filename_Test
                    #print "Simple_Region_Filename : ",Simple_Region_Filename
                    Simple_Region_Filepath=path_Obs+Simple_Region_Filename
                    #print "Simple_Region_Filepath : ", Simple_Region_Filepath
                    #Area_Calc_Frac_B_2_Alt_8.Area_Calc_Frac_B_2_Alt_2(Gname,Simple_Region_Filename,Cur_Evt2_Filepath)
                    #Cur_Area_L=Area_Calc_Frac_B_2_Alt_8.Area_Calc_Frac_B_2_Alt_2(Gname,Cur_Evt2_Filepath,Simple_Region_Filename)
                    Cur_Area_L=Area_Calc_Frac_B_2_Alt_8.Area_Calc_Frac_B_2_Alt_2(Gname,Cur_Evt2_Filepath,Simple_Region_Filepath)
                    #print Cur_Area_L
                    #system('pwd')
                    #Simple_Region_Filename_L=Simple_Region_Filename.split("CCD")
                    #print "Simple_Region_Filename_L : ",Simple_Region_Filename_L
                    #Simple_Region_Filename_Reduced=Simple_Region_Filename_L[0]
                    #print "Simple_Region_Filename_Reduced : ",Simple_Region_Filename_Reduced
                    #Area_List_Filename=Simple_Region_Filename_Reduced+"Area_List.txt"
                    #print "Area_List_Filename : ",Area_List_Filename
                    #print "fovfname_reduced : ",fovfname_reduced
                    #print "Cur_Evt2_Filepath : ",Cur_Evt2_Filepath
                    #Cur_Evt2_Filepath_L=Cur_Evt2_Filepath.split("/")
                    #print "Cur_Evt2_Filepath_L : ",Cur_Evt2_Filepath_L
                    #Cur_Evt2_Filename=Cur_Evt2_Filepath_L[len(Cur_Evt2_Filepath_L)-1]
                    #print "Cur_Evt2_Filename : ",Cur_Evt2_Filename
                    """
                    Area_Calc_File=open(Area_List_Filename,"w")
                    for Cur_Area in Cur_Area_L:
                        if (Cur_Area==False):
                            #Area_Calc_File.write("Invalid_Observation:GC_Outside_Chandra_FOV")
                            for i in range (0,10):
                                print "Area Circle Outside Chandra FOV"
                            break
                        Cur_Area_Str=str(Cur_Area)
                        Area_Calc_File.write(Cur_Area_Str +"\n")
                    #This_is_Ment_To_Break_The_Code
                    """
                    #print "PWD before Path_5 : "
                    #system('pwd')
        #path_5=os.path.realpath('../../../../')
        #print "path_5 : ",path_5
        #os.chdir(path_5)
        #print "THE PWD AT VERY END IS :"
        #system('pwd')
        #Need to add the rest of Pipeline B after XPA_DS9_Region_Generator

def Pipeline_C(Gname_L):
    """
    dir = os.path.dirname(__file__)
    #print "dir : ", dir
    #print "PWD C : "
    #system('pwd')
    path=os.path.realpath('../')
    #print "Path=",path
    #system('pwd')
    #print "Before : "
    #print sys.path
    sys.path.append(os.path.abspath(path))
    #print "After : "
    #print sys.path
    #print "Modules PWD : "
    #system('pwd')
    #print sys.path
    #Import Desktop Modules Here !!!
    from File_Query_Code import File_Query_Code_5
    from Source_Region_Generator import Source_Region_Generator_Radius_Modifed_V3
    from Background_Finder import Background_Finder_10
    from Detection_Probablity_Calc import Detection_Probability_Calc_7
    from Known_Flux_Finder import Known_Flux_Finder
    from Counts_To_Flux_Converter import Counts_To_Flux_Converter_3
    from Galaxy_Name_Reducer import Galaxy_Name_Reducer
    """
    for Gname in Gname_L:
        #Pipeline_C Code
        print "Gname C: ", Gname
        """
        Gname_List=Gname.split(" ")
        print "Gname_List: ", Gname_List
        if(len(Gname_List)>1):
            Gname_Modifed=Gname_List[0]+"_"+Gname_List[1] #Adds underscore to remove space from "NGC #" to change to "NGC_#" if there is a space in the name
        else:
            Gname_Modifed=Gname # Does nothing if the galaxy name has no space, ie. NGC#, For example NGC253 instead of NGC 253 or NGC_253
        """
        #print "PWD C 2 : "
        #system('pwd')
        Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
        #print "Gname_Modifed ", Gname_Modifed
        #print "PWD C 3 : "
        #system('pwd')
        path_2=os.path.realpath('../Master_Code/Master_Output/')
        #print "path_2 : ", path_2
        path_3=path_2+'/'+Gname_Modifed+'/'
        #print "path_3 : ", path_3
        directory = os.path.dirname(path_3)
        if not os.path.exists(directory):
            os.makedirs(directory)
        #os.chdir(path_3) #Goes to Current Galaxies Folder
        path_Flux_90=path_3+'Flux_90_Files/'
        #print "path_Flux_90 : ", path_Flux_90
        directory_Flux_90=os.path.dirname(path_Flux_90)
        if not os.path.exists(directory_Flux_90):
            os.makedirs(directory_Flux_90)
        #print "path_Flux_90=",path_Flux_90
        #os.chdir(path_Flux_90)
        Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
        Reg_File_H_L=File_Query_Code_5.File_Query(Gname,"reg",".reg")
        #print "Evt2_File_H_L ", Evt2_File_H_L
        #print "Reg_File_H_L ", Reg_File_H_L
        for Evt2_File_L in Evt2_File_H_L:
            Cur_Evt2_ObsID=Evt2_File_L[0]
            Cur_Evt2_Filepath=Evt2_File_L[1]
            for Reg_File_L in Reg_File_H_L:
                Cur_Reg_ObsID=Reg_File_L[0]
                Cur_Reg_Filepath=Reg_File_L[1]
                if(Cur_Evt2_ObsID==Cur_Reg_ObsID):
                    #print "Test"
                    #path_Obs=path_Flux_90+'/'+str(Cur_Evt2_ObsID)+'/'
                    #print "Cur_Evt2_ObsID : ",Cur_Evt2_ObsID
                    #print "type(Cur_Evt2_ObsID) : ",type(Cur_Evt2_ObsID)
                    #print "Cur_Evt2_Filepath : ", Cur_Evt2_Filepath
                    #Cur_Evt2_Filepath_L=Cur_Evt2_Filepath.split("/")
                    #print "Cur_Evt2_Filepath_L : ",Cur_Evt2_Filepath_L
                    #Cur_Evt2_Filename=Cur_Evt2_Filepath_L[-1]
                    #print "Cur_Evt2_Filename : ", Cur_Evt2_Filename
                    path_Obs=path_Flux_90+str(Cur_Evt2_ObsID)+'/'
                    directory_Obs=os.path.dirname(path_Obs)
                    if not os.path.exists(directory_Obs):
                        os.makedirs(directory_Obs)
                    #print "path_Obs : ", path_Obs
                    #os.chdir(path_Obs)
                    #Cur_Evt2_Filepath_Full=path_Obs+Cur_Evt2_Filename
                    #print "path_Obs : ", path_Obs
                    #print "Cur_Evt2_Filepath_Full : ", Cur_Evt2_Filepath_Full
                    #print "THE PWD AT END IS :"
                    #system('pwd')
                    Source_Region_Generator_Radius_Modifed_V3.Source_Region_Generator_Radius_Modifed_V3(Gname,path_Obs)
                    if(Gname[3]==" "):
                        Gname_Underscore=Gname.replace(Gname[3], "_", 1)
                    elif(Gname[3]!="_"):
                        Gname_Underscore_L=Gname.split(Gname[2])
                        #print "Gname_Underscore_L : ",Gname_Underscore_L
                        Gname_Underscore=Gname_Underscore_L[0]+Gname[2]+"_"+Gname_Underscore_L[1]
                    #print "Gname_Underscore Master : ", Gname_Underscore
                    #NGC_4258_ObsID_1618_Source_Regions_Radius_Modifed.txt
                    ObjF_Filename=Gname_Underscore+"_ObsID_"+str(Cur_Evt2_ObsID)+"_Source_Regions_Radius_Modifed.txt"
                    ObjF_Filepath=path_Obs+ObjF_Filename
                    #print "ObjF_Filepath : ", ObjF_Filepath
                    BG_Radius=50
                    while (BG_Radius>20):
                        #Background_Finder_3(gname,evtfpath,objLfname,R)
                        Background_Ratio=Background_Finder_10.Background_Finder_3(Gname,Cur_Evt2_Filepath,ObjF_Filepath,BG_Radius)
                        if(Background_Ratio != "None_Found"):
                            break
                        BG_Radius=BG_Radius-10
                    #print "Background_Ratio : ", Background_Ratio
                    Background_Ratio_L=[Background_Ratio]
                    #D_P_C_Big_Input_90_Per_Check(Backgrounds,Off_Angs,C_Min=2,C_Max=110)
                    #print "THE PWD AT END IS :"
                    #system('pwd')
                    #path_4=os.path.realpath('../../../../')
                    #print "path_4 : ",path_4
                    #os.chdir(path_4)
                    #print "Output : ",Detection_Probability_Calc_7.D_P_C_Big_Input_90_Per_Check(Background_Ratio_L)
                    #system('pwd')
                    C_90_Per_First_L_H=Detection_Probability_Calc_7.D_P_C_Big_Input_90_Per_Check(Background_Ratio_L)
                    #print "C_90_Per_First_L_H : ", C_90_Per_First_L_H
                    #os.chdir(path_Obs)
                    #print "THE PWD AT END IS :"
                    #system('pwd')
                    #Known_Flux_Finder('NGC2403','acisf02014_repro_evt2.fits')
                    Known_Flux=Known_Flux_Finder.Known_Flux_Finder(Gname,Cur_Evt2_Filepath)
                    #print "Known_Flux : ",Known_Flux
                    Known_Flux_L=[Known_Flux]
                    #print "Known_Flux_L : ",Known_Flux_L
                    Flux_90_L_H=Counts_To_Flux_Converter_3.Counts_To_Flux_Converter(C_90_Per_First_L_H,Known_Flux_L)
                    #print "Flux_90_L_H : ", Flux_90_L_H
                    #print "THE PWD AT END IS :"
                    #system('pwd')
                    #os.chdir(path_Obs)
                    #print "THE PWD AT END IS :"
                    #system('pwd')
                    Flux_90_L=Flux_90_L_H[0]
                    #print "Flux_90_L : ", Flux_90_L
                    #NGC_4258_ObsID_1618
                    file=open(path_Obs+Gname_Modifed+"_ObsID_"+str(Cur_Evt2_ObsID)+"_Flux_90.txt","w")
                    file.write("Background_Ratio:"+str(Background_Ratio)+"|"+"\n")
                    for Flux_90 in Flux_90_L:
                        file.write(str(Flux_90)+"\n")
        #path_5=os.path.realpath('../../../../')
        #print "path_5 : ",path_5
        #os.chdir(path_5)
        #print "THE PWD AT VERY END IS :"
        #system('pwd')

def Pipeline_D(Gname_L):
    """
    dir = os.path.dirname(__file__)
    path=os.path.realpath('../')
    #print "Path=",path
    #system('pwd')
    sys.path.append(os.path.abspath(path))
    #print sys.path
    from File_Query_Code import File_Query_Code_5
    from Coords_Calc import Coords_Calc
    from Galaxy_Name_Reducer import Galaxy_Name_Reducer
    """
    for Gname in Gname_L:
        #Pipeline_D Code
        print "Gname D: ", Gname
        Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
        #print "Gname_Modifed ", Gname_Modifed
        path_2=os.path.realpath('../Master_Code/Master_Output/')
        path_3=path_2+'/'+Gname_Modifed+'/'
        directory = os.path.dirname(path_3)
        if not os.path.exists(directory):
            os.makedirs(directory)
        #os.chdir(path_3) #Goes to Current Galaxies Folder
        path_Coords=path_3+'Coords_Lists/'
        directory_Coords=os.path.dirname(path_Coords)
        if not os.path.exists(directory_Coords):
            os.makedirs(directory_Coords)
        #print "path_Coords=",path_Coords
        Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
        Reg_File_H_L=File_Query_Code_5.File_Query(Gname,"reg",".reg")
        #print "Evt2_File_H_L ", Evt2_File_H_L
        #print "Reg_File_H_L ", Reg_File_H_L
        for Evt2_File_L in Evt2_File_H_L:
            Cur_Evt2_ObsID=Evt2_File_L[0]
            Cur_Evt2_Filepath=Evt2_File_L[1]
            for Reg_File_L in Reg_File_H_L:
                Cur_Reg_ObsID=Reg_File_L[0]
                Cur_Reg_Filepath=Reg_File_L[1]
                if(Cur_Evt2_ObsID==Cur_Reg_ObsID):
                    #print "Test"
                    #path_Obs=path_Flux_90+'/'+str(Cur_Evt2_ObsID)+'/'
                    #print "Cur_Evt2_ObsID : ",Cur_Evt2_ObsID
                    #print "type(Cur_Evt2_ObsID) : ",type(Cur_Evt2_ObsID)
                    #print "Cur_Evt2_Filepath : ", Cur_Evt2_Filepath
                    #print "Cur_Reg_Filepath : ", Cur_Reg_Filepath
                    path_Obs=path_Coords+str(Cur_Evt2_ObsID)+'/'
                    directory_Obs=os.path.dirname(path_Obs)
                    if not os.path.exists(directory_Obs):
                        os.makedirs(directory_Obs)
                    #print "path_Obs : ", path_Obs
                    #os.chdir(path_Obs)
                    #Cur_Evt2_Filepath_Full=path_Obs+Cur_Evt2_Filename
                    #print "path_Obs : ", path_Obs
                    Source_C_L=Coords_Calc.Coords_Calc(Cur_Evt2_Filepath,Cur_Reg_Filepath)
                    #print "PWD AT THE END : "
                    #system('pwd')
                    file2=open(path_Obs+Gname_Modifed+"_ObsID_"+str(Cur_Evt2_ObsID)+"_Coords.csv","w")
                    #[Cur_X,Cur_Y,Cur_Chip_X,Cur_Chip_Y,Cur_Chip_ID,Cur_RA,Cur_DEC,Cur_Theta]
                    file2.write("Phys_X,Phys_Y,Chip_X,Chip_Y,Chip_ID,RA,DEC,Offaxis_Angle"+"\n")
                    for Source_C in Source_C_L:
                        Phys_X=Source_C[0]
                        Phys_Y=Source_C[1]
                        Chip_X=Source_C[2]
                        Chip_Y=Source_C[3]
                        Chip_ID=Source_C[4]
                        RA=Source_C[5]
                        DEC=Source_C[6]
                        Offaxis_Angle=Source_C[7]
                        file2.write(str(Phys_X)+","+str(Phys_Y)+","+str(Chip_X)+","+str(Chip_Y)+","+str(Chip_ID)+","+str(RA)+","+str(DEC)+","+str(Offaxis_Angle)+"\n")
        #path_5=os.path.realpath('../../../../')
        #print "path_5 : ",path_5
        #os.chdir(path_5)
        #print "THE PWD AT VERY END IS :"
        #system('pwd')

def Master(Gname_L):
    Thread(target = Pipeline_A(Gname_L)).start()
    Thread(target = Pipeline_B(Gname_L)).start()
    Thread(target = Pipeline_C(Gname_L)).start()
    Thread(target = Pipeline_D(Gname_L)).start()
    print "Number of Threads : ", str(threading.activeCount())
    print "Master Complete"

"""
def Master(Gname_L):
    A=Thread(target = Pipeline_A, args=(Gname_L,))
    B=Thread(target = Pipeline_B, args=(Gname_L,))
    C=Thread(target = Pipeline_C, args=(Gname_L,))
    D=Thread(target = Pipeline_D, args=(Gname_L,))
    A.start()
    B.start()
    C.start()
    D.start()
    print "Number of Threads : ", str(threading.activeCount())
    print "Master Complete"
"""
if __name__ == '__main__':
    #Master(['NGC4258','M31','NGC 1365']) #This works
    #Master(['NGC4258','NGC 1332'])
    #Master(['NGC4258','NGC 1365'])
    #Master(['NGC4258'])
    Master(['NGC 4449', 'NGC 6946', 'Willman 1', 'NGC 602', 'SN 2004am', 'SN 1996aq', 'NGC 4278', 'DDO 68', 'NGC7507', 'PGC135659', 'NGC 5054', 'NGC1300', 'NGC4742', 'NGC5576', 'NGC3384', 'NGC4486A', 'NGC4459', '3C 299', 'NGC3115', 'NGC 247', 'PTF11eon', 'SN2011dh', 'NGC 4472', 'NGC5813', 'NGC 1042', '2XMM J120405.8+201345', 'M83', 'NGC 5139', 'SN2011ja', 'NGC 253', 'N119', 'SN 2011ja', 'ngc2997', 'ngc6744', 'NGC3923', 'M31', 'NGC 4490', 'NGC4594', 'NGC3379', 'NGC1097', 'NGC4258', 'NGC4388', 'M51', 'M33', 'NGC 346', 'SNR 1987A', 'SN 1998S', 'NGC2403', 'NGC4365', 'NGC 2865', 'NGC 1316', 'NGC 604', 'RXJ1416.4+2315', 'NGC 3556', 'NGC 4559', 'NGC 4214', 'NGC 5253', 'NGC 3628', 'NGC 278', 'NGC 628', 'NGC 1291', 'NGC 2681', 'NGC 4314', 'NGC 5236', 'IC 5332', 'NGC 4621', 'NGC 1700', 'NGC 5018', 'NGC 3608', 'NGC 4494', 'LBQS 1231+1320', '3C31', 'NGC 4303', 'IC 1459', 'NGC 5055', 'NGC 7331', 'NGC 741 GROUP', 'QSO 1508+5714', 'NGC 55', 'CIRCINUS GALAXY', 'NGC4486', 'NGC5471B', 'NGC 1332', 'NGC 4501', 'M82', 'NGC 1313', 'NGC 4725', 'NGC4698', 'NGC 4039', 'NGC 4038', 'NGC 3507', 'NGC4457', 'NGC 3557', 'DEM L50', 'NGC 4258', 'M87', 'NGC 1365', 'NGC 1850', 'NGC 3031', 'DEM L238', 'NGC 5204 X-1', 'NGC 1818', 'IC5267', 'NGC 4565', 'NGC 3631', 'NGC 7793', 'NGC4527', 'FORNAX CLUSTER', 'SN 2002HH', 'SN 1986J', 'SN 2004dj', 'SN 2004et', 'NGC 4473', 'NGC 2787', 'M101', 'NGC4278', 'NGC1427', 'NGC4214', 'NGC 1313 X-1', 'NGC 1313 X-2', 'VIRGO CLUSTER', 'IC 1613', 'M84', 'NGC 3351', 'ngc 1672', 'M81', 'NGC 2841', 'IRAS08572+3915', 'NGC 7090', 'SN 1993J', 'SNR 0509-67.5', 'SN1999em', 'SN1998S', 'NGC 7552', 'NGC 4649', 'NGC 4308', 'NGC 5846', 'NGC 891', 'NGC 4631', 'NGC 4374', 'NGC 4570', 'NGC 4478', 'I ZW 18', 'NGC 4550', 'NGC 4476', 'UGC 7658', '2MASX J12293498+0803286', 'LHA 120-N 11', 'SNR 0104-72.3', 'SN1978K', 'SN 1979C', 'NGC3585', 'M86', 'NGC4477', 'NGC1399', 'Sombrero', 'M81 DwA', 'Holmberg IX', 'NGC 5474', 'NGC 3627', 'NGC 855', 'NGC 3198', 'NGC 3521', 'NGC 4736'])
