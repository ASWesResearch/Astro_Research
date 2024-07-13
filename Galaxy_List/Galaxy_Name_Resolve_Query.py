import numpy as np
import pandas as pd
def Galaxy_Name_Resolve_Query(Standard_Filepath="/opt/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv",Resolved_Name_Filepath="/opt/xray/anthony/Research_Git/SQL_Standard_File/All_Galaxy_Names_3.csv", Outfile_Path="", Flux_Cut=None):
    Standard_File_Data=pd.read_csv(Standard_Filepath)
    if(Flux_Cut!=None):
        Standard_File_Data=Standard_File_Data[Standard_File_Data["Exposure "]>10.0]
    Resolved_Name_Data=pd.read_csv(Resolved_Name_Filepath)
    #print("Standard_File_Data:\n", Standard_File_Data)
    #print("Resolved_Name_Data:\n", Resolved_Name_Data)
    Target_Name_A=Standard_File_Data["Target Name"]
    Target_Name_L=list(Target_Name_A)
    Object_Name_A=Resolved_Name_Data["Object_Name"]
    Object_Name_L=list(Object_Name_A)
    Resolved_Name_A=Resolved_Name_Data["Gname_Resolved"]
    Resolved_Name_L=list(Resolved_Name_A)
    Match_L=[]
    Homogeneous_Name_L=[]
    Num_Missing=0
    Num_Found=0
    j=0
    for Target_Name in Target_Name_L:
        #for Object_Name in Object_Name_L:
        Homogeneous_Name_Found_Bool=False
        Count=0
        for i in range(0,len(Object_Name_L)):
            Object_Name_Test=Object_Name_L[i]
            Resolved_Name_Test=Resolved_Name_L[i]
            #Count=0
            if(Target_Name==Object_Name_Test):
                Resolved_Name=Resolved_Name_Test
                #Homogeneous_Name_Found_Bool=True
                if((isinstance(Resolved_Name,float)==False)):
                    Homogeneous_Name_L.append(Resolved_Name)
                    Homogeneous_Name_Found_Bool=True
                    Num_Found=Num_Found+1
                    Count=Count+1
                    #print("Num_Found: ", Num_Found)
                if((Resolved_Name not in Match_L) and (isinstance(Resolved_Name,float)==False)):
                    Match_L.append(Resolved_Name)
                #break
                if(Count>1):
                    print("Duplicate Found!!!!")
                    print("Target_Name Dup: ", Target_Name)
                    print("Resolved_Name Dup: ", Resolved_Name)
        if(Homogeneous_Name_Found_Bool==False):
            Homogeneous_Name_L.append(np.nan)
            Num_Missing=Num_Missing+1
            #print("Num_Missing: ", Num_Missing)
        j=j+1
        #print("j: ", j)
    #print("Match_L:\n", Match_L)
    #print("len(Match_L): ", len(Match_L))
    Duplicate_L=[]
    for i in range(0,len(Match_L)):
        Cur_Match=Match_L[i]
        #for Object_Name in Object_Name_L:
        for j in range(0, len(Object_Name_L)):
            Object_Name=Object_Name_L[j]
            Resolved_Name=Resolved_Name_L[j]
            if((Object_Name==Cur_Match) and (Object_Name!=Resolved_Name)):
                #print("Duplicate Galaxy Name: ", Cur_Match)
                Duplicate_L.append(Cur_Match)
    #print("Duplicate_L: ", Duplicate_L)
    Match_L_Reduced=[]
    for Match in Match_L:
        if(Match not in Duplicate_L):
            Match_L_Reduced.append(Match)
    #print("Match_L_Reduced: ", Match_L_Reduced)
    """
    Match_L_Reduced_Messier_Corrected=[]
    for Match in Match_L_Reduced:
        Match_No_Whitespace=Match.replace(" ","")
        if((Match[0]=="M") and (Match[1].isdigit())):
            Messier_Number=int(Match[1:])
            #print("Messier_Number: ", Messier_Number)
            if(Messier_Number<10):
                Messier_Match="MESSIER 00"+Match[1:]
            if(Messier_Number<100):
                Messier_Match="MESSIER 0"+Match[1:]
            else:
                Messier_Match="MESSIER "+Match[1:]
            #print("Messier_Match: ", Messier_Match)
            Match_L_Reduced_Messier_Corrected.append(Messier_Match)
        else:
            Match_L_Reduced_Messier_Corrected.append(Match)
    """
    Match_L_Reduced_Messier_Corrected=Match_L_Reduced #For Testing
    print("Match_L_Reduced_Messier_Corrected: ", Match_L_Reduced_Messier_Corrected)
    print("len(Match_L_Reduced_Messier_Corrected): ", len(Match_L_Reduced_Messier_Corrected))
    #Match_L_Reduced_Messier_Corrected_Reduced=list(set(Match_L_Reduced_Messier_Corrected))
    Match_L_Reduced_Messier_Corrected_Reduced=[]
    for Match in Match_L_Reduced_Messier_Corrected:
        if(Match in Match_L_Reduced_Messier_Corrected_Reduced):
            print("Duplicate Match: ", Match)
        if(Match not in Match_L_Reduced_Messier_Corrected_Reduced):
            Match_L_Reduced_Messier_Corrected_Reduced.append(Match)
    print("Match_L_Reduced_Messier_Corrected_Reduced: ", Match_L_Reduced_Messier_Corrected_Reduced)
    print("len(Match_L_Reduced_Messier_Corrected_Reduced): ", len(Match_L_Reduced_Messier_Corrected_Reduced))
    #df = pd.DataFrame(lst)
    Match_L_Reduced_Messier_Corrected_Reduced_A=pd.DataFrame(Match_L_Reduced_Messier_Corrected_Reduced)
    print("Match_L_Reduced_Messier_Corrected_Reduced_A: ", Match_L_Reduced_Messier_Corrected_Reduced_A)
    Match_L_Reduced_Messier_Corrected_Reduced_A.columns = ["Galaxy_Name_Reduced"]
    Outfilename="Galaxy_Names_Reduced_Homogeneous_Resolved_Unique.csv"
    if(Flux_Cut!=None):
        Outfilename="Galaxy_Names_Reduced_Homogeneous_Resolved_Unique_with_"+str(int(Flux_Cut))+"ks_Exposure_Cut.csv"
    OutFpath=Outfile_Path+Outfilename
    Match_L_Reduced_Messier_Corrected_Reduced_A.to_csv(OutFpath)

    Homogeneous_Name_A=pd.DataFrame(Homogeneous_Name_L)
    Homogeneous_Name_A.columns = ["Galaxy_Name_Homogenized"]
    Homogeneous_Outfilename="Galaxy_Name_Homogenized.csv"
    if(Flux_Cut!=None):
        Homogeneous_Outfilename="Galaxy_Name_Homogenized_"+str(int(Flux_Cut))+"ks_Exposure_Cut.csv"
    Homogeneous_Outpath=Outfile_Path+Homogeneous_Outfilename
    Homogeneous_Name_A.to_csv(Homogeneous_Outpath)
    print("len(Target_Name_L): ", len(Target_Name_L))
    print("Num_Found: ", Num_Found)
    print("Num_Missing: ", Num_Missing)
Galaxy_Name_Resolve_Query()
Galaxy_Name_Resolve_Query(Flux_Cut=10.0)
