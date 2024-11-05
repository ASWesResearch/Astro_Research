import numpy as np
import os
from os import system
import sys
import glob
import re
from ciao_contrib.runtool import * #Imports ciao tools into python
import ciao_contrib.runtool as rt
import time
import logging
from multiprocessing import Pool
from astropy.io import fits

dir = os.path.dirname(__file__)
path=os.path.realpath('../')
sys.path.append(os.path.abspath(path))
#from Background_Generator import Background_Generator
from Source_Generator import Source_Generator

####Constants####
Postage_Stamp_Coords_L=[[[0, 0], [80.0, 80.0], [4145.0, 4135.0], ['359.9933716666962', '0.005261666616669011']], [[0, 1], [80.0, 224.0], [4145.0, 4279.0], ['359.9933716666962', '0.02494166492429339']], [[0, 2], [80.0, 368.0], [4145.0, 4423.0], ['359.9933716666962', '0.04462165734674123']], [[0, 3], [80.0, 512.0], [4145.0, 4567.0], ['359.9933716666962', '0.06430163924036164']], [[0, 4], [80.0, 656.0], [4145.0, 4711.0], ['359.9933716666962', '0.08398160596151538']], [[0, 5], [80.0, 800.0], [4145.0, 4855.0], ['359.9933716666962', '0.1036615528666012']], [[0, 6], [80.0, 944.0], [4145.0, 4999.0], ['359.9933716666962', '0.1233414753120392']], [[1, 0], [224.0, 80.0], [4289.0, 4135.0], ['359.9736916685156', '0.0052616660972041']], [[1, 1], [224.0, 224.0], [4289.0, 4279.0], ['359.9736916685156', '0.02494166246190883']], [[1, 2], [224.0, 368.0], [4289.0, 4423.0], ['359.9736916685156', '0.04462165294143504']], [[1, 3], [224.0, 512.0], [4289.0, 4567.0], ['359.9736916685156', '0.06430163289215492']], [[1, 4], [224.0, 656.0], [4289.0, 4711.0], ['359.9736916685156', '0.08398159767039177']], [[1, 5], [224.0, 800.0], [4289.0, 4855.0], ['359.9736916685156', '0.1036615426325772']], [[1, 6], [224.0, 944.0], [4289.0, 4999.0], ['359.9736916685156', '0.1233414631351299']], [[2, 0], [368.0, 80.0], [4433.0, 4135.0], ['359.9540116765426', '0.00526166495697853']], [[2, 1], [368.0, 224.0], [4433.0, 4279.0], ['359.9540116765426', '0.02494165705694917']], [[2, 2], [368.0, 368.0], [4433.0, 4423.0], ['359.9540116765426', '0.04462164327174108']], [[2, 3], [368.0, 512.0], [4433.0, 4567.0], ['359.9540116765426', '0.06430161895770789']], [[2, 4], [368.0, 656.0], [4433.0, 4711.0], ['359.9540116765426', '0.08398157947124001']], [[2, 5], [368.0, 800.0], [4433.0, 4855.0], ['359.9540116765426', '0.1036615201687066']], [[2, 6], [368.0, 944.0], [4433.0, 4999.0], ['359.9540116765426', '0.123341436406556']], [[3, 0], [512.0, 80.0], [4577.0, 4135.0], ['359.9343316954208', '0.00526166319598787']], [[3, 1], [512.0, 224.0], [4577.0, 4279.0], ['359.9343316954208', '0.02494164870939743']], [[3, 2], [512.0, 368.0], [4577.0, 4423.0], ['359.9343316954208', '0.04462162833762061']], [[3, 3], [512.0, 512.0], [4577.0, 4567.0], ['359.9343316954208', '0.06430159743705187']], [[3, 4], [512.0, 656.0], [4577.0, 4711.0], ['359.9343316954208', '0.08398155136404363']], [[3, 5], [512.0, 800.0], [4577.0, 4855.0], ['359.9343316954208', '0.1036614854750053']], [[3, 6], [512.0, 944.0], [4577.0, 4999.0], ['359.9343316954208', '0.1233413951263738']], [[4, 0], [656.0, 80.0], [4721.0, 4135.0], ['359.9146517297941', '0.005261660814234067']], [[4, 1], [656.0, 224.0], [4721.0, 4279.0], ['359.9146517297941', '0.02494163741926511']], [[4, 2], [656.0, 368.0], [4721.0, 4423.0], ['359.9146517297941', '0.04462160813912187']], [[4, 3], [656.0, 512.0], [4721.0, 4567.0], ['359.9146517297941', '0.06430156833020197']], [[4, 4], [656.0, 656.0], [4721.0, 4711.0], ['359.9146517297941', '0.08398151334885186']], [[4, 5], [656.0, 800.0], [4721.0, 4855.0], ['359.9146517297941', '0.1036614385515127']], [[4, 6], [656.0, 944.0], [4721.0, 4999.0], ['359.9146517297941', '0.1233413392946094']], [[5, 0], [800.0, 80.0], [4865.0, 4135.0], ['359.8949717843058', '0.005261657811719962']], [[5, 1], [800.0, 224.0], [4865.0, 4279.0], ['359.8949717843059', '0.02494162318656983']], [[5, 2], [800.0, 368.0], [4865.0, 4423.0], ['359.8949717843059', '0.04462158267626447']], [[5, 3], [800.0, 512.0], [4865.0, 4567.0], ['359.8949717843059', '0.06430153163718179']], [[5, 4], [800.0, 656.0], [4865.0, 4711.0], ['359.8949717843059', '0.08398146542570789']], [[5, 5], [800.0, 800.0], [4865.0, 4855.0], ['359.8949717843058', '0.1036613793982855']], [[5, 6], [800.0, 944.0], [4865.0, 4999.0], ['359.8949717843059', '0.1233412689113129']], [[6, 0], [944.0, 80.0], [5009.0, 4135.0], ['359.8752918635997', '0.005261654188448438']], [[6, 1], [944.0, 224.0], [5009.0, 4279.0], ['359.8752918635997', '0.02494160601132736']], [[6, 2], [944.0, 368.0], [5009.0, 4423.0], ['359.8752918635997', '0.04462155194906044']], [[6, 3], [944.0, 512.0], [5009.0, 4567.0], ['359.8752918635997', '0.06430148735803921']], [[6, 4], [944.0, 656.0], [5009.0, 4711.0], ['359.8752918635997', '0.08398140759466759']], [[6, 5], [944.0, 800.0], [5009.0, 4855.0], ['359.8752918635997', '0.1036613080153593']], [[6, 6], [944.0, 944.0], [5009.0, 4999.0], ['359.8752918635997', '0.1233411839765937']]]
#################


def Angle_Convert(Angle):
    Angle=Angle%360
    return Angle

def Make_Directory(Outpath):
    path=os.path.realpath(Outpath)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def Postage_Stamp_Coords_Calc(n=3, N=49, d=1024.0, X_P_Start=4065.0, Y_P_Start=4055.0, Empty_Filepath="../Required_Files_Generated/empty.fits"):
    n_s=int(np.sqrt(N))
    S=d/(2.0**n)
    W=d/(2.0**(n+1))
    g=(d-S*n_s)/(1.0+n_s)
    print("gap: ", g)
    Coords_L=[]
    for j in range(0,n_s):
        #print(j)
        X=W+(g*(j+1))+(S*j)
        X_P=X+X_P_Start
        for k in range(0,n_s):
            Y=W+(g*(k+1))+(S*k)
            Y_P=Y+Y_P_Start
            Cur_Index_L=[j,k]
            Cur_Positon=[X,Y]
            Cur_Physical_Postion=[X_P,Y_P]
            with rt.new_pfiles_environment(ardlib=True):
                Dmcoords=rt.make_tool("dmcoords")
                Dmcoords(infile=str(Empty_Filepath), x=float(X_P), y=float(Y_P), option='sky', verbose=0, celfmt='deg')
                RA=Dmcoords.ra
                Dec=Dmcoords.dec
            Cur_Cel_Positon=[RA,Dec]
            Cur_Coords=[Cur_Index_L, Cur_Positon, Cur_Physical_Postion, Cur_Cel_Positon]
            Coords_L.append(Cur_Coords)
    return Coords_L, S, g

def MSC_to_Physical_Convert(Theta,Phi,Empty_Filepath="../Required_Files_Generated/empty.fits", Empty_Coords_Gen_Bool=False):
    if(Empty_Coords_Gen_Bool):
        Empty_Coords_Generator()
    with rt.new_pfiles_environment(ardlib=True):
        Dmcoords=rt.make_tool("dmcoords")
        Dmcoords(infile=str(Empty_Filepath), theta=float(Theta), phi=float(Phi), option='msc', verbose=0, celfmt='deg')
        X=Dmcoords.x
        Y=Dmcoords.y
    return X, Y

def Source_Reproject(Source_Path, Source_RA, Source_Dec, Target_RA, Target_Dec, Outpath, Reproject_Parameter_Path, Counts=None):
    if(Counts==0):
        print("Source_Reproject 0 Counts Test")
        return
    #print("Source_RA: ", Source_RA)
    #print("type(Source_RA): ", type(Source_RA))
    #print("Target_RA: ", Target_RA)
    #print("type(Target_RA): ", type(Target_RA))
    Transformed_RA=Source_RA-Target_RA
    Transformed_Dec=Source_Dec-Target_Dec
    Transformed_RA=Angle_Convert(Transformed_RA)
    #os.system("cp /Users/asantini/cxcds_param4/reproject_events.par "+Reproject_Parameter_Path)
    os.system("cp ../Parameter_Files/cxcds_param4/reproject_events.par "+Reproject_Parameter_Path)
    Command='reproject_events @@'+str(Reproject_Parameter_Path)+' infile='+str(Source_Path)+' outfile='+str(Outpath)+' aspect=none match="'+str(Transformed_RA)+' '+str(Transformed_Dec)+'" random=-1 verbose=0 clobber=yes'
    os.system(Command)

def Source_Injection(Source_Path, Background_Path, Outpath, Dmmerge_Parameter_Path, Background_Float=None, Counts=None):
    if((float(Background_Float)==0.0) and (int(Counts)==0)):
        print("Source_Injection 0 Counts and Background Test")
        return
    if(Background_Float==0.0):
        Command='cp '+str(Source_Path)+" "+str(Outpath)
        os.system(Command)
        return
    if(Counts==0):
        Command='cp '+str(Background_Path)+" "+str(Outpath)
        os.system(Command)
        return
    #dmmerge "Source.fits,Source_New_11.fits" merged.fits
    #os.system("cp /Users/asantini/cxcds_param4/dmmerge.par "+Dmmerge_Parameter_Path)
    os.system("cp ../Parameter_Files/cxcds_param4/dmmerge.par "+Dmmerge_Parameter_Path)
    #Command='dmmerge "'+str(Source_Path)+'[EVENTS][columns sky],'+str(Background_Path)+'[EVENTS][columns sky]" '+str(Outpath)+' lookupTab=dmmerge_header_lookup_Modified.txt clobber=yes verbose=0'
    Command='dmmerge @@'+str(Dmmerge_Parameter_Path)+' "'+str(Source_Path)+'[EVENTS][columns sky],'+str(Background_Path)+'[EVENTS][columns sky]" '+str(Outpath)+' lookupTab=../Required_Files/dmmerge_header_lookup_Modified.txt clobber=yes verbose=0'
    #Command='dmmerge @@'+str(Dmmerge_Parameter_Path)+' "'+str(Source_Path)+','+str(Background_Path)+'" '+str(Outpath)+' lookupTab=../Required_Files/dmmerge_header_lookup_Modified.txt clobber=yes verbose=0'
    """
    File # 1 : column 0 is TIME
    File # 1 : column 1 is CCD_ID
    File # 1 : column 2 is NODE_ID
    File # 1 : column 3 is EXPNO
    File # 1 : column 4 is chip
    File # 1 : column 5 is tdet
    File # 1 : column 6 is det
    File # 1 : column 7 is sky
    File # 1 : column 8 is PHA
    File # 1 : column 9 is ENERGY
    File # 1 : column 10 is PI
    File # 1 : column 11 is FLTGRADE
    File # 1 : column 12 is GRADE
    File # 1 : column 13 is STATUS
    File # 1 : column 14 is SHELL
    File # 1 : column 15 is ZCOS
    File # 1 : column 16 is YCOS
    File # 1 : column 17 is XCOS
    File # 1 : column 18 is ZPOS
    File # 1 : column 19 is YPOS
    File # 1 : column 20 is XPOS
    File # 1 : column 21 is MARX_ENERGY
    """
    os.system(Command)

def Swap_Header(Dmmerge_Parameter_Path, Background_Path):
    Background_Data, Background_Header = fits.getdata(Background_Path, header=True)
    Injected_Data, Injected_Header = fits.getdata(Dmmerge_Parameter_Path, header=True)
    fits.writeto(Dmmerge_Parameter_Path, Injected_Data, Background_Header, overwrite=True)

def Crop_Image(X_Low, X_High, Y_Low, Y_High, Evt2_Fpath, Outfile, Dmcopy_Parameter_Path):
    ##Command='dmcopy "'+str(Evt2_Fpath)+'[EVENTS][bin x='+str(X_Low)+':'+str(X_High)+':1,y='+str(Y_Low)+':'+str(Y_High)+':1]" '+str(Outfile)+' clobber=yes'
    #print("Dmcopy_Parameter_Path: ", Dmcopy_Parameter_Path)
    #os.system("cp /Users/asantini/cxcds_param4/dmcopy.par "+Dmcopy_Parameter_Path)
    os.system("cp ../Parameter_Files/cxcds_param4/dmcopy.par "+Dmcopy_Parameter_Path)
    Command='dmcopy @@'+str(Dmcopy_Parameter_Path)+' "'+str(Evt2_Fpath)+'[EVENTS][bin x='+str(X_Low)+':'+str(X_High)+':1,y='+str(Y_Low)+':'+str(Y_High)+':1]" '+str(Outfile)+' clobber=yes'
    #print("Command: ", Command)
    os.system(Command)

def Crop_Image_Centered(X, Y, Evt2_Fpath, Outfile, Dmcopy_Parameter_Path, Background_Float=None, Counts=None, X_Length=128.0, Y_Length=128.0):
    if((Background_Float==0.0) and (Counts==0)):
        print("Crop_Image_Centered 0 Counts and Background Test")
        return
    X_Low=X-(X_Length/2.0)
    X_High=X+(X_Length/2.0)
    Y_Low=Y-(Y_Length/2.0)
    Y_High=Y+(Y_Length/2.0)
    Crop_Image(X_Low, X_High, Y_Low, Y_High, Evt2_Fpath=Evt2_Fpath, Outfile=Outfile, Dmcopy_Parameter_Path=Dmcopy_Parameter_Path)


def Source_Reproject_Big_Input_Generator(Max_Runs=1):
    #Source_Coords_HL=Source_Coords_Generator()
    ##Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]], [15, [1, 2, 3, 4, 5, 6, 7, 8]], [30, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [45, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [60, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [75, [1, 2, 3, 4, 5, 6, 7, 8]], [90, [1, 2, 3, 4, 5, 6, 7, 8]], [105, [2, 3, 4, 5, 6, 7, 8]], [120, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [135, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [150, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [165, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [180, [1, 2, 3, 4, 5, 6, 7, 8]], [195, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [210, [2, 3, 4, 5, 6, 7, 8, 9, 10]], [225, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [240, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [255, [2, 3, 4, 5, 6, 7, 8, 9]], [270, [1, 2, 3, 4, 5, 6, 7, 8]], [285, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [300, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [315, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [330, [2, 3, 4, 5, 6, 7, 8, 9]], [345, [1, 3, 4, 5, 6, 7, 8]]]
    #Source_Coords_HL=[[0, [1, 2]]]
    Source_Coords_HL=[[0, [1]]]
    Max_Runs=Max_Runs+1
    #Counts_L=np.arange(C_Min,C_Max,step=Count_Step)
    #print("Counts_L: ", Counts_L)
    Run_Count_L=list(np.arange(1,Max_Runs))
    #print("Run_Count_L: ", Run_Count_L)
    Background_Str_L=Source_Generator.Background_Str_List_Genertator()
    Background_Str_L=[Background_Str_L[25]] #For Testing
    #Background_Str_L=[Background_Str_L[0]] #For Testing
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
            Cur_Counts_L=[Cur_Counts_L[3]] #For Testing
            #Cur_Counts_L=[Cur_Counts_L[0]] #For Testing
            #print("Cur_Counts_L: ", Cur_Counts_L)
            Cur_RA,Cur_Dec=Source_Generator.MSC_to_CEL_Convert(Cur_Theta,Cur_Phi)
            Cur_X,Cur_Y=MSC_to_Physical_Convert(Cur_Theta,Cur_Phi)
            #Need to convert source RA and Dec to Physical Coordinates
            for Cur_Counts in Cur_Counts_L:
                #Number_of_Sources=Number_of_Sources+1
                for Cur_Background in Background_Str_L:
                    Number_of_Sources=Number_of_Sources+1
                    Cur_Background_Float=float(Cur_Background)
                    for Run_Count in Run_Count_L:
                        Run_Index=int(Run_Count-1)
                        Number_of_Runs=Number_of_Runs+1
                        Cur_Outpath="./Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)
                        ##print("Cur_Outpath: ", Cur_Outpath)
                        Cur_Source_Path="../Source_Generator/Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+".fits"
                        #../Synthetic_Background_Generator/Synthetic_Backgrounds/0/1/78/8E-2/0_1_78_8E-2_bkg.fits
                        Cur_Synthetic_Background_Path="../Synthetic_Background_Generator/Synthetic_Backgrounds/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_bkg.fits"
                        Cur_Reproject_Outpath=Cur_Outpath+"_Reprojected.fits"
                        Cur_Postage_Stamp_Coords=Postage_Stamp_Coords_L[Run_Index]
                        Cur_Injected_Outpath=Cur_Outpath+"_Injected.fits"
                        Cur_Postage_Stamp_Outpath=Cur_Outpath+"_Postage_Stamp.fits"
                        Cur_Postage_Stamp_No_Background_Outpath=Cur_Outpath+"_No_Background_Postage_Stamp.fits"
                        Cur_Postage_Stamp_No_Source_Outpath=Cur_Outpath+"_No_Source_Postage_Stamp.fits"
                        Cur_Postage_Stamp_Original_Source_Outpath=Cur_Outpath+"_Original_Source_Postage_Stamp.fits"
                        #Cur_Run_L=[Cur_Phi, Cur_Theta, Cur_RA, Cur_Dec, Cur_Counts, Cur_Background, Run_Count, Cur_Outpath, Cur_Parameter_Outpath, Cur_Aspect_Parameter_Outpath, Cur_Postage_Stamp_Coords, Cur_Seed, Cur_Seed_Biased]
                        Cur_Reproject_Parameter_Path=Cur_Outpath+"_reproject_events.par"
                        Cur_Dmmerge_Parameter_Path=Cur_Outpath+"_dmmerge.par"
                        Cur_Dmcopy_Parameter_Path=Cur_Outpath+"_dmcopy.par"
                        ##Cur_Run_L=[Cur_RA, Cur_Dec, Cur_Outpath, Cur_Source_Path, Cur_Synthetic_Background_Path, Cur_Reproject_Outpath, Cur_Injected_Outpath, Cur_Postage_Stamp_Outpath, Cur_Postage_Stamp_Coords, Cur_Reproject_Parameter_Path, Cur_Dmmerge_Parameter_Path, Cur_Dmcopy_Parameter_Path, Cur_Background_Float, Cur_Counts]
                        Cur_Run_L=[Cur_RA, Cur_Dec, Cur_Outpath, Cur_Source_Path, Cur_Synthetic_Background_Path, Cur_Reproject_Outpath, Cur_Injected_Outpath, Cur_Postage_Stamp_Outpath, Cur_Postage_Stamp_Coords, Cur_Reproject_Parameter_Path, Cur_Dmmerge_Parameter_Path, Cur_Dmcopy_Parameter_Path, Cur_Background_Float, Cur_Counts, Cur_Postage_Stamp_No_Background_Outpath, Cur_Postage_Stamp_No_Source_Outpath, Cur_X, Cur_Y, Cur_Postage_Stamp_Original_Source_Outpath]
                        Run_Input_L.append(Cur_Run_L)
    #print("Number_of_Sources: ", Number_of_Sources)
    print("Number_of_Runs: ", Number_of_Runs)
    return Run_Input_L

def Source_Reproject_Generator_Wrapper(Input_L):
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
    Crop_Image_Centered(X_Original_Source, Y_Original_Source, Source_Path, Postage_Stamp_Original_Source_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
    if(Counts==0):
        Crop_Image_Centered(X, Y, Synthetic_Background_Path, Postage_Stamp_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
    if(Counts>0):
        Source_Reproject(Source_Path, Source_RA, Source_Dec, Target_RA, Target_Dec, Reproject_Outpath, Reproject_Parameter_Path, Counts)
    if(Background_Float==0.0):
        Crop_Image_Centered(X, Y, Reproject_Outpath, Postage_Stamp_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
    else:
        Source_Injection(Reproject_Outpath, Synthetic_Background_Path, Injected_Outpath, Dmmerge_Parameter_Path, Background_Float, Counts)
        #Swap_Header(Injected_Outpath, Synthetic_Background_Path)
        Crop_Image_Centered(X, Y, Injected_Outpath, Postage_Stamp_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
        #Swap_Header(Postage_Stamp_Outpath, Synthetic_Background_Path)
        ####No Background####
        Crop_Image_Centered(X, Y, Reproject_Outpath, Postage_Stamp_No_Background_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)
        ####No Source####
        Crop_Image_Centered(X, Y, Synthetic_Background_Path, Postage_Stamp_No_Source_Outpath, Dmcopy_Parameter_Path, Background_Float, Counts)


def Driver(Func, Array):
    if __name__ == '__main__':
        P = Pool()
        P.map(Func, Array)

def Source_Reproject_Generator_Driver():
    Input_L=Source_Reproject_Big_Input_Generator()
    Driver(Source_Reproject_Generator_Wrapper, Input_L)

#print(Postage_Stamp_Coords_Calc())
#print(Postage_Stamp_Coords_L[0])
#print(Source_Reproject_Big_Input_Generator())
##Source_Reproject_Generator_Driver()
#print(MSC_to_Physical_Convert(0,1))
