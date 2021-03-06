#!/bin/sh

if [[ $# -eq 0 ]] ; then
    echo 'No arguments given. Please provide image path.'
    exit 1
fi

python label_image.py --graph=./model/output_graph.pb --labels=./model/output_labels.txt --input_layer=Placeholder --output_layer=final_result --image=$1