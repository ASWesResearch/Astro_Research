#! /bin/bash

export PFILES="$3/cxcds_param4:$PFILES"
cp -r ../Parameter_Files/cxcds_param4 $3
mkpsfmap $1 $2 2.3 ecf=0.9 clobber=yes
