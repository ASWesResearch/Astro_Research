import astropy.io.ascii as ascii
import tarfile
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import os
from os import system
from astropy.io import fits
from astroquery.ned import Ned
import sys
path_GR=os.path.realpath('../')
#../../Research_Git/
#path_GR=os.path.realpath('../../Research_Git/')
#print "path_GR=",path_GR
sys.path.append(os.path.abspath(path_GR))
from Galaxy_Name_Reducer import Galaxy_Name_Reducer
from D25_Finder import D25_Finder
from File_Query_Code import File_Query_Code_5
def Histogram_Organizer(Gname_L,D25_Threshold=0.5):
    f=open("D25_Source_Ratios_Max.csv","w")
    Initial_CSV_Line="Gname,Obs_ID,Exposure_Time,D25_Deg,D25_Arcmin,Frac_of_Reasonable_FOV,Num_Sources,Num_Sources_in_D25,Num_Sources_Outside_D25,Ratio\n"
    f.write(Initial_CSV_Line)
    for Gname in Gname_L:
        """
        Gname: str- The name of the galaxy in the form NGC #
        Data: array- a table of data containg the coordinates of each object

        This fucntion takes the inputs for the name of the galaxy and returns a histrogram that plots the number of objects per bin by the
        area enclosed by the cirlce centered on the center of the galaxy that inculdes the objects in each bin in
        square degrees divided by the visible area of the galaxy in square degrees.
        This function plots the visible Major axis of the galaxy area enclosed by a circle that uses the Major axis as
        the diameter of the cirlce divided by itself to give 1 on histogram.
        This function uses astroquary to get data directly from NED

        #THIS IS THE CURRENT RUNNING VERSION OF THIS CODE
        """
        Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
        #Gname=Gname_Modifed
        print "Gname : ", Gname
        import math
        from astropy.io import ascii
        import matplotlib.pyplot as plt
        #system('pwd')
        #system('cd ~/Desktop/SQL_Standard_File/')
        #import os
        dir = os.path.dirname(__file__)
        #filename= os.path.join(dir, '~','Desktop','SQL_Standard_File',)
        #filepath=os.path.abspath("~/Desktop/SQL_Standard_File")
        #print "Filepath =",filepath
        #path= os.path.join(dir,'~','Desktop','SQL_Standard_File',)
        #path=os.path.realpath('~/Desktop/SQL_Standard_File/SQL_Sandard_File.csv')
        #path=os.path.realpath('../SQL_Standard_File/SQL_Standard_File.csv')
        path=os.path.realpath('../SQL_Standard_File/Source_Flux_Table.csv')
        Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
        if(Evt2_File_H_L==False):
            print "Invalid Galaxy"
            return
        """
        Galaxy_Obs_ID_L=[]
        for Evt2_File_L in Evt2_File_H_L:
            Cur_Galaxy_Obs_ID=Evt2_File_L[0]
            #Cur_Filepath=Evt2_File_L[1]
            Galaxy_Obs_ID_L.append(Cur_Galaxy_Obs_ID)
        """
        data = ascii.read(path) #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
        #data2=open("SQL_Sandard_File.csv","r")
        #print data2
        #system('cd ~/Desktop/galaxies/out')
        RA_A=data['sourceRA'] #RA_A:-astropy.table.column.Column, Right_Ascension_Array, The array containing all Right Ascensions in the SQL Standard File
        #print type(RA_A)
        RA_L=list(RA_A) #RA_L:-list, Right_Ascension_List, The list containing all Right Ascensions in the SQL Standard File
        #print RA_L
        Dec_A=data['sourceDec'] #Dec_A:-astropy.table.column.Column, Declination_Array, The array containing all Declinations in the SQL Standard File
        Dec_L=list(Dec_A) #Dec_L:-List, Declination_List, The list containing all Declinations in the SQL Standard File
        #print Dec_L
        #Obs_ID_A=data["obsid"] #Obs_ID_A:-astropy.table.column.Column, Observation_Idenification_Array, The array containing all Observation IDs in the SQL_Standard_File (not indexable)
        #print type(Obs_ID_A)
        #Obs_ID_L=list(Obs_ID_A) #Obs_ID_L:-List, Observation_Idenification_List, The list containing all Observation IDs in the SQL_Standard_File (So it is indexable)
        Obs_ID_A=data["OBSID"] #Obs_ID_A:-astropy.table.column.Column, Observation_Idenification_Array, The array containing all Observation IDs in the SQL_Standard_File (not indexable)
        #print type(Obs_ID_A)
        Obs_ID_L=list(Obs_ID_A) #Obs_ID_L:-List, Observation_Idenification_List, The list containing all Observation IDs in the SQL_Standard_File (So it is indexable)
        #print "Obs_ID_L ", Obs_ID_L
        #print "Galaxy_Obs_ID_L: ",Galaxy_Obs_ID_L
        #f=open("D25_Source_Ratios.csv","w")
        #Initial_CSV_Line="Gname,Obs_ID,Exposure_Time,D25_Deg,D25_Arcmin,Num_Sources,Num_Sources_in_D25,Num_Sources_Outside_D25,Ratio\n"
        #f.write(Initial_CSV_Line)
        #for Obs_ID in Galaxy_Obs_ID_L:
        """
        for Evt2_File_L in Evt2_File_H_L:
            Obs_ID=Evt2_File_L[0]
            print "Current Obs_ID: ", Obs_ID
            Cur_Filepath=Evt2_File_L[1]
            print "Cur_Filepath : ", Cur_Filepath
        """
        Max_Exposure_Time=0
        Max_Exp_Fpath=""
        for Evt2_File_L in Evt2_File_H_L:
            Obs_ID=Evt2_File_L[0]
            print "Current Obs_ID: ", Obs_ID
            Cur_Filepath=Evt2_File_L[1]
            print "Cur_Filepath : ", Cur_Filepath
            hdul = fits.open(Cur_Filepath)
            #Num_Rows_in_Array=hdul[1].header['NROWS'] #Num_Rows_in_Array:-int, Number of Row in the Array, The number of rows in a (sub)array, if less then 1024 then the observation is a subarray and will be removed from the sample
            #print "Num_Rows_in_Array : ", Num_Rows_in_Array
            #print "type(Num_Rows_in_Array) : ", type(Num_Rows_in_Array)
            Exposure_Time=hdul[1].header['EXPOSURE'] #Exposure_Time:-float, Exposure Time, The Exposure Time of the observation (I think the longest time of all the chips) in seconds (not kiloseconds), If this is less the 5000s then the observation is invaild and will be removed from the sample
            #print "Exposure_Time : ", Exposure_Time
            if(Exposure_Time>Max_Exposure_Time):
                Max_Exposure_Time=Exposure_Time
                Max_Exp_Fpath=Cur_Filepath
        Cur_Filepath=Max_Exp_Fpath
        #print type(Obs_ID_L)
        #print Obs_ID_A
        #FGname_A=data["foundName"]
        #FGname_L=list(FGname_A)
        #print FGname_A
        #QGname_A=data["queriedName"] #QGname_A:-Obs_ID_A:-astropy.table.column.Column, Query_Galaxy_Name_Array, The array containing all Query Galaxy Names in the SQL_Standard_File (not indexable)
        """
        QGname_A=data["resolvedObject"] #QGname_A:-Obs_ID_A:-astropy.table.column.Column, Query_Galaxy_Name_Array, The array containing all Query Galaxy Names in the SQL_Standard_File (not indexable)
        QGname_L=list(QGname_A) #QGname_L:-List, Query_Galaxy_Name_Array, The list containing all Query Galaxy Names in the SQL_Standard_File (So it is indexable)
        #print type(QGname_A)
        #print QGname_A
        Matching_Index_List=[] #Matching_Index_List:-List, Matching_Index_List, The list of all indexes (ref. QGname_L) that corresepond to the input Galaxy Name, All arrays are of equal lenth, and "ith" value of an array is the correseponding value for any other arrays "ith" value, so for example Obs_ID_L[228]=794 and the Galaxy in the Observation is QGname_L[228]="NGC 891", Note both lists have the same index
        for i in range(0,len(QGname_L)): # i:-int, i, the "ith" index of QGname_L
            #print "i ", i
            QGname=QGname_L[i] #QGname:-string, Query_Galaxy_Name, The current test Galaxy Name, if this Galaxy name equals the input Galaxy Name (Gname) then this Matching_Index, i (ref. QGname_L) will be appended to the Matching_Index_List
            #QGname_Reduced=QGname.replace(" ", "")
            #print "QGname ", QGname
            #print "QGname_Reduced ", QGname_Reduced
            if(Gname==QGname): #Checks to see if the current test Galaxy Name is the same as the input Galaxy Name, if so it appends the current index (ref. QGname_L) to the Matching_Index_List
                #print "i ", i
                Matching_Index_List.append(i) #Appends the current index (ref. QGname_L) to the Matching_Index_List
        """
        Matching_Index_List=[] #Matching_Index_List:-List, Matching_Index_List, The list of all indexes (ref. QGname_L) that corresepond to the input Galaxy Name, All arrays are of equal lenth, and "ith" value of an array is the correseponding value for any other arrays "ith" value, so for example Obs_ID_L[228]=794 and the Galaxy in the Observation is QGname_L[228]="NGC 891", Note both lists have the same index
        for i in range(0,len(Obs_ID_L)): # i:-int, i, the "ith" index of QGname_L
            #print "i ", i
            QObs_ID=Obs_ID_L[i] #QGname:-string, Query_Galaxy_Name, The current test Galaxy Name, if this Galaxy name equals the input Galaxy Name (Gname) then this Matching_Index, i (ref. QGname_L) will be appended to the Matching_Index_List
            #QGname_Reduced=QGname.replace(" ", "")
            #print "QGname ", QGname
            #print "QGname_Reduced ", QGname_Reduced
            if(Obs_ID==QObs_ID): #Checks to see if the current test Galaxy Name is the same as the input Galaxy Name, if so it appends the current index (ref. QGname_L) to the Matching_Index_List
                #print "i ", i
                Matching_Index_List.append(i) #Appends the current index (ref. QGname_L) to the Matching_Index_List
        RA_Match_L=[] #RA_Match_L:-List, Right_Ascension_Match_List, The list of all source RA's for the input Galaxy Name in decimal degrees
        Dec_Match_L=[] #Dec_Match_L:-List, Declination_Match_List, The list of all source Dec's for the input Galaxy Name in decimal degrees
        for Cur_Matching_Index in Matching_Index_List: #Cur_Matching_Index:-int, Current_Matching_Index, The current index (ref. QGname_L) in the list of matching indexes for the current input Galaxy Name (Matching_Index_List)
            Cur_Match_RA=RA_L[Cur_Matching_Index] #Cur_Match_RA:-numpy.float64, Current_Match_Right_Ascension, The RA of the current source in decimal degrees
            #print type(Cur_Match_RA)
            Cur_Match_Dec=Dec_L[Cur_Matching_Index] #Cur_Match_Dec:-numpy.float64, Current_Match_Declination, The Dec of the current source in decimal degrees
            RA_Match_L.append(Cur_Match_RA) #RA_Match_L:-list, Right_Ascension_Match_List, The list of all source RA's for the input Galaxy Name in decimal degrees
            Dec_Match_L.append(Cur_Match_Dec) #Dec_Match_L:-list, Declination_Match_List, The list of all source Dec's for the input Galaxy Name in decimal degrees
        #print RA_Match_L
        #print len(RA_Match_L)
        #print Dec_Match_L
        #print len(Dec_Match_L)
        #decA=Data['dec']
        #raA=Data['ra']
        #Maj=Maj/3600
        #S_Maj=Maj/2
        #area_T=((S_Maj)**2)*math.pi
        G_Data= Ned.query_object(Gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The Galaxy Data Table queried from NED
        #print type(G_Data)
        D25_S_Maj_Deg=D25_Finder.D25_Finder(Gname)
        area_T=((D25_S_Maj_Deg)**2)*math.pi
        raGC=float(G_Data['RA(deg)'])
        decGC=float(G_Data['DEC(deg)'])
        #print "GC Coords : ", [raGC,decGC]
        #area_A=[((((((decGC-dec)**2)+((raGC-ra)**2)))*(math.pi))/area_T) for dec,ra in zip(decA,raA)]
        #area_A=[((((((decGC-dec)**2)+((raGC-ra)**2)))*(math.pi))/area_T) for dec,ra in zip(Dec_Match_L,RA_Match_L)] #REAL ONE
        #disA=[math.sqrt(((decGC-dec)**2)+((raGC-ra)**2)) for dec,ra in zip(dec_A,raA)] #REAL ONE?
        disA=[math.sqrt(((decGC-dec)**2)+((raGC-ra)**2)) for dec,ra in zip(Dec_Match_L,RA_Match_L)] #REAL ONE #MAJOR BUG HERE!!! This should be calculated with the Haversine_Distance NOT the Pythagorean Theorem!
        #print "disA : ", disA
        #disA.sort()
        print "D25_S_Maj_Deg : ", D25_S_Maj_Deg
        D25_S_Maj_Arcmin=D25_S_Maj_Deg*60.0
        print "D25_S_Maj_Arcmin : ", D25_S_Maj_Arcmin
        Frac_of_Reasonable_FOV=D25_S_Maj_Arcmin/10.0
        print "Frac_of_Reasonable_FOV : ", Frac_of_Reasonable_FOV
        Dist_in_D25_L=[]
        Dist_Outside_D25_L=[]
        for Dist in disA:
            if(Dist<D25_S_Maj_Deg):
                Dist_in_D25_L.append(Dist)
            if(Dist>D25_S_Maj_Deg):
                Dist_Outside_D25_L.append(Dist)
        Num_Sources=len(disA)
        print "Num_Sources : ", Num_Sources
        Num_Sources_in_D25=len(Dist_in_D25_L)
        print "Num_Sources_in_D25 : ", Num_Sources_in_D25
        Num_Sources_Outside_D25=len(Dist_Outside_D25_L)
        print "Num_Sources_Outside_D25 : ", Num_Sources_Outside_D25
        R=float(Num_Sources_Outside_D25)/float(Num_Sources)
        print "R : ", R
        #print "Filepath : ", Filepath
        #print "Cur_Galaxy_Obs_ID_Filepath : ", Cur_Galaxy_Obs_ID_Filepath
        hdul = fits.open(Cur_Filepath)
        #Num_Rows_in_Array=hdul[1].header['NROWS'] #Num_Rows_in_Array:-int, Number of Row in the Array, The number of rows in a (sub)array, if less then 1024 then the observation is a subarray and will be removed from the sample
        #print "Num_Rows_in_Array : ", Num_Rows_in_Array
        #print "type(Num_Rows_in_Array) : ", type(Num_Rows_in_Array)
        Exposure_Time=hdul[1].header['EXPOSURE'] #Exposure_Time:-float, Exposure Time, The Exposure Time of the observation (I think the longest time of all the chips) in seconds (not kiloseconds), If this is less the 5000s then the observation is invaild and will be removed from the sample
        print "Exposure_Time : ", Exposure_Time
        #print "type(Exposure_Time) : ", type(Exposure_Time)
        #Grating_Flag=hdul[1].header['GRATING']
        #print "Grating_Flag : ", Grating_Flag
        #print Grating_Flag
        #Initial_CSV_Line="Gname,Obs_ID,D25_Deg,D25_Arcmin,Num_Sources,Num_Sources_in_D25,Num_Sources_Outside_D25,Ratio\n"
        #Initial_CSV_Line="Gname,Obs_ID,Exposure_Time,D25_Deg,D25_Arcmin,Num_Sources,Num_Sources_in_D25,Num_Sources_Outside_D25,Ratio\n"
        Current_CSV_Line=str(Gname_Modifed)+","+str(Obs_ID)+","+str(Exposure_Time)+","+str(D25_S_Maj_Deg)+","+str(D25_S_Maj_Arcmin)+","+str(Frac_of_Reasonable_FOV)+","+str(Num_Sources)+","+str(Num_Sources_in_D25)+","+str(Num_Sources_Outside_D25)+","+str(R)+"\n"
        f.write(Current_CSV_Line)
        #if(R>D25_Threshold):
            #return True
        #return False
    #Output_Data=pd.read_csv(Current_CSV_Line)
    #print Output_Data
    #Output_D25_L=Output_Data[]
#print Histogram_Organizer("NGC 0253")
#print Histogram_Organizer("NGC 1300")
#print Histogram_Organizer("NGC_253")
#print Histogram_Organizer(["NGC_253","NGC 1300"])
#['NGC 4278', 'NGC 2841', 'NGC 3877', 'MESSIER 106', 'NGC 5194', 'MESSIER 104', 'MESSIER 105', 'MESSIER 101', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'MESSIER 081', 'NGC 0278', 'MESSIER 088', 'NGC 6744', 'IC 5332', 'NGC 3585', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4476', 'NGC 4570', 'NGC 5576', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'NGC 4490', 'IC 1613', 'NGC 4477', 'NGC 4365', 'NGC 2787', 'NGC 3557', 'IC 5267', 'NGC 4388', 'NGC 3923', 'NGC 4945', 'NGC 891', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'UGCA 166', 'NGC 4314', 'NGC 4550', 'Holmberg IX                   ', 'NGC 4559', 'NGC 1399', 'NGC 4039', 'NGC 4038', 'NGC 1316', 'NGC 1097', 'NGC 0383', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4631', 'MESSIER 060', 'NGC 4742', 'NGC 1672', 'NGC 5846', 'NGC 4725', 'NGC 2403', 'NGC 3507', 'MESSIER 087', 'NGC 0891', 'NGC 3384', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 0119', 'NGC 2865', 'MESSIER 059', 'NGC 1427', 'NGC 3628', 'NGC 3608', 'NGC 0055', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521', 'NGC 4565', 'NGC 1313', 'NGC 0253'] #Only Vaild Galaxys in this list
#print Histogram_Organizer(['NGC 4278', 'NGC 2841', 'NGC 3877', 'MESSIER 106', 'NGC 5194', 'MESSIER 104', 'MESSIER 105', 'MESSIER 101', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'MESSIER 081', 'NGC 0278', 'MESSIER 088', 'NGC 6744', 'IC 5332', 'NGC 3585', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4476', 'NGC 4570', 'NGC 5576', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'NGC 4490', 'IC 1613', 'NGC 4477', 'NGC 4365', 'NGC 2787', 'NGC 3557', 'IC 5267', 'NGC 4388', 'NGC 3923', 'NGC 4945', 'NGC 891', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'UGCA 166', 'NGC 4314', 'NGC 4550', 'Holmberg IX                   ', 'NGC 4559', 'NGC 1399', 'NGC 4039', 'NGC 4038', 'NGC 1316', 'NGC 1097', 'NGC 0383', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4631', 'MESSIER 060', 'NGC 4742', 'NGC 1672', 'NGC 5846', 'NGC 4725', 'NGC 2403', 'NGC 3507', 'MESSIER 087', 'NGC 0891', 'NGC 3384', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 0119', 'NGC 2865', 'MESSIER 059', 'NGC 1427', 'NGC 3628', 'NGC 3608', 'NGC 0055', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521', 'NGC 4565', 'NGC 1313', 'NGC 0253'])
print Histogram_Organizer(['NGC 2841', 'NGC 3877', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'NGC 0278', 'MESSIER 088', 'NGC 3585', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4570', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'IC 1613', 'NGC 4477', 'NGC 2787', 'IC 5267', 'NGC 3923', 'NGC 891', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'NGC 4314', 'NGC 4559', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4742', 'NGC 1672', 'NGC 4725', 'NGC 0891', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 2865', 'MESSIER 059', 'NGC 1427', 'NGC 3628', 'NGC 0055', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521']) #These are the 67 galaxies used in the final version of the Master's Thesis
