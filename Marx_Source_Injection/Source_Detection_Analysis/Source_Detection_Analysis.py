import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
from os import system
import sys
from functools import partial
from scipy.special import erfinv, erf

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
                        Cur_Data=pd.read_csv(Cur_Filepath)
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
    with pd.option_context('display.max_columns', None):  # more options can be specified also
        #print("Data:\n", Data)
        Data_Grouped=Data.groupby(['Grouping_Key'])
        for key, item in Data_Grouped:
            Cur_Data=Data_Grouped.get_group(key)
            #print("Cur_Data\n: ", Cur_Data)
        Data_Grouped_Mean=Data.groupby(['Grouping_Key']).mean()
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
        Detection_Probability_Tuple=Wilson_Probability_Calc(Data_Grouped_Mean_Filtered['Detection_Bool'])
        Detection_Probability=Detection_Probability_Tuple[0]
        Detection_Probability_Errors=Detection_Probability_Tuple[1]
        #plt.semilogx(Background, Detection_Probability, color=Color_L[i], linestyle='-', marker='o')
        #plt.errorbar(Background, Detection_Probability, yerr=Detection_Probability_Errors, color=Color_L[i], linestyle='', alpha=0.5, label=str(Counts)+" counts")
        plt.semilogx(Background, Detection_Probability, color=Color_L[i], linestyle='-', marker='o', label=str(Counts)+" cnt")
        plt.errorbar(Background, Detection_Probability, yerr=Detection_Probability_Errors, color=Color_L[i], linestyle='', alpha=0.5)
        Background_L=list(Background)
        Background_L=Background_L[1:-1]
        Background_L.append(2E-1)
        Background_L=[5E-4]+Background_L
        Detection_Probability_Kim_L=[]
        for BG in Background_L:
            Cur_Detection_Probablity_Kim=Detection_Probability_Calc_7.Detection_Probability_Calc_3(BG,Counts,Theta)
            Detection_Probability_Kim_L.append(Cur_Detection_Probablity_Kim)
        plt.semilogx(Background_L, Detection_Probability_Kim_L, color=Color_L[i], linestyle='--', marker='.')
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

def Detection_Threshold_Count_Range_Calc(Fpath):
    with pd.option_context('display.max_columns', None):  # more options can be specified also
        Data, Data_Grouped, Data_Grouped_Mean, Data_Grouped_Sum=Process_Data(Fpath)
        Data_Grouped_Mean_2=Data_Grouped_Mean.groupby(['Phi', 'Theta', 'Background'])
        count=0
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
                count=count+1
            else:
                print("Missed Phi, Theta, Background: ", (Cur_Data["Phi"].iloc[Match_Index], Cur_Data["Theta"].iloc[Match_Index],  Cur_Data["Background"].iloc[Match_Index]))
        print("count: ", count)


#Merge_Data()
Detection_Threshold_Count_Range_Calc("Marx_Source_Detection_Data.csv")
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
