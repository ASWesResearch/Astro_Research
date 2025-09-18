import numpy as np
import pandas as pd

def Missing_Source_Finder(Standard_File_Fpath="../SQL_Standard_File/Source_Flux_All_Modified_6.csv", Region_Path="/Volumes/expansion/Hybrid_Regions/"):
    Data_Standard_File=pd.read_csv(Standard_File_Fpath)
    Data_Standard_File_ObsID_Grouped=Data_Standard_File.groupby("ObsID")
    #Data_Standard_File_ObsID_Grouped=Data_Standard_File.groupby("ObsID", as_index=False)
    #print("Data_Standard_File_ObsID_Grouped: ", Data_Standard_File_ObsID_Grouped)
    #print("Data_Standard_File_ObsID_Grouped.groups: ", Data_Standard_File_ObsID_Grouped.groups)
    #ObsID_L=list(Data_Standard_File_ObsID_Grouped.groups.keys())
    #print("ObsID_L: ", ObsID_L)
    ObsID_Missing_L=[]
    ObsID_Mismatch_L=[]
    for ObsID_Group in Data_Standard_File_ObsID_Grouped:
        #print("ObsID_Group:\n", ObsID_Group)
        Cur_ObsID=int(ObsID_Group[0])
        Cur_Data=ObsID_Group[1]
        print("Cur_ObsID: ", Cur_ObsID)
        #print("Cur_Data:\n", Cur_Data)
        #print("len(Cur_Data): ", len(Cur_Data))
        Number_of_Standard_File_Sources=len(Cur_Data)
        print("Number_of_Standard_File_Sources: ", Number_of_Standard_File_Sources)
        Cur_Reg_Path=Region_Path+str(Cur_ObsID)+"/"+str(Cur_ObsID)+"_Nearest_Neighbor_Hybrid.reg"
        with open(Cur_Reg_Path, 'r') as fp:
            lines = len(fp.readlines())
            #print('Total Number of lines:', lines)
            Number_of_Region_Sources=int(lines-2)
            print("Number_of_Region_Sources: ", Number_of_Region_Sources)
            if(Number_of_Standard_File_Sources<Number_of_Region_Sources):
                print("Missing Sources Found!!!")
                ObsID_Missing_L.append(Cur_ObsID)
            if(Number_of_Standard_File_Sources>Number_of_Region_Sources):
                print("Mismatch Found!!!")
                ObsID_Mismatch_L.append(Cur_ObsID)
    return ObsID_Missing_L, ObsID_Mismatch_L

print(Missing_Source_Finder())
