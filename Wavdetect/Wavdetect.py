import os
from os import system
import sys
import glob
import re
from ciao_contrib.runtool import * #Imports ciao tools into python
import time
def File_Query(ObsID,ObsID_Path='/Volumes/expansion/ObsIDs/',key="evt2"):
    #Query_Path='/Volumes/xray/simon/all_chandra_observations/'+str(ObsID)+'/primary/*evt2*'
    #Query_Path=ObsID_Path+str(ObsID)+'/primary/*evt2*'
    ##Query_Path=ObsID_Path+str(ObsID)+'/*/*'+str(key)+'*'
    #files = glob.glob('/home/geeks/Desktop/gfg/**/*.txt', recursive = True)
    Query_Path=ObsID_Path+str(ObsID)+'/**/*'+str(key)+'*'
    fpath_L=glob.glob(Query_Path, recursive = True)
    print("fpath_L: ", fpath_L)
    if(len(fpath_L)!=1):
        raise Exception(str(ObsID)+" has "+str(len(fpath_L))+" "+str(key)+" Files ! ! !")
    fpath=fpath_L[0]
    return fpath
def Split_FPath(FPath):
    FPath_L=FPath.split("/")
    FPath_L.pop(-1)
    Path_L=FPath_L
    Path=""
    for str in Path_L:
        Path=Path+str+"/"
    return Path
def Fluximage(ObsID_L,ObsID_Path='/Volumes/expansion/ObsIDs/', key="evt2"):
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
        os.system("fluximage "+str(Filepath)+" "+str(Outpath)+" psfecf=0.9 binsize=1 clobber=yes")
def Wavdetect(ObsID_L,ObsID_Path='/Volumes/expansion/ObsIDs/', key="broad_thresh"):
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
        os.system("wavdetect "+str(Broad_Thresh_Img_Path)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='1 2 4 8'"+" expfile="+str(Exposure_Map_Path)+" psffile="+str(PSF_Map_Path)+" clobber=yes") #This is a test without the 16 scale
        ##os.system("wavdetect "+str(Broad_Flux_Img_Path)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='1 2 4 8 16'"+" expfile="+str(Exposure_Map_Path)+" psffile="+str(PSF_Map_Path)+" clobber=yes")
        #os.system("wavdetect "+str(Broad_Flux_Img_Path)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='1 2 4 8'"+" expfile="+str(Exposure_Map_Path)+" psffile="+str(PSF_Map_Path)+" clobber=yes") #This is a test without the 16 scale
        ##Input_Filepath=File_Query(ObsID_N,ObsID_Path,key=key)
        ##print("Input_Filepath: ", Input_Filepath)
        #os.system("wavdetect "+str(Input_Filepath)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='2 4 8 16'"+"psffile=default  verbose=1 clobber=yes")
        ##os.system("wavdetect "+str(Input_Filepath)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='2 4 8 16'"+"psffile="+str(PSF_Map_Path)+" clobber=yes")
        #os.system("wavdetect "+str(Input_Filepath)+" outfile="+str(Outfile)+" scellfile="+str(Scellfile)+" imagefile="+str(Imagefile)+" defnbkgfile="+str(Defnbkgfile)+" regfile="+str(Regfile)+" scales='1 2 4 8 16'"+" expfile="+str(Exposure_Map_Path)+" psffile="+str(PSF_Map_Path)+" clobber=yes")
def Test_Main(ObsID_L,ObsID_Path="/Volumes/expansion/ObsID_Test/"):
    for ObsID in ObsID_L:
        """
        Simon's Version
        os.system("dmcopy \"chandra_from_csc/" + obsid + "/primary/*_evt2.fits.gz[sky=region(chandra_from_csc/" + obsid + "/primary/acis" + fov_name + "_fov1.fits.gz[ccd_id=0,1,2,3]),ccd_id=0,1,2,3][energy=300:8000]\" chandra_from_csc/" + obsid + "/primary/" + obsid + "_chips.fits clobber=yes")
        .
        .
        os.system("wavdetect chandra_from_csc/" + obsid + "/primary/" + obsid + "_chips.fits chandra_from_csc/" + obsid + "/primary/" + obsid + "_sources.fits chandra_from_csc/" + obsid + "/primary/" + obsid + "_source_cell.fits chandra_from_csc/" + obsid + "/primary/" + obsid + "_wav_image.fits chandra_from_csc/" + obsid + "/primary/" + obsid + "_background.fits scales='2 4 8 16' regfile='" + obsid+ "_reg.reg' psffile=default verbose=1 clobber=yes")
        """
        ObsID_N=int(ObsID)
        Evt2_Filepath=File_Query(ObsID_N,ObsID_Path)
        print("Evt2_Filepath: ", Evt2_Filepath)
        FOV1_Filepath=File_Query(ObsID_N,ObsID_Path,key="fov1")
        print("FOV1_Filepath: ", FOV1_Filepath)
        Primary_Path=Split_FPath(Evt2_Filepath)
        Exposure_Path=Primary_Path+"exposure_correction/"
        ##Exposure_Path=Primary_Path
        os.system("dmcopy "+"\'"+str(Evt2_Filepath)+"[sky=region("+str(FOV1_Filepath)+"[ccd_id=0,1,2,3]),ccd_id=0,1,2,3][energy=300:8000]"+"\' "+Exposure_Path+str(ObsID)+"_chips.fits clobber=yes")
        #time.sleep(10) #This is a hack and a test
        Fluximage([ObsID],ObsID_Path="/Volumes/expansion/ObsID_Test/",key="chips")
        #time.sleep(10) #This is a hack and a test
        Wavdetect([ObsID],ObsID_Path="/Volumes/expansion/ObsID_Test/",key="chips")

#print(Split_FPath("/Volumes/expansion/ObsIDs/10125/primary/acisf10125N003_evt2.fits.gz"))
##Fluximage([10125],ObsID_Path="/Volumes/expansion/ObsID_Test/")
##Wavdetect([10125],ObsID_Path="/Volumes/expansion/ObsID_Test/")
#13813
Fluximage([13813],ObsID_Path="/Volumes/expansion/ObsID_Test/")
Wavdetect([13813],ObsID_Path="/Volumes/expansion/ObsID_Test/")
##Test_Main([10125])
