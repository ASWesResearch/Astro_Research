import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re

def Clean_TSV_Header(Fpath):
    File = open(Fpath, "r")
    Str_L=File.readlines()
    #New_Str_L=[]
    Info_Str=""
    Data_Str=""
    for Cur_Line in Str_L:
        if(Cur_Line[0]=="#"):
            Info_Str=Info_Str+Cur_Line
            #continue
        else:
            #New_Str_L.append(Cur_Line)
            Data_Str=Data_Str+Cur_Line
            #Data_Str=Data_Str+Cur_Line+"\n"
            #Data_Str=Data_Str+"\n"+Cur_Line
    return Data_Str, Info_Str

def Read_CSC_TSV(Fpath):
    Data=pd.read_csv(Fpath, sep='\t', header=63)
    print(Data.keys())

Read_CSC_TSV("../CSC_Data/635.tsv")
