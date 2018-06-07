#!/bin/bash
printf "1"
unset PYTHONHOME
printf "2"
source /soft/ciao/bin/ciao.bash -q -o
printf "3"
ciaorun "$*"
