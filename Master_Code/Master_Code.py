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
import webbrowser #Not nessary for the functionally of the code, Can be removed without any problem whatsoever
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
    Galaxy_Fail_A_L=[]
    Galaxy_No_Obs_B_L=[]
    for Gname in Gname_L:
        #Pipeline_A Code
        print "Gname A: ", Gname
        Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
        if(Evt2_File_H_L==False):
            print "Invalid Galaxy"
            Galaxy_No_Obs_B_L.append(Gname)
            continue
        """
        try:
            Galaxy_Histogram_Code_3.Driver_Code(Gname) #This runs the histrogram code and creates the histrograms and the directories with the histrograms in them
        except:
            Galaxy_Fail_A_L.append(Gname)
    print "Galaxy_Fail_A_L : ", Galaxy_Fail_A_L
        """
        #try:
        Galaxy_Histogram_Code_3.Driver_Code(Gname) #This runs the histrogram code and creates the histrograms and the directories with the histrograms in them
        #except:
        #Galaxy_Fail_A_L.append(Gname)
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
    Galaxy_Fail_B_L=[]
    Galaxy_No_Obs_B_L=[]
    for Gname in Gname_L:
        #Pipeline_B Code
        try:
            print "Gname B: ", Gname
            """
            Gname_List=Gname.split(" ")
            print "Gname_List: ", Gname_List
            if(len(Gname_List)>1):
                Gname_Modifed=Gname_List[0]+"_"+Gname_List[1] #Adds underscore to remove space from "NGC #" to change to "NGC_#" if there is a space in the name
            else:
                Gname_Modifed=Gname # Does nothing if the galaxy name has no space, ie. NGC#, For example NGC253 instead of NGC 253 or NGC_253
            """
            Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
            if(Evt2_File_H_L==False):
                print "Invalid Galaxy"
                Galaxy_No_Obs_B_L.append(Gname)
                continue
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
                        print "Cur_Evt2_ObsID : ", Cur_Evt2_ObsID
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
                        Cur_Area_L_D25=Area_Calc_Frac_B_2_Alt_8.Area_Calc_Frac_B_2_Alt_2(Gname,Cur_Evt2_Filepath,Simple_Region_Filepath,D25_Steps_Bool=True,Fnamekey="D25")
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
        except:
            Galaxy_Fail_B_L.append(Gname)

    print "Galaxy_Fail_B_L : ", Galaxy_Fail_B_L
    print "Galaxy_No_Obs_B_L : ", Galaxy_No_Obs_B_L

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
    Galaxy_Fail_C_L=[]
    ObsID_Fail_C_L=[]
    Galaxy_No_Obs_C_L=[]
    for Gname in Gname_L:
        #Pipeline_C Code
        try:
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
            Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
            if(Evt2_File_H_L==False):
                print "Invalid Galaxy"
                Galaxy_No_Obs_C_L.append(Gname)
                continue
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
                        print "Cur_Evt2_ObsID : ", Cur_Evt2_ObsID
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
                        """
                        if(Gname[3]==" "):
                            Gname_Underscore=Gname.replace(Gname[3], "_", 1)
                        elif(Gname[3]!="_"):
                            Gname_Underscore_L=Gname.split(Gname[2])
                            #print "Gname_Underscore_L : ",Gname_Underscore_L
                            Gname_Underscore=Gname_Underscore_L[0]+Gname[2]+"_"+Gname_Underscore_L[1]
                        #print "Gname_Underscore Master : ", Gname_Underscore
                        """
                        #NGC_4258_ObsID_1618_Source_Regions_Radius_Modifed.txt
                        #ObjF_Filename=Gname_Underscore+"_ObsID_"+str(Cur_Evt2_ObsID)+"_Source_Regions_Radius_Modifed.txt"
                        ObjF_Filename=Gname_Modifed+"_ObsID_"+str(Cur_Evt2_ObsID)+"_Source_Regions_Radius_Modifed.txt"
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
                        #print "Background_Ratio_L: ", Background_Ratio_L
                        #D_P_C_Big_Input_90_Per_Check(Backgrounds,Off_Angs,C_Min=2,C_Max=110)
                        #print "THE PWD AT END IS :"
                        #system('pwd')
                        #path_4=os.path.realpath('../../../../')
                        #print "path_4 : ",path_4
                        #os.chdir(path_4)
                        #print "Output : ",Detection_Probability_Calc_7.D_P_C_Big_Input_90_Per_Check(Background_Ratio_L)
                        #system('pwd')
                        #C_90_Per_First_L_H=Detection_Probability_Calc_7.D_P_C_Big_Input_90_Per_Check(Background_Ratio_L)
                        try: #This "Try-Except" with be replaced with the Obs_ID_Checker module
                            C_90_Per_First_L_H=Detection_Probability_Calc_7.D_P_C_Big_Input_90_Per_Check(Background_Ratio_L)
                        except:
                            ObsID_Fail_C_L.append([Gname,Cur_Evt2_ObsID])
                            continue
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
        except:
            Galaxy_Fail_C_L.append(Gname)

    print "Galaxy_Fail_C_L : ", Galaxy_Fail_C_L
    print "Galaxy_No_Obs_C_L : ", Galaxy_No_Obs_C_L
    print "ObsID_Fail_C_L : ", ObsID_Fail_C_L

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
    Galaxy_Fail_D_L=[]
    Galaxy_No_Obs_D_L=[]
    for Gname in Gname_L:
        try:
            #Pipeline_D Code
            print "Gname D: ", Gname
            Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
            if(Evt2_File_H_L==False):
                print "Invalid Galaxy"
                Galaxy_No_Obs_D_L.append(Gname)
                continue
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
                        print "Cur_Evt2_ObsID : ", Cur_Evt2_ObsID
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
            #path_5=os.path.realpath('../../../../')
            #print "path_5 : ",path_5
            #os.chdir(path_5)
            #print "THE PWD AT VERY END IS :"
            #system('pwd')
        except:
            Galaxy_Fail_D_L.append(Gname)
    print "Galaxy_Fail_D_L : ", Galaxy_Fail_D_L
    print "Galaxy_No_Obs_D_L : ", Galaxy_No_Obs_D_L

def Master(Gname_L):
    webbrowser.open_new("https://www.youtube.com/watch?v=xnKhsTXoKCI") # OBEY YOUR MASTER ! ! !      Not nesseary for the fuctionality of the code, Can be removed without any problem whatsoever but this code would be much less metal if removed
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
    #Master(['NGC 4449', 'NGC 6946', 'Willman 1', 'NGC 602', 'SN 2004am', 'SN 1996aq', 'NGC 4278', 'DDO 68', 'NGC7507', 'PGC135659', 'NGC 5054', 'NGC1300', 'NGC4742', 'NGC5576', 'NGC3384', 'NGC4486A', 'NGC4459', '3C 299', 'NGC3115', 'NGC 247', 'PTF11eon', 'SN2011dh', 'NGC 4472', 'NGC5813', 'NGC 1042', '2XMM J120405.8+201345', 'M83', 'NGC 5139', 'SN2011ja', 'NGC 253', 'N119', 'SN 2011ja', 'ngc2997', 'ngc6744', 'NGC3923', 'M31', 'NGC 4490', 'NGC4594', 'NGC3379', 'NGC1097', 'NGC4258', 'NGC4388', 'M51', 'M33', 'NGC 346', 'SNR 1987A', 'SN 1998S', 'NGC2403', 'NGC4365', 'NGC 2865', 'NGC 1316', 'NGC 604', 'RXJ1416.4+2315', 'NGC 3556', 'NGC 4559', 'NGC 4214', 'NGC 5253', 'NGC 3628', 'NGC 278', 'NGC 628', 'NGC 1291', 'NGC 2681', 'NGC 4314', 'NGC 5236', 'IC 5332', 'NGC 4621', 'NGC 1700', 'NGC 5018', 'NGC 3608', 'NGC 4494', 'LBQS 1231+1320', '3C31', 'NGC 4303', 'IC 1459', 'NGC 5055', 'NGC 7331', 'NGC 741 GROUP', 'QSO 1508+5714', 'NGC 55', 'CIRCINUS GALAXY', 'NGC4486', 'NGC5471B', 'NGC 1332', 'NGC 4501', 'M82', 'NGC 1313', 'NGC 4725', 'NGC4698', 'NGC 4039', 'NGC 4038', 'NGC 3507', 'NGC4457', 'NGC 3557', 'DEM L50', 'NGC 4258', 'M87', 'NGC 1365', 'NGC 1850', 'NGC 3031', 'DEM L238', 'NGC 5204 X-1', 'NGC 1818', 'IC5267', 'NGC 4565', 'NGC 3631', 'NGC 7793', 'NGC4527', 'FORNAX CLUSTER', 'SN 2002HH', 'SN 1986J', 'SN 2004dj', 'SN 2004et', 'NGC 4473', 'NGC 2787', 'M101', 'NGC4278', 'NGC1427', 'NGC4214', 'NGC 1313 X-1', 'NGC 1313 X-2', 'VIRGO CLUSTER', 'IC 1613', 'M84', 'NGC 3351', 'ngc 1672', 'M81', 'NGC 2841', 'IRAS08572+3915', 'NGC 7090', 'SN 1993J', 'SNR 0509-67.5', 'SN1999em', 'SN1998S', 'NGC 7552', 'NGC 4649', 'NGC 4308', 'NGC 5846', 'NGC 891', 'NGC 4631', 'NGC 4374', 'NGC 4570', 'NGC 4478', 'I ZW 18', 'NGC 4550', 'NGC 4476', 'UGC 7658', '2MASX J12293498+0803286', 'LHA 120-N 11', 'SNR 0104-72.3', 'SN1978K', 'SN 1979C', 'NGC3585', 'M86', 'NGC4477', 'NGC1399', 'Sombrero', 'M81 DwA', 'Holmberg IX', 'NGC 5474', 'NGC 3627', 'NGC 855', 'NGC 3198', 'NGC 3521', 'NGC 4736']) #Complete List of All galaxies
    #Master(['Willman 1', 'NGC 602', 'SN 2004am', 'SN 1996aq', 'NGC7507', 'PGC135659', 'NGC4486A', '3C 299', 'PTF11eon', 'SN2011dh', '2XMM J120405.8+201345', 'NGC 5139', 'SN2011ja', 'N119', 'SN 2011ja', 'NGC3923', 'NGC1097', 'M51', 'NGC 346', 'SNR 1987A', 'SN 1998S', 'NGC 2865', 'NGC 1316', 'NGC 604', 'RXJ1416.4+2315', 'NGC 5253', 'NGC 1291', 'NGC 5018', 'LBQS 1231+1320', 'IC 1459', 'NGC 741 GROUP', 'QSO 1508+5714', 'NGC5471B', 'NGC 1332', 'NGC 3557', 'DEM L50', 'NGC 1850', 'DEM L238', 'NGC 5204 X-1', 'NGC 1818', 'IC5267', 'FORNAX CLUSTER', 'SN 2002HH', 'SN 1986J', 'SN 2004dj', 'SN 2004et', 'NGC1427', 'NGC 1313 X-1', 'NGC 1313 X-2', 'VIRGO CLUSTER', 'ngc 1672', 'IRAS08572+3915', 'SN 1993J', 'SNR 0509-67.5', 'SN1999em', 'SN1998S', 'NGC 7552', 'UGC 7658', '2MASX J12293498+0803286', 'LHA 120-N 11', 'SNR 0104-72.3', 'SN1978K', 'SN 1979C', 'NGC3585', 'NGC1399', 'M81 DwA']) #Fail List From Pipeline A
    #Master(['NGC4258']) #Fail List From Pipeline C
    #Master(['NGC 4278', 'NGC 5204', 'NGC 2841', 'VCC 1199', 'NGC 0346', 'LBQS 1231+1320', 'NGC 3877', 'MESSIER 106', 'NGC 5194', 'MESSIER 104', 'MESSIER 105', 'MESSIER 101', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'NGC 0741 GROUP', 'MESSIER 063', 'WILLMAN 1', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'MESSIER 081', 'NGC 0278', 'MESSIER 088', 'NGC 0602', 'NGC 1042', 'NGC 0604', 'NGC 6744', 'IC 5332', 'NGC 3585', 'NGC 4478', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4476', 'NGC 4570', 'NGC 5576', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'NGC 0247', 'NGC 4490', 'IC 1613', '3C 299', 'SUMSS J010618-720523', 'NGC 4477', 'omega Cen                     ', 'NGC 4365', 'NGC 2787', 'NGC 3557', 'NGC 4565', 'Fornax Cluster                ', 'IC 5267', 'NGC 4388', 'NGC 0253', 'NGC 3923', 'Virgo Cluster                 ', 'NGC 4945', 'NGC 891', 'NGC 1313', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'PMN J0459-7009', 'UGCA 166', 'NGC 4314', 'NGC 4550', 'NGC 1850', 'Holmberg IX                   ', 'NGC 4559', 'IC 1459', 'NGC 1399', 'NGC 4039', 'NGC 4038', 'NGC 4486A', 'IRAS  08572+3915', 'NGC 1316', 'NGC 1097', 'NGC 0383', 'WARP J1416.4+2315', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4631', 'NGC 4308', 'MESSIER 060', 'NGC 4742', 'SDSS J120405.83+201345.0', 'NGC 1672', 'NGC 5846', 'MESSIER 033', 'MESSIER 031', 'NGC 4725', 'NGC 2403', 'MESSIER 081 DWARF A', 'NGC 3507', 'MESSIER 087', 'NGC 0891', 'NGC 4698', 'NGC 3384', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 4527', 'NGC 7552', 'NGC 2997', 'PMN J0534-7034', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 0119', 'NGC 2865', 'Circinus Galaxy               ', 'MESSIER 059', 'SDSS J024310.55-001546.3', 'NGC 7331', 'SN 1987A', 'NGC 1427', 'NGC 3628', 'NGC 3608', 'NGC 0055', 'MESSIER 051', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 1818', 'RBS 0624', 'NGC 3521']) #Used to be the master input
    #Master(['NGC 4565', 'NGC 0253', 'NGC 891', 'NGC 1313', 'UGCA 166', 'NGC 0383', 'NGC 4631', 'MESSIER 060', 'NGC 5846', 'MESSIER 033', 'MESSIER 031', 'MESSIER 087', 'NGC 0891', 'NGC 1291:[LFF2012] 084', 'NGC 1700', 'MESSIER 049', 'NGC 3628']) #Galaxy_Fail_C_Without_A_L
    #Master(['MESSIER 101', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'MESSIER 081', 'NGC 1637', 'NGC 4490', 'NGC 4565', 'NGC 0253', 'NGC 891', 'NGC 1313', 'UGCA 166', 'NGC 0383', 'NGC 4631', 'MESSIER 060', 'NGC 5846', 'MESSIER 033', 'MESSIER 031', 'MESSIER 087', 'NGC 0891', 'NGC 1291:[LFF2012] 084', 'NGC 1700', 'MESSIER 049', 'NGC 3628']) #Galaxy_Fail_C_Without_A_L now removing galaxy names as the problem is understood
    #Master(['NGC 4565', 'NGC 0253', 'NGC 1313', 'MESSIER 033', 'MESSIER 031']) #Galaxy_Fail_C_Without_A_L After modification to the PIMMS file to allow for dates earlier then 2001
    #Master(['MESSIER 033', 'MESSIER 031']) #Galaxy_Fail_C_Without_A_L After modification to the PIMMS file to allow for dates earlier then 2001 now removing galaxy names as the problem is understood
    #Master(['MESSIER 031']) #Galaxy_Fail_C_Without_A_L After modification to the PIMMS file to allow for dates earlier then 2001 now removing galaxy names as the problem is understood
    #Master(['NGC 4278', 'NGC 5204', 'NGC 2841', 'NGC 5194', 'MESSIER 104', 'MESSIER 105', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'NGC 0278', 'MESSIER 088', 'NGC 1042', 'NGC 6744', 'IC 5332', 'NGC 3585', 'NGC 4478', 'NGC 7507', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4476', 'NGC 4570', 'NGC 5576', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'NGC 0247', 'IC 1613', 'NGC 4477', 'NGC 4365', 'NGC 2787', 'NGC 3557', 'IC 5267', 'NGC 4388', 'NGC 3923', 'NGC 4945', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'NGC 4314', 'NGC 4550', 'Holmberg IX                   ', 'NGC 4559', 'IC 1459', 'NGC 1399', 'NGC 4039', 'NGC 4038', 'NGC 1316', 'NGC 1097', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4308', 'NGC 4742', 'NGC 1672', 'NGC 4725', 'NGC 2403', 'NGC 3507', 'NGC 4698', 'NGC 3384', 'NGC 6946', 'NGC 3115', 'NGC 1332', 'NGC 5584', 'NGC 4527', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 0119', 'NGC 2865', 'Circinus Galaxy               ', 'MESSIER 059', 'NGC 7331', 'NGC 1427', 'NGC 3608', 'NGC 0055', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521']) #This an old galaxy name list (This needs to be fixed need to add Messier Objects back in) Note_2: It is fixed in the new Master Code Input Galaxy Name List
    #Master(['NGC 4278', 'NGC 5204', 'NGC 2841', 'NGC 3877', 'MESSIER 106', 'NGC 5194', 'MESSIER 104', 'MESSIER 105', 'MESSIER 101', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'MESSIER 081', 'NGC 0278', 'MESSIER 088', 'NGC 1042', 'NGC 6744', 'IC 5332', 'NGC 3585', 'NGC 4478', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4476', 'NGC 4570', 'NGC 5576', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'NGC 0247', 'NGC 4490', 'IC 1613', 'NGC 4477', 'NGC 4365', 'NGC 2787', 'NGC 3557', 'IC 5267', 'NGC 4388', 'NGC 3923', 'NGC 4945', 'NGC 891', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'UGCA 166', 'NGC 4314', 'NGC 4550', 'Holmberg IX                   ', 'NGC 4559', 'IC 1459', 'NGC 1399', 'NGC 4039', 'NGC 4038', 'NGC 1316', 'NGC 1097', 'NGC 0383', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4631', 'NGC 4308', 'MESSIER 060', 'NGC 4742', 'NGC 1672', 'NGC 5846', 'NGC 4725', 'NGC 2403', 'NGC 3507', 'MESSIER 087', 'NGC 0891', 'NGC 4698', 'NGC 3384', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 4527', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 0119', 'NGC 2865', 'Circinus Galaxy               ', 'MESSIER 059', 'NGC 7331', 'NGC 1427', 'NGC 3628', 'NGC 3608', 'NGC 0055', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521']) #This was the correct Master Code Input Galaxy Name List without 3 galaxies that had bad observations in them, these 3 galaxies will now be included in the new current correct Master Code Input Galaxy Name List
    #Master(['NGC 4565', 'NGC 0253', 'NGC 1313']) #List of galaxy names that work in Pipeline A but not in Pipeline C, Probably because there is too short of an exposure time for one of the ObsIDs for each galaxy without duplicates and Messier Objects
    #Master(['NGC 4278', 'NGC 5204', 'NGC 2841', 'NGC 5194', 'MESSIER 104', 'MESSIER 105', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'NGC 0278', 'MESSIER 088', 'NGC 1042', 'NGC 6744', 'IC 5332', 'NGC 3585', 'NGC 4478', 'NGC 7507', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4476', 'NGC 4570', 'NGC 5576', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'NGC 0247', 'IC 1613', 'NGC 4477', 'NGC 4365', 'NGC 2787', 'NGC 3557', 'IC 5267', 'NGC 4388', 'NGC 3923', 'NGC 4945', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'NGC 4314', 'NGC 4550', 'Holmberg IX                   ', 'NGC 4559', 'IC 1459', 'NGC 1399', 'NGC 4039', 'NGC 4038', 'NGC 1316', 'NGC 1097', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4308', 'NGC 4742', 'NGC 1672', 'NGC 4725', 'NGC 2403', 'NGC 3507', 'NGC 4698', 'NGC 3384', 'NGC 6946', 'NGC 3115', 'NGC 1332', 'NGC 5584', 'NGC 4527', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 0119', 'NGC 2865', 'Circinus Galaxy               ', 'MESSIER 059', 'NGC 7331', 'NGC 1427', 'NGC 3608', 'NGC 0055', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521']) #This an old galaxy name list (This needs to be fixed need to add Messier Objects back in) Note_2: It is fixed in the new Master Code Input Galaxy Name List
    #Master(['NGC 4278', 'NGC 5204', 'NGC 2841', 'NGC 3877', 'MESSIER 106', 'NGC 5194', 'MESSIER 104', 'MESSIER 105', 'MESSIER 101', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'MESSIER 081', 'NGC 0278', 'MESSIER 088', 'NGC 1042', 'NGC 6744', 'IC 5332', 'NGC 3585', 'NGC 4478', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4476', 'NGC 4570', 'NGC 5576', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'NGC 0247', 'NGC 4490', 'IC 1613', 'NGC 4477', 'NGC 4365', 'NGC 2787', 'NGC 3557', 'IC 5267', 'NGC 4388', 'NGC 3923', 'NGC 4945', 'NGC 891', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'UGCA 166', 'NGC 4314', 'NGC 4550', 'Holmberg IX                   ', 'NGC 4559', 'IC 1459', 'NGC 1399', 'NGC 4039', 'NGC 4038', 'NGC 1316', 'NGC 1097', 'NGC 0383', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4631', 'NGC 4308', 'MESSIER 060', 'NGC 4742', 'NGC 1672', 'NGC 5846', 'NGC 4725', 'NGC 2403', 'NGC 3507', 'MESSIER 087', 'NGC 0891', 'NGC 4698', 'NGC 3384', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 4527', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 0119', 'NGC 2865', 'Circinus Galaxy               ', 'MESSIER 059', 'NGC 7331', 'NGC 1427', 'NGC 3628', 'NGC 3608', 'NGC 0055', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521','NGC 4565', 'NGC 1313', 'NGC 0253']) #This is the final version used for the Master Thesis
    #Master(['NGC 4278', 'NGC 5204', 'NGC 2841']) #Small Sample of Galaxies for testing
    #Master(['NGC 0253']) #Small Sample of Galaxies for testing
    Master(['NGC 3631']) #Small Sample of Galaxies for testing
    #Master(['NGC 2841', 'NGC 3877', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'NGC 0278', 'MESSIER 088', 'NGC 3585', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4570', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'IC 1613', 'NGC 4477', 'NGC 2787', 'IC 5267', 'NGC 3923', 'NGC 891', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'NGC 4314', 'NGC 4559', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4742', 'NGC 1672', 'NGC 4725', 'NGC 0891', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 2865', 'MESSIER 059', 'NGC 1427', 'NGC 3628', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521']) #This is the current correct Master Code Input Galaxy Name List, The Master Code is Ready to Run ! ! !
    #Master(['MESSIER 063','MESSIER 084','NGC 1365','NGC 4559','NGC 5018','MESSIER 049']) #Small Sample of Galaxies for testing
    #Master(['MESSIER 049']) #Small Sample of Galaxies for testing
    #Master(['NGC 4559']) #Small Sample of Galaxies for testing
    #Master(['NGC 1365']) #Small Sample of Galaxies for testing
