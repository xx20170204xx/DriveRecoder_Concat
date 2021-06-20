#!/bin/bash

#ああああ
if [ ! -e Video ]; then
    exit 1
fi

if [ ! -e Video/MAP ]; then
    mkdir Video/MAP
fi

if [ ! -e Event ]; then
    exit 1
fi

if [ ! -e Event/MAP ]; then
    mkdir Event/MAP
fi

if [ ! -e Movie ]; then
    mkdir Movie
fi



find $(pwd)/Video/NMEA -name "*.NMEA" -exec python ./fileread.py {} \;
mv -vf $(pwd)/Video/NMEA/*.png $(pwd)/Video/MAP/
find $(pwd)/Event/NMEA -name "*.NMEA" -exec python ./fileread.py {} \;
mv -vf $(pwd)/Event/NMEA/*.png $(pwd)/Event/MAP/

rm -f vlist*.txt

while read LINE
do
    NMEA_FILE=$(basename $LINE)
    ID=${NMEA_FILE##FILE}
    ID=${ID%%-M.NMEA}
    echo $ID$'\t'Video >>vlist_tmp.txt
done <<< $(find $(pwd)/Video/NMEA -name "*.NMEA")

while read LINE
do
    NMEA_FILE=$(basename $LINE)
    ID=${NMEA_FILE##EMER}
    ID=${ID%%-M.NMEA}
    echo $ID$'\t'Event >>vlist_tmp.txt
done <<< $(find $(pwd)/Event/NMEA -name "*.NMEA")

cat vlist_tmp.txt | sort >vlist.txt

while read -u 3 ID TYPE
do
    echo "${ID},${TYPE}"
    if [ "${TYPE}" = "Video" ]; then
        MAP_FILE="FILE${ID}-M.NMEA_map.png"
        VIDEO_FILE="FILE${ID}-M.MP4"
	    if [ -e Video/MAP/${MAP_FILE} ]; then
	        ffmpeg -i Video/M/${VIDEO_FILE} -i Video/MAP/${MAP_FILE} -filter_complex "[1:v]format=yuva420p,lut=a='val*0.7',[0:v] overlay=0:H-h" Movie/${VIDEO_FILE}
	        echo "file $(pwd)/Movie/${VIDEO_FILE}" >>vlist_ffmpeg.txt
	    else
	        echo "file $(pwd)/Video/M/${VIDEO_FILE}" >>vlist_ffmpeg.txt
	    fi
    elif [ "${TYPE}" = "Event" ]; then
        MAP_FILE="EMER${ID}-M.NMEA_map.png"
        VIDEO_FILE="EMER${ID}-M.MP4"
	    if [ -e Event/MAP/${MAP_FILE} ]; then
	        ffmpeg -i Event/M/${VIDEO_FILE} -i Event/MAP/${MAP_FILE} -filter_complex "[1:v]format=yuva420p,lut=a='val*0.7',[0:v] overlay=0:H-h" Movie/${VIDEO_FILE}
	        echo "file $(pwd)/Movie/${VIDEO_FILE}" >>vlist_ffmpeg.txt
	    else
	        echo "file $(pwd)/Event/M/${VIDEO_FILE}" >>vlist_ffmpeg.txt
	    fi
    else
        echo ""
    fi

done 3<vlist.txt

while read -u 3 ID TYPE
do
    echo "${ID},${TYPE}"
    if [ "${TYPE}" = "Video" ]; then
        VIDEO_FILE="FILE${ID}-2.MP4"
        echo "file $(pwd)/Video/2/${VIDEO_FILE}" >>vlist_ffmpeg2.txt
    elif [ "${TYPE}" = "Event" ]; then
        VIDEO_FILE="EMER${ID}-2.MP4"
        echo "file $(pwd)/Event/2/${VIDEO_FILE}" >>vlist_ffmpeg2.txt
    else
        echo ""
    fi

done 3<vlist.txt


ffmpeg -f concat -safe 0 -i vlist_ffmpeg.txt movie.mp4
ffmpeg -f concat -safe 0 -i vlist_ffmpeg2.txt movie2.mp4

# ffmpeg -i M/FILE210403-015854-000105-M.MP4 -i ./NMEA/FILE210403-015854-000105-N.NMEAmap.png -filter_complex "[1:v]format=yuva420p,lut=a='val*0.7',[0:v] overlay=0:H-h" M/FILE210403-015854-000105-M.MP4_map.mp4


