from astroquery.ned import Ned
#from ciao_contrib.runtool import *
#from region import *
import numpy as np
import math
import os
os.system("sh ciao_wrapper.sh dmlist 'acisf02014_repro_evt2.fits' cols")

def Background_Finder_3(gname,evtfname,objLfname,n,R):
    """
    gname:-str, Galaxy Name, The name of the galaxy in the form NGC #, For Example 'NGC 3077'
    evtfname:-str, Event File Name, The name of the event file of the observation, For Example 'acisf02076_repro_evt2.fits'
    objLfname:-str, Object List File Name, The name of the object list file which is a list of circluar regions around the X-ray objects. For Example 'ngc3077_ObsID-2076_Source_List_R_Mod_2.txt'
    n:-int, Number of objects, The number of objects in the observation
    R:-float(?) or int, Radius, The radius of the circle used to find the background in pixels
    Returns: BG_Ratio:-float, Background Ratio, The background ratio in number of counts per pixel
             or "None" if a region without an object in it cannot be found
    """
    Obj_L=[]
    Obj_B=True #Obj_B:-bool, Object Boolean, A Boolean statement in regards to if there is no X-ray objects in the area being used to find the background
    BG_R=R # Note: Physical Radius might not be equal to the Pixel Radius
    Num_BG_Pix=math.pi*((BG_R)**2) #Num_BG_Pix:-float or int, the number of pixels in the background test region
    print Num_BG_Pix
    CCD_L=[] # Note: I don't even know if I need this, It's only defined here and never used again I think
    Obj_Shape="" # Note: I don't even know if I need this, It's only defined here and never used again I think
    Objfile=open("/home/asantini/Desktop/Big_Object_Regions/"+str(objLfname),"r")
    #print type(Objfile)
    Objstring=Objfile.read()
    G_Data = Ned.query_object(gname)
    raGC=float(G_Data['RA(deg)']) # raGC:-float, Right Ascension of Galatic Center, The right ascension of the galatic center of the current galaxy in degrees.
    decGC=float(G_Data['DEC(deg)']) #decGC:-float, Declination of Galatic Center, The declination of the galatic center of the current galaxy in degrees.
    Dia_A= Ned.get_table(gname,table='diameters')
    Dia_A2=Dia_A[6]
    Maj=Dia_A2[18]
    Min=Dia_A2[25]
    S_Maj=Maj/2
    dmcoords(infile=str(evtfname),ra=str(raGC), dec=str(decGC), option='cel', verbose=0, celfmt='deg')
    X_Phys=dmcoords.x
    Y_Phys=dmcoords.y
    Chip_ID=dmcoords.chip_id
    print Chip_ID
    print "GC X is ", X_Phys
    print "GC Y is ", Y_Phys
    R_Phys=S_Maj*2.03252032520325
    print "Radius of Galaxy is ", R_Phys
    Gal_V_Shape='circle(' + str(X_Phys) +','+ str(Y_Phys)+','+ str(R_Phys)+')'
    for i in range(0,n):
        Cur_Obj= Objstring.split("\n")[i]
        Obj_L.append(Cur_Obj)
    for c in range(0+BG_R,1025-BG_R):   # c is "x"  #Check Bounds
        for v in range(0+BG_R,1025-BG_R): # v is "y"  #Check Bounds
            #print "         " # Puts a space between objects
            BG_X=c
            BG_Y=v
            #print "Chip x is ",c
            #print "Chip y is ",v
            dmcoords(infile=str(evtfname),chipx=BG_X, chipy=BG_Y, chip_id=Chip_ID, option='chip', verbose=0)
            BG_X_Pix=dmcoords.x
            BG_Y_Pix=dmcoords.y
            print "Background X is ", BG_X_Pix
            print "Background Y is ", BG_Y_Pix
            print "Background R is ", BG_R
            Dis_GC=math.sqrt(((BG_X_Pix-X_Phys)**2)+((BG_Y_Pix-Y_Phys)**2))
            print "Distance to GC is ", Dis_GC
            #print "R_Phys is ", R_Phys
            print "The GC Test is ", Dis_GC-R_Phys-BG_R
            if((Dis_GC-R_Phys-BG_R)>0):
                for Obj_S in Obj_L: #String split X, Y and the R out
                    Cur_X=Obj_S.split(",")[0]
                    Cur_X_R=Cur_X.split('(')[1]
                    Cur_Y=Obj_S.split(",")[1]
                    Cur_R=Obj_S.split(",")[2]
                    Cur_R_R=Cur_R.split(')')[0]
                    Cur_X_N=float(Cur_X_R)
                    Cur_Y_N=float(Cur_Y)
                    Cur_R_N=float(Cur_R_R)
                    Dis_Obj=math.sqrt(((BG_X_Pix-Cur_X_N)**2)+((BG_Y_Pix-Cur_Y_N)**2))
                    #print "Distance to Object is ", Dis_Obj
                    #print "Cur_R_N is ", Cur_R_N
                    #print "BG_R is ", BG_R
                    #print "The Obj Test is ", Dis_Obj-Cur_R_N-BG_R
                    if((Dis_Obj-Cur_R_N-BG_R)<=0):
                        Obj_B=False
                if(Obj_B==True):
                    Dm_Out=dmlist(infile=str(evtfname)+"[sky=circle("+str(BG_X_Pix)+","+str(BG_Y_Pix)+","+str(BG_R)+")]", opt='counts', outfile="", verbose=2) #dmlist "acis_evt2.fits[sky=rotbox(4148,4044,8,22,44.5)]" counts
                    Num_Counts_S=Dm_Out.split('\n')[9]
                    Num_Counts=float(Num_Counts_S)
                    BG_Ratio=Num_Counts/Num_BG_Pix
                    return BG_Ratio
    return "None"

    #Need for figure out how to select where the test circle should be, needs to be on a CCD, (back and front Illiminated?)
os.system("ciao_wrapper.sh dmlist some_file_name cols")




#Background_Finder_3('NGC 3077','acisf02076_repro_evt2.fits','ngc3077_ObsID-2076_Source_List_R_Mod_2.txt',16,10)
