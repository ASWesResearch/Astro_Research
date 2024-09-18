#! /bin/bash

marx @@/opt/anaconda3/envs/ciao-4.14/share/marx/pfiles/marx.par RA_Nom=0 Dec_Nom=0 Roll_Nom=0 SourceRA=0 SourceDEC=0 OutputDir=test
marx2fits test test.fits
marxasp MarxDir="test" OutputFile="test_asol1.fits"
