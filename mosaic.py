import glob
from PIL import Image
from scipy import spatial
import numpy as np

def createMosaic(main_filepath, tile_photos, tile_size):
    main_filepath = main_filepath
    tile_photos = tile_photos
    tile_size = (tile_size, tile_size) # specify size of each image within photomosaic: 25 x 25 pixels

    # Get every tile inside tiles folder
    tile_paths = []
    for file in glob.glob(tile_photos):
        tile_paths.append(file)


    tiles = []
    for tile in tile_paths:
        im = Image.open(tile)
        
        width, height = im.size # get width and height properties
        im1 = im.crop((0, 0, width, width)) # crop image so that it fits into square shape (decided to crop from bottom because face is on top)
        im1 = im1.resize(tile_size) # resize image to 25 x 25 pixels
        tiles.append(im1)

    colors = []

    for tile in tiles:
        mean_color = np.array(tile).mean(axis=0).mean(axis=0)
        colors.append(mean_color)

    # Pixelate main photo, resizing it to get the corresponding average color values
    main_photo = Image.open(main_filepath)
    width = int(np.round(main_photo.size[0] / tile_size[0]))
    height = int(np.round(main_photo.size[1] / tile_size[1]))

    resize_photo = main_photo.resize((width, height))

    updatedTiles = []
    # Mask filter
    for x in range(width):
        for y in range(height):
            pixel = resize_photo.getpixel((x, y))
            pixel = list(pixel)
            pixel[-1] = 126
            pixel = tuple(pixel)
            img = Image.new('RGBA', (tile_size[0], tile_size[1]), pixel)
            updatedTiles.append(img)

    # Use a k-d tree to find main_photo's closest tile photo for every pixel (based on average color)
    #Create KDtree
    tree = spatial.KDTree(colors)

    closest_tiles = np.zeros((width, height), dtype=np.uint32)

    for x in range(width):
        for y in range(height):
            pixel = resize_photo.getpixel((x, y)) # pixel color at (x, y) of pixelated main_photo
            closest = tree.query(pixel)
            closest_tiles[x, y] = closest[1]
            
    output = Image.new('RGB', main_photo.size)
    q = 0
    for x in range(width):
        for y in range(height):
            
            a, b = x*tile_size[0], y*tile_size[1]
            index = closest_tiles[x, y]
            #newImg = Image.new('RGBA', (tile_size[0], tile_size[1]), (255, 0, 0, 50))
            im3 = Image.blend(tiles[index], updatedTiles[q], 0.5)
            
            
            output.paste(im3, (a, b))   
            q += 1
    return output
     