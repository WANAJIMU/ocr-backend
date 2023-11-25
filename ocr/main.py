import cv2
import PIL from Image
import pytesseract

# open up an image
im_file = 'data/cert1.jpg'
im  = Image.open(im_file)

# print(im)
# print(im.size)

# show image
# im.show()

# save image
im.save('temp/cert.jpg')