from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import PIL
import re
import mosaic
from image import *
from collage import *
bgColor = "light blue"
fontColor = "white"


window = Tk()


window.title("Python Image Processing Project - Family Portrait")
window.configure(background=bgColor)

# Title
Label (window, text="Welcome to FamCollage!", font="none 15 bold").grid(row=0, column=0, sticky=W+E)

# Header image
photo1 = ImageTk.PhotoImage(Image.open("img/mosaic_img/tiles/kevin-1.png").resize((500, 125)))
Label (window, image=photo1, bg=bgColor).grid(row=1, column=0, sticky=W+E)

# Text section
Label (window, text="Calling all families in need of a memorable portrait frame...", bg=bgColor, fg=fontColor, font="none 14 italic").grid(row=2, column=0, sticky=W)

Label (window, text="Image Collage:",bg=bgColor, fg=fontColor, font="none 14 bold").grid(row=4, column=0, sticky="W")
Label(window,text="Start by choosing a MASK IMAGE. \nThen, select your set of collaged images (requires 1 or more images).\nNext, select the density, scale, assortment, and angle \nat which you wish to set your collage.\nFinally, select a frame for your program.",bg=bgColor, fg=fontColor,font="none 12",justify=LEFT).grid(row=4,column=1)

Label (window, text="Photomosaic:", bg=bgColor, fg=fontColor,font="none 14 bold").grid(row=5, column=0, sticky="W")
Label(window,text="Start by choosing a MAIN IMAGE. \nThen, select your set of collaged images (requires 1 or more images).\nNext, select the tile size of each tiled image (smaller = higher res).\nFinally, select a frame for your program.",bg=bgColor, fg=fontColor,font="none 12",justify=LEFT).grid(row=5,column=1)

Label (window, text="Wordcloud Mask:",bg=bgColor, fg=fontColor, font="none 14 bold").grid(row=6, column=0, sticky="W")
Label(window,text="Start by choosing a MASK IMAGE. \nThen, select your set of collaged images (requires 1 or more images).\nFinally, select a frame for your program.",bg=bgColor, fg=fontColor,font="none 12",justify=LEFT).grid(row=6,column=1)

# Allow user to choose program to use
Label(window, text='Which program would you like to use?', bg=bgColor, fg=fontColor, font="none 12 bold").grid(row=7, column=0, sticky=W) 


#Select dropdown
programChoice = [
    'Image Collage',
    'Photomosaic',
    'Wordcloud Mask'
    ]

# Option selecter (For dropdown)
optionSelect = StringVar(window)
optionSelect.set(programChoice[0])

w = OptionMenu(window, optionSelect, *programChoice)
w.grid(row=7, column=1, sticky=W, pady=10)
    
# Browse files
textFilename = ''
textFilenameWordcloud = ''
updateFolder = ''

# Open file for single image (main image/mask)
def askopenfile():
    global my_image
    global textFilename
    window.filename = filedialog.askopenfile(initialdir="/", title="Select A File")
    textFilename = str(window.filename).split("'")[1] # Adjust program to only cut out the filename
    my_label = Label(window, text=str(window.filename).split("'")[1]).grid(row=10, column=3, sticky=W)
    try:
        my_image = ImageTk.PhotoImage(Image.open(window.filename))
        
    except:
        pass
# Open file for wordcloud image
def askopenfilewordcloud():
    global my_image
    global textFilenameWordcloud
    window.filename = filedialog.askopenfile(initialdir="/", title="Select A File")
    textFilenameWordcloud = str(window.filename).split("'")[1] # Adjust program to only cut out the filename
    my_label = Label(window, text=str(window.filename).split("'")[1]).grid(row=12, column=3, sticky=W)
    try:
        my_image = ImageTk.PhotoImage(Image.open(window.filename))
        
    except:
        pass

# Open folder that contains multiple images (image collage and photomosaic)
def askopenfiles():
    global my_image2
    global updateFolder
    window.filename = filedialog.askdirectory(initialdir="/", title="Select File(s)")
    updateFolder =  str(window.filename) + "/*"
    my_label = Label(window, text=window.filename).grid(row=15, column=3, sticky=W)
    try:
        my_image2 = ImageTk.PhotoImage(Image.open(window.filename))
        
    except:
        pass


# Label section

Label (window, text="Please select your main/mask image: ", 
       bg=bgColor, fg=fontColor, font="none 12 bold").grid(row=10, column=0, sticky=W)
Label (window, text="(FOR WORDCLOUD MASK ONLY) Please select your wordcloud image: ", 
       bg=bgColor, fg=fontColor, font="none 12 bold").grid(row=12, column=0, sticky=W)
Label (window, text="(FOR PHOTOMOSAIC AND IMAGE COLLAGE ONLY) Please select your image set: ", 
       bg=bgColor, fg=fontColor, font="none 12 bold").grid(row=15, column=0, sticky=W)

# Browse entries button
browseButton1 = Button(window, text="Browse", command=askopenfile)
browseButton1.grid(row=10, column=1, sticky="W")
browseButtonWordcloud = Button(window, text="Browse", command=askopenfilewordcloud)
browseButtonWordcloud.grid(row=12, column=1, sticky="W")
browseButton2 = Button(window, text="Browse", command=askopenfiles)
browseButton2.grid(row=15, column=1, sticky="W")


# Density
Label (window, text="(FOR IMAGE COLLAGE ONLY) Please select the density%:\nNote: >= 90 recommended", bg=bgColor, fg=fontColor, font="none 12 bold").grid(row=26, column=0, sticky="W")
density = Scale(window, from_=1, to=100, orient=HORIZONTAL)
density.grid(row=26,column=1,sticky=W)

# Scale
Label (window, text="(FOR IMAGE COLLAGE ONLY) Please select the scale:", bg=bgColor, fg=fontColor, font="none 12 bold").grid(row=27, column=0, sticky="W")
scale = Scale(window, from_=1, to=100, orient=HORIZONTAL)
scale.grid(row=27,column=1,sticky=W)


# Cutoff
cutoff = ['True', 'False']
Label (window, text="(FOR IMAGE COLLAGE ONLY) Please select the cutoff:", bg=bgColor, fg=fontColor, font="none 12 bold").grid(row=28, column=0, sticky="W")
optionSelectCutoff = StringVar(window)
optionSelectCutoff.set(cutoff[0])

cutoffMenu = OptionMenu(window, optionSelectCutoff, *cutoff)
cutoffMenu.grid(row=28, column=1, sticky=W)

# Assortment
assortment = ['square', 'random']
Label (window, text="(FOR IMAGE COLLAGE ONLY) Please select the assortment:", bg=bgColor, fg=fontColor, font="none 12 bold").grid(row=29, column=0, sticky="W")
optionSelectAssortment = StringVar(window)
optionSelectAssortment.set(assortment[1])

assortmentMenu = OptionMenu(window, optionSelectAssortment, *assortment)
assortmentMenu.grid(row=29, column=1, sticky=W)

# Angle adjust
Label (window, text="(FOR IMAGE COLLAGE ONLY) Please select your collage angle (none=0):", bg=bgColor, fg=fontColor, font="none 12 bold").grid(row=30, column=0, sticky="W")
angle = Scale(window, from_=0, to=360, orient=HORIZONTAL)
angle.grid(row=30, column=1, sticky=W)

# Tile size
Label (window, text="(FOR PHOTOMOSAIC ONLY) Please select your tile size:", bg=bgColor, fg=fontColor, font="none 12 bold").grid(row=31, column=0, sticky="W")
z = Scale(window, from_=1, to=100, orient=HORIZONTAL)

z.grid(row=31, column=1, sticky=W)

# Frame
programChoiceFrame = [
    'gold',
    'neon',
    'flower'
]
    

# Option selecter (For dropdown)
Label (window, text="Please select the frame you would like to apply to your image:", bg=bgColor, fg=fontColor, font="none 12 bold").grid(row=35, column=0, sticky="W")
optionSelectFrame = StringVar(window)
optionSelectFrame.set(programChoiceFrame[0])

w = OptionMenu(window, optionSelectFrame, *programChoiceFrame)
w.grid(row=35, column=1, sticky=W, pady=10)

# Create button
def createImg():
    imgProgram = optionSelect.get()

    #run if-elif-else chain based on which program user selects
    if imgProgram == "Image Collage":
        addFrame(generate_random_collage(updateFolder, textFilename, density.get(), scale.get(), cutOff = (optionSelectCutoff.get() == "True"), assortment = optionSelectAssortment.get(), angle = angle.get()))
            
        
    elif imgProgram == "Photomosaic":
        # createMosaic returns a PIL image, which also runs through addFrame
        photoMosaic = mosaic.createMosaic(textFilename, updateFolder, z.get())
        addFrame(photoMosaic)

    else:
        # createWordcloud also returns a PIL image, which will run through addFrame
        wordCloud = createWordcloud(textFilename, textFilenameWordcloud)
        addFrame(wordCloud)
        
def addFrame(im):
    # get a PIL image as input and, based on what frame was selected, apply a different frame and save to file - "finalResult.png"
    if optionSelectFrame.get() == "gold":
        add_border(im, "gold").save('finalResult.png')
    elif optionSelectFrame.get() == "neon":
        add_border(im, "neon").save('finalResult.png')
    elif optionSelectFrame.get() == "flower":
        add_border(im, "flower").save('finalResult.png')
        
# Create button
createProject = Button(window, text="Create!", command=createImg).grid(row=50, column=1,sticky="w")

window.mainloop()

