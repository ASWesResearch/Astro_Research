import pandas as pd
import matplotlib.pyplot as plt
import glob
import re

def Source_Test_Overlap(Test_Row):
    Test_L=list(Test_Row)
    #print("Test_L: ", Test_L)
    Test_L=Test_L[1:]
    Test=Test_L[1]
    #for Test in Test_L:
    #Test=re.split(",", Test)
    #print("Test: ", Test)
    if(len(Test)>2):
        return True
    else:
        return False
def Background_Test_Overlap(Test_Row):
    Test_L=list(Test_Row)
    print("Test_L: ", Test_L)
    Test_L=Test_L[1:]
    Test=Test_L[0]
    #for Test in Test_L:
    #Test=re.split(",", Test)
    #print("Test: ", Test)
    if(len(Test)>2):
        return True
    else:
        return False
def Source_Overlap_Query():
    #/opt/xray/anthony/expansion_backup/Hybrid_Regions/10125/10125_Overlapping_Sources.csv
    Overlapping_Sources_Filepaths=glob.glob("/opt/xray/anthony/expansion_backup/Hybrid_Regions/*/*_Overlapping_Sources.csv")
    #Overlapping_Sources_Filepaths=glob.glob("/opt/xray/anthony/expansion_backup/Hybrid_Regions/969/969_Overlapping_Sources.csv") #For Testing
    #print("Overlapping_Sources_Filepaths:\n", Overlapping_Sources_Filepaths)
    Coords_Filepaths=glob.glob("/opt/xray/anthony/expansion_backup/Hybrid_Regions/*/*_Coords.csv")
    #Coords_Filepaths=glob.glob("/opt/xray/anthony/expansion_backup/Hybrid_Regions/969/*969*_Coords.csv") #For testing
    #print("Coords_Filepaths:\n", Coords_Filepaths)
    for i in range(0,len(Overlapping_Sources_Filepaths)):
    #for i in range(0,1):
        #i=0 #For testing
        Overlapping_Sources_Filepath=Overlapping_Sources_Filepaths[i]
        Overlapping_Sources_A=pd.read_csv(Overlapping_Sources_Filepath,";")
        print("Overlapping_Sources_A: ", Overlapping_Sources_A)
        Overlapping_Sources_Modified_A=Overlapping_Sources_A
        #print("Overlapping_Sources_A.apply(Test_Overlap, axis=1): ", Overlapping_Sources_A.apply(Test_Overlap, axis=1))
        #Overlapping_Sources_Modified_A["Overlap_Bool"]=Overlapping_Sources_A.apply(Test_Overlap, axis=1)
        Overlapping_Sources_Modified_A["Source_Overlap_Bool"]=Overlapping_Sources_A.apply(Source_Test_Overlap, axis=1)
        Overlapping_Sources_Modified_A["Background_Overlap_Bool"]=Overlapping_Sources_A.apply(Background_Test_Overlap, axis=1)
        print("Overlapping_Sources_Modified_A: ", Overlapping_Sources_Modified_A)
        #Only_Overlapping=Overlapping_Sources_A[Overlapping_Sources_A.apply(Test_Overlap, axis=1)]
        #Only_Overlapping=Overlapping_Sources_Modified_A[Overlapping_Sources_Modified_A["Source_Overlap_Bool"] | Overlapping_Sources_Modified_A["Background_Overlap_Bool"]]
        #print("Only_Overlapping:\n", Only_Overlapping)
        Coords_Filepath=Coords_Filepaths[i]
        Coords_A=pd.read_csv(Coords_Filepath)
        #print("Coords_A.iloc[0]['Offaxis_Angle']:", Coords_A.iloc[0]["Offaxis_Angle"])
        Offaxis_Angle_A=Coords_A["Offaxis_Angle"]
        print("Offaxis_Angle_A:\n", Offaxis_Angle_A)
        Overlapping_Sources_Modified_A["Offaxis_Angle"]=Offaxis_Angle_A
        print("Overlapping_Sources_Modified_A:\n", Overlapping_Sources_Modified_A)
        Only_Overlapping=Overlapping_Sources_Modified_A[Overlapping_Sources_Modified_A["Source_Overlap_Bool"] | Overlapping_Sources_Modified_A["Background_Overlap_Bool"]]
        Source_Only_Overlapping=Overlapping_Sources_Modified_A[Overlapping_Sources_Modified_A["Source_Overlap_Bool"]]
        Background_Only_Overlapping=Overlapping_Sources_Modified_A[Overlapping_Sources_Modified_A["Background_Overlap_Bool"]]
        print("Only_Overlapping:\n", Only_Overlapping)
        if(i<1):
            Only_Overlapping_All=Only_Overlapping
            Source_Only_Overlapping_All=Source_Only_Overlapping
            Background_Only_Overlapping_All=Background_Only_Overlapping
        else:
            #JWST_Data=pd.concat([JWST_Short_Data, JWST_Long_Data], ignore_index=True)
            Only_Overlapping_All=pd.concat([Only_Overlapping_All, Only_Overlapping], ignore_index=True)
            Source_Only_Overlapping_All=pd.concat([Source_Only_Overlapping_All, Source_Only_Overlapping], ignore_index=True)
            Background_Only_Overlapping_All=pd.concat([Background_Only_Overlapping_All, Background_Only_Overlapping], ignore_index=True)
    print("Only_Overlapping_All: ", Only_Overlapping_All)
    print("Source_Only_Overlapping_All: ", Source_Only_Overlapping_All)
    print("Background_Only_Overlapping_All: ", Background_Only_Overlapping_All)
    ##Hist_A=plt.hist(Only_Overlapping_All["Offaxis_Angle"])
    #Hist_A=plt.hist(Source_Only_Overlapping_All["Offaxis_Angle"], density=True, label="Source Overlap")
    #Hist_A=plt.hist(Background_Only_Overlapping_All["Offaxis_Angle"], density=True, label="Background Overlap")
    Hist_A=plt.hist(Background_Only_Overlapping_All["Offaxis_Angle"], label="Background Overlap")
    Hist_A=plt.hist(Source_Only_Overlapping_All["Offaxis_Angle"], label="Source Overlap")
    #Hist_A=plt.hist(Background_Only_Overlapping_All["Offaxis_Angle"], label="Background Overlap")
    plt.xlabel("Offaxis_Angle")
    plt.ylabel("Number of Overlapping Sources")
    plt.title("Overlapping Sources")
    plt.legend()
    ##plt.savefig("Source_Overlap_Vs_Offaxis_Angle.pdf")
    ##plt.savefig("Source_Overlap_Vs_Offaxis_Angle.png")
    #plt.show()
Source_Overlap_Query()
