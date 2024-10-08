#! /bin/bash

export PFILES="$3/cxcds_param4:/Users/asantini/cxcds_param4;/opt/anaconda3/envs/ciao-4.14/param"
cp -r /Users/asantini/cxcds_param4 $3
export ASCDS_WORK_PATH=$3/tmpdir
mkdir $3/tmpdir
wavdetect $1 outfile=$2 scellfile=$3_source_cell.fits imagefile=$3_image.fits defnbkgfile=$3_background.fits scales='1 2 4 8' psffile=$4 interdir=$ASCDS_WORK_PATH clobber=yes verbose=0
#echo $PFILES
#echo $ASCDS_WORK_PATH
