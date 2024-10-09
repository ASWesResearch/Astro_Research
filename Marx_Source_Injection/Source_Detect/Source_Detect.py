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
from astropy.io import fits
from multiprocessing import Pool

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
    
'''
def Fluximage(Filepath, Outpath):
    """
    with rt.new_pfiles_environment(ardlib=True):
        with new_tmpdir() as tmpdir:
    """
    #os.system("fluximage "+str(Filepath)+" "+str(Outpath)+" psfecf=0.9 binsize=1 clobber=yes verbose=1")
    os.system("fluximage "+str(Filepath)+" "+str(Outpath)+" psfecf=0.9 binsize=1 asolfile='0_1_78_8E-2_1_asol1.fits' badpixfile='NONE' maskfile='NONE' clobber=yes verbose=0")
'''

def Make_PSF_Map(Filepath, PSF_Outpath, Outpath):
    ##os.system("mkpsfmap "+str(Filepath)+" "+str(Outpath)+" 1.4 ecf=0.9 clobber=yes")
    Bash_Command="bash Bash_Scripts/Make_PSF_Map.sh "+str(Filepath)+" "+str(PSF_Outpath)+" "+Outpath
    #print(Bash_Command)
    os.system(Bash_Command)

def Wavdetect(Filepath, Outpath, PSF_Map_Path):
    ##Wavdetect_Command="wavdetect "+str(Filepath)+" outfile="+str(Outpath)+" scellfile=source_cell.fits imagefile=image.fits defnbkgfile=background.fits regfile="+str(Regfile)+" scales='1 2 4 8' psffile="+str(PSF_Map_Path)+" clobber=yes verbose=1"
    Outfile=Outpath+"_Wavdetect.fits"
    Scellfile=Outpath+"_source_cell.fits"
    Imagefile=Outpath+"_image.fits"
    Defnbkgfile=Outpath+"_background.fits"
    Bash_Command="bash Bash_Scripts/Wavdetect.sh "+str(Filepath)+" "+str(Outfile)+" "+str(Outpath)+" "+str(PSF_Map_Path)
    #print(Bash_Command)
    os.system(Bash_Command)

def Source_Detection_Bool_Calc(Filepath, X_Expected, Y_Expected, Tolarance=17):
    hdul = fits.open(Filepath)
    Data=hdul[1].data
    hdul.close()
    X=list(Data["X"])
    Y=list(Data["Y"])
    #print("(X,Y): ", (X,Y))
    if(len(X)<1):
        ##return False
        return (False,0)
    for i in range(0,len(X)):
        Cur_Test_X=X[i]
        Cur_Test_Y=Y[i]
        #print(Cur_Test_X,Cur_Test_Y)
        X_Diff=np.abs(X_Expected-Cur_Test_X)
        Y_Diff=np.abs(Y_Expected-Cur_Test_Y)
        #print("(X_Diff,Y_Diff): ", (X_Diff,Y_Diff))
        if((X_Diff<=Tolarance) and (Y_Diff<=Tolarance)):
            ##return True
            return (True,len(X))
    ##return False
    return (False,len(X))

def Save_Detection_Bool(Filepath, X_Expected, Y_Expected, Outpath, Tolarance=17):
    Outfile=Outpath+"_Detection_Bool.txt"
    Outfile_Amount=Outpath+"_Detection_Amount.txt"
    Source_Detection_Bool=Source_Detection_Bool_Calc(Filepath, X_Expected, Y_Expected, Tolarance=Tolarance)[0]
    Source_Detection_Amount=Source_Detection_Bool_Calc(Filepath, X_Expected, Y_Expected, Tolarance=Tolarance)[1]
    Command='echo "'+str(int(Source_Detection_Bool))+'" > '+str(Outfile)
    #print(Command)
    os.system(Command)
    Command_Amount='echo "'+str(int(Source_Detection_Amount))+'" > '+str(Outfile_Amount)
    #print(Command_Amount)
    os.system(Command_Amount)

def Source_Detect_Big_Input_Generator(Max_Runs=1):
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
            #print("Cur_Counts_L: ", Cur_Counts_L)
            Cur_RA,Cur_Dec=Source_Generator.MSC_to_CEL_Convert(Cur_Theta,Cur_Phi)
            for Cur_Counts in Cur_Counts_L:
                #Number_of_Sources=Number_of_Sources+1
                for Cur_Background in Background_Str_L:
                    Number_of_Sources=Number_of_Sources+1
                    for Run_Count in Run_Count_L:
                        Run_Index=int(Run_Count-1)
                        Number_of_Runs=Number_of_Runs+1
                        Cur_Outpath="./Wavdetect_Outputs/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)
                        Cur_Postage_Stamp_Outpath="../Source_Reproject/Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Postage_Stamp.fits"
                        Cur_PSF_Outpath=Cur_Outpath+"_PSF.fits"
                        Cur_Postage_Stamp_Coords=Postage_Stamp_Coords_L[Run_Index]
                        Cur_Wavdetect_Outfile=Cur_Outpath+"_Wavdetect.fits"
                        Cur_Run_L=[Cur_Outpath, Cur_Postage_Stamp_Outpath, Cur_PSF_Outpath, Cur_Wavdetect_Outfile, Cur_Postage_Stamp_Coords]
                        Run_Input_L.append(Cur_Run_L)
    #print("Number_of_Sources: ", Number_of_Sources)
    print("Number_of_Runs: ", Number_of_Runs)
    return Run_Input_L

def Source_Detect_Generator_Wrapper(Input_L):
    Outpath=Input_L[0]
    Postage_Stamp_Outpath=Input_L[1]
    PSF_Outpath=Input_L[2]
    Wavdetect_Outfile=Input_L[3]
    Postage_Stamp_Coords=Input_L[4]
    #Postage_Stamp_Coords[0]=[[0, 0], [80.0, 80.0], [4145.0, 4135.0], ['359.9933716666962', '0.005261666616669011']]
    Target_Physical_Coords=Postage_Stamp_Coords[2]
    Target_X=Target_Physical_Coords[0]
    Target_Y=Target_Physical_Coords[1]
    Make_Directory(Outpath)
    Make_PSF_Map(Postage_Stamp_Outpath, PSF_Outpath, Outpath)
    Wavdetect(Postage_Stamp_Outpath, Outpath, PSF_Outpath)
    #Source_Detection_Bool_Calc(Wavdetect_Outfile, Target_RA, Target_Dec)
    Save_Detection_Bool(Wavdetect_Outfile, Target_X, Target_Y, Outpath)

def Driver(Func, Array):
    if __name__ == '__main__':
        P = Pool()
        P.map(Func, Array)

def Source_Detect_Generator_Driver():
    Input_L=Source_Detect_Big_Input_Generator()
    Driver(Source_Detect_Generator_Wrapper, Input_L)





#"../Synthetic_Background_Generator/Synthetic_Backgrounds/0/1/78/8E-2/1/0_1_78_8E-2_1_bkg_source_with_bkg.fits"

##Fluximage("Test.fits", "Test_Outpath")
#Fluximage("Cropped.fits", "Cropped_Outpath")
#Make_PSF_Map("Test.fits", "Test_PSF.fits")
#Wavdetect("Test.fits", "Test_Outpath")
#Wavdetect("Cropped.fits", "Cropped_Outpath")
##Make_PSF_Map("Cropped.fits", "Cropped_PSF.fits")
##Crop_Image("Test2.fits","Cropped_2.fits")
##Make_PSF_Map("Cropped_2.fits", "Cropped_2_PSF.fits")
##Wavdetect("Cropped_2.fits", "./Outputs/Cropped_Wavdetect_Outfile.fits", "Cropped_2_PSF.fits", "./Outputs/Cropped.reg")
#Crop_Image("Test.fits","Cropped.fits")
#Make_PSF_Map("Cropped.fits", "Cropped_PSF.fits")
#Wavdetect("Cropped.fits", "./Outputs/Cropped_Wavdetect_Outfile.fits", "Cropped_PSF.fits", "./Outputs/Cropped.reg")
#Crop_Image_Centered(X=4218.666, X_Length=128.0, Y=4096.1666, Y_Length=128.0, Evt2_Fpath="Test.fits", Outfile="Cropped_Centered_Test.fits")
#Make_PSF_Map("Cropped_Centered_Test.fits", "Cropped_Centered_Test_PSF.fits")
#Wavdetect("Cropped_Centered_Test.fits", "./Outputs/Cropped_Centered_Test_Wavdetect_Outfile.fits", "Cropped_Centered_Test_PSF.fits", "./Outputs/Cropped_Centered_Test.reg")
##Crop_Image_Centered(X=4218.666, X_Length=256.0, Y=4096.1666, Y_Length=256.0, Evt2_Fpath="Test.fits", Outfile="Cropped_Centered_Test_256.fits")
##Make_PSF_Map("Cropped_Centered_Test_256.fits", "Cropped_Centered_Test_PSF_256.fits")
##Wavdetect("Cropped_Centered_Test_256.fits", "./Outputs/Cropped_Centered_Test_256_Wavdetect_Outfile.fits", "Cropped_Centered_Test_PSF_256.fits", "./Outputs/Cropped_Centered_Test_256.reg")
#Crop_Image_Centered(X=4218.666, X_Length=64.0, Y=4096.1666, Y_Length=64.0, Evt2_Fpath="Test.fits", Outfile="Cropped_Centered_Test_64.fits")
#Make_PSF_Map("Cropped_Centered_Test_64.fits", "Cropped_Centered_Test_PSF_64.fits")
#Wavdetect("Cropped_Centered_Test_64.fits", "./Outputs/Cropped_Centered_Test_64_Wavdetect_Outfile.fits", "Cropped_Centered_Test_PSF_64.fits", "./Outputs/Cropped_Centered_Test_64.reg")
#print(Postage_Stamp_Coords_Calc())
#Make_PSF_Map("0_1_78_8E-2_1_Postage_Stamp.fits", "0_1_78_8E-2_1_Postage_Stamp_PSF.fits")
#Wavdetect("0_1_78_8E-2_1_Postage_Stamp.fits", "./Outputs/0_1_78_8E-2_1_Postage_Stamp_Wavdetect_Outfile.fits", "0_1_78_8E-2_1_Postage_Stamp_PSF.fits")
#print(Source_Detection_Bool_Calc("./Test_Runs/Outputs/0_1_78_8E-2_1_Postage_Stamp_Wavdetect_Outfile.fits", 359.9833379, 0.0000078))
#print(Source_Detection_Bool_Calc("./Test_Runs/Outputs/0_1_78_8E-2_1_Postage_Stamp_Wavdetect_Outfile.fits", 350.933379, 0.0000078))
#print(Source_Detect_Big_Input_Generator())
Source_Detect_Generator_Driver()
