from sherpa.astro.ui import *
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from ciao_contrib.runtool import *
import os
from os import system
import sys
import glob
from datetime import datetime


def Background_Date_Query(Path):
    #acis3sD2009-09-21bkgrnd_ctiN0003.fits
    Date_Str=Path.split("D")[-1].split("bk")[0].split("bg")[0]
    #print("Date_Str: ", Date_Str)
    datetime_object = datetime.strptime(Date_Str, "%Y-%m-%d")
    return datetime_object

def Background_File_Query(Key, Background_Path="/opt/anaconda3/envs/ciao-4.14/CALDB/data/chandra/acis/bkgrnd/", Latest_Bool=True):
    #Background_Path="/opt/anaconda3/envs/ciao-4.14/CALDB/data/chandra/acis/bkgrnd/"
    #acis<chip><aimpoint>D<date>bkgrndN<version>.fits
    Background_Path_L=glob.glob(Background_Path+"*.fits")
    Background_Path_L.sort(key=Background_Date_Query)
    #return Background_Path_L
    Match_L=[]
    for Background_Path in Background_Path_L:
        if((Key in Background_Path) and ("cti" not in Background_Path)):
            Match_L.append(Background_Path)
    if(Latest_Bool):
        return Match_L[-1]
    return Match_L

def Background_to_Counts_Calc(Background):
    #1024*1024=1,048,576
    Counts=Background*1048576.0
    return Counts

def Background_to_Background_String_Convert(Background, Include_Zero_Bool=True):
    Background_Str_Dict={0.0001:"1E-4",0.0002:"2E-4",0.0003:"3E-4",0.0004:"4E-4",0.0005:"5E-4",0.0006:"6E-4",0.0007:"7E-4",0.0008:"8E-4",0.0009:"9E-4",0.001:"1E-3",0.002:"2E-3",0.003:"3E-3",0.004:"4E-3",0.005:"5E-3",0.006:"6E-3",0.007:"7E-3",0.008:"8E-3",0.009:"9E-3",0.01:"1E-2",0.02:"2E-2",0.03:"3E-2",0.04:"4E-2",0.05:"5E-2",0.06:"6E-2",0.07:"7E-2",0.08:"8E-2",0.09:"9E-2",0.1:"1E-1",0.2:"2E-1",0.3:"3E-1",0.4:"4E-1",0.5:"5E-1",0.6:"6E-1",0.7:"7E-1",0.8:"8E-1",0.9:"9E-1"}
    if(Include_Zero_Bool):
        Background_Str_Dict={0.0:"0E-0",0.0001:"1E-4",0.0002:"2E-4",0.0003:"3E-4",0.0004:"4E-4",0.0005:"5E-4",0.0006:"6E-4",0.0007:"7E-4",0.0008:"8E-4",0.0009:"9E-4",0.001:"1E-3",0.002:"2E-3",0.003:"3E-3",0.004:"4E-3",0.005:"5E-3",0.006:"6E-3",0.007:"7E-3",0.008:"8E-3",0.009:"9E-3",0.01:"1E-2",0.02:"2E-2",0.03:"3E-2",0.04:"4E-2",0.05:"5E-2",0.06:"6E-2",0.07:"7E-2",0.08:"8E-2",0.09:"9E-2",0.1:"1E-1",0.2:"2E-1",0.3:"3E-1",0.4:"4E-1",0.5:"5E-1",0.6:"6E-1",0.7:"7E-1",0.8:"8E-1",0.9:"9E-1"}
    Background_Str=Background_Str_Dict[Background]
    return Background_Str

def Background_Generator(Background, Key, Outpath="./Backgrounds/"):
    Background_Path=Background_File_Query(Key)
    Total_Counts=Background_to_Counts_Calc(Background)
    if(Total_Counts==0):
        return
    #OutFpath=str(Outpath)+"Background_"+str(Key)+"_"+str(Background)+".fits"
    OutFpath=str(Outpath)+"Background_"+str(Key)+"_"+str(Background_to_Background_String_Convert(Background))+".fits"
    ##Bash_Command_Str="bash Bash_Scripts/Generate_Background.sh "+str(Background_Path)+" "+str(Total_Counts)+" "+str(Outpath)+"BG_"+str(Key)+"_"+str(Background)+".fits"
    Bash_Command_Str="bash Bash_Scripts/Generate_Background.sh "+str(Background_Path)+" "+str(Total_Counts)+" "+str(OutFpath)
    os.system(Bash_Command_Str)

def Background_Array_Calc(Include_Zero_Bool=True):
    a2 = np.arange(1,10,1)
    a1 = 10.**(np.arange(-4,0))
    X=np.outer(a1, a2).flatten()
    X=np.round(X,4)
    if(Include_Zero_Bool):
        X=np.insert(X, 0, 0.0)
    #X=np.format_float_positional(X, precision=3)
    return X

def Max_Background_Check(Background_Filepath):
    Num_BG_Pix=1024.0**2.0 #1,048,576
    #Dm_Out=dmlist(infile=str(evtfpath)+"[sky=circle("+str(BG_X_Pix)+","+str(BG_Y_Pix)+","+str(BG_R)+"),energy=300:10000]", opt='counts', outfile="", verbose=2) #Dm_Out:-ciao_contrib.runtool.CIAOPrintableString,Dmlist_Out,Uses the Dmlist CIAO tool to find the amount of counts in the background cirlce, Note: mlist "acis_evt2.fits[sky=rotbox(4148,4044,8,22,44.5)]" counts #Energy filter (0.3kev to 10kev) has been applied to the counts, This may allow the code to treat back illuminated chips and front illuminated chips the same, if not then the code must be modifed to consider both cases
    #Background_Filepath=Background_File_Query(Key)
    #Background_Filepath_L=Background_File_Query(Key, Latest_Bool=False)
    #Dm_Out=dmlist(infile=str(Background_Filepath)+"[energy=300:10000]", opt='counts', outfile="", verbose=2) #Dm_Out:-ciao_contrib.runtool.CIAOPrintableString,Dmlist_Out,Uses the Dmlist CIAO tool to find the amount of counts in the background cirlce, Note: mlist "acis_evt2.fits[sky=rotbox(4148,4044,8,22,44.5)]" counts #Energy filter (0.3kev to 10kev) has been applied to the counts, This may allow the code to treat back illuminated chips and front illuminated chips the same, if not then the code must be modifed to consider both cases
    Dm_Out=dmlist(infile=str(Background_Filepath), opt='counts', outfile="", verbose=2) #Dm_Out:-ciao_contrib.runtool.CIAOPrintableString,Dmlist_Out,Uses the Dmlist CIAO tool to find the amount of counts in the background cirlce, Note: mlist "acis_evt2.fits[sky=rotbox(4148,4044,8,22,44.5)]" counts #Energy filter (0.3kev to 10kev) has been applied to the counts, This may allow the code to treat back illuminated chips and front illuminated chips the same, if not then the code must be modifed to consider both cases
    Num_Counts_S=Dm_Out.split('\n')[9] #Num_Counts_S:-str, Number_of_Counts_String, The number of counts in the background cirlce as a string
    Num_Counts=float(Num_Counts_S) #Num_Counts:-float, Number_of_Counts, The number of counts as a float
    BG_Ratio=Num_Counts/Num_BG_Pix #BG_Ratio:-float, Background_Ratio, The background of the observation
    return BG_Ratio

def Background_Generator_Driver():
    Background_A=Background_Array_Calc()
    Chip_ID_A=["0i","1i","2i","3i","6i","7i","8i","1s","2s","3s","5s","6s","7s","8s","9s"]
    #Background_Str_Dict={0.0001:"1E-4",0.0002:"2E-4",0.0003:"3E-4",0.0004:"4E-4",0.0005:"5E-4",0.0006:"6E-4",0.0007:"7E-4",0.0008:"8E-4",0.0009:"9E-4",0.001:"1E-3",0.002:"2E-3",0.003:"3E-3",0.004:"4E-3",0.005:"5E-3",0.006:"6E-3",0.007:"7E-3",0.008:"8E-3",0.009:"9E-3",0.01:"1E-2",0.02:"2E-2",0.03:"3E-2",0.04:"4E-2",0.05:"5E-2",0.06:"6E-2",0.07:"7E-2",0.08:"8E-2",0.09:"9E-2",0.1:"1E-1",0.2:"2E-1",0.3:"3E-1",0.4:"4E-1",0.5:"5E-1",0.6:"6E-1",0.7:"7E-1",0.8:"8E-1",0.9:"9E-1"}
    """
    for Chip_ID in Chip_ID_A:
        Background_Path_L=Background_File_Query(Chip_ID,Latest_Bool=False)
        for Background_Path in Background_Path_L:
            print("Background_Path: ", Background_Path)
            Cur_Date=Background_Date_Query(Background_Path)
            Cur_Date_Str=Cur_Date.strftime('%m/%d/%Y')
            print(str(Chip_ID)+" "+Cur_Date_Str+": ", Max_Background_Check(Background_Path))
    """
    #Standard_Chip_ID="5s"
    for Background in Background_A:
        #print("Background: ", Background)
        #print("Background_Str: ", Background_Str_Dict[Background])
        #print("Background: ", str(Background)+"="+str(Background_Str_Dict[Background]))
        #print("Background: ", str(Background)+" = "+str(Background_to_Background_String_Convert(Background)))
        Background_Generator(Background,"5s")



#print(Background_Date_Query("/opt/anaconda3/envs/ciao-4.14/CALDB/data/chandra/acis/bkgrnd/acis3sD2009-09-21bkgrnd_ctiN0003.fits"))
#print(Background_File_Query("7s"))
#Background_Spectrum_Extract()
#Background_Generator()
#print(Background_to_Counts_Calc(0.001))
#print(Background_File_Query("6s"))
#Background_Generator(0.01,"5s")
#print(Max_Background_Check("6s"))
#print(Max_Background_Check("7s"))
##Background_Generator_Driver()
#print(Background_File_Query("5s"))
#print(Background_to_Counts_Calc(0.0))
#print(Background_Array_Calc())
