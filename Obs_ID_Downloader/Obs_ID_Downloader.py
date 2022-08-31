import os
from os import system
import sys
##import pandas as pd
from ciao_contrib.runtool import * #Imports ciao tools into python
def Obs_ID_Downloader(Obs_ID_L):
    """
    Obs_ID_L:- List   This is a list of strings, each string being a Obs ID that will be downloaded

    This Function takes a list of Obs ID strings, downloads the Obs ID's and reprocesses them.
    """
    #from ciao_contrib.runtool import * #Imports ciao tools into ipython #This code is broken now because "import * only allowed at module level"
    for Obs_ID in Obs_ID_L:
        Obs_ID_N=int(Obs_ID)
        download_chandra_obsid(obsid=Obs_ID_N) #This might not be the right symtax
        chandra_repro(indir= "/home/asantini/Desktop/Galaxy_Test/" + str(Obs_Id_N), outdir="/home/asantini/Desktop/Galaxy_Test/" + str(Obs_Id_N) + "/new", cleanup=no)
    print("Done")

def Read_ObsIDs(Fpath,Remove_Dups=True,Raw=False):
    if(Raw):
        #pass
        File = open(Fpath, "r")
        #for line in range(1,File):
        ObsID_L_With_Head=[]
        for Line in File:
            #print(Line)
            ObsID_Str_With_Head=Line.split(",")[1]
            #print(ObsID_Str_With_Head)
            ObsID_L_With_Head.append(ObsID_Str_With_Head)
        ObsID_Str_L=ObsID_L_With_Head[1:]
        ObsID_L=[]
        for ObsID_Str in ObsID_Str_L:
            ObsID=int(ObsID_Str)
            ObsID_L.append(ObsID)
        #print(ObsID_L)
    else:
        Data=pd.read_csv(Fpath)
        ObsID_A=Data["Obs ID"]
        ObsID_L=list(ObsID_A)
    if(Remove_Dups):
        ObsID_L_With_Dups=ObsID_L
        ObsID_L=list(set(ObsID_L))
        print("Number of Duplicates: ",len(ObsID_L_With_Dups)-len(ObsID_L))
    return ObsID_L

def Obs_ID_Downloader_2(Obs_ID_L,Outpath,Repo_Bool=False):
    os.chdir(Outpath) #Change Directory to where the output will be saved
    cwd = os.getcwd()
    print("Current_Working_Directory: "+str(cwd))
    #Outpath="/Volumes/expansion/" #Wrong Outpath for Testing
    print("Outpath: ",Outpath)
    if(cwd!=Outpath):
        raise Exception("The Current_Working_Directory is NOT the intended Outpath!!!")
    for Obs_ID in Obs_ID_L:
        Obs_ID_N=int(Obs_ID)
        ##download_chandra_obsid(obsid=Obs_ID_N)
        os.system("download_chandra_obsid "+str(Obs_ID_N))
        if(Repo_Bool):
            #chandra_repro(indir= "/Volumes/xray/anthony/Research_Git/Obs_ID_Downloader/" + str(Obs_Id_N), outdir="/Volumes/xray/anthony/Research_Git/Obs_ID_Downloader/" + str(Obs_Id_N) + "/new", cleanup=no)
            #chandra_repro(indir=cwd + str(Obs_ID_N), outdir=cwd + str(Obs_ID_N) + "/new", cleanup='no')
            Repo_Command="chandra_repro "+str(cwd)+"/"+str(Obs_ID_N)+" outdir="+str(cwd)+"/"+str(Obs_ID_N)+"/new cleanup=no"
            print("Repo_Command: ", Repo_Command)
            #os.system("chandra_repro "+str(cwd)+str(Obs_ID_N)+" outdir="+str(cwd)+ str(Obs_ID_N)+" /new cleanup=no")
            os.system(Repo_Command)

def Obs_ID_Downloader_2_Big_Input(Data_Path,Outpath,Remove_Dups_Bool=True,Raw_Bool=False,Repo_Bool_Var=False):
    ObsID_List=Read_ObsIDs(Data_Path,Remove_Dups=Remove_Dups_Bool,Raw=Raw_Bool)
    Obs_ID_Downloader_2(ObsID_List,Outpath,Repo_Bool=Repo_Bool_Var)
##Obs_ID_Downloader_2([10125],"/Volumes/xray/anthony/Research_Git/Obs_ID_Downloader/testdir",Repo_Bool=True)
#Obs_ID_Downloader_2([10125],"/opt/xray/anthony/Research_Git/Obs_ID_Downloader/testdir",Repo_Bool=True)
#/Volumes/expansion/ObsIDs
#Obs_ID_Downloader_2([10125],"/Volumes/expansion/ObsIDs")
#/Volumes/expansion/ObsID_Test
#Obs_ID_Downloader_2([10125],"/Volumes/expansion/ObsID_Test")
#print(Read_ObsIDs("/opt/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv",Remove_Dups=True,Raw=True))
#Read_ObsIDs("/opt/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv",Remove_Dups=True,Raw=True)
##print(Read_ObsIDs("/opt/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv"))
#Obs_ID_Downloader([10125])
##Obs_ID_Downloader_2_Big_Input("/opt/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv","/Volumes/expansion/ObsIDs",Remove_Dups_Bool=False,Raw_Bool=True)
##Obs_ID_Downloader_2([316, 361, 378, 380, 388, 389, 392, 393, 394, 395, 400, 407, 409, 414, 784, 790, 792, 864, 870, 871, 963, 969, 1302, 1578, 349, 353],"/Volumes/expansion/ObsIDs", Repo_Bool=True) # Wavdetect Fail List after parameter file bug fix
#Obs_ID_Downloader_2([316],"/Volumes/expansion/ObsIDs", Repo_Bool=True)
Obs_ID_Downloader_2_Big_Input("/opt/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv","/Volumes/expansion/ObsIDs", Remove_Dups_Bool=False, Raw_Bool=True, Repo_Bool_Var=True)
