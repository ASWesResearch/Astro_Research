import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
from os import system
import sys
from functools import partial
from scipy.special import erfinv, erf
from scipy import interpolate
from scipy.interpolate import interp1d

dir = os.path.dirname(__file__)
path=os.path.realpath('../')
sys.path.append(os.path.abspath(path))

from Source_Generator import Source_Generator


dir = os.path.dirname(__file__)
path=os.path.realpath('../../')
sys.path.append(os.path.abspath(path))

from Detection_Probablity_Calc import Detection_Probability_Calc_7

def Read_Path_Value_String(Path):
    Path_L=Path.split("/")
    Value_Str=Path_L[-2]
    return Value_Str

def Read_Path_Value(Path):
    Value_Str=Read_Path_Value_String(Path)
    if("E" in Value_Str):
        Value=float(Value_Str)
    else:
        Value=int(Value_Str)
    return Value

def Merge_Data():
    #../Main_Code/Wavdetect_Outputs/45/1/3/1E-4/1/45_1_3_1E-4_1_Standard_Outputs.csv
    Phi_Glob_Str="../Main_Code/Wavdetect_Outputs/*/"
    Phi_Glob_L=glob.glob(Phi_Glob_Str)
    Phi_Glob_L.sort(key=Read_Path_Value)
    #print("Phi_Glob_L: ", Phi_Glob_L)
    Incomplete_L=[]
    i=0
    for Phi_Path in Phi_Glob_L:
        #print("Phi_Path: ", Phi_Path)
        Phi=Read_Path_Value(Phi_Path)
        #print("Phi: ", Phi)
        Theta_Glob_Str="../Main_Code/Wavdetect_Outputs/"+str(Phi)+"/*/"
        Theta_Glob_L=glob.glob(Theta_Glob_Str)
        Theta_Glob_L.sort(key=Read_Path_Value)
        #Theta_Glob_L=[Theta_Glob_L[0]] #For Testing
        for Theta_Path in Theta_Glob_L:
            Theta=Read_Path_Value(Theta_Path)
            #print("Theta: ", Theta)
            Counts_Glob_Str="../Main_Code/Wavdetect_Outputs/"+str(Phi)+"/"+str(Theta)+"/*/"
            Counts_Glob_L=glob.glob(Counts_Glob_Str)
            Counts_Glob_L.sort(key=Read_Path_Value)
            #Counts_Glob_L=[Counts_Glob_L[0]] #For Testing
            for Counts_Path in Counts_Glob_L:
                Counts=Read_Path_Value(Counts_Path)
                #print("Counts: ", Counts)
                Background_Glob_Str="../Main_Code/Wavdetect_Outputs/"+str(Phi)+"/"+str(Theta)+"/"+str(Counts)+"/*/"
                Background_Glob_L=glob.glob(Background_Glob_Str)
                Background_Glob_L.sort(key=Read_Path_Value)
                #Background_Glob_L=[Background_Glob_L[0],Background_Glob_L[1]] #For Testing
                for Background_Path in Background_Glob_L:
                    Background_Str=Read_Path_Value_String(Background_Path)
                    #print("Background_Str: ", Background_Str)
                    Background=Read_Path_Value(Background_Path)
                    #print("Background: ", Background)
                    Run_Count_Glob_Str="../Main_Code/Wavdetect_Outputs/"+str(Phi)+"/"+str(Theta)+"/"+str(Counts)+"/"+str(Background_Str)+"/*/"
                    Run_Count_Glob_L=glob.glob(Run_Count_Glob_Str)
                    Run_Count_Glob_L.sort(key=Read_Path_Value)
                    Cur_Background_Seed, Cur_Background_Seed_Biased=Source_Generator.Seed_Generator(Phi,Theta,Counts,Background_Str,Run_Count=None)
                    for Run_Count_Path in Run_Count_Glob_L:
                        Run_Count=Read_Path_Value(Run_Count_Path)
                        ##print("Run_Count: ", Run_Count)
                        #../Main_Code/Wavdetect_Outputs/45/1/3/1E-4/1/45_1_3_1E-4_1_Standard_Outputs.csv
                        Cur_Filepath="../Main_Code/Wavdetect_Outputs/"+str(Phi)+"/"+str(Theta)+"/"+str(Counts)+"/"+str(Background_Str)+"/"+str(Run_Count)+"/"+str(Phi)+"_"+str(Theta)+"_"+str(Counts)+"_"+str(Background_Str)+"_"+str(Run_Count)+"_Standard_Outputs.csv"
                        #Cur_Seed, Cur_Seed_Biased=Source_Generator.Seed_Generator(Phi,Theta,Counts,Background_Str,Run_Count=Run_Count)
                        try:
                            Cur_Data=pd.read_csv(Cur_Filepath)
                        except:
                            Incomplete_L.append(Cur_Filepath)
                            continue
                        Cur_Data.insert(loc = 0, column = "Phi", value = Phi)
                        Cur_Data.insert(loc = 1, column = "Theta", value = Theta)
                        Cur_Data.insert(loc = 2, column = "Counts", value = Counts)
                        Cur_Data.insert(loc = 3, column = "Background", value = Background_Str)
                        Cur_Data.insert(loc = 4, column = "Run_Count", value = Run_Count)
                        Cur_Data.insert(loc = 5, column = "Grouping_Key", value = Cur_Background_Seed)
                        if(i==0):
                            Data=Cur_Data
                        else:
                            #pass
                            Data=pd.concat([Data, Cur_Data], ignore_index=True)
                        ##print("Cur_Data:\n", Cur_Data)
                        #f = open(Cur_Filepath, "r")
                        #f.readline()
                        #print(f.readline(1))
                        i=i+1
    Data.to_csv('Marx_Source_Detection_Data.csv')
    print("Incomplete_L: ", Incomplete_L)

def Alpha_Quantile(p):
    Alpha=1-p
    Alpha_Quantile=1-(Alpha/2.0)
    return Alpha_Quantile

def Probit(x):
    Probit=np.sqrt(2)*erfinv((2.0*x)-1.0)
    return Probit

def Wald_Probability_Calc(s, z=1.0, n=49, scale=1.0):
    #s/n+-(z/sqrt(n))*sqrt((s/n)*((n-s)/n))
    s=scale*s
    n=scale*n
    p=float(s)/float(n)
    Error=(z/np.sqrt(n))*np.sqrt((s/float(n))*((n-s)/float(n)))
    return p, Error

def Wilson_Probability_Calc(s, z=1.0, n=49, scale=1.0):
    #(s+z^2/2)/(n+z^2)+-(z/(n+z^2))*sqrt(((s*(n-s))/n)+(z^2/4))
    s=scale*s
    n=scale*n
    p=(s+((z**2.0)/2.0))/(n+(z**2.0))
    Error=(z/(n+(z**2.0)))*np.sqrt(((s*(n-s))/n)+(z**2.0/4.0))
    return p, Error

def Probability_Model_Plotting():
    Wald_L=[]
    Wald_Error_L=[]
    Wilson_L=[]
    Wilson_Error_L=[]
    Wilson_L_Scaled=[]
    Wilson_Error_Scaled_L=[]
    s_L=[]
    for s in range(0,50):
        s_L.append(s)
        Cur_Wald_Tuple=Wald_Probability_Calc(s)
        Wald_L.append(Cur_Wald_Tuple[0])
        Wald_Error_L.append(Cur_Wald_Tuple[1])
        Cur_Wilson_Tuple=Wilson_Probability_Calc(s)
        Wilson_L.append(Cur_Wilson_Tuple[0])
        Wilson_Error_L.append(Cur_Wilson_Tuple[1])
        Cur_Wilson_Tuple_Scaled=Wilson_Probability_Calc(s, scale=4.0)
        Wilson_L_Scaled.append(Cur_Wilson_Tuple_Scaled[0])
        Wilson_Error_Scaled_L.append(Cur_Wilson_Tuple_Scaled[1])
    #plt.plot(s_L, Wald_L, label="Wald")
    #ax = plt.gca()
    #ax.set_yscale('function', functions=(partial(np.power, 10.0), np.log10))
    ##plt.errorbar(s_L, Wald_L, yerr=Wald_Error_L, color="blue", alpha=0.3, label="Wald")
    #plt.plot(s_L, Wilson_L, label="Wilson")
    plt.errorbar(s_L, Wilson_L, yerr=Wilson_Error_L, color="orange", alpha=0.3, label="Wilson")
    plt.errorbar(s_L, Wilson_L_Scaled, yerr=Wilson_Error_Scaled_L, color="red", alpha=0.3, label="Wilson Scaled")
    plt.axhline(y=0.9, color='green', linestyle='--')
    #for s in s_L:
    #    plt.axvline(x=s, color="grey", alpha=0.5)
    plt.legend()
    plt.savefig("Probability_Model_Plot.pdf")

def Process_Data(Fpath):
    Data=pd.read_csv(Fpath)
    print("Data:\n", Data)
    Data["Detection_Bool"]=Data['SDB']>0
    #Data["SNR_1"]=(Data["Counts"]/(128.0**2.0))/(Data["Background"])
    Data["SNR"]=(Data["Counts"])/(Data["Background"]*(128.0**2.0))
    #Number_of_Samples = ((Data_Grouped_Mean["Phi"]==Phi) & (Data_Grouped_Mean["Theta"]==Theta) & (Data_Grouped_Mean["Counts"]==Counts)).sum()
    #Data['Background'] = Data['Background'].astype(float)

    with pd.option_context('display.max_columns', None):  # more options can be specified also
        #print("Data:\n", Data)
        Data_Grouped=Data.groupby(['Grouping_Key'])
        for key, item in Data_Grouped:
            #print("key: ", key)
            Cur_Data=Data_Grouped.get_group(key)
            #print("Cur_Data\n: ", Cur_Data)
            #Cur_Number_of_Samples=Cur_Data.size
            Cur_Number_of_Samples=Cur_Data.shape[0]
            #print("Cur_Number_of_Samples: ", Cur_Number_of_Samples)
        Data_Grouped_Mean=Data.groupby(['Grouping_Key']).mean()
        Data_Grouped_Mean["Number_of_Samples"]=Data_Grouped.size()
        #print("Data_Grouped_Mean:\n", Data_Grouped_Mean)
        Data_Grouped_Sum=Data.groupby(['Grouping_Key']).sum()
        #print("Data_Grouped_Sum:\n", Data_Grouped_Sum)
        Data_Grouped_Mean["Detection_Bool"]=Data_Grouped_Sum["Detection_Bool"]
        print("Data_Grouped_Mean:\n", Data_Grouped_Mean)
        return Data, Data_Grouped, Data_Grouped_Mean, Data_Grouped_Sum

def Plot_Detection_Probability(Theta, Counts_L, Fpath):
    Color_L=['b','g','r','c','m','y','orange']
    Data, Data_Grouped, Data_Grouped_Mean, Data_Grouped_Sum=Process_Data(Fpath)
    #Data_Grouped_Mean_Filtered=Data_Grouped_Mean[(Data_Grouped_Mean["Theta"]==10) & (Data_Grouped_Mean["Counts"]==30.0)]
    for i in range(0, len(Counts_L)):
        Counts=Counts_L[i]
        Data_Grouped_Mean_Filtered=Data_Grouped_Mean[(Data_Grouped_Mean["Theta"]==Theta) & (Data_Grouped_Mean["Counts"]==Counts)]
        Data_Grouped_Mean_Filtered=Data_Grouped_Mean_Filtered.sort_values(by=["Background"])
        print("Data_Grouped_Mean_Filtered:\n", Data_Grouped_Mean_Filtered)
        Background=Data_Grouped_Mean_Filtered["Background"]
        ##Detection_Probability=Data_Grouped_Mean_Filtered["SDB"]
        #Detection_Probability=Wilson_Probability_Calc(Data_Grouped_Mean_Filtered['Detection_Bool'])[0]
        #print("Data_Grouped_Mean_Filtered['Detection_Bool']: ", Data_Grouped_Mean_Filtered['Detection_Bool'])
        #Number_of_Samples = ((Data_Grouped_Mean["Theta"]==Theta) & (Data_Grouped_Mean["Counts"]==Counts)).sum()
        ##Detection_Probability_Tuple=Wilson_Probability_Calc(Data_Grouped_Mean_Filtered['Detection_Bool'])
        Detection_Probability_Tuple=Wilson_Probability_Calc(Data_Grouped_Mean_Filtered['Detection_Bool'], n=Data_Grouped_Mean_Filtered['Number_of_Samples'])
        Detection_Probability=Detection_Probability_Tuple[0]
        Detection_Probability_Errors=Detection_Probability_Tuple[1]
        #plt.semilogx(Background, Detection_Probability, color=Color_L[i], linestyle='-', marker='o')
        #plt.errorbar(Background, Detection_Probability, yerr=Detection_Probability_Errors, color=Color_L[i], linestyle='', alpha=0.5, label=str(Counts)+" counts")
        ##plt.semilogx(Background, Detection_Probability, color=Color_L[i], linestyle='-', marker='o', label=str(Counts)+" cnt")
        plt.semilogx(Background, Detection_Probability, color=Color_L[i], linestyle='-', marker='.', label=str(Counts)+" cnt")
        plt.errorbar(Background, Detection_Probability, yerr=Detection_Probability_Errors, color=Color_L[i], linestyle='', alpha=0.5)
        Background_L=list(Background)
        Background_L=Background_L[1:-1]
        Background_L.append(2E-1)
        Background_L=[5E-4]+Background_L
        Detection_Probability_Kim_L=[]
        for BG in Background_L:
            Cur_Detection_Probablity_Kim=Detection_Probability_Calc_7.Detection_Probability_Calc_3(BG,Counts,Theta)
            if(Cur_Detection_Probablity_Kim==0):
                Cur_Detection_Probablity_Kim=np.nan
            Detection_Probability_Kim_L.append(Cur_Detection_Probablity_Kim)
        ##plt.semilogx(Background_L, Detection_Probability_Kim_L, color=Color_L[i], linestyle='--', marker='.')
        plt.semilogx(Background_L, Detection_Probability_Kim_L, color=Color_L[i], linestyle='--', marker='', alpha=0.5)
    plt.ylim(0,1)
    plt.xlabel("Background (cnt/pix)")
    plt.ylabel("Detection Probability")
    #plt.title("Detection Probability: Offaxis="+str(Theta)+"' & Counts="+str(Counts))
    plt.title("Detection Probability: Offaxis="+str(Theta)+"'")
    plt.legend(loc='upper right')
    #Outfilename="Detection_Probability_Offaxis_"+str(Theta)+"_"+str(Counts)+"_Counts.pdf"
    #Outfilename="Detection_Probability_Offaxis_"+str(Theta)+".pdf"
    Outfilename="./Detection_Probability_Plots/Detection_Probability_Offaxis_"+str(Theta)+".pdf"
    plt.savefig(Outfilename)
    plt.cla()
    plt.clf()

def Limiting_Counts_Calc(Background, Data_Input):
    if(isinstance(Data_Input,str)):
        Data, Data_Grouped, Data_Grouped_Mean, Data_Grouped_Sum=Process_Data(Data_Input)
    else:
        Data_Grouped_Mean=Data_Input
    Background=np.float64(Background)
    print("Background: ", Background)
    Data_Grouped_Mean_Filtered=Data_Grouped_Mean[(np.isclose(Data_Grouped_Mean["Background"], Background))]
    #print("Data_Grouped_Mean_Filtered Before: ", Data_Grouped_Mean_Filtered)
    Data_Grouped_Mean_Filtered=Data_Grouped_Mean_Filtered.sort_values(by=["Theta"])
    Detection_Probability_Tuple=Wilson_Probability_Calc(Data_Grouped_Mean_Filtered['Detection_Bool'], n=Data_Grouped_Mean_Filtered['Number_of_Samples'])
    Data_Grouped_Mean_Filtered["Detection_Probability"]=Detection_Probability_Tuple[0]
    Data_Grouped_Mean_Filtered["Detection_Probability_Errors"]=Detection_Probability_Tuple[1]
    Data_Grouped_Mean_Filtered=Data_Grouped_Mean_Filtered[Data_Grouped_Mean_Filtered["Detection_Probability"]>=0.90]
    print("Data_Grouped_Mean_Filtered:\n", Data_Grouped_Mean_Filtered)
    Data_Grouped_Min=Data_Grouped_Mean_Filtered.loc[Data_Grouped_Mean_Filtered.groupby('Theta').Detection_Probability.idxmin()]
    print("Data_Grouped_Min:\n", Data_Grouped_Min)
    Theta_A=Data_Grouped_Min["Theta"]
    Limiting_Counts_A=Data_Grouped_Min["Counts"]
    return Theta_A, Limiting_Counts_A

def Data_Interpolation(X,Y):
    F=interpolate.interp1d(X,Y,bounds_error=0,fill_value=(float("NaN"),1.0)) #P_C_f:-scipy.interpolate.interpolate.interp1d, Probablity Count Function, This is a function that interpolates the probablity and count arrays and returns the probablity as a function of counts #Note: May have to remove bounds_error variable, it also might make the data for C=30 counts wrong
    #F=interpolate.interp1d(X,Y) #P_C_f:-scipy.interpolate.interpolate.interp1d, Probablity Count Function, This is a function that interpolates the probablity and count arrays and returns the probablity as a function of counts #Note: May have to remove bounds_error variable, it also might make the data for C=30 counts wrong
    #P_C_f=interpolate.interp1d(C_L,P_L,bounds_error=1,fill_value=(float("NaN"),1.0)) #P_C_f:-scipy.interpolate.interpolate.interp1d, Probablity Count Function, This is a function that interpolates the probablity and count arrays and returns the probablity as a function of counts #Note: May have to remove bounds_error variable, it also might make the data for C=30 counts wrong
    #P_C=P_C_f(C) #P_C:-numpy.ndarray, Probablity as a function of Counts, The probablity of making a dectection for a given amount of counts, Counts is not any count but the User chosen amount of counts
    return F
"""
def Limiting_Counts_to_Theta(Limiting_Counts, Background, Data_Input="Marx_Source_Detection_Data.csv"):
    Theta_A, Limiting_Counts_A=Limiting_Counts_Calc(Background, Data_Input)
    Limiting_Counts_to_Theta=Data_Interpolation(Limiting_Counts_A,Theta_A)
    Theta=Limiting_Counts_to_Theta(Limiting_Counts)
    return Theta
"""

def Backgrounds_Calc(Data_Input="Marx_Source_Detection_Data.csv"):
    if(isinstance(Data_Input,str)):
        Data, Data_Grouped, Data_Grouped_Mean, Data_Grouped_Sum=Process_Data(Data_Input)
    Backgronds_Unique=list(set(list(np.round(Data_Grouped_Mean["Background"],4))))
    Backgronds_Unique.sort()
    return Backgronds_Unique

def Background_Exists_Check(Background, Data_Input="Marx_Source_Detection_Data.csv"):
    Background_L=Backgrounds_Calc(Data_Input=Data_Input)
    if Background in Background_L:
        return True

def Nearest_Backgrounds_Calc(Background, Data_Input="Marx_Source_Detection_Data.csv"):
    Background_L=Backgrounds_Calc(Data_Input=Data_Input)
    """
    if Background in Background_L:
        return Background
    """
    if(Background_Exists_Check(Background)):
        return Background
    for i in range(0,len(Background_L)):
        Background_Test=Background_L[i]
        if(Background_Test>Background):
            Background_Low=Background_L[i-1]
            Background_High=Background_L[i]
            return Background_Low, Background_High

def Limiting_Counts_Interpolation(Background, Data_Input="Marx_Source_Detection_Data.csv"):
    if(Background_Exists_Check(Background)):
        Theta_A, Limiting_Counts_A=Limiting_Counts_Calc(Background, Data_Input)
        return Theta_A, Limiting_Counts_A
    Background_Low, Background_High=Nearest_Backgrounds_Calc(Background, Data_Input=Data_Input)
    print("Background_Low: ", Background_Low)
    print("Background_High: ", Background_High)
    Theta_Low_A, Limiting_Counts_Low_A=Limiting_Counts_Calc(Background_Low, Data_Input=Data_Input)
    Theta_High_A, Limiting_Counts_High_A=Limiting_Counts_Calc(Background_High, Data_Input=Data_Input)
    #print("Theta_Low_A: ", Theta_Low_A)
    #print("Limiting_Counts_Low_A: ", Limiting_Counts_Low_A)
    #print("Theta_High_A: ", Theta_High_A)
    #print("Limiting_Counts_High_A: ", Limiting_Counts_High_A)
    Limiting_Counts_Interpolated_Low_A=pd.DataFrame(np.interp(list(range(0,11)), Theta_Low_A, Limiting_Counts_Low_A, left=np.nan, right=np.nan), columns=['Limiting_Counts_Interpolated_Low'], dtype=np.float64)
    #Limiting_Counts_Interpolated_Low_A=Limiting_Counts_Interpolated_Low_A.squeeze(axis=0)
    Limiting_Counts_Interpolated_Low_A=Limiting_Counts_Interpolated_Low_A.iloc[:,0]
    Theta_Interpolated_Low_A=pd.DataFrame(Limiting_Counts_Interpolated_Low_A.index.to_numpy())
    #Limiting_Counts_Interpolated_High_A=np.interp(list(range(0,11)), Theta_High_A, Limiting_Counts_High_A)
    Limiting_Counts_Interpolated_High_A=pd.DataFrame(np.interp(list(range(0,11)), Theta_High_A, Limiting_Counts_High_A, left=np.nan, right=np.nan), columns=['Limiting_Counts_Interpolated_High'], dtype=np.float64)
    #Limiting_Counts_Interpolated_High_A=Limiting_Counts_Interpolated_High_A.squeeze(axis=0)
    Limiting_Counts_Interpolated_High_A=Limiting_Counts_Interpolated_High_A.iloc[:,0]
    Theta_Interpolated_High_A=pd.DataFrame(Limiting_Counts_Interpolated_High_A.index.to_numpy())
    #print("Theta_Interpolated_Low_A: ", Theta_Interpolated_Low_A)
    #print("Theta_Interpolated_High_A: ", Theta_Interpolated_High_A)
    #print("Limiting_Counts_Interpolated_Low_A: ", Limiting_Counts_Interpolated_Low_A)
    #print("Limiting_Counts_Interpolated_High_A: ", Limiting_Counts_Interpolated_High_A)
    #Slope=(Limiting_Counts_Interpolated_High_A-Limiting_Counts_Interpolated_Low_A)/(Theta_Interpolated_High_A-Theta_Interpolated_Low_A) #m=(y2-y1)/(x2-x1)
    #print("Limiting_Counts_Interpolated_High_A-Limiting_Counts_Interpolated_Low_A: ", Limiting_Counts_Interpolated_High_A-Limiting_Counts_Interpolated_Low_A)
    Slope=(Limiting_Counts_Interpolated_High_A-Limiting_Counts_Interpolated_Low_A)/(Background_High-Background_Low) #m=(y2-y1)/(x2-x1)
    #print("Slope:\n", Slope)
    #Interpolated_Limiting_Counts=Slope*Background #y=mx+b
    Interpolated_Limiting_Counts=Slope*(Background-Background_Low)+Limiting_Counts_Interpolated_Low_A #y=m(x-x1)+y1
    print("Interpolated_Limiting_Counts:\n", Interpolated_Limiting_Counts)
    Theta_Interpolated_A=pd.DataFrame(Interpolated_Limiting_Counts.index.to_numpy()).iloc[:,0]
    return Theta_Interpolated_A, Interpolated_Limiting_Counts

def Plot_Theta_Inversion(Limiting_Counts_Data):
    Limiting_Counts_Data=Limiting_Counts_Data.sort_values(by=['Limiting_Counts'])
    plt.plot(Limiting_Counts_Data["Limiting_Counts"],Limiting_Counts_Data["Theta"])
    plt.savefig("Inverted_Theta_Test.pdf")

def Theta_Interpolation(Limiting_Counts, Limiting_Counts_Data):
    Theta_A=Limiting_Counts_Data["Theta"]
    Limiting_Counts_A=Limiting_Counts_Data["Limiting_Counts"]
    Theta_L=list(Theta_A)
    Nearest_Counts_L=[]
    for i in range(0,len(Theta_L)-1):
        Low_Row=Limiting_Counts_Data.iloc[[i]]
        High_Row=Limiting_Counts_Data.iloc[[i+1]]
        #print("Low_Row: ", Low_Row)
        #print("High_Row: ", High_Row)
        Theta_Low=Low_Row["Theta"].values[0]
        Limiting_Counts_Low=Low_Row["Limiting_Counts"].values[0]
        #Limiting_Counts_Low=Low_Row.get('Limiting_Counts')
        #print("Limiting_Counts_Low: ", Limiting_Counts_Low)
        #print("type(Limiting_Counts_Low): ", type(Limiting_Counts_Low))
        Theta_High=High_Row["Theta"].values[0]
        Limiting_Counts_High=High_Row["Limiting_Counts"].values[0]
        #Limiting_Counts_High=High_Row.get('Limiting_Counts')
        #print("Limiting_Counts_High: ", Limiting_Counts_High)
        if((Limiting_Counts>Limiting_Counts_Low) and (Limiting_Counts<Limiting_Counts_High) or (Limiting_Counts<Limiting_Counts_Low) and (Limiting_Counts>Limiting_Counts_High)):
            #print("Inside")
            #Nearest_Backgrounds_L.append([Limiting_Counts_Low,Limiting_Counts_High])
            Nearest_Counts_L.append([[Theta_Low,Limiting_Counts_Low],[Theta_High,Limiting_Counts_High]])
    #print("Nearest_Counts_L: ", Nearest_Counts_L)
    Interpolated_Theta_L=[]
    for Nearest_Counts in Nearest_Counts_L:
        Low_Point=Nearest_Counts[0]
        Theta_Low=Low_Point[0]
        Limiting_Counts_Low=Low_Point[1]
        High_Point=Nearest_Counts[1]
        Theta_High=High_Point[0]
        Limiting_Counts_High=High_Point[1]
        #Slope=(Limiting_Counts_High-Limiting_Counts_Low)/(Theta_High-Theta_Low) #m=(y2-y1)/(x2-x1)
        Slope=(Theta_High-Theta_Low)/(Limiting_Counts_High-Limiting_Counts_Low) #m=(y2-y1)/(x2-x1)
        print("Slope: ", Slope)
        #y=m(x-x1)+y1
        Cur_Interpolated_Theta=Slope*(Limiting_Counts-Limiting_Counts_Low)+Theta_Low
        Interpolated_Theta_L.append(Cur_Interpolated_Theta)
    return Interpolated_Theta_L


def Limiting_Counts_to_Theta(Limiting_Counts, Background, Data_Input="Marx_Source_Detection_Data.csv"):
    Theta_A, Limiting_Counts_A=Limiting_Counts_Interpolation(Background, Data_Input)
    print("Theta_A: ", Theta_A)
    print("Limiting_Counts_A: ", Limiting_Counts_A)
    Limiting_Counts_Data=pd.DataFrame({'Theta': Theta_A, 'Limiting_Counts': Limiting_Counts_A})
    print("Limiting_Counts_Data: ", Limiting_Counts_Data)
    """
    Limiting_Counts_Data=Limiting_Counts_Data.sort_values(by=['Limiting_Counts'])
    #Plot_Theta_Inversion(Limiting_Counts_Data)
    Theta_A=Limiting_Counts_Data["Theta"]
    Limiting_Counts_A=Limiting_Counts_Data["Limiting_Counts"]
    print("Theta_A After: ", Theta_A)
    print("Limiting_Counts_A After: ", Limiting_Counts_A)
    """
    Interpolated_Theta_L=Theta_Interpolation(Limiting_Counts, Limiting_Counts_Data)
    ##Limiting_Counts_to_Theta_Function=Data_Interpolation(Limiting_Counts_A,Theta_A)
    ##Theta=Limiting_Counts_to_Theta_Function(Limiting_Counts)
    return Interpolated_Theta_L

def Limiting_Counts_Annuli_Calc(Limiting_Counts_Low, Limiting_Counts_High, Background, Data_Input="Marx_Source_Detection_Data.csv"):
    Theta_Intersection_L_Low=Limiting_Counts_to_Theta(Limiting_Counts_Low, Background, Data_Input=Data_Input)
    Theta_Intersection_L_High=Limiting_Counts_to_Theta(Limiting_Counts_High, Background, Data_Input=Data_Input)
    Theta_Intersection_L=Theta_Intersection_L_Low+Theta_Intersection_L_High
    Theta_Intersection_L.sort()
    print("Theta_Intersection_L: ", Theta_Intersection_L)
    Theta_A, Limiting_Counts_A=Limiting_Counts_Interpolation(Background)
    Limiting_Counts_Data=pd.DataFrame({'Theta': Theta_A, 'Limiting_Counts': Limiting_Counts_A})
    Limiting_Counts_Data=Limiting_Counts_Data.dropna()
    Theta_A=Limiting_Counts_Data['Theta']
    Limiting_Counts_A=Limiting_Counts_Data['Limiting_Counts']
    print("Limiting_Counts_A: ", Limiting_Counts_A)
    #Inital_Limiting_Counts=Limiting_Counts_A[Limiting_Counts_A["Theta"]==0]
    #Limiting_Counts_A=Limiting_Counts_A.dropna()
    Inital_Theta=Theta_A.values[0]
    Inital_Limiting_Counts=Limiting_Counts_A.values[0]
    print("Inital_Limiting_Counts: ", Inital_Limiting_Counts)
    ##if((Inital_Limiting_Counts>Limiting_Counts_Low) and (Inital_Limiting_Counts<Limiting_Counts_High)):
    if((Inital_Limiting_Counts>=Limiting_Counts_Low) and (Inital_Limiting_Counts<Limiting_Counts_High)):
        Theta_Intersection_L=[Inital_Theta]+Theta_Intersection_L
    Final_Theta=Theta_A.values[-1]
    Final_Limiting_Counts=Limiting_Counts_A.values[-1]
    print("Final_Limiting_Counts: ", Final_Limiting_Counts)
    ##if((Final_Limiting_Counts>Limiting_Counts_Low) and (Final_Limiting_Counts<Limiting_Counts_High)):
    if((Final_Limiting_Counts>Limiting_Counts_Low) and (Final_Limiting_Counts<=Limiting_Counts_High)):
        Theta_Intersection_L=Theta_Intersection_L+[Final_Theta]
    print("Theta_Intersection_L After: ", Theta_Intersection_L)
    Theta_Intersection_HL=[]
    if(len(Theta_Intersection_L)>0):
        for i in range(0,len(Theta_Intersection_L)-1, 2):
            First_Intersection=Theta_Intersection_L[i]
            Second_Intersection=Theta_Intersection_L[i+1]
            Cur_Set=[First_Intersection,Second_Intersection]
            Theta_Intersection_HL.append(Cur_Set)
    return Theta_Intersection_HL


def Limiting_Counts_Plot(Background_L, Fpath):
    Color_L=['b','g','r','c','m','y','orange']
    Data, Data_Grouped, Data_Grouped_Mean, Data_Grouped_Sum=Process_Data(Fpath)
    for i in range(0,len(Background_L)):
        Background=Background_L[i]
        ###Theta_A, Limiting_Counts_A=Limiting_Counts_Calc(Background, Data_Grouped_Mean)
        Theta_A, Limiting_Counts_A=Limiting_Counts_Interpolation(Background)
        #print("Limiting_Counts_A: ", Limiting_Counts_A)
        ##Label_Str=str("{:0.0E}".format(Background))
        ##Label_Str.replace("-0", "-")
        Label_Str=str(Background)
        plt.plot(Theta_A,Limiting_Counts_A, marker='.', color=Color_L[i], label=Label_Str, alpha=0.60)
        #plt.semilogy(Theta_A,Limiting_Counts_A, marker='.', color=Color_L[i], label=Label_Str, alpha=0.75)
    #plt.axhline(y=10, color='r', linestyle='--')
    plt.axhline(y=11, color='r', linestyle='--')
    plt.axhline(y=12, color='b', linestyle='--')
    plt.legend(title="Background (cnt/pix)", loc='upper left')
    plt.xlabel("Offaxis Angle (arcmin)")
    plt.ylabel("Limiting Counts (cnt)")
    #plt.title("Detection Probability: Offaxis="+str(Theta)+"' & Counts="+str(Counts))
    #plt.title("Limiting Counts: Background="+str(Background)+" (cnt/pix)")
    plt.title("Limiting Counts vs Offaxis Angle")
    ##Outfilename="./Detection_Probability_Plots/Limiting_Counts_"+str("{:0.0E}".format(Background))+".pdf"
    ##Outfilename=Outfilename.replace("-0", "-")
    Outfilename="./Detection_Probability_Plots/Limiting_Counts.pdf"
    print("Outfilename: ", Outfilename)
    plt.savefig(Outfilename)
    plt.cla()
    plt.clf()

def Excess_Sources_Plot(Fpath):
    Data, Data_Grouped, Data_Grouped_Mean, Data_Grouped_Sum=Process_Data(Fpath)
    Data_Grouped_Mean=Data_Grouped_Mean.sort_values(by=['SNR'])
    print("Data_Grouped_Mean: ", Data_Grouped_Mean)
    #plt.plot(Data_Grouped_Mean["SNR"], Data_Grouped_Mean["SDA"])
    Excess_Sources_A=Data_Grouped_Mean["SDA"]-Data_Grouped_Mean["SDB"]
    plt.semilogx(Data_Grouped_Mean["SNR"], Excess_Sources_A, ".")
    plt.savefig("SDA_vs_SNR.pdf")

def Detection_Threshold_Count_Range_Calc(Fpath, Save_Output_Bool=False):
    with pd.option_context('display.max_columns', None):  # more options can be specified also
        Data, Data_Grouped, Data_Grouped_Mean, Data_Grouped_Sum=Process_Data(Fpath)
        Data_Grouped_Mean_2=Data_Grouped_Mean.groupby(['Phi', 'Theta', 'Background'])
        count=0
        if(Save_Output_Bool):
            f = open("Count_Limits.csv", "w")
            Header="Phi,Theta,Background,Counts_Low,Counts_High\n"
            f.write(Header)
        for key, item in Data_Grouped_Mean_2:
            Cur_Data=Data_Grouped_Mean_2.get_group(key)
            Counts_L=list(Cur_Data["Counts"])
            Match_Bool=False
            for i in range(0,len(Counts_L)):
                ##Cur_Detection_Probablity=Cur_Data.iloc[i]['SDB']
                Cur_Detection_Probablity=Wilson_Probability_Calc(Cur_Data.iloc[i]['Detection_Bool'])[0]
                #print("Cur_Detection_Probablity: ", Cur_Detection_Probablity)
                if(Cur_Detection_Probablity>0.90):
                    Match_Index=i
                    Match_Bool=True
                    break
            if(Match_Bool):
                Cur_Data_Upper_Limit=Cur_Data.iloc[Match_Index]
                if(i>0):
                    Cur_Data_Lower_Limit=Cur_Data.iloc[Match_Index-1]
                #print("Detection Limits: ", (Cur_Data_Lower_Limit['SDB'], Cur_Data_Upper_Limit['SDB']))
                #print((Cur_Data["Phi"].iloc[Match_Index], Cur_Data["Theta"].iloc[Match_Index],  Cur_Data["Background"].iloc[Match_Index]))
                #print("Count Limits: ", (Cur_Data_Lower_Limit['Counts'], Cur_Data_Upper_Limit['Counts']))
                Print_String=str(Cur_Data["Phi"].iloc[Match_Index])+","+str(Cur_Data["Theta"].iloc[Match_Index])+","+str(np.round(Cur_Data["Background"].iloc[Match_Index], 4))+":  "+str((Cur_Data_Lower_Limit['Counts'], Cur_Data_Upper_Limit['Counts']))
                print(Print_String)
                Outstring=str(Cur_Data["Phi"].iloc[Match_Index])+","+str(Cur_Data["Theta"].iloc[Match_Index])+","+str(np.round(Cur_Data["Background"].iloc[Match_Index], 4))+","+str(Cur_Data_Lower_Limit['Counts'])+","+str(Cur_Data_Upper_Limit['Counts'])+"\n"
                print("Outstring: ", Outstring)
                if(Save_Output_Bool):
                    f.write(Outstring)
                count=count+1
            else:
                print("Missed Phi, Theta, Background: ", (Cur_Data["Phi"].iloc[Match_Index], Cur_Data["Theta"].iloc[Match_Index],  Cur_Data["Background"].iloc[Match_Index]))
        print("count: ", count)


#Merge_Data()
##Detection_Threshold_Count_Range_Calc("Marx_Source_Detection_Data.csv")
#print(Wilson_Probability_Calc(44))
#print(Wald_Probability_Calc(44))
#Probability_Model_Plotting()
#Plot_Detection_Probability(0, [3,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(1, [3,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(2, [3,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(5, [3,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(10, [3,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(10, [3,15,150], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(10, [3,15,150,180,195], "Marx_Source_Detection_Data.csv")
#print(Alpha_Quantile(0.95))
#print(Probit(Alpha_Quantile(0.95)))
#print(Probit(0.025))
#print(Alpha_Quantile(0.682689492137086))
#print(Probit(Alpha_Quantile(0.682689492137086)))
#print(Probit(Alpha_Quantile(0.682689492137086)))
#print(Detection_Probability_Calc_7.Detection_Probability_Calc_3(0.01,3,1))
#Excess_Sources_Plot("Marx_Source_Detection_Data.csv")

#Plot_Detection_Probability(0, [3,5,10,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(1, [3,5,10,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(2, [3,5,10,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(5, [3,5,10,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(10, [3,5,10,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(10, [3,15,150], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(10, [3,15,150,180,195], "Marx_Source_Detection_Data.csv")

#Plot_Detection_Probability(0, [3,7,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(1, [3,7,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(2, [3,7,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(5, [3,7,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(8, [3,7,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(9, [3,7,15], "Marx_Source_Detection_Data.csv")
#Plot_Detection_Probability(10, [15,60,150], "Marx_Source_Detection_Data.csv")
#Process_Data("Marx_Source_Detection_Data.csv")
#Plot_Limiting_Counts(1E-4, "Marx_Source_Detection_Data.csv")
#Plot_Limiting_Counts(1E-3, "Marx_Source_Detection_Data.csv")
#Plot_Limiting_Counts(1E-2, "Marx_Source_Detection_Data.csv")
#Plot_Limiting_Counts(1E-1, "Marx_Source_Detection_Data.csv")
#Limiting_Counts_Plot([1E-4,1E-3,1E-2,1E-1], "Marx_Source_Detection_Data.csv")
#Limiting_Counts_Plot([1E-4], "Marx_Source_Detection_Data.csv")
#Limiting_Counts_Plot([1E-3], "Marx_Source_Detection_Data.csv")
#Limiting_Counts_Plot([1E-1,1E-2,1E-3,1E-4], "Marx_Source_Detection_Data.csv")
#Limiting_Counts_Plot([1E-1,5E-2,1E-2,1E-3,1E-4], "Marx_Source_Detection_Data.csv")
#print(Limiting_Counts_Calc(1E-3, "Marx_Source_Detection_Data.csv"))
#print(Limiting_Counts_to_Theta(10,1E-3, "Marx_Source_Detection_Data.csv"))
#print(Limiting_Counts_to_Theta(10,25E-3, "Marx_Source_Detection_Data.csv"))
#print(Limiting_Counts_to_Theta(5,1E-2, "Marx_Source_Detection_Data.csv"))
#print(Limiting_Counts_to_Theta(10,1E-2, "Marx_Source_Detection_Data.csv"))
#print(Backgrounds_Calc())
#print(Nearest_Backgrounds_Calc(1E-3))
#print(Nearest_Backgrounds_Calc(25E-3))
#print(Limiting_Counts_Interpolation(25E-3))
#print(Limiting_Counts_to_Theta(10,25E-3, "Marx_Source_Detection_Data.csv"))
#Limiting_Counts_Plot([1E-1,1E-2,1E-3,1E-4], "Marx_Source_Detection_Data.csv")
#Limiting_Counts_Plot([1E-1,1E-2,1E-3,1E-4,25E-3], "Marx_Source_Detection_Data.csv")
#Limiting_Counts_Plot([1E-1,1E-2,1E-3,1E-4,25E-3,5E-1,9E-1], "Marx_Source_Detection_Data.csv")
#Limiting_Counts_Plot([9E-1,1E-1,25E-3,1E-2,1E-3,1E-4], "Marx_Source_Detection_Data.csv")
#Limiting_Counts_Plot([1E-1,25E-3,1E-2,1E-3,1E-4], "Marx_Source_Detection_Data.csv")
#print(Limiting_Counts_to_Theta(10,1E-2, "Marx_Source_Detection_Data.csv"))
#print(Limiting_Counts_to_Theta(10,25E-3, "Marx_Source_Detection_Data.csv"))
#print(Limiting_Counts_to_Theta(10,1E-3, "Marx_Source_Detection_Data.csv"))
#print(Limiting_Counts_to_Theta(10,1E-4, "Marx_Source_Detection_Data.csv"))
#print(Limiting_Counts_to_Theta(5,1E-4, "Marx_Source_Detection_Data.csv"))
#print(Limiting_Counts_Annuli_Calc(10, 20, 1E-2))
#print(Limiting_Counts_Annuli_Calc(0, 50, 1E-2))
#print(Limiting_Counts_Annuli_Calc(50, 70, 1E-2))
#print(Limiting_Counts_Annuli_Calc(0, 50, 25E-3))
#print(Limiting_Counts_Annuli_Calc(20, 10, 1E-2))
#print(Limiting_Counts_Annuli_Calc(44, 45, 1E-2))
#print(Limiting_Counts_Annuli_Calc(5, 6, 1E-2))
#print(Limiting_Counts_Annuli_Calc(6, 7, 1E-2))
#print(Limiting_Counts_Annuli_Calc(43, 44, 1E-2))
#print(Limiting_Counts_Annuli_Calc(6, 44, 1E-2))
#print(Limiting_Counts_Annuli_Calc(44, 45, 1E-2))
print(Limiting_Counts_Annuli_Calc(11, 12, 1E-2))
