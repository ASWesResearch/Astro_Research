#! /bin/bash

#dmcopy "temp.fits[randnum=0:1]" temp2.fits clobber=yes
# Assign some random time during the observation to each photon.
#cp `paccess dmkeypar` $3_dmkeypar.par
#cp `paccess dmtcalc` $3_dmtcalc.par
#cp `paccess dmsort` $3_dmsort.par

echo "test1"
#t0=`dmkeypar $1 TSTART echo+`
#t0=`dmkeypar @@$3_dmkeypar.par $1 TSTART echo+`
t0=`dmkeypar @@$6 $1 TSTART echo+`
t1=`dmkeypar @@$6 $1 TSTOP echo+`
#t1=`dmkeypar  @@$3_dmkeypar.par $1 TSTOP echo+`
echo $t0
echo $t1
echo "test2"

#dmtcalc temp2.fits temp3.fits expression="time=$t0+($t1-$t0)*#trand" clobber=yes
#cp `paccess dmtcalc` $3"_dmtcalc.par"
echo "test2.1"
#dmtcalc $2 $3_temp3.fits expression="time=$t0+($t1-$t0)*#trand" clobber=yes
#echo $3_dmtcalc.par
#echo "$t0+($t1-$t0)*#trand"
#echo $t0+($t1-$t0)
t3=$t1-$t0
echo $t3
#dmtcalc @@$7 $2 $3_temp3.fits expression="time=$t0+($t1-$t0)*#trand" clobber=yes
#dmtcalc @@$7 $2 $3_temp3.fits expression="time=$t0+($t3)*#trand" clobber=yes
dmtcalc @@$7 $2 $3_temp3.fits expression="time=$t0+($t1-$t0)*#rand" clobber=yes
#dmtcalc @@$7 $2 $3_temp3.fits expression="time=$t0+($t1-$t0)*#trand" clobber=h
#dmtcalc @@$3_dmtcalc.par $2 $3_temp3.fits expression="time=$t0+($t1-$t0)*#trand" clobber=yes
echo "test2.2"
dmsort @@$8 $3_temp3.fits $3_temp4.fits keys=TIME clobber=yes
#dmsort @@$3_dmsort.par $3_temp3.fits $3_temp4.fits keys=TIME clobber=yes
echo "test3"

# Reproject the blank sky fields to the same position on the sky as the marx simulation.
##punlearn reproject_events
#pset reproject_events clobber=yes
#reproject_events infile=temp4.fits outfile=acis7s_bkg_reproj.fits aspect=diffuse_asol1.fits match=$1 clobber=yes
#cp `paccess reproject_events` $5
#echo "test4"
#ls `paccess reproject_events` $5
reproject_events @@$5 infile=$3_temp4.fits outfile=$3_acis5s_bkg_reproj.fits aspect=$4 match=$1 clobber=yes
echo "test5"

# Merge marx simulation and blank sky fields into a single fits table.
##punlearn dmmerge
##dmmerge "$1[cols ccd_id,node_id,chip,det,sky,pha,energy,pi,fltgrade,grade,status,time]","acis7s_bkg_reproj.fits[cols ccd_id,node_id,chip,det,sky,pha,energy,pi,fltgrade,grade,status,time]" merged.fits clobber=yes
