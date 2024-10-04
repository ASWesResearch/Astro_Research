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
"""
def Reproject_Background(Asolfile, Source_Evtfile, Outpath, Reproject_Parameter_Outpath, Dmkeypar_Parameter_Outpath, Dmtcalc_Parameter_Outpath, Dmsort_Parameter_Outpath, Background_Evtfile="/opt/anaconda3/envs/ciao-4.14/CALDB/data/chandra/acis/bkgrnd/acis5sD2009-09-21bkgrndN0002.fits"):
    #Bash_Command="bash Bash_Scripts/Background_Reproject.sh "+str(Background_Evtfile)+" "+str(Asolfile)+" "+str(Source_Evtfile)+" "+str(Chip_ID)+" "+str(Outpath)
    path=os.path.realpath(Outpath)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    #Bash_Command="bash Bash_Scripts/Background_Reproject.sh "+str(Source_Evtfile)+" "+str(Background_Evtfile)+" "+str(Outpath)+" "+str(Asolfile)
    #Bash_Command="bash Bash_Scripts/Background_Reproject.sh "+str(Source_Evtfile)+" "+str(Background_Evtfile)+" "+str(Outpath)+" "+str(Asolfile)+" "+str(Reproject_Parameter_Outpath)
    #os.system("cp /opt/anaconda3/envs/ciao-4.14/param/reproject_events.par "+Reproject_Parameter_Outpath)
    os.system("cp /Users/asantini/cxcds_param4/reproject_events.par "+Reproject_Parameter_Outpath)
    os.system("cp /Users/asantini/cxcds_param4/dmkeypar.par "+Dmkeypar_Parameter_Outpath)
    os.system("cp /Users/asantini/cxcds_param4/dmtcalc.par "+Dmtcalc_Parameter_Outpath)
    os.system("cp /Users/asantini/cxcds_param4/dmsort.par "+Dmsort_Parameter_Outpath)
    #dos2unix
    Bash_Command="bash Bash_Scripts/Background_Reproject.sh "+str(Source_Evtfile)+" "+str(Background_Evtfile)+" "+str(Outpath)+" "+str(Asolfile)+" "+str(Reproject_Parameter_Outpath)+" "+str(Dmkeypar_Parameter_Outpath)+" "+str(Dmtcalc_Parameter_Outpath)+" "+str(Dmsort_Parameter_Outpath)
    os.system(Bash_Command)

def Extract_Background_Spectrum(Asolfile, Source_Evtfile, Chip_ID, Outpath):
    #os.system("bash Background_Extract.sh "+"diffuse_asol1.fits"+" "+"diffuse_evt2.fits"+" "+"7")
    #os.system("bash Background_Extract.sh "+str(Asolfile)+" "+str(Source_Evtfile)+" "+str(Chip_ID))
    path=os.path.realpath(Outpath)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    #Bash_Command="bash Bash_Scripts/Background_Extract.sh "+str(Background_Evtfile)+" "+str(Asolfile)+" "+str(Source_Evtfile)+" "+str(Chip_ID)+" "+str(Outpath)
    Bash_Command="bash Bash_Scripts/Background_Extract.sh "+str(Asolfile)+" "+str(Source_Evtfile)+" "+str(Chip_ID)+" "+str(Outpath)
    print("Bash_Command: ", Bash_Command)
    os.system(Bash_Command)

def Table_Convert(Outpath):
    load_data(Outpath+"_"+'blank_sky.pi')
    load_rmf(Outpath+"_"+'blank_sky.rmf')
    load_arf(Outpath+"_"+'blank_sky.arf')
    plot_data()
    plt.savefig(Outpath+"_"+'extracted_bkgspec.png')
    plt.savefig(Outpath+"_"+'extracted_bkgspec.eps')
    pl = get_data_plot()
    save_arrays(Outpath+"_"+'bkgspec.tbl', [pl.x, pl.y], ['Energy', pl.ylabel], ascii=True)
"""
#def Synthetic_Background_Generator(Outpath, Background_Counts, RA, Dec, Source_Path, Parameter_Outpath, Background_Evtfile="/opt/anaconda3/envs/ciao-4.14/CALDB/data/chandra/acis/bkgrnd/acis5sD2009-09-21bkgrndN0002.fits"):
def Synthetic_Background_Generator(Outpath, Background_Counts, Parameter_Outpath, Seed):
    #os.system("bash Background_Marx_Run.sh")
    path=os.path.realpath(Outpath)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    print("Before copy")
    print("cp /opt/anaconda3/envs/ciao-4.14/share/marx/pfiles/marx.par "+Parameter_Outpath)
    os.system("cp /opt/anaconda3/envs/ciao-4.14/share/marx/pfiles/marx.par "+Parameter_Outpath)
    print("After copy")
    #os.system("cp /opt/anaconda3/envs/ciao-4.14/share/marx/pfiles/marxasp.par "+Aspect_Parameter_Outpath)
    #os.system("bash Background_Marx_Run.sh "+str(Background_Evtfile)+" "+str(Background_Counts)+" "+str(RA)+" "+str(Dec)+" "+str(Source_Path)+" "+str(Outpath))
    #Bash_Command="bash Bash_Scripts/Background_Marx_Run.sh "+str(Background_Evtfile)+" "+str(Background_Counts)+" "+str(RA)+" "+str(Dec)+" "+str(Source_Path)+" "+str(Outpath)+" "+str(Parameter_Outpath)
    #Bash_Command="bash Bash_Scripts/Background_Marx_Run.sh "+str(Background_Counts)+" "+str(RA)+" "+str(Dec)+" "+str(Source_Path)+" "+str(Outpath)+" "+str(Parameter_Outpath)
    ###Bash_Command="bash Bash_Scripts/Background_Marx_Run.sh "+str(Background_Counts)+" "+str(RA)+" "+str(Dec)+" "+str(Source_Path)+" "+str(Outpath)+" "+str(Parameter_Outpath)+" "+str(Background_Evtfile)
    ##Bash_Command="bash Bash_Scripts/Background_Marx_Run_Chip_Centered.sh "+str(Background_Counts)+" "+str(Outpath)+" "+str(Parameter_Outpath)
    Bash_Command="bash Bash_Scripts/Background_Marx_Run_Chip_Centered.sh "+str(Background_Counts)+" "+str(Outpath)+" "+str(Parameter_Outpath)+" "+str(Seed)
    print("Bash_Command: ", Bash_Command)
    os.system(Bash_Command)

def Chip_ID_Calc(Theta,Phi,Empty_Filepath="/opt/xray/anthony/Research_Git/Marx_Source_Injection/Source_Generator/Empty_Coords/empty.fits"):
    dmcoords(infile=str(Empty_Filepath), theta=float(Theta), phi=float(Phi), option='msc', verbose=0, celfmt='deg')
    Chip_ID=dmcoords.chip_id
    return Chip_ID

def Seed_Generator(Phi,Theta,Counts,Background_Str,Run_Count=None, Seed_Bias=1727923560): #Seed_Bias is unix time stamp for Thu Oct 03 2024 02:46:00 GMT+0000 (The maximum of the annular eclipse as seen from Wailuku, Maui).
    Background_Str_L=Background_Str.split("E")
    Backgorund_Factor_Str=Background_Str_L[0]
    Backgorund_Power=int(Background_Str_L[-1])
    if(Backgorund_Power<0):
        Backgorund_Power=Backgorund_Power*-1
    Backgorund_Power_Str=str(Backgorund_Power)
    if(Run_Count==None):
        Seed_Str=str(int(Phi))+str(int(Theta))+str(int(Counts))+str(int(Backgorund_Factor_Str))+str(int(Backgorund_Power))
    else:
        Seed_Str=str(int(Phi))+str(int(Theta))+str(int(Counts))+str(int(Backgorund_Factor_Str))+str(int(Backgorund_Power))+str(int(Run_Count))
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
    #Counts_L=np.arange(C_Min,C_Max,step=Count_Step)
    #print("Counts_L: ", Counts_L)
    #Run_Count_L=list(np.arange(1,Max_Runs))
    #print("Run_Count_L: ", Run_Count_L)
    Background_Str_L=Source_Generator.Background_Str_List_Genertator()
    #Background_Str_L=[Background_Str_L[1]] #For Testing
    Background_Str_L=[Background_Str_L[25]] #For Testing
    #Background_Str_L=[Background_Str_L[32]] #For Testing
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
            #print("Cur_Counts_L: ", Cur_Counts_L)
            #Cur_RA,Cur_Dec=Source_Generator.MSC_to_CEL_Convert(Cur_Theta,Cur_Phi)
            #Cur_Chip_ID=Chip_ID_Calc(Cur_Theta,Cur_Phi)
            Cur_Counts_L=[Cur_Counts_L[3]]
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
                    #print("Cur_Outpath: ", Cur_Outpath)
                    #Synthetic_Background_Generator(Outpath, Background_Counts, Parameter_Outpath)
                    Number_of_Runs=Number_of_Runs+1
                    Cur_Run_L=[Cur_Outpath, Cur_Background_Counts, Cur_Parameter_Outpath, Cur_Seed, Cur_Seed_Biased]
                    Run_Input_L.append(Cur_Run_L)
    print("Number_of_Runs: ", Number_of_Runs)
    return Run_Input_L

def Postage_Stamp_Coords_Calc(n=3, N=49, d=1024.0, X_P_Start=4065.0, Y_P_Start=4055.0, Empty_Filepath="/opt/xray/anthony/Research_Git/Marx_Source_Injection/Source_Generator/Empty_Coords/empty.fits"):
    n_s=int(np.sqrt(N))
    S=d/(2.0**n)
    W=d/(2.0**(n+1))
    g=(d-S*n_s)/(1.0+n_s)
    print("gap: ", g)
    Coords_L=[]
    for j in range(0,n_s):
        #print(j)
        #X=W*j #This is wrong
        X=W+(g*(j+1))+(S*j)
        X_P=X+X_P_Start
        for k in range(0,n_s):
            #Y=W*k #This is wrong
            Y=W+(g*(k+1))+(S*k)
            Y_P=Y+Y_P_Start
            Cur_Index_L=[j,k]
            Cur_Positon=[X,Y]
            Cur_Physical_Postion=[X_P,Y_P]
            dmcoords(infile=str(Empty_Filepath), x=float(X_P), y=float(Y_P), option='sky', verbose=0, celfmt='deg')
            RA=dmcoords.ra
            Dec=dmcoords.dec
            Cur_Cel_Positon=[RA,Dec]
            Cur_Coords=[Cur_Index_L, Cur_Positon, Cur_Physical_Postion, Cur_Cel_Positon]
            Coords_L.append(Cur_Coords)
    return Coords_L, S, g

"""
def Synthetic_Background_Generator_Big_Input_Generator(Max_Runs=1):
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
    Max_Runs=Max_Runs+1
    #Counts_L=np.arange(C_Min,C_Max,step=Count_Step)
    #print("Counts_L: ", Counts_L)
    Run_Count_L=list(np.arange(1,Max_Runs))
    #print("Run_Count_L: ", Run_Count_L)
    Background_Str_L=Source_Generator.Background_Str_List_Genertator()
    #Background_Str_L=[Background_Str_L[1]] #For Testing
    Background_Str_L=[Background_Str_L[25]] #For Testing
    #Background_Str_L=[Background_Str_L[32]] #For Testing
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
            #print("Cur_Counts_L: ", Cur_Counts_L)
            Cur_RA,Cur_Dec=Source_Generator.MSC_to_CEL_Convert(Cur_Theta,Cur_Phi)
            Cur_Chip_ID=Chip_ID_Calc(Cur_Theta,Cur_Phi)
            Cur_Counts_L=[Cur_Counts_L[3]]
            for Cur_Counts in Cur_Counts_L:
                #Number_of_Sources=Number_of_Sources+1
                for Cur_Background in Background_Str_L:
                    Number_of_Sources=Number_of_Sources+1
                    Cur_Background_Float=float(Cur_Background)
                    #print("Cur_Background_Float: ", Cur_Background+"="+str(Cur_Background_Float))
                    Cur_Background_Counts=int(Background_Generator.Background_to_Counts_Calc(Cur_Background_Float))
                    for Run_Count in Run_Count_L:
                        Number_of_Runs=Number_of_Runs+1
                        Cur_Outpath="./Synthetic_Backgrounds/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_bkg"
                        ##print("Cur_Outpath: ", Cur_Outpath)
                        Cur_Source_Path="../Source_Generator/Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)
                        Cur_Asol_Path="../Source_Generator/Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_asol1.fits"
                        #print("Cur_Asol_Path: ", Cur_Asol_Path)
                        Cur_Source_Evt_Path="../Source_Generator/Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+".fits"
                        Cur_Parameter_Outpath="./Synthetic_Backgrounds/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_marx.par"
                        #print("Cur_Parameter_Outpath: ", Cur_Parameter_Outpath)
                        #Cur_Aspect_Parameter_Outpath="./Synthetic_Backgrounds/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_marxasp.par"
                        #print("Cur_Asol_Path: ", Cur_Asol_Path)
                        Cur_Reproject_Parameter_Outpath="./Synthetic_Backgrounds/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_reproject_events.par"
                        #print("Cur_Reproject_Parameter_Outpath: ", Cur_Reproject_Parameter_Outpath)
                        Cur_Dmkeypar_Parameter_Outpath="./Synthetic_Backgrounds/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_dmkeypar.par"
                        #print("Cur_Dmkeypar_Parameter_Outpath: ", Cur_Dmkeypar_Parameter_Outpath)
                        Cur_Dmtcalc_Parameter_Outpath="./Synthetic_Backgrounds/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_dmtcalc.par"
                        #print("Cur_Dmtcalc_Parameter_Outpath: ", Cur_Dmtcalc_Parameter_Outpath)
                        Cur_Dmsort_Parameter_Outpath="./Synthetic_Backgrounds/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_dmsort.par"
                        #print("Cur_Dmsort_Parameter_Outpath: ", Cur_Dmsort_Parameter_Outpath)
                        #Cur_Run_L=[Cur_Asol_Path, Cur_Source_Evt_Path, Cur_Outpath, Cur_RA, Cur_Dec, Cur_Chip_ID, Cur_Background_Counts, Cur_Source_Path, Cur_Parameter_Outpath, Cur_Reproject_Parameter_Outpath]
                        Cur_Run_L=[Cur_Asol_Path, Cur_Source_Evt_Path, Cur_Outpath, Cur_RA, Cur_Dec, Cur_Chip_ID, Cur_Background_Counts, Cur_Source_Path, Cur_Parameter_Outpath, Cur_Reproject_Parameter_Outpath, Cur_Dmkeypar_Parameter_Outpath, Cur_Dmtcalc_Parameter_Outpath, Cur_Dmsort_Parameter_Outpath]
                        Run_Input_L.append(Cur_Run_L)
    #print("Number_of_Sources: ", Number_of_Sources)
    print("Number_of_Runs: ", Number_of_Runs)
    return Run_Input_L

def Synthetic_Background_Generator_Wrapper(Input_L):
    Asolfile=Input_L[0]
    Source_Evtfile=Input_L[1]
    Chip_ID=Input_L[5]
    Outpath=Input_L[2]
    Background_Counts=Input_L[6]
    RA=Input_L[3]
    Dec=Input_L[4]
    Source_Path=Input_L[7]
    Parameter_Outpath=Input_L[8]
    Reproject_Parameter_Outpath=Input_L[9]
    Dmkeypar_Parameter_Outpath=Input_L[10]
    Dmtcalc_Parameter_Outpath=Input_L[11]
    Dmsort_Parameter_Outpath=Input_L[12]
    #Aspect_Parameter_Outpath=Input_L[9]
    #Reproject_Background(Asolfile, Source_Evtfile, Outpath, Reproject_Parameter_Outpath, Background_Evtfile="/opt/anaconda3/envs/ciao-4.14/CALDB/data/chandra/acis/bkgrnd/acis5sD2009-09-21bkgrndN0002.fits")
    ##Reproject_Background(Asolfile, Source_Evtfile, Outpath, Reproject_Parameter_Outpath, Dmkeypar_Parameter_Outpath, Dmtcalc_Parameter_Outpath, Dmsort_Parameter_Outpath)
    ##Extract_Background_Spectrum(Asolfile, Source_Evtfile, Chip_ID, Outpath)
    ##Table_Convert(Outpath)
    #Synthetic_Background_Generator(Outpath, Background_Counts, RA, Dec, Source_Path)
    #Synthetic_Background_Generator(Outpath, Background_Counts, RA, Dec, Parameter_Outpath, Source_Path)
    Synthetic_Background_Generator(Outpath=Outpath, Background_Counts=Background_Counts, RA=RA, Dec=Dec, Source_Path=Source_Path, Parameter_Outpath=Parameter_Outpath)
"""
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
Synthetic_Background_Generator_Driver()
#['../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1_asol1.fits', '../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1.fits', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_bkg', '359.9833303205489', '2.676250189553372e-06', 3, 838860.8, '../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_marx.par', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_reproject_events.par'], ['../Source_Generator/Marx_Sources/0/1/153/9E-1/1/0_1_153_9E-1_1_asol1.fits', '../Source_Generator/Marx_Sources/0/1/153/9E-1/1/0_1_153_9E-1_1.fits', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_bkg', '359.9833303205489', '2.676250189553372e-06', 3, 943718.4, '../Source_Generator/Marx_Sources/0/1/153/9E-1/1/0_1_153_9E-1_1', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_marx.par', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_reproject_events.par']
#Reproject_Background(Asolfile='../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1_asol1.fits', Source_Evtfile='../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1.fits', Outpath='./Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_bkg', Reproject_Parameter_Outpath='./Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_reproject_events.par', Background_Evtfile="/opt/anaconda3/envs/ciao-4.14/CALDB/data/chandra/acis/bkgrnd/acis5sD2009-09-21bkgrndN0002.fits")
#['../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1_asol1.fits', '../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1.fits', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_bkg', '359.9833303205489', '2.676250189553372e-06', 3, 838860.8, '../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_marx.par', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_reproject_events.par', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_dmkeypar.par', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_dmtcalc.par', './Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_dmsort.par'], ['../Source_Generator/Marx_Sources/0/1/153/9E-1/1/0_1_153_9E-1_1_asol1.fits', '../Source_Generator/Marx_Sources/0/1/153/9E-1/1/0_1_153_9E-1_1.fits', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_bkg', '359.9833303205489', '2.676250189553372e-06', 3, 943718.4, '../Source_Generator/Marx_Sources/0/1/153/9E-1/1/0_1_153_9E-1_1', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_marx.par', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_reproject_events.par', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_dmkeypar.par', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_dmtcalc.par', './Synthetic_Backgrounds/0/1/153/9E-1/1/0_1_153_9E-1_1_dmsort.par']
#Reproject_Background(Asolfile='../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1_asol1.fits', Source_Evtfile='../Source_Generator/Marx_Sources/0/1/153/8E-1/1/0_1_153_8E-1_1.fits', Outpath='./Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_bkg', Reproject_Parameter_Outpath='./Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_reproject_events.par', Dmkeypar_Parameter_Outpath='./Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_dmkeypar.par', Dmtcalc_Parameter_Outpath='./Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_dmtcalc.par', Dmsort_Parameter_Outpath='./Synthetic_Backgrounds/0/1/153/8E-1/1/0_1_153_8E-1_1_dmsort.par', Background_Evtfile="/opt/anaconda3/envs/ciao-4.14/CALDB/data/chandra/acis/bkgrnd/acis5sD2009-09-21bkgrndN0002.fits")
#print(Postage_Stamp_Coords_Calc(3,d=1024.0))
#print(Synthetic_Background_Generator_Big_Input_Generator())
