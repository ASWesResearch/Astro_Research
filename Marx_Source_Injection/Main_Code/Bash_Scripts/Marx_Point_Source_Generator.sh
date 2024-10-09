#! /bin/bash

marx @@$6 RA_Nom=0 Dec_Nom=0 Roll_Nom=$3 SourceRA=$1 SourceDEC=$2 OutputDir=$5 ExposureTime=0 NumRays=-$4 MinEnergy=0.2 MaxEnergy=10.0 GratingType=NONE DetectorType=ACIS-I RandomSeed=$8
marx2fits $5 $5.fits
marxasp @@$7 MarxDir=$5 OutputFile="$5_asol1.fits"
