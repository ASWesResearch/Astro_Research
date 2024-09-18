#! /bin/bash

dmextract infile="acis5sbkg.fits[sky=rotbox(0:00:58,+0:00:10,8.0',8.0',0)][bin pi]" outfile='blank_sky.pi' wmap="[bin tdet=8]" clobber=yes
#asphist infile=diffuse_asol1.fits outfile=blank_sky.asphist evtfile="diffuse_evt2.fits[ccd_id=7]" clobber=yes
asphist infile=$1 outfile=blank_sky.asphist evtfile="$2[ccd_id=$3]" clobber=yes
sky2tdet infile="acis5sbkg.fits[sky=rotbox(0:00:58,+0:00:10,8.0',8.0',0)][bin sky=8]" asphistfile="blank_sky.asphist" outfile="blank_sky_tdet.fits[wmap]" clobber=yes
mkwarf infile="blank_sky_tdet.fits[wmap]" outfile=blank_sky.arf weightfile=blank_sky.wfef egridspec=0.3:11.0:0.1  mskfile=NONE spectrumfile=NONE pbkfile=NONE clobber=yes
mkrmf infile=CALDB outfile=blank_sky.rmf axis1="energy=0:1" axis2="pi=1:1024:1" weights=blank_sky.wfef clobber=yes
