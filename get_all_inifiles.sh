#!/bin/sh
cd /home/li/Documents/local-corr/data/210209
INI_FILES="all_inifiles.ini"
rm $INI_FILES

for f in $(find . -name "*ini"); do
    echo "####################################################" >> $INI_FILES
    echo "# $(basename $f)" >> $INI_FILES
    echo "####################################################" >> $INI_FILES
    cat $f >> $INI_FILES
    echo "" >> $INI_FILES
done

