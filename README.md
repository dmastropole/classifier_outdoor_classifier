# classifier_outdoor_classifier

This project retrains the Inception V3 model to classify indoor and outdoor images. 

## Creating the Dataset

The dataset was created from a subset of the [YouTube-8M Video-level features dataset](https://research.google.com/youtube8m/index.html), 
and instructions on how to download the dataset and the corresponding labels can be found [here](https://research.google.com/youtube8m/download.html).

To generate the subset of video records used in this application, run the following line in the empty video folder:

`curl data.yt8m.org/download.py | shard=1,100 partition=2/video/train mirror=us python`

The video folder will be populated with `.tfrecord` files. 
To retrieve the images and class labels, run `get_data.py`, which will create the subdirectories `indoor` and `outdoor` in the
`test_images` and `train_images` directories and populate them with `.jpg` files. 

## Training the Model

[This TensorFlow tutorial](https://www.tensorflow.org/hub/tutorials/image_retraining) covers the process of retraining the Inception V3 model.
The code for retraining and inference have been downloaded from the website and are called `retrain.py` and `label_image.py` in this repository.
You can run the python script directly, according to the instructions on the tutorial, or you can run the script `train.sh`.
You should end up with an accuracy of roughly 86%. 

NOTE: The `retrain.py` script splits the images in `train_images` into training/validation sets and computes training/validation accuracies.
The directory `test_images` exists as an example of how to create a train/test split of the data.

## Classifying Images

Run `predict.sh <image_path>`, which will give you the probabilities of the image belonging to the indoor and outdoor classes. 
Alternatively, you can run `label_image.py` with the appropriate arguments.

## Running Tests

Run `python tests.py`.




