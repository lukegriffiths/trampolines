# Trampoline detection using YOLOv5
## Background

Walking around Oslo, you can see many gardens with trampolines - but how many? 

This repo contains:
* Code to get satellite images from Google Maps using the Static Maps API
* Instructions to:
    - label the data
    - Prepare the data for YOLOv5
    - Train the model and make predictions
    - Visualise the model predictions using PyGMT

Results of the prediction are the coordinates of bounding boxes around the trampolines in the satellite images, as below.

![](./resources/val_batch0_pred.jpg)
## To do

* Extract long and lat of each trampoline from predicted data
* Make maps of trampoline density across Oslo
* Make get_images.py into commandline tool
* Optimise spacing between images to get no overlap at different zooms

## Resources

Train custom object detection model with YOLO V5 - Abhishek Thakur
https://www.youtube.com/watch?v=NU9Xr_NYslo

## Installation

Install the requirements in requirements.txt, which has been adapted from the YOLOv5 requirements file. I used a conda environment (called yolo5env) with python 3.9, and then pip for all required packages, as below:

    conda create -n yolo5env python=3.9
    conda activate yolo5env
    pip install -r requirements.txt

I found that cuda version cu102 had some issues, but cu101 worked well. I haven't tried any newer versions of the cuda package.

Clone Yolov5 from https://github.com/ultralytics/yolov5 into the subfolder /yolov5.

## Data

Image data is loaded from Google static maps API using get_images.py

This script requires an API Key which is stored in api_key.env text file containing one line(you need to make this yourself):

    API_KEY = "YOUR_KEY_HERE"
    
get_images.py will save the images in /images along with a csv text file with the image number, long and lat, and the zoom level.

### Labelling data

I used https://github.com/tzutalin/labelImg to label the data according to the YOLO formatting standard. I cloned the repository and installed the dependencies into a separate clean environment used only for labelling images. 

For labelling, open the folder where you have the images (/images in this case), change type to YOLO, and I used autosave and single class mode ('trampolines').

For YOLO, jmages need to be split into train and validation sets using the file structure below Labels contains text files, and images contains the images. If you follow the below structure, then split_data.py will perform a train-test-split and put the data in the right places. 

    ├───data

        ├───images

            ├───train

            └───validation
        └───labels

            ├───train

            └───validation
    ├───yolov5
        ├───models
            ├───trampolines.yaml

    ├───images


* /images contains images and their labels
* /data contains all the data for training and validation
* /yolov5 contains the cloned YOLOv5 repo, with trampolines.yaml copied from this repo into the /yolov5/models folder.

## Training 

Copy trampolines.yaml into the /yolov5/data/ folder. This contains some model parameters, for example here I use the the yolov5 small model. This file also contains the relative filepaths of the training and validation images.

First cd to the the /yolov5 directory and run

    python .\train.py --img 640 --batch 32 --epochs 200 --data data/trampolines.yaml --cfg models\yolov5s.yaml --name tm

The trained model and metrics will be saved to /yolov5/runs/train in a folder named tmX with X incrementing by 1 each time.

## Testing

From the yolov5 directory, run the following, with the weights folder you want to use (below it looks for the weights in /tm7):

    python .\detect.py --source ../images/data_2022-02-12 --weights runs/train/tm14/weights/best.pt --save-txt --data data/trampolines.yaml

The classified images will be will be saved to /yolov5/runs/detect