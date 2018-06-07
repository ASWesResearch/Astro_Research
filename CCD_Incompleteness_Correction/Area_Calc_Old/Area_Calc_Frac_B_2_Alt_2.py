from ciao_contrib.runtool import *
from region import *
def Area_Calc_Frac_B_2_Alt_2(xc,yc,polyfname,inner_r,rchange,outer_r,CCD_amt,B):
    """
    xc:-float, X Circle, The X coordinate of the center of the area cirlces in pixels(?)
    yc:-float, Y Circle, The Y coordinate of the center of the area cirlces in pixels(?)
    ployfname:-str, PolyFileName, The filename of the simple_region_no_header_modifed file as a string
    inner_r:-int(float?), Inner_Radius, The inner radius of the inner most area circle in pixels
    rchange:-int(float?), Radius Change, The change in radius from one area cirlce to another area cirlce in pixels
    outer_r:-int(float?), Outer Radius, The outer radius of the outer most area cirlce in pixels
    CCD_amt:-int, CCD Amount, The amount of CCDs in the observation
    B:-int, Binning, The binning on the regArea CIAO tool
    """
    cur_r=inner_r #cur_r:-int(float?), Current_Radius, The current radius of the area circle in pixels
    n=1 #n:-int, n, the radius change multiplier, ie the the maximum n is the number of times the radius increases
    a_tot=0
    a_L=[]
    polystring_L=[]
    polyfile=open("/home/asantini/Desktop/Polygons/"+str(polyfname),"r") #polyfile:-file, Polyfile, The polygon file that has the CCD shape strings in it
    #print type(polyfile)
    #print polyfile
    polystring=polyfile.read() #polystring:-str, Polystring, The string containing the CCD shapes strings in it seperated by "\n"
    for i in range(1,CCD_amt+1): #Splits up the polystring into the CCD shape strings
        cur_polys=polystring.split("\n")[i] #cur_polys:-str, Current Polystring, The current CCD shape string
        polystring_L.append(cur_polys) #polystring_L:-list, Polystring List, A list of all the CCD shape strings
    while((cur_r)<=outer_r): #makes sure the largest area circle used is not larger then the outer radius outer_r
        cur_r=(n*rchange) + inner_r #increases the current radius by n times the change in radius
        shape1 ='circle(' + str(xc) +','+ str(yc)+','+ str(cur_r)+')' #shape1:-str, shape1, The shape string of the current area circle
        r1 = regParse(shape1) #r1:-Region, Region 1, the region of the current area circle
        a_tot=0 #a_tot:-int(float?), Area_Total, The total area of the CCD within the current area circle
        a1_cur = regArea(r1,0,0,8192,8192,B) #a1_cur:-float, Area_1_Current, The area of the current area circle
        for s in polystring_L: #s:-str, String, the current CCD string
            shape2 =s #Renames "s" to "shape2"
            r2 = regParse(shape2) #r2:-region, Region 2, The region of the current CCD
            r3 = regParse(shape2 + "-" + shape1) #r3:-region, Region 3, The region of the current area circle that is NOT on the CCD
            cur_a= regArea(r2,0,0,8192,8192,B) - regArea(r3,0,0,8192,8192,B) #cur_a:-float, Current_Area, The area of the current CCD that is intersecting with the area circle (?)
            #print "Current Area is ", cur_a
            a_tot=a_tot+cur_a #a_tot:-float, Area_Total, The total intersecting area of all the CCDs currently intersecting with the area circle
            #print "Area Total is ", a_tot
            #print ""
        a_ratio=float(a_tot)/float(a1_cur) # a_ratio:-float, Area_Ratio, The ratio of the total intersecting area on the total area of the current area circle
        #print "Area Ratio is ", a_ratio
        a_L.append(a_ratio) #a_L:-list, Area_List, The list of Area Ratios for each n
        n=n+1 # Itterates n
        cur_r=(n*rchange) + inner_r #Increases the current radius by n times the change in radius
    return a_L #Returns the Area List

print Area_Calc_Frac_B_2_Alt_2(4132.6997,4090.6476,"acisf03931_repro_simple_region_no_header_modifed",0,120,3000,2,1)
