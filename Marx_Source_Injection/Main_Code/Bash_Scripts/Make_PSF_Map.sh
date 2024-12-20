#! /bin/bash

export PFILES="$3"
cp -r ../Parameter_Files/param $3
mkpsfmap $1 $2 2.3 ecf=0.9 clobber=yes
