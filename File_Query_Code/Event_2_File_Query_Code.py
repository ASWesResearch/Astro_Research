from astropy.io import ascii
import os
def Event_2_File_Query(Gname):
    data = ascii.read("/home/asantini/Desktop/SQL_Standard_File/SQL_Sandard_File.csv")
    #print data
    #Standard_File=open("/home/asantini/Desktop/SQL_Standard_File/SQL_Sandard_File.csv","r")
    #print Standard_File
    Obs_ID_A=data["obsid"]
    Obs_ID_L=list(Obs_ID_A)
    #print "Obs_ID_L ", Obs_ID_L
    #print type(Obs_ID_L)
    #print Obs_ID_A
    FGname_A=data["foundName"]
    FGname_L=list(FGname_A)
    #print FGname_A
    QGname_A=data["queriedName"]
    QGname_L=list(QGname_A)
    #print type(QGname_A)
    #print QGname_A
    Matching_Index_List=[]
    for i in range(0,len(QGname_L)):
        QGname=QGname_L[i]
        #QGname_Reduced=QGname.replace(" ", "")
        #print "QGname ", QGname
        #print "QGname_Reduced ", QGname_Reduced
        if(Gname==QGname):
            Matching_Index_List.append(i)
    Matching_Obs_ID_L=[]
    for Cur_Matching_Index in Matching_Index_List:
        Cur_Matching_Obs_ID=Obs_ID_L[Cur_Matching_Index]
        if(Cur_Matching_Obs_ID not in Matching_Obs_ID_L):
            Matching_Obs_ID_L.append(Cur_Matching_Obs_ID)
    #print "Matching_Index_List ", Matching_Index_List
    print "Matching_Obs_ID_L ", Matching_Obs_ID_L
    for Cur_Obs_ID in Matching_Obs_ID_L:
        #print "Cur_Obs_ID ", Cur_Obs_ID
        #print "type(Cur_Obs_ID) ", type(Cur_Obs_ID)
        Cur_Obs_ID_Str=str(Cur_Obs_ID)
        #print "type(Cur_Obs_ID_Str) ", type(Cur_Obs_ID_Str)
        os.chdir("/Volumes/xray/simon/chandra_from_csc/")
        retval = os.getcwd()
        #print "type(retval) ", type(retval)
        print "Directory changed successfully %s" % retval  #Checks the this line and the line above it combined check what the current working directory is
        LS_Str_In_CSC= os.popen("ls").read()
        #print "LS_Str_In_CSC ", LS_Str_In_CSC
        #print "type(LS_Str_In_CSC) ", type(LS_Str_In_CSC)
        LS_Str_In_CSC_L=LS_Str_In_CSC.split("\n")
        print "LS_Str_In_CSC_L ", LS_Str_In_CSC_L
        #print "type(LS_Str_In_CSC_L) ", type(LS_Str_In_CSC_L)
        if(Cur_Obs_ID_Str in LS_Str_In_CSC_L):
            os.chdir("/Volumes/xray/simon/chandra_from_csc/"+Cur_Obs_ID_Str+"/primary/")
            retval_In_CSC = os.getcwd()
            #print "type(retval) ", type(retval)
            print "Directory changed successfully %s" % retval_In_CSC  #Checks the this line and the line above it combined check what the current working directory is
            LS_Str_In_CSC_Primary=os.popen("ls").read()
            print "LS_Str_In_CSC_Primary", LS_Str_In_CSC_Primary


#Event_2_File_Query("NGC 891") #NOT in CSC
Event_2_File_Query("NGC 6946") #In CSC
