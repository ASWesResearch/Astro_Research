import pandas as pd
import matplotlib.pyplot as plt
def Reasonable_FOV_Hist(fpath):
    Data=pd.read_csv(fpath)
    f=open("Galaxy_Sample_D25_Hist.txt","w")
    #Header_Line=""
    D25_Arcmin_A=Data["D25_Arcmin"]
    Hist=plt.hist(D25_Arcmin_A,range=(0,10))
    Bin_Hight_A=Hist[0]
    for Num_Galaxies in Bin_Hight_A:
        Cur_Line=str(Num_Galaxies)+"\n"
        f.write(Cur_Line)
    #Hist=plt.hist(D25_Arcmin_A)
    plt.ylabel("Number of Galaxies")
    plt.xlabel("D25 of Galaxy (Arcmin)")
    #print Hist
    #plt.show()
    plt.savefig("Galaxy_Sample_D25_Hist.png")
Reasonable_FOV_Hist("/Volumes/xray/anthony/Research_Git/Histogram_Organizer/D25_Source_Ratios_Max.csv")
