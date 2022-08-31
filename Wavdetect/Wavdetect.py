import os
from os import system
import sys
import glob
import re
from ciao_contrib.runtool import * #Imports ciao tools into python
import ciao_contrib.runtool as rt
import time
import logging
def File_Query(ObsID,ObsID_Path='/Volumes/expansion/ObsIDs/',key="evt2"):
    #Query_Path='/Volumes/xray/simon/all_chandra_observations/'+str(ObsID)+'/primary/*evt2*'
    #Query_Path=ObsID_Path+str(ObsID)+'/primary/*evt2*'
    ##Query_Path=ObsID_Path+str(ObsID)+'/*/*'+str(key)+'*'
    #files = glob.glob('/home/geeks/Desktop/gfg/**/*.txt', recursive = True)
    Query_Path=ObsID_Path+str(ObsID)+'/**/*'+str(key)+'*'
    fpath_L=glob.glob(Query_Path, recursive = True)
    print("fpath_L: ", fpath_L)
    if(len(fpath_L)!=1):
        ##raise Exception(str(ObsID)+" has "+str(len(fpath_L))+" "+str(key)+" Files ! ! !")
        for cur_fpath in fpath_L:
            if("repro" in cur_fpath):
                print("Match")
                fpath=cur_fpath
                break
            elif("/new/" in cur_fpath):
                fpath=cur_fpath
                break
            else:
                raise Exception(str(ObsID)+" has "+str(len(fpath_L))+" "+str(key)+" Files ! ! !")
    else:
        fpath=fpath_L[0]
    return fpath
def Read_ObsIDs(Fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv",Remove_Dups=True,Raw=False):
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
def Split_FPath(FPath):
    FPath_L=FPath.split("/")
    FPath_L.pop(-1)
    Path_L=FPath_L
    Path=""
    for str in Path_L:
        Path=Path+str+"/"
    return Path
def Fluximage(ObsID_L,ObsID_Path='/Volumes/expansion/ObsIDs/', key="evt2", Clobber_Bool=False):
    for ObsID in ObsID_L:
        ObsID_N=int(ObsID)
        Filepath=File_Query(ObsID_N,ObsID_Path,key)
        print("Filepath: ", Filepath)
        Filename=Filepath.split("/")[-1]
        print("Filename: ", Filename)
        Filename_Reduced=Filename.split("_")[0]
        print("Filename_Reduced: ", Filename_Reduced)
        Primary_Path=Split_FPath(Filepath)
        print("Primary_Path: ", Primary_Path)
        #Outpath=Primary_Path+"exposure_correction/"
        Outpath=Primary_Path+"exposure_correction/"+str(ObsID_N)
        ##Outpath=Primary_Path+str(ObsID_N)
        print("Outpath: ", Outpath)
        if(Clobber_Bool):
            os.system("fluximage "+str(Filepath)+" "+str(Outpath)+" psfecf=0.9 binsize=1 clobber=yes verbose=1")
        else:
            os.system("fluximage "+str(Filepath)+" "+str(Outpath)+" psfecf=0.9 binsize=1 clobber=no verbose=1")

def Wavdetect(ObsID_L,ObsID_Path='/Volumes/expansion/ObsIDs/', key="broad_thresh", Clobber_Bool=False):
    for ObsID in ObsID_L:
        ObsID_N=int(ObsID)
        Evt2_Filepath=File_Query(ObsID_N,ObsID_Path)
        print("Evt2_Filepath: ", Evt2_Filepath)
        FOV1_Filepath=File_Query(ObsID_N,ObsID_Path,key="fov1")
        print("FOV1_Filepath: ", FOV1_Filepath)
        Primary_Path=Split_FPath(Evt2_Filepath)
        print("Primary_Path: ", Primary_Path)
        Exposure_Path=Primary_Path+"exposure_correction/"
        ##Exposure_Path=Primary_Path
        ##"""
        Broad_Thresh_Img_Path=File_Query(ObsID_N,ObsID_Path,key="broad_thresh.img")
        print("Broad_Thresh_Img_Path: ", Broad_Thresh_Img_Path)
        Broad_Flux_Img_Path=File_Query(ObsID_N,ObsID_Path,key="broad_flux.img")
        print("Broad_Flux_Img_Path: ", Broad_Flux_Img_Path)
        Exposure_Map_Path=File_Query(ObsID_N,ObsID_Path,key="expmap")
        print("Exposure_Map_Path: ", Exposure_Map_Path)
        ##"""
        PSF_Map_Path=File_Query(ObsID_N,ObsID_Path,key="psfmap")
        print("PSF_Map_Path: ", PSF_Map_Path)
        #Outfile=Exposure_Path+str(ObsID)
        Outfile=Exposure_Path+str(ObsID)+"_src.fits"
        print("Outfile: ", Outfile)
        Scellfile=Exposure_Path+str(ObsID)+"_scell.fits"
        print("Scellfile: ", Scellfile)
        Imagefile=Exposure_Path+str(ObsID)+"_imgfile.fits"
        print("Imagefile: ", Imagefile)
        Defnbkgfile=Exposure_Path+str(ObsID)+"_nbgd.fits"
        print("Defnbkgfile: ", Defnbkgfile)
        Regfile=Exposure_Path+str(ObsID)+"_src.reg"
        print("Regfile: ", Regfile)
        #os.system("wavdetect "+str(Broad_Thresh_Img_Path)+" outfile="+str(Outfile)+" scellfile="+str(Outfile)+" imagefile="+str(Outfile)+" defnbkgfile="+str(Outfile)+" regfile="+str(Outfile)+" scales='1 2 4 8 16'"+" expfile="+str(Exposure_Map_Path)+" psffile="+str(PSF_Map_Path)+" clobber=yes")
        #os.system("wavdetect "+str(Broad_Thresh_Img_Path)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='1 2 4 8 16'"+" expfile="+str(Exposure_Map_Path)+" psffile="+str(PSF_Map_Path)+" clobber=yes")
        ##os.system("wavdetect "+str(Broad_Thresh_Img_Path)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='1 2 4 8 16'"+" expfile="+str(Exposure_Map_Path)+" psffile="+str(PSF_Map_Path)+" clobber=yes") #This is a test without the 16 scale
        if(Clobber_Bool):
            os.system("wavdetect "+str(Broad_Thresh_Img_Path)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='1 2 4 8'"+" expfile="+str(Exposure_Map_Path)+" psffile="+str(PSF_Map_Path)+" clobber=yes verbose=1") #This is a test without the 16 scale
        else:
            os.system("wavdetect "+str(Broad_Thresh_Img_Path)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='1 2 4 8'"+" expfile="+str(Exposure_Map_Path)+" psffile="+str(PSF_Map_Path)+" clobber=no verbose=1") #This is a test without the 16 scale
        ##os.system("wavdetect "+str(Broad_Flux_Img_Path)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='1 2 4 8 16'"+" expfile="+str(Exposure_Map_Path)+" psffile="+str(PSF_Map_Path)+" clobber=yes")
        #os.system("wavdetect "+str(Broad_Flux_Img_Path)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='1 2 4 8'"+" expfile="+str(Exposure_Map_Path)+" psffile="+str(PSF_Map_Path)+" clobber=yes") #This is a test without the 16 scale
        ##Input_Filepath=File_Query(ObsID_N,ObsID_Path,key=key)
        ##print("Input_Filepath: ", Input_Filepath)
        #os.system("wavdetect "+str(Input_Filepath)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='2 4 8 16'"+"psffile=default  verbose=1 clobber=yes")
        ##os.system("wavdetect "+str(Input_Filepath)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='2 4 8 16'"+"psffile="+str(PSF_Map_Path)+" clobber=yes")
        #os.system("wavdetect "+str(Input_Filepath)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='1 2 4 8 16'"+" expfile="+str(Exposure_Map_Path)+" psffile="+str(PSF_Map_Path)+" clobber=yes")
def Main():
    Fluximage_Fail_L=[]
    Wavdetect_Fail_L=[]
    ObsID_L=Read_ObsIDs(Raw=True) #Full List
    #Wav_not_in_Flux_L:[316, 361, 378, 380, 388, 389, 392, 393, 394, 395, 400, 407, 409, 414, 784, 790, 792, 864, 870, 871, 963, 969, 1302, 1578, 12155, 12156, 3965, 20353, 16260, 16261, 16262, 20356, 10125, 16276, 16277, 8086, 14230, 14231, 8091, 8098, 18340, 18341, 18342, 18343, 4010, 4016, 4017, 18352, 4019, 8125, 8126, 12238, 12239, 6096, 6097, 22478, 22479, 22480, 22482, 2014, 6114, 6115, 6118, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2039, 2040, 14332, 8190]
    #Fluximage_Fail_L:[349, 353, 24979, 24980, 25179, 25186, 25191, 25220, 23599, 23638, 25689, 25777, 25778, 25779, 25780, 25781, 25782, 23479, 23480, 23481, 25989, 25990, 23489, 23490, 23491, 26038, 26039, 23494, 23495, 23496, 23497, 23498, 23499, 23500, 23501, 24392, 24393, 24438, 24439, 24440, 24441, 24442, 22481]
    ##ObsID_L=[316, 361, 378, 380, 388, 389, 392, 393, 394, 395, 400, 407, 409, 414, 784, 790, 792, 864, 870, 871, 963, 969, 1302, 1578, 12155, 12156, 3965, 20353, 16260, 16261, 16262, 20356, 10125, 16276, 16277, 8086, 14230, 14231, 8091, 8098, 18340, 18341, 18342, 18343, 4010, 4016, 4017, 18352, 4019, 8125, 8126, 12238, 12239, 6096, 6097, 22478, 22479, 22480, 22482, 2014, 6114, 6115, 6118, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2039, 2040, 14332, 8190, 349, 353, 24979, 24980, 25179, 25186, 25191, 25220, 23599, 23638, 25689, 25777, 25778, 25779, 25780, 25781, 25782, 23479, 23480, 23481, 25989, 25990, 23489, 23490, 23491, 26038, 26039, 23494, 23495, 23496, 23497, 23498, 23499, 23500, 23501, 24392, 24393, 24438, 24439, 24440, 24441, 24442, 22481] #Error List = Wav_not_in_Flux_L + Fluximage_Fail_L
    #ObsID_L=[316, 361, 378, 380, 388, 389, 392, 393, 394, 395, 400, 407, 409, 414, 784, 790, 792, 864, 870, 871, 963, 969, 1302, 1578, 12155, 12156, 3965, 20353, 16260, 16261, 16262, 20356, 10125, 16276, 16277, 8086, 14230, 14231, 8091, 8098, 18340, 18341, 18342, 18343, 4010, 4016, 4017, 18352, 4019, 8125, 8126, 12238, 12239, 6096, 6097, 22478, 22479, 22480, 22482, 2014, 6114, 6115, 6118, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2039, 2040, 14332, 8190, 349, 353, 23479, 23489, 23494] #Error List = Wav_not_in_Flux_L + Fluximage_Fail_L without ObsIDs with missing data
    ##ObsID_L=[316, 361, 378, 380, 388, 389, 392, 393, 394, 395, 400, 407, 409, 414, 784, 790, 792, 864, 870, 871, 963, 969, 1302, 1578, 349, 353] #Fail list after parameter file bug fix
    #ObsID_L=[316] #Fail list after parameter file bug fix. Only 1 selected for a testing.
    #ObsID_L=[8197] #Test
    Error_Log_File=open("/Volumes/expansion/Error_Log.txt","w")
    Fluximage_Error_Log_File=open("/Volumes/expansion/Fluximage_Error_Log.txt","w")
    Wavdetect_Error_Log_File=open("/Volumes/expansion/Wavdetect_Error_Log.txt","w")
    for ObsID in ObsID_L:
        with rt.new_pfiles_environment(ardlib=True):
            try:
                Fluximage([ObsID],ObsID_Path="/Volumes/expansion/ObsIDs/", Clobber_Bool=True)
                #Fluximage([ObsID],ObsID_Path="/Volumes/expansion/ObsIDs/", Clobber_Bool=False)
            except Exception as Argument:
                Fluximage_Fail_L.append(ObsID)
                Error_Log_File.write(str(ObsID)+" "+"Fluximage Error:\n"+str(Argument)+"\n")
                Fluximage_Error_Log_File.write(str(ObsID)+":\n"+str(Argument)+"\n")
            try:
                Wavdetect([ObsID],ObsID_Path="/Volumes/expansion/ObsIDs/", Clobber_Bool=True)
                #Wavdetect([ObsID],ObsID_Path="/Volumes/expansion/ObsIDs/", Clobber_Bool=False)
            except Exception as Argument:
                Wavdetect_Fail_L.append(ObsID)
                Error_Log_File.write(str(ObsID)+" "+"Wavdetect Error:\n"+str(Argument)+"\n")
                Wavdetect_Error_Log_File.write(str(ObsID)+":\n"+str(Argument)+"\n")
    print("Fluximage_Fail_L:\n", Fluximage_Fail_L)
    print("Wavdetect_Fail_L:\n", Wavdetect_Fail_L)
    f=open("/Volumes/expansion/Fail_List.txt","w")
    f.write("Fluximage_Fail_L: "+str(Fluximage_Fail_L)+"\n")
    f.write("Wavdetect_Fail_L: "+str(Wavdetect_Fail_L)+"\n")
    f.close()
    Error_Log_File.close()
    Fluximage_Error_Log_File.close()
    Wavdetect_Error_Log_File.close()
Main()

#print(Split_FPath("/Volumes/expansion/ObsIDs/10125/primary/acisf10125N003_evt2.fits.gz"))
##Fluximage([10125],ObsID_Path="/Volumes/expansion/ObsID_Test/")
##Wavdetect([10125],ObsID_Path="/Volumes/expansion/ObsID_Test/")
#13813
#Fluximage([13813],ObsID_Path="/Volumes/expansion/ObsID_Test/")
#Wavdetect([13813],ObsID_Path="/Volumes/expansion/ObsID_Test/")
##Test_Main([10125])
#8197
#Fluximage([8197],ObsID_Path="/Volumes/expansion/ObsID_Test/")
#Wavdetect([8197],ObsID_Path="/Volumes/expansion/ObsID_Test/")
