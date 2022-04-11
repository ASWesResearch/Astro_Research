import pandas as pd
import os
from os import system
import sys
dir = os.path.dirname(__file__)
path=os.path.realpath('../')
sys.path.append(os.path.abspath(path))
from Galaxy_Name_Reducer import Galaxy_Name_Reducer
from Galaxy_Name_Query import Galaxy_Name_Query
def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))
"""
def Compare(L1,L2):
    L1_In_L2=[]
    L1_Not_In_L2=[]
    L2_Not_In_L1=[]
    for X in L1:
        if X in L2:
            L1_In_L2.append(X)
    for X in L1:
        if X not in L2:
            L1_Not_In_L2.append(X)
    for X in L2:
        if X not in L1:
            L2_Not_In_L1.append(X)
    return [L1_In_L2, L1_Not_In_L2, L2_Not_In_L1]
"""
def Intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
def Subtraction(li1, li2):
    return list(set(li1) - set(li2))
def Compare(L1,L2):
    L1_In_L2=[]
    L1_Not_In_L2=[]
    L2_Not_In_L1=[]
    ##for X in L1 and L2:
        ##L1_In_L2.append(X)
    L1_In_L2=Intersection(L1, L2)
    L1_Not_In_L2=Subtraction(L1, L2)
    L2_Not_In_L1=Subtraction(L2, L1)
    return [L1_In_L2, L1_Not_In_L2, L2_Not_In_L1]

def Main():
    New_A=pd.read_csv("/Volumes/xray/anthony/Research_Git/SQL_Standard_File/ocatResult_Modified.csv")
    New_A=New_A[New_A["Exposure "]>9.0]
    Gname_New_A=New_A["Target Name"]
    Gname_New_L=list(Gname_New_A)
    Old_A=pd.read_csv("/Volumes/xray/anthony/Research_Git/SQL_Standard_File/SQL_Standard_File.csv")
    #print New_L
    Gname_Old_A=Old_A["queriedName"]
    Gname_Old_L=list(Gname_Old_A)
    New_L=list(set(Gname_New_L))
    New_L_Reduced=[]
    for Gname_New in New_L:
        New_Galaxy_Name_Queried_A=Galaxy_Name_Query.Galaxy_Name_Query(Gname_New)
        if(New_Galaxy_Name_Queried_A==False):
            #Error exception
            print "Query Error: ", Gname_New
            continue
        New_Galaxy_Name_Queried=Galaxy_Name_Query.Galaxy_Name_Query(Gname_New)[0]
        print "New_Galaxy_Name_Queried: ", New_Galaxy_Name_Queried
        New_Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(New_Galaxy_Name_Queried)
        New_L_Reduced.append(New_Gname_Modifed)
    New_L=list(set(New_L_Reduced))
    Old_L=list(set(Gname_Old_L))
    Old_L_Reduced=[]
    for Gname_Old in Old_L:
        Old_Galaxy_Name_Queried=Galaxy_Name_Query.Galaxy_Name_Query(Gname_Old)
        Old_Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Old_Galaxy_Name_Queried)
        Old_L_Reduced.append(Old_Gname_Modifed)
    Old_L=list(set(Old_L_Reduced))
    List_Length_Subtraction=len(New_L)-len(Old_L)
    print "len(Old_L): ", len(Old_L)
    print "len(New_L): ", len(New_L)
    print "List_Length_Subtraction: ", List_Length_Subtraction
    Diff_L=Diff(Old_L, New_L)
    print "len(Diff_L): ", len(Diff_L)
    #print Diff_L
    Compare_HL=Compare(Old_L, New_L)
    Common_L=Compare_HL[0]
    print "Common_L:\n", Common_L
    print "len(Common_L): ", len(Common_L)
    Old_Not_In_New=Compare_HL[1]
    print "Old_Not_In_New:\n", Old_Not_In_New
    print "len(Old_Not_In_New): ", len(Old_Not_In_New)
    New_Not_In_Old=Compare_HL[2]
    print "New_Not_In_Old:\n", New_Not_In_Old
    print "len(New_Not_In_Old): ", len(New_Not_In_Old)

Main()
