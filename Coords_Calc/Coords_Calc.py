from ciao_contrib.runtool import *
#import pyregion
import re
def Coords_Calc(evtfpath,regfpath,header=""):
    """
    evtfpath:-str, Event 2 Filepath, The filepath of the event 2 file of the observation
    regfpath:-str, Region Filepath, The filepath of the source region file of the observation

    Returns: Source_Data_L:-hlist, Source Data List, The list of all source Coordinate Data Lists

    This code is takes the event 2 file and Region file as an input and returns a list of coordinate data lists for all sources
    in the observation. The coordinate data lists are in the form of [Cur_X,Cur_Y,Cur_Chip_X,Cur_Chip_Y,Cur_Chip_ID,Cur_RA,Cur_DEC,Cur_Theta]
    where Cur_X and Cur_Y are in Physical Coordinates(?)
    """
    #print "regfpath: ", regfpath
    #Reg_Data=pyregion.open(regfpath)
    Region_File=open(regfpath,"r")
    Region_Str=Region_File.read()
    #print "Region_Str:\n",Region_Str
    if(header==""):
        Region_Str_Redueced=Region_Str
    else:
        Region_Str_L=Region_Str.split(header)
        #print "Region_Str_L:\n", Region_Str_L
        Region_Str_Redueced=Region_Str_L[len(Region_Str_L)-1]
        #print "Region_Str_Redueced:\n", Region_Str_Redueced
    #Test_Out=re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+',Region_Str_Redueced)
    #Test_Out=re.findall(r'((.))',Region_Str_Redueced)
    #Test_Out=re.split(r'([()])',Region_Str_Redueced)
    #Test_Out=re.findall('\([^\)]*\)',Region_Str_Redueced)
    #Test_Out=re.findall('\([^\)]*\)',Region_Str_Redueced) #This works! But if there is a "(" or a ")" in the header or in any other part of the region file other then a shape string then the code will break ! ! !
    #print "Test_Out:\n", Test_Out
    #print "type(Test_Out): ", type(Test_Out)
    Coord_Str_L=re.findall('\([^\)]*\)',Region_Str_Redueced) #This works! But if there is a "(" or a ")" in the header or in any other part of the region file other then a shape string then the code will break ! ! !
    #print "Coord_Str_L:\n", Coord_Str_L
    #print "type(Coord_Str_L): ", type(Coord_Str_L)
    Source_Data_L=[]
    for Coord_Str in Coord_Str_L:
        #Source_Data_L=[]
        #Reg_Data=[1,2,3,4,5]
        #for Cur_Reg_Data in Reg_Data:
        """
        Format=Cur_Reg_Data.coord_format #Format:-str, Format, The current coordinate format that the Cur_Reg_Data is in, This code will always use "physical" coordinates
        #print type(Format)
        Coords_L=Cur_Reg_Data.coord_list #Coords_L:-List, Coordinates_List, This is the list of coordinates that makes up the points that make the the current polygon in the form [X1,Y1,X2,Y2...,Xn,Yn] for finte n
        #print type(Coords_L)
        Shape=Cur_Reg_Data.name #Shape:-str, Shape, The string name of the current type of shape

        #print type(Shape)
        #print "Format ", Format
        #print "Shape ", Shape
        #print "Coords_L ", Coords_L
        Cur_X=Coords_L[0]
        Cur_Y=Coords_L[1]
        """
        Coord_Str_Redueced_L=re.split('[\(\),]',Coord_Str)
        #print "Coord_Str_Redueced_L Before: ", Coord_Str_Redueced_L
        Coord_Str_Redueced_L.pop(0)
        Coord_Str_Redueced_L.pop(len(Coord_Str_Redueced_L)-1)
        #print "Coord_Str_Redueced_L After: ", Coord_Str_Redueced_L
        Cur_X_Str=Coord_Str_Redueced_L[0]
        Cur_Y_Str=Coord_Str_Redueced_L[1]
        Cur_X=float(Cur_X_Str)
        Cur_Y=float(Cur_Y_Str)
        #continue
        dmcoords(infile=str(evtfpath),x=float(Cur_X), y=float(Cur_Y), option='sky', verbose=0, celfmt='deg') #Calls dmcoords to get the offaxis angle from the physical coordinates #I should just use the RA and DEC of each X-ray object instead of the SKY coordinate
        Cur_Theta=dmcoords.theta #Cur_Theta:-float, Current Theta, The current offaxis angle of the object in arcmin
        #print "Cur_Theta : ", Cur_Theta
        Cur_RA=dmcoords.ra
        #print "Cur_RA : ", Cur_RA
        Cur_DEC=dmcoords.dec
        #print "Cur_DEC : ", Cur_DEC
        Cur_Chip_ID=dmcoords.chip_id
        #print "Cur_Chip_ID : ", Cur_Chip_ID
        Cur_Chip_X=dmcoords.chipx
        #print "Cur_Chip_X : ", Cur_Chip_X
        Cur_Chip_Y=dmcoords.chipy
        #print "Cur_Chip_Y : ", Cur_Chip_Y
        Cur_Det_X=dmcoords.detx
        #print "Cur_Det_X : ", Cur_Det_X
        Cur_Det_Y=dmcoords.dety
        #print "Cur_Det_Y : ", Cur_Det_Y
        Cur_Source_Coords=[Cur_X,Cur_Y,Cur_Chip_X,Cur_Chip_Y,Cur_Chip_ID,Cur_RA,Cur_DEC,Cur_Det_X,Cur_Det_Y,Cur_Theta]
        #print "Cur_Source_Coords : ", Cur_Source_Coords
        Source_Data_L.append(Cur_Source_Coords)
    Region_File.close()
    return Source_Data_L
#print Coords_Calc("/Volumes/xray/simon/chandra_from_csc/1043/primary/acisf01043N003_evt2.fits","/Volumes/xray/simon/chandra_from_csc/1043/primary/1043_reg.reg")
