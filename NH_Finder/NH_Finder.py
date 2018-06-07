from astroquery.ned import Ned
import subprocess as sp
def NH_Finder(gname):
    G_Data = Ned.query_object(gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The queryed data of the galaxy from NED in the form of a astropy table
    #print G_Data
    #print type(G_Data)
    raGC=float(G_Data['RA(deg)']) #raGC:-float, Right Ascension of Galatic Center, The right ascension of the galatic center of the current galaxy in degrees.
    decGC=float(G_Data['DEC(deg)']) #decGC:-float, Declination of Galatic Center, The declination of the galatic center of the current galaxy in degrees.
    pointingRA=raGC
    pointingDec=decGC
    #THIS IS WERE SIMON'S CODE BEGINS
    nH_for_obs = sp.check_output("nh equinox=2000 ra=" + str(pointingRA) + " dec=" + str(pointingDec) + " | tail -1 | cut -d ' ' -f 10", shell=True) # This is the NH tool that HEA runs
    print nH_for_obs    # This is for the whole observation - should work for every source since it barely changes, ANTHONY: in units of hydrogen atoms cm**-2
    nH_corrected = float(nH_for_obs)/1e22 #ANTHONY(ME): I MAY HAVE TO CHANGE THE UNITS TO SOMTHING I USE INSTEAD OF WHAT THE SHERPA TOOL (Simon used this) USES
    print nH_corrected  # Fixed, since sherpa takes un units of 1e22 atoms/cm^2
    #THIS IS WHERE SIMON'S CODE ENDS

NH_Finder('NGC 3077')
#NH_Finder('NGC 253')
