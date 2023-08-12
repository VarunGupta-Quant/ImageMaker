import matplotlib.pyplot as plt                                     # Import libraries
import os.path
import numpy as np
from PIL import Image

def createWordcloud(file, wordCloud):                                          # Take in strings for names of files
    directory = os.path.dirname(os.path.abspath(__file__))          # Setup for file names
    filename = os.path.join(directory, file)
    wordCloudName = os.path.join(directory, wordCloud)

    image = Image.open(filename)
    image = image.convert('RGBA')                                   # Create image that uses RGBA
    
    imageArr = np.array(image)
    x = len(imageArr)                                               # Create variables for array size
    y = len(imageArr[0])

    cloud = Image.open(wordCloudName)                               # Opens wordcloud
    result = cloud.convert('RGBA')
    
    resultArr = np.array(result)                                    # Creates array for output image
    w = len(resultArr)
    z = len(resultArr[0])

    colRatio = z / y                                                # Determines ratio of dimensions
    rowRatio = w / x                                                # of image to wordcloud
    imageRatio = min(colRatio, rowRatio)

    scaledImage = image.resize( (int(y * imageRatio), int(x * imageRatio)) )
    
    transparentImage = Image.new('RGBA', (z, w), color = 0)
    transparentImage.paste(scaledImage, (int((z - y * imageRatio)/2), int((w - x * imageRatio)/2)) )
    #transparentImage.save('image.png')
    
    transImgArr = np.array(transparentImage)
    

    for r in range(z):                                              # Iterate through pixels
        for c in range(w):                                          # to find which are transparent
                if (transImgArr[c][r][3] < 50 or sum(transImgArr[c][r]) > 950):
                    resultArr[c][r] = [0, 0, 0, 255]
    
    result = Image.fromarray(resultArr, 'RGBA')                     # Use modified numpy array to alter image
    return result                                       # Outputs image to .png file format
