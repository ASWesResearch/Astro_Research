def Obs_ID_Downloader(Obs_ID_L):
    """
    Obs_ID_L:- List   This is a list of strings, each string being a Obs ID that will be downloaded

    This Function takes a list of Obs ID strings, downloads the Obs ID's and reprocesses them.
    """
    from ciao_contrib.runtool import * #Imports ciao tools into ipython
    for Obs_ID in Obs_ID_L:
        Obs_ID_N=int(Obs_ID)
        download_chandra_obsid(obsid=Obs_ID_N) #This might not be the right symtax
        chandra_repro(indir= "/home/asantini/Desktop/Galaxy_Test/" + str(Obs_Id_N), outdir="/home/asantini/Desktop/Galaxy_Test/" + str(Obs_Id_N) + "/new", cleanup=no)
    print "Done"
