# features.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import numpy as np
import util
import samples

DIGIT_DATUM_WIDTH=28
DIGIT_DATUM_HEIGHT=28

def basicFeatureExtractor(datum):
    """
    Returns a binarized and flattened version of the image datum.

    Args:
        datum: 2-dimensional numpy.array representing a single image.

    Returns:
        A 1-dimensional numpy.array of features indicating whether each pixel
            in the provided datum is white (0) or gray/black (1).
    """
    features = np.zeros_like(datum, dtype=int)
    features[datum > 0] = 1
    return features.flatten()

def enhancedFeatureExtractor(datum):
    """
    Returns a feature vector of the image datum.

    Args:
        datum: 2-dimensional numpy.array representing a single image.

    Returns:
        A 1-dimensional numpy.array of features designed by you. The features
            can have any length.

    ## DESCRIBE YOUR ENHANCED FEATURES HERE...

    new_features is of length 3
    first element = 1 if there is one white region; 0 otherwise
    second element = 1 if there are two separate white regions; 0 otherwise
    third element = 1 if there are three separate white regions; 0 otherwise

    ##
    """
    features = basicFeatureExtractor(datum)

    "*** YOUR CODE HERE ***"
    original_feature = np.array(features)
    new_features = np.zeros(3, int)
    count = 0

    for width in range(DIGIT_DATUM_WIDTH):
        for height in range(DIGIT_DATUM_HEIGHT):
            if original_feature[DIGIT_DATUM_HEIGHT*width+height] == 0:
                count += 1
                dfs(width, height, original_feature)

    if count == 1:
        new_features[0] = 1

    if count == 2:
        new_features[1] = 1

    if count == 3:
        new_features[2] = 1

    return np.append(features, new_features)


def dfs(width, height, original_feature):
  
    if width+1 < DIGIT_DATUM_WIDTH: 
        if original_feature[DIGIT_DATUM_HEIGHT*(width+1)+height] == 0:
            original_feature[DIGIT_DATUM_HEIGHT*(width+1)+height] = 1
            dfs(width+1, height, original_feature)

    if width-1 >= 0:
        if original_feature[DIGIT_DATUM_HEIGHT*(width-1)+height] == 0:
            original_feature[DIGIT_DATUM_HEIGHT*(width-1)+height] = 1
            dfs(width-1, height, original_feature)

    if height+1 < DIGIT_DATUM_HEIGHT:
        if original_feature[DIGIT_DATUM_HEIGHT*width+(height+1)] == 0:
            original_feature[DIGIT_DATUM_HEIGHT*width+(height+1)] = 1
            dfs(width, height+1, original_feature) 

    if height-1 >= 0:
        if original_feature[DIGIT_DATUM_HEIGHT*width+(height-1)] == 0:
            original_feature[DIGIT_DATUM_HEIGHT*width+(height-1)] = 1
            dfs(width, height-1, original_feature)          


def analysis(model, trainData, trainLabels, trainPredictions, valData, valLabels, validationPredictions):
    """
    This function is called after learning.
    Include any code that you want here to help you analyze your results.

    Use the print_digit(numpy array representing a training example) function
    to the digit

    An example of use has been given to you.

    - model is the trained model
    - trainData is a numpy array where each row is a training example
    - trainLabel is a list of training labels
    - trainPredictions is a list of training predictions
    - valData is a numpy array where each row is a validation example
    - valLabels is the list of validation labels
    - valPredictions is a list of validation predictions

    This code won't be evaluated. It is for your own optional use
    (and you can modify the signature if you want).
    """

    # Put any code here...
    # Example of use:
    # for i in range(len(trainPredictions)):
    #     prediction = trainPredictions[i]
    #     truth = trainLabels[i]
    #     if (prediction != truth):
    #         print "==================================="
    #         print "Mistake on example %d" % i
    #         print "Predicted %d; truth is %d" % (prediction, truth)
    #         print "Image: "
    #         print_digit(trainData[i,:])


## =====================
## You don't have to modify any code below.
## =====================

def print_features(features):
    str = ''
    width = DIGIT_DATUM_WIDTH
    height = DIGIT_DATUM_HEIGHT
    for i in range(width):
        for j in range(height):
            feature = i*height + j
            if feature in features:
                str += '#'
            else:
                str += ' '
        str += '\n'
    print(str)

def print_digit(pixels):
    width = DIGIT_DATUM_WIDTH
    height = DIGIT_DATUM_HEIGHT
    pixels = pixels[:width*height]
    image = pixels.reshape((width, height))
    datum = samples.Datum(samples.convertToTrinary(image),width,height)
    print(datum)

def _test():
    import datasets
    train_data = datasets.tinyMnistDataset()[0]
    for i, datum in enumerate(train_data):
        print_digit(datum)

if __name__ == "__main__":
    _test()
