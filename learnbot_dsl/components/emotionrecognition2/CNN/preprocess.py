from __future__ import print_function
import os
import numpy as np
import random
import cv2
from six.moves import cPickle as pickle

# Destination folder for final pickle file.
PICKLE_FOLDER = '.'

# Name of final pickle file.
FINAL_PICKLE = 'emotion_dataset.pickle'

# Name of folders containing image data.
# Important Note: Remember this order of folders, as class labels are generated according to this order.
FOLDERS = [
    'data/happy',
    'data/sad',
    'data/neutral',
    'data/angry',
    'data/surprised',
    ]

IMAGE_HEIGHT = 128  # Images will be resized having this height
IMAGE_WIDTH = 128   # Images will be resized having this width
NUM_CHANNELS = 1    # Number of channels (1 for grayscale images, 3 for RGB images)

VALID_SIZE = 4000   # Total number of images in validation set ( number of classes * validation images per class)
TEST_SIZE = 4000    # Total number of images in test set ( number of classes * test images per class)
TRAIN_SIZE = 18750  # Total number of images in training set ( number of classes * training images per class)

np.random.seed(100)


def load_emotion(folder):
    """Function for loading the data for a single emotion label"""

    # Get image files in the folder and randomly shuffle them
    image_files = os.listdir(folder)
    random.shuffle(image_files)

    # Create numpy array to store data of all images
    dataset = np.ndarray(shape=(len(image_files), IMAGE_HEIGHT, IMAGE_WIDTH), dtype=np.float64)
    print(folder)

    num_images = 0
    for image in image_files:

        image_file = os.path.join(folder, image)

        # Read image
        image_data = cv2.imread(image_file)

        # Resize image
        image_data = cv2.resize(image_data,(IMAGE_WIDTH, IMAGE_HEIGHT))

        # Convert image to grayscale
        if(image_data.ndim == 3):
            image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2GRAY)

        # Zero mean normalization
        image_data = (image_data - np.mean(image_data)) / np.std(image_data)

        # Add image to data set
        dataset[num_images, :, :] = image_data
        num_images = num_images + 1

    print('Full dataset tensor:', dataset.shape)
    print('Mean:', np.mean(dataset))
    print('Standard deviation:', np.std(dataset))

    return dataset


def create_pickle(data_folders, force=False):
    """Function for converting data into separate pickle files for each label.
    data_folders is the list of folder names of all classes.
    Set force = False if pickle files are already created and are not to be overwritten.
    Set force = True to overwrite already created pickle files.
    """
    # List of names of pickle files for individual classes
    dataset_names = []

    for folder in data_folders:
        set_filename = folder + '.pickle'
        dataset_names.append(set_filename)

        if os.path.exists(set_filename) and not force:
            print('%s already present - Skipping pickling.' % set_filename)
        else:
            print('Pickling %s.' % set_filename)
            dataset = load_emotion(folder)
            try:
                with open(set_filename, 'wb') as f:
                    pickle.dump(dataset, f, pickle.HIGHEST_PROTOCOL)
            except Exception as e:
                print('Unable to save data to', set_filename, ':', e)

    return dataset_names


train_datasets = create_pickle(FOLDERS)


def make_arrays(nrows, img_height,img_width):
    """ Function for creating numpy arrays to store data 
    according to number of examples and image size
    """
    dataset = np.ndarray((nrows, img_height, img_width), dtype=np.float64)
    labels = np.ndarray(nrows, dtype=np.int32)
    return dataset, labels


def merge_datasets(pickle_files):
    """Function for merging the pickle files of different labels 
    and creating training, validation and test datasets
    """
    num_classes = len(pickle_files)

    # Create numpy arrays for storing final validation, test and training sets
    valid_dataset, valid_labels = make_arrays(VALID_SIZE, IMAGE_HEIGHT, IMAGE_WIDTH)
    test_dataset, test_labels = make_arrays(TEST_SIZE, IMAGE_HEIGHT, IMAGE_WIDTH)
    train_dataset, train_labels = make_arrays(TRAIN_SIZE, IMAGE_HEIGHT, IMAGE_WIDTH)

    # Calculate number of images per class
    vsize_per_class = VALID_SIZE // num_classes
    testsize_per_class = TEST_SIZE // num_classes
    tsize_per_class = TRAIN_SIZE // num_classes

    start_v, start_t, start_test = 0, 0, 0
    end_v, end_t ,end_test = vsize_per_class, tsize_per_class, testsize_per_class
    end_l = vsize_per_class + tsize_per_class + testsize_per_class

    # Take corresponding number of images from each class and add to the final numpy arrays
    for label, pickle_file in enumerate(pickle_files):
        try:
            with open(pickle_file, 'rb') as f:
                emotion_set = pickle.load(f)
                np.random.shuffle(emotion_set)

                if valid_dataset is not None:
                    valid_emotion = emotion_set[: vsize_per_class, : , :]
                    valid_dataset[start_v : end_v, : , :] = valid_emotion
                    valid_labels[start_v : end_v] = label
                    start_v += vsize_per_class
                    end_v += vsize_per_class

                test_emotion = emotion_set[vsize_per_class : vsize_per_class + testsize_per_class, : , :]
                test_dataset[start_test : end_test, : , :] = test_emotion
                test_labels[start_test : end_test] = label
                start_test += testsize_per_class
                end_test += testsize_per_class

                train_emotion = emotion_set[vsize_per_class + testsize_per_class : end_l, : , :]
                train_dataset[start_t : end_t, : , :] = train_emotion
                train_labels[start_t : end_t] = label
                start_t += tsize_per_class
                end_t += tsize_per_class

        except Exception as e:
            print('Unable to process data from', pickle_file, ':', e)
            raise

    return valid_dataset, valid_labels, test_dataset, test_labels, train_dataset, train_labels


valid_dataset, valid_labels, test_dataset, test_labels, train_dataset, train_labels = merge_datasets(train_datasets)
print('Training:', train_dataset.shape, train_labels.shape)
print('Validation:', valid_dataset.shape, valid_labels.shape)
print('Testing:', test_dataset.shape, test_labels.shape)


def randomize(dataset, labels):
    """Function for randomly shuffling the data"""
    permutation = np.random.permutation(labels.shape[0])
    shuffled_dataset = dataset[permutation, :]
    shuffled_labels = labels[permutation]
    return shuffled_dataset, shuffled_labels


train_dataset, train_labels = randomize(train_dataset, train_labels)
test_dataset, test_labels = randomize(test_dataset, test_labels)
valid_dataset, valid_labels = randomize(valid_dataset, valid_labels)

# Save the final pickle file containing training, validation and test data
final_pickle = os.path.join( PICKLE_FOLDER, FINAL_PICKLE )
try:
    with open(final_pickle, 'wb') as f:
        save = {
            'train_dataset': train_dataset,
            'train_labels': train_labels,
            'valid_dataset': valid_dataset,
            'valid_labels': valid_labels,
            'test_dataset': test_dataset,
            'test_labels': test_labels,
            }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        f.close()
except Exception as e:
    print('Unable to save data to', final_pickle, ':', e)
    raise

# Print final pickle size
statinfo = os.stat(final_pickle)
print('Compressed pickle size:', statinfo.st_size)