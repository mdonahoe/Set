import Image
import os

def first_visible_pixel(image,forward=True,horizontal=True):
    """Scan the image along a dominant direction
    until a visible pixel is found. Return that coordinate"""
    width,height = image.size
    first, second = (width,height) if horizontal else (height,width)
    firsts = range(first)
    if not forward: firsts.reverse()
    seconds = range(second)
    for i in firsts:
        for j in seconds:
            pt = (i,j) if horizontal else (j,i)
            r,g,b,a = image.getpixel(pt)
            if a: return i
    return first

def crop_invisible(image):
    # Find the edges of the drawing so we can crop
    f = first_visible_pixel
    left   = f(image)
    top    = f(image, horizontal=False)
    right  = f(image, forward=False) + 1
    bottom = f(image, forward=False, horizontal=False) + 1
    box = (left, top, right, bottom)
    return image.crop(box)

def double(im):
    """
    given an image, create two, centered
    """
    W,H = im.size
    im = crop_invisible(im)
    w,h = im.size
    a = (W - 2 * w) // 3
    b = (H - h) // 2
    out = Image.new('RGBA', (W,H),(0,0,0,0))
    out.paste(im,(a,b))
    out.paste(im,(2 * a + w, b))
    return out

def triple(im):
    """
    given an image, create three, centered
    """
    W,H = im.size
    out = Image.new('RGBA', (W,H),(0,0,0,0))
    im = crop_invisible(im)
    w,h = im.size
    # create the bottom two first
    a = (W - 2 * w) //3
    b = (H - 2 * h) // 3
    c = 2 * b + h
    out.paste(im,(a,c))
    out.paste(im,(2 * a + w, c))
    # then the top one
    d = (W - w) // 2
    out.paste(im,(d,b))
    return out

def genall():
    # get images
    images = os.listdir('src')
    print images
    for image in images:
        im = Image.open('src/' + image)
        basename = 'gen/' + image.replace('.png', '')
        im.save(basename + '1.png')
        double(im).save(basename + '2.png')
        triple(im).save(basename + '3.png')

if __name__ == '__main__':
    genall()
