import numpy as np
import scipy.special
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
from PSF_Size_Calc import PSF_Size_Calc

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

def CEL_to_CHIP_Convert(RA,Dec,Empty_Filepath="../Required_Files_Generated/empty.fits", Empty_Coords_Gen_Bool=False):
    if(Empty_Coords_Gen_Bool):
        Empty_Coords_Generator()
    with rt.new_pfiles_environment(ardlib=True):
        Dmcoords=rt.make_tool("dmcoords")
        Dmcoords(infile=str(Empty_Filepath), ra=float(RA), dec=float(Dec), option='cel', verbose=0, celfmt='deg')
        Chip_X=Dmcoords.chipx
        Chip_Y=Dmcoords.chipy
        Chip_ID=Dmcoords.chip_id
    return Chip_X, Chip_Y, Chip_ID

'''
def Fluximage(Filepath, Outpath):
    """
    with rt.new_pfiles_environment(ardlib=True):
        with new_tmpdir() as tmpdir:
    """
    #os.system("fluximage "+str(Filepath)+" "+str(Outpath)+" psfecf=0.9 binsize=1 clobber=yes verbose=1")
    os.system("fluximage "+str(Filepath)+" "+str(Outpath)+" psfecf=0.9 binsize=1 asolfile='0_1_78_8E-2_1_asol1.fits' badpixfile='NONE' maskfile='NONE' clobber=yes verbose=0")
'''

def Make_Expsoure_Map(Outpath, Source_Path, Source_Reprojected_Path, Aspect_Path, Chip_X, Chip_Y, Chip_ID, X, Y, S=128):

    Pixel_X=1024-Chip_X
    Pixel_Y=1024-Chip_Y

    Pixel_X_Low=int(Pixel_X-(S/2.0))
    Pixel_X_High=int(Pixel_X+(S/2.0))
    Pixel_Y_Low=int(Pixel_Y-(S/2.0))
    Pixel_Y_High=int(Pixel_Y+(S/2.0))


    Pixel_X_Low=int(Pixel_X_Low-16)
    Pixel_X_High=int(Pixel_X_High+16)
    Pixel_Y_Low=int(Pixel_Y_Low-16)
    Pixel_Y_High=int(Pixel_Y_High+16)

    """
    Chip_X_Low=int(Chip_X-(S/2.0)-16) #Note: 16 pixel buffer added
    Chip_X_High=int(Chip_X+(S/2.0)+16) #Note: 16 pixel buffer added
    Chip_Y_Low=int(Chip_Y-(S/2.0)-16) #Note: 16 pixel buffer added
    Chip_Y_High=int(Chip_Y+(S/2.0)+16) #Note: 16 pixel buffer added
    """

    #"x0:x1:#nx,y0:y1:#n2"
    #pixelgrid="1:1024:#1024,1:1024:#1024"
    ##Pixelgrid_Str=str(Chip_X_Low)+":"+str(Chip_X_High)+":#"+str(int(S))+","+str(Chip_Y_Low)+":"+str(Chip_Y_High)+":#"+str(int(S))
    #Pixelgrid_Str="1:1024:#1024,1:1024:#1024"
    #Pixelgrid_Str="256:512:#512,256:512:#512"
    ##Pixelgrid_Str="56:968:#912,56:968:#912" #Note: Corner visible!
    ##Pixelgrid_Str="56:998:#942,56:968:#912" #Note: Corner moved down
    ##Pixelgrid_Str="56:968:#912,56:998:#942" #Note: Corner moved left
    ##Pixelgrid_Str="56:938:#882,56:968:#912" #Note: Coner moved up?
    ##Pixelgrid_Str="938:968:#30,968:998:#30" #Note: Square visible on left side
    ##Pixelgrid_Str="880:1008:#128,880:1008:#128" #Note: Square almost covers whole 128x128 image
    ##Pixelgrid_Str="890:998:#108,890:998:#108"  #Note: Square is almost centered (slightly top left) and smaller
    ##Pixelgrid_Str="864:1024:#160,864:1024:#160" #Note: Square covers the whole 128x128 image!!!
    ##Pixelgrid_Str=str(Pixel_X_Low)+":"+str(Pixel_X_High)+":#"+str(int(S))+","+str(Pixel_Y_Low)+":"+str(Pixel_Y_High)+":#"+str(int(S)) #Note: This works for the [80,80] case! Maybe all of them!
    Pixelgrid_Str=str(Pixel_X_Low)+":"+str(Pixel_X_High)+":#"+str(int(S+32))+","+str(Pixel_Y_Low)+":"+str(Pixel_Y_High)+":#"+str(int(S+32)) #Note: 16 pixel buffer added #Bug Here! The expsosure map is inncorrect if the insturment map is larger than the exposure map!!! #None: This isn't a bug.
    ##print("Pixelgrid_Str: ", Pixelgrid_Str)
    X_Low=float(X-(S/2.0))
    X_High=float(X+(S/2.0))
    Y_Low=float(Y-(S/2.0))
    Y_High=float(Y+(S/2.0))
    #xygrid="3094.5:5050.3:#256,2042.0:5320.0:#512"
    XYgrid_Str=str(X_Low)+":"+str(X_High)+":#"+str(int(S))+","+str(Y_Low)+":"+str(Y_High)+":#"+str(int(S))
    #XYgrid_Str=str(2800)+":"+str(5000)+":#"+str(int(2200))+","+str(3000)+":"+str(5200)+":#"+str(int(2200))
    ##XYgrid_Str="4081.0:4209.0:#128,4071.0:4199.0:#128"
    #XYgrid_Str=str(X_Low)+":"+str(X_High)+":#"+str(int(S/2))+","+str(Y_Low)+":"+str(Y_High)+":#"+str(int(S/2))
    ##print("XYgrid_Str: ", XYgrid_Str)
    ##print("X,Y: ", X,Y)
    Bash_Command="bash Bash_Scripts/Make_Expsoure_Map.sh "+str(Outpath)+" "+str(Pixelgrid_Str)+" "+str(Source_Reprojected_Path)+" "+str(Aspect_Path)+" "+str(XYgrid_Str)+" "+str(Source_Path)+" "+str(Chip_ID)
    #Bash_Command="bash -x Bash_Scripts/Make_Expsoure_Map.sh "+str(Outpath)+" "+str(Pixelgrid_Str)+" "+str(Source_Reprojected_Path)+" "+str(Aspect_Path)+" "+str(XYgrid_Str)+" "+str(Source_Path)+" "+str(Chip_ID)
    ##print("Bash_Command: ", Bash_Command)
    #mkarf detsubsys="ACIS-7;uniform;bpmask=0"
    ##asphist infile=$4 outfile=$1_blank_sky.asphist evtfile="$3[ccd_id=3]" clobber=yes
    os.system(Bash_Command)

def Fluximage(Outpath, Source_Path, Source_Reprojected_Path, Aspect_Path, Cur_Postage_Stamp_Outpath):
    """
    with rt.new_pfiles_environment(ardlib=True):
        with new_tmpdir() as tmpdir:
    """
    #os.system("fluximage "+str(Filepath)+" "+str(Outpath)+" psfecf=0.9 binsize=1 clobber=yes verbose=1")
    os.system("fluximage "+str(Source_Reprojected_Path)+" "+str(Outpath)+" psfecf=0.9 binsize=1 asolfile='"+str(Aspect_Path)+"' badpixfile='NONE' maskfile='NONE' xygrid="+str(Cur_Postage_Stamp_Outpath)+" cleanup=no clobber=yes verbose=0")

def Make_PSF_Map(Filepath, PSF_Outpath, Outpath, Background_Float, Counts):
    if((float(Background_Float)==0.0) and (int(Counts)==0)):
        #print("Make_PSF_Map 0 Counts and Background Test")
        return
    ##os.system("mkpsfmap "+str(Filepath)+" "+str(Outpath)+" 1.4 ecf=0.9 clobber=yes")
    Bash_Command="bash Bash_Scripts/Make_PSF_Map.sh "+str(Filepath)+" "+str(PSF_Outpath)+" "+Outpath #BUG HERE!!! The ECF should be 2.3 keV which coresponds to the broad band Effective Energy used by default in fluximage!!! #Note: Bug Fixed
    #print(Bash_Command)
    os.system(Bash_Command)

def Wavdetect(Filepath, Outpath, PSF_Map_Path, Background_Float, Counts, Key="", Input_Background_Bool=False):
    if((float(Background_Float)==0.0) and (int(Counts)==0)):
        print("Wavdetect 0 Counts and Background Test")
        return
    ##Wavdetect_Command="wavdetect "+str(Filepath)+" outfile="+str(Outpath)+" scellfile=source_cell.fits imagefile=image.fits defnbkgfile=background.fits regfile="+str(Regfile)+" scales='1 2 4 8' psffile="+str(PSF_Map_Path)+" clobber=yes verbose=1"
    Outfile=Outpath+Key+"_Wavdetect.fits"
    Scellfile=Outpath+Key+"_source_cell.fits"
    Imagefile=Outpath+Key+"_image.fits"
    Defnbkgfile=Outpath+Key+"_background.fits"
    Regfile=Outpath+Key+".reg"
    #Bash_Command="bash Bash_Scripts/Wavdetect.sh "+str(Filepath)+" "+str(Outfile)+" "+str(Outpath)+" "+str(PSF_Map_Path)
    ##Bash_Command="bash Bash_Scripts/Wavdetect.sh "+str(Filepath)+" "+str(Outfile)+" "+str(Outpath)+" "+str(PSF_Map_Path)+" "+str(Regfile)
    if(Input_Background_Bool):
        Input_Background_File=Outpath+"_background.fits"
        Bash_Command="bash Bash_Scripts/Wavdetect.sh "+str(Filepath)+" "+str(Outfile)+" "+str(Outpath)+" "+str(PSF_Map_Path)+" "+str(Regfile)+" "+str(Scellfile)+" "+str(Imagefile)+" "+str(Defnbkgfile)+" "+str(Input_Background_File)
    else:
        Bash_Command="bash Bash_Scripts/Wavdetect.sh "+str(Filepath)+" "+str(Outfile)+" "+str(Outpath)+" "+str(PSF_Map_Path)+" "+str(Regfile)+" "+str(Scellfile)+" "+str(Imagefile)+" "+str(Defnbkgfile)+" "+str("NONE")
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

def Save_Detection_Bool(Filepath, X_Expected, Y_Expected, Outpath, Background_Float, Counts, Tolarance=17, Key=""):
    if((float(Background_Float)==0.0) and (int(Counts)==0)):
        #print("Save_Detection_Bool 0 Counts and Background Test")
        return
    Outfile=Outpath+Key+"_Detection_Bool.txt"
    Outfile_Amount=Outpath+Key+"_Detection_Amount.txt"
    Source_Detection_Bool=Source_Detection_Bool_Calc(Filepath, X_Expected, Y_Expected, Tolarance=Tolarance)[0]
    Source_Detection_Amount=Source_Detection_Bool_Calc(Filepath, X_Expected, Y_Expected, Tolarance=Tolarance)[1]
    Command='echo "'+str(int(Source_Detection_Bool))+'" > '+str(Outfile)
    #print(Command)
    os.system(Command)
    Command_Amount='echo "'+str(int(Source_Detection_Amount))+'" > '+str(Outfile_Amount)
    #print(Command_Amount)
    os.system(Command_Amount)

def Fac(n):
    return scipy.special.factorial(n)

def BACKSCAL_Calc(Phi, Theta, S=128, PSF_Radius=None): #Bug Here! This is not the correct way to calculate BACKSCAL!!! #Bug Fixed!
    R_Max=S/2.0
    if(PSF_Radius==None):
        PSF_Radius_Pix=PSF_Size_Calc.Calc_PSF_Pixel_Size(Phi, Theta, energy=2.3, ecf=0.90)
    M=np.floor(R_Max/PSF_Radius_Pix)
    if(M>4):
        M=4.0
    BACKSCAL=(M**2.0)-1.0
    return M,BACKSCAL

def Ideal_Type_I_Parameters_Calc(Phi, Theta, Background_Float, Counts):
    #M,BACKSCAL=BACKSCAL_Calc(Phi, Theta, PSF_Radius=PSF_Radius_Pix)
    M,BACKSCAL=BACKSCAL_Calc(Phi, Theta)
    PSF_Radius_Pix=PSF_Size_Calc.Calc_PSF_Pixel_Size(Phi, Theta, energy=2.3, ecf=0.90)
    Source_Area=np.pi*(PSF_Radius_Pix**2.0)
    Source_Background_Counts=Background_Float*Source_Area
    S=int(Counts+Source_Background_Counts)
    Background_Area=Source_Area*BACKSCAL
    B=int(Background_Float*Background_Area)
    return S,B,BACKSCAL,Background_Area

def Empirical_Type_I_Parameters_Calc(Evtfpath, Phi, Theta, Target_X, Target_Y):
    PSF_Radius_Pix=PSF_Size_Calc.Calc_PSF_Pixel_Size(Phi, Theta, energy=2.3, ecf=0.90)
    #M,BACKSCAL=BACKSCAL_Calc(Phi, Theta, PSF_Radius=PSF_Radius_Pix)
    M,BACKSCAL=BACKSCAL_Calc(Phi, Theta)
    with rt.new_pfiles_environment(ardlib=True):
        Dmcoords=rt.make_tool("dmlist")
        Dm_Out=dmlist(infile=str(Evtfpath)+"[sky=circle("+str(Target_X)+","+str(Target_Y)+","+str(PSF_Radius_Pix)+")]", opt='counts', outfile="", verbose=0)
        #print("Dm_Out: ", Dm_Out)
        #Num_Counts_S=Dm_Out.split('\n')[9]
        Num_Counts_S=Dm_Out
        S=float(Num_Counts_S)
    with rt.new_pfiles_environment(ardlib=True):
        Dmcoords=rt.make_tool("dmlist")
        Dm_Out_Full=dmlist(infile=str(Evtfpath)+"[sky=circle("+str(Target_X)+","+str(Target_Y)+","+str(M*PSF_Radius_Pix)+")]", opt='counts', outfile="", verbose=0)
        #Num_Counts_Full_S=Dm_Out_Full.split('\n')[9] #Num_Counts_Full_S:-str,The number of counts in the background cirlce as a string
        Num_Counts_Full_S=Dm_Out_Full
        Num_Counts_Full=float(Num_Counts_Full_S)
        #print("Num_Counts_Full: ", Num_Counts_Full)
    B=Num_Counts_Full-S
    S=int(S)
    B=int(B)
    return S,B,BACKSCAL

def Empirical_Isolated_Counts_Calc(Evtfpath, Phi, Theta, Target_X, Target_Y):
    PSF_Radius_Pix=PSF_Size_Calc.Calc_PSF_Pixel_Size(Phi, Theta, energy=2.3, ecf=0.90)
    with rt.new_pfiles_environment(ardlib=True):
        Dmcoords=rt.make_tool("dmlist")
        Dm_Out=dmlist(infile=str(Evtfpath)+"[sky=circle("+str(Target_X)+","+str(Target_Y)+","+str(PSF_Radius_Pix)+")]", opt='counts', outfile="", verbose=0)
        Num_Counts_S=Dm_Out
        S=float(Num_Counts_S)
    S=int(S)
    return S


def Type_I_Calc(S,B,BACKSCAL=4.0):
    N=S+B
    p=(1.0/(1.0+BACKSCAL))
    P_B=0
    for X in range(S,N):
        Cur=(Fac(N)/(Fac(X)*Fac(N-X)))*(p**X)*((1-p)**(N-X))
        P_B=P_B+Cur
    return P_B

def Ideal_Type_I_Calc(Phi, Theta, Background_Float, Counts, Parameter_Tuple=None):
    if(Parameter_Tuple==None):
        S,B,BACKSCAL,Background_Area=Ideal_Type_I_Parameters_Calc(Phi, Theta, Background_Float, Counts)
    else:
        S=Parameter_Tuple[0]
        B=Parameter_Tuple[1]
        BACKSCAL=Parameter_Tuple[2]
    P_B=Type_I_Calc(S,B,BACKSCAL=BACKSCAL)
    return P_B

def Empirical_Type_I_Calc(Evtfpath, Phi, Theta, Target_X, Target_Y, Background_Float, Counts, Parameter_Tuple=None):
    if(Parameter_Tuple==None):
        S,B,BACKSCAL=Empirical_Type_I_Parameters_Calc(Evtfpath, Phi, Theta, Target_X, Target_Y)
    else:
        S=Parameter_Tuple[0]
        B=Parameter_Tuple[1]
        BACKSCAL=Parameter_Tuple[2]
    P_B=Type_I_Calc(S,B,BACKSCAL=BACKSCAL)
    return P_B

def Type_II_Calc(P_B, P_B_Thresh=0.007):
    Detection_Bool=(float(P_B)<float(P_B_Thresh))
    return Detection_Bool

def Save_Type_II_Detection_Bool(P_B, Outpath, P_B_Thresh=0.007,Key="Type_II"):
    Outfile=Outpath+Key+"_Detection_Bool.txt"
    Outfile_Amount=Outpath+Key+"_Detection_Amount.txt"
    Source_Detection_Bool=Type_II_Calc(P_B, P_B_Thresh=0.007)
    Command='echo "'+str(int(Source_Detection_Bool))+'" > '+str(Outfile)
    #print(Command)
    os.system(Command)

def Save_Parameter(Input, Outpath, Key="", Suffix=".txt"):
    #Outfile=Outpath+Key+".txt"
    Outfile=Outpath+Key+Suffix
    Command='echo "'+str(Input)+'" > '+str(Outfile)
    #print(Command)
    os.system(Command)

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
    #Background_Str_L=[Background_Str_L[0]] #For Testing
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
            #Cur_Counts_L=[Cur_Counts_L[0]] #For Testing
            #print("Cur_Counts_L: ", Cur_Counts_L)
            Cur_RA,Cur_Dec=Source_Generator.MSC_to_CEL_Convert(Cur_Theta,Cur_Phi)
            Cur_Chip_X, Cur_Chip_Y, Cur_Chip_ID=Source_Generator.MSC_to_Chip_Convert(Cur_Theta,Cur_Phi)
            for Cur_Counts in Cur_Counts_L:
                #Number_of_Sources=Number_of_Sources+1
                for Cur_Background in Background_Str_L:
                    Cur_Background_Float=float(Cur_Background)
                    Number_of_Sources=Number_of_Sources+1
                    for Run_Count in Run_Count_L:
                        Run_Index=int(Run_Count-1)
                        Number_of_Runs=Number_of_Runs+1
                        Cur_Outpath="./Wavdetect_Outputs/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)
                        Cur_Postage_Stamp_Outpath="../Source_Reproject/Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Postage_Stamp.fits"
                        Cur_Postage_Stamp_No_Background_Outpath="../Source_Reproject/Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_No_Background_Postage_Stamp.fits"
                        Cur_Postage_Stamp_No_Source_Outpath="../Source_Reproject/Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_No_Source_Postage_Stamp.fits"
                        Cur_Postage_Stamp_Original_Source_Outpath="../Source_Reproject/Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Original_Source_Postage_Stamp.fits"
                        Cur_PSF_Outpath=Cur_Outpath+"_PSF.fits"
                        Cur_Postage_Stamp_Coords=Postage_Stamp_Coords_L[Run_Index]
                        Cur_Wavdetect_Outfile=Cur_Outpath+"_Wavdetect.fits"
                        Cur_Wavdetect_No_Background_Outfile=Cur_Outpath+"_No_Background_Wavdetect.fits"
                        Cur_Wavdetect_No_Background_Fixed_Outfile=Cur_Outpath+"_No_Background_Fixed_Wavdetect.fits"
                        Cur_Wavdetect_No_Source_Outfile=Cur_Outpath+"_No_Source_Wavdetect.fits"
                        Cur_Reproject_Outpath="../Source_Reproject/Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Reprojected.fits"
                        Cur_Source_Aspect_Path="../Source_Generator/Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_asol1.fits"
                        Cur_Source_Path="../Source_Generator/Marx_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+".fits"
                        Cur_Injected_Outpath="../Source_Reproject/Injected_Sources/"+str(Cur_Phi)+"/"+str(Cur_Theta)+"/"+str(Cur_Counts)+"/"+str(Cur_Background)+"/"+str(Run_Count)+"/"+str(Cur_Phi)+"_"+str(Cur_Theta)+"_"+str(Cur_Counts)+"_"+str(Cur_Background)+"_"+str(Run_Count)+"_Injected.fits"
                        ##Cur_Run_L=[Cur_Outpath, Cur_Postage_Stamp_Outpath, Cur_PSF_Outpath, Cur_Wavdetect_Outfile, Cur_Postage_Stamp_Coords, Cur_Background_Float, Cur_Counts, Cur_Postage_Stamp_No_Background_Outpath, Cur_Postage_Stamp_No_Source_Outpath, Cur_Wavdetect_No_Background_Outfile, Cur_Wavdetect_No_Source_Outfile, Cur_Postage_Stamp_Original_Source_Outpath, Cur_Reproject_Outpath, Cur_Source_Aspect_Path, Cur_Source_Path, Cur_Chip_ID]
                        Cur_Run_L=[Cur_Outpath, Cur_Postage_Stamp_Outpath, Cur_PSF_Outpath, Cur_Wavdetect_Outfile, Cur_Postage_Stamp_Coords, Cur_Background_Float, Cur_Counts, Cur_Postage_Stamp_No_Background_Outpath, Cur_Postage_Stamp_No_Source_Outpath, Cur_Wavdetect_No_Background_Outfile, Cur_Wavdetect_No_Background_Fixed_Outfile, Cur_Wavdetect_No_Source_Outfile, Cur_Postage_Stamp_Original_Source_Outpath, Cur_Reproject_Outpath, Cur_Source_Aspect_Path, Cur_Source_Path, Cur_Chip_ID, Cur_Phi, Cur_Theta, Cur_Injected_Outpath]
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
    Background_Float=Input_L[5]
    Counts=Input_L[6]
    Postage_Stamp_No_Background_Outpath=Input_L[7]
    Postage_Stamp_No_Source_Outpath=Input_L[8]
    Wavdetect_No_Background_Outfile=Input_L[9]
    Wavdetect_No_Background_Fixed_Outfile=Input_L[10]
    Wavdetect_No_Source_Outfile=Input_L[11]
    Postage_Stamp_Original_Source_Outpath=Input_L[12]
    Reproject_Outpath=Input_L[13]
    Source_Aspect_Path=Input_L[14]
    Source_Path=Input_L[15]
    Chip_ID=Input_L[16]
    Phi=Input_L[17]
    Theta=Input_L[18]
    Injected_Outpath=Input_L[19]
    #Postage_Stamp_Coords[0]=[[0, 0], [80.0, 80.0], [4145.0, 4135.0], ['359.9933716666962', '0.005261666616669011']]
    Target_Chip_Coords=Postage_Stamp_Coords[1]
    Chip_X=Target_Chip_Coords[0]
    Chip_Y=Target_Chip_Coords[1]
    Target_Physical_Coords=Postage_Stamp_Coords[2]
    Target_X=Target_Physical_Coords[0]
    Target_Y=Target_Physical_Coords[1]


    Make_Directory(Outpath)
    Make_PSF_Map(Postage_Stamp_Original_Source_Outpath, PSF_Outpath, Outpath, Background_Float, Counts)
    Make_Expsoure_Map(Outpath, Source_Path, Reproject_Outpath, Source_Aspect_Path, Chip_X, Chip_Y, Chip_ID, Target_X, Target_Y)
    #Fluximage(Outpath, Source_Path, Reproject_Outpath, Source_Aspect_Path, Postage_Stamp_Outpath)
    Wavdetect(Postage_Stamp_Outpath, Outpath, PSF_Outpath, Background_Float, Counts)
    ##Save_Detection_Bool(Wavdetect_Outfile, Target_X, Target_Y, Outpath, Background_Float, Counts)
    Source_Detection_Bool, Source_Detection_Amount=Source_Detection_Bool_Calc(Wavdetect_Outfile, Target_X, Target_Y)


    M,BACKSCAL=BACKSCAL_Calc(Phi, Theta)

    ##Save_Parameter(M, Outpath, Key="_Background_Radius_Multiplier")
    ##Save_Parameter(BACKSCAL, Outpath, Key="_BACKSCAL")
    Ideal_Parameter_Tuple=Ideal_Type_I_Parameters_Calc(Phi, Theta, Background_Float, Counts)
    Background_Area=Ideal_Parameter_Tuple[3]
    #Ideal_Parameter_Tuple=(Ideal_Parameter_Tuple[0],Ideal_Parameter_Tuple[1],Ideal_Parameter_Tuple[2])
    P_B_Ideal=Ideal_Type_I_Calc(Phi, Theta, Background_Float, Counts, Parameter_Tuple=Ideal_Parameter_Tuple)

    ##Save_Parameter(P_B_Ideal, Outpath, Key="_P_B_Ideal")

    ##Save_Type_II_Detection_Bool(P_B_Ideal, Outpath ,Key="_Type_II_Ideal")
    Ideal_Type_II_Source_Detection_Bool=Type_II_Calc(P_B_Ideal)


    Empirical_Parameter_Tuple=Empirical_Type_I_Parameters_Calc(Injected_Outpath, Phi, Theta, Target_X, Target_Y)

    ##Save_Parameter(Empirical_Parameter_Tuple[0], Outpath, Key="_Empirical_Raw_Counts")
    ##Save_Parameter(Empirical_Parameter_Tuple[1], Outpath, Key="_Empirical_Background_Counts")

    #Empirical_Enclosed_Source_Counts=Empirical_Type_I_Parameters_Calc(Reproject_Outpath, Phi, Theta, Target_X, Target_Y)[0]
    Empirical_Enclosed_Source_Counts=Empirical_Isolated_Counts_Calc(Reproject_Outpath, Phi, Theta, Target_X, Target_Y)

    ##Save_Parameter(Empirical_Enclosed_Source_Counts, Outpath, Key="_Empirical_Enclosed_Source_Counts")

    Empirical_Background_Counts=Empirical_Parameter_Tuple[1]
    Empirical_Background=float(Empirical_Background_Counts)/float(Background_Area)

    ##Save_Parameter(Empirical_Background, Outpath, Key="_Empirical_Background")


    P_B_Empirical=Empirical_Type_I_Calc(Postage_Stamp_Outpath, Phi, Theta, Target_X, Target_Y, Background_Float, Counts, Parameter_Tuple=Empirical_Parameter_Tuple)

    ##Save_Parameter(P_B_Empirical, Outpath, Key="_P_B_Empirical")

    ##Save_Type_II_Detection_Bool(P_B_Empirical, Outpath ,Key="_Type_II_Empirical")
    Empirical_Type_II_Source_Detection_Bool=Type_II_Calc(P_B_Empirical)


    if((float(Background_Float)>0) and (int(Counts)>0)):
        ####No Background####
        Wavdetect(Postage_Stamp_No_Background_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Background")
        ##Save_Detection_Bool(Wavdetect_No_Background_Outfile, Target_X, Target_Y, Outpath, Background_Float, Counts, Key="_No_Background")
        Source_Detection_Bool_No_Background, Source_Detection_Amount_No_Background=Source_Detection_Bool_Calc(Wavdetect_No_Background_Outfile, Target_X, Target_Y)

        Wavdetect(Postage_Stamp_No_Background_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Background_Fixed", Input_Background_Bool=True)
        ##Save_Detection_Bool(Wavdetect_No_Background_Fixed_Outfile, Target_X, Target_Y, Outpath, Background_Float, Counts, Key="_No_Background_Fixed")
        Source_Detection_Bool_No_Background_Fixed, Source_Detection_Amount_No_Background_Fixed=Source_Detection_Bool_Calc(Wavdetect_No_Background_Fixed_Outfile, Target_X, Target_Y)

        ####No Source####
        ##Wavdetect(Postage_Stamp_No_Source_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Source")
        Wavdetect(Postage_Stamp_No_Source_Outpath, Outpath, PSF_Outpath, Background_Float, Counts, Key="_No_Source", Input_Background_Bool=True)
        ##Save_Detection_Bool(Wavdetect_No_Source_Outfile, Target_X, Target_Y, Outpath, Background_Float, Counts, Key="_No_Source")
        Source_Detection_Bool_No_Source, Source_Detection_Amount_No_Source=Source_Detection_Bool_Calc(Wavdetect_No_Source_Outfile, Target_X, Target_Y)


        #Outfile_Str=str(Source_Detection_Bool)+","+str(Source_Detection_Amount)+","+str(Source_Detection_Bool_No_Background)+","+str(Source_Detection_Amount_No_Background)+","+str(Source_Detection_Bool_No_Background_Fixed)+","+str(Source_Detection_Amount_No_Background_Fixed)+","+str(Source_Detection_Bool_No_Source)+","+str(Source_Detection_Amount_No_Source)+","+str(M)+","+str(BACKSCAL)+","+str(Background_Area)+","+str(P_B_Ideal)+","+str(Ideal_Type_II_Source_Detection_Bool)+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(Empirical_Background)+","+str(P_B_Empirical)+","+str(Empirical_Type_II_Source_Detection_Bool)
        Outfile_Str=str(int(Source_Detection_Bool))+","+str(Source_Detection_Amount)+","+str(int(Source_Detection_Bool_No_Background))+","+str(Source_Detection_Amount_No_Background)+","+str(int(Source_Detection_Bool_No_Background_Fixed))+","+str(Source_Detection_Amount_No_Background_Fixed)+","+str(int(Source_Detection_Bool_No_Source))+","+str(Source_Detection_Amount_No_Source)+","+str(M)+","+str(BACKSCAL)+","+str(np.round(Background_Area,5))+","+str(np.round(P_B_Ideal,5))+","+str(int(Ideal_Type_II_Source_Detection_Bool))+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(np.round(Empirical_Background,5))+","+str(np.round(P_B_Empirical,5))+","+str(int(Empirical_Type_II_Source_Detection_Bool))
    else:
        #Outfile_Str=str(Source_Detection_Bool)+","+str(Source_Detection_Amount)+","+","+","+","+","+","+","+str(M)+","+str(BACKSCAL)+","+str(Background_Area)+","+str(P_B_Ideal)+","+str(Ideal_Type_II_Source_Detection_Bool)+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(Empirical_Background)+","+str(P_B_Empirical)+","+str(Empirical_Type_II_Source_Detection_Bool)
        Outfile_Str=str(int(Source_Detection_Bool))+","+str(Source_Detection_Amount)+","+","+","+","+","+","+","+str(M)+","+str(BACKSCAL)+","+str(np.round(Background_Area,5))+","+str(np.round(P_B_Ideal,5))+","+str(int(Ideal_Type_II_Source_Detection_Bool))+","+str(Empirical_Enclosed_Source_Counts)+","+str(Empirical_Background_Counts)+","+str(np.round(Empirical_Background,5))+","+str(np.round(P_B_Empirical,5))+","+str(int(Empirical_Type_II_Source_Detection_Bool))

    #Save_Parameter(P_B_Ideal, Outpath, Key="_P_B_Ideal")
    Outfile_Header="SDB,SDA,SDBNB,SDANB,SDBNBF,SDANBF,SDBNS,SDANS,M,BACKSCAL,BA,PBI,T2I,EEC,EEBC,EB,PBE,T2E\n"
    Outfile_Str_Merged=Outfile_Header+Outfile_Str
    Save_Parameter(Outfile_Str_Merged, Outpath, Key="_Standard_Outputs", Suffix=".csv")




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
##print(Source_Detect_Big_Input_Generator())
#[80.0, 80.0], [4145.0, 4135.0]
#Make_Expsoure_Map(80.0, 80.0, 4145.0, 4135.0, S=128)
#print(CEL_to_CHIP_Convert(359.927781967,0.066895244))
##print(Ideal_Type_I_Calc(0, 5, 0.03, 20, BACKSCAL=4.0))
#print(Ideal_Type_I_Calc(0, 5, 0.03, 3, BACKSCAL=4.0))
#print(BACKSCAL_Calc(0, 0))
#print(BACKSCAL_Calc(0, 10))
Source_Detect_Generator_Driver()
