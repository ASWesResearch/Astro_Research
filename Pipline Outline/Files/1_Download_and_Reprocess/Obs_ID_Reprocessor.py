def Obs_ID_Reprocessor(Obs_ID_L):
    """
    Obs_ID_L:- List   This is a list of strings or integers, each element of the list being a Obs ID that will be downloaded

    This Function takes a list of Obs ID strings and reprocesses the Obs IDs each one represents.
    """
    #from ciao_contrib.runtool import * #Imports ciao tools into ipython
    for Obs_ID in Obs_ID_L:
        Obs_ID_N=int(Obs_ID)
        #download_chandra_obsid(obsids=Obs_ID_N) #This might not be the right symtax, Note: it's not working # Cutting to modify code to just reprocess data
        chandra_repro(indir= "/home/asantini/Desktop/Galaxy_Test/" + str(Obs_ID_N), outdir="/home/asantini/Desktop/Galaxy_Test/" + str(Obs_ID_N) + "/new", cleanup= 'no')
    print "Done"

IDs=[2076,2022,2198,9518,797]
Obs_ID_Reprocessor(IDs)

# download_chandra_obsid 7144,2076,2022,2198,9518,797
