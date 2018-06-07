from ciao_contrib.runtool import *
from region import *
def Reg_Area_Test(Shape):
    B=1
    shape1=Shape
    print "shape1 : ",shape1
    r1 = regParse(shape1) #r1:-Region, Region 1, the region of the current area circle
    a1_cur = regArea(r1,0,0,8192,8192,B) #original
    #a1_cur = regArea(r1,0,0,10000,10000,B) #Test
    print "a1_cur : ",a1_cur
    print "float(a1_cur) : ",float(a1_cur)
#S=circle(' + str(X_Phys) +','+ str(Y_Phys)+','+ str(cur_r)+')'
#S_F="circle(8686.44253733,901.759332867,121.9512195)"
S_S="circle(4087.50466113,4062.96745774,121.9512195)"
S_T="circle(8192,4062.96745774,121.9512195)"
S_T2="circle(8192,8192,121.9512195)"
#Reg_Area_Test(S_F)
Reg_Area_Test(S_S)
Reg_Area_Test(S_T)
Reg_Area_Test(S_T2)
