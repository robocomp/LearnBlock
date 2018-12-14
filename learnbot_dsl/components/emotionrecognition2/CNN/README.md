# Data Pre-Processing and Training the CNN

The data pre-processing code is present in `preprocess.py`. The code for training the CNN on this pre-processed data is present in `train.py`.

## Directory Structure

```
CNN
|--checkpoints
|--data
|   |--angry
|   |   |--angry face images
|   |--happy
|   |   |--happy face images
|   |--neutral
|   |   |--neutral face images
|   |--sad
|   |   |--sad face images
|   |--surprised
|       |--surprised face images
|--preprocess.py
|--train.py
|--README.md
|--pickles (optional)
|--pb (optional)
```

The data folder has sub-folders, each corresponding to one emotion label. Each sub-folder should contain all the images of that emotion label; in jpg, png, tiff or any other format supported by [cv2.imread](https://docs.opencv.org/3.0-beta/modules/imgcodecs/doc/reading_and_writing_images.html#imread). Note that you don't need to manually split the data set into training, validation and test sets. This will be done during preprocessing.

Each image should contain only one face. The images may be colored or black-and-white. They may be of different sizes.

You can optionally add 2 other folders: 'pickles' and/or 'pb' as shown in the above directory structure. These can be used to store the .pickle(obtained after pre-processing) and .pb(obtained after training) files respectively. This is just to keep similar files together when you are training multiple models.

## preprocess.py

The following pre-processing is done on each image:
1. Resizing to a common size
2. Converting to grayscale
3. Zero mean normalization

The images are randomly shuffled and divided into training, validation and test sets. Numeric labels are created. All the three sets, along with the labels are saved together in a single `.pickle` file.

Currently, the training and pre-processing has been done for 5 classes. To add more classes, add new sub-folders in the data folder. Add the names of these folders to the `FOLDERS` list in `preprocess.py`. Add the new emotions to `specificworker.py` in the **same order** as that in `preprocess.py`.

## train.py

It loads the data sets from the `.pickle` file created after pre-processing, and trains the CNN using this data. The model is evaluated after every 50 steps, and the mini-batch and validation accuracies are printed. A checkpoint is saved after every 50 steps in the `checkpoints` folder. These can be useful in case the training stops in the middle due to some system failure.

After the training is completed, the trained model is saved in a `.pb` file. In order to use the model for emotion recognition, you need to move this file to the `emotionrecognition2/assets` folder. Also remember to update the model file name in `specificworker.py`.

The current emotion recognition model has been trained using [AffectNet](http://mohammadmahoor.com/affectnet/) data set.

## References:

1. A. Mollahosseini; B. Hasani; M. H. Mahoor, "AfectNet: A Database for Facial Expression, Valence, and Arousal Computing in the Wild," in IEEE Transactions on Afective Computing, 2017.
2. [Assignments for Udacity Deep Learning class with TensorFlow](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/udacity)
