#! /bin/bash

export PFILES="$3"
cp -r ../Parameter_Files/cxcds_param4 $3
export ASCDS_WORK_PATH=$3/tmpdir
mkdir $3/tmpdir
wavdetect $1 outfile=$2 scellfile=$6 imagefile=$7 defnbkgfile=$8 scales='1 2 4 8' psffile=$4 regfile=$5 interdir=$ASCDS_WORK_PATH expfile=$3_expmap.fits bkginput=$9 clobber=yes verbose=0
#wavdetect $1 outfile=$2 scellfile=$6 imagefile=$7 defnbkgfile=$8 scales='1 2 4 8 16' psffile=$4 regfile=$5 interdir=$ASCDS_WORK_PATH expfile=$3_expmap.fits bkginput=$9 clobber=yes verbose=0
##wavdetect $1 outfile=$2 scellfile=$6 imagefile=$7 defnbkgfile=$8 scales='1 2 4 8 16' psffile=$4 regfile=$5 interdir=$ASCDS_WORK_PATH bkginput=$9 clobber=yes verbose=0
#wavdetect $1 outfile=$2 scellfile=$6 imagefile=$7 defnbkgfile=$8 scales='1 2 4 8' psffile=$4 regfile=$5 interdir=$ASCDS_WORK_PATH expfile=$3_expmap.fits bkginput=$9 bkgerrinput=$10 clobber=yes verbose=4
#wavdetect $1 outfile=$2 scellfile=$6 imagefile=$7 defnbkgfile=$8 scales='1 2 4 8' psffile=$4 regfile=$5 interdir=$ASCDS_WORK_PATH expfile=$3_expmap.fits bkginput=$9 bkgerrinput=yes log=no clobber=yes verbose=4
##wavdetect $1 outfile=$2 scellfile=$6 imagefile=$7 defnbkgfile=$8 scales='1 2 4 8' psffile=$4 regfile=$5 interdir=$ASCDS_WORK_PATH expfile=$3_expmap.fits exptime=${10} bkginput=$9 bkgtime=${11} bkgerrinput=yes log=no clobber=yes verbose=0
#wavdetect $1 outfile=$2 scellfile=$6 imagefile=$7 defnbkgfile=$8 scales=${12} psffile=$4 regfile=$5 interdir=$ASCDS_WORK_PATH expfile=$3_expmap.fits exptime=${10} bkginput=$9 bkgtime=${11} bkgerrinput=yes log=no clobber=yes verbose=0
#wavdetect $1 outfile=$2 scellfile=$6 imagefile=$7 defnbkgfile=$8 scales='${12}' psffile=$4 regfile=$5 interdir=$ASCDS_WORK_PATH expfile=$3_expmap.fits exptime=${10} bkginput=$9 bkgtime=${11} bkgerrinput=yes log=no clobber=yes verbose=0
##wavdetect $1 outfile=$2 scellfile=$6 imagefile=$7 defnbkgfile=$8 scales='$9' psffile=$4 regfile=$5 interdir=$ASCDS_WORK_PATH expfile=$3_expmap.fits bkgerrinput=yes log=no clobber=yes verbose=0
