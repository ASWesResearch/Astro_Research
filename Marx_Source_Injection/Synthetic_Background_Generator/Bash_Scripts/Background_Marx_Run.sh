#dmcopy "acis7sbkg.fits[EVENTS][bin x=::32,y=::32]" chip-shape.fits option=image
#dmcopy $1"[EVENTS][bin x=::32,y=::32]" $6_chip-shape.fits option=image
#$5"_bkgspec.tbl"
#dmcopy $5"_acis5s_bkg_reproj.fits[EVENTS][bin x=::32,y=::32]" $5_chip-shape.fits option=image
##dmcopy $7"[sky=rotbox(0:00:58,+0:00:10,8.5',8.5',0)]" $5_image.fits
#dmcopy $7"[EVENTS][bin x=::32,y=::32]" $5_chip-shape.fits option=image
##dmcopy $5_image.fits"[EVENTS][bin x=::32,y=::32]" $5_chip-shape.fits option=image
marx @@$6 SourceFlux=3. SpectrumType="FILE" SpectrumFile=../Background_Generator/Test_Example/bkgspec.tbl \
       ExposureTime=0 NumRays=-$1 OutputDir=$5 \
       DetectorType="ACIS-I" DitherModel="INTERNAL" RA_Nom=$2 Dec_Nom=$3 \
       Roll_Nom=0 SourceRA=$2 SourceDEC=$3 \
       SourceType="IMAGE" S-ImageFile=../Background_Generator/Test_Example/chip-shape.fits GratingType=NONE
#$5"_chip-shape.fits"
#TStart=2012.5
#marxcat diffuse bkg diffuse_with_bkg
#marxcat $4 $5 $5_source_with_bkg
marxcat $5 $4 $5_source_with_bkg
marx2fits $5_source_with_bkg $5_source_with_bkg.fits
marx2fits $5 $5.fits
