#!/bin/sh

python retrain.py --image_dir=./train_images --output_graph=./model/output_graph.pb --output_labels=./model/output_labels.txt --summaries_dir=./model/retrain_logs --how_many_training_steps=2000