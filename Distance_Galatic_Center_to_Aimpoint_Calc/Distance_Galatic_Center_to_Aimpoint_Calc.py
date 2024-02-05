import numpy as np
import matplotlib.pyplot as plt
from ciao_contrib.runtool import *
from astroquery.ned import Ned
import os
from os import system
import sys
from astropy.io.fits import Header
from astropy.io import fits
dir = os.path.dirname(__file__)
path=os.path.realpath('../')
sys.path.append(os.path.abspath(path))
from Galaxy_Name_Reducer import Galaxy_Name_Reducer
from File_Query_Code import File_Query_Code_5
def Distance_Galatic_Center_to_Aimpoint_Calc(Gname,Exp_Max_Bool=True):
    #pass
    Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
    if(Exp_Max_Bool):
        Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2",Exp_Max_B=True)
    else:
        Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
    G_Data = Ned.query_object(Gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The queryed data of the galaxy from NED in the form of a astropy table
    #print G_Data
    #print type(G_Data)
    raGC=float(G_Data['RA(deg)']) #raGC:-float, Right Ascension of Galatic Center, The right ascension of the galatic center of the current galaxy in degrees.
    decGC=float(G_Data['DEC(deg)']) #decGC:-float, Declination of Galatic Center, The declination of the galatic center of the current galaxy in degrees.
    Dist_H_L=[]
    for Evt2_File_L in Evt2_File_H_L:
        Cur_Evt2_ObsID=Evt2_File_L[0]
        Cur_Evt2_Filepath=Evt2_File_L[1]
        hdulist = fits.open(Cur_Evt2_Filepath)
        #Exposure_Time=hdulist[1].header['EXPOSURE']
        Pointing_RA=hdulist[1].header['RA_PNT']
        Pointing_Dec=hdulist[1].header['DEC_PNT']
        Pointing_Diff_RA=Pointing_RA-raGC
        Pointing_Diff_Dec=Pointing_Dec-decGC
        Dist=np.sqrt((Pointing_Diff_RA**2.0)+(Pointing_Diff_Dec**2.0)) #MAJOR BUG HERE!!! This should be calculated with the Haversine_Distance NOT the Pythagorean Theorem!
        Dist_Arcmin=Dist*60.0
        Dist_L=[Cur_Evt2_ObsID,Dist_Arcmin]
        Dist_H_L.append(Dist_L)
    return Dist_H_L

def Distance_Galatic_Center_to_Aimpoint_Big_Calc(Gname_L,Exp_Max_Bool=True):
    Galaxy_Dist_H_L=[]
    for Gname in Gname_L:
        try:
            Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
            if(Exp_Max_Bool):
                Dist_H_L=Distance_Galatic_Center_to_Aimpoint_Calc(Gname)
            else:
                Dist_H_L=Distance_Galatic_Center_to_Aimpoint_Calc(Gname,Exp_Max_Bool=False)
            Galaxy_Dist_L=[Gname_Modifed,Dist_H_L]
            Galaxy_Dist_H_L.append(Galaxy_Dist_L)
        except:
            print Gname_Modifed+" has an error ! ! !"
    return Galaxy_Dist_H_L
def Distance_Galatic_Center_to_Aimpoint_Big_Calc_Plot(Gname_L,Exp_Max_Bool=True):
    Galaxy_Dist_H_L=Distance_Galatic_Center_to_Aimpoint_Big_Calc(Gname_L,Exp_Max_Bool)
    Sample_Dist_L=[]
    for Galaxy_Dist_L in Galaxy_Dist_H_L:
        Gname=Galaxy_Dist_L[0]
        Dist_H_L=Galaxy_Dist_L[1]
        for Dist_L in Dist_H_L:
            ObsID=Dist_L[0]
            Dist=Dist_L[1]
            Sample_Dist_L.append(Dist)
    Hist=plt.hist(Sample_Dist_L)
    plt.xlabel('Pointing Distance from GC (arcmin)')
    plt.ylabel('Number of Galaxies')
    print "Hist: ", Hist
    plt.savefig("Pointing_Distance_from_GC.pdf")
    #plt.show()
#print Distance_Galatic_Center_to_Aimpoint_Calc("NGC 3631")
#print Distance_Galatic_Center_to_Aimpoint_Calc("NGC 7507")
#['NGC 2841', 'NGC 3877', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'NGC 0278', 'MESSIER 088', 'NGC 3585', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4570', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'IC 1613', 'NGC 4477', 'NGC 2787', 'IC 5267', 'NGC 3923', 'NGC 891', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'NGC 4314', 'NGC 4559', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4742', 'NGC 1672', 'NGC 4725', 'NGC 0891', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 2865', 'MESSIER 059', 'NGC 1427', 'NGC 3628', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521']
#print Distance_Galatic_Center_to_Aimpoint_Big_Calc(["NGC 3631","NGC 7507"])
#print Distance_Galatic_Center_to_Aimpoint_Big_Calc(['NGC 2841', 'NGC 3877', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'NGC 0278', 'MESSIER 088', 'NGC 3585', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4570', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'IC 1613', 'NGC 4477', 'NGC 2787', 'IC 5267', 'NGC 3923', 'NGC 891', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'NGC 4314', 'NGC 4559', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4742', 'NGC 1672', 'NGC 4725', 'NGC 0891', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 2865', 'MESSIER 059', 'NGC 1427', 'NGC 3628', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521']
Distance_Galatic_Center_to_Aimpoint_Big_Calc_Plot(['NGC 2841', 'NGC 3877', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'NGC 0278', 'MESSIER 088', 'NGC 3585', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4570', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'IC 1613', 'NGC 4477', 'NGC 2787', 'IC 5267', 'NGC 3923', 'NGC 891', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'NGC 4314', 'NGC 4559', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4742', 'NGC 1672', 'NGC 4725', 'NGC 0891', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 2865', 'MESSIER 059', 'NGC 1427', 'NGC 3628', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521']
)
