import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from os import system
import sys

ir = os.path.dirname(__file__)
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))

from File_Query_Code import File_Query_Code_5
from Galaxy_Name_Reducer import Galaxy_Name_Reducer
from Background_Finder import Background_Finder_10


def Background_Calc(Gname):
    Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
    Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
    print("Evt2_File_H_L: ", Evt2_File_H_L)
    Fov1_File_H_L=File_Query_Code_5.File_Query(Gname,"fov1")
    print("Fov1_File_H_L: ", Fov1_File_H_L)
    Reg_File_H_L=File_Query_Code_5.File_Query(Gname,"reg")
    print("Reg_File_H_L: ", Reg_File_H_L)
    if((len(Evt2_File_H_L)!=len(Fov1_File_H_L)) or (len(Evt2_File_H_L)!=len(Reg_File_H_L)) or (len(Fov1_File_H_L)!=len(Reg_File_H_L))):
        raise "Missing File!!!"
    Background_HL=[]
    for i in range(0,len(Evt2_File_H_L)):
        Cur_Evt2_File_L=Evt2_File_H_L[i]
        Cur_ObsID=Cur_Evt2_File_L[0]
        Cur_Evt2_Path=Cur_Evt2_File_L[1]
        Cur_Fov1_File_L=Fov1_File_H_L[i]
        Cur_Fov1_ObsID=Cur_Fov1_File_L[0]
        Cur_Fov1_Path=Cur_Fov1_File_L[1]
        Cur_Reg_File_L=Reg_File_H_L[i]
        Cur_Reg_ObsID=Cur_Reg_File_L[0]
        Cur_Reg_Path=Cur_Reg_File_L[1]
        if((Cur_ObsID!=Cur_Fov1_ObsID) or (Cur_ObsID!=Cur_Reg_ObsID) or (Cur_Fov1_ObsID!=Cur_Reg_ObsID)):
            raise "Mismatched File!!!"
        Cur_Background_Ratio_Tuple=Background_Finder_10.Background_Finder_V2(Gname,Cur_Evt2_Path,Cur_Reg_Path,Cur_Fov1_Path)
        #print("Cur_Background_Ratio_Tuple: ", Cur_Background_Ratio_Tuple)
        Cur_Background_L=[Cur_ObsID, Cur_Background_Ratio_Tuple]
        Background_HL.append(Cur_Background_L)
    return Background_HL

#print(Background_Calc('NGC 3077'))
