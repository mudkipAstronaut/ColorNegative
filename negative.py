from PIL import Image
from PIL import ImageChops
import numpy as np

def get_colors(imgPIL, numcolors=4, resize=150):
    # Resize image to speed up processing
    img = imgPIL.copy()
    img.thumbnail((resize, resize))

    # Reduce to palette
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=numcolors)

    # Find dominant colors
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    colors = list()
    for i in range(numcolors):
        palette_index = color_counts[i][1]
        dominant_color = palette[palette_index*3:palette_index*3+3]
        colors.append(tuple(dominant_color))

    #after the dominant colors have been indentified find
    #the closest to cyan
    cyan = (55,140,195)

    domCyan = (0,0,0)
    curr = colors[0]
    for color in colors:
        if( tuple(np.absolute(np.subtract(cyan, color))) < tuple(np.absolute(np.subtract(cyan, curr))) ):
            curr = color

    #color that we need to subtract to the image
    return curr

if __name__=="__main__":
    path = "/home/andres/Pictures/film/IMG_0326.jpg"

    img = Image.open(path, 'r')
    newimg = img.copy()
    pixs = newimg.load()

    """
    #color inversion
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            #iterate through every pixel
            sub = tuple(map(lambda a,b: a-b, (255,255,255), pixs[i,j]))
            pixs[i,j] = sub
    """

    #PIL has a invert function
    newimg = ImageChops.invert(newimg)
    
    print("Finished inverting the image")

    #subtraction
    subMask = get_colors(newimg)

    #apply the mask

    """
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            #iterate through every pixel
            sub = tuple(map(lambda a,b: a-b, pixs[i,j], subMask))
            pixs[i,j] = sub
    """

    #PIL has a subtract function
    colMask = Image.new('RGB', (newimg.size[0], newimg.size[1]), subMask)
    newimg = ImageChops.subtract(newimg, colMask)
    
    print("Finished extracting the color and subtracting")
    
    newimg.save("inverted.jpg")
