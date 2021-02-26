import pandas as pd
import sys
import os
#from os import system
path_GR="/Volumes/xray/anthony/Research_Git"
sys.path.append(os.path.abspath(path_GR))
from Galaxy_Name_Reducer import Galaxy_Name_Reducer
def Standard_File_Query(Gname=False,ObsID=False,Source_Num=False,Cut_Bool_Key_L=False,Standard_File_Path="/Volumes/xray/anthony/Simon_Sandboxed_Code/Source_Counts_To_Flux_Converter/counts_info_Flux_Calc.csv"):
    """
    Gname:-str, Galaxy Name, The galaxy name associated with the data of intrest
    ObsID:-int or str, Observation ID, The ObsID associated with the data of intrest
    Source_Num:-int or str, Source Number, The source number associated with the data of intrest
    Standard_File_Path:-str, Standard File Path, The path to the standard file (counts_info_Flux_Calc.csv) contianing the data of intrest

    Returns:-pandas.core.frame.DataFrame, This code returns the data frame of the filtered data.

    This code reads the data in the standard file and then can filter it by Galaxy Name, ObsID or Source Number and then returns the filtered DataFrame.
    """
    #Raises Exception if a source number without a coresponding ObsID is inputed
    if((Source_Num!=False) and (ObsID==False)):
        raise Exception('ObsID must be specified if Source_Num is specified')
    data=pd.read_csv(Standard_File_Path)
    #This filters the data by Galaxy Name
    if(Gname!=False):
        Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
        data=data[data.Gname_Modifed==Gname_Modifed] #The correct spelling is Gname_Modified not Gname_Modifed. I need to go back and fix this
        data=data.reset_index(drop=True)
    #This Filters the data by ObsID
    if(ObsID!=False):
        ObsID=int(ObsID)
        data=data[data.OBSID==ObsID]
        data=data.reset_index(drop=True)
        #This Filters the data already filtered by ObsID by Source Number
        if(Source_Num!=False):
            Source_Num=int(Source_Num)
            data=data[data.SOURCE==Source_Num]
            data=data.reset_index(drop=True)
    #Filters Data on custom boolean key (Valid keys for counts_info_Flux_Calc.csv: 'Flux_Cut_Bool[.3-7.5]', 'Inside_FOV_Bool', 'Outside_D25_Bool')
    if(isinstance(Cut_Bool_Key_L, list)):
        for Cut_Bool_Key in Cut_Bool_Key_L:
            data=data.dropna(subset=[Cut_Bool_Key]) #NaN values must be removed before bool cut
            data=data[data[Cut_Bool_Key]]
            data=data.reset_index(drop=True)
    #print "data.columns:\n", data.columns
    return data

#print Standard_File_Query("NGC 3631")
#print Standard_File_Query("NGC_3877")
#print Standard_File_Query("NGC_3877",1971)
#print Standard_File_Query("NGC_3877",1971,1)
#print Standard_File_Query(ObsID=1971)
#print Standard_File_Query(ObsID=1971,Source_Num=1)
#print Standard_File_Query(ObsID="1971",Source_Num="1")
#print Standard_File_Query(Source_Num=1)
#print Standard_File_Query()
#print type(Standard_File_Query())
#print Standard_File_Query("NGC_3877",Cut_Bool_Key_L=['Flux_Cut_Bool[.3-7.5]','Inside_FOV_Bool','Outside_D25_Bool'])
#print Standard_File_Query("NGC_3877",Cut_Bool_Key_L=['Outside_D25_Bool'])
#print Standard_File_Query("NGC_3877",Cut_Bool_Key_L=['Inside_FOV_Bool'])
#print Standard_File_Query("NGC_3877",Cut_Bool_Key_L=['Inside_FOV_Bool','Flux_Cut_Bool[.3-7.5]'])
#print Standard_File_Query(Cut_Bool_Key_L=['Inside_FOV_Bool','Flux_Cut_Bool[.3-7.5]'])
#print Standard_File_Query(Cut_Bool_Key_L=['Flux_Cut_Bool[.3-7.5]'])
#print Standard_File_Query(Cut_Bool_Key_L=['Inside_FOV_Bool'])
#print Standard_File_Query("NGC_3877",1971,1,Cut_Bool_Key_L=['Flux_Cut_Bool[.3-7.5]','Inside_FOV_Bool','Outside_D25_Bool'])
#print Standard_File_Query(Cut_Bool_Key_L=['Flux_Cut_Bool[.3-7.5]','Inside_FOV_Bool','Outside_D25_Bool'])
