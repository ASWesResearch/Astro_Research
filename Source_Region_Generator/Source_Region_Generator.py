from astropy.io import ascii
from ciao_contrib.runtool import *
from region import *
def Source_Reg_Gen(fname,evtfname,n):
    data = ascii.read(str(fname))
    Maj_L=data['mjr_axis_raw_b']
    Min_L=data['mnr_axis_raw_b']
    Angle_L=data['pos_angle_raw_b']
    RA_L=data['ra']
    DEC_L=data['dec']
    file=open(fname+'_Source_List.txt','w')
    for i in range(0,n):
        Cur_Maj=Maj_L[i]
        Cur_Min=Min_L[i]
        Cur_Angle=Angle_L[i]
        Cur_RA=RA_L[i]
        Cur_DEC=DEC_L[i]
        Cur_Maj_Phy=Cur_Maj*2.03252032520325
        Cur_Min_Phy=Cur_Min*2.03252032520325
        dmcoords(infile=str(evtfname),ra=str(Cur_RA), dec=str(Cur_DEC), option='cel', verbose=0, celfmt='deg')
        Cur_X=dmcoords.x
        Cur_Y=dmcoords.y
        Cur_Shape='ellipse('+str(Cur_X)+','+str(Cur_Y)+','+str(Cur_Maj_Phy)+','+str(Cur_Min_Phy)+','+str(Cur_Angle)+')'+'\n' #ellipse(xc,yc,r_major_in,r_minor_in,angle)
        file.write(Cur_Shape)

Source_Reg_Gen('ngc4651_ObsID-2096.tsv','acisf02096_repro_evt2.fits',20)
