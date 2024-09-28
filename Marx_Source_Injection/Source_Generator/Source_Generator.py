import numpy as np
from ciao_contrib.runtool import *
import os
from os import system
import sys
from multiprocessing import Pool

dir = os.path.dirname(__file__)
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))
#from Histogram_Code import Galaxy_Histogram_Code_3
from Background_Generator import Background_Generator

def Empty_Coords_Generator(Roll_Angle=0.0):
    os.system("bash Bash_Scripts/Empty_Generator.sh "+str(Roll_Angle))

def Angle_Convert(Angle):
    if(Angle<0):
        Angle=Angle+360.0
    return Angle

def On_Chip_Bool_Calc(Theta,Phi,Empty_Filepath="/opt/xray/anthony/Research_Git/Marx_Source_Injection/Source_Generator/Empty_Coords/empty.fits", Empty_Coords_Gen_Bool=False):
    On_Chip_Bool=False
    if(Empty_Coords_Gen_Bool):
        Empty_Coords_Generator()
    dmcoords(infile=str(Empty_Filepath), theta=float(Theta), phi=float(Phi), option='msc', verbose=0, celfmt='deg')
    Chip_ID=dmcoords.chip_id
    Chip_X=dmcoords.chipx
    Chip_Y=dmcoords.chipy
    if((Chip_X>=1.0) and (Chip_X<=1024.0) and (Chip_Y>=1.0) and (Chip_Y<=1024.0)):
        On_Chip_Bool=True
    return On_Chip_Bool

def MSC_to_CEL_Convert(Theta,Phi,Empty_Filepath="/opt/xray/anthony/Research_Git/Marx_Source_Injection/Source_Generator/Empty_Coords/empty.fits", Empty_Coords_Gen_Bool=False):
    if(Empty_Coords_Gen_Bool):
        Empty_Coords_Generator()
    dmcoords(infile=str(Empty_Filepath), theta=float(Theta), phi=float(Phi), option='msc', verbose=0, celfmt='deg')
    RA=dmcoords.ra
    Dec=dmcoords.dec
    return RA, Dec

def Source_Generator(Counts,X,Y,Outpath="Source_Test", Parameter_Outpath="Source_Test_marx.par", Aspect_Parameter_Outpath="Source_Test_marxasp.par", Check_On_Chip_Bool=False, MSC_TO_CEL_Convert_Bool=True):
    if(Check_On_Chip_Bool and MSC_TO_CEL_Convert_Bool):
        #On_Chip_Bool=On_Chip_Bool_Calc(Theta,Phi)
        On_Chip_Bool=On_Chip_Bool_Calc(X,Y)
        if(On_Chip_Bool==False):
            raise Exception(str((X,Y))+" not on chip!")
    if(MSC_TO_CEL_Convert_Bool):
        RA,Dec=MSC_to_CEL_Convert(X,Y)
    else:
        RA=X
        Dec=Y
    #print("RA, Dec: ", RA,Dec)
    Roll_Angle=0.0
    #os.system("mkdir "+str(Outpath))
    path=os.path.realpath(Outpath)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    #Insert parameter file copying code
    os.system("cp /opt/anaconda3/envs/ciao-4.14/share/marx/pfiles/marx.par "+Parameter_Outpath)
    os.system("cp /opt/anaconda3/envs/ciao-4.14/share/marx/pfiles/marxasp.par "+Aspect_Parameter_Outpath)
    ##Bash_Command_Str="bash Bash_Scripts/Marx_Point_Source_Generator.sh "+str(RA)+" "+str(Dec)+" "+str(Roll_Angle)+" "+str(Counts)+" "+str(Outpath)
    Bash_Command_Str="bash Bash_Scripts/Marx_Point_Source_Generator.sh "+str(RA)+" "+str(Dec)+" "+str(Roll_Angle)+" "+str(Counts)+" "+str(Outpath)+" "+str(Parameter_Outpath)+" "+str(Aspect_Parameter_Outpath)
    #Bash_Command_Str="bash Bash_Scripts/Marx_Point_Source_Generator.sh "+str(RA)+" "+str(Dec)+" "+str(Roll_Angle)+" "+str(Counts)+" "+str(Outpath)+" "+str("/opt/anaconda3/envs/ciao-4.14/share/marx/pfiles/marx.par")+" "+str("/opt/anaconda3/envs/ciao-4.14/share/marx/pfiles/marxasp.par")
    os.system(Bash_Command_Str)

def Source_Coords_Generator(Phi_Step=15):
    Phi_A=np.arange(360,step=Phi_Step)
    #print("Phi_A: ", Phi_A)
    Phi_L=list(Phi_A)
    #print("Phi_L: ", Phi_L)
    Theta_A=np.arange(1,11)
    #print("Theta_A: ", Theta_A)
    Theta_L=list(Theta_A)
    #print("Theta_L: ", Theta_L)
    Coords_HL=[]
    for Phi in Phi_L:
        Theta_On_Chip_L=[]
        for Theta in Theta_L:
            On_Chip_Bool=On_Chip_Bool_Calc(Theta, Phi)
            if(On_Chip_Bool):
                Theta_On_Chip_L.append(Theta)
        Cur_Coords_HL=[Phi, Theta_On_Chip_L]
        Coords_HL.append(Cur_Coords_HL)
    return Coords_HL
#'''
def Source_Generator_Bulk(C_Min=3, C_Max=200, Count_Step=1, Number_of_Runs=50):
    #Source_Coords_HL=Source_Coords_Generator()
    Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]], [15, [1, 2, 3, 4, 5, 6, 7, 8]], [30, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [45, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [60, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [75, [1, 2, 3, 4, 5, 6, 7, 8]], [90, [1, 2, 3, 4, 5, 6, 7, 8]], [105, [2, 3, 4, 5, 6, 7, 8]], [120, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [135, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [150, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [165, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [180, [1, 2, 3, 4, 5, 6, 7, 8]], [195, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [210, [2, 3, 4, 5, 6, 7, 8, 9, 10]], [225, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [240, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [255, [2, 3, 4, 5, 6, 7, 8, 9]], [270, [1, 2, 3, 4, 5, 6, 7, 8]], [285, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [300, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [315, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [330, [2, 3, 4, 5, 6, 7, 8, 9]], [345, [1, 3, 4, 5, 6, 7, 8]]]
    #Counts_L=list(np.arange(3,201))
    C_Max=C_Max+Count_Step
    Number_of_Runs=Number_of_Runs+1
    Cur_Counts_L=np.arange(C_Min,C_Max,step=Count_Step)
    #print("Counts_L: ", Counts_L)
    Run_Count_L=list(np.arange(1,Number_of_Runs))
    #print("Run_Count_L: ", Run_Count_L)
    Number_of_Sources=0
    Number_of_Runs=0
    for Source_Coords_L in Source_Coords_HL:
        Cur_Phi=Source_Coords_L[0]
        Cur_Theta_L=Source_Coords_L[1]
        for Cur_Theta in Cur_Theta_L:
            Cur_Coords=(Cur_Theta,Cur_Phi)
            """
            if(Cur_Theta<=2.0):
                Cur_Counts_L=Counts_L_Low
            else:
                Cur_Counts_L=Counts_L_High
            """
            for Cur_Counts in Cur_Counts_L:
                Number_of_Sources=Number_of_Sources+1
                for Run_Count in Run_Count_L:
                    Number_of_Runs=Number_of_Runs+1
                    #(Cur_Counts,Cur_Theta,Cur_Phi,Outpath="Source_Test")
    print("Number_of_Sources: ", Number_of_Sources)
    print("Number_of_Runs: ", Number_of_Runs)
#'''

def Max_Counts_Calc(Theta, C_Low=3, C_High=150):
    return C_High

def Max_Counts_Calc_Broken(Theta, C_Low=3, C_High=150, Theta_Break=2):
    if(Theta<=Theta_Break):
        C_Max=C_Low
    if(Theta>Theta_Break):
        C_Max=C_High
    return C_Max

def Counts_List_Genertator(Max_Counts_Calc_Func,Theta, C_Min=3, Count_Step=25):
    C_Max=Max_Counts_Calc_Func(Theta)
    C_Max=C_Max+Count_Step
    Counts_L=np.arange(C_Min,C_Max,step=Count_Step)
    return Counts_L

def Background_Str_List_Genertator():
    Background_A=Background_Generator.Background_Array_Calc()
    Background_L=list(Background_A)
    Background_Str_L=[]
    for Background in Background_L:
        Background_Str=Background_Generator.Background_to_Background_String_Convert(Background)
        Background_Str_L.append(Background_Str)
    return Background_Str_L

def Source_Generator_Big_Input(Source_Coords_L, Max_Runs=1):
    Phi=Source_Coords_L[0]
    Theta_L=Source_Coords_L[1]
    Max_Runs=Max_Runs+1
    #Counts_L=np.arange(C_Min,C_Max,step=Count_Step)
    #print("Counts_L: ", Counts_L)
    Run_Count_L=list(np.arange(1,Max_Runs))
    #print("Run_Count_L: ", Run_Count_L)
    Background_Str_L=Background_Str_List_Genertator()
    print("Background_Str_L: ", Background_Str_L)
    Number_of_Sources=0
    Number_of_Runs=0
    for Cur_Theta in Theta_L:
        Cur_Coords=(Cur_Theta,Phi)
        Cur_Counts_L=Counts_List_Genertator(Max_Counts_Calc,Cur_Theta)
        #Cur_Counts_L=Counts_List_Genertator(Max_Counts_Calc_Broken,Cur_Theta)
        #print("Cur_Counts_L: ", Cur_Counts_L)
        Cur_RA,Cur_Dec=MSC_to_CEL_Convert(Cur_Theta,Phi)
        for Cur_Counts in Cur_Counts_L:
            Number_of_Sources=Number_of_Sources+1
            for Cur_Background in Background_Str_L:
                for Run_Count in Run_Count_L:
                    Number_of_Runs=Number_of_Runs+1
                    ##Cur_Outpath="./Marx_Sources/"+str(Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Run_Count)+"/"+str(Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Run_Count)
                    Cur_Outpath="./Marx_Sources/"+str(Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Run_Count)
                    print("Cur_Outpath: ", Cur_Outpath)
                    #Source_Generator(Cur_Counts,Cur_Theta,Phi,Outpath=Cur_Outpath)
                    ###Source_Generator(Cur_Counts,Cur_RA,Cur_Dec,Outpath=Cur_Outpath,MSC_TO_CEL_Convert_Bool=False)
        #print("Number_of_Sources: ", Number_of_Sources)
        print("Number_of_Runs: ", Number_of_Runs)

def Source_Generator_Big_Input_Generator(Max_Runs=1):
    #Source_Coords_HL=Source_Coords_Generator()
    ##Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]], [15, [1, 2, 3, 4, 5, 6, 7, 8]], [30, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [45, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [60, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [75, [1, 2, 3, 4, 5, 6, 7, 8]], [90, [1, 2, 3, 4, 5, 6, 7, 8]], [105, [2, 3, 4, 5, 6, 7, 8]], [120, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [135, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [150, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [165, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [180, [1, 2, 3, 4, 5, 6, 7, 8]], [195, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [210, [2, 3, 4, 5, 6, 7, 8, 9, 10]], [225, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [240, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [255, [2, 3, 4, 5, 6, 7, 8, 9]], [270, [1, 2, 3, 4, 5, 6, 7, 8]], [285, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [300, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [315, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [330, [2, 3, 4, 5, 6, 7, 8, 9]], [345, [1, 3, 4, 5, 6, 7, 8]]]
    #Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]], [45, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [90, [1, 2, 3, 4, 5, 6, 7, 8]], [135, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [180, [1, 2, 3, 4, 5, 6, 7, 8]], [225, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [270, [1, 2, 3, 4, 5, 6, 7, 8]], [315, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]]
    #Phi=Source_Coords_L[0]
    #Theta_L=Source_Coords_L[1]
    #Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]],[15, [1, 2, 3, 4, 5, 6, 7, 8]]]
    #Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]]]
    Source_Coords_HL=[[0, [1, 2]]]
    Max_Runs=Max_Runs+1
    #Counts_L=np.arange(C_Min,C_Max,step=Count_Step)
    #print("Counts_L: ", Counts_L)
    Run_Count_L=list(np.arange(1,Max_Runs))
    #print("Run_Count_L: ", Run_Count_L)
    Background_Str_L=Background_Str_List_Genertator()
    #print("Background_Str_L: ", Background_Str_L)
    Number_of_Sources=0
    Number_of_Runs=0
    Run_Input_L=[]
    for Source_Coords_L in Source_Coords_HL:
        Cur_Phi=Source_Coords_L[0]
        Cur_Theta_L=Source_Coords_L[1]
        for Cur_Theta in Cur_Theta_L:
            Cur_Coords=(Cur_Theta,Cur_Phi)
            Cur_Counts_L=Counts_List_Genertator(Max_Counts_Calc,Cur_Theta)
            #Cur_Counts_L=Counts_List_Genertator(Max_Counts_Calc_Broken,Cur_Theta)
            #print("Cur_Counts_L: ", Cur_Counts_L)
            Cur_RA,Cur_Dec=MSC_to_CEL_Convert(Cur_Theta,Cur_Phi)
            for Cur_Counts in Cur_Counts_L:
                #Number_of_Sources=Number_of_Sources+1
                for Cur_Background in Background_Str_L:
                    Number_of_Sources=Number_of_Sources+1
                    for Run_Count in Run_Count_L:
                        Number_of_Runs=Number_of_Runs+1
                        ##Cur_Outpath="./Marx_Sources/"+str(Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Run_Count)+"/"+str(Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Run_Count)
                        Cur_Outpath="./Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)
                        ##print("Cur_Outpath: ", Cur_Outpath)
                        Cur_Parameter_Outpath="./Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_marx.par"
                        #print("Cur_Parameter_Outpath: ", Cur_Parameter_Outpath)
                        Cur_Aspect_Parameter_Outpath="./Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_marxasp.par"
                        #print("Cur_Aspect_Parameter_Outpath: ", Cur_Aspect_Parameter_Outpath)
                        #Source_Generator(Cur_Counts,Cur_Theta,Phi,Outpath=Cur_Outpath)
                        ###Source_Generator(Cur_Counts,Cur_RA,Cur_Dec,Outpath=Cur_Outpath,MSC_TO_CEL_Convert_Bool=False)
                        Cur_Run_L=[Cur_Phi, Cur_Theta, Cur_RA, Cur_Dec, Cur_Counts, Cur_Background, Run_Count, Cur_Outpath, Cur_Parameter_Outpath, Cur_Aspect_Parameter_Outpath]
                        Run_Input_L.append(Cur_Run_L)
    #print("Number_of_Sources: ", Number_of_Sources)
    print("Number_of_Runs: ", Number_of_Runs)
    return Run_Input_L

def Source_Generator_Input_Wrapper(Input_L):
    Cur_Counts=Input_L[4]
    Cur_RA=Input_L[2]
    Cur_Dec=Input_L[3]
    Cur_Outpath=Input_L[7]
    Cur_Parameter_Outpath=Input_L[8]
    Cur_Aspect_Parameter_Outpath=Input_L[9]
    #print("Cur Input: ", str((Cur_Counts, Cur_RA, Cur_Dec, Cur_Outpath)))
    #print("Cur Input: ", str((Cur_Counts, Cur_RA, Cur_Dec, Cur_Outpath, Cur_Parameter_Outpath, Cur_Aspect_Parameter_Outpath)))
    #Source_Generator(Cur_Counts,Cur_RA,Cur_Dec,Outpath=Cur_Outpath,MSC_TO_CEL_Convert_Bool=False)
    Source_Generator(Cur_Counts, Cur_RA, Cur_Dec, Outpath=Cur_Outpath, Parameter_Outpath=Cur_Parameter_Outpath, Aspect_Parameter_Outpath=Cur_Aspect_Parameter_Outpath, MSC_TO_CEL_Convert_Bool=False)

def Squared(x):
    return x**2.0

def Driver(Func, Array):
    if __name__ == '__main__':
        P = Pool()
        P.map(Func, Array)

def Source_Generator_Driver():
    #Source_Coords_HL=Source_Coords_Generator()
    #Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]], [15, [1, 2, 3, 4, 5, 6, 7, 8]], [30, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [45, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [60, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [75, [1, 2, 3, 4, 5, 6, 7, 8]], [90, [1, 2, 3, 4, 5, 6, 7, 8]], [105, [2, 3, 4, 5, 6, 7, 8]], [120, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [135, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [150, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [165, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [180, [1, 2, 3, 4, 5, 6, 7, 8]], [195, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [210, [2, 3, 4, 5, 6, 7, 8, 9, 10]], [225, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [240, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [255, [2, 3, 4, 5, 6, 7, 8, 9]], [270, [1, 2, 3, 4, 5, 6, 7, 8]], [285, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [300, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [315, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [330, [2, 3, 4, 5, 6, 7, 8, 9]], [345, [1, 3, 4, 5, 6, 7, 8]]]
    #Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]]]
    ##Source_Coords_HL=[[0, [1, 2, 3, 4, 5, 6, 7, 8]], [45, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [90, [1, 2, 3, 4, 5, 6, 7, 8]], [135, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [180, [1, 2, 3, 4, 5, 6, 7, 8]], [225, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [270, [1, 2, 3, 4, 5, 6, 7, 8]], [315, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]]
    ##Driver(Source_Generator_Big_Input, Source_Coords_HL)
    Input_L=Source_Generator_Big_Input_Generator()
    Driver(Source_Generator_Input_Wrapper, Input_L)






#print(MSC_to_CEL_Convert(5,90))
#Source_Generator(100,5,90)
#Source_Generator(1000,5,90)
#Source_Generator(1000,5,0)
#print(MSC_to_CEL_Convert(5,0))
#print(MSC_to_CEL_Convert(5,360))
#print(MSC_to_CEL_Convert(1,0))
#print(MSC_to_CEL_Convert(0,0))
#Source_Generator(1000,0,0)
#Source_Generator(100,1,90)
#Source_Generator(100,2,90)
#Source_Generator(100,5,90)
#Source_Generator(100,5,0)
#Source_Generator(100,2,0)
#Source_Generator(100,2,90)
#Source_Generator(100,10,0)
#Source_Generator(100,2,180)
#Source_Generator(100,9,0)
#Source_Generator(100,10,45)
#Source_Generator(100,10,0)
#943718.4
#Source_Generator(int(943718.4),0,0)
#print(MSC_to_CEL_Convert(10,0))
#print(On_Chip_Bool_Calc(10,0))
#print(On_Chip_Bool_Calc(10,45))
"""
Offaxis_Test_A=np.linspace(0,1,10)
for Offaxis_Test in Offaxis_Test_A:
    print("Offaxis_Test: ", Offaxis_Test)
    print(On_Chip_Bool_Calc(Offaxis_Test,180))
"""
#print(On_Chip_Bool_Calc(10,55))
#print(Source_Coords_Generator())
#Source_Generator(3,1,90)
#Source_Generator(200,1,90)
#Source_Generator_Big_Input()
#Driver(Squared, list(np.arange(0,1000000)))
#Source_Generator_Driver()
#Source_Generator_Bulk()
#Source_Generator_Bulk(C_Max=150)
#print(Source_Coords_Generator(Phi_Step=45))
#print(Source_Generator_Big_Input_Generator())
