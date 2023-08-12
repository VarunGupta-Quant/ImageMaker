import glob
import matplotlib as plt
from matplotlib.pyplot import contour
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math
import random
import itertools
from cv2 import cv2

def generate_random_collage(images, mask, density, scale, border = 'color', borderColor = 0, borderSize = 0, cutOff = False, assortment = 'random', angle = 45):
    '''
    Generates a collage with a random assortment of images given

    images contains the list of images
    density specifies how close the images are placed
    scale determines how large the images are
    border, borderColor, borderSize specifies parameters of the border / frame of each pasted image
    cutOff describes if the images will be cleanly cutoff at the edges of the mask
    assortment determines if the pasted images will be rotated or not
    angle determines the bounds of the degree value of rotation if assortment = 'random'

    Returns final collage image
    '''
    mask = Image.open(mask)
    width, height = mask.size
    
    # creating lattice points and distance between them to paste pictures onto
    latticePoints, xdist, ydist = generate_lattice_points(width, height, density/100)

    # background to paste onto
    background = Image.new('RGBA', (width, height), (0,0,0,0))

    if(not cutOff): # checks parameter
        latticePoints = points_Contour(latticePoints, mask) 
        # removes lattice points outside of contour

    high = int(math.floor(scale * max(xdist, ydist)))

    
    imagesUpdated = []
    for file in glob.glob(images):
        imagesUpdated.append(Image.open(file))
    images = imagesUpdated

    if(assortment == 'random'):

        for point in latticePoints:
            deg = random.randint(-1 * angle, angle) # generates random angle withing bounds  
            background = image_Paster(point, images, background, high, border, borderColor, borderSize, deg)

    else:

        for point in latticePoints: 
            background = image_Paster(point, images, background, high, border, borderColor, borderSize)


    if(cutOff):    

        # white background
        templatePaste = Image.new('RGBA', background.size, (0,0,0,0))

        # masks the final image
        background = Image.composite( background, templatePaste, mask )

    return background



def generate_lattice_points(width, height, density):
    '''
    Create lattice points in the image depending on the given 
    density parameter, describing points and locations to paste the 
    given images into

    Returns list of lattice points and distances between them
    '''
    
    # finds number of points per row and column
    numOfPoints = int ( math.floor ( 1 / (1 - density) ) )
    xdist = width / numOfPoints
    ydist = height / numOfPoints

    x = []
    y = []

    for i in range(numOfPoints+1):
        x.append( int( math.floor( i * xdist ) ) )
        y.append( int( math.floor( i * ydist ) ) )
    
    # cartesian product of x and y coordinates
    latticePoints = list(itertools.product(x, y))
    
    return latticePoints, xdist, ydist



def add_border(im, type = 'color', borderColor = (255,255,255,0), borderSize = 0):
    '''
    Adds a border to the given image
    type specifies which frame is used
    borderColor specifies the color fo the frame if type = 'color'
    borderSize specifies proportion of border width if type = 'color'

    Returns image with border
    '''
    if(type == 'color'): 
        # set width, height, and proportional border sizes
        width, height = im.size
        borderWidth = int(math.floor(borderSize * width)) # left and right border width
        borderHeight = int(math.floor(borderSize * height)) # top and bottom border width

        # white background to paste on    
        border = Image.new('RGBA', im.size, borderColor)

        # draws the black border on the mask
        mask = Image.new('L', im.size, 255)
        draw = ImageDraw.Draw(mask)
        draw.line([(0,0), (0, height)], fill=0, width = borderWidth)
        draw.line([(0,0), (width, 0)], fill=0, width = borderHeight)
        draw.line([(width,0), (width, height)], fill=0, width = borderWidth)
        draw.line([(0,height), (width, height)], fill=0, width = borderHeight)

        # composites the white background onto the image
        # based on the black border of the mask
        im = Image.composite( im, border, mask )

    elif(type == 'gold'):
        gold = Image.open('goldframe.png').resize(im.size)
        im.paste(gold, (0,0), gold)        

    elif(type == 'neon'): 
        block = Image.open('neonframe.png').resize(im.size)
        im.paste(block, (0,0), block)

    elif(type == 'flower'): 
        flower = Image.open('flowerframe.png').resize(im.size)
        im.paste(flower, (0,0), flower)

    return im



def mask_To_Countor(mask): 
    '''
    Receives an input PIL Image mask as an argument
    Converts and returns it as a contour for use in cv libraries

    Returns mask as list of contours
    '''

    # Converting PIL Image to a greyscale cv image
    pil_im = mask.convert('RGB')
    cv_im = np.array(pil_im)
    cv_im = cv_im[:, :, ::-1].copy() 
    img_gray = cv2.cvtColor(cv_im, cv2.COLOR_BGR2GRAY)

    # binary thresholding for easier detection
    # apply binary thresholding
    ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    # visualize the binary image
    cv2.imwrite('image_thres1.jpg', thresh)

    contour, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(cv_im, contour, -1, (0,255,0), 3)
    # cv2.imshow('contour', cv_im)
    cv2.imwrite('contour.jpg', cv_im)

    # Extracting contour from cv image
    
    return contour, cv_im



def points_Contour(latticePoints, mask): 
    '''
    Takes in a list of points and a mask
    Removes all lattice points outside of the mask
    Returns the modified array
    '''
    
    # convert mask to contour
    contour, cv_im = mask_To_Countor(mask)

    modifiedLattice = []

    # iterating through all contours except for border contour
    for i in range(1, len(contour)):

        j = 0 # counter
            
        while(j < len(latticePoints)):
            # if point is outside contour
            if(cv2.pointPolygonTest(contour[i], latticePoints[j], False) != -1):
                cv2.circle(cv_im, latticePoints[j], 8, (255,100,100), -1) # draw red circle
                modifiedLattice.append(latticePoints.pop(j)) # remove from array
            else: 
                cv2.circle(cv_im, latticePoints[j], 8, (100,100,255), -1) # draw blue circle
                j+=1 # move to next element in array
        
        cv2.imwrite('contour_points.jpg', cv_im)
        cv2.destroyAllWindows()
    
    return modifiedLattice



def image_Paster(point, images, background, size, border, borderColor, borderSize, deg = 0): 
    '''
    Pastes images onto the background with the given parameters
    
    latticePoints specifies point to paste onto
    images specifies list of images to select from
    background specifies image to paste on
    size specifies dimensions of the pasted image
    border, borderColor, borderSize specifies parameters of add_border()
    deg specifies the angle at which the point is pasted
    '''

    index = random.randint(0, len(images)-1) # randomizes the image selected

    # resizing and rotating image
    im = images[index]
    im = im.resize((size, size)) # resizes to manageable square size
    im = add_border(im, border, borderColor, borderSize) # adds border
    im_mask = Image.new('L', im.size, 255)
    im = im.rotate(deg, expand=True)
    im_mask = im_mask.rotate(deg, expand=True)
        
    # pastes image onto background
    background.paste( im, point, im_mask )

    return background
