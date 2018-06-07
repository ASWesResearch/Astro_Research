def Obs_ID_Downloader(Obs_ID_L):
    """
    Obs_ID_L:- List   This is a list of strings or integers, each string being a Obs ID that will be downloaded

    This Function takes a list of Obs ID strings, downloads the Obs ID's and reprocesses them.
    """
    #from ciao_contrib.runtool import * #Imports ciao tools into ipython
    for Obs_ID in Obs_ID_L:
        Obs_ID_N=int(Obs_ID)
        download_chandra_obsid(obsids=Obs_ID_N) #This might not be the right symtax, Note: it's not working
        chandra_repro(indir= "/home/asantini/Desktop/Galaxy_Test/" + str(Obs_ID_N), outdir="/home/asantini/Desktop/Galaxy_Test/" + str(Obs_ID_N) + "/new", cleanup= 'no')
    print "Done"

IDs=[7144,2076,2022,2198,9518,797]
Obs_ID_Downloader([7144])

# download_chandra_obsid 7144, 2076, 2022, 2198, 9518, 797
