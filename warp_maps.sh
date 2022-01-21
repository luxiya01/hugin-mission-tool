#!/bin/sh
PUBLIC_IMAGERY="/run/user/1000/gvfs/smb-share:server=157.132.128.55,share=public/perm/Imagery"
HUGIN_MAP="/run/user/1000/gvfs/smb-share:server=157.132.128.55,share=science/NBP2202/hugin_maps"
AMSR2_DIR="$PUBLIC_IMAGERY/amsr2"
AMSR2_HUGIN_DIR="$HUGIN_MAP/AMSR2-seaice-concentration"
MODIS_DIR="$PUBLIC_IMAGERY/extra/Geotiffs"
MODIS_HUGIN_DIR="$HUGIN_MAP/MODIS-seaice-imagery"
POLARVIEW_DIR="$PUBLIC_IMAGERY/extra/PolarView"
POLARVIEW_HUGIN_DIR="$HUGIN_MAP/polarView-satellite-data"

# Warp AMSR2 data
today=$(date -I | sed -E 's/-([0-9]{2})-/_\1_/')
antarctic_AMSR2="Antarctic_AMSR2_$today.tif"
amundsen_AMSR2="Amundsen_AMSR2_$today.tif"
gdalwarp -t_srs EPSG:4326 -te -180 -90 180 90 "$AMSR2_DIR/$antarctic_AMSR2" $antarctic_AMSR2
gdalwarp -t_srs EPSG:4326 "$AMSR2_DIR/$amundsen_AMSR2" $amundsen_AMSR2
cp $antarctic_AMSR2 "$AMSR2_HUGIN_DIR/Antarctic/$antarctic_AMSR2"
cp $amundsen_AMSR2 "$AMSR2_HUGIN_DIR/Amundsen/$amundsen_AMSR2"
rm $amundsen_AMSR2 $antarctic_AMSR2

# Warp MODIS data
MODIS_files=$(ls $MODIS_DIR *tiff)
for f in $MODIS_files; do
    echo "Checking $f..."
    mod_date=$(stat -c %y "$MODIS_DIR/$f" | sed -E 's/ .+//' | sed -E 's/-([0-9]{2})-/_\1_/')
    echo "Modification date $f: $mod_date"
    if [ $mod_date = $today ]; then
        echo "Warping MODIS $f..."
        warped_MODIS="$(echo $f | sed 's/tiff/tif/')"
        gdalwarp -t_srs EPSG:4326 "$MODIS_DIR/$f" $warped_MODIS
        cp $warped_MODIS "$MODIS_HUGIN_DIR/$warped_MODIS"
        rm $warped_MODIS
    fi
done

# Warp PolarView JP2 images
dirs=$(ls $POLARVIEW_DIR)
for email_dir in $dirs; do
    mod_date=$(stat -c %y "$POLARVIEW_DIR/$email_dir" | sed -E 's/ .+//' | sed -E 's/-([0-9]{2})-/_\1_/')
    echo "Modification date $f: $mod_date"
    if [ $mod_date = $today ]; then
        jp2_files=$(ls $POLARVIEW_DIR/$email_dir | grep jp2)
        for f in $jp2_files; do
            warped_POLARVIEW="$(echo $f | sed -E 's/\w{4}.\w{3}_[A-Z]{2}_[A-Z]{4}_\w{4}_//' | sed -E 's/_.+$/.tif'/)"
            gdalwarp -s_srs EPSG:3031 -t_srs EPSG:4326 "$POLARVIEW_DIR/$email_dir/$f" $warped_POLARVIEW
            cp $warped_POLARVIEW "$POLARVIEW_HUGIN_DIR/$warped_POLARVIEW"
            rm $warped_POLARVIEW
        done
    fi
done
