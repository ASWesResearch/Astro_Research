import os
#from ciao_contrib.runtool import *
import numpy as np
import glob
#from sherpa.astro import ui as sherpa
from sherpa.astro.ui import *
from pychips.hlui import *
from pycrates import *
import subprocess as sp
from astropy.io import fits
from time import sleep
import csv
from done_email import when_done

# ciao and hea must both be running in order for this to work

#TEST TRY STATEMENT WITH OBSID 1575

def clean_results(obsid):
    for i in range(0,len(obsid)):
        obsid[i] = int(obsid[i])
    return obsid


def specFit(obsid, goodSources, failedCovar):#, counts_obsids, counts_source, countsSoft, countsMed, countsHard):

    obsid = str(int(obsid))
    goodSources = str(int(goodSources))
    obsid = str(obsid)
    
    print "Beginning spectral fitting for obsid " + obsid

    print "Getting name of evt2 file..."
    try:
        name1 = glob.glob("/Volumes/xray/simon/chandra_from_csc/" + obsid + "/primary/*_evt2.fits")
        name1 = name1[0][-24:]
    except IndexError:
        print "no csc for observation: " + obsid
    else:
        name = glob.glob("/Volumes/xray/simon/chandra_from_csc/" + obsid + "/primary/*_evt2.fits")
        csc = 'yes'
    try:
        name2 = glob.glob("/Volumes/xray/simon/chandra_not_csc/" + obsid + "/primary/*_evt2.fits")
        name2 = name2[0][-24:]
    except IndexError:
        print "already found in csc: " + obsid
    else:
        name = glob.glob("/Volumes/xray/simon/chandra_not_csc/" + obsid + "/primary/*_evt2.fits")
        csc ='no'
        good = 'no'
    try:
        name3 = glob.glob("/Volumes/xray/simon/chandra_not_csc_GOOD/" + obsid + "/primary/*_evt2.fits")
        name3 = name3[0][-24:]
    except:
        print "this is not a GOOD non-csc file"
    else:
        name = glob.glob("/Volumes/xray/simon/chandra_not_csc_GOOD/" + obsid + "/primary/*_evt2.fits")
        csc = 'no'
        good = 'yes'
    print name
    print "Shortening name..."
    name = name[0][-24:]
    print name
    print "Getting system path..."
    path = '/Volumes/xray/spirals/trace/' + obsid + '/'
    print "Getting number of files in the current obsid's directory..."
    num_files = len([f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))])
    print str(num_files) + " files found..."
    num = int((num_files-4)/5)
    print str(num) + " source(s) to be fit..."

    # Getting pointing RA and Dec in order to get nH for the observation
    if csc == 'yes':
        directory = "/Volumes/xray/simon/chandra_from_csc/" + obsid + "/primary/" + name
    if csc == 'no':
            if good == 'no':
                directory = "/Volumes/xray/simon/chandra_not_csc/" + obsid + "/primary/" + name
            if good == 'yes':
                directory = "/Volumes/xray/simon/chandra_not_csc_GOOD/" + obsid + "/primary/" + name
    pointingRA = sp.check_output("dmkeypar " + directory + " RA_PNT echo+", shell=True)
    pointingDec = sp.check_output("dmkeypar " + directory + " DEC_PNT echo+", shell=True)
    pointingRA = float(pointingRA)
    pointingDec = float(pointingDec)

    nH_for_obs = sp.check_output("nh equinox=2000 ra=" + str(pointingRA) + " dec=" + str(pointingDec) + " | tail -1 | cut -d ' ' -f 10", shell=True)
    print nH_for_obs    # This is for the whole observation - should work for every source since it barely changes
    nH_corrected = float(nH_for_obs)/1e22
    print nH_corrected  # Fixed, since sherpa takes un units of 1e22 atoms/cm^2
        
    print "\nLoading data for source", goodSources
    #sherpa.load_data("'/Volumes/xray/simon/chandra_from_csc/" + obsid + "/primary/extracted/extracted_" + obsid + "_" + str(i) + ".pi'")

    load_data("/Volumes/xray/hannah/chandra_all_sources/" + obsid + "/primary/extracted/extracted_" + obsid + "_" + goodSources + ".pi")

    #index = np.where(counts_obsid == int(obsid) and counts_source == i)

    print "Subtracting background, filtering by energy level, and grouping counts..."
    try:
        subtract()
    except:
        print "No background file found"
#        headUpdateFile = fits.open('/Volumes/xray/simon/chandra_from_csc/' + obsid + '/primary/extracted/extracted_' + obsid + '_' + str(i) + '.pi', 'update')
#        headUpdateFile[1].header['BACKFILE'] = 'extracted_' + obsid + '_' + str(i) + '_bkg.pi'
#        headUpdateFile.close()
#        sleep(2)
#        print "Updated header, backfile is now:"
#        print sp.check_output('dmlist /Volumes/xray/simon/chandra_from_csc/' + obsid + '/primary/extracted/extracted_' + obsid + '_' + str(i) + '.pi header | grep BACKFILE', shell=True)
        #subtract()

    notice(0.3, 7.5)
    group_counts(15)
    print "Setting chi2gehrels model..."
    #set_stat("chi2datavar")
    set_stat("chi2gehrels")

###################### Fit power law model #########################

    print "Setting power law model..."
    #set_source("powlaw1d.pl")#xstbabs.abs1 * powlaw1d.pl)
    set_source("xstbabs.abs1 * powlaw1d.pl")


    abs1.nH.min = float(nH_corrected)
    print "Fitting power law model..."
    fit()

    print "Saving model..."
    save_model("/Volumes/xray/hannah/spectralfits/pow_fit_" + obsid + "_" + goodSources + "_model_info.fits", clobber=True)

#plot_fit_delchi() #will commenting this out keep it from displaying the plot without losing any info? May want to do that, since CHIPS likes to crash sometimes.

    fitResults = get_fit_results()
    #print str(results)
    fitResultsFile = open("/Volumes/xray/hannah/spectralfits/pow_fit_" + obsid + "_" + goodSources + "_fit_results.txt", 'w')
    fitResultsFile.write(str(fitResults))
    fitResultsFile.close()
    #print get_fit_plot()
    #print "\n"

    try:
        print "Getting covariance pow..."
        covar()
        print "Saving covariance pow..."
        covarResults = get_covar_results()
        covarResultsFile = open("/Volumes/xray/hannah/spectralfits/pow_fit_" + obsid + "_" + goodSources + "_covar_results.txt", 'w')
        covarResultsFile.write(str(covarResults) + "\n")
        covarResultsFile.close()
    except:             # Bad practice. Should figure out how to handle the error properly. - sherpa.utils.err.EstError
        print "Pow covariance failed. Degrees of freedom may be zero or lower."
        failedCovar.write(obsid + "," + goodSources)
    print "Getting pow energy flux..."
    energyFlux = calc_energy_flux()
    energyFluxResultsFile = open("/Volumes/xray/hannah/spectralfits/pow_fit_" + obsid + "_" + goodSources + "_energy_flux.txt", 'w')
    energyFluxResultsFile.write(str(energyFlux))
    energyFluxResultsFile.close()

###################### Fit mekal model #########################

    print "Setting mekal model..."
    
    set_source("xstbabs.abs2 * xsmekal.mek1")
    
    
    abs2.nH.min = float(nH_corrected)
    print "Fitting mekal model..."
    fit()
    
    print "Saving model..."
    save_model("/Volumes/xray/hannah/spectralfits/mekal_fit_" + obsid + "_" + goodSources + "_model_info.fits", clobber=True)
    
    # plot_fit_delchi() #will commenting this out keep it from displaying the plot without losing any info? May want to do that, since CHIPS likes to crash sometimes.
    
    fitResults = get_fit_results()
    #print str(results)
    fitResultsFile = open("/Volumes/xray/hannah/spectralfits/mekal_fit_" + obsid + "_" + goodSources + "_fit_results.txt", 'w')
    fitResultsFile.write(str(fitResults))
    fitResultsFile.close()
    #print get_fit_plot()
    #print "\n"
    
    try:
        print "Getting covariance mekal..."
        covar()
        print "Saving covariance mekal..."
        covarResults = get_covar_results()
        covarResultsFile = open("/Volumes/xray/hannah/spectralfits/mekal_fit_" + obsid + "_" + goodSources + "_covar_results.txt", 'w')
        covarResultsFile.write(str(covarResults) + "\n")
        covarResultsFile.close()
    except:             # Bad practice. Should figure out how to handle the error properly. - sherpa.utils.err.EstError
        print "Pow covariance failed. Degrees of freedom may be zero or lower."
        failedCovar.write(obsid + "," + goodSources)
    print "Getting mekal energy flux..."
    energyFlux = calc_energy_flux()
    energyFluxResultsFile = open("/Volumes/xray/hannah/spectralfits/mekal_fit_" + obsid + "_" + goodSources + "_energy_flux.txt", 'w')
    energyFluxResultsFile.write(str(energyFlux))
    energyFluxResultsFile.close()

###################### Fitdiskbb model #########################

    print "Setting diskbb model..."
    
    set_source("xstbabs.abs3 * xsdiskbb.disk1")
    
    
    abs3.nH.min = float(nH_corrected)
    print "Fitting diskbb model..."
    fit()
    
    print "Saving model..."
    save_model("/Volumes/xray/hannah/spectralfits/diskbb_fit_" + obsid + "_" + goodSources + "_model_info.fits", clobber=True)
    
    # plot_fit_delchi() #will commenting this out keep it from displaying the plot without losing any info? May want to do that, since CHIPS likes to crash sometimes.
    
    fitResults = get_fit_results()
    #print str(results)
    fitResultsFile = open("/Volumes/xray/hannah/spectralfits/diskbb_fit_" + obsid + "_" + goodSources + "_fit_results.txt", 'w')
    fitResultsFile.write(str(fitResults))
    fitResultsFile.close()
    #print get_fit_plot()
    #print "\n"
    
    try:
        print "Getting covariance diskbb..."
        covar()
        print "Saving covariance diskbb..."
        covarResults = get_covar_results()
        covarResultsFile = open("/Volumes/xray/hannah/spectralfits/diskbb_fit_" + obsid + "_" + goodSources + "_covar_results.txt", 'w')
        covarResultsFile.write(str(covarResults) + "\n")
        covarResultsFile.close()
    except:             # Bad practice. Should figure out how to handle the error properly. - sherpa.utils.err.EstError
        print "diskbb covariance failed. Degrees of freedom may be zero or lower."
        failedCovar.write(obsid + "," + goodSources)
    print "Getting diskbb energy flux..."
    energyFlux = calc_energy_flux()
    energyFluxResultsFile = open("/Volumes/xray/hannah/spectralfits/diskbb_fit_" + obsid + "_" + goodSources + "_energy_flux.txt", 'w')
    energyFluxResultsFile.write(str(energyFlux))
    energyFluxResultsFile.close()

        #log_scale()
        #print_window("/Volumes/xray/simon/spectralfits/pow_fit_" + obsid + "_" + str(i) + "_fit.pdf")

# def get_counts_info():
    # data = pd.read_csv('counts_info.csv', header=0)
#
    # counts_obsids = data['OBSID']
    # counts_source = data['SOURCE']
#
    # foo = data['RAW_COUNTS[.3-1]']
    # bar = data['BKG_COUNTS[.3-1]']
    # countsSoft = foo - bar
#
    # foo = data['RAW_COUNTS[1-2.1]']
    # bar = data['BKG_COUNTS[1-2.1]']
    # countsMed = foo - bar
#
    # foo = data['RAW_COUNTS[2.1-7.5]']
    # bar = data['BKG_COUNTS[2.1-7.5]']
    # countsHard = foo - bar
#
    # return counts_obsids, counts_source, countsSoft, countsMed, countsHard

if __name__ == '__main__':

    print "Reading in obsids... "
#    
#    to_fit = csv.reader(open('to_extract.csv', 'r'), delimiter = ';')
#    obsid = list(zip(*to_fit))[0]
#

#    with open("to_extract.csv") as tsv:
#        to_fit = zip(*(line.strip().split(';') for line in tsv))
#    
#    obsid = np.array(to_fit[0])
#    print obsid
#    print("reading in source numbers")
#    
#    goodSource = np.array(to_fit[1])


#    to_fit = csv.reader(open('to_extract.csv', 'r'), delimiter = ';')
#    
#    goodSource = list(zip(*to_fit))[1]
#

    import pandas as pd

    df = pd.read_csv('300_source_list.csv', header=None)
    obsid = np.array(df[0])
    print obsid
    
    obsid = clean_results(obsid)

    goodSource = np.array(df[1])
    print goodSource

    print "All obsid names processed."

    failedCovar = open("failed_covar.txt", 'w')
    NoExtract = open("NoExtract.txt", 'w')

    for i in range(852,857):
        print "\nStarting obsid " + str(i) + " of " + str(len(obsid)) + "...\n"
        try:
            #print "Attempting spec..."
            specFit(obsid[i], goodSource[i], failedCovar)#, counts_obsids, counts_source, countsSoft, countsMed, countsHard)
            print "done with obsid " + str(obsid[i])
        except OSError:
            print "No extracted sources in obsid " + str(obsid[i])
            print "Spectral fitting failed for obsid " + str(obsid[i])
            

    failedCovar.close()

    when_done("specfit")
