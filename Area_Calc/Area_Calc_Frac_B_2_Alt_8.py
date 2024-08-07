from ciao_contrib.runtool import *
from region import *
#from paramio import *
#from astroquery.ned import Ned
from astroquery.ipac.ned import Ned
import numpy as np
import os
from os import system
import sys
from astropy.io.fits import Header
from astropy.io import fits
import pandas as pd
#import subprocess
#subprocess.call("pset dmkeypar mode='hl'")
dir = os.path.dirname(__file__)
path=os.path.realpath('../')
sys.path.append(os.path.abspath(path))
from Galaxy_Name_Reducer import Galaxy_Name_Reducer
from D25_Finder import D25_Finder

def Area_Calc_Frac_B_2_Alt_2(gname,evtfpath,polyfpath,rchange=121.95121955,B=1,D25_Steps_Bool=False,Reasonable_FOV_Bool=True,Fnamekey=""): #NEED to finish this code, Check to see if the radius is increaing correctly and write outputs to a file, Also the evt 2 filename should be a event 2 filepath
    #This is the latest version, 4/20/18
    """
    gname:-str, Galaxy Name, The name of the galaxy in the form NGC #, For Example 'NGC 3077'
    evtfpath:-str, Event File Path, The path of the event file of the observation, For Example '/example_path/acisf02076_repro_evt2.fits'
    ployfname:-str, PolyFileName, The filename of the simple_region_modifed file as a string
    rchange:-int(float?), Radius Change, The change in radius from one area cirlce to another area cirlce in pixels, must equal one arcminute in pixels (1 arcmin= 121.95121955 pixels), Update(7/2/19): This will now be set to 0.1 arcmin = 12.19512195 pixels
    B:-int, Binning, The binning on the regArea CIAO tool, It's standard value is 1 pixel
    """
    #print "PWD 1:"
    #system('pwd')
    #homepath=os.path.realpath('.')
    #print "homepath :",homepath
    D25_S_Maj_Deg=D25_Finder.D25_Finder(gname)
    D25_S_Maj=D25_S_Maj_Deg*3600.0 #D25_S_Maj:-float, D25_Semi_Major_Axis, The D25 Semi Major Axis of the current galaxy in arcseconds
    R_Phys=D25_S_Maj*2.03252032520325 #R_Phys:-numpy.float64, Radius_Physical, The radius of the galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
    if(D25_Steps_Bool):
        rchange=R_Phys
    inner_r=0.0 #inner_r:-float, Inner_Radius, The radius of the inner most circle
    #outer_r_gap=25.0 #outer_r_gap:-float, Outer_Radius_Gap, The addtional distance that needs to be added to the outer radius inorder to account for dithering #The addtional distance that needs to be added to the outer radius inorder to account for dithering
    outer_r_gap=40.0 #outer_r_gap:-float, Outer_Radius_Gap, The addtional distance that needs to be added to the outer radius inorder to account for dithering #The addtional distance that needs to be added to the outer radius inorder to account for dithering
    cur_r=inner_r #cur_r:-float?, Current_Radius, The current radius of the area circle in pixels
    n=1 #n:-int, n, the radius change multiplier, ie the the maximum n is the number of times the radius increases
    a_tot=0.0 #a_tot:-float, Area_Total, The total intersecting area of all the CCDs currently intersecting with the area circle
    a_L=[] #a_L:-list, Area_List, The list of Area Ratios for each n
    evtfpath_L=evtfpath.split("/")
    evtfname=evtfpath_L[len(evtfpath_L)-1]
    #print "evtfname: ", evtfname
    polyfpath_L=polyfpath.rsplit("/",1)
    print("polyfpath_L : ", polyfpath_L)
    polyfpath_no_fname=polyfpath_L[0]
    print("polyfpath_no_fname : ", polyfpath_no_fname)
    Evtfname_Reduced=evtfname.split(".")[0] #Evtfname_Reduced:-str, Event_Filename_Reduced, The filename of the event 2 file of the observation without the extention ".fits" at the end, for example "acisf02076_repro_evt2"
    Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(gname)
    if(Fnamekey==""):
        Output_File=open(polyfpath_no_fname+"/"+str(Gname_Modifed)+"_"+Evtfname_Reduced+"_Area_List.txt","w") #Output_File:-file, Output_File, The Area_List file, which is the file were the list of Area_Ratios one for each circle (ie. each n) are saved, in the form of one line per ratio
    else:
        Output_File=open(polyfpath_no_fname+"/"+str(Gname_Modifed)+"_"+Evtfname_Reduced+"_"+Fnamekey+"_Area_List.txt","w") #Output_File:-file, Output_File, The Area_List file, which is the file were the list of Area_Ratios one for each circle (ie. each n) are saved, in the form of one line per ratio
    polystring_L=[] #polystring_L:-list, Polygon String List, A list of all the CCD shape strings
    dir = os.path.dirname(__file__)
    #system('pwd')
    #system('cd ../..')
    #system('pwd')
    path=polyfpath
    #path=os.path.realpath('../Polygons/'+str(polyfname)) #For when code in run in Desktop/Area_Calc #Going to need to modify inorder to use the filepath of the simple_region_modifed file outputed in Master_Output or more a easier option is to run in code where the simple_region_modifed is and just feed it the file while the code is in the same directory
    #path=os.path.realpath('../../Polygons/'+str(polyfname)) #For when code in run in Desktop/CCD_Incompleteness_Correction/Area_Calc
    #path=os.path.realpath('../SQL_Standard_File/SQL_Sandard_File.csv')
    #print "Path=",path
    #data = ascii.read(path)
    #polyfile=open("/home/asantini/Desktop/Polygons/"+str(polyfname),"r") #polyfile:-file, Polyfile, The polygon file that has the CCD shape strings in it #OLD
    polyfile=open(path,"r") #polyfile:-file, Polyfile, The polygon file that has the CCD shape strings in it
    #print type(polyfile)
    #print polyfile
    G_Data = Ned.query_object(gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The queryed data of the galaxy from NED in the form of a astropy table
    #print G_Data
    #print type(G_Data)
    raGC=float(G_Data['RA(deg)']) #raGC:-float, Right Ascension of Galactic Center, The right ascension of the Galactic center of the current galaxy in degrees.
    decGC=float(G_Data['DEC(deg)']) #decGC:-float, Declination of Galactic Center, The declination of the Galactic center of the current galaxy in degrees.
    #print "PWD 2:"
    #system('pwd')
    #os.chdir(evtfpath)
    #dmcoords(infile=str(evtfname),ra=str(raGC), dec=str(decGC), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the GC to SKY coodinates in pixels (?)
    dmcoords(infile=str(evtfpath),ra=str(raGC), dec=str(decGC), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the GC to SKY coodinates in pixels (?)
    X_Phys=dmcoords.x #X_Phys:-float, X_Physical, The sky plane X pixel coordinate in units of pixels of the Galactic center
    Y_Phys=dmcoords.y #Y_Phys:-float, Y_Physical, The sky plane Y pixel coordinate in units of pixels of the Galactic center
    Chip_ID=dmcoords.chip_id #Chip_ID:-int, Chip_ID, The Chip ID number the GC is on
    #print "PWD 2:"
    #system('pwd')
    #os.chdir(homepath)
    #print "PWD 3:"
    #system('pwd')
    #print "X_Phys ", X_Phys
    #print "Y_Phys ", Y_Phys
    #Max_Min_Chip_Coord_L=[0,1024]
    #Max_Min_Chip_Coord_L=[1,1025]
    #dmkeypar acisf03931_repro_evt2.fits "DETNAM"
    #punlearn("dmkeypar") #This wipes the dmkeypar paramiter file
    #pset("dmkeypar",'hl') #This symtax is wrong
    #pset("dmkeypar", "mode", "hl")
    #pset("dmkeypar", "infile", str(evtfname))
    #pset("dmkeypar", "keyword","DETNAM")
    """
    pars = plist("dmkeypar")
    values = {}
    for p in pars:
        values[p] = pget( "dmkeypar", p )
    print pars
    print values
    """
    #dmkeypar(infile=str(evtfname), keyword="DETNAM") #Runs the dmkeypar tool which finds the data in the FITS header asscoiated with a certain header name, in this case dmkeypar is finding the "DETNAM" header info, which is a string containing what CCDs are used in the FOV1.fits file for the observation, For example "ACIS-356789" Chip_ID_String contains the chip IDs the string segment "356789" where each number in the list is its own CCD ID
    """
    pars = plist("dmkeypar")
    values = {}
    for p in pars:
        values[p] = pget( "dmkeypar", p )
    print pars
    print values
    """
    """
    This Par of the code finds what CCD's are used in the current observation by finding a string in the "DETNAM" header in the Event 2 file
    """
    #os.chdir(evtfpath)
    Header_String=dmlist(infile=str(evtfpath),opt="header")
    #os.chdir(homepath)
    #print Header_String
    Header_String_Reduced=Header_String.split("DETNAM")[1]
    #print Header_String_Reduced
    Header_String_Reduced_2=Header_String_Reduced.split("String")[0]
    #print Header_String_Reduced_2
    Header_String_Reduced_3=Header_String_Reduced_2.replace(' ', '')
    #print Header_String_Reduced_3
    #dmkeypar(infile=str(evtfname), keyword="DETNAM")
    #pget(paramfile, paramname)
    #Chip_ID_String=pget(toolname="dmkeypar", parameter="value")
    #Chip_ID_String=pget("dmkeypar","value") #Chip_ID_String:-str, Chip_Idenifcation_String, Runs the pget tool to get the string containing what CCDs are used in the FOV1.fits file from the parameter file asscoiated with the dmkeypar tool and sets it equal to the Chip_ID_String (This) variable
    Chip_ID_String=Header_String_Reduced_3 #Chip_ID_String:-str, Chip_Idenifcation_String, Runs the pget tool to get the string containing what CCDs are used in the FOV1.fits file from the parameter file asscoiated with the dmkeypar tool and sets it equal to the Chip_ID_String (This) variable
    #Chip_ID_String=pget(toolname="dmkeypar", p_value="value")
    #print "Chip_ID_String ", Chip_ID_String
    Chip_ID_String_L=Chip_ID_String.split('-') #Chip_ID_String_L:-List, Chip_Idenifcation_String_List, The resulting list from spliting the Chip_ID_String on "_", This list contains 2 elements, the first element is the string "ACIS" and the second element is the string segment in the form (Example) "356789" where each number in the list is its own CCD ID
    #print "Chip_ID_String_L ", Chip_ID_String_L
    Chip_ID_String_Reduced=Chip_ID_String_L[1] #Chip_ID_String_Reduced:-str, Chip_Idenifcation_String_Reduced, the string segment in the form (Example) "356789" where each number in the list is its own CCD ID
    #print "Chip_ID_String_Reduced ", Chip_ID_String_Reduced
    Chip_ID_L=[] #Chip_ID_L:-List, Chip_Idenifcation_List, The list of all the int CCD IDs in FOV1.fits file
    for Cur_Chip_ID_Str in Chip_ID_String_Reduced: #Cur_Chip_ID_Str:-str, Current_Chip_Idenifcation_Str, The string vaule of the current string CCD ID in the Chip_ID_String_Reduced string, for example "3"
        Cur_Chip_ID=int(Cur_Chip_ID_Str) #Cur_Chip_ID:-int, Current_Chip_Idenifcation, The current chip ID number as an int, for example 3
        Chip_ID_L.append(Cur_Chip_ID) #Appends The current chip ID number as an int to Chip_Idenifcation_List
    #print "Chip_ID_L ", Chip_ID_L
    """
    This part of the code finds every distance between the Galactic Center and each corner of each CCD and puts them all into a list (Dist_L), The largest distance in Dist_L is the Outer_Radius
    """
    #Max_Min_Chip_Coord_L=[0.0,1025.0] #Max_Min_Chip_Coord_L:-List, Maximum_Minimum_Chip_Coordinates_List, A list containing 2 elements the first of which is the lowest possble Chip value (X or Y) for the given Axis (in pixels) and the second is the largest possble Chip value (X or Y) for the given Axis. Since the CCDs on Chandra are square 1024 X 1024 pixel CCDs, the minimun and maximum Chip X values and Chip Y values are identical and therefore can be represented by this single list
    #Max_Min_Chip_Coord_L=[0,1025] #Max_Min_Chip_Coord_L:-List, Maximum_Minimum_Chip_Coordinates_List, A list containing 2 elements the first of which is the lowest possble Chip value (X or Y) for the given Axis (in pixels) and the second is the largest possble Chip value (X or Y) for the given Axis. Since the CCDs on Chandra are square 1024 X 1024 pixel CCDs, the minimun and maximum Chip X values and Chip Y values are identical and therefore can be represented by this single list
    Max_Min_Chip_Coord_L=[1,1024] #Max_Min_Chip_Coord_L:-List, Maximum_Minimum_Chip_Coordinates_List, A list containing 2 elements the first of which is the lowest possble Chip value (X or Y) for the given Axis (in pixels) and the second is the largest possble Chip value (X or Y) for the given Axis. Since the CCDs on Chandra are square 1024 X 1024 pixel CCDs, the minimun and maximum Chip X values and Chip Y values are identical and therefore can be represented by this single list
    #Max_Min_Chip_Coord_L=[0,1023] #Max_Min_Chip_Coord_L:-List, Maximum_Minimum_Chip_Coordinates_List, A list containing 2 elements the first of which is the lowest possble Chip value (X or Y) for the given Axis (in pixels) and the second is the largest possble Chip value (X or Y) for the given Axis. Since the CCDs on Chandra are square 1024 X 1024 pixel CCDs, the minimun and maximum Chip X values and Chip Y values are identical and therefore can be represented by this single list
    Dist_L=[] #Dist_L:-List, Distance_List, The list of every distance between the Galactic Center and each corner of each CCD
    for Chip_ID_Test in Chip_ID_L: #Chip_ID_Test:-int, Chip_Idenifcation_Test, The current test CCD were that four corners are being tested as the furthest point of the Galactic Center
        #print "Chip_ID_Test ", Chip_ID_Test
        #print type(Chip_ID_Test)
        for Cur_Chip_X in Max_Min_Chip_Coord_L: #Cur_Chip_X:-float, Current_Chip_X, The chip X value of the current corner in pixels (Can be either 0.0 or 1025.0)
            #print type(Cur_Chip_X)
            for Cur_Chip_Y in Max_Min_Chip_Coord_L: #Cur_Chip_Y:-float, Current_Chip_Y, The chip Y value of the current corner in pixels (Can be either 0.0 or 1025.0)
                #os.chdir(evtfpath)
                #dmcoords(infile=str(evtfname),chipx=Cur_Chip_X, chipy=Cur_Chip_Y, chip_id=Chip_ID_Test, option='chip', verbose=0) #Runs dmcoords to convert the current CCD corner coordinates from CHIP coordinates to SKY coordinates
                dmcoords(infile=str(evtfpath),chipx=Cur_Chip_X, chipy=Cur_Chip_Y, chip_id=Chip_ID_Test, option='chip', verbose=0) #Runs dmcoords to convert the current CCD corner coordinates from CHIP coordinates to SKY coordinates
                #pars = plist("dmcoords")
                #values = {}
                #for p in pars:
                    #values[p] = pget( "dmcoords", p )
                #print pars
                #print values
                X_Phys_Test=dmcoords.x #X_Phys_Test:-float, X_Physical_Test, The X value current CCD corner being tested in SKY coordinates
                #print type(X_Phys_Test)
                Y_Phys_Test=dmcoords.y #Y_Phys_Test:-float, Y_Physical_Test, The Y value current CCD corner being tested in SKY coordinates
                #os.chdir(homepath)
                #print "Test Point CHIP ", [Cur_Chip_X,Cur_Chip_Y,Chip_ID_Test]
                #print "Test Point SKY ", [X_Phys_Test,Y_Phys_Test]
                X_Phys_Diff=X_Phys-X_Phys_Test #X_Phys_Diff:-float, X_Physical_Difference, The differnce between the Galactic Center X value and the current chip corner X value
                Y_Phys_Diff=Y_Phys-Y_Phys_Test #Y_Phys_Diff:-float, Y_Physical_Difference, The differnce between the Galactic Center Y value and the current chip corner Y value
                Dist=np.sqrt(((X_Phys_Diff)**2)+((Y_Phys_Diff)**2)) #Dist:-numpy.float64, Distance, The distance between the Galactic Center and the current CCD Corner
                #print "Dist ", Dist
                #print type(Dist)
                Dist_L.append(Dist) #Appends the current Distance to Distance_List
    #print "Dist_L ", Dist_L
    Dist_Max=max(Dist_L) #Dist_Max:-numpy.float64, Distance_Maximum, The distance between the Galactic Center and the furthest CCD Corner
    #print "Dist_Max ", Dist_Max
    #print type(Dist_Max)
    outer_r=Dist_Max+outer_r_gap #outer_r:-numpy.float64, Outer_Radius, The largest radius of the area circle, this radius should just barely inclose the all the active CCDs for the observation (All the CCDs used in the FOV1.fits file)
    if(Reasonable_FOV_Bool):
        outer_r=1219.5121955
    #print "outer_r ", outer_r
    #print type(outer_r)
    polystring=polyfile.read() #polystring:-str, Polystring, The string containing the CCD shapes strings in it seperated by "\n"
    cur_polys_L=polystring.split("\n") #cur_polys_L:-List, Current_Polygons_List, The list of all the CCD Polygons (Simple Regions) strings for the observation, Since it is split on "\n" it is in the form ['Polystring_1','Polystring_2',...'Polystring_n',''], Example, ['box(4344.13761125,3924.99595875,5253.72685384,1088.14064223,-34.6522013895)', 'box(3728.26318125,2700.00581875,1086.83938437,1086.83938437,-34.6522013895)', ''], This has an extra element on the end that is a empty string needs to be removed from the list
    #print "cur_polys_L ", cur_polys_L
    del cur_polys_L[len(cur_polys_L)-1] #This deletes the last element containing the "" from the cur_polys_L
    #print "cur_polys_L ", cur_polys_L
    """
    #This is for simple_region_no_header_modifed files
    for i in range(1,CCD_amt+1): #Splits up the polystring into the CCD shape strings
        cur_polys=polystring.split("\n")[i] #cur_polys:-str, Current Polystring, The current CCD shape string
        polystring_L.append(cur_polys) #polystring_L:-list, Polystring List, A list of all the CCD shape strings
    """
    for cur_poly in cur_polys_L: #cur_poly:-str, Current_Polygon, The Current_Polygon string in Current_Polygons_List
        polystring_L.append(cur_poly) #Appends the Current_Polygon string to polystring_L
    while((cur_r)<=outer_r): #makes sure the largest area circle used is not larger then the outer radius outer_r
        cur_r=(n*rchange) + inner_r #increases the current radius by n times the change in radius #This is the outer radius of the annulus
        cur_inner_r=((n-1)*rchange) + inner_r #Calculates the inner radius of the annulus
        #print "cur_r 1 : ",cur_r
        #shape1 ='circle(' + str(X_Phys) +','+ str(Y_Phys)+','+ str(cur_r)+')' #shape1:-str, shape1, The shape string of the current area circle #Bug: This should be an annulus not a circle. The Subpipe B data products and the data products dependent upon Subpipe B must be recalculated.
        ##shape1 ='circle(' + str(X_Phys) +','+ str(Y_Phys)+','+ str(cur_r)+')'+'-'+'circle(' + str(X_Phys) +','+ str(Y_Phys)+','+ str(cur_inner_r)+')' #shape1:-str, shape1, The shape string of the current area annulus #Note: This used to be the area circle but that was not a useful metric as all further calculations assume annulus
        shape1 ='annulus(' + str(X_Phys) +','+ str(Y_Phys)+','+ str(cur_inner_r)+','+ str(cur_r)+')' #shape1:-str, shape1, The shape string of the current area annulus #Note: This used to be the area circle but that was not a useful metric as all further calculations assume annulus
        #print "shape1 : ",shape1
        r1 = regParse(shape1) #r1:-Region, Region 1, the region of the current annulus circle
        a_tot=0.0 #a_tot:-float, Area_Total, The total intersecting area of all the CCDs currently intersecting with the area circle
        if(((X_Phys<cur_r) or (Y_Phys<cur_r)) or (((8192-X_Phys)<cur_r) or ((8192-Y_Phys)<cur_r))):
            a_ratio=False
            a_L.append(a_ratio)
            break
        a1_cur = regArea(r1,0,0,8192,8192,B) #a1_cur:-float, Area_1_Current, The area of the current area circle
        #print "a1_cur : ",a1_cur
        for s in polystring_L: #s:-str, String, the current CCD string
            shape2 =s #Renames "s" to "shape2"
            r2 = regParse(shape2) #r2:-region, Region 2, The region of the current CCD
            r3 = regParse(shape2 + "-" + shape1) #r3:-region, Region 3, The region of the current area circle that is NOT on the CCD
            cur_a= regArea(r2,0,0,8192,8192,B) - regArea(r3,0,0,8192,8192,B) #cur_a:-float, Current_Area, The area of the current CCD that is intersecting with the area circle (?)
            #print "Current Area is ", cur_a
            a_tot=a_tot+cur_a #Adds the intersecting area of the current CCD polygon to the total intersecting area of all previous the CCD polygons for the current radius (cur_r)
            #print "Area Total is ", a_tot
            #print ""
        #print "a_tot ", a_tot #When the previous area total is equal to the current area total the previous radius is greater then or equal to the maximum radius, this could be used to tell the code when to stop
        #print "float(a1_cur) : ",float(a1_cur)
        #print "float(a_tot) : ",float(a_tot)
        a_ratio=float(a_tot)/float(a1_cur) # a_ratio:-float, Area_Ratio, The ratio of the total intersecting area on the total area of the current area annulus
        #print "Area Ratio is ", a_ratio
        a_L.append(a_ratio) #a_L:-list, Area_List, The list of Area Ratios for each n
        n=n+1 # Itterates n
        cur_r=(n*rchange) + inner_r #Increases the current radius by n times the change in radius
        cur_inner_r=((n-1)*rchange) + inner_r #Calculates the inner radius of the annulus
    Remainder_FOV=cur_r-outer_r
    print("Remainder_FOV : ", Remainder_FOV)
    for Current_Ratio in a_L: #Current_Ratio:-float, Current_Ratio, The Current_Ratio of the total intersecting area on the total area of the current area circle in a_L
        #print type(Current_Ratio)
        Current_Ratio_Str=str(Current_Ratio) #Current_Ratio_Str:-Str, Current_Ratio_String, The Current_Ratio as a string value
        Current_Ratio_Str_New_Line=Current_Ratio_Str+"\n" #Current_Ratio_Str_New_Line:-str, Current_Ratio_String_New_Line, The Current_Ratio_String with a "\n" at the end of the string to make sure that each line in the output file contains only one Area_Ratio
        Output_File.write(Current_Ratio_Str_New_Line) #Writes the Current_Ratio_String_New_Line to the Output_File
    return a_L #Returns the Area List #May not be nessary


def Aimpoint_Coords_Calc(Evt2_Fpath):
    #Evt2_Fpath=File_Query(ObsID)
    Evt2_Fpath=Evt2_Fpath
    hdulist = fits.open(Evt2_Fpath)
    Pointing_RA=hdulist[1].header['RA_PNT']
    Pointing_Dec=hdulist[1].header['DEC_PNT']
    return Pointing_RA, Pointing_Dec

def Aimpoint_Physical_Coords_Calc(Evt2_Fpath):
    Pointing_RA, Pointing_Dec=Aimpoint_Coords_Calc(Evt2_Fpath)
    dmcoords(infile=str(Evt2_Fpath),ra=str(Pointing_RA), dec=str(Pointing_Dec), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the GC to SKY coodinates in pixels (?)
    X_Phys=dmcoords.x #X_Phys:-float, X_Physical, The sky plane X pixel coordinate in units of pixels of the aimpoint
    Y_Phys=dmcoords.y #Y_Phys:-float, Y_Physical, The sky plane Y pixel coordinate in units of pixels of the aimpoint
    #Chip_ID=dmcoords.chip_id #Chip_ID:-int, Chip_ID, The Chip ID number the aimpoint is on
    return X_Phys, Y_Phys

def Offaxis_Angle_Annulus_CCD_Completeness_Calc(Evt2_Fpath, FOV_Filepath, Offaxis_Angle_Annulus_Number, rchange=121.95121955): #rchange=121.95121955 #Pixel size	23.985 microns (0.4920±0.0001 arcsec) => 121.95121955 pix/arcmin
    #myreg = annulus(x,y,inner,outer)
    #Offaxis_Angle_Annulus_Number=Offaxis_Angle_Annulus_Number_Calc(ObsID,Source_Num)
    if(Offaxis_Angle_Annulus_Number>9):
        return np.nan
    Pointing_X,Pointing_Y=Aimpoint_Physical_Coords_Calc(Evt2_Fpath)
    #rchange=121.95121955 #Pixel size	23.985 microns (0.4920±0.0001 arcsec) => 121.95121955 pix/arcmin
    Inner_Radius_Index=Offaxis_Angle_Annulus_Number
    Outer_Radius_Index=Offaxis_Angle_Annulus_Number+1
    Inner_Radius=Inner_Radius_Index*rchange
    Outer_Radius=Outer_Radius_Index*rchange
    Annulus_Region=annulus(Pointing_X,Pointing_Y,Inner_Radius,Outer_Radius)
    #q = c.shapes[0]
    Annulus_Region_Str=str(Annulus_Region.shapes[0])
    #print("Annulus_Region_Str: ", Annulus_Region_Str)
    #print("type(Annulus_Region_Str): ", type(Annulus_Region_Str))
    #my_subspace=CXCRegion("img.fits","sky")
    ##FOV_Filepath=File_Query(ObsID,key="fov1")
    #FOV_Region=CXCRegion(FOV_Filepath,"sky")
    #print("FOV_Filepath: ", FOV_Filepath)
    FOV_Region=CXCRegion(FOV_Filepath)
    Annulus_Region_Area=Annulus_Region.area()
    Intersected_Region=FOV_Region*Annulus_Region
    Intersected_Region_Area=Intersected_Region.area()
    #print("Intersected_Region: ", Intersected_Region)
    ##print("Intersected_Region_Area: ", Intersected_Region_Area)
    #FOV_Region*Annulus_Region

    #print("FOV_Area: ", FOV_Area)
    ##Ratio=Intersected_Region_Area/Annulus_Region_Area
    Ratio=Intersected_Region_Area/Annulus_Region_Area
    return Ratio

def GC_Query(Gname):
    """
    ObsID:-int  Observation ID, The integer ObsID
    raGC, decGC
    Output: tuple:
        raGC:-float, Right Ascension Galactic Center, The Right Ascension of the Galactic Center
        decGC:-float, Declination Galactic Center, The Declination of the Galactic Center

    This function takes an ObsID as an input and returns the associated galaxy's Galactic center coordinates.

    """
    #print "ObsID: ", ObsID
    ##Gname=Gname_Query(ObsID)
    #print("Gname: ", Gname)
    #print("type(Gname): ", type(Gname))
    #print("ObsID: ", ObsID)
    if(str(Gname)=="nan"):
        print("Error Gname: ", Gname)
        #return "Error","Error"
        return np.nan,np.nan
    try:
        #print "NED Gname: ", Gname
        G_Data= Ned.query_object(Gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The Galaxy Data Table queried from NED
    except:
        raise Exception("Galaxy name "+str(Gname)+" ObsID "+str(ObsID)+" Not Queryied from NED")
    #print G_Data
    try:
        raGC=float(G_Data['RA(deg)'])
        decGC=float(G_Data['DEC(deg)'])
    except:
        raGC=float(G_Data['RA'])
        decGC=float(G_Data['DEC'])
    return raGC, decGC

def Galactic_Center_Physical_Coords_Calc(Gname, Evt2_Fpath):
    #Pointing_RA, Pointing_Dec=Aimpoint_Coords_Calc(Evt2_Fpath)
    raGC, decGC = GC_Query(Gname)
    dmcoords(infile=str(Evt2_Fpath),ra=str(raGC), dec=str(decGC), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the GC to SKY coodinates in pixels (?)
    X_Phys=dmcoords.x #X_Phys:-float, X_Physical, The sky plane X pixel coordinate in units of pixels of the aimpoint
    Y_Phys=dmcoords.y #Y_Phys:-float, Y_Physical, The sky plane Y pixel coordinate in units of pixels of the aimpoint
    #Chip_ID=dmcoords.chip_id #Chip_ID:-int, Chip_ID, The Chip ID number the aimpoint is on
    return X_Phys, Y_Phys

def Reasonable_FOV_Region_Calc(Evt2_Fpath, rchange=121.95121955): #rchange=121.95121955 #Pixel size	23.985 microns (0.4920±0.0001 arcsec) => 121.95121955 pix/arcmin
    #myreg = circle(x,y,r)
    Pointing_X,Pointing_Y=Aimpoint_Physical_Coords_Calc(Evt2_Fpath)
    Radius_Index=10
    Radius=Radius_Index*rchange
    Circle_Region=circle(Pointing_X,Pointing_Y,Radius)
    return Circle_Region

def Galactic_Center_Offaxis_Angle_Annulus_CCD_Completeness_Calc(Gname, Evt2_Fpath, FOV_Filepath, Annulus_Number, rchange=121.95121955, Reasonable_FOV_Bool=True): #rchange=121.95121955 #Pixel size	23.985 microns (0.4920±0.0001 arcsec) => 121.95121955 pix/arcmin
    #myreg = annulus(x,y,inner,outer)
    #Offaxis_Angle_Annulus_Number=Offaxis_Angle_Annulus_Number_Calc(ObsID,Source_Num)
    if(Annulus_Number>9):
        return np.nan
    #Pointing_X,Pointing_Y=Aimpoint_Physical_Coords_Calc(Evt2_Fpath)
    #print("Pointing_X, Pointing_Y: ", str(Pointing_X)+" , "+str(Pointing_Y))
    GC_X,GC_Y=Galactic_Center_Physical_Coords_Calc(Gname, Evt2_Fpath)
    #print("GC_X, GC_Y: ", str(GC_X)+" , "+str(GC_Y))
    #rchange=121.95121955 #Pixel size	23.985 microns (0.4920±0.0001 arcsec) => 121.95121955 pix/arcmin
    Inner_Radius_Index=Annulus_Number
    Outer_Radius_Index=Annulus_Number+1
    Inner_Radius=Inner_Radius_Index*rchange
    Outer_Radius=Outer_Radius_Index*rchange
    Annulus_Region=annulus(GC_X,GC_Y,Inner_Radius,Outer_Radius)
    Reasonable_FOV_Region=Reasonable_FOV_Region_Calc(Evt2_Fpath)
    Annulus_Region_Reasonable_FOV_Intersected=Annulus_Region*Reasonable_FOV_Region
    FOV_Region=CXCRegion(FOV_Filepath)
    Annulus_Region_Area=Annulus_Region.area()
    if(Reasonable_FOV_Bool==False):
        Intersected_Region=FOV_Region*Annulus_Region
    if(Reasonable_FOV_Bool):
        Intersected_Region=FOV_Region*Annulus_Region_Reasonable_FOV_Intersected
    Intersected_Region_Area=Intersected_Region.area()
    Annulus_Region_Reasonable_FOV_Intersected_Area=Annulus_Region_Reasonable_FOV_Intersected.area()
    #print("Intersected_Region: ", Intersected_Region)
    ##print("Intersected_Region_Area: ", Intersected_Region_Area)
    #FOV_Region*Annulus_Region

    #print("FOV_Area: ", FOV_Area)
    Ratio=Intersected_Region_Area/Annulus_Region_Area
    #Ratio=Intersected_Region_Area/Annulus_Region_Reasonable_FOV_Intersected_Area
    return Ratio

def Galactic_Center_Offaxis_Angle_Annulus_CCD_Incompleteness_Calc(Gname, Evt2_Fpath, FOV_Filepath, Annulus_Number, rchange=121.95121955, Reasonable_FOV_Bool=True): #rchange=121.95121955 #Pixel size	23.985 microns (0.4920±0.0001 arcsec) => 121.95121955 pix/arcmin
    #myreg = annulus(x,y,inner,outer)
    #Offaxis_Angle_Annulus_Number=Offaxis_Angle_Annulus_Number_Calc(ObsID,Source_Num)
    if(Annulus_Number>9):
        return np.nan
    #Pointing_X,Pointing_Y=Aimpoint_Physical_Coords_Calc(Evt2_Fpath)
    #print("Pointing_X, Pointing_Y: ", str(Pointing_X)+" , "+str(Pointing_Y))
    GC_X,GC_Y=Galactic_Center_Physical_Coords_Calc(Gname, Evt2_Fpath)
    #print("GC_X, GC_Y: ", str(GC_X)+" , "+str(GC_Y))
    #rchange=121.95121955 #Pixel size	23.985 microns (0.4920±0.0001 arcsec) => 121.95121955 pix/arcmin
    Inner_Radius_Index=Annulus_Number
    Outer_Radius_Index=Annulus_Number+1
    Inner_Radius=Inner_Radius_Index*rchange
    Outer_Radius=Outer_Radius_Index*rchange
    Annulus_Region=annulus(GC_X,GC_Y,Inner_Radius,Outer_Radius)
    Reasonable_FOV_Region=Reasonable_FOV_Region_Calc(Evt2_Fpath)
    Annulus_Region_Reasonable_FOV_Intersected=Annulus_Region*Reasonable_FOV_Region
    FOV_Region=CXCRegion(FOV_Filepath)
    Annulus_Region_Area=Annulus_Region.area()
    if(Reasonable_FOV_Bool==False):
        #Intersected_Region=FOV_Region*Annulus_Region
        Intersected_Region=Annulus_Region-FOV_Region
    if(Reasonable_FOV_Bool):
        #Intersected_Region=FOV_Region*Annulus_Region_Reasonable_FOV_Intersected
        Intersected_Region=Annulus_Region_Reasonable_FOV_Intersected-FOV_Region
    Intersected_Region_Area=Intersected_Region.area()
    Annulus_Region_Reasonable_FOV_Intersected_Area=Annulus_Region_Reasonable_FOV_Intersected.area()
    #print("Intersected_Region: ", Intersected_Region)
    ##print("Intersected_Region_Area: ", Intersected_Region_Area)
    #FOV_Region*Annulus_Region

    #print("FOV_Area: ", FOV_Area)
    Ratio=Intersected_Region_Area/Annulus_Region_Area
    #Ratio=Intersected_Region_Area/Annulus_Region_Reasonable_FOV_Intersected_Area
    return Ratio

def Area_Calc(Gname, Evt2_Fpath, FOV_Filepath, rchange=121.95121955, Num_Steps=10, D25_Steps_Bool=False):
    Ratio_L=[]
    if(D25_Steps_Bool):
        Reasonable_FOV=10*60*2.03252032520325
        D25_S_Maj_Deg=D25_Finder.D25_Finder(Gname)
        D25_S_Maj=D25_S_Maj_Deg*3600.0 #D25_S_Maj:-float, D25_Semi_Major_Axis, The D25 Semi Major Axis of the current galaxy in arcseconds
        R_Phys=D25_S_Maj*2.03252032520325 #R_Phys:-numpy.float64, Radius_Physical, The radius of the galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
        rchange=R_Phys
        Num_Steps=int(np.floor(Reasonable_FOV/rchange))
    for Step in range(0, Num_Steps):
        Cur_Ratio=Offaxis_Angle_Annulus_CCD_Completeness_Calc(Evt2_Fpath, FOV_Filepath, Step, rchange=rchange)
        Ratio_L.append(Cur_Ratio)
    return Ratio_L

def GC_Area_Calc(Gname, Evt2_Fpath, FOV_Filepath, rchange=121.95121955, Num_Steps=10, D25_Steps_Bool=False, Reasonable_FOV_Bool=True):
    Ratio_L=[]
    Ratio_Incompleteness_L=[]
    if(D25_Steps_Bool):
        Reasonable_FOV=10*60*2.03252032520325
        D25_S_Maj_Deg=D25_Finder.D25_Finder(Gname)
        D25_S_Maj=D25_S_Maj_Deg*3600.0 #D25_S_Maj:-float, D25_Semi_Major_Axis, The D25 Semi Major Axis of the current galaxy in arcseconds
        R_Phys=D25_S_Maj*2.03252032520325 #R_Phys:-numpy.float64, Radius_Physical, The radius of the galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
        rchange=R_Phys
        Num_Steps=int(np.floor(Reasonable_FOV/rchange))
    for Step in range(0, Num_Steps):
        #Cur_Ratio=Offaxis_Angle_Annulus_CCD_Completeness_Calc(Evt2_Fpath, FOV_Filepath, Step, rchange=rchange)
        Cur_Ratio=Galactic_Center_Offaxis_Angle_Annulus_CCD_Completeness_Calc(Gname, Evt2_Fpath, FOV_Filepath, Step, rchange=rchange, Reasonable_FOV_Bool=Reasonable_FOV_Bool)
        Cur_Ratio_Incompleteness=Galactic_Center_Offaxis_Angle_Annulus_CCD_Incompleteness_Calc(Gname, Evt2_Fpath, FOV_Filepath, Step, rchange=rchange, Reasonable_FOV_Bool=Reasonable_FOV_Bool)
        Ratio_L.append(Cur_Ratio)
        Ratio_Incompleteness_L.append(Cur_Ratio_Incompleteness)
    return Ratio_L, Ratio_Incompleteness_L


def Offaxis_Angle_Annulus_Region_Calc(Evt2_Fpath, FOV_Filepath, Offaxis_Angle_Annulus_Number, rchange=121.95121955): #rchange=121.95121955 #Pixel size	23.985 microns (0.4920±0.0001 arcsec) => 121.95121955 pix/arcmin
    #myreg = annulus(x,y,inner,outer)
    #Offaxis_Angle_Annulus_Number=Offaxis_Angle_Annulus_Number_Calc(ObsID,Source_Num)
    if(Offaxis_Angle_Annulus_Number>9):
        return np.nan
    Pointing_X,Pointing_Y=Aimpoint_Physical_Coords_Calc(Evt2_Fpath)
    #rchange=121.95121955 #Pixel size	23.985 microns (0.4920±0.0001 arcsec) => 121.95121955 pix/arcmin
    Inner_Radius_Index=Offaxis_Angle_Annulus_Number
    Outer_Radius_Index=Offaxis_Angle_Annulus_Number+1
    Inner_Radius=Inner_Radius_Index*rchange
    Outer_Radius=Outer_Radius_Index*rchange
    Annulus_Region=annulus(Pointing_X,Pointing_Y,Inner_Radius,Outer_Radius)
    Annulus_Region_Str=str(Annulus_Region.shapes[0])
    FOV_Region=CXCRegion(FOV_Filepath)
    Annulus_Region_Area=Annulus_Region.area()
    Intersected_Region=FOV_Region*Annulus_Region
    Intersected_Region_Area=Intersected_Region.area()
    return Annulus_Region, Intersected_Region

def Galactic_Center_Offaxis_Angle_Annulus_Calc(Gname, Evt2_Fpath, FOV_Filepath, Annulus_Number, rchange=121.95121955): #rchange=121.95121955 #Pixel size	23.985 microns (0.4920±0.0001 arcsec) => 121.95121955 pix/arcmin
    #myreg = annulus(x,y,inner,outer)
    #Offaxis_Angle_Annulus_Number=Offaxis_Angle_Annulus_Number_Calc(ObsID,Source_Num)
    if(Annulus_Number>9):
        return np.nan
    #Pointing_X,Pointing_Y=Aimpoint_Physical_Coords_Calc(Evt2_Fpath)
    GC_X,GC_Y=Galactic_Center_Physical_Coords_Calc(Gname, Evt2_Fpath)
    #rchange=121.95121955 #Pixel size	23.985 microns (0.4920±0.0001 arcsec) => 121.95121955 pix/arcmin
    Inner_Radius_Index=Annulus_Number
    Outer_Radius_Index=Annulus_Number+1
    Inner_Radius=Inner_Radius_Index*rchange
    Outer_Radius=Outer_Radius_Index*rchange
    Annulus_Region=annulus(GC_X,GC_Y,Inner_Radius,Outer_Radius)
    Annulus_Region_Str=str(Annulus_Region.shapes[0])
    FOV_Region=CXCRegion(FOV_Filepath)
    Annulus_Region_Area=Annulus_Region.area()
    Intersected_Region=FOV_Region*Annulus_Region
    Intersected_Region_Area=Intersected_Region.area()
    return Annulus_Region, Intersected_Region

def Area_Intersection_Map(Gname, Evt2_Fpath, FOV_Filepath, rchange=121.95121955, Num_Steps=10, D25_Steps_Bool=False, CCD_Completeness_Bool=False):
    Ratio_HL=[]
    CCD_Completeness_Int=int(CCD_Completeness_Bool)
    if(D25_Steps_Bool):
        Reasonable_FOV=10*60*2.03252032520325
        D25_S_Maj_Deg=D25_Finder.D25_Finder(Gname)
        D25_S_Maj=D25_S_Maj_Deg*3600.0 #D25_S_Maj:-float, D25_Semi_Major_Axis, The D25 Semi Major Axis of the current galaxy in arcseconds
        R_Phys=D25_S_Maj*2.03252032520325 #R_Phys:-numpy.float64, Radius_Physical, The radius of the galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
        rchange=R_Phys
        Num_Steps=int(np.floor(Reasonable_FOV/rchange))
    #Reasonable_FOV_Region=Reasonable_FOV_Region_Calc(Gname, Evt2_Fpath)
    for Step in range(0, Num_Steps):
        Ratio_L=[]
        #Cur_Ratio=Offaxis_Angle_Annulus_CCD_Completeness_Calc(Evt2_Fpath, FOV_Filepath, Step, rchange=rchange)
        Offaxis_Angle_Annulus=Offaxis_Angle_Annulus_Region_Calc(Evt2_Fpath, FOV_Filepath, Step, rchange=rchange)[CCD_Completeness_Int]
        Offaxis_Angle_Annulus_Area=Offaxis_Angle_Annulus.area()
        for GC_Step in range(0, Num_Steps):
            GC_Offaxis_Angle_Annulus=Galactic_Center_Offaxis_Angle_Annulus_Calc(Gname, Evt2_Fpath, FOV_Filepath, GC_Step, rchange=rchange)[CCD_Completeness_Int]
            #print("Offaxis_Angle_Annulus: ", Offaxis_Angle_Annulus)
            #print("GC_Offaxis_Angle_Annulus: ", GC_Offaxis_Angle_Annulus)
            #GC_Offaxis_Angle_Annulus_Area=GC_Offaxis_Angle_Annulus.area()
            Intersected_Region=Offaxis_Angle_Annulus*GC_Offaxis_Angle_Annulus
            Intersected_Region_Area=Intersected_Region.area()
            #Intersected_Ratio=Intersected_Region_Area/GC_Offaxis_Angle_Annulus_Area
            Intersected_Ratio=Intersected_Region_Area/Offaxis_Angle_Annulus_Area
            Ratio_L.append(Intersected_Ratio)
        Ratio_HL.append(Ratio_L)
        Ratio_DF = pd.DataFrame(Ratio_HL)
    return Ratio_DF

def Galactic_Area_Intersection_Map(Gname, Evt2_Fpath, FOV_Filepath, rchange=121.95121955, Num_Steps=10, D25_Steps_Bool=False):
    Ratio_HL=[]
    if(D25_Steps_Bool):
        Reasonable_FOV=10*60*2.03252032520325
        D25_S_Maj_Deg=D25_Finder.D25_Finder(Gname)
        D25_S_Maj=D25_S_Maj_Deg*3600.0 #D25_S_Maj:-float, D25_Semi_Major_Axis, The D25 Semi Major Axis of the current galaxy in arcseconds
        R_Phys=D25_S_Maj*2.03252032520325 #R_Phys:-numpy.float64, Radius_Physical, The radius of the galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
        rchange=R_Phys
        Num_Steps=int(np.floor(Reasonable_FOV/rchange))
    for GC_Step in range(0, Num_Steps):
        Ratio_L=[]
        #Cur_Ratio=Offaxis_Angle_Annulus_CCD_Completeness_Calc(Evt2_Fpath, FOV_Filepath, Step, rchange=rchange)
        GC_Offaxis_Angle_Annulus=Galactic_Center_Offaxis_Angle_Annulus_Calc(Gname, Evt2_Fpath, FOV_Filepath, GC_Step, rchange=rchange)[0]
        GC_Offaxis_Angle_Annulus_Area=GC_Offaxis_Angle_Annulus.area()
        for Step in range(0, Num_Steps):
            #GC_Offaxis_Angle_Annulus=Galactic_Center_Offaxis_Angle_Annulus_Calc(Gname, Evt2_Fpath, FOV_Filepath, GC_Step, rchange=rchange)[0]
            Offaxis_Angle_Annulus=Offaxis_Angle_Annulus_Region_Calc(Evt2_Fpath, FOV_Filepath, Step, rchange=rchange)[0]
            #print("Offaxis_Angle_Annulus: ", Offaxis_Angle_Annulus)
            #print("GC_Offaxis_Angle_Annulus: ", GC_Offaxis_Angle_Annulus)
            #GC_Offaxis_Angle_Annulus_Area=GC_Offaxis_Angle_Annulus.area()
            Intersected_Region=Offaxis_Angle_Annulus*GC_Offaxis_Angle_Annulus
            Intersected_Region_Area=Intersected_Region.area()
            #Intersected_Ratio=Intersected_Region_Area/GC_Offaxis_Angle_Annulus_Area
            Intersected_Ratio=Intersected_Region_Area/GC_Offaxis_Angle_Annulus_Area
            Ratio_L.append(Intersected_Ratio)
        Ratio_HL.append(Ratio_L)
        Ratio_DF = pd.DataFrame(Ratio_HL)
    return Ratio_DF

def Galactic_Area_Reasonable_FOV_Intersection_Calc(Gname, Evt2_Fpath, FOV_Filepath, rchange=121.95121955, Num_Steps=10, D25_Steps_Bool=False):
    Ratio_L=[]
    if(D25_Steps_Bool):
        Reasonable_FOV=10*60*2.03252032520325
        D25_S_Maj_Deg=D25_Finder.D25_Finder(Gname)
        D25_S_Maj=D25_S_Maj_Deg*3600.0 #D25_S_Maj:-float, D25_Semi_Major_Axis, The D25 Semi Major Axis of the current galaxy in arcseconds
        R_Phys=D25_S_Maj*2.03252032520325 #R_Phys:-numpy.float64, Radius_Physical, The radius of the galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
        rchange=R_Phys
        Num_Steps=int(np.floor(Reasonable_FOV/rchange))
    Reasonable_FOV_Region=Reasonable_FOV_Region_Calc(Evt2_Fpath, rchange=rchange)
    for GC_Step in range(0, Num_Steps):
        #Cur_Ratio=Offaxis_Angle_Annulus_CCD_Completeness_Calc(Evt2_Fpath, FOV_Filepath, Step, rchange=rchange)
        GC_Offaxis_Angle_Annulus=Galactic_Center_Offaxis_Angle_Annulus_Calc(Gname, Evt2_Fpath, FOV_Filepath, GC_Step, rchange=rchange)[0]
        GC_Offaxis_Angle_Annulus_Area=GC_Offaxis_Angle_Annulus.area()
        Intersected_Region=Reasonable_FOV_Region*GC_Offaxis_Angle_Annulus
        Intersected_Region_Area=Intersected_Region.area()
        #Intersected_Ratio=Intersected_Region_Area/GC_Offaxis_Angle_Annulus_Area
        Intersected_Ratio=Intersected_Region_Area/GC_Offaxis_Angle_Annulus_Area
        Ratio_L.append(Intersected_Ratio)
    return Ratio_L

def Galactic_Area_Reasonable_FOV_Intersection_Bool_Calc(Gname, Evt2_Fpath, FOV_Filepath, rchange=121.95121955, Num_Steps=10, D25_Steps_Bool=False):
    Completeness_Bool_L=[]
    Ratio_L=Galactic_Area_Reasonable_FOV_Intersection_Calc(Gname, Evt2_Fpath, FOV_Filepath, rchange=rchange, Num_Steps=Num_Steps, D25_Steps_Bool=D25_Steps_Bool)
    for Cur_Ratio in Ratio_L:
        Cur_Ratio_Rounded=np.round(Cur_Ratio,2)
        Cur_Completeness_Bool=(Cur_Ratio_Rounded==1.0)
        Completeness_Bool_L.append(Cur_Completeness_Bool)
    return Completeness_Bool_L


#print Area_Calc_Frac_B_2_Alt_2("NGC 253","acisf03931_repro_evt2.fits","acisf03931_repro_CCD_Regions_simple_region_no_header_modifed.txt",0,120,3000,2,1)
#print Area_Calc_Frac_B_2_Alt_2("NGC 253","acisf03931_repro_evt2.fits","acisf03931_repro_CCD_Regions_simple_region_modifed_Code.txt",0,120,3000)
#print Area_Calc_Frac_B_2_Alt_2("NGC 253","acisf03931_repro_evt2.fits","acisf03931_repro_CCD_Regions_simple_region_modifed_Code.txt")
#print Area_Calc_Frac_B_2_Alt_2("NGC 253","acisf13830_repro_evt2.fits","acisf13830_Unconnnected_simple_region_modifed_Code.txt") #This does not work, The polyfpath needs to be a real observation
#print Area_Calc_Frac_B_2_Alt_2("NGC 253","acisf13830_repro_evt2.fits","acisf13830_repro_CCD_Regions_simple_region_modifed_Code.txt")
#print Area_Calc_Frac_B_2_Alt_2("NGC 253","/Network/Servers/vimes.astro.wesleyan.edu/Volumes/vvodata/home/asantini/Desktop/CCD_Incompleteness_Correction/Area Calc/acisf13830_repro_evt2.fits","acisf13830_repro_CCD_Regions_simple_region_modifed_Code.txt")
#print Area_Calc_Frac_B_2_Alt_2("NGC 253","/home/asantini/Desktop/CCD_Incompleteness_Correction/Area Calc/acisf13830_repro_evt2.fits","acisf13830_repro_CCD_Regions_simple_region_modifed_Code.txt")
#print Area_Calc_Frac_B_2_Alt_2("NGC 253","/Network/Servers/vimes.astro.wesleyan.edu/Volumes/vvodata/home/asantini/Desktop/CCD_Incompleteness_Correction/Area_Calc/acisf13830_repro_evt2.fits","acisf13830_repro_CCD_Regions_simple_region_modifed_Code.txt",Fnamekey="Arcmin_Test")
#print Area_Calc_Frac_B_2_Alt_2("NGC 253","/Network/Servers/vimes.astro.wesleyan.edu/Volumes/vvodata/home/asantini/Desktop/CCD_Incompleteness_Correction/Area_Calc/acisf13830_repro_evt2.fits","acisf13830_repro_CCD_Regions_simple_region_modifed_Code.txt",D25_Steps_Bool=True,Fnamekey="D25_Test")
#print Area_Calc_Frac_B_2_Alt_2("NGC 253","/Network/Servers/vimes.astro.wesleyan.edu/Volumes/vvodata/home/asantini/Desktop/CCD_Incompleteness_Correction/Area_Calc/acisf13830_repro_evt2.fits","acisf13830_repro_CCD_Regions_simple_region_modifed_Code.txt",Fnamekey="Annulus_Arcmin_Test")
#print Area_Calc_Frac_B_2_Alt_2("NGC 253","/Network/Servers/vimes.astro.wesleyan.edu/Volumes/vvodata/home/asantini/Desktop/CCD_Incompleteness_Correction/Area_Calc/acisf13830_repro_evt2.fits","acisf13830_repro_CCD_Regions_simple_region_modifed_Code.txt",D25_Steps_Bool=True,Fnamekey="Annulus_D25_Test")
#print(Area_Calc("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits"))
#print(Area_Calc("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits", D25_Steps_Bool=True))
#print(Area_Intersection_Map("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits"))
#print(Galactic_Area_Intersection_Map("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits"))
#print(Area_Intersection_CCD_Completeness_Map("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits"))
#print(Area_Intersection_Map("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits"))
#print(Area_Intersection_Map("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits",CCD_Completeness_Bool=True))
#GC_Area_Calc(Gname, Evt2_Fpath, FOV_Filepath,)
#print(GC_Area_Calc("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits"))
#print(GC_Area_Calc("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits", Reasonable_FOV_Bool=False))
#print(Galactic_Area_Reasonable_FOV_Intersection_Calc("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits"))
#print(Area_Intersection_Map("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits", D25_Steps_Bool=True))
#print(Area_Intersection_Map("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits", D25_Steps_Bool=True, CCD_Completeness_Bool=True))
#print(Galactic_Area_Reasonable_FOV_Intersection_Calc("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits", D25_Steps_Bool=True))
#print(Galactic_Area_Reasonable_FOV_Intersection_Bool_Calc("NGC 4449", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_evt2.fits", "/opt/xray/anthony/expansion_backup/ObsIDs/10125/new/acisf10125_repro_fov1.fits"))
