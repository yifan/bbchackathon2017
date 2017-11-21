#!/bin/bash -ex 

# this script will make story from aljazeera website and SUMMA API's

rm -fr data output.txt data_aljazeera

#process aljazeera data 
python scripts/getAljazeeraStory.py   > tmp$$
cat tmp$$ | awk -F "\t" '{print $1}' > story.txt 
cat tmp$$ | awk -F "\t" '{print $2}' > story_images.txt 
rm -fr tmp$$
data=data_aljazeera
mkdir -p $data
nl story.txt | while read id txt2; do
     txt=$(echo $txt2 | tr '\r' ' ' | sed 's: $::')
     echo "Processing: TEXT ${txt}"
     echo "Processing: ID ${id}"
     python scripts/google_image_search.py -n 5 "$txt" $data/$id
     python scripts/tts.py "$txt" "$data/$id"
done

nl story_images.txt | grep [0-9] |  while read id image; do
    echo "Getting image: $id $image"
    wget $image -O $data/$id/0.jpg
done
    

rm -fr output.txt
