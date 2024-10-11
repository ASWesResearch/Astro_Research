from sherpa.astro.ui import *
from matplotlib import pyplot as plt
import numpy as np
import os
from os import system
import sys
from ciao_contrib.runtool import *
from multiprocessing import Pool
import time

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

def Main_Big_Input_Generator(Max_Runs=1):
    #Source_Coords_HL=Source_Coords_Generator()
    ##Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]], [15, [1, 2, 3, 4, 5, 6, 7, 8]], [30, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [45, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [60, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [75, [1, 2, 3, 4, 5, 6, 7, 8]], [90, [1, 2, 3, 4, 5, 6, 7, 8]], [105, [2, 3, 4, 5, 6, 7, 8]], [120, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [135, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [150, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [165, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [180, [1, 2, 3, 4, 5, 6, 7, 8]], [195, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [210, [2, 3, 4, 5, 6, 7, 8, 9, 10]], [225, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [240, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [255, [2, 3, 4, 5, 6, 7, 8, 9]], [270, [1, 2, 3, 4, 5, 6, 7, 8]], [285, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [300, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [315, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [330, [2, 3, 4, 5, 6, 7, 8, 9]], [345, [1, 3, 4, 5, 6, 7, 8]]]
    #Source_Coords_HL=[[0, [1, 2]]]
    Source_Coords_HL=[[0, [1]]]
    Max_Runs=Max_Runs+1
    Run_Count_L=list(np.arange(1,Max_Runs))
    #print("Run_Count_L: ", Run_Count_L)
    Background_Str_L=Source_Generator.Background_Str_List_Genertator()
    #Background_Str_L=[Background_Str_L[25]] #For Testing
    #Background_Str_L=[Background_Str_L[-1]] #For Testing
    #Background_Str_L=[Background_Str_L[0]] #For Testing
    Background_Str_L=[Background_Str_L[0],Background_Str_L[1]] #For Testing
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
            #Cur_Counts_L=Counts_List_Genertator(Max_Counts_Calc_Broken,Cur_Theta)
            #Cur_Counts_L=[Cur_Counts_L[3]] #For Testing
            #Cur_Counts_L=[Cur_Counts_L[-1]] #For Testing
            #Cur_Counts_L=[Cur_Counts_L[2]] #For Testing
            #Cur_Counts_L=[Cur_Counts_L[0]] #For Testing
            Cur_Counts_L=[Cur_Counts_L[0], Cur_Counts_L[1]] #For Testing
            #print("Cur_Counts_L: ", Cur_Counts_L)
            Cur_RA,Cur_Dec=Source_Generator.MSC_to_CEL_Convert(Cur_Theta,Cur_Phi)
            for Cur_Counts in Cur_Counts_L:
                #Number_of_Sources=Number_of_Sources+1
                for Cur_Background in Background_Str_L:
                    Cur_Background_Float=float(Cur_Background)
                    if((float(Cur_Background_Float)==0.0) and (int(Cur_Counts)==0)):
                        continue
                        #pass
                    Number_of_Sources=Number_of_Sources+1
                    for Run_Count in Run_Count_L:
                        Cur_Run_HL=[]

                        ###Source_Generator Inputs###

                        Number_of_Runs=Number_of_Runs+1
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
                        Cur_Reproject_Parameter_Path=Cur_Outpath_Source_Reproject+"_reproject_events.par"
                        Cur_Dmmerge_Parameter_Path=Cur_Outpath_Source_Reproject+"_dmmerge.par"
                        Cur_Dmcopy_Parameter_Path=Cur_Outpath_Source_Reproject+"_dmcopy.par"
                        #Cur_Run_L=[Cur_RA, Cur_Dec, Cur_Outpath_Source_Reproject, Cur_Source_Path, Cur_Synthetic_Background_Path, Cur_Reproject_Outpath, Cur_Injected_Outpath, Cur_Postage_Stamp_Outpath, Cur_Postage_Stamp_Coords, Cur_Reproject_Parameter_Path, Cur_Dmmerge_Parameter_Path, Cur_Dmcopy_Parameter_Path]
                        #Run_Input_L.append(Cur_Run_L)
                        Cur_Source_Reproject_Run_L=[Cur_RA, Cur_Dec, Cur_Outpath_Source_Reproject, Cur_Source_Path, Cur_Synthetic_Background_Path, Cur_Reproject_Outpath, Cur_Injected_Outpath, Cur_Postage_Stamp_Outpath, Cur_Postage_Stamp_Coords, Cur_Reproject_Parameter_Path, Cur_Dmmerge_Parameter_Path, Cur_Dmcopy_Parameter_Path, Cur_Background_Float, Cur_Counts]
                        Cur_Run_HL.append(Cur_Source_Reproject_Run_L)

                        ###Source_Detect Inputs###

                        Run_Index=int(Run_Count-1)
                        Cur_Outpath_Source_Detect="./Wavdetect_Outputs/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)
                        Cur_Postage_Stamp_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Postage_Stamp.fits"
                        Cur_PSF_Outpath=Cur_Outpath_Source_Detect+"_PSF.fits"
                        Cur_Postage_Stamp_Coords=Postage_Stamp_Coords_L[Run_Index]
                        Cur_Wavdetect_Outfile=Cur_Outpath_Source_Detect+"_Wavdetect.fits"
                        ##Cur_Source_Detect_Run_L=[Cur_Outpath_Source_Detect, Cur_Postage_Stamp_Outpath, Cur_PSF_Outpath, Cur_Wavdetect_Outfile, Cur_Postage_Stamp_Coords]
                        Cur_Source_Detect_Run_L=[Cur_Outpath_Source_Detect, Cur_Postage_Stamp_Outpath, Cur_PSF_Outpath, Cur_Wavdetect_Outfile, Cur_Postage_Stamp_Coords, Cur_Background_Float, Cur_Counts]
                        #Run_Input_L.append(Cur_Run_L)
                        Cur_Run_HL.append(Cur_Source_Detect_Run_L)

                        Run_Input_L.append(Cur_Run_HL)
    #print("Number_of_Sources: ", Number_of_Sources)
    print("Number_of_Runs: ", Number_of_Runs)
    return Run_Input_L

def Driver(Func, Array):
    if __name__ == '__main__':
        P = Pool()
        P.map(Func, Array)

def Main_Wrapper(Input_HL):
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
        #Source_Reproject.Source_Injection(Reproject_Outpath, Synthetic_Background_Path, Injected_Outpath, Dmmerge_Parameter_Path, Background_Float)
        Source_Reproject.Crop_Image_Centered(X, Y, Reproject_Outpath, Postage_Stamp_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
    else:
        Source_Reproject.Source_Injection(Reproject_Outpath, Synthetic_Background_Path, Injected_Outpath, Dmmerge_Parameter_Path, Background_Float, Counts)
        Source_Reproject.Crop_Image_Centered(X, Y, Injected_Outpath, Postage_Stamp_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)

    ###Source_Detect###

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
    Synthetic_Background_Generator_Driver()
    Empty_Coords_Generator_Main()
    Main_Driver()

Main()
#Main_Big_Input_Generator()
#print(Main_Big_Input_Generator())
