import pyds9
import os
from os import system
import sys
from astroquery.ned import Ned
from ciao_contrib.runtool import *
#from region import *
from astropy.io import fits
path=os.path.realpath('../')
print "path : ", path
sys.path.append(os.path.abspath(path))
from File_Query_Code import File_Query_Code_5
from Galaxy_Name_Reducer import Galaxy_Name_Reducer
def Observation_Tester(Gname_L,Simple_Reg_B=False,Max_Exp_B=False):
    #d = pyds9.DS9()
    Accept_L=[]
    Reject_L=[]
    Question_L=[]
    Warning_L=[]
    Galaxy_Counter=0
    Obs_ID_Counter=0
    Num_Galaxies=len(Gname_L)
    #print "Testing ! ! !"
    for Gname in Gname_L:
        Galaxy_Counter=Galaxy_Counter+1
        Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
        print "Gname : ",Gname_Modifed
        G_Data = Ned.query_object(Gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The queryed data of the galaxy from NED in the form of a astropy table
        #print G_Data
        #print type(G_Data)
        raGC=float(G_Data['RA(deg)']) #raGC:-float, Right Ascension of Galatic Center, The right ascension of the galatic center of the current galaxy in degrees.
        decGC=float(G_Data['DEC(deg)']) #decGC:-float, Declination of Galatic Center, The declination of the galatic center of the current galaxy in degrees.
        if(Max_Exp_B):
            print "Test: True"
            Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2",Obs_Check_B=False,Exp_Max_B=True)
            #print "Evt2_File_H_L : ", Evt2_File_H_L
            Reg_File_H_L=File_Query_Code_5.File_Query(Gname,"reg",".reg",Obs_Check_B=False)
            Fov_File_H_L=File_Query_Code_5.File_Query(Gname,"fov1",Obs_Check_B=False)
        else:
            print "TEST: False"
            Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2",Obs_Check_B=False)
            Reg_File_H_L=File_Query_Code_5.File_Query(Gname,"reg",".reg",Obs_Check_B=False)
            Fov_File_H_L=File_Query_Code_5.File_Query(Gname,"fov1",Obs_Check_B=False)
        #/Volumes/xray/anthony/Thesis/Galaxy_Optical_Image_Query/Galaxy_Optical_Images/MESSIER_066
        D25_Region_Path="/Volumes/xray/anthony/Thesis/Galaxy_Optical_Image_Query/Galaxy_Optical_Images/"+Gname_Modifed+"/"+Gname_Modifed+".reg"
        #print "Evt2_File_H_L ", Evt2_File_H_L
        #print "Fov_File_H_L ", Fov_File_H_L
        for Evt2_File_L in Evt2_File_H_L:
            Cur_Evt2_ObsID=Evt2_File_L[0]
            Cur_Evt2_Filepath=Evt2_File_L[1]
            for Fov_File_L in Fov_File_H_L:
                Cur_Fov_ObsID=Fov_File_L[0]
                Cur_Fov_Filepath=Fov_File_L[1]
                if(Cur_Evt2_ObsID==Cur_Fov_ObsID):
                    print "Cur_Evt2_ObsID : ", Cur_Evt2_ObsID
                    for Reg_File_L in Reg_File_H_L:
                        Cur_Reg_ObsID=Reg_File_L[0]
                        Cur_Reg_Filepath=Reg_File_L[1]
                        if(Cur_Evt2_ObsID==Cur_Reg_ObsID):
                            Obs_ID_Counter=Obs_ID_Counter+1
                            Obs_Info_L=[Gname,Cur_Evt2_ObsID]
                            print "Obs_Info_L : ", Obs_Info_L
                            dmcoords(infile=str(Cur_Evt2_Filepath),ra=str(raGC), dec=str(decGC), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the GC to SKY coodinates in pixels (?)
                            X_Phys=dmcoords.x #X_Phys:-float, X_Physical, The sky plane X pixel coordinate in units of pixels of the galatic center
                            Y_Phys=dmcoords.y #Y_Phys:-float, Y_Physical, The sky plane Y pixel coordinate in units of pixels of the galatic center
                            Chip_ID=dmcoords.chip_id #Chip_ID:-int, Chip_ID, The Chip ID number the GC is on
                            GC_Coords=[X_Phys,Y_Phys,Chip_ID]
                            print "GC_Coords : ", GC_Coords
                            hdul = fits.open(Cur_Evt2_Filepath)
                            Num_Rows_in_Array=hdul[1].header['NROWS'] #Num_Rows_in_Array:-int, Number of Row in the Array, The number of rows in a (sub)array, if less then 1024 then the observation is a subarray and will be removed from the sample
                            print "Num_Rows_in_Array : ", Num_Rows_in_Array
                            #print "type(Num_Rows_in_Array) : ", type(Num_Rows_in_Array)
                            Exposure_Time=hdul[1].header['EXPOSURE'] #Exposure_Time:-float, Exposure Time, The Exposure Time of the observation (I think the longest time of all the chips) in seconds (not kiloseconds), If this is less the 5000s then the observation is invaild and will be removed from the sample
                            print "Exposure_Time : ", Exposure_Time
                            #print "type(Exposure_Time) : ", type(Exposure_Time)
                            Grating_Flag=hdul[1].header['GRATING']
                            print "Grating_Flag : ", Grating_Flag
                            #print Grating_Flag
                            if((Num_Rows_in_Array!=1024) or (Exposure_Time<5000) or (Grating_Flag!="NONE")): #Checks to see if the current observation is invaild (invalid if: it is a subarray or has an exposure time less then 5000s)
                                Warning_L.append(Obs_Info_L)
                                print "Warning Current Observaton Automatically Detected As Invalid ! ! !"
                            if(Simple_Reg_B==True):
                                Master_Out_Path=os.path.realpath('../Master_Code/Master_Output/'+Gname_Modifed+'/Area_Lists/'+str(Cur_Evt2_ObsID)+'/')
                                #print "Master_Out_Path : ", Master_Out_Path
                                Master_Out_LS= os.popen("ls "+Master_Out_Path).read()
                                #print "Master_Out_LS : ", Master_Out_LS
                                Master_Out_LS_L=Master_Out_LS.split("\n")
                                #print "Master_Out_LS_L : ", Master_Out_LS_L
                                for Master_Fname in Master_Out_LS_L:
                                    #print "Master_Fname : ", Master_Fname
                                    if("simple_region_modifed" in Master_Fname):
                                        Simple_Region_Filename=Master_Fname
                                Simple_Region_Filepath=Master_Out_Path+"/"+Simple_Region_Filename
                                print "Simple_Region_Filepath : ", Simple_Region_Filepath
                                #print "Master_Out_LS : ", Master_Out_LS
                                #Master_Out_LS_L=Master_Out_LS.split("\n")
                            #print "Master_Out_LS_L : ", Master_Out_LS_L
                            d = pyds9.DS9()
                            #d.set("file "+str(Cur_Evt2_Filepath)+" -regions "+str(Cur_Fov_Filepath))
                            d.set("file "+str(Cur_Evt2_Filepath))
                            d.set("regions " + str(Cur_Fov_Filepath))
                            if(Simple_Reg_B==True):
                                d.set("regions " + str(Simple_Region_Filepath))
                            d.set("regions " + str(Cur_Reg_Filepath))
                            d.set("regions " + str(D25_Region_Path))
                            d.set("scale log")
                            d.set("bin buffersize 8192")
                            d.set("zoom to fit")
                            User_Input=raw_input("y,n or q :\n")
                            if((User_Input=="y") or (User_Input=="Y")):
                                Accept_L.append(Obs_Info_L)
                            if((User_Input=="n") or (User_Input=="N")):
                                #Reject_L.append(Obs_Info_L)
                                Rejection_Reason_Input=raw_input("Reasoning: ")
                                if(Rejection_Reason_Input!=""):
                                    Obs_Info_L.append(Rejection_Reason_Input)
                                Reject_L.append(Obs_Info_L)
                            if((User_Input=="q") or (User_Input=="Q")):
                                #Reject_L.append(Obs_Info_L)
                                Rejection_Reason_Input=raw_input("Reasoning: ")
                                if(Rejection_Reason_Input!=""):
                                    Obs_Info_L.append(Rejection_Reason_Input)
                                Question_L.append(Obs_Info_L)
                            Print_Input=raw_input("p to print update: ")
                            if((Print_Input=="p") or (Print_Input=="P")):
                                print "Accept_L : \n", Accept_L
                                print "Reject_L : \n", Reject_L
                                print "Question_L : \n", Question_L
                                print "Warning_L : \n", Warning_L
                                Update_String=str(Galaxy_Counter)+" Out of "+str(Num_Galaxies)+" Galaxies Checked : "+str(Obs_ID_Counter)+" Observations Checked"
                                print Update_String
    print "Accept_L : \n", Accept_L
    print "Reject_L : \n", Reject_L
    print "Question_L : \n", Question_L
    print "Warning_L : \n", Warning_L




#Observation_Tester(["NGC 253"])
#Observation_Tester(['NGC 4278', 'NGC 5204', 'NGC 2841', 'NGC 3877', 'MESSIER 106', 'NGC 5194', 'MESSIER 104', 'MESSIER 105', 'MESSIER 101', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'MESSIER 081', 'NGC 0278', 'MESSIER 088', 'NGC 1042', 'NGC 6744', 'IC 5332', 'NGC 3585', 'NGC 4478', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4476', 'NGC 4570', 'NGC 5576', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'NGC 0247', 'NGC 4490', 'IC 1613', 'NGC 4477', 'NGC 4365', 'NGC 2787', 'NGC 3557', 'IC 5267', 'NGC 4388', 'NGC 3923', 'NGC 4945', 'NGC 891', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'UGCA 166', 'NGC 4314', 'NGC 4550', 'Holmberg IX                   ', 'NGC 4559', 'IC 1459', 'NGC 1399', 'NGC 4039', 'NGC 4038', 'NGC 1316', 'NGC 1097', 'NGC 0383', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4631', 'NGC 4308', 'MESSIER 060', 'NGC 4742', 'NGC 1672', 'NGC 5846', 'NGC 4725', 'NGC 2403', 'NGC 3507', 'MESSIER 087', 'NGC 0891', 'NGC 4698', 'NGC 3384', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 4527', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 0119', 'NGC 2865', 'Circinus Galaxy               ', 'MESSIER 059', 'NGC 7331', 'NGC 1427', 'NGC 3628', 'NGC 3608', 'NGC 0055', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521','NGC 4565', 'NGC 1313', 'NGC 0253'])

#Observation_Tester(['NGC 4278', 'NGC 2841', 'NGC 3877', 'NGC 5194', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'NGC 0278', 'MESSIER 088', 'NGC 3585', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4570', 'NGC 5576', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'IC 1613', 'NGC 4477', 'NGC 4365', 'NGC 2787', 'NGC 3557', 'IC 5267', 'NGC 4388', 'NGC 3923', 'NGC 891', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'UGCA 166', 'NGC 4314', 'NGC 4550', 'Holmberg IX                   ', 'NGC 4559', 'NGC 1399', 'NGC 1316', 'NGC 1097', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4631', 'MESSIER 060', 'NGC 4742', 'NGC 1672', 'NGC 5846', 'NGC 4725', 'NGC 3507', 'MESSIER 087', 'NGC 0891', 'NGC 3384', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 0119', 'NGC 2865', 'MESSIER 059', 'NGC 1427', 'NGC 3628', 'NGC 3608', 'NGC 0055', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521', 'NGC 4565', 'NGC 1313'],Simple_Reg_B=False, Max_Exp_B=True)
#Observation_Tester(["NGC 1313"])
#Observation_Tester(["MESSIER_083"])
#Observation_Tester(["NGC 3608"])
#Observation_Tester(["NGC 4457","NGC 5813","NGC 3631"])
#Observation_Tester(['NGC 4278', 'NGC 5194', 'NGC 5054', 'NGC 5813', 'MESSIER 061', 'MESSIER 086', 'MESSIER 084', 'NGC 7507', 'NGC 4473', 'NGC 5576', 'NGC 4321', 'NGC 4477', 'NGC 4365', 'NGC 3557', 'NGC 4388', 'NGC 4314', 'NGC 4550', 'Holmberg IX                   ', 'NGC 1399', 'NGC 1316', 'NGC 1097', 'NGC 2681', 'NGC 5018', 'NGC 4631', 'MESSIER 060', 'NGC 5846', 'NGC 3507', 'MESSIER 087', 'NGC 3384', 'NGC 6946', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'MESSIER 059', 'NGC 3608', 'NGC 4459', 'NGC 4565'],Max_Exp_B=True)
#NGC 5813
#Observation_Tester(["NGC 5813"])
#NGC 4473
#Observation_Tester(["NGC 4473"])
#NGC_4321
#Observation_Tester(["NGC_4321"])
#Holmberg IX
#Observation_Tester(["Holmberg IX"])
#NGC 4631
#Observation_Tester(["NGC 4631"])
#NGC 3507
#Observation_Tester(["NGC 3507"])
#NGC 3608
#Observation_Tester(["NGC 3608"])
#Observation_Tester(["NGC 1313"])
