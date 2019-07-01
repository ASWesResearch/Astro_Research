import os
import pandas as pd
from astroquery.ned import Ned
import astropy.units as u
import sys
from astropy.io import ascii
#path=os.path.realpath('../') #Reltive Path
path=os.path.realpath('/Volumes/xray/anthony/Research_Git/') #Absolute Path
sys.path.append(os.path.abspath(path))
from File_Query_Code import File_Query_Code_5
def D25_Finder(Gname):
    #print "Hello_World"
    """
    Gname_No_W=Gname.replace(" ", "")
    print "Gname_No_W : ", Gname_No_W
    path_Dia_T=os.path.realpath('../SQL_Standard_File/RC3_Query_Modifed_No_Whitespace.csv')
    #print "path_Dia_T : ", path_Dia_T
    #Dia_Table=ascii.read(path_Dia_T,format='csv')
    Dia_Table=pd.read_csv(path_Dia_T,sep=';')
    #print Dia_Table
    D25_Table=Dia_Table["D25"]
    #print D25_Table
    D25_L=list(D25_Table)
    #print "D25_L : ", D25_L
    Name_Table=Dia_Table["name"]
    #print "Name_Table : ", Name_Table
    Altname_Table=Dia_Table["altname"]
    #print "Altname_Table : ", Altname_Table
    PGC_Table=Dia_Table["PGC"]
    #print "PGC_Table : ", PGC_Table
    Dia_Table_L=[Name_Table,Altname_Table,PGC_Table]
    for N_Table in Dia_Table_L:
        #print "N_Table : ", N_Table
        #print N_Table.values
        N_L=list(N_Table)
        #print N_L
        if Gname_No_W in N_Table.values:
            #print "Found Name"
            #N_L=list(N_Table)
            #print N_L
            Gname_No_W_Bool= (Gname_No_W in N_L)
            #print "Gname_No_W_Bool : ", Gname_No_W_Bool
            #if(Gname_No_W_Bool):
            #print "In RC3 ! ! !"
            N_Inx=N_L.index(Gname_No_W)
            #print "N_Inx : ", N_Inx
            D25_Log_Arc=D25_L[N_Inx]
            #print "D25 : ", D25
            #print "type(D25) : ", type(D25)
            D25_S_Maj_Deg=(8.0+(1.0/3.0))*(10.0**(D25_Log_Arc-4.0))
            #D25_S_Maj_Deg=float(D25_S_Maj_Deg) # So it will throw up an expectation, when the value is "None"
            if D25_S_Maj_Deg is not None:
                return D25_S_Maj_Deg
            #return D25_S_Maj_Deg
        else:
            #print "Not in RC3 ! ! !"
            #result_table = Ned.query_region(Gname_No_W, radius=0.05 * u.deg)
            result_table = Ned.query_region(Gname_No_W, radius=(1.0/60.0) * u.deg)
            #result_table = Ned.query_region(Gname_No_W, radius=(5.0/60.0) * u.deg)
            print(result_table)
            Resolved_Name_Table=result_table['Object Name']
            #print "Resolved_Name_Table : \n", Resolved_Name_Table
            Resolved_Name_L=list(Resolved_Name_Table)
            print "Resolved_Name_L : ", Resolved_Name_L
            for Resolved_Name in Resolved_Name_L:
                Resolved_Name_Reduced_L=Resolved_Name.split(":")
                Resolved_Name_Reduced=Resolved_Name_Reduced_L[0]
                print "Resolved_Name_Reduced : ", Resolved_Name_Reduced
                Resolved_Name_Reduced_No_Whitespace=Resolved_Name_Reduced.replace(" ","")
                Resolved_Name_Reduced_No_Whitespace_No_0_L=Resolved_Name_Reduced_No_Whitespace.split('0',1)
                print "Resolved_Name_Reduced_No_Whitespace_No_0_L : ", Resolved_Name_Reduced_No_Whitespace_No_0_L #Removes the "0" form NGC 0###, for example "NGC0253" becomes "NGC253"
                if(Resolved_Name_Reduced_No_Whitespace_No_0_L[0]=="NGC"):
                    Resolved_Name_Reduced_No_Whitespace=Resolved_Name_Reduced_No_Whitespace_No_0_L[0]+Resolved_Name_Reduced_No_Whitespace_No_0_L[1]
                #print "Resolved_Name_Reduced_No_Whitespace : ", Resolved_Name_Reduced_No_Whitespace
                if(Resolved_Name_Reduced_No_Whitespace in N_L):
                    print "Resolved_Name_Reduced_No_Whitespace : ", Resolved_Name_Reduced_No_Whitespace
                    #Gname_No_W_Bool= (Gname_No_W in N_L)
                    #print "Gname_No_W_Bool : ", Gname_No_W_Bool
                    #if(Gname_No_W_Bool):
                    #print "In RC3 ! ! !"
                    N_Inx=N_L.index(Resolved_Name_Reduced_No_Whitespace)
                    #print "N_Inx : ", N_Inx
                    D25_Log_Arc=D25_L[N_Inx]
                    #print "D25 : ", D25
                    #print "type(D25) : ", type(D25)
                    D25_S_Maj_Deg=(8.0+(1.0/3.0))*(10.0**(D25_Log_Arc-4.0))
                    #break
                    #D25_S_Maj_Deg=float(D25_S_Maj_Deg) # So it will throw up an expectation, when the value is "None"
                    if D25_S_Maj_Deg is not None:
                        return D25_S_Maj_Deg
    return "None Found"/0.0 # So it will throw up an expectation, when the value is "None"
                    #return D25_S_Maj_Deg
                #break
        #return D25_S_Maj_Deg
        """
    Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
    print "Evt2_File_H_L : ", Evt2_File_H_L
    Evt2_File_L=Evt2_File_H_L[0]
    Obs_ID=Evt2_File_L[0]
    #print "Obs_ID : ", Obs_ID
    #path_Source_Flux_Table=os.path.realpath('../SQL_Standard_File/Source_Flux_Table.csv') #Reltive Path
    path_Source_Flux_Table=os.path.realpath('/Volumes/xray/anthony/Research_Git/SQL_Standard_File/Source_Flux_Table.csv') #Absolute Path
    #print "path_Source_Flux_Table : ", path_Source_Flux_Table
    Source_Flux_Table=ascii.read(path_Source_Flux_Table)
    #print "Source_Flux_Table : \n", Source_Flux_Table
    Obs_ID_A=Source_Flux_Table["OBSID"]
    Obs_ID_L=list(Obs_ID_A)
    #print "Obs_ID_L : ", Obs_ID_L
    Obs_ID_Inx=Obs_ID_L.index(Obs_ID)
    #print "Obs_ID_Inx : ", Obs_ID_Inx
    Resolved_Name_A=Source_Flux_Table["resolvedObject"]
    #print "Resolved_Name_A : ", Resolved_Name_A
    Resolved_Name_L=list(Resolved_Name_A)
    #print "Resolved_Name_L : ", Resolved_Name_L
    Resolved_Name=Resolved_Name_L[Obs_ID_Inx]
    #print "Resolved_Name : ", Resolved_Name
    #Dia_Table = Ned.get_table(Gname, table='diameters') #Dia_Table:-astropy.table.table.Table, Diameter_Table, The Data table queried from NED that contains the infomation about the Major Axis of the input Galaxy Name
    Dia_Table = Ned.get_table(Resolved_Name, table='diameters') #Dia_Table:-astropy.table.table.Table, Diameter_Table, The Data table queried from NED that contains the infomation about the Major Axis of the input Galaxy Name
    #print type(Dia_Table)
    #print G_Data
    #print Dia_Table
    #print Dia_Table.colnames
    #print Dia_Table.meta
    #print Dia_Table.columns
    Dia_Table_Feq=Dia_Table['Frequency targeted'] #Dia_Table_Feq:-astropy.table.column.MaskedColumn, Diameter_Table_Fequency, The Array containing all named frequencies of light that are being used for the Major Axis Measurement
    #print Dia_Table['NED Frequency']
    #print Dia_Table_Feq
    #print type(Dia_Table_Feq)
    Dia_Table_Feq_L=list(Dia_Table_Feq) #Dia_Table_Feq_L:-List, Diameter_Table_Fequency_List, The list containing all named frequencies of light that are being used for the Major Axis Measurement
    #print Dia_Table_Feq_L
    Dia_Table_Num=Dia_Table['No.'] #Dia_Table_Num:-astropy.table.column.MaskedColumn, Diameter_Table_Number, The number Ned assigns to
    #print Dia_Table_Num
    #print type(Dia_Table_Num)
    Dia_Table_Num_L=list(Dia_Table_Num)
    #print Dia_Table_Num_L
    for i in range(0,len(Dia_Table_Feq_L)-1): #There is a bug here with index matching, The matched index isn't that same index for the major axis
        Cur_Feq=Dia_Table_Feq_L[i]
        #print Cur_Feq
        if(Cur_Feq=="RC3 D_25, R_25 (blue)"):
            Match_inx=i
            Match_Feq=Dia_Table_Feq_L[Match_inx]
            Match_Num=Dia_Table_Num_L[Match_inx]
            #Match_Num
            #print "Match_Feq ", Match_Feq
            #print "Match_inx ", Match_inx
            #print "Match_Num ", Match_Num
    #Dia_Table_Maj=Dia_Table['Major Axis']
    Dia_Table_Maj=Dia_Table['NED Major Axis']
    #print Dia_Table_Maj
    Dia_Table_Maj_L=list(Dia_Table_Maj)
    #print Dia_Table_Maj_L
    Dia_Table_Maj_Units=Dia_Table['Major Axis Unit']
    #print Dia_Table_Maj_Units
    Dia_Table_Maj_Units_L=list(Dia_Table_Maj_Units)
    #print Dia_Table_Maj_Units_L
    #print "i ", i
    D25_Maj=Dia_Table_Maj_L[Match_inx]
    #print "D25_Maj ", D25_Maj
    D25_Units=Dia_Table_Maj_Units[Match_inx]
    #print "D25_Units ", D25_Units
    #print type(Dia_Table)
    #print Dia_Table.info()
    #Dia_Table_2=Dia_Table[6]
    #print Dia_Table_2
    #Maj=Dia_Table_2[18]
    #print "Maj, ! ! !", Maj
    D25_S_Maj=D25_Maj/2.0
    D25_S_Maj_Deg=D25_S_Maj/3600.0
    return D25_S_Maj_Deg



def D25_List_Run(Gname_L):
    Fail_L=[]
    for Gname in Gname_L:
        try:
            Cur_D25=D25_Finder(Gname)
            print Cur_D25
        except:
            Fail_L.append(Gname)
    print "Fail_L : \n", Fail_L



#print D25_Finder("A2357+47")
#print D25_Finder("UGC12889")
#print D25_Finder("PGC2")
#NGC4594
#print D25_Finder("NGC 4594")
#print D25_Finder("NGC 253")
#print D25_Finder("SN 1986J")
#NGC 1313 X-2
#print D25_Finder("NGC 1313 X-2")
#print D25_Finder("NGC 1313 X-1")
#print D25_Finder("SN2011ja")
#print D25_Finder("NGC 604")
#3C31
#print D25_Finder("3C31")
#NGC 891
#print D25_Finder("NGC 891")
#print D25_Finder("NGC 7507")
"""
D25_List_Run(['SN 2004am', 'SN 1996aq', 'PGC135659', 'M51', 'SN2011ja', 'N119',
'SN 2011ja', 'NGC 346', 'SNR 1987A', 'SN 1998S', 'NGC 604', 'NGC5471B', 'NGC 5204 X-1', 'NGC 1818', 'FORNAX CLUSTER', 'SN 2002HH', 'SN 1986J', 'SN 2004dj', 'SN 2004et', 'NGC 1313 X-1', 'NGC 1313 X-2', 'VIRGO CLUSTER', 'ngc 1672', 'SN 1993J',
'SNR 0509-67.5', 'SN1999em', 'SN1998S',
'UGC 7658', 'SNR 0104-72.3',
 'SN1978K'])
"""

#D25_List_Run(['SN 2004am','SN 1996aq','PGC135659','M51','SN2011ja','N119','SN 2011ja','NGC 346','SNR 1987A','SN 1998S','NGC 604','NGC5471B','NGC 5204 X-1','NGC 1818','FORNAX CLUSTER','SN 2002HH','SN 1986J','SN 2004dj','SN 2004et','NGC 1313 X-1','NGC 1313 X-2','VIRGO CLUSTER','ngc 1672','SN 1993J','SNR 0509-67.5','SN1999em','SN1998S','UGC 7658','SNR 0104-72.3','SN1978K','NGC7507','NGC 4472','M83','NGC 253','NGC3923','NGC 4490','NGC1097','M33','NGC 2865','NGC 1316','NGC 5253','NGC 3628','NGC 1291','NGC 5236','NGC 1700','NGC 5018','3C31','IC 1459','NGC 1332','M82','NGC 3557','NGC 4258','M87','NGC 3031','IC5267','NGC 4565','M101','NGC1427','M84','M81','NGC 7552','NGC 4649','NGC 5846','NGC 891','NGC 4631','NGC 4374','I ZW 18','NGC3585','M86','NGC1399'])
