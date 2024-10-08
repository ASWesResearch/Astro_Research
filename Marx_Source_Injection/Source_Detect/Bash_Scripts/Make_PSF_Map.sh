#! /bin/bash

export PFILES="$3/cxcds_param4:/Users/asantini/cxcds_param4;/opt/anaconda3/envs/ciao-4.14/param"
cp -r /Users/asantini/cxcds_param4 $3
#echo $PFILES
mkpsfmap $1 $2 1.4 ecf=0.9 clobber=yes
