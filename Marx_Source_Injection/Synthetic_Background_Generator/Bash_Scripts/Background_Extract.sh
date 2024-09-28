#! /bin/bash

#dmextract infile="acis5sbkg.fits[sky=rotbox(0:00:58,+0:00:10,8.0',8.0',0)][bin pi]" outfile='blank_sky.pi' wmap="[bin tdet=8]" clobber=yes
#dmextract infile="$1[sky=rotbox(0:00:58,+0:00:10,8.0',8.0',0)][bin pi]" outfile=$5'_blank_sky.pi' wmap="[bin tdet=8]" clobber=yes
#dmextract infile="$1[sky=rotbox(0:00:58,+0:00:10,3.2',3.5',0)][bin pi]" outfile=$5'_blank_sky.pi' wmap="[bin tdet=8]" clobber=yes
#dmextract infile="$1[sky=rotbox(0:00:58,+0:00:10,2.2',2.5',0)][bin pi]" outfile=$5'_blank_sky.pi' wmap="[bin tdet=8]" clobber=yes
#outfile=$3_acis5s_bkg_reproj.fits
dmextract infile=$4"_acis5s_bkg_reproj.fits[sky=rotbox(0:00:58,+0:00:10,8.0',8.0',0)][bin pi]" outfile=$4'_blank_sky.pi' wmap="[bin tdet=8]" clobber=yes
#asphist infile=diffuse_asol1.fits outfile=blank_sky.asphist evtfile="diffuse_evt2.fits[ccd_id=7]" clobber=yes
asphist infile=$1 outfile=$4_blank_sky.asphist evtfile=$2"[ccd_id=$3]" clobber=yes
#sky2tdet infile=$1"[sky=rotbox(0:00:58,+0:00:10,8.0',8.0',0)][bin sky=8]" asphistfile=$5"_blank_sky.asphist" outfile=$5"_blank_sky_tdet.fits[wmap]" clobber=yes
sky2tdet infile=$4"_acis5s_bkg_reproj.fits[sky=rotbox(0:00:58,+0:00:10,8.0',8.0',0)][bin sky=8]" asphistfile=$4"_blank_sky.asphist" outfile=$4"_blank_sky_tdet.fits[wmap]" clobber=yes
#sky2tdet infile=$1"[sky=rotbox(0:00:58,+0:00:10,3.2',3.5',0)][bin sky=8]" asphistfile=$5"_blank_sky.asphist" outfile=$5"_blank_sky_tdet.fits[wmap]" clobber=yes
#sky2tdet infile=$1"[sky=rotbox(0:00:58,+0:00:10,2.2',2.5',0)][bin sky=8]" asphistfile=$5"_blank_sky.asphist" outfile=$5"_blank_sky_tdet.fits[wmap]" clobber=yes
mkwarf infile=$4"_blank_sky_tdet.fits[wmap]" outfile=$4_blank_sky.arf weightfile=$4_blank_sky.wfef egridspec=0.3:11.0:0.1  mskfile=NONE spectrumfile=NONE pbkfile=NONE clobber=yes
mkrmf infile=CALDB outfile=$4_blank_sky.rmf axis1="energy=0:1" axis2="pi=1:1024:1" weights=$4_blank_sky.wfef clobber=yes
