from sherpa.astro.ui import *
from matplotlib import pyplot as plt
import numpy as np
import os
from os import system
import sys
from ciao_contrib.runtool import *
from multiprocessing import Pool

dir = os.path.dirname(__file__)
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))
#from Histogram_Code import Galaxy_Histogram_Code_3
from Background_Generator import Background_Generator
from Source_Generator import Source_Generator
#def Synthetic_Background_Generator(Outpath, Background_Counts, RA, Dec, Source_Path, Parameter_Outpath, Background_Evtfile="/opt/anaconda3/envs/ciao-4.14/CALDB/data/chandra/acis/bkgrnd/acis5sD2009-09-21bkgrndN0002.fits"):
def Synthetic_Background_Generator(Outpath, Background_Counts, Parameter_Outpath, Seed):
    #os.system("bash Background_Marx_Run.sh")
    if(Background_Counts==0):
        return
    path=os.path.realpath(Outpath)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    #print("Before copy")
    ##print("cp /opt/anaconda3/envs/ciao-4.14/share/marx/pfiles/marx.par "+Parameter_Outpath)
    ##os.system("cp /opt/anaconda3/envs/ciao-4.14/share/marx/pfiles/marx.par "+Parameter_Outpath)
    print("cp ../Parameter_Files/pfiles/marx.par "+Parameter_Outpath)
    os.system("cp ../Parameter_Files/pfiles/marx.par "+Parameter_Outpath)
    #print("After copy")
    #Bash_Command="bash Bash_Scripts/Background_Marx_Run.sh "+str(Background_Counts)+" "+str(RA)+" "+str(Dec)+" "+str(Source_Path)+" "+str(Outpath)+" "+str(Parameter_Outpath)+" "+str(Background_Evtfile)
    Bash_Command="bash Bash_Scripts/Background_Marx_Run_Chip_Centered.sh "+str(Background_Counts)+" "+str(Outpath)+" "+str(Parameter_Outpath)+" "+str(Seed)
    print("Bash_Command: ", Bash_Command)
    os.system(Bash_Command)

"""
def Chip_ID_Calc(Theta,Phi,Empty_Filepath="/opt/xray/anthony/Research_Git/Marx_Source_Injection/Source_Generator/Empty_Coords/empty.fits"):
    dmcoords(infile=str(Empty_Filepath), theta=float(Theta), phi=float(Phi), option='msc', verbose=0, celfmt='deg')
    Chip_ID=dmcoords.chip_id
    return Chip_ID
"""

def Seed_Generator(Phi,Theta,Counts,Background_Str,Run_Count=None, Seed_Bias=1727923560): #Seed_Bias is unix time stamp for Thu Oct 03 2024 02:46:00 GMT+0000 (The maximum of the annular eclipse as seen from Wailuku, Maui).
    Background_Str_L=Background_Str.split("E")
    Backgorund_Factor_Str=Background_Str_L[0]
    Backgorund_Power=int(Background_Str_L[-1])
    if(Backgorund_Power<0):
        Backgorund_Power=Backgorund_Power*-1
    Backgorund_Power_Str=str(Backgorund_Power)
    if(Run_Count==None):
        Seed_Str="1"+str(int(Phi))+str(int(Theta))+str(int(Counts))+str(int(Backgorund_Factor_Str))+str(int(Backgorund_Power)) #Note: the leading "1" makes sure the Phi=0 degrees and Theta=0 arcmin are not removed during int conversion
    else:
        Seed_Str="1"+str(int(Phi))+str(int(Theta))+str(int(Counts))+str(int(Backgorund_Factor_Str))+str(int(Backgorund_Power))+str(int(Run_Count)) #Note: the leading "1" makes sure the Phi=0 degrees and Theta=0 arcmin are not removed during int conversion
    Seed=int(Seed_Str)
    Seed_Biased=Seed+int(Seed_Bias)
    return Seed, Seed_Biased

def Synthetic_Background_Generator_Big_Input_Generator():
    #Source_Coords_HL=Source_Coords_Generator()
    ##Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]], [15, [1, 2, 3, 4, 5, 6, 7, 8]], [30, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [45, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [60, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [75, [1, 2, 3, 4, 5, 6, 7, 8]], [90, [1, 2, 3, 4, 5, 6, 7, 8]], [105, [2, 3, 4, 5, 6, 7, 8]], [120, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [135, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [150, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [165, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [180, [1, 2, 3, 4, 5, 6, 7, 8]], [195, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [210, [2, 3, 4, 5, 6, 7, 8, 9, 10]], [225, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [240, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [255, [2, 3, 4, 5, 6, 7, 8, 9]], [270, [1, 2, 3, 4, 5, 6, 7, 8]], [285, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [300, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [315, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [330, [2, 3, 4, 5, 6, 7, 8, 9]], [345, [1, 3, 4, 5, 6, 7, 8]]]
    #Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]], [45, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [90, [1, 2, 3, 4, 5, 6, 7, 8]], [135, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [180, [1, 2, 3, 4, 5, 6, 7, 8]], [225, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [270, [1, 2, 3, 4, 5, 6, 7, 8]], [315, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]]
    #Phi=Source_Coords_L[0]
    #Theta_L=Source_Coords_L[1]
    #Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]],[15, [1, 2, 3, 4, 5, 6, 7, 8]]]
    #Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]]]
    #Source_Coords_HL=[[0, [1, 2]]]
    Source_Coords_HL=[[0, [1]]]
    #Source_Coords_HL=[[135, [2]]]
    #Max_Runs=Max_Runs+1
    Background_Str_L=Source_Generator.Background_Str_List_Genertator()
    #Background_Str_L=[Background_Str_L[1]] #For Testing
    #Background_Str_L=[Background_Str_L[25]] #For Testing
    #Background_Str_L=[Background_Str_L[32]] #For Testing
    #Background_Str_L=[Background_Str_L[-1]] #For Testing
    #Background_Str_L=[Background_Str_L[0]] #For Testing
    Background_Str_L=[Background_Str_L[0],Background_Str_L[1]] #For Testing
    #print("Background_Str_L: ", Background_Str_L)
    Number_of_Sources=0
    Number_of_Runs=0
    Run_Input_L=[]
    #Test_Seed_L=[]
    for Source_Coords_L in Source_Coords_HL:
        Cur_Phi=Source_Coords_L[0]
        Cur_Theta_L=Source_Coords_L[1]
        for Cur_Theta in Cur_Theta_L:
            Cur_Coords=(Cur_Theta,Cur_Phi)
            Cur_Counts_L=Source_Generator.Counts_List_Genertator(Source_Generator.Max_Counts_Calc,Cur_Theta)
            #Cur_Counts_L=[Cur_Counts_L[3]] #For Testing
            #Cur_Counts_L=[Cur_Counts_L[-1]] #For Testing
            #Cur_Counts_L=[Cur_Counts_L[0]] #For Testing
            Cur_Counts_L=[Cur_Counts_L[0], Cur_Counts_L[1]] #For Testing
            for Cur_Counts in Cur_Counts_L:
                #Number_of_Sources=Number_of_Sources+1
                for Cur_Background in Background_Str_L:
                    Number_of_Sources=Number_of_Sources+1
                    Cur_Seed,Cur_Seed_Biased=Seed_Generator(Cur_Phi,Cur_Theta,Cur_Counts,Cur_Background)
                    Cur_Background_Float=float(Cur_Background)
                    #print("Cur_Background_Float: ", Cur_Background+"="+str(Cur_Background_Float))
                    Cur_Background_Counts=int(Background_Generator.Background_to_Counts_Calc(Cur_Background_Float))
                    Cur_Outpath="./Synthetic_Backgrounds/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_bkg"
                    Cur_Parameter_Outpath="./Synthetic_Backgrounds/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_marx.par"
                    Number_of_Runs=Number_of_Runs+1
                    #Test_Seed_L.append(Cur_Seed_Biased)
                    Cur_Run_L=[Cur_Outpath, Cur_Background_Counts, Cur_Parameter_Outpath, Cur_Seed, Cur_Seed_Biased]
                    Run_Input_L.append(Cur_Run_L)
    print("Number_of_Runs: ", Number_of_Runs)
    #Test_Number_of_Seed_Dups=len(Test_Seed_L)-len(list(set(Test_Seed_L)))
    #print("Test_Number_of_Seed_Dups: ", Test_Number_of_Seed_Dups)
    return Run_Input_L

def Synthetic_Background_Generator_Wrapper(Input_L):
    #Cur_Run_L=[Cur_Outpath, Cur_Background_Counts, Cur_Parameter_Outpath]
    Outpath=Input_L[0]
    Background_Counts=Input_L[1]
    Parameter_Outpath=Input_L[2]
    Seed_Biased=Input_L[4]
    Synthetic_Background_Generator(Outpath, Background_Counts, Parameter_Outpath, Seed_Biased)

def Driver(Func, Array):
    if __name__ == '__main__':
        P = Pool()
        P.map(Func, Array)

def Synthetic_Background_Generator_Driver():
    #Source_Coords_HL=Source_Coords_Generator()
    #Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]], [15, [1, 2, 3, 4, 5, 6, 7, 8]], [30, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [45, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [60, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [75, [1, 2, 3, 4, 5, 6, 7, 8]], [90, [1, 2, 3, 4, 5, 6, 7, 8]], [105, [2, 3, 4, 5, 6, 7, 8]], [120, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [135, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [150, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [165, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [180, [1, 2, 3, 4, 5, 6, 7, 8]], [195, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [210, [2, 3, 4, 5, 6, 7, 8, 9, 10]], [225, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [240, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [255, [2, 3, 4, 5, 6, 7, 8, 9]], [270, [1, 2, 3, 4, 5, 6, 7, 8]], [285, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [300, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [315, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [330, [2, 3, 4, 5, 6, 7, 8, 9]], [345, [1, 3, 4, 5, 6, 7, 8]]]
    #Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]]]
    ##Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]], [45, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [90, [1, 2, 3, 4, 5, 6, 7, 8]], [135, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [180, [1, 2, 3, 4, 5, 6, 7, 8]], [225, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [270, [1, 2, 3, 4, 5, 6, 7, 8]], [315, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]]
    ##Driver(Source_Generator_Big_Input, Source_Coords_HL)
    #os.system("punlearn reproject_events")
    #os.system("pset reproject_events clobber=yes")
    Input_L=Synthetic_Background_Generator_Big_Input_Generator()
    Driver(Synthetic_Background_Generator_Wrapper, Input_L)

#Synthetic_Background_Big_Input([0, [1, 2, 3, 4, 5, 6, 7, 8]], Max_Runs=1)
#print(Synthetic_Background_Generator_Big_Input_Generator())
##Synthetic_Background_Generator_Driver()
#['../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1_asol1.fits', '../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1.fits', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_bkg', '359.9833303205489', '2.676250189553372e-06', 3, 838860.8, '../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_marx.par', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_reproject_events.par'], ['../Source_Generator/Marx_Sources/0/1/153/9E-1/1/0_1_153_9E-1_1_asol1.fits', '../Source_Generator/Marx_Sources/0/1/153/9E-1/1/0_1_153_9E-1_1.fits', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_bkg', '359.9833303205489', '2.676250189553372e-06', 3, 943718.4, '../Source_Generator/Marx_Sources/0/1/153/9E-1/1/0_1_153_9E-1_1', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_marx.par', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_reproject_events.par']
#Reproject_Background(Asolfile='../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1_asol1.fits', Source_Evtfile='../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1.fits', Outpath='./Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_bkg', Reproject_Parameter_Outpath='./Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_reproject_events.par', Background_Evtfile="/opt/anaconda3/envs/ciao-4.14/CALDB/data/chandra/acis/bkgrnd/acis5sD2009-09-21bkgrndN0002.fits")
#['../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1_asol1.fits', '../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1.fits', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_bkg', '359.9833303205489', '2.676250189553372e-06', 3, 838860.8, '../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_marx.par', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_reproject_events.par', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_dmkeypar.par', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_dmtcalc.par', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_dmsort.par'], ['../Source_Generator/Marx_Sources/0/1/153/9E-1/1/0_1_153_9E-1_1_asol1.fits', '../Source_Generator/Marx_Sources/0/1/153/9E-1/1/0_1_153_9E-1_1.fits', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_bkg', '359.9833303205489', '2.676250189553372e-06', 3, 943718.4, '../Source_Generator/Marx_Sources/0/1/153/9E-1/1/0_1_153_9E-1_1', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_marx.par', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_reproject_events.par', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_dmkeypar.par', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_dmtcalc.par', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_dmsort.par']
#Reproject_Background(Asolfile='../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1_asol1.fits', Source_Evtfile='../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1.fits', Outpath='./Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_bkg', Reproject_Parameter_Outpath='./Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_reproject_events.par', Dmkeypar_Parameter_Outpath='./Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_dmkeypar.par', Dmtcalc_Parameter_Outpath='./Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_dmtcalc.par', Dmsort_Parameter_Outpath='./Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_dmsort.par', Background_Evtfile="/opt/anaconda3/envs/ciao-4.14/CALDB/data/chandra/acis/bkgrnd/acis5sD2009-09-21bkgrndN0002.fits")
#print(Postage_Stamp_Coords_Calc(3,d=1024.0))
#print(Synthetic_Background_Generator_Big_Input_Generator())
