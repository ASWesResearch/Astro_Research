#! /bin/bash

export PFILES="$1"
cp -r ../Parameter_Files/cxcds_param4 $1
asphist infile=$4 outfile=$1_blank_sky.asphist evtfile="$6[ccd_id=$7]" clobber=yes verbose=0
mkinstmap outfile="$1_instmap.fits" monoenergy=2.3 spectrumfile=NONE grating=NONE maskfile=NONE pixelgrid="$2" obsfile="$3" dafile=CALDB detsubsys="ACIS-3;uniform;bpmask=0" mirror=HRMA mode=h clobber=yes verbose=0
mkexpmap asphistfile=$1_blank_sky.asphist outfile=$1_expmap.fits instmapfile=$1_instmap.fits xygrid="$5" useavgaspect=no normalize=no mode=h clobber=yes verbose=0
