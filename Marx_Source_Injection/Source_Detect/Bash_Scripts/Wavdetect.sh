#! /bin/bash

export PFILES="$3/cxcds_param4:$PFILES"
cp -r ../Parameter_Files/cxcds_param4 $3
export ASCDS_WORK_PATH=$3/tmpdir
mkdir $3/tmpdir
#wavdetect $1 outfile=$2 scellfile=$3_source_cell.fits imagefile=$3_image.fits defnbkgfile=$3_background.fits scales='1 2 4 8' psffile=$4 regfile=$5 interdir=$ASCDS_WORK_PATH expfile=$3_expmap.fits clobber=yes verbose=0
##wavdetect $1 outfile=$2 scellfile=$6 imagefile=$7 defnbkgfile=$8 scales='1 2 4 8' psffile=$4 regfile=$5 interdir=$ASCDS_WORK_PATH expfile=$3_expmap.fits clobber=yes verbose=0
wavdetect $1 outfile=$2 scellfile=$6 imagefile=$7 defnbkgfile=$8 scales='1 2 4 8' psffile=$4 regfile=$5 interdir=$ASCDS_WORK_PATH expfile=$3_expmap.fits bkginput=$9 clobber=yes verbose=0
