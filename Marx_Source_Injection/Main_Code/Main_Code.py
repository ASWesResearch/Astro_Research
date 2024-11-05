from sherpa.astro.ui import *
from matplotlib import pyplot as plt
import numpy as np
import os
from os import system
import sys
from ciao_contrib.runtool import *
from multiprocessing import Pool
import time
import glob

dir = os.path.dirname(__file__)
path=os.path.realpath('../')
sys.path.append(os.path.abspath(path))

from Background_Generator import Background_Generator
from Source_Generator import Source_Generator
from Synthetic_Background_Generator import Synthetic_Background_Generator
from Source_Reproject import Source_Reproject
from Source_Detect import Source_Detect

####Constants####
Postage_Stamp_Coords_L=[[[0, 0], [80.0, 80.0], [4145.0, 4135.0], ['359.9933716666962', '0.005261666616669011']], [[0, 1], [80.0, 224.0], [4145.0, 4279.0], ['359.9933716666962', '0.02494166492429339']], [[0, 2], [80.0, 368.0], [4145.0, 4423.0], ['359.9933716666962', '0.04462165734674123']], [[0, 3], [80.0, 512.0], [4145.0, 4567.0], ['359.9933716666962', '0.06430163924036164']], [[0, 4], [80.0, 656.0], [4145.0, 4711.0], ['359.9933716666962', '0.08398160596151538']], [[0, 5], [80.0, 800.0], [4145.0, 4855.0], ['359.9933716666962', '0.1036615528666012']], [[0, 6], [80.0, 944.0], [4145.0, 4999.0], ['359.9933716666962', '0.1233414753120392']], [[1, 0], [224.0, 80.0], [4289.0, 4135.0], ['359.9736916685156', '0.0052616660972041']], [[1, 1], [224.0, 224.0], [4289.0, 4279.0], ['359.9736916685156', '0.02494166246190883']], [[1, 2], [224.0, 368.0], [4289.0, 4423.0], ['359.9736916685156', '0.04462165294143504']], [[1, 3], [224.0, 512.0], [4289.0, 4567.0], ['359.9736916685156', '0.06430163289215492']], [[1, 4], [224.0, 656.0], [4289.0, 4711.0], ['359.9736916685156', '0.08398159767039177']], [[1, 5], [224.0, 800.0], [4289.0, 4855.0], ['359.9736916685156', '0.1036615426325772']], [[1, 6], [224.0, 944.0], [4289.0, 4999.0], ['359.9736916685156', '0.1233414631351299']], [[2, 0], [368.0, 80.0], [4433.0, 4135.0], ['359.9540116765426', '0.00526166495697853']], [[2, 1], [368.0, 224.0], [4433.0, 4279.0], ['359.9540116765426', '0.02494165705694917']], [[2, 2], [368.0, 368.0], [4433.0, 4423.0], ['359.9540116765426', '0.04462164327174108']], [[2, 3], [368.0, 512.0], [4433.0, 4567.0], ['359.9540116765426', '0.06430161895770789']], [[2, 4], [368.0, 656.0], [4433.0, 4711.0], ['359.9540116765426', '0.08398157947124001']], [[2, 5], [368.0, 800.0], [4433.0, 4855.0], ['359.9540116765426', '0.1036615201687066']], [[2, 6], [368.0, 944.0], [4433.0, 4999.0], ['359.9540116765426', '0.123341436406556']], [[3, 0], [512.0, 80.0], [4577.0, 4135.0], ['359.9343316954208', '0.00526166319598787']], [[3, 1], [512.0, 224.0], [4577.0, 4279.0], ['359.9343316954208', '0.02494164870939743']], [[3, 2], [512.0, 368.0], [4577.0, 4423.0], ['359.9343316954208', '0.04462162833762061']], [[3, 3], [512.0, 512.0], [4577.0, 4567.0], ['359.9343316954208', '0.06430159743705187']], [[3, 4], [512.0, 656.0], [4577.0, 4711.0], ['359.9343316954208', '0.08398155136404363']], [[3, 5], [512.0, 800.0], [4577.0, 4855.0], ['359.9343316954208', '0.1036614854750053']], [[3, 6], [512.0, 944.0], [4577.0, 4999.0], ['359.9343316954208', '0.1233413951263738']], [[4, 0], [656.0, 80.0], [4721.0, 4135.0], ['359.9146517297941', '0.005261660814234067']], [[4, 1], [656.0, 224.0], [4721.0, 4279.0], ['359.9146517297941', '0.02494163741926511']], [[4, 2], [656.0, 368.0], [4721.0, 4423.0], ['359.9146517297941', '0.04462160813912187']], [[4, 3], [656.0, 512.0], [4721.0, 4567.0], ['359.9146517297941', '0.06430156833020197']], [[4, 4], [656.0, 656.0], [4721.0, 4711.0], ['359.9146517297941', '0.08398151334885186']], [[4, 5], [656.0, 800.0], [4721.0, 4855.0], ['359.9146517297941', '0.1036614385515127']], [[4, 6], [656.0, 944.0], [4721.0, 4999.0], ['359.9146517297941', '0.1233413392946094']], [[5, 0], [800.0, 80.0], [4865.0, 4135.0], ['359.8949717843058', '0.005261657811719962']], [[5, 1], [800.0, 224.0], [4865.0, 4279.0], ['359.8949717843059', '0.02494162318656983']], [[5, 2], [800.0, 368.0], [4865.0, 4423.0], ['359.8949717843059', '0.04462158267626447']], [[5, 3], [800.0, 512.0], [4865.0, 4567.0], ['359.8949717843059', '0.06430153163718179']], [[5, 4], [800.0, 656.0], [4865.0, 4711.0], ['359.8949717843059', '0.08398146542570789']], [[5, 5], [800.0, 800.0], [4865.0, 4855.0], ['359.8949717843058', '0.1036613793982855']], [[5, 6], [800.0, 944.0], [4865.0, 4999.0], ['359.8949717843059', '0.1233412689113129']], [[6, 0], [944.0, 80.0], [5009.0, 4135.0], ['359.8752918635997', '0.005261654188448438']], [[6, 1], [944.0, 224.0], [5009.0, 4279.0], ['359.8752918635997', '0.02494160601132736']], [[6, 2], [944.0, 368.0], [5009.0, 4423.0], ['359.8752918635997', '0.04462155194906044']], [[6, 3], [944.0, 512.0], [5009.0, 4567.0], ['359.8752918635997', '0.06430148735803921']], [[6, 4], [944.0, 656.0], [5009.0, 4711.0], ['359.8752918635997', '0.08398140759466759']], [[6, 5], [944.0, 800.0], [5009.0, 4855.0], ['359.8752918635997', '0.1036613080153593']], [[6, 6], [944.0, 944.0], [5009.0, 4999.0], ['359.8752918635997', '0.1233411839765937']]]
#################

def Make_Directory(Outpath):
    path=os.path.realpath(Outpath)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def Check_Directory(Path):
    """
    path=os.path.realpath(Path)
    directory = os.path.dirname(path)
    if os.path.exists(directory):
        return True
    return False
    """
    Glob_L=glob.glob(Path)
    if(len(Glob_L)>0):
        return True
    return False

def Check_Files(Phi, Theta, Counts, Background, Run_Count):
    #"./Wavdetect_Outputs/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"
    if __name__ == '__main__':
        Base_Directory_String=str(Phi)+"/"+str(Theta)+"/"+str(Counts)+"/"+str(Background)+"/"+str(Run_Count)
        Base_File_String=str(Phi)+"_"+str(Theta)+"_"+str(Counts)+"_"+str(Background)+"_"+str(Run_Count)
        #Sources_Directory="./Marx_Sources/"+Base_Directory_String+"/"
        #Sources_Marx_Parameters_Directory=Sources_Directory+Base_File_String+"/"
        #Injected_Sources_Directory="./Injected_Sources/"+Base_Directory_String+"/"
        #Wavdetect_Outputs/45/1/3/1E-1/1/45_1_3_1E-1_1_Standard_Outputs.csv
        Wavdetect_Outputs_Directory="./Wavdetect_Outputs/"+Base_Directory_String+"/"
        Wavdetect_Data_Filepath=Wavdetect_Outputs_Directory+Base_File_String+"_Standard_Outputs.csv"
        Check_Directory_Bool=Check_Directory(Wavdetect_Data_Filepath)
        return Check_Directory_Bool

def Main_Big_Input_Generator(Max_Runs=49):
    #Source_Coords_HL=Source_Coords_Generator()
    ##Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]], [15, [1, 2, 3, 4, 5, 6, 7, 8]], [30, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [45, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [60, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [75, [1, 2, 3, 4, 5, 6, 7, 8]], [90, [1, 2, 3, 4, 5, 6, 7, 8]], [105, [2, 3, 4, 5, 6, 7, 8]], [120, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [135, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [150, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [165, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [180, [1, 2, 3, 4, 5, 6, 7, 8]], [195, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [210, [2, 3, 4, 5, 6, 7, 8, 9, 10]], [225, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [240, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [255, [2, 3, 4, 5, 6, 7, 8, 9]], [270, [1, 2, 3, 4, 5, 6, 7, 8]], [285, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [300, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [315, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [330, [2, 3, 4, 5, 6, 7, 8, 9]], [345, [1, 3, 4, 5, 6, 7, 8]]]
    #Source_Coords_HL=[[0, [1, 2]]]
    #Source_Coords_HL=[[0, [1]]]
    #Source_Coords_HL=[[45, [10]]]
    #Source_Coords_HL=[[225, [10]]]
    ##Source_Coords_HL=[[45, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]]
    #Source_Coords_HL=[[45, [9, 10]]]
    Source_Coords_HL=[[0, [0]]]
    Max_Runs=Max_Runs+1
    Run_Count_L=list(np.arange(1,Max_Runs))
    #Run_Count_L=[Run_Count_L[16]] #For Testing
    #print("Run_Count_L: ", Run_Count_L)
    ###Background_Str_L=Source_Generator.Background_Str_List_Genertator()
    #Background_Str_L=Source_Generator.Background_Str_List_Genertator(Include_Zero_Bool=False)
    Background_Str_L=Source_Generator.Background_Str_List_Genertator(Factor_High=2, Append_End=9E-1)
    #Background_Str_L=[Background_Str_L[25]] #For Testing
    #Background_Str_L=[Background_Str_L[-1]] #For Testing
    #Background_Str_L=[Background_Str_L[0]] #For Testing
    ##Background_Str_L=[Background_Str_L[0],Background_Str_L[1]] #For Testing
    #print("Background_Str_L: ", Background_Str_L)
    Number_of_Sources=0
    Number_of_Runs=0
    Run_Input_L=[]
    for Source_Coords_L in Source_Coords_HL:
        Cur_Phi=Source_Coords_L[0]
        Cur_Theta_L=Source_Coords_L[1]
        for Cur_Theta in Cur_Theta_L:
            Cur_Coords=(Cur_Theta,Cur_Phi)
            Cur_Counts_L=Source_Generator.Counts_List_Genertator(Source_Generator.Max_Counts_Calc,Cur_Theta)
            #Cur_Counts_L=Source_Generator.Counts_List_Genertator(Source_Generator.Max_Counts_Calc,Cur_Theta, Include_Zero_Bool=False)
            #Cur_Counts_L=Counts_List_Genertator(Max_Counts_Calc_Broken,Cur_Theta)
            #Cur_Counts_L=[Cur_Counts_L[3]] #For Testing
            #Cur_Counts_L=[Cur_Counts_L[4]] #For Testing
            #Cur_Counts_L=[Cur_Counts_L[-1]] #For Testing
            #Cur_Counts_L=[Cur_Counts_L[2]] #For Testing
            #Cur_Counts_L=[Cur_Counts_L[0]] #For Testing
            #Cur_Counts_L=[Cur_Counts_L[0], Cur_Counts_L[1]] #For Testing
            #Cur_Counts_L=[1] #For Testing
            #Cur_Counts_L=[165,180,195,210] #For Testing
            Cur_Counts_L=[Cur_Counts_L[0], Cur_Counts_L[1], Cur_Counts_L[2]] #For Testing
            #print("Cur_Counts_L: ", Cur_Counts_L)
            Cur_RA,Cur_Dec=Source_Generator.MSC_to_CEL_Convert(Cur_Theta,Cur_Phi)
            Cur_X,Cur_Y=Source_Reproject.MSC_to_Physical_Convert(Cur_Theta,Cur_Phi)
            Cur_Chip_X, Cur_Chip_Y, Cur_Chip_ID=Source_Generator.MSC_to_Chip_Convert(Cur_Theta,Cur_Phi)
            for Cur_Counts in Cur_Counts_L:
                #print("Cur_Counts: ", Cur_Counts)
                #Number_of_Sources=Number_of_Sources+1
                for Cur_Background in Background_Str_L:
                    Cur_Background_Float=float(Cur_Background)
                    if((float(Cur_Background_Float)==0.0) and (int(Cur_Counts)==0)):
                        continue
                        #pass
                    Number_of_Sources=Number_of_Sources+1
                    for Run_Count in Run_Count_L:
                        Cur_Run_HL=[]
                        Number_of_Runs=Number_of_Runs+1

                        ###Source_Generator Inputs###
                        #Number_of_Runs=Number_of_Runs+1
                        ##Cur_Outpath="./Marx_Sources/"+str(Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Run_Count)+"/"+str(Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Run_Count)
                        Cur_Outpath_Source_Generator="./Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)
                        ##print("Cur_Outpath_Source_Generator: ", Cur_Outpath_Source_Generator)
                        Cur_Marx_Parameter_Outpath="./Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_marx.par"
                        #print("Cur_Marx_Parameter_Outpath: ", Cur_Marx_Parameter_Outpath)
                        Cur_Aspect_Parameter_Outpath="./Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_marxasp.par"
                        Cur_Seed,Cur_Seed_Biased=Source_Generator.Seed_Generator(Cur_Phi,Cur_Theta,Cur_Counts,Cur_Background,Run_Count=Run_Count)
                        ##Cur_Run_L=[Cur_Phi, Cur_Theta, Cur_RA, Cur_Dec, Cur_Counts, Cur_Background, Run_Count, Cur_Outpath_Source_Generator, Cur_Marx_Parameter_Outpath, Cur_Aspect_Parameter_Outpath, Cur_Seed, Cur_Seed_Biased]
                        ##Run_Input_L.append(Cur_Run_L)
                        Cur_Source_Generator_Run_L=[Cur_Phi, Cur_Theta, Cur_RA, Cur_Dec, Cur_Counts, Cur_Background, Run_Count, Cur_Outpath_Source_Generator, Cur_Marx_Parameter_Outpath, Cur_Aspect_Parameter_Outpath, Cur_Seed, Cur_Seed_Biased]
                        Cur_Run_HL.append(Cur_Source_Generator_Run_L)

                        ###Source_Reproject Inputs###
                        """
                        Run_Index=int(Run_Count-1)
                        Cur_Outpath_Source_Reproject="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)
                        ##print("Cur_Outpath_Source_Reproject: ", Cur_Outpath_Source_Reproject)
                        Cur_Source_Path="./Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+".fits"
                        #../Synthetic_Background_Generator/Synthetic_Backgrounds/0/1/78/8E-2/0_1_78_8E-2_bkg.fits
                        Cur_Synthetic_Background_Path="./Synthetic_Backgrounds/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_bkg.fits"
                        Cur_Reproject_Outpath=Cur_Outpath_Source_Reproject+"_Reprojected.fits"
                        Cur_Postage_Stamp_Coords=Postage_Stamp_Coords_L[Run_Index]
                        Cur_Injected_Outpath=Cur_Outpath_Source_Reproject+"_Injected.fits"
                        Cur_Postage_Stamp_Outpath=Cur_Outpath_Source_Reproject+"_Postage_Stamp.fits"
                        Cur_Postage_Stamp_No_Background_Outpath=Cur_Outpath_Source_Reproject+"_No_Background_Postage_Stamp.fits"
                        Cur_Postage_Stamp_No_Source_Outpath=Cur_Outpath_Source_Reproject+"_No_Source_Postage_Stamp.fits"
                        Cur_Reproject_Parameter_Path=Cur_Outpath_Source_Reproject+"_reproject_events.par"
                        Cur_Dmmerge_Parameter_Path=Cur_Outpath_Source_Reproject+"_dmmerge.par"
                        Cur_Dmcopy_Parameter_Path=Cur_Outpath_Source_Reproject+"_dmcopy.par"
                        #Cur_Run_L=[Cur_RA, Cur_Dec, Cur_Outpath_Source_Reproject, Cur_Source_Path, Cur_Synthetic_Background_Path, Cur_Reproject_Outpath, Cur_Injected_Outpath, Cur_Postage_Stamp_Outpath, Cur_Postage_Stamp_Coords, Cur_Reproject_Parameter_Path, Cur_Dmmerge_Parameter_Path, Cur_Dmcopy_Parameter_Path]
                        #Run_Input_L.append(Cur_Run_L)
                        ##Cur_Source_Reproject_Run_L=[Cur_RA, Cur_Dec, Cur_Outpath_Source_Reproject, Cur_Source_Path, Cur_Synthetic_Background_Path, Cur_Reproject_Outpath, Cur_Injected_Outpath, Cur_Postage_Stamp_Outpath, Cur_Postage_Stamp_Coords, Cur_Reproject_Parameter_Path, Cur_Dmmerge_Parameter_Path, Cur_Dmcopy_Parameter_Path, Cur_Background_Float, Cur_Counts]
                        Cur_Source_Reproject_Run_L=[Cur_RA, Cur_Dec, Cur_Outpath_Source_Reproject, Cur_Source_Path, Cur_Synthetic_Background_Path, Cur_Reproject_Outpath, Cur_Injected_Outpath, Cur_Postage_Stamp_Outpath, Cur_Postage_Stamp_Coords, Cur_Reproject_Parameter_Path, Cur_Dmmerge_Parameter_Path, Cur_Dmcopy_Parameter_Path, Cur_Background_Float, Cur_Counts,  Cur_Postage_Stamp_No_Background_Outpath, Cur_Postage_Stamp_No_Source_Outpath]
                        Cur_Run_HL.append(Cur_Source_Reproject_Run_L)
                        """
                        Run_Index=int(Run_Count-1)
                        #Number_of_Runs=Number_of_Runs+1
                        Cur_Outpath_Source_Reproject="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)
                        ##print("Cur_Outpath_Source_Reproject: ", Cur_Outpath_Source_Reproject)
                        Cur_Source_Path="./Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+".fits"
                        #../Synthetic_Background_Generator/Synthetic_Backgrounds/0/1/78/8E-2/0_1_78_8E-2_bkg.fits
                        ###Cur_Synthetic_Background_Path="./Synthetic_Backgrounds/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_bkg.fits"
                        Cur_Synthetic_Background_Path="/Volumes/expansion/Marx_Testing/Synthetic_Backgrounds/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_bkg.fits"
                        Cur_Reproject_Outpath=Cur_Outpath_Source_Reproject+"_Reprojected.fits"
                        Cur_Postage_Stamp_Coords=Postage_Stamp_Coords_L[Run_Index]
                        Cur_Injected_Outpath=Cur_Outpath_Source_Reproject+"_Injected.fits"
                        Cur_Postage_Stamp_Outpath=Cur_Outpath_Source_Reproject+"_Postage_Stamp.fits"
                        Cur_Postage_Stamp_No_Background_Outpath=Cur_Outpath_Source_Reproject+"_No_Background_Postage_Stamp.fits"
                        Cur_Postage_Stamp_No_Source_Outpath=Cur_Outpath_Source_Reproject+"_No_Source_Postage_Stamp.fits"
                        Cur_Postage_Stamp_Original_Source_Outpath=Cur_Outpath_Source_Reproject+"_Original_Source_Postage_Stamp.fits"
                        #Cur_Run_L=[Cur_Phi, Cur_Theta, Cur_RA, Cur_Dec, Cur_Counts, Cur_Background, Run_Count, Cur_Outpath_Source_Reproject, Cur_Parameter_Outpath, Cur_Aspect_Parameter_Outpath, Cur_Postage_Stamp_Coords, Cur_Seed, Cur_Seed_Biased]
                        Cur_Reproject_Parameter_Path=Cur_Outpath_Source_Reproject+"_reproject_events.par"
                        Cur_Dmmerge_Parameter_Path=Cur_Outpath_Source_Reproject+"_dmmerge.par"
                        Cur_Dmcopy_Parameter_Path=Cur_Outpath_Source_Reproject+"_dmcopy.par"
                        ##Cur_Run_L=[Cur_RA, Cur_Dec, Cur_Outpath_Source_Reproject, Cur_Source_Path, Cur_Synthetic_Background_Path, Cur_Reproject_Outpath, Cur_Injected_Outpath, Cur_Postage_Stamp_Outpath, Cur_Postage_Stamp_Coords, Cur_Reproject_Parameter_Path, Cur_Dmmerge_Parameter_Path, Cur_Dmcopy_Parameter_Path, Cur_Background_Float, Cur_Counts]
                        Cur_Source_Reproject_Run_L=[Cur_RA, Cur_Dec, Cur_Outpath_Source_Reproject, Cur_Source_Path, Cur_Synthetic_Background_Path, Cur_Reproject_Outpath, Cur_Injected_Outpath, Cur_Postage_Stamp_Outpath, Cur_Postage_Stamp_Coords, Cur_Reproject_Parameter_Path, Cur_Dmmerge_Parameter_Path, Cur_Dmcopy_Parameter_Path, Cur_Background_Float, Cur_Counts, Cur_Postage_Stamp_No_Background_Outpath, Cur_Postage_Stamp_No_Source_Outpath, Cur_X, Cur_Y, Cur_Postage_Stamp_Original_Source_Outpath]
                        Cur_Run_HL.append(Cur_Source_Reproject_Run_L)

                        ###Source_Detect Inputs###

                        """
                        Run_Index=int(Run_Count-1)
                        Cur_Outpath_Source_Detect="./Wavdetect_Outputs/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)
                        Cur_Postage_Stamp_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Postage_Stamp.fits"
                        Cur_PSF_Outpath=Cur_Outpath_Source_Detect+"_PSF.fits"
                        Cur_Postage_Stamp_Coords=Postage_Stamp_Coords_L[Run_Index]
                        Cur_Wavdetect_Outfile=Cur_Outpath_Source_Detect+"_Wavdetect.fits"
                        ##Cur_Source_Detect_Run_L=[Cur_Outpath_Source_Detect, Cur_Postage_Stamp_Outpath, Cur_PSF_Outpath, Cur_Wavdetect_Outfile, Cur_Postage_Stamp_Coords]
                        Cur_Source_Detect_Run_L=[Cur_Outpath_Source_Detect, Cur_Postage_Stamp_Outpath, Cur_PSF_Outpath, Cur_Wavdetect_Outfile, Cur_Postage_Stamp_Coords, Cur_Background_Float, Cur_Counts]
                        #Run_Input_L.append(Cur_Run_L)
                        """
                        """
                        Run_Index=int(Run_Count-1)
                        Number_of_Runs=Number_of_Runs+1
                        Cur_Outpath_Source_Detect="./Wavdetect_Outputs/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)
                        Cur_Postage_Stamp_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Postage_Stamp.fits"
                        Cur_Postage_Stamp_No_Background_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_No_Background_Postage_Stamp.fits"
                        Cur_Postage_Stamp_No_Source_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_No_Source_Postage_Stamp.fits"
                        Cur_Postage_Stamp_Original_Source_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Original_Source_Postage_Stamp.fits"
                        Cur_PSF_Outpath=Cur_Outpath_Source_Detect+"_PSF.fits"
                        Cur_Postage_Stamp_Coords=Postage_Stamp_Coords_L[Run_Index]
                        Cur_Wavdetect_Outfile=Cur_Outpath_Source_Detect+"_Wavdetect.fits"
                        Cur_Wavdetect_No_Background_Outfile=Cur_Outpath_Source_Detect+"_No_Background_Wavdetect.fits"
                        Cur_Wavdetect_No_Source_Outfile=Cur_Outpath_Source_Detect+"_No_Source_Wavdetect.fits"
                        Cur_Reproject_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Reprojected.fits"
                        Cur_Source_Aspect_Path="./Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_asol1.fits"
                        Cur_Source_Path="./Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+".fits"
                        Cur_Source_Detect_Run_L=[Cur_Outpath_Source_Detect, Cur_Postage_Stamp_Outpath, Cur_PSF_Outpath, Cur_Wavdetect_Outfile, Cur_Postage_Stamp_Coords, Cur_Background_Float, Cur_Counts, Cur_Postage_Stamp_No_Background_Outpath, Cur_Postage_Stamp_No_Source_Outpath, Cur_Wavdetect_No_Background_Outfile, Cur_Wavdetect_No_Source_Outfile, Cur_Postage_Stamp_Original_Source_Outpath, Cur_Reproject_Outpath, Cur_Source_Aspect_Path, Cur_Source_Path, Cur_Chip_ID]
                        """
                        Run_Index=int(Run_Count-1)
                        #Number_of_Runs=Number_of_Runs+1
                        Cur_Outpath_Source_Detect="./Wavdetect_Outputs/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)
                        Cur_Postage_Stamp_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Postage_Stamp.fits"
                        Cur_Postage_Stamp_No_Background_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_No_Background_Postage_Stamp.fits"
                        Cur_Postage_Stamp_No_Source_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_No_Source_Postage_Stamp.fits"
                        Cur_Postage_Stamp_Original_Source_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Original_Source_Postage_Stamp.fits"
                        Cur_PSF_Outpath=Cur_Outpath_Source_Detect+"_PSF.fits"
                        Cur_Postage_Stamp_Coords=Postage_Stamp_Coords_L[Run_Index]
                        Cur_Wavdetect_Outfile=Cur_Outpath_Source_Detect+"_Wavdetect.fits"
                        Cur_Wavdetect_No_Background_Outfile=Cur_Outpath_Source_Detect+"_No_Background_Wavdetect.fits"
                        Cur_Wavdetect_No_Background_Fixed_Outfile=Cur_Outpath_Source_Detect+"_No_Background_Fixed_Wavdetect.fits"
                        Cur_Wavdetect_No_Source_Outfile=Cur_Outpath_Source_Detect+"_No_Source_Wavdetect.fits"
                        Cur_Wavdetect_No_Source_Fixed_Outfile=Cur_Outpath_Source_Detect+"_No_Source_Fixed_Wavdetect.fits"
                        Cur_Wavdetect_No_Source_Control_Outfile=Cur_Outpath_Source_Detect+"_No_Source_Control_Wavdetect.fits"
                        Cur_Wavdetect_No_Source_Control_Fixed_Outfile=Cur_Outpath_Source_Detect+"_No_Source_Control_Fixed_Wavdetect.fits"
                        Cur_Reproject_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Reprojected.fits"
                        Cur_Source_Aspect_Path="./Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_asol1.fits"
                        Cur_Source_Path="./Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+".fits"
                        Cur_Injected_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Injected.fits"
                        Cur_Wavdetect_Scale_16_Outfile=Cur_Outpath_Source_Detect+"_Scale_16_Wavdetect.fits"
                        #Cur_Run_L=[Cur_Outpath_Source_Detect, Cur_Postage_Stamp_Outpath, Cur_PSF_Outpath, Cur_Wavdetect_Outfile, Cur_Postage_Stamp_Coords, Cur_Background_Float, Cur_Counts, Cur_Postage_Stamp_No_Background_Outpath, Cur_Postage_Stamp_No_Source_Outpath, Cur_Wavdetect_No_Background_Outfile, Cur_Wavdetect_No_Source_Outfile, Cur_Postage_Stamp_Original_Source_Outpath, Cur_Reproject_Outpath, Cur_Source_Aspect_Path, Cur_Source_Path, Cur_Chip_ID]
                        ##Cur_Source_Detect_Run_L=[Cur_Outpath_Source_Detect, Cur_Postage_Stamp_Outpath, Cur_PSF_Outpath, Cur_Wavdetect_Outfile, Cur_Postage_Stamp_Coords, Cur_Background_Float, Cur_Counts, Cur_Postage_Stamp_No_Background_Outpath, Cur_Postage_Stamp_No_Source_Outpath, Cur_Wavdetect_No_Background_Outfile, Cur_Wavdetect_No_Background_Fixed_Outfile, Cur_Wavdetect_No_Source_Outfile, Cur_Postage_Stamp_Original_Source_Outpath, Cur_Reproject_Outpath, Cur_Source_Aspect_Path, Cur_Source_Path, Cur_Chip_ID, Cur_Phi, Cur_Theta, Cur_Injected_Outpath]
                        Cur_Source_Detect_Run_L=[Cur_Outpath_Source_Detect, Cur_Postage_Stamp_Outpath, Cur_PSF_Outpath, Cur_Wavdetect_Outfile, Cur_Postage_Stamp_Coords, Cur_Background_Float, Cur_Counts, Cur_Postage_Stamp_No_Background_Outpath, Cur_Postage_Stamp_No_Source_Outpath, Cur_Wavdetect_No_Background_Outfile, Cur_Wavdetect_No_Background_Fixed_Outfile, Cur_Wavdetect_No_Source_Outfile, Cur_Postage_Stamp_Original_Source_Outpath, Cur_Reproject_Outpath, Cur_Source_Aspect_Path, Cur_Source_Path, Cur_Chip_ID, Cur_Phi, Cur_Theta, Cur_Injected_Outpath, Cur_Wavdetect_Scale_16_Outfile, Cur_Wavdetect_No_Source_Fixed_Outfile, Cur_Wavdetect_No_Source_Control_Outfile, Cur_Wavdetect_No_Source_Control_Fixed_Outfile]

                        Cur_Run_HL.append(Cur_Source_Detect_Run_L)

                        ###Cleanup_Files###

                        Cleanup_Run_L=[Cur_Phi, Cur_Theta, Cur_Counts, Cur_Background, Run_Count]
                        #print("Cleanup_Run_L: ", Cleanup_Run_L)
                        Cur_Run_HL.append(Cleanup_Run_L)

                        Run_Input_L.append(Cur_Run_HL)
    #print("Number_of_Sources: ", Number_of_Sources)
    print("Number_of_Runs: ", Number_of_Runs)
    return Run_Input_L

def Cleanup_Files(Phi, Theta, Counts, Background, Run_Count):
    #"./Wavdetect_Outputs/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"
    if __name__ == '__main__':
        Base_Directory_String=str(Phi)+"/"+str(Theta)+"/"+str(Counts)+"/"+str(Background)+"/"+str(Run_Count)
        Base_File_String=str(Phi)+"_"+str(Theta)+"_"+str(Counts)+"_"+str(Background)+"_"+str(Run_Count)
        Sources_Directory="./Marx_Sources/"+Base_Directory_String+"/"
        Sources_Marx_Parameters_Directory=Sources_Directory+Base_File_String+"/"
        Injected_Sources_Directory="./Injected_Sources/"+Base_Directory_String+"/"
        Wavdetect_Outputs_Directory="./Wavdetect_Outputs/"+Base_Directory_String+"/"
        Wavdetect_Parameters_Directory=Wavdetect_Outputs_Directory+Base_File_String+"/"
        Wavdetect_Parameters_Directory_Cxcds_Param4=Wavdetect_Parameters_Directory+"cxcds_param4/"
        Wavdetect_Tempdir_Directory=Wavdetect_Parameters_Directory+"tmpdir/"
        #Path_L=[Sources_Directory, Sources_Marx_Parameters_Directory, Injected_Sources_Directory, Wavdetect_Outputs_Directory, Wavdetect_Parameters_Directory]
        #Path_L=[Sources_Marx_Parameters_Directory, Sources_Directory, Injected_Sources_Directory, Wavdetect_Parameters_Directory, Wavdetect_Outputs_Directory]
        Path_L=[Sources_Marx_Parameters_Directory, Sources_Directory, Injected_Sources_Directory, Wavdetect_Tempdir_Directory, Wavdetect_Parameters_Directory_Cxcds_Param4, Wavdetect_Parameters_Directory, Wavdetect_Outputs_Directory]
        print("Path_L: ", Path_L)
        for Path in Path_L:
            if(Path[0]!="."):
                raise "Incorrect Delete Path!!!: The current path is does NOT start in the CWD!!!"
            if(len(Path)<=15):
                raise "Incorrect Delete Path!!!: The current path is to short to be a vaild path!!!"
            #Command_Prefix="ls"
            Command_Prefix="rm"
            Command_Suffix_L=["*.fits", "*.fit", "*.par", "*.dat","*.reg", "*.asphist"]
            for Command_Suffix in Command_Suffix_L:
                Path_Command=str(Path)+Command_Suffix
                print("Path_Command: ", Path_Command)
                Path_Command_Glob_L=glob.glob(Path_Command)
                if(len(Path_Command_Glob_L)==0):
                    continue
                #Command=Command_Prefix+" "+str(Path)+Command_Suffix
                Command=Command_Prefix+" "+Path_Command
                print("Command: ", Command)
                os.system(Command)
            if(Path==Wavdetect_Outputs_Directory):
                continue
            #Delete_Directory_Command="ls "+Path
            Delete_Directory_Command="rmdir "+Path
            print("Delete_Directory_Command: ", Delete_Directory_Command)
            os.system(Delete_Directory_Command)



def Driver(Func, Array):
    if __name__ == '__main__':
        P = Pool()
        P.map(Func, Array)

def Main_Wrapper(Input_HL):

    ###Check Files###
    Input_L=Input_HL[3]
    Phi=Input_L[0]
    Theta=Input_L[1]
    Counts=Input_L[2]
    Background=Input_L[3]
    Run_Count=Input_L[4]


    Check_Files_Bool=Check_Files(Phi, Theta, Counts, Background, Run_Count)

    if(Check_Files_Bool): #Prevents Clobbering
        return

    start_time = time.time()
    ###Source_Generator###

    #Cur_Run_L=[Cur_Phi, Cur_Theta, Cur_RA, Cur_Dec, Cur_Counts, Cur_Background, Run_Count, Cur_Outpath, Cur_Parameter_Outpath, Cur_Aspect_Parameter_Outpath, Cur_Seed, Cur_Seed_Biased]

    Input_L=Input_HL[0]
    Cur_Counts=Input_L[4]
    Cur_RA=Input_L[2]
    Cur_Dec=Input_L[3]
    Cur_Outpath=Input_L[7]
    Cur_Parameter_Outpath=Input_L[8]
    Cur_Aspect_Parameter_Outpath=Input_L[9]
    Seed_Biased=Input_L[11]
    Source_Generator.Source_Generator(Cur_Counts, Cur_RA, Cur_Dec, Seed_Biased, Outpath=Cur_Outpath, Parameter_Outpath=Cur_Parameter_Outpath, Aspect_Parameter_Outpath=Cur_Aspect_Parameter_Outpath, MSC_TO_CEL_Convert_Bool=False)

    ###Source_Reproject###

    """
    Input_L=Input_HL[1]
    Outpath=Input_L[2]
    Source_Path=Input_L[3]
    Source_RA=float(Input_L[0])
    Source_Dec=float(Input_L[1])
    Postage_Stamp_Coords=Input_L[8]
    Reproject_Outpath=Input_L[5]
    Synthetic_Background_Path=Input_L[4]
    Injected_Outpath=Input_L[6]
    Postage_Stamp_Outpath=Input_L[7]
    Reproject_Parameter_Path=Input_L[9]
    Dmmerge_Parameter_Path=Input_L[10]
    Dmcopy_Parameter_Path=Input_L[11]
    Background_Float=Input_L[12]
    Counts=Input_L[13]
    Postage_Stamp_No_Background_Outpath=Input_L[14]
    Postage_Stamp_No_Source_Outpath=Input_L[15]
    #Postage_Stamp_Coords[0]=[[0, 0], [80.0, 80.0], [4145.0, 4135.0], ['359.9933716666962', '0.005261666616669011']]
    Physical_Coords=Postage_Stamp_Coords[2]
    X=Physical_Coords[0]
    Y=Physical_Coords[1]
    Target_Cel_Coords=Postage_Stamp_Coords[3]
    Target_RA=float(Target_Cel_Coords[0])
    Target_Dec=float(Target_Cel_Coords[1])
    Make_Directory(Outpath)
    if(Counts==0):
        Source_Reproject.Crop_Image_Centered(X, Y, Synthetic_Background_Path, Postage_Stamp_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
    if(Counts>0):
        Source_Reproject.Source_Reproject(Source_Path, Source_RA, Source_Dec, Target_RA, Target_Dec, Reproject_Outpath, Reproject_Parameter_Path, Counts)
    if(Background_Float==0.0):
        Source_Reproject.Crop_Image_Centered(X, Y, Reproject_Outpath, Postage_Stamp_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
    else:
        Source_Reproject.Source_Injection(Reproject_Outpath, Synthetic_Background_Path, Injected_Outpath, Dmmerge_Parameter_Path, Background_Float, Counts)
        Source_Reproject.Crop_Image_Centered(X, Y, Injected_Outpath, Postage_Stamp_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
        ####No Background####
        Source_Reproject.Crop_Image_Centered(X, Y, Reproject_Outpath, Postage_Stamp_No_Background_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
        ####No Source####
        Source_Reproject.Crop_Image_Centered(X, Y, Synthetic_Background_Path, Postage_Stamp_No_Source_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
    """
    #print("Source_Reproject!!!")
    Input_L=Input_HL[1]
    Outpath=Input_L[2]
    Source_Path=Input_L[3]
    Source_RA=float(Input_L[0])
    Source_Dec=float(Input_L[1])
    Postage_Stamp_Coords=Input_L[8]
    Reproject_Outpath=Input_L[5]
    Synthetic_Background_Path=Input_L[4]
    Injected_Outpath=Input_L[6]
    Postage_Stamp_Outpath=Input_L[7]
    Reproject_Parameter_Path=Input_L[9]
    Dmmerge_Parameter_Path=Input_L[10]
    Dmcopy_Parameter_Path=Input_L[11]
    Background_Float=Input_L[12]
    Counts=Input_L[13]
    Postage_Stamp_No_Background_Outpath=Input_L[14]
    Postage_Stamp_No_Source_Outpath=Input_L[15]
    X_Original_Source=Input_L[16]
    Y_Original_Source=Input_L[17]
    Postage_Stamp_Original_Source_Outpath=Input_L[18]
    #Postage_Stamp_Coords[0]=[[0, 0], [80.0, 80.0], [4145.0, 4135.0], ['359.9933716666962', '0.005261666616669011']]
    Physical_Coords=Postage_Stamp_Coords[2]
    X=Physical_Coords[0]
    Y=Physical_Coords[1]
    Target_Cel_Coords=Postage_Stamp_Coords[3]
    Target_RA=float(Target_Cel_Coords[0])
    Target_Dec=float(Target_Cel_Coords[1])
    Make_Directory(Outpath)
    """
    Source_Reproject(Source_Path, Source_RA, Source_Dec, Target_RA, Target_Dec, Reproject_Outpath, Reproject_Parameter_Path, Counts)
    Source_Injection(Reproject_Outpath, Synthetic_Background_Path, Injected_Outpath, Dmmerge_Parameter_Path, Background_Float, Counts)
    Crop_Image_Centered(X, Y, Injected_Outpath, Postage_Stamp_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
    """
    Source_Reproject.Crop_Image_Centered(X_Original_Source, Y_Original_Source, Source_Path, Postage_Stamp_Original_Source_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
    if(Counts==0):
        Source_Reproject.Crop_Image_Centered(X, Y, Synthetic_Background_Path, Postage_Stamp_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
    if(Counts>0):
        Source_Reproject.Source_Reproject(Source_Path, Source_RA, Source_Dec, Target_RA, Target_Dec, Reproject_Outpath, Reproject_Parameter_Path, Counts)
    if(Background_Float==0.0):
        Source_Reproject.Crop_Image_Centered(X, Y, Reproject_Outpath, Postage_Stamp_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
    else:
        Source_Reproject.Source_Injection(Reproject_Outpath, Synthetic_Background_Path, Injected_Outpath, Dmmerge_Parameter_Path, Background_Float, Counts)
        #Source_Reproject.Swap_Header(Injected_Outpath, Synthetic_Background_Path)
        Source_Reproject.Crop_Image_Centered(X, Y, Injected_Outpath, Postage_Stamp_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
        #Source_Reproject.Swap_Header(Postage_Stamp_Outpath, Synthetic_Background_Path)
        ####No Background####
        Source_Reproject.Crop_Image_Centered(X, Y, Reproject_Outpath, Postage_Stamp_No_Background_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
        ####No Source####
        Source_Reproject.Crop_Image_Centered(X, Y, Synthetic_Background_Path, Postage_Stamp_No_Source_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)

    ###Source_Detect###
    #print("Source_Detect!!!")

    """
    Input_L=Input_HL[2]
    Outpath=Input_L[0]
    Postage_Stamp_Outpath=Input_L[1]
    PSF_Outpath=Input_L[2]
    Wavdetect_Outfile=Input_L[3]
    Postage_Stamp_Coords=Input_L[4]
    Background_Float=Input_L[5]
    Counts=Input_L[6]
    #Postage_Stamp_Coords[0]=[[0, 0], [80.0, 80.0], [4145.0, 4135.0], ['359.9933716666962', '0.005261666616669011']]
    Target_Physical_Coords=Postage_Stamp_Coords[2]
    Target_X=Target_Physical_Coords[0]
    Target_Y=Target_Physical_Coords[1]
    Make_Directory(Outpath)
    Source_Detect.Make_PSF_Map(Postage_Stamp_Outpath, PSF_Outpath, Outpath, Background_Float, Counts)
    Source_Detect.Wavdetect(Postage_Stamp_Outpath, Outpath, PSF_Outpath, Background_Float, Counts)
    Source_Detect.Save_Detection_Bool(Wavdetect_Outfile, Target_X, Target_Y, Outpath, Background_Float, Counts)
    """
    Input_L=Input_HL[2]
    Outpath=Input_L[0]
    Postage_Stamp_Outpath=Input_L[1]
    PSF_Outpath=Input_L[2]
    Wavdetect_Outfile=Input_L[3]
    Postage_Stamp_Coords=Input_L[4]
    Background_Float=Input_L[5]
    Counts=Input_L[6]
    Postage_Stamp_No_Background_Outpath=Input_L[7]
    Postage_Stamp_No_Source_Outpath=Input_L[8]
    Wavdetect_No_Background_Outfile=Input_L[9]
    Wavdetect_No_Background_Fixed_Outfile=Input_L[10]
    Wavdetect_No_Source_Outfile=Input_L[11]
    Postage_Stamp_Original_Source_Outpath=Input_L[12]
    Reproject_Outpath=Input_L[13]
    Source_Aspect_Path=Input_L[14]
    Source_Path=Input_L[15]
    Chip_ID=Input_L[16]
    Phi=Input_L[17]
    Theta=Input_L[18]
    Injected_Outpath=Input_L[19]
    Wavdetect_Scale_16_Outfile=Input_L[20]
    Wavdetect_No_Source_Fixed_Outfile=Input_L[21]
    Wavdetect_No_Source_Control_Outfile=Input_L[22]
    Wavdetect_No_Source_Control_Fixed_Outfile=Input_L[23]
    #Postage_Stamp_Coords[0]=[[0, 0], [80.0, 80.0], [4145.0, 4135.0], ['359.9933716666962', '0.005261666616669011']]
    Target_Chip_Coords=Postage_Stamp_Coords[1]
    Chip_X=Target_Chip_Coords[0]
    Chip_Y=Target_Chip_Coords[1]
    Target_Physical_Coords=Postage_Stamp_Coords[2]
    Target_X=Target_Physical_Coords[0]
    Target_Y=Target_Physical_Coords[1]

    Make_Directory(Outpath)
    Source_Detect.Make_PSF_Map(Postage_Stamp_Original_Source_Outpath, PSF_Outpath, Outpath, Background_Float, Counts)
    Source_Detect.Make_Expsoure_Map(Outpath, Source_Path, Reproject_Outpath, Source_Aspect_Path, Chip_X, Chip_Y, Chip_ID, Target_X, Target_Y)
    #Fluximage(Outpath, Source_Path, Reproject_Outpath, Source_Aspect_Path, Postage_Stamp_Outpath)
    Source_Detect.Wavdetect(Postage_Stamp_Outpath, Outpath, PSF_Outpath, Background_Float, Counts)
    #Source_Detect.Wavdetect(Postage_Stamp_No_Source_Outpath, Outpath, PSF_Outpath, Background_Float, Counts)
    Source_Detection_Bool, Source_Detection_Amount=Source_Detect.Source_Detection_Bool_Calc(Wavdetect_Outfile, Target_X, Target_Y)
    #Source_Detect.Wavdetect(Postage_Stamp_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Scales="'1 2 4 8 16'", Key="_Scale_16")
    #Source_Detection_Bool_Scale_16, Source_Detection_Amount_Scale_16=Source_Detect.Source_Detection_Bool_Calc(Wavdetect_Scale_16_Outfile, Target_X, Target_Y)
    M,BACKSCAL=Source_Detect.BACKSCAL_Calc(Phi, Theta)
    Ideal_Parameter_Tuple=Source_Detect.Ideal_Type_I_Parameters_Calc(Phi, Theta, Background_Float, Counts)
    Background_Area=Ideal_Parameter_Tuple[3]
    P_B_Ideal=Source_Detect.Ideal_Type_I_Calc(Phi, Theta, Background_Float, Counts, Parameter_Tuple=Ideal_Parameter_Tuple)
    Ideal_Type_II_Source_Detection_Bool=Source_Detect.Type_II_Calc(P_B_Ideal)
    Empirical_Parameter_Tuple=Source_Detect.Empirical_Type_I_Parameters_Calc(Injected_Outpath, Phi, Theta, Target_X, Target_Y)
    Empirical_Enclosed_Source_Counts=Source_Detect.Empirical_Isolated_Counts_Calc(Reproject_Outpath, Phi, Theta, Target_X, Target_Y)
    Empirical_Background_Counts=Empirical_Parameter_Tuple[1]
    Empirical_Background=float(Empirical_Background_Counts)/float(Background_Area)
    P_B_Empirical=Source_Detect.Empirical_Type_I_Calc(Postage_Stamp_Outpath, Phi, Theta, Target_X, Target_Y, Background_Float, Counts, Parameter_Tuple=Empirical_Parameter_Tuple)
    Empirical_Type_II_Source_Detection_Bool=Source_Detect.Type_II_Calc(P_B_Empirical)
    if((float(Background_Float)>0) and (int(Counts)>0)):
        ####No Background####
        Source_Detect.Wavdetect(Postage_Stamp_No_Background_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Background")
        Source_Detection_Bool_No_Background, Source_Detection_Amount_No_Background=Source_Detect.Source_Detection_Bool_Calc(Wavdetect_No_Background_Outfile, Target_X, Target_Y)
        Source_Detect.Wavdetect(Postage_Stamp_No_Background_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Background_Fixed", Input_Background_Bool=True)
        Source_Detection_Bool_No_Background_Fixed, Source_Detection_Amount_No_Background_Fixed=Source_Detect.Source_Detection_Bool_Calc(Wavdetect_No_Background_Fixed_Outfile, Target_X, Target_Y)
        ####No Source####
        ##Source_Detect.Wavdetect(Postage_Stamp_No_Source_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Source", Input_Background_Bool=True)
        #Source_Detect.Wavdetect(Postage_Stamp_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Source", Input_Background_Bool=True)
        Source_Detect.Wavdetect(Postage_Stamp_No_Source_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Source")
        #Source_Detect.Wavdetect(Postage_Stamp_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Source", Input_Background_Bool=True)
        #Source_Detect.Wavdetect(Postage_Stamp_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Source")
        Source_Detection_Bool_No_Source, Source_Detection_Amount_No_Source=Source_Detect.Source_Detection_Bool_Calc(Wavdetect_No_Source_Outfile, Target_X, Target_Y)
        Source_Detect.Wavdetect(Postage_Stamp_No_Source_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Source_Fixed", Input_Background_Bool=True)
        Source_Detection_Bool_No_Source_Fixed, Source_Detection_Amount_No_Source_Fixed=Source_Detect.Source_Detection_Bool_Calc(Wavdetect_No_Source_Fixed_Outfile, Target_X, Target_Y)

        Source_Detect.Wavdetect(Postage_Stamp_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Source_Control")
        Source_Detection_Bool_No_Source_Control, Source_Detection_Amount_No_Source_Control=Source_Detect.Source_Detection_Bool_Calc(Wavdetect_No_Source_Control_Outfile, Target_X, Target_Y)
        Source_Detect.Wavdetect(Postage_Stamp_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Source_Control_Fixed", Input_Background_Bool=True)
        Source_Detection_Bool_No_Source_Control_Fixed, Source_Detection_Amount_No_Source_Control_Fixed=Source_Detect.Source_Detection_Bool_Calc(Wavdetect_No_Source_Control_Fixed_Outfile, Target_X, Target_Y)

        #Outfile_Str=str(Source_Detection_Bool)+","+str(Source_Detection_Amount)+","+str(Source_Detection_Bool_No_Background)+","+str(Source_Detection_Amount_No_Background)+","+str(Source_Detection_Bool_No_Background_Fixed)+","+str(Source_Detection_Amount_No_Background_Fixed)+","+str(Source_Detection_Bool_No_Source)+","+str(Source_Detection_Amount_No_Source)+","+str(M)+","+str(BACKSCAL)+","+str(Background_Area)+","+str(P_B_Ideal)+","+str(Ideal_Type_II_Source_Detection_Bool)+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(Empirical_Background)+","+str(P_B_Empirical)+","+str(Empirical_Type_II_Source_Detection_Bool)
        ##Outfile_Str=str(int(Source_Detection_Bool))+","+str(Source_Detection_Amount)+","+str(int(Source_Detection_Bool_No_Background))+","+str(Source_Detection_Amount_No_Background)+","+str(int(Source_Detection_Bool_No_Background_Fixed))+","+str(Source_Detection_Amount_No_Background_Fixed)+","+str(int(Source_Detection_Bool_No_Source))+","+str(Source_Detection_Amount_No_Source)+","+str(M)+","+str(BACKSCAL)+","+str(np.round(Background_Area,5))+","+str(np.round(P_B_Ideal,5))+","+str(int(Ideal_Type_II_Source_Detection_Bool))+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(np.round(Empirical_Background,5))+","+str(np.round(P_B_Empirical,5))+","+str(int(Empirical_Type_II_Source_Detection_Bool))
        ##Outfile_Str=str(int(Source_Detection_Bool))+","+str(Source_Detection_Amount)+","+str(int(Source_Detection_Bool_No_Background))+","+str(Source_Detection_Amount_No_Background)+","+str(int(Source_Detection_Bool_No_Background_Fixed))+","+str(Source_Detection_Amount_No_Background_Fixed)+","+str(int(Source_Detection_Bool_No_Source))+","+str(Source_Detection_Amount_No_Source)+","+str(M)+","+str(BACKSCAL)+","+str(np.round(Background_Area,5))+","+str(P_B_Ideal)+","+str(int(Ideal_Type_II_Source_Detection_Bool))+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(np.round(Empirical_Background,5))+","+str(P_B_Empirical)+","+str(int(Empirical_Type_II_Source_Detection_Bool))
        #Outfile_Str=str(int(Source_Detection_Bool))+","+str(Source_Detection_Amount)+","+str(int(Source_Detection_Bool_No_Background))+","+str(Source_Detection_Amount_No_Background)+","+str(int(Source_Detection_Bool_No_Source))+","+str(Source_Detection_Amount_No_Source)+","+str(M)+","+str(BACKSCAL)+","+str(np.round(Background_Area,5))+","+str(P_B_Ideal)+","+str(int(Ideal_Type_II_Source_Detection_Bool))+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(np.round(Empirical_Background,5))+","+str(P_B_Empirical)+","+str(int(Empirical_Type_II_Source_Detection_Bool))
        ##Outfile_Str=str(int(Source_Detection_Bool))+","+str(Source_Detection_Amount)+","+str(int(Source_Detection_Bool_No_Background))+","+str(Source_Detection_Amount_No_Background)+","+str(int(Source_Detection_Bool_No_Background_Fixed))+","+str(Source_Detection_Amount_No_Background_Fixed)+","+str(int(Source_Detection_Bool_No_Source))+","+str(Source_Detection_Amount_No_Source)+","+str(int(Source_Detection_Bool_No_Source_Fixed))+","+str(Source_Detection_Amount_No_Source_Fixed)+","+str(M)+","+str(BACKSCAL)+","+str(np.round(Background_Area,5))+","+str(P_B_Ideal)+","+str(int(Ideal_Type_II_Source_Detection_Bool))+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(np.round(Empirical_Background,5))+","+str(P_B_Empirical)+","+str(int(Empirical_Type_II_Source_Detection_Bool))
        Outfile_Str=str(int(Source_Detection_Bool))+","+str(Source_Detection_Amount)+","+str(int(Source_Detection_Bool_No_Background))+","+str(Source_Detection_Amount_No_Background)+","+str(int(Source_Detection_Bool_No_Background_Fixed))+","+str(Source_Detection_Amount_No_Background_Fixed)+","+str(int(Source_Detection_Bool_No_Source))+","+str(Source_Detection_Amount_No_Source)+","+str(int(Source_Detection_Bool_No_Source_Fixed))+","+str(Source_Detection_Amount_No_Source_Fixed)+","+str(int(Source_Detection_Bool_No_Source_Control))+","+str(Source_Detection_Amount_No_Source_Control)+","+str(int(Source_Detection_Bool_No_Source_Control_Fixed))+","+str(Source_Detection_Amount_No_Source_Control_Fixed)+","+str(M)+","+str(BACKSCAL)+","+str(np.round(Background_Area,5))+","+str(P_B_Ideal)+","+str(int(Ideal_Type_II_Source_Detection_Bool))+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(np.round(Empirical_Background,5))+","+str(P_B_Empirical)+","+str(int(Empirical_Type_II_Source_Detection_Bool))


    else:
        #Outfile_Str=str(Source_Detection_Bool)+","+str(Source_Detection_Amount)+","+","+","+","+","+","+","+str(M)+","+str(BACKSCAL)+","+str(Background_Area)+","+str(P_B_Ideal)+","+str(Ideal_Type_II_Source_Detection_Bool)+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(Empirical_Background)+","+str(P_B_Empirical)+","+str(Empirical_Type_II_Source_Detection_Bool)
        ##Outfile_Str=str(int(Source_Detection_Bool))+","+str(Source_Detection_Amount)+","+","+","+","+","+","+","+str(M)+","+str(BACKSCAL)+","+str(np.round(Background_Area,5))+","+str(np.round(P_B_Ideal,5))+","+str(int(Ideal_Type_II_Source_Detection_Bool))+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(np.round(Empirical_Background,5))+","+str(np.round(P_B_Empirical,5))+","+str(int(Empirical_Type_II_Source_Detection_Bool))
        ##Outfile_Str=str(int(Source_Detection_Bool))+","+str(Source_Detection_Amount)+","+","+","+","+","+","+","+str(M)+","+str(BACKSCAL)+","+str(np.round(Background_Area,5))+","+str(P_B_Ideal)+","+str(int(Ideal_Type_II_Source_Detection_Bool))+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(np.round(Empirical_Background,5))+","+str(P_B_Empirical)+","+str(int(Empirical_Type_II_Source_Detection_Bool))
        #Outfile_Str=str(int(Source_Detection_Bool))+","+str(Source_Detection_Amount)+","+","+","+","+","+str(M)+","+str(BACKSCAL)+","+str(np.round(Background_Area,5))+","+str(P_B_Ideal)+","+str(int(Ideal_Type_II_Source_Detection_Bool))+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(np.round(Empirical_Background,5))+","+str(P_B_Empirical)+","+str(int(Empirical_Type_II_Source_Detection_Bool))
        ##Outfile_Str=str(int(Source_Detection_Bool))+","+str(Source_Detection_Amount)+","+","+","+","+","+","+","+","+","+str(M)+","+str(BACKSCAL)+","+str(np.round(Background_Area,5))+","+str(P_B_Ideal)+","+str(int(Ideal_Type_II_Source_Detection_Bool))+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(np.round(Empirical_Background,5))+","+str(P_B_Empirical)+","+str(int(Empirical_Type_II_Source_Detection_Bool))
        Outfile_Str=str(int(Source_Detection_Bool))+","+str(Source_Detection_Amount)+","+","+","+","+","+","+","+","+","+","+","+","+","+str(M)+","+str(BACKSCAL)+","+str(np.round(Background_Area,5))+","+str(P_B_Ideal)+","+str(int(Ideal_Type_II_Source_Detection_Bool))+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(np.round(Empirical_Background,5))+","+str(P_B_Empirical)+","+str(int(Empirical_Type_II_Source_Detection_Bool))

    #Outfile_Header="SDB,SDA,SDBNB,SDANB,SDBNBF,SDANBF,SDBNS,SDANS,M,BACKSCAL,BA,PBI,T2I,EEC,EEBC,EB,PBE,T2E\n"
    #Outfile_Header="SDB,SDA,SDBNB,SDANB,SDBNS,SDANS,M,BACKSCAL,BA,PBI,T2I,EEC,EEBC,EB,PBE,T2E\n"
    #Outfile_Header="SDB,SDA,SDBNB,SDANB,SDBNBF,SDANBF,SDBNS,SDANS,SDBNSF,SDANSF,M,BACKSCAL,BA,PBI,T2I,EEC,EEBC,EB,PBE,T2E\n"
    Outfile_Header="SDB,SDA,SDBNB,SDANB,SDBNBF,SDANBF,SDBNS,SDANS,SDBNSF,SDANSF,NSC,NSA,NSCF,NSAF,M,BACKSCAL,BA,PBI,T2I,EEC,EEBC,EB,PBE,T2E\n"

    Outfile_Str_Merged=Outfile_Header+Outfile_Str
    Source_Detect.Save_Parameter(Outfile_Str_Merged, Outpath, Key="_Standard_Outputs", Suffix=".csv")


    ###Cleanup Files###

    Input_L=Input_HL[3]
    Phi=Input_L[0]
    Theta=Input_L[1]
    Counts=Input_L[2]
    Background=Input_L[3]
    Run_Count=Input_L[4]


    Cleanup_Files(Phi, Theta, Counts, Background, Run_Count)


    print("--- %s seconds ---" % (time.time() - start_time))

def Synthetic_Background_Generator_Driver():
    Input_L=Synthetic_Background_Generator.Synthetic_Background_Generator_Big_Input_Generator()
    Driver(Synthetic_Background_Generator.Synthetic_Background_Generator_Wrapper, Input_L)

def Empty_Coords_Generator_Main():
    Source_Generator.Empty_Coords_Generator()
    os.system("cp Empty_Coords/empty.fits ../Required_Files_Generated/")

def Main_Driver():
    Input_L=Main_Big_Input_Generator()
    Driver(Main_Wrapper, Input_L)

def Main():
    if __name__ == '__main__':
        Synthetic_Background_Generator_Driver()
        ###Empty_Coords_Generator_Main()
        start_time_Big = time.time()
        Main_Driver()
        print("--- %s seconds Big ---" % (time.time() - start_time_Big))

Main()
#Main_Big_Input_Generator()
#print(Main_Big_Input_Generator())
#print("sys.float_info.max: ", sys.float_info.max)
