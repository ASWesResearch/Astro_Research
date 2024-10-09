#! /bin/bash

marx @@../Parameter_Files/pfiles/marx.par RA_Nom=0 Dec_Nom=0 Roll_Nom=$1 SourceRA=0 SourceDEC=0 OutputDir=./Empty_Coords/empty ExposureTime=0 NumRays=-1 DetectorType=ACIS-I
marx2fits ./Empty_Coords/empty ./Empty_Coords/empty.fits
marxasp @@../Parameter_Files/pfiles/marxasp.par MarxDir="./Empty_Coords/empty" OutputFile="./Empty_Coords/empty_asol1.fits"
