import subprocess
import threading
from threading import Thread
import os
from os import system
import sys
import gzip
def Pipeline_A(Gname_L):
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
    print "Path=",path
    system('pwd')
    #os.system('python '+path) #This works when inputs are not used
    #import Galaxy_Histogram_Code_2
    #Driver_Code('NGC4258')
    sys.path.append(os.path.abspath(path))
    print sys.path
    #from Galaxy_Histogram_Code_2 import *
    #import Galaxy_Histogram_Code_2
    from Histogram_Code import Galaxy_Histogram_Code_3
    for Gname in Gname_L:
        #Pipeline_A Code
        Galaxy_Histogram_Code_3.Driver_Code(Gname) #This runs the histrogram code and creates the histrograms and the directories with the histrograms in them

# Pipelines are quoted until they are finished

def Pipeline_B(Gname_L):
    dir = os.path.dirname(__file__)
    path=os.path.realpath('../')
    #print "Path=",path
    system('pwd')
    sys.path.append(os.path.abspath(path))
    #print sys.path
    from File_Query_Code import File_Query_Code_5
    from XPA_DS9_Region_Generator import XPA_DS9_Region_Generator_3
    #from CCD_Region_Testing import Simple_Region_Generator_8
    from Simple_Region_Generator import Simple_Region_Generator_9
    from Area_Calc import Area_Calc_Frac_B_2_Alt_8
    for Gname in Gname_L:
        #Pipeline_B Code
        Gname_List=Gname.split(" ")
        print "Gname_List: ", Gname_List
        if(len(Gname_List)>1):
            Gname_Modifed=Gname_List[0]+"_"+Gname_List[1] #Adds underscore to remove space from "NGC #" to change to "NGC_#" if there is a space in the name
        else:
            Gname_Modifed=Gname # Does nothing if the galaxy name has no space, ie. NGC#, For example NGC253 instead of NGC 253 or NGC_253
        print "Gname_Modifed ", Gname_Modifed
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
        print "path_Area=",path_Area
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
        print "Evt2_File_H_L ", Evt2_File_H_L
        print "Fov_File_H_L ", Fov_File_H_L
        for Evt2_File_L in Evt2_File_H_L:
            Cur_Evt2_ObsID=Evt2_File_L[0]
            Cur_Evt2_Filepath=Evt2_File_L[1]
            for Fov_File_L in Fov_File_H_L:
                Cur_Fov_ObsID=Fov_File_L[0]
                Cur_Fov_Filepath=Fov_File_L[1]
                if(Cur_Evt2_ObsID==Cur_Fov_ObsID):
                    #print "Test"
                    path_Obs=path_Area+'/'+str(Cur_Evt2_ObsID)+'/'
                    directory_Obs=os.path.dirname(path_Obs)
                    if not os.path.exists(directory_Obs):
                        os.makedirs(directory_Obs)
                    os.chdir(path_Obs)
                    print "THE PWD AT END IS :"
                    system('pwd')
                    print "CURRENT FOV FILEPATH IS :", Cur_Fov_Filepath
                    Cur_Fov_Filename_L=Cur_Fov_Filepath.split("/")
                    print "Cur_FOV_Filename_L : ",Cur_Fov_Filename_L
                    Cur_Fov_Filepath_No_Fname_L=Cur_Fov_Filepath.rsplit("/",1)
                    print "Cur_Fov_Filepath_No_Fname_L : ",Cur_Fov_Filepath_No_Fname_L
                    Cur_Fov_Filepath_No_Fname=Cur_Fov_Filepath_No_Fname_L[0]
                    print "Cur_Fov_Filepath_No_Fname : ",Cur_Fov_Filepath_No_Fname
                    Cur_Fov_Filename=Cur_Fov_Filename_L[len(Cur_Fov_Filename_L)-1]
                    print "Cur_Fov_Filename : ",Cur_Fov_Filename
                    Cur_Fov_Filename_Ext_L=Cur_Fov_Filename.split(".")
                    print "Cur_Fov_Filename_Ext_L : ",Cur_Fov_Filename_Ext_L
                    Cur_Fov_Filename_Ext=Cur_Fov_Filename_Ext_L[len(Cur_Fov_Filename_Ext_L)-1]
                    print "Cur_Fov_Filename_Ext : ", Cur_Fov_Filename_Ext
                    if(Cur_Fov_Filename_Ext=="gz"):
                        Output_Fov_Filename=Cur_Fov_Filename_Ext_L[0]+"."+Cur_Fov_Filename_Ext_L[1]
                        #os.chdir(path_Obs)
                        os.chdir(Cur_Fov_Filepath_No_Fname)
                        system('pwd')
                        Output_Fov_Filepath=Cur_Fov_Filepath_No_Fname+"/"+Output_Fov_Filename
                        print "Output_Fov_Filepath : ",Output_Fov_Filepath
                        inF = gzip.open(Cur_Fov_Filename, 'rb')
                        outF = open(Output_Fov_Filename, 'wb')
                        outF.write( inF.read() )
                        inF.close()
                        outF.close()
                        os.chdir(path_Obs)
                        Cur_Fov_Filepath=Output_Fov_Filepath
                    print "Cur_Evt2_Filepath : ", Cur_Evt2_Filepath
                    print "Cur_Fov_Filepath : ", Cur_Fov_Filepath
                    XPA_DS9_Region_Generator_3.XPA_DS9_Region_Generator(Cur_Evt2_Filepath,Cur_Fov_Filepath)
                    print "The Filepath Before End is : "
                    system('pwd')
                    Region_File_LS= os.popen("ls").read()
                    Region_File_LS_L=Region_File_LS.split("\n")
                    print "Region_File_LS_L : ",Region_File_LS_L
                    for Region_Filename_Test in Region_File_LS_L:
                        Region_Filename_Test_L=Region_Filename_Test.split("_")
                        print "Region_Filename_Test_L : ",Region_Filename_Test_L
                        if(len(Region_Filename_Test_L)==4):
                            Region_Filename=Region_Filename_Test
                    print "Region_Filename : ",Region_Filename
                    #This_is_Ment_To_Break_The_Code
                    Simple_Region_Generator_9.Simple_Region_Generator(Region_Filename,Cur_Evt2_Filepath)
                    #print "Cur_Evt2_Filepath: ", Cur_Evt2_Filepath
                    #Area_Calc_Frac_B_2_Alt_2("NGC 253","/Network/Servers/vimes.astro.wesleyan.edu/Volumes/vvodata/home/asantini/Desktop/CCD_Incompleteness_Correction/Area_Calc/acisf13830_repro_evt2.fits","acisf13830_repro_CCD_Regions_simple_region_modifed_Code.txt")
                    Simple_Region_File_LS= os.popen("ls").read()
                    Simple_Region_File_LS_L=Region_File_LS.split("\n")
                    print "Simple_Region_File_LS_L : ",Simple_Region_File_LS_L
                    for Simple_Region_Filename_Test in Simple_Region_File_LS_L:
                        Simple_Region_Filename_Test_L=Simple_Region_Filename_Test.split("_")
                        print "Simple_Region_Filename_Test_L : ",Simple_Region_Filename_Test_L
                        if(len(Simple_Region_Filename_Test_L)==8):
                            Simple_Region_Filename=Simple_Region_Filename_Test
                    print "Simple_Region_Filename : ",Simple_Region_Filename
                    #Area_Calc_Frac_B_2_Alt_8.Area_Calc_Frac_B_2_Alt_2(Gname,Simple_Region_Filename,Cur_Evt2_Filepath)
                    Cur_Area_L=Area_Calc_Frac_B_2_Alt_8.Area_Calc_Frac_B_2_Alt_2(Gname,Cur_Evt2_Filepath,Simple_Region_Filename)
                    print Cur_Area_L
                    system('pwd')
                    Simple_Region_Filename_L=Simple_Region_Filename.split("CCD")
                    print "Simple_Region_Filename_L : ",Simple_Region_Filename_L
                    Simple_Region_Filename_Reduced=Simple_Region_Filename_L[0]
                    print "Simple_Region_Filename_Reduced : ",Simple_Region_Filename_Reduced
                    Area_List_Filename=Simple_Region_Filename_Reduced+"Area_List.txt"
                    print "Area_List_Filename : ",Area_List_Filename
                    #print "fovfname_reduced : ",fovfname_reduced
                    print "Cur_Evt2_Filepath : ",Cur_Evt2_Filepath
                    #Cur_Evt2_Filepath_L=Cur_Evt2_Filepath.split("/")
                    #print "Cur_Evt2_Filepath_L : ",Cur_Evt2_Filepath_L
                    #Cur_Evt2_Filename=Cur_Evt2_Filepath_L[len(Cur_Evt2_Filepath_L)-1]
                    #print "Cur_Evt2_Filename : ",Cur_Evt2_Filename
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
                    print "PWD before Path_5 : "
                    system('pwd')
        path_5=os.path.realpath('../../../../')
        print "path_5 : ",path_5
        os.chdir(path_5)
        print "THE PWD AT VERY END IS :"
        system('pwd')
        #Need to add the rest of Pipeline B after XPA_DS9_Region_Generator

def Pipeline_C(Gname_L):
    dir = os.path.dirname(__file__)
    path=os.path.realpath('../')
    #print "Path=",path
    system('pwd')
    sys.path.append(os.path.abspath(path))
    #print "Modules PWD : "
    #system('pwd')
    #print sys.path
    #Import Desktop Modules Here !!!
    from File_Query_Code import File_Query_Code_5
    from Source_Region_Generator import Source_Region_Generator_Radius_Modifed_V3
    from Background_Finder import Background_Finder_10
    from Detection_Probablity_Calc import Detection_Probability_Calc_7
    for Gname in Gname_L:
        #Pipeline_C Code
        Gname_List=Gname.split(" ")
        print "Gname_List: ", Gname_List
        if(len(Gname_List)>1):
            Gname_Modifed=Gname_List[0]+"_"+Gname_List[1] #Adds underscore to remove space from "NGC #" to change to "NGC_#" if there is a space in the name
        else:
            Gname_Modifed=Gname # Does nothing if the galaxy name has no space, ie. NGC#, For example NGC253 instead of NGC 253 or NGC_253
        print "Gname_Modifed ", Gname_Modifed
        path_2=os.path.realpath('../Master_Code/Master_Output/')
        path_3=path_2+'/'+Gname_Modifed+'/'
        directory = os.path.dirname(path_3)
        if not os.path.exists(directory):
            os.makedirs(directory)
        #os.chdir(path_3) #Goes to Current Galaxies Folder
        path_Flux_90=path_3+'Flux_90_Files/'
        directory_Flux_90=os.path.dirname(path_Flux_90)
        if not os.path.exists(directory_Flux_90):
            os.makedirs(directory_Flux_90)
        print "path_Flux_90=",path_Flux_90
        #os.chdir(path_Flux_90)
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
                    #path_Obs=path_Flux_90+'/'+str(Cur_Evt2_ObsID)+'/'
                    print "Cur_Evt2_ObsID : ",Cur_Evt2_ObsID
                    #print "type(Cur_Evt2_ObsID) : ",type(Cur_Evt2_ObsID)
                    print "Cur_Evt2_Filepath : ", Cur_Evt2_Filepath
                    #Cur_Evt2_Filepath_L=Cur_Evt2_Filepath.split("/")
                    #print "Cur_Evt2_Filepath_L : ",Cur_Evt2_Filepath_L
                    #Cur_Evt2_Filename=Cur_Evt2_Filepath_L[-1]
                    #print "Cur_Evt2_Filename : ", Cur_Evt2_Filename
                    path_Obs=path_Flux_90+str(Cur_Evt2_ObsID)+'/'
                    directory_Obs=os.path.dirname(path_Obs)
                    if not os.path.exists(directory_Obs):
                        os.makedirs(directory_Obs)
                    os.chdir(path_Obs)
                    #Cur_Evt2_Filepath_Full=path_Obs+Cur_Evt2_Filename
                    print "path_Obs : ", path_Obs
                    #print "Cur_Evt2_Filepath_Full : ", Cur_Evt2_Filepath_Full
                    print "THE PWD AT END IS :"
                    system('pwd')
                    Source_Region_Generator_Radius_Modifed_V3.Source_Region_Generator_Radius_Modifed_V3(Gname,path_Obs)
                    if(Gname[3]==" "):
                        Gname_Underscore=Gname.replace(Gname[3], "_", 1)
                    elif(Gname[3]!="_"):
                        Gname_Underscore_L=Gname.split(Gname[2])
                        print "Gname_Underscore_L : ",Gname_Underscore_L
                        Gname_Underscore=Gname_Underscore_L[0]+Gname[2]+"_"+Gname_Underscore_L[1]
                    print "Gname_Underscore Master : ", Gname_Underscore
                    #NGC_4258_ObsID_1618_Source_Regions_Radius_Modifed.txt
                    ObjF_Filename=Gname_Underscore+"_ObsID_"+str(Cur_Evt2_ObsID)+"_Source_Regions_Radius_Modifed.txt"
                    BG_Radius=50
                    while (BG_Radius>20):
                        #Background_Finder_3(gname,evtfpath,objLfname,R)
                        Background_Ratio=Background_Finder_10.Background_Finder_3(Gname,Cur_Evt2_Filepath,ObjF_Filename,BG_Radius)
                        if(Background_Ratio != "None_Found"):
                            break
                        BG_Radius=BG_Radius-10
                    print "Background_Ratio : ", Background_Ratio
                    Background_Ratio_L=[Background_Ratio]
                    #D_P_C_Big_Input_90_Per_Check(Backgrounds,Off_Angs,C_Min=2,C_Max=110)
                    Detection_Probability_Calc_7.D_P_C_Big_Input_90_Per_Check(Background_Ratio_L,Off_Angs)
"""
def Pipeline_D(Gname_L):
    for Gname in Gname_L:
        #Pipeline_D Code
"""

def Master(Gname_L):
    if __name__ == '__main__':
        #Thread(target = Pipeline_A(Gname_L)).start()
        #Thread(target = Pipeline_B(Gname_L)).start()
        Thread(target = Pipeline_C(Gname_L)).start()
        #Thread(target = Pipeline_D(Gname_L)).start()

#Master(['NGC4258','M31','NGC 1365']) #This works
Master(['NGC4258'])
