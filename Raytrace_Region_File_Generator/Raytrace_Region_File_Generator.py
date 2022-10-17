from astropy.io import ascii
import os
from os import system
import sys
import numpy
import re
#import pyregion
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))
from Coords_Calc import Coords_Calc
from ObsID_From_CSV_Query import ObsID_From_CSV_Query
#Constants:
#Root_Path="/Volumes/"
Root_Path="/opt/"
def File_Num(Fname): #Need to modify to make sure only the number is used. There is a bug where "10new" is used instead of "10"
    Fname_L=Fname.split(".")
    Fname_Number_Str=Fname_L[0]
    Fname_Number_Int=int(Fname_Number_Str) #Some Bug pointed here ! ! ! Seems like a filename I did not consider with the string segment "10new" is casuing an error.
    return Fname_Number_Int
def Raytrace_Region_File_Generator(ObsID):
    Header_String='# Region file format: DS9 version 3.0\nglobal color=blue font="helvetica 10 normal" select=1 edit=1 move=1 delete=1 include=1 fixed=0\n'
    path_Coords=Root_Path+"xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"
    path_Obs=path_Coords+str(ObsID)+'/'
    directory_Obs=os.path.dirname(path_Obs)
    if not os.path.exists(directory_Obs):
        os.makedirs(directory_Obs)
    Raytrace_Reg_Fname="ObsID_"+str(ObsID)+"_Raytraced_Source_Regions.reg"
    Raytrace_Reg_Fpath=path_Obs+Raytrace_Reg_Fname
    print("Raytrace_Reg_Fpath: ", Raytrace_Reg_Fpath)
    ObsID_Reg_File=open(Raytrace_Reg_Fpath,"w")
    ObsID_Reg_File.write(Header_String)
    #f=open(ObsID_Reg_File,"w")
    Trace_Path=Root_Path+"/xray/spirals/trace/"+"/"+str(ObsID)+"/"
    Trace_LS_String=os.popen("ls " +Trace_Path+"| grep '.reg' | grep -v 'bkg' | grep -v '.fits' | grep -v 'new' | grep -v 'sky'").read()
    Trace_LS_String_L=Trace_LS_String.split("\n")
    #print "Trace_LS_String_L Before Pop: ", Trace_LS_String_L
    #print "len(Trace_LS_String_L) Before Pop: ", len(Trace_LS_String_L)
    Trace_LS_String_L.pop(len(Trace_LS_String_L)-1)
    #print "Trace_LS_String_L After Pop:", Trace_LS_String_L
    Trace_LS_String_L.sort(key=File_Num)
    #print "Trace_LS_String_L After Sort:", Trace_LS_String_L
    #print "len(Trace_LS_String_L) After Pop:", len(Trace_LS_String_L)
    for Cur_reg_fname in Trace_LS_String_L:
        Cur_reg_fpath=Trace_Path+Cur_reg_fname
        #print "Cur_reg_fpath: ", Cur_reg_fpath
        Cur_Reg_File=open(Cur_reg_fpath)
        #print "Cur_Reg_File: ", Cur_Reg_File
        Cur_Reg_Str=Cur_Reg_File.read()
        #print "Cur_Reg_Str: ", Cur_Reg_Str
        Cur_Reg_Str_L=Cur_Reg_Str.split("\n")
        #print "Cur_Reg_Str_L: ", Cur_Reg_Str_L
        #Cur_Header=Cur_Reg_Str_L[0]+"\n"+Cur_Reg_Str_L[1]+"\n"
        #print "Cur_Header:\n", Cur_Header
        Cur_Shape_Str=Cur_Reg_Str_L[2]
        #print "Cur_Shape_Str: ", Cur_Shape_Str
        #Cur_Shape_Str_L=Cur_Shape_Str.split(";")
        #Cur_Shape_Str_Reduced=Cur_Shape_Str_L[1]
        #ObsID_Reg_File.write(Cur_Shape_Str_Reduced+"\n")
        ObsID_Reg_File.write(Cur_Shape_Str+"\n")
        Cur_Reg_File.close()
    ObsID_Reg_File.close()
    #return Raytrace_Reg_Fpath
    #/Volumes/xray/simon/all_chandra_observations/10025/primary
    ObsID_Filepath=Root_Path+"/xray/simon/all_chandra_observations/"+str(ObsID)+"/primary/"
    Evt2_LS_String=os.popen("ls " +ObsID_Filepath+"| grep 'evt2.fit'").read()
    #print "Evt2_LS_String: ", Evt2_LS_String
    Evt2_LS_String_L=Evt2_LS_String.split("\n")
    #print "Evt2_LS_String_L: ", Evt2_LS_String_L
    Evt2_Fname=Evt2_LS_String_L[0]
    #print "Evt2_Fname: ", Evt2_Fname
    Evt2_Filepath=ObsID_Filepath+Evt2_Fname
    print("Evt2_Filepath: ", Evt2_Filepath)
    #Reg_Fpath=Raytrace_Region_File_Generator(ObsID)
    #ObsID_Coords_Calc(ObsID,Evt2_Filepath,Raytrace_Reg_Fpath)
    #print "Raytrace_Reg_Fpath Test: ", Raytrace_Reg_Fpath
    #Source_C_L=Coords_Calc.Coords_Calc(Evt2_Filepath,Raytrace_Reg_Fpath,header=Header_String)
    Source_C_L=Coords_Calc.Coords_Calc(Evt2_Filepath,Raytrace_Reg_Fpath)
    #print "Source_C_L:\n", Source_C_L
    Raytraced_Coord_Outpath=path_Obs+"Raytraced_Sources_ObsID_"+str(ObsID)+"_Coords.csv"
    #print "Raytraced_Coord_Outpath: ", Raytraced_Coord_Outpath
    file2=open(Raytraced_Coord_Outpath,"w")
    #[Cur_X,Cur_Y,Cur_Chip_X,Cur_Chip_Y,Cur_Chip_ID,Cur_RA,Cur_DEC,Cur_Theta]
    file2.write("Phys_X,Phys_Y,Chip_X,Chip_Y,Chip_ID,RA,DEC,Det_X,Det_Y,Offaxis_Angle"+"\n")
    Det_Coords_Reg_Outpath=path_Obs+"Raytraced_Sources_ObsID_"+str(ObsID)+"_Detector_Coords.reg"
    Det_Coords_Reg_File=open(Det_Coords_Reg_Outpath,"w")
    Det_Coords_Reg_File.write(Header_String)
    Raytrace_Reg_File=open(Raytrace_Reg_Fpath)
    Raytrace_Reg_Str=Raytrace_Reg_File.read()
    #print "Raytrace_Reg_Str:\n", Raytrace_Reg_Str
    Raytrace_Reg_Str_L=Raytrace_Reg_Str.split(Header_String)
    #print "Raytrace_Reg_Str_L: ", Raytrace_Reg_Str_L
    Raytrace_Reg_Str_Reduced=Raytrace_Reg_Str_L[1]
    #print "Raytrace_Reg_Str_Reduced:\n", Raytrace_Reg_Str_Reduced
    Raytrace_Reg_Str_Reduced_L=Raytrace_Reg_Str_Reduced.split("\n")
    #print "Raytrace_Reg_Str_Reduced_L: ", Raytrace_Reg_Str_Reduced_L
    #print "len(Raytrace_Reg_Str_Reduced_L) Before Pop: ", len(Raytrace_Reg_Str_Reduced_L)
    Raytrace_Reg_Str_Reduced_L.pop(len(Raytrace_Reg_Str_Reduced_L)-1)
    #print "Raytrace_Reg_Str_Reduced_L After Pop: ", Raytrace_Reg_Str_Reduced_L
    #print "len(Raytrace_Reg_Str_Reduced_L) After Pop: ", len(Raytrace_Reg_Str_Reduced_L)
    #print "len(Source_C_L): ", len(Source_C_L)
    #for Source_C in Source_C_L:
    for i in range(0,len(Source_C_L)):
        Source_C=Source_C_L[i]
        #print "Source_C: ", Source_C
        Cur_Reg=Raytrace_Reg_Str_Reduced_L[i]
        #print "Cur_Reg: ", Cur_Reg
        Phys_X=Source_C[0]
        Phys_Y=Source_C[1]
        Chip_X=Source_C[2]
        Chip_Y=Source_C[3]
        Chip_ID=Source_C[4]
        RA=Source_C[5]
        DEC=Source_C[6]
        Det_X=Source_C[7]
        Det_Y=Source_C[8]
        Offaxis_Angle=Source_C[9]
        file2.write(str(Phys_X)+","+str(Phys_Y)+","+str(Chip_X)+","+str(Chip_Y)+","+str(Chip_ID)+","+str(RA)+","+str(DEC)+","+str(Det_X)+","+str(Det_Y)+","+str(Offaxis_Angle)+"\n")
        #Cur_Reg_Str="detector;Ellipse("4095.41,3893.44,4.12171,3.24946,2.0637) #"
        Cur_Reg_String_L=re.split("[(),]",Cur_Reg)
        #print "Cur_Reg_String_L: ", Cur_Reg_String_L
        #Cur_Reg_Str="detector;Circle("+str(Det_X)+","+str(Det_Y)+","+str(10)+") #\n" #This needs to be updated to preserve the region shape
        Cur_Reg_Str=Cur_Reg_String_L[0]+"("+str(Det_X)+","+str(Det_Y)+","+Cur_Reg_String_L[3]+","+Cur_Reg_String_L[4]+","+Cur_Reg_String_L[5]+")"+Cur_Reg_String_L[6]+"\n"
        #print "Cur_Reg_Str: ", Cur_Reg_Str
        Det_Coords_Reg_File.write(Cur_Reg_Str)
    file2.close()
    Det_Coords_Reg_File.close()
#Raytrace_Region_File_Generator(140)
#Raytrace_Region_File_Generator(10125)

def Raytrace_All_Soucres_Region_File_Generator(ObsID_L,Generate_Bool=False):
    Header_String='# Region file format: DS9 version 3.0\nglobal color=blue font="helvetica 10 normal" select=1 edit=1 move=1 delete=1 include=1 fixed=0\n'
    Raytrace_Files_Path=Root_Path+"/xray/anthony/Research_Git/Raytrace_Region_File_Generator/Raytrace_Region_Files/"
    Sky_Coord_All_Soruces_File=open(Raytrace_Files_Path+"Sky_Coord_All_Soruces.reg","w")
    Sky_Coord_All_Soruces_File.write(Header_String)
    Detector_Coord_All_Soruces_File=open(Raytrace_Files_Path+"Detector_Coord_All_Soruces.reg","w")
    Detector_Coord_All_Soruces_File.write(Header_String)
    for ObsID in ObsID_L:
        if(Generate_Bool):
            Raytrace_Region_File_Generator(ObsID)
        Cur_Raytrace_Sky_Path=Raytrace_Files_Path+str(ObsID)+"/ObsID_"+str(ObsID)+"_Raytraced_Source_Regions.reg"
        Cur_Raytrace_Detector_Path=Raytrace_Files_Path+str(ObsID)+"/Raytraced_Sources_ObsID_"+str(ObsID)+"_Detector_Coords.reg"
        Cur_Raytrace_Sky_File=open(Cur_Raytrace_Sky_Path)
        Cur_Raytrace_Sky_Str=Cur_Raytrace_Sky_File.read()
        #print "Cur_Raytrace_Sky_Str: ", Cur_Raytrace_Sky_Str
        Cur_Raytrace_Sky_Str_L=Cur_Raytrace_Sky_Str.split("fixed=0\n")
        #print "Cur_Raytrace_Sky_Str_L: ", Cur_Raytrace_Sky_Str_L
        Cur_Raytrace_Sky_Str_Reduced=Cur_Raytrace_Sky_Str_L[1]
        #print "Cur_Raytrace_Sky_Str_Reduced:\n", Cur_Raytrace_Sky_Str_Reduced
        #print "Cur_Raytrace_Sky_Str_Reduced Sum:\n",Header_String+Cur_Raytrace_Sky_Str_Reduced+Cur_Raytrace_Sky_Str_Reduced
        Sky_Coord_All_Soruces_File.write(Cur_Raytrace_Sky_Str_Reduced)
        Cur_Raytrace_Detector_File=open(Cur_Raytrace_Detector_Path)
        Cur_Raytrace_Detector_Str=Cur_Raytrace_Detector_File.read()
        #print "Cur_Raytrace_Detector_Str: ", Cur_Raytrace_Detector_Str
        Cur_Raytrace_Detector_Str_L=Cur_Raytrace_Detector_Str.split("fixed=0\n")
        #print "Cur_Raytrace_Detector_Str_L: ", Cur_Raytrace_Detector_Str_L
        Cur_Raytrace_Detector_Str_Reduced=Cur_Raytrace_Detector_Str_L[1]
        #print "Cur_Raytrace_Detector_Str_Reduced:\n", Cur_Raytrace_Detector_Str_Reduced
        #print "Cur_Raytrace_Detector_Str_Reduced Sum:\n",Header_String+Cur_Raytrace_Detector_Str_Reduced+Cur_Raytrace_Detector_Str_Reduced
        Detector_Coord_All_Soruces_File.write(Cur_Raytrace_Detector_Str_Reduced)
    Sky_Coord_All_Soruces_File.close()
    Detector_Coord_All_Soruces_File.close()

#Raytrace_All_Soucres_Region_File_Generator([10125])
#Raytrace_All_Soucres_Region_File_Generator([10125],Generate_Bool=True)
##Raytrace_All_Soucres_Region_File_Generator([6096, 1971, 1972, 768, 952, 11674, 13255, 13253, 13246, 12952, 12953, 13247, 12951, 2025, 9548, 2149, 2197, 9510, 6131, 5908, 803, 14342, 12995, 2064, 16024, 12992, 14332, 13202, 793, 2933, 11104, 379, 2056, 2055, 2922, 9506, 11344, 766, 4688, 6869, 6872, 3554, 2057, 2058, 8041, 9121, 9546, 7252, 7060, 9553, 5930, 5931, 5929, 2079, 5905, 9527, 4689, 3947, 1563, 9507, 4613, 794, 11775, 11271, 3951, 2062, 2027, 2060, 2061, 2070, 2032, 7154, 7153, 11779, 5932, 2976, 4613, 794, 1043, 4632, 4631, 4633, 4404, 2059, 12095, 2040, 2915, 4372, 2069, 11229, 7848, 15383, 10125, 2031, 10875, 12889, 12888, 321, 322, 9551, 9550, 3954, 2020, 2068, 4742, 2039, 3150, 2030, 4743, 5197, 11784, 9552],Generate_Bool=True)
#ObsID_L=ObsID_From_CSV_Query.Read_ObsIDs(Remove_Unarchived=True)
#print(ObsID_L)
#print("len(ObsID_L): ", len(ObsID_L))
#Raytrace_All_Soucres_Region_File_Generator(ObsID_L, Generate_Bool=True)
Raytrace_All_Soucres_Region_File_Generator([8197, 8198, 14341, 6152, 2057, 2058, 2059, 14342, 12301, 14349, 14350, 2064, 2065, 14351, 20495, 18454, 18455, 6169, 6170, 2075, 2076, 18461, 18462, 6175, 10274, 10275, 10276, 10277, 10278, 10279, 6184, 6185, 10280, 10281, 14376, 14378, 14383, 14384, 10289, 10290, 10291, 10292, 10293, 14412, 4176, 14419, 2148, 14437, 16484, 16485, 20585, 14442, 24707, 14471, 2197, 2198, 12437, 16556, 12473, 22714, 22715, 16580, 2255, 2260, 6361, 8458, 8464, 8465, 12562, 20752, 20753, 2340, 8489, 8490, 10542, 10543, 10544, 10545, 20794, 316, 318, 10559, 10560, 18760, 14675, 14676, 349, 350, 353, 354, 361, 16745, 378, 379, 380, 12668, 383, 384, 388, 389, 390, 391, 392, 393, 394, 395, 400, 402, 404, 405, 407, 12696, 409, 410, 411, 24981, 413, 414, 24986, 18875, 4555, 4556, 4557, 4558, 12748, 14795, 14801, 10722, 10723, 10724, 10725, 10726, 20965, 20966, 20992, 20993, 4613, 20997, 20998, 20999, 21000, 21001, 21003, 4627, 4628, 4629, 4630, 23075, 23076, 21036, 14896, 14902, 14912, 6727, 16969, 4688, 4689, 4690, 16978, 4692, 4693, 4694, 16983, 4696, 4697, 21077, 21082, 16991, 16994, 16995, 16996, 16997, 23140, 23141, 17000, 18440, 17003, 17007, 10868, 4725, 4726, 4727, 4728, 4729, 4730, 4731, 4732, 4733, 2686, 4734, 4735, 4736, 4737, 6781, 6782, 4743, 4744, 4745, 4746, 4747, 4748, 4749, 4750, 4751, 4752, 4753, 4754, 10925, 23216, 23217, 12978, 23218, 23219, 12981, 23220, 23223, 12992, 12993, 12994, 12995, 12996, 13018, 735, 23266, 21230, 17155, 782, 784, 790, 792, 793, 794, 795, 11032, 797, 11033, 11034, 17180, 808, 15149, 2879, 2885, 11080, 11081, 11082, 11083, 11084, 11085, 11086, 15190, 864, 11104, 15200, 19297, 2916, 2917, 870, 871, 872, 2918, 2919, 19304, 21350, 2925, 21351, 21352, 882, 2933, 2934, 2949, 2950, 21384, 19339, 19344, 19345, 13202, 19346, 7060, 19348, 19350, 19351, 19354, 7069, 19357, 2976, 7073, 9122, 2978, 7074, 7075, 7076, 934, 9120, 9121, 7082, 7083, 7084, 942, 7086, 7087, 19374, 7090, 7091, 23472, 7093, 23473, 7095, 7096, 13241, 7098, 19386, 19387, 7101, 15294, 7103, 7104, 7105, 962, 963, 3012, 7106, 13248, 7111, 15295, 969, 7113, 7115, 7116, 19397, 7118, 19403, 7120, 7121, 19407, 7123, 7124, 19411, 19414, 7127, 19416, 19417, 7132, 19421, 7134, 19422, 21471, 21472, 21473, 21474, 19428, 15333, 21479, 7146, 7147, 19437, 7150, 7152, 7153, 7154, 13303, 13304, 11260, 11268, 23559, 11272, 11273, 23561, 23564, 15382, 15384, 11289, 15386, 15387, 11295, 19497, 21545, 11309, 11311, 11317, 17461, 17462, 9278, 17471, 17472, 19521, 19522, 19524, 5197, 7252, 25689, 13439, 21639, 15496, 21640, 17547, 19363, 21647, 21648, 21649, 17569, 17570, 5283, 17571, 17578, 5296, 5297, 5300, 5301, 5302, 5309, 15553, 21698, 21699, 7369, 5322, 5323, 15572, 15574, 5337, 5338, 5339, 5340, 15579, 15582, 15587, 15588, 15589, 15594, 15603, 3325, 15616, 17678, 1302, 15646, 19392, 19747, 19393, 19748, 19394, 9532, 9533, 9534, 9535, 9536, 9537, 9538, 9539, 9540, 9541, 9542, 9543, 9545, 9546, 9547, 9548, 9549, 9550, 9551, 9552, 9553, 23474, 21853, 23475, 9570, 23476, 23477, 23478, 23479, 13686, 23480, 23481, 23482, 23483, 23484, 15756, 23485, 15760, 23486, 23487, 15771, 23488, 13728, 23489, 23490, 23491, 23492, 23493, 10875, 15803, 23494, 23495, 13765, 23496, 23497, 3550, 3551, 13791, 17890, 17891, 13796, 11761, 5619, 13812, 13813, 13814, 13815, 13816, 13817, 13819, 13820, 13821, 13822, 13829, 11782, 13830, 13831, 13832, 11786, 5644, 19981, 19982, 11800, 1564, 1578, 1579, 1586, 1587, 11846, 11847, 9805, 1618, 1621, 1622, 1624, 1633, 1634, 1635, 1636, 1637, 1638, 1640, 7797, 7798, 7799, 7800, 14984, 18047, 16000, 16001, 14985, 16002, 16003, 16005, 18048, 18053, 18054, 18062, 18063, 18064, 18065, 18066, 18067, 18068, 9877, 18069, 16023, 16024, 18070, 18071, 9883, 16028, 16029, 18072, 18073, 16032, 16033, 7850, 22189, 7858, 22194, 7863, 17032, 14017, 14018, 16068, 16069, 3786, 3787, 3788, 7885, 16121, 16122, 5905, 5911, 5929, 5930, 5931, 10025, 10026, 10027, 5935, 5936, 5937, 5938, 5939, 5940, 5941, 5942, 5943, 5944, 5945, 5946, 5947, 5948, 5949, 12095, 3925, 3930, 3931, 3932, 3933, 3934, 3935, 3936, 3937, 3938, 3939, 3940, 3941, 3942, 3943, 22372, 22375, 16234, 3949, 3950, 20333, 3953, 3954, 8050, 8052, 8053, 20343, 8058, 12155, 12156, 3965, 20353, 16260, 16261, 16262, 20356, 10125, 16276, 16277, 8086, 14230, 14231, 8091, 8098, 18340, 18341, 18342, 18343, 4010, 4016, 4017, 18352, 4019, 8125, 8126, 12238, 12239, 6096, 6097, 22478, 22479, 22480, 22481, 22482, 2014, 6114, 6115, 6118, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2039, 2040, 14332, 8190], Generate_Bool=True)
