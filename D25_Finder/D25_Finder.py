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
        if Gname_No_W in N_Table.values:
            #print "Found Name"
            N_L=list(N_Table)
            #print N_L
            if Gname_No_W in N_L:
                N_Inx=N_L.index(Gname_No_W)
            else:
                result_table = Ned.query_region(Gname_No_W, radius=0.05 * u.deg)
                print(result_table)
            #print "N_Inx : ", N_Inx
            D25_Log_Arc=D25_L[N_Inx]
            #print "D25 : ", D25
            #print "type(D25) : ", type(D25)
            D25_S_Maj_Deg=(8.0+(1.0/3.0))*(10.0**(D25_Log_Arc-4.0))
            return D25_S_Maj_Deg


#print D25_Finder("A2357+47")
#print D25_Finder("UGC12889")
#print D25_Finder("PGC2")
#NGC4594
#print D25_Finder("NGC 4594")
print D25_Finder("NGC 253")
