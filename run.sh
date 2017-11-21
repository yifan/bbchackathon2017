#!/bin/bash -ex 

# this script expects story.txt to be exist in the same folder 

rm -fr data output.txt
nl story.txt | while read id txt2; do
     mkdir -p data
     txt=$(echo $txt2 | tr '\r' ' ' | sed 's: $::')
     echo "Processing: TEXT ${txt}"
     echo "Processing: ID ${id}"
     python scripts/google_image_search.py -n 5 "$txt" data/$id
     python scripts/tts.py "$txt" "data/$id"
done
rm -fr output.txt
