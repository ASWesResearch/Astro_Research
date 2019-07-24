import os
from os import system
import sys
import numpy
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))
#from Coords_Calc import Coords_Calc
from Galaxy_Name_Reducer import Galaxy_Name_Reducer
from File_Query_Code import File_Query_Code_5
def Galaxy_List_to_ObsID_List_Converter(Gname_L,Bulk_Bool=False):
    ObsID_Bulk_List=[]
    Galaxy_Info_H_L=[]
    for Gname in Gname_L:
        Cur_ObsID_L=[]
        Gname_Modifed=Galaxy_Name_Reducer.Galaxy_Name_Reducer(Gname)
        Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
        for Evt2_File_L in Evt2_File_H_L:
            Cur_ObsID=Evt2_File_L[0]
            Cur_ObsID_L.append(Cur_ObsID)
            ObsID_Bulk_List.append(Cur_ObsID)
        Galaxy_Info_L=[Gname_Modifed,Cur_ObsID_L]
        Galaxy_Info_H_L.append(Galaxy_Info_L)
    if(Bulk_Bool):
        return ObsID_Bulk_List
    else:
        return Galaxy_Info_H_L

#Updated List Without the Erroneously Included NGC 0055 (This is the best and most current version of the sample):
#print Galaxy_List_to_ObsID_List_Converter(['NGC 2841', 'NGC 3877', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'NGC 0278', 'MESSIER 088', 'NGC 3585', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4570', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'IC 1613', 'NGC 4477', 'NGC 2787', 'IC 5267', 'NGC 3923', 'NGC 891', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'NGC 4314', 'NGC 4559', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4742', 'NGC 1672', 'NGC 4725', 'NGC 0891', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 2865', 'MESSIER 059', 'NGC 1427', 'NGC 3628', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521'])

#Output:
#[['NGC_2841', [6096]], ['NGC_3877', [1971, 1972, 768, 952]], ['NGC_5054', [11674]], ['NGC_5813', [13255, 13253, 13246, 12952, 12953, 13247, 12951]], ['MESSIER_108', [2025]], ['MESSIER_066', [9548]], ['MESSIER_061', [2149]], ['MESSIER_063', [2197]], ['MESSIER_086', [9510]], ['MESSIER_084', [6131, 5908, 803]], ['MESSIER_083', [14342, 12995, 2064, 16024, 12992, 14332, 13202, 793]], ['MESSIER_082', [2933, 11104, 379]], ['NGC_278', [2056, 2055]], ['MESSIER_088', [2922]], ['NGC_3585', [9506]], ['NGC_7507', [11344]], ['NGC_1637', [766]], ['NGC_4473', [4688]], ['NGC_1365', [6869, 6872, 3554]], ['MESSIER_074', [2057, 2058]], ['NGC_4570', [8041]], ['NGC_4321', [9121]], ['NGC_5474', [9546]], ['NGC_7090', [7252, 7060]], ['MESSIER_094', [9553]], ['MESSIER_095', [5930, 5931, 5929]], ['NGC_4494', [2079]], ['IC_1613', [5905]], ['NGC_4477', [9527]], ['NGC_2787', [4689]], ['IC_5267', [3947]], ['NGC_3923', [1563, 9507]], ['NGC_891', [4613, 794]], ['NGC_1300', [11775]], ['UGC_05340', [11271]], ['NGC_3631', [3951]], ['NGC_4314', [2062]], ['NGC_4559', [2027]], ['NGC_2681', [2060, 2061]], ['NGC_5018', [2070]], ['NGC_5253', [2032, 7154, 7153]], ['NGC_4742', [11779]], ['NGC_1672', [5932]], ['NGC_4725', [2976]], ['NGC_891', [4613, 794]], ['NGC_6946', [1043, 4632, 4631, 4633, 4404]], ['NGC_1291:[LFF2012]_084', [2059]], ['NGC_3115', [12095, 2040]], ['NGC_1332', [2915, 4372]], ['NGC_1700', [2069]], ['NGC_5584', [11229]], ['NGC_7552', [7848]], ['NGC_2997', [15383]], ['NGC_4449', [10125, 2031, 10875]], ['MESSIER_049', [12889, 12888, 321, 322]], ['NGC_3198', [9551]], ['NGC_855', [9550]], ['NGC_7793', [3954]], ['NGC_2865', [2020]], ['MESSIER_059', [2068]], ['NGC_1427', [4742]], ['NGC_3628', [2039]], ['NGC_4457', [3150]], ['NGC_4214', [2030, 4743, 5197]], ['NGC_4459', [11784]], ['NGC_3521', [9552]]]

#Updated List Without the Erroneously Included NGC 0055 (This is the best and most current version of the sample):
#print Galaxy_List_to_ObsID_List_Converter(['NGC 2841', 'NGC 3877', 'NGC 5054', 'NGC 5813', 'MESSIER 108', 'MESSIER 066', 'MESSIER 061', 'MESSIER 063', 'MESSIER 086', 'MESSIER 084', 'MESSIER 083', 'MESSIER 082', 'NGC 0278', 'MESSIER 088', 'NGC 3585', 'NGC 7507', 'NGC 1637', 'NGC 4473', 'NGC 1365', 'MESSIER 074', 'NGC 4570', 'NGC 4321', 'NGC 5474', 'NGC 7090', 'MESSIER 094', 'MESSIER 095', 'NGC 4494', 'IC 1613', 'NGC 4477', 'NGC 2787', 'IC 5267', 'NGC 3923', 'NGC 891', 'NGC 1300', 'UGC 05340', 'NGC 3631', 'NGC 4314', 'NGC 4559', 'NGC 2681', 'NGC 5018', 'NGC 5253', 'NGC 4742', 'NGC 1672', 'NGC 4725', 'NGC 0891', 'NGC 6946', 'NGC 1291:[LFF2012] 084', 'NGC 3115', 'NGC 1332', 'NGC 1700', 'NGC 5584', 'NGC 7552', 'NGC 2997', 'NGC 4449', 'MESSIER 049', 'NGC 3198', 'NGC 0855', 'NGC 7793', 'NGC 2865', 'MESSIER 059', 'NGC 1427', 'NGC 3628', 'NGC 4457', 'NGC 4214', 'NGC 4459', 'NGC 3521'], Bulk_Bool=True)

#Output: #(112 ObsIDs in the sample)
#[6096, 1971, 1972, 768, 952, 11674, 13255, 13253, 13246, 12952, 12953, 13247, 12951, 2025, 9548, 2149, 2197, 9510, 6131, 5908, 803, 14342, 12995, 2064, 16024, 12992, 14332, 13202, 793, 2933, 11104, 379, 2056, 2055, 2922, 9506, 11344, 766, 4688, 6869, 6872, 3554, 2057, 2058, 8041, 9121, 9546, 7252, 7060, 9553, 5930, 5931, 5929, 2079, 5905, 9527, 4689, 3947, 1563, 9507, 4613, 794, 11775, 11271, 3951, 2062, 2027, 2060, 2061, 2070, 2032, 7154, 7153, 11779, 5932, 2976, 4613, 794, 1043, 4632, 4631, 4633, 4404, 2059, 12095, 2040, 2915, 4372, 2069, 11229, 7848, 15383, 10125, 2031, 10875, 12889, 12888, 321, 322, 9551, 9550, 3954, 2020, 2068, 4742, 2039, 3150, 2030, 4743, 5197, 11784, 9552]
