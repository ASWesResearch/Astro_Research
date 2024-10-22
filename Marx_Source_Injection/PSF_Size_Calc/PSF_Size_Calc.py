import numpy as np
import psf
import caldb4

"""
cdb = caldb4.Caldb(telescope="CHANDRA", product="REEF")
reef = cdb.search[0]
reef = reef.split('[')[0]
pdata = psf.psfInit(reef)
"""

def Calc_PSF_Pixel_Size(phi, theta, energy=2.3, ecf=0.90):
    cdb = caldb4.Caldb(telescope="CHANDRA", product="REEF")
    reef = cdb.search[0]
    reef = reef.split('[')[0]
    pdata = psf.psfInit(reef)
    PSF = psf.psfSize(pdata, energy, theta, phi, ecf)
    psf.psfClose(pdata)
    PSF_Pix=PSF*2.032520325203252
    return PSF_Pix

def Circle_Check(Phi_Step=15, energy=10, theta=10, ecf=0.90):
    Phi_A=np.arange(360,step=Phi_Step)
    #print("Phi_A: ", Phi_A)
    Phi_L=list(Phi_A)
    for Phi in Phi_L:
        Cur_PSF_Pixel_Size=Calc_PSF_Pixel_Size(Phi, energy=energy, theta=theta, ecf=ecf)
        Cur_PSF_Pixel_Size_Rounded=np.round(Cur_PSF_Pixel_Size)
        print(str(Phi)+": "+str(Cur_PSF_Pixel_Size_Rounded))
        if(Phi<=180.0):
            Cur_PSF_Pixel_Size_Phased=Calc_PSF_Pixel_Size(Phi+180.0, energy=energy, theta=theta, ecf=ecf)
            Cur_PSF_Pixel_Size_Diff=Cur_PSF_Pixel_Size_Phased-Cur_PSF_Pixel_Size
            Cur_PSF_Pixel_Size_Diff_Rounded=np.round(Cur_PSF_Pixel_Size_Diff)
            #print(str(Phi)+"="+str(Phi+180.0)+": "+str(Cur_PSF_Pixel_Size_Diff_Rounded))
#print(Calc_PSF_Pixel_Size(pdata, 10, 10, 0, 0.9))
#print(Calc_PSF_Pixel_Size(0))
#Circle_Check()
#Circle_Check(theta=10)
#Circle_Check(theta=10, energy=8.0)
##print(Calc_PSF_Pixel_Size(phi=0, theta=8, energy=2.3))
#Circle_Check(theta=10, energy=2.3)
#Circle_Check(theta=10, energy=10)
#psf.psfClose(pdata)
