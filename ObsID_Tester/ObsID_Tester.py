from astropy.io import fits
import glob
def ObsID_Tester(ObsID_L):
    Subarray_Fail_L=[]
    Exposure_Time_Fail_L=[]
    Grating_Fail_L=[]
    for ObsID in ObsID_L:
        obsid=ObsID
        Evt2_Fpath_L = glob.glob("/Volumes/xray/simon/all_chandra_observations/" + str(obsid) + "/primary/*_evt2.fit*")
        Evt2_Fpath=Evt2_Fpath_L[0]
        print "Evt2_Fpath: ", Evt2_Fpath
        hdul = fits.open(Evt2_Fpath)
        Num_Rows_in_Array=hdul[1].header['NROWS'] #Num_Rows_in_Array:-int, Number of Row in the Array, The number of rows in a (sub)array, if less then 1024 then the observation is a subarray and will be removed from the sample
        print "Num_Rows_in_Array : ", Num_Rows_in_Array
        #print "type(Num_Rows_in_Array) : ", type(Num_Rows_in_Array)
        Exposure_Time=hdul[1].header['EXPOSURE'] #Exposure_Time:-float, Exposure Time, The Exposure Time of the observation (I think the longest time of all the chips) in seconds (not kiloseconds), If this is less the 5000s then the observation is invaild and will be removed from the sample
        print "Exposure_Time : ", Exposure_Time
        #print "type(Exposure_Time) : ", type(Exposure_Time)
        Grating_Flag=hdul[1].header['GRATING']
        print "Grating_Flag : ", Grating_Flag
        #print Grating_Flag
        #if((Num_Rows_in_Array!=1024) or (Exposure_Time<5000) or (Grating_Flag!="NONE")): #Checks to see if the current observation is invaild (invalid if: it is a subarray or has an exposure time less then 5000s)
        if((Num_Rows_in_Array!=1024) or (Exposure_Time<6000) or (Grating_Flag!="NONE")): #Checks to see if the current observation is invaild (invalid if: it is a subarray or has an exposure time less then 6000s)
            print "Warning Current Observaton Automatically Detected As Invalid ! ! !"
        if((Num_Rows_in_Array!=1024)):
            print str(ObsID)+": Subarray"
            Subarray_Fail_L.append(ObsID)
        #if((Exposure_Time<5000)):
        if((Exposure_Time<6000)):
            Exposure_Time_Fail_L.append(ObsID)
            print str(ObsID)+": Short Exposure Time"
        if((Grating_Flag!="NONE")):
            Grating_Fail_L.append(ObsID)
            print str(ObsID)+": Grating"
    print "Subarray_Fail_L:\n", Subarray_Fail_L
    print "len(Subarray_Fail_L) :", len(Subarray_Fail_L)
    print "Exposure_Time_Fail_L:\n", Exposure_Time_Fail_L
    print "len(Exposure_Time_Fail_L) : ", len(Exposure_Time_Fail_L)
    print "Grating_Fail_L:\n", Grating_Fail_L
    print "len(Grating_Fail_L): ", len(Grating_Fail_L)
    #return Subarray_Fail_L,Exposure_Time_Fail_L,Grating_Fail_L

#All ObsIDs from Query (Old) (306 ObsIDs)
print ObsID_Tester(['10125', '1043', '10534', '10875', '10985', '10986', '11104', '11229', '11269', '11271', '11344', '11358', '11674', '11775', '11779', '11781', '11782', '11783', '11784', '11978', '11979', '11988', '11989', '12019', '12095', '12124', '12130', '12134', '12136', '12437', '12562', '12668', '12888', '12889', '12951', '12952', '12953', '12988', '12990', '12992', '12995', '13202', '13246', '13247', '13253', '13255', '13726', '13727', '13791', '13830', '13831', '13832', '14031', '14332', '14342', '14412', '15383', '15384', '1563', '1575', '1576', '1579', '1580', '1581', '1582', '1584', '1586', '1587', '16024', '1611', '1618', '1619', '1622', '1730', '1881', '1967', '1971', '1972', '2014', '2015', '2020', '2022', '2023', '2024', '2025', '2026', '2027', '2030', '2031', '2032', '2039', '2040', '2048', '2049', '2050', '2055', '2056', '2057', '2058', '2059', '2060', '2061', '2062', '2064', '2066', '2067', '2068', '2069', '2070', '2073', '2079', '2107', '2147', '2149', '2196', '2197', '2198', '2223', '2241', '2255', '2454', '2686', '2707', '2779', '2894', '2895', '2896', '2897', '2899', '2900', '2901', '2902', '2915', '2922', '2933', '2950', '2976', '3008', '3040', '3042', '3043', '3044', '308', '310', '311', '314', '3149', '3150', '321', '3217', '322', '3355', '350', '352', '354', '3550', '3551', '3554', '3717', '3718', '379', '3810', '383', '390', '3908', '3931', '3933', '3945', '3947', '3950', '3951', '3954', '4017', '404', '4169', '4177', '4360', '4372', '4404', '4536', '4541', '4613', '4628', '4629', '4630', '4631', '4632', '4633', '4688', '4689', '4725', '4726', '4732', '4736', '4741', '4742', '4743', '4747', '4748', '4750', '517', '5197', '5309', '5905', '5908', '5929', '5930', '5931', '5932', '5935', '5936', '5937', '5938', '5939', '5940', '5941', '5942', '5943', '5944', '5945', '5946', '5947', '5948', '5949', '6096', '6114', '6131', '6152', '6167', '6376', '6377', '6380', '6381', '6383', '6385', '6386', '6389', '6862', '6868', '6869', '6870', '6871', '6872', '6873', '7060', '7073', '7074', '7075', '7076', '7077', '7078', '7079', '7080', '7081', '7153', '7154', '7196', '7197', '7198', '7199', '7252', '735', '7635', '766', '768', '7848', '785', '7853', '786', '788', '793', '794', '797', '803', '8041', '8047', '805', '8050', '8057', '8063', '8107', '8182', '8210', '8507', '8554', '9100', '9120', '9121', '9122', '934', '9506', '9507', '9510', '952', '9527', '9530', '9532', '9535', '9540', '9546', '9548', '9550', '9551', '9552', '9553', '9810'])
