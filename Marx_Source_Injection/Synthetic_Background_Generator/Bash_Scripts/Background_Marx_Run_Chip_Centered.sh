#dmcopy "acis7sbkg.fits[EVENTS][bin x=::32,y=::32]" chip-shape.fits option=image
#dmcopy $1"[EVENTS][bin x=::32,y=::32]" $6_chip-shape.fits option=image
#$5"_bkgspec.tbl"
#dmcopy $5"_acis5s_bkg_reproj.fits[EVENTS][bin x=::32,y=::32]" $5_chip-shape.fits option=image
##dmcopy $7"[sky=rotbox(0:00:58,+0:00:10,8.5',8.5',0)]" $5_image.fits
#dmcopy $7"[EVENTS][bin x=::32,y=::32]" $5_chip-shape.fits option=image
##dmcopy $5_image.fits"[EVENTS][bin x=::32,y=::32]" $5_chip-shape.fits option=image
#23:59:44.242 = 359.934341667
#+00:03:51.82 =0.0643944444444444
#-0.0065597 = 359.927781967
#0.0025008 =0.0668952444444444
marx @@$3 SourceFlux=3. SpectrumType="FILE" SpectrumFile=../Required_Files/bkgspec.tbl \
       ExposureTime=0 NumRays=-$1 OutputDir=$2 \
       DetectorType="ACIS-I" DitherModel="INTERNAL" RA_Nom=0 Dec_Nom=0 \
       Roll_Nom=0 SourceRA=359.927781967 SourceDEC=0.066895244 \
       SourceType="IMAGE" S-ImageFile=../Required_Files/chip-shape_Centered_Full.fits GratingType=NONE RandomSeed=$4
#$5"_chip-shape.fits"
#TStart=2012.5
#marxcat diffuse bkg diffuse_with_bkg
#marxcat $4 $5 $5_source_with_bkg
##marxcat $3 $2 $3_source_with_bkg
##marx2fits $3_source_with_bkg $3_source_with_bkg.fits
marx2fits $2 $2.fits
