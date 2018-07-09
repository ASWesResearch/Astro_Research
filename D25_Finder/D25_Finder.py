import os
import pandas as pd
from astroquery.ned import Ned
import astropy.units as u
def D25_Finder(Gname):
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
            #result_table = Ned.query_region(Gname_No_W, radius=(1.0/60.0) * u.deg)
            result_table = Ned.query_region(Gname_No_W, radius=(5.0/60.0) * u.deg)
            #print(result_table)
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
print D25_Finder("3C31")
"""
D25_List_Run(['SN 2004am', 'SN 1996aq', 'PGC135659', 'M51', 'SN2011ja', 'N119',
'SN 2011ja', 'NGC 346', 'SNR 1987A', 'SN 1998S', 'NGC 604', 'NGC5471B', 'NGC 5204 X-1', 'NGC 1818', 'FORNAX CLUSTER', 'SN 2002HH', 'SN 1986J', 'SN 2004dj', 'SN 2004et', 'NGC 1313 X-1', 'NGC 1313 X-2', 'VIRGO CLUSTER', 'ngc 1672', 'SN 1993J',
'SNR 0509-67.5', 'SN1999em', 'SN1998S',
'UGC 7658', 'SNR 0104-72.3',
 'SN1978K'])
"""

#D25_List_Run(['SN 2004am','SN 1996aq','PGC135659','M51','SN2011ja','N119','SN 2011ja','NGC 346','SNR 1987A','SN 1998S','NGC 604','NGC5471B','NGC 5204 X-1','NGC 1818','FORNAX CLUSTER','SN 2002HH','SN 1986J','SN 2004dj','SN 2004et','NGC 1313 X-1','NGC 1313 X-2','VIRGO CLUSTER','ngc 1672','SN 1993J','SNR 0509-67.5','SN1999em','SN1998S','UGC 7658','SNR 0104-72.3','SN1978K','NGC7507','NGC 4472','M83','NGC 253','NGC3923','NGC 4490','NGC1097','M33','NGC 2865','NGC 1316','NGC 5253','NGC 3628','NGC 1291','NGC 5236','NGC 1700','NGC 5018','3C31','IC 1459','NGC 1332','M82','NGC 3557','NGC 4258','M87','NGC 3031','IC5267','NGC 4565','M101','NGC1427','M84','M81','NGC 7552','NGC 4649','NGC 5846','NGC 891','NGC 4631','NGC 4374','I ZW 18','NGC3585','M86','NGC1399'])
