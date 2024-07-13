import numpy as np
import pandas as pd
def Galaxy_List_Generator(fpath="/opt/xray/anthony/Research_Git/SQL_Standard_File/Source_Flux_All_Modified_3.csv",key="Gname_Modifed"):
    Data=pd.read_csv(fpath)
    Gname_A=Data[key]
    Gname_L=list(Gname_A)
    Gname_L_Reduced=[]
    for Gname in Gname_L:
        if(Gname not in Gname_L_Reduced):
            Gname_L_Reduced.append(Gname)
    Gname_A_Reduced=np.array(Gname_L_Reduced)
    Gname_Reduced_DF=pd.DataFrame({key:Gname_A_Reduced})
    Gname_Reduced_DF.to_csv("Galaxy_Names.csv")
    print("Number of Unique Galaxy Names: ", len(Gname_L_Reduced))
    return Gname_L_Reduced

print(Galaxy_List_Generator())
