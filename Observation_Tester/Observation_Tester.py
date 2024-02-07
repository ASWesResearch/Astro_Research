import sys
sys.path=sys.path[:-2]+[sys.path[-1]]+[sys.path[-2]]
print("sys.path: ", sys.path)
import numpy as np
import pandas as pd
import pyds9
import os
from os import system
from astroquery.ned import Ned
from ciao_contrib.runtool import *
#from region import *
from astropy.io import fits
import time
#Constants:
#Root_Path="/Volumes/"
Root_Path="/opt/"
path=os.path.realpath('../')
print("path : ", path)
sys.path.append(os.path.abspath(path))
from File_Query_Code import File_Query_Code_5
from Galaxy_Name_Reducer import Galaxy_Name_Reducer
def Observation_Tester(Gname_L,Simple_Reg_B=False,Max_Exp_B=False,Optical_Bool=True,Outpath="Test_Out.txt"):
    #d = pyds9.DS9()
    Outfile=open(Outpath,"a+")
    Accept_L=[]
    Reject_L=[]
    Question_L=[]
    Warning_L=[]
    Galaxy_Counter=0
    Obs_ID_Counter=0
    Num_Galaxies=len(Gname_L)
    #print "Testing ! ! !"
    Galaxy_Reject_L=[]
    #Galaxy_Index=0
    #while(Galaxy_Index<len(Gname_L)):
    for Gname in Gname_L:
        #Gname=Gname_L[Galaxy_Index]
        Galaxy_Counter=Galaxy_Counter+1
        Reject_Galaxy_Bool=False
        Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
        print("Gname : ",Gname_Modifed)
        G_Data = Ned.query_object(Gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The queryed data of the galaxy from NED in the form of a astropy table
        #print G_Data
        #print type(G_Data)
        #raGC=float(G_Data['RA(deg)']) #raGC:-float, Right Ascension of Galatic Center, The right ascension of the galatic center of the current galaxy in degrees.
        #decGC=float(G_Data['DEC(deg)']) #decGC:-float, Declination of Galatic Center, The declination of the galatic center of the current galaxy in degrees.
        try:
            raGC=float(G_Data['RA(deg)'])  #raGC:-float, Right Ascension of Galatic Center, The right ascension of the galatic center of the current galaxy in degrees.
            decGC=float(G_Data['DEC(deg)']) #decGC:-float, Declination of Galatic Center, The declination of the galatic center of the current galaxy in degrees.
        except:
            raGC=float(G_Data['RA'])  #raGC:-float, Right Ascension of Galatic Center, The right ascension of the galatic center of the current galaxy in degrees.
            decGC=float(G_Data['DEC']) #decGC:-float, Declination of Galatic Center, The declination of the galatic center of the current galaxy in degrees.
        if(Max_Exp_B):
            #print "Test: True"
            Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2",Obs_Check_B=False,Exp_Max_B=True)
            #print "Evt2_File_H_L Exp_Max_B=True : ", Evt2_File_H_L
            Reg_File_H_L=File_Query_Code_5.File_Query(Gname,"reg",".reg",Obs_Check_B=False)
            Fov_File_H_L=File_Query_Code_5.File_Query(Gname,"fov1",Obs_Check_B=False)
        else:
            #print "TEST: False"
            Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2",Obs_Check_B=False)
            Reg_File_H_L=File_Query_Code_5.File_Query(Gname,"reg",".reg",Obs_Check_B=False)
            Fov_File_H_L=File_Query_Code_5.File_Query(Gname,"fov1",Obs_Check_B=False)
        #/Volumes/xray/anthony/Thesis/Galaxy_Optical_Image_Query/Galaxy_Optical_Images/MESSIER_066
        D25_Region_Path=Root_Path+"xray/anthony/Thesis/Galaxy_Optical_Image_Query/Galaxy_Optical_Images/"+Gname_Modifed+"/"+Gname_Modifed+".reg"
        print("Evt2_File_H_L ", Evt2_File_H_L)
        #print "Fov_File_H_L ", Fov_File_H_L
        for Evt2_File_L in Evt2_File_H_L:
            Cur_Evt2_ObsID=Evt2_File_L[0]
            Cur_Evt2_Filepath=Evt2_File_L[1]
            for Fov_File_L in Fov_File_H_L:
                Cur_Fov_ObsID=Fov_File_L[0]
                Cur_Fov_Filepath=Fov_File_L[1]
                print("Cur_Fov_Filepath: ", Cur_Fov_Filepath)
                if(Cur_Evt2_ObsID==Cur_Fov_ObsID):
                    print("Cur_Evt2_ObsID : ", Cur_Evt2_ObsID)
                    for Reg_File_L in Reg_File_H_L:
                        Cur_Reg_ObsID=Reg_File_L[0]
                        Cur_Reg_Filepath=Reg_File_L[1]
                        if(Cur_Evt2_ObsID==Cur_Reg_ObsID):
                            Obs_ID_Counter=Obs_ID_Counter+1
                            Obs_Info_L=[Gname,Cur_Evt2_ObsID]
                            print("Obs_Info_L : ", Obs_Info_L)
                            dmcoords(infile=str(Cur_Evt2_Filepath),ra=str(raGC), dec=str(decGC), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the GC to SKY coodinates in pixels (?)
                            X_Phys=dmcoords.x #X_Phys:-float, X_Physical, The sky plane X pixel coordinate in units of pixels of the galatic center
                            Y_Phys=dmcoords.y #Y_Phys:-float, Y_Physical, The sky plane Y pixel coordinate in units of pixels of the galatic center
                            Chip_ID=dmcoords.chip_id #Chip_ID:-int, Chip_ID, The Chip ID number the GC is on
                            GC_Coords=[X_Phys,Y_Phys,Chip_ID]
                            print("GC_Coords : ", GC_Coords)
                            hdul = fits.open(Cur_Evt2_Filepath)
                            Num_Rows_in_Array=hdul[1].header['NROWS'] #Num_Rows_in_Array:-int, Number of Row in the Array, The number of rows in a (sub)array, if less then 1024 then the observation is a subarray and will be removed from the sample
                            print("Num_Rows_in_Array : ", Num_Rows_in_Array)
                            #print "type(Num_Rows_in_Array) : ", type(Num_Rows_in_Array)
                            Exposure_Time=hdul[1].header['EXPOSURE'] #Exposure_Time:-float, Exposure Time, The Exposure Time of the observation (I think the longest time of all the chips) in seconds (not kiloseconds), If this is less the 5000s then the observation is invaild and will be removed from the sample
                            print("Exposure_Time : ", Exposure_Time)
                            #print "type(Exposure_Time) : ", type(Exposure_Time)
                            Grating_Flag=hdul[1].header['GRATING']
                            print("Grating_Flag : ", Grating_Flag)
                            #print Grating_Flag
                            Roll_Angle=hdul[1].header['ROLL_PNT']
                            print("Roll_Angle : ", Roll_Angle)
                            if((Num_Rows_in_Array!=1024) or (Exposure_Time<5000) or (Grating_Flag!="NONE")): #Checks to see if the current observation is invaild (invalid if: it is a subarray or has an exposure time less then 5000s)
                                Warning_L.append(Obs_Info_L)
                                print("Warning Current Observaton Automatically Detected As Invalid ! ! !")
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
                                print("Simple_Region_Filepath : ", Simple_Region_Filepath)
                                #print "Master_Out_LS : ", Master_Out_LS
                                #Master_Out_LS_L=Master_Out_LS.split("\n")
                            #print "Master_Out_LS_L : ", Master_Out_LS_L
                            #if(Reject_Galaxy_Bool==False):
                            d = pyds9.DS9()
                            #d.set("file "+str(Cur_Evt2_Filepath)+" -regions "+str(Cur_Fov_Filepath))
                            d.set("file "+str(Cur_Evt2_Filepath))
                            d.set("regions " + str(Cur_Fov_Filepath))
                            print("Cur_Fov_Filepath: ", Cur_Fov_Filepath)
                            if(Simple_Reg_B==True):
                                d.set("regions " + str(Simple_Region_Filepath))
                            #d.set("regions " + str(Cur_Reg_Filepath))
                            d.set("regions " + str(D25_Region_Path))
                            d.set("regions " + str(Cur_Reg_Filepath))
                            d.set("regions system wcs")
                            Outpath_Region_WCS=Root_Path+"xray/anthony/Research_Git/Observation_Tester/Converted_Regions/"+str(Cur_Evt2_ObsID)+"_Source_WCS.reg"
                            d.set("regions save "+Outpath_Region_WCS)
                            d.set("scale log")
                            d.set("bin buffersize 8192")
                            d.set("zoom to fit")
                            if(Optical_Bool):
                                D25_File_Path=Root_Path+"xray/anthony/Thesis/Galaxy_Optical_Image_Query/Galaxy_Optical_Images/"+Gname_Modifed+"/"+Gname_Modifed+".fit"
                                d.set("frame new")
                                d.set("file "+str(D25_File_Path))
                                d.set("tile yes")
                                d.set("frame first")
                                d.set("match frame wcs")
                                d.set("lock frame wcs")
                                d.set("frame prev")
                                #d.set("region sky fk5")
                                #d.set("regions " + str(Cur_Fov_Filepath))
                                ##d.set("regions " + str(D25_Region_Path))
                                d.set("regions " + str(Outpath_Region_WCS))
                                #d.set("regions system physical")
                                #d.set("regions system wcs")
                                ##d.set("regions " + str(Cur_Fov_Filepath))
                                ##d.set("regions " + str(Cur_Reg_Filepath))
                                d.set("frame first")
                            #d.set("region load all " + str(Cur_Fov_Filepath))
                            #d.set("region load all " + str(Cur_Reg_Filepath))
                            #d.set("region load all " + str(D25_Region_Path))
                            if(Reject_Galaxy_Bool):
                                Obs_Info_L.append("Galaxy Rejected")
                                Reject_L.append(Obs_Info_L)
                                #Galaxy_Reject_L.append(Gname)
                            else:
                                User_Input=input("y,n, RG or q :\n")
                                if(User_Input=="RG"):
                                    Reject_Galaxy_Bool=True
                                    Galaxy_Reject_L.append(Gname)
                                    Obs_Info_L.append("Galaxy Rejected")
                                    Reject_L.append(Obs_Info_L)
                                if((User_Input=="y") or (User_Input=="Y")):
                                    #Accept_L.append(Obs_Info_L)
                                    User_Input_Source_Check=input("Check Sources?: y,n or q :\n")
                                    if((User_Input_Source_Check=="n") or (User_Input_Source_Check=="N")):
                                        Accept_L.append(Obs_Info_L)
                                    if((User_Input_Source_Check=="y") or (User_Input_Source_Check=="Y")):
                                        #/opt/xray/anthony/expansion_backup/Hybrid_Regions/316/Nearest_Neighbor_Hybrid_Sources_ObsID_316_Coords.csv
                                        Coords_Path=Root_Path+"xray/anthony/expansion_backup/Hybrid_Regions/"+str(Cur_Evt2_ObsID)+"/Nearest_Neighbor_Hybrid_Sources_ObsID_"+str(Cur_Evt2_ObsID)+"_Coords.csv"
                                        Data_Coords=pd.read_csv(Coords_Path)
                                        Source_Phys_X_L=list(Data_Coords["Phys_X"])
                                        Source_Phys_Y_L=list(Data_Coords["Phys_Y"])
                                        print("Source_Phys_X_L: ", Source_Phys_X_L)
                                        print("Source_Phys_Y_L: ", Source_Phys_Y_L)
                                        Num_Sources=len(Source_Phys_X_L)
                                        print("Number of Sources: ", Num_Sources)
                                        #for i in range(0,len(Source_Phys_X_L)):
                                        #Batch_List=[10,5,1]
                                        #for i in range(0,int(Num_Sources/15)):
                                        Source_Reject_L=[]
                                        for i in range(0,int(Num_Sources)):
                                        #while(i<int(Num_Sources)):
                                            t0 = time.time()
                                            print("i: ", i)
                                            Source_Num=i+1
                                            print("Source_Num: ", Source_Num)
                                            Source_Phys_X=Source_Phys_X_L[i]
                                            Source_Phys_Y=Source_Phys_Y_L[i]
                                            #/opt/xray/anthony/expansion_backup/Hybrid_Regions/316/Individual_Source_Regions/Source_1_ObsID_316_Nearest_Neighbor_Hybrid.reg
                                            Individual_Source_Path=Root_Path+"xray/anthony/expansion_backup/Hybrid_Regions/"+str(Cur_Evt2_ObsID)+"/Individual_Source_Regions/Source_"+str(Source_Num)+"_ObsID_"+str(Cur_Evt2_ObsID)+"_Nearest_Neighbor_Hybrid.reg"
                                            with open(Individual_Source_Path) as f:
                                                lines = f.readlines()
                                            Region_Str = lines[2]
                                            print("Region_Str: ", Region_Str)
                                            #d.set("regions override color yes") #Note: I am not sure if this works!
                                            d.set("region edit yes")
                                            #d.set("region select back")
                                            #d.set("regions color yellow")
                                            d.set("region select all")
                                            d.set("regions " + str(Individual_Source_Path))
                                            d.set("region select invert")
                                            #d.set("region select back")
                                            #d.set("region select all")
                                            d.set("regions color yellow")
                                            #d.set("regions " + str(Individual_Source_Path)+" color yellow")
                                            #d.set("regions color yellow regions" + str(Individual_Source_Path))
                                            #d.set('region command '+Region_Str+' color=yellow')
                                            d.set("region move front")
                                            #d.set("pan 200 200")
                                            #d.set("pan open")
                                            print("Source_Phys_X: ", Source_Phys_X)
                                            print("Source_Phys_Y: ", Source_Phys_Y)
                                            d.set("pan to "+str(Source_Phys_X)+" "+str(Source_Phys_Y)+" physical")
                                            #d.set("pan to 500 500 physical")
                                            #d.set("zoom to 2")
                                            d.set("zoom to 1")
                                            Individual_Source_Outpath_Region_WCS=Root_Path+"xray/anthony/Research_Git/Observation_Tester/Converted_Regions/"+str(Cur_Evt2_ObsID)+"_Source_"+str(Source_Num)+"_WCS.reg"
                                            d.set("region save select "+Individual_Source_Outpath_Region_WCS)
                                            d.set("frame next")
                                            d.set("region select all")
                                            d.set("regions " + str(Individual_Source_Outpath_Region_WCS))
                                            d.set("region select invert")
                                            d.set("regions color yellow")
                                            d.set("region move front")
                                            d.set("frame prev")
                                            t1 = time.time()
                                            total_time = t1-t0
                                            print("total_time: ", total_time)
                                            User_Input_Source=input("Source "+str(Source_Num)+": y,n or q :\n")
                                            if((User_Input_Source=="n") or (User_Input_Source=="N")):
                                                Source_Reject_L.append(Source_Num)
                                            #d.set("frame prev")
                                            d.set("regions color magenta")
                                            d.set("frame next")
                                            d.set("regions color magenta")
                                            d.set("frame prev")
                                        Obs_Info_L.append(Source_Reject_L)
                                        Accept_L.append(Obs_Info_L)
                                        d.set("regions select none")
                                        d.set("regions color green")
                                if((User_Input=="n") or (User_Input=="N")):
                                    #Reject_L.append(Obs_Info_L)
                                    Rejection_Reason_Input=input("Reasoning: ")
                                    if(Rejection_Reason_Input!=""):
                                        Obs_Info_L.append(Rejection_Reason_Input)
                                    Reject_L.append(Obs_Info_L)
                                if((User_Input=="q") or (User_Input=="Q")):
                                    #Reject_L.append(Obs_Info_L)
                                    Rejection_Reason_Input=input("Reasoning: ")
                                    if(Rejection_Reason_Input!=""):
                                        Obs_Info_L.append(Rejection_Reason_Input)
                                    Question_L.append(Obs_Info_L)
                                Print_Input=input("p to print update: ")
                                if((Print_Input=="p") or (Print_Input=="P")):
                                    print("Accept_L : \n", Accept_L)
                                    print("Reject_L : \n", Reject_L)
                                    print("Question_L : \n", Question_L)
                                    print("Warning_L : \n", Warning_L)
                                    print("Galaxy_Reject_L: \n", Galaxy_Reject_L)
                                    Update_String=str(Galaxy_Counter)+" Out of "+str(Num_Galaxies)+" Galaxies Checked : "+str(Obs_ID_Counter)+" Observations Checked"
                                    print(Update_String)
                                Outstring="Accept_L: "+str(Accept_L)+"\n"+"Reject_L: "+str(Reject_L)+"\n"
                                Outfile.write(Outstring)
                            #d.set("regions color green")
                            d.set("frame prev")
                            d.set("frame delete")
        #Galaxy_Index=Galaxy_Index+1


    print("Accept_L : \n", Accept_L)
    print("Reject_L : \n", Reject_L)
    print("Question_L : \n", Question_L)
    print("Warning_L : \n", Warning_L)
    print("Galaxy_Reject_L: \n", Galaxy_Reject_L)

def TEST():
    import glob
    #dir_ = os.path.dirname(__file__)
    dir_="/opt/anaconda3/envs/ciao-4.14/lib/python3.9/site-packages/"
    print("dir_", dir_)
    libxpa = glob.glob(os.path.join(dir_, "libxpa*so*"))
    print("libxpa: ", libxpa)
    d = pyds9.DS9()




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
#Observation_Tester(["NGC 253","NGC 5813"],Max_Exp_B=True)
#Observation_Tester(["NGC 3631"])
#Observation_Tester(["MESSIER 049"], Max_Exp_B=True)
#Observation_Tester(["MESSIER 049"])
Observation_Tester(["MESSIER 049", "MESSIER 063"])
#print(File_Query("MESSIER 049","evt2"))
#TEST()
