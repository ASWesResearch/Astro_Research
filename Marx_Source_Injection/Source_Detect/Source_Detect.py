import os
from os import system
import sys
import glob
import re
from ciao_contrib.runtool import * #Imports ciao tools into python
import ciao_contrib.runtool as rt
import time
import logging

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

def Crop_Image(X_Low, X_High, Y_Low, Y_High, Evt2_Fpath, Outfile):
    #Command='dmcopy "'+str(Evt2_Fpath)+'[EVENTS][bin x=4050:4300:1,y=4050:4300:1]" '+str(Outfile)
    Command='dmcopy "'+str(Evt2_Fpath)+'[EVENTS][bin x='+str(X_Low)+':'+str(X_High)+':1,y='+str(Y_Low)+':'+str(Y_High)+':1]" '+str(Outfile)
    #print("Command: ", Command)
    os.system(Command)

def Crop_Image_Centered(X, X_Length, Y, Y_Length, Evt2_Fpath, Outfile):
    X_Low=X-(X_Length/2.0)
    X_High=X+(X_Length/2.0)
    Y_Low=Y-(Y_Length/2.0)
    Y_High=Y+(Y_Length/2.0)
    Crop_Image(X_Low, X_High, Y_Low, Y_High, Evt2_Fpath=Evt2_Fpath, Outfile=Outfile)

def Fluximage(Filepath, Outpath):
    """
    with rt.new_pfiles_environment(ardlib=True):
        with new_tmpdir() as tmpdir:
    """
    #os.system("fluximage "+str(Filepath)+" "+str(Outpath)+" psfecf=0.9 binsize=1 clobber=yes verbose=1")
    os.system("fluximage "+str(Filepath)+" "+str(Outpath)+" psfecf=0.9 binsize=1 asolfile='0_1_78_8E-2_1_asol1.fits' badpixfile='NONE' maskfile='NONE' clobber=yes verbose=0")

def Make_PSF_Map(Filepath, Outpath):
    os.system("mkpsfmap "+str(Filepath)+" "+str(Outpath)+" 1.4 ecf=0.5 clobber=yes")

def Wavdetect(Filepath, Outpath, PSF_Map_Path, Regfile):
    ##Wavdetect_Command="wavdetect "+str(Filepath)+" outfile="+str(Outpath)+" scellfile=source_cell.fits imagefile=image.fits defnbkgfile=background.fits regfile="+str(Regfile)+" scales='1 2 4 8' psffile="+str(PSF_Map_Path)+" clobber=yes verbose=1"
    Wavdetect_Command="wavdetect "+str(Filepath)+" outfile="+str(Outpath)+" scellfile=source_cell.fits imagefile=image.fits defnbkgfile=background.fits scales='1 2 4 8' psffile="+str(PSF_Map_Path)+" clobber=yes verbose=1" #Note: Wavdetect is 3 seconds faster without creating the ASCII file.
    os.system(Wavdetect_Command) #This is a test without the 16 scale




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
