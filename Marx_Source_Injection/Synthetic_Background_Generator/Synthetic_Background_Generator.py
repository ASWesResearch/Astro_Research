from sherpa.astro.ui import *
from matplotlib import pyplot as plt
import numpy as np
import os
from os import system
import sys
from ciao_contrib.runtool import *

#"""
dir = os.path.dirname(__file__)
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))
#from Histogram_Code import Galaxy_Histogram_Code_3
from Source_Generator import Source_Generator
#"""

def Extract_Background_Spectrum(Asolfile, Evtfile, Chip_ID):
    #os.system("bash Background_Extract.sh "+"diffuse_asol1.fits"+" "+"diffuse_evt2.fits"+" "+"7")
    os.system("bash Background_Extract.sh "+str(Asolfile)+" "+str(Evtfile)+" "+str(Chip_ID))

def Table_Convert():
    load_data('blank_sky.pi')
    load_rmf('blank_sky.rmf')
    load_arf('blank_sky.arf')
    plot_data()
    plt.savefig('extracted_bkgspec.png')
    plt.savefig('extracted_bkgspec.eps')
    pl = get_data_plot()
    save_arrays('bkgspec.tbl', [pl.x, pl.y], ['Energy', pl.ylabel], ascii=True)

def Synthetic_Background_Gen():
    os.system("bash Background_Marx_Run.sh")

#"""
def Synthetic_Background_Big_Input(Source_Coords_L, Max_Runs=1):
    Phi=Source_Coords_L[0]
    Theta_L=Source_Coords_L[1]
    Max_Runs=Max_Runs+1
    #Counts_L=np.arange(C_Min,C_Max,step=Count_Step)
    #print("Counts_L: ", Counts_L)
    Run_Count_L=list(np.arange(1,Max_Runs))
    #print("Run_Count_L: ", Run_Count_L)
    Number_of_Sources=0
    Number_of_Runs=0
    for Cur_Theta in Theta_L:
        Cur_Coords=(Cur_Theta,Phi)
        Cur_Counts_L=Source_Generator.Counts_List_Genertator(Source_Generator.Max_Counts_Calc,Cur_Theta)
        #Cur_Counts_L=Counts_List_Genertator(Max_Counts_Calc_Broken,Cur_Theta)
        #print("Cur_Counts_L: ", Cur_Counts_L)
        Cur_RA,Cur_Dec=Source_Generator.MSC_to_CEL_Convert(Cur_Theta,Phi)
        for Cur_Counts in Cur_Counts_L:
            Number_of_Sources=Number_of_Sources+1
            for Run_Count in Run_Count_L:
                Number_of_Runs=Number_of_Runs+1
                Cur_Source_Path="../Source_Generator/Marx_Sources/"+str(Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Run_Count)+"/"+str(Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Run_Count)
                print("Cur_Outpath: ", Cur_Outpath)
                Cur_Outpath="./Synthetic_Backgrounds/"+str(Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Run_Count)+"/"+str(Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Run_Count)
                print("Cur_Outpath: ", Cur_Outpath)
                #Source_Generator(Cur_Counts,Cur_Theta,Phi,Outpath=Cur_Outpath)
                ##Source_Generator(Cur_Counts,Cur_RA,Cur_Dec,Outpath=Cur_Outpath,MSC_TO_CEL_Convert_Bool=False)
    #print("Number_of_Sources: ", Number_of_Sources)
    print("Number_of_Runs: ", Number_of_Runs)

Synthetic_Background_Big_Input([0, [1, 2, 3, 4, 5, 6, 7, 8]], Max_Runs=1)
#"""
