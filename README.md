# Trampoline detection using CNN

## Intro

This repo contains some code used in my research project on neighborhood effects in consumption. You can download a working paper on my personal [website](http://erikgrenestam.se/wp-content/uploads/2019/04/Bouncing-with-the-Joneses-ErikG.pdf).

Trampolines are popular among Swedish families. Thanks to their size and distinct shape, they can be detected in an aerial photo. To collect data on trampoline ownership, I apply an instance of Inception ResNet to a large set of aerial photos of Swedish neighborhoods taken between 2006 and 2018.

## Installation
conda create -n yolo5env python=3.9
conda activate yolo
pip install -r requirements.txt

## Data

### Image data

Image data is loaded from Google static maps API. Run get_images.py to download the files. This requires a api_key.env text file for the API key.

### Labelling data

I used https://github.com/tzutalin/labelImg to label the data according to the YOLO formatting standard.

Images are split into train and validation sets.

├───images
│   ├───train
│   └───validation
└───labels
    ├───train
    └───validation


## Training 

From the yolov5 directory, run

    python .\train.py --img 640 --batch 16 --epochs 100 --data data/trampolines.yaml --cfg models\yolov5s.yaml --name tm

## Testing

From the yolov5 directory, run

    python .\detect.py --source ../data/test --weights runs/train/tm7/weights/best.pt --data data/trampolines.yaml