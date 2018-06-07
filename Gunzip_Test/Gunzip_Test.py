import gzip
def Unzip(fname,outfname):
    inF = gzip.open(fname, 'rb')
    outF = open(outfname, 'wb')
    outF.write( inF.read() )
    inF.close()
    outF.close()
#Unzip("acisf01618_000N003_fov1.fits.gz","acisf01618_000N003_fov1.fits")
Unzip("/home/asantini/Desktop/Gunzip_Test/acisf01618_000N003_fov1.fits.gz","/home/asantini/Desktop/Gunzip_Test/acisf01618_000N003_fov1.fits")
