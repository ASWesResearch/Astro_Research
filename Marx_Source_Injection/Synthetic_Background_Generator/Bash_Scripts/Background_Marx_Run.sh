#dmcopy "acis7sbkg.fits[EVENTS][bin x=::32,y=::32]" chip-shape.fits option=image
dmcopy "$1[EVENTS][bin x=::32,y=::32]" chip-shape.fits option=image
marx @@/opt/anaconda3/envs/ciao-4.14/share/marx/pfiles/marx.par SourceFlux=3. SpectrumType="FILE" SpectrumFile="bkgspec.tbl" \
       ExposureTime=0 NumRays=$2 TStart=2012.5 OutputDir=$6 \
       DetectorType="ACIS-S" DitherModel="INTERNAL" RA_Nom=0 Dec_Nom=0 \
       Roll_Nom=0 SourceRA=$3 SourceDEC=$4 \
       SourceType="IMAGE" S-ImageFile="chip-shape.fits"
#marxcat diffuse bkg diffuse_with_bkg
marxcat $5 $6 source_with_bkg
marx2fits source_with_bkg source_with_bkg.fits
