#! /bin/bash

marx @@$3 SourceFlux=3. SpectrumType="FILE" SpectrumFile=../Required_Files/bkgspec.tbl \
       ExposureTime=0 NumRays=-$1 OutputDir=$2 \
       DetectorType="ACIS-I" DitherModel="INTERNAL" RA_Nom=0 Dec_Nom=0 \
       Roll_Nom=0 SourceRA=359.927781967 SourceDEC=0.066895244 \
       SourceType="IMAGE" S-ImageFile=../Required_Files/chip-shape_Centered_Full.fits GratingType=NONE RandomSeed=$4
marx2fits $2 $2.fits
