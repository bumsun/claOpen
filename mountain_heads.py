import shutil
import requests
import cv2
import numpy as np
import glob
from PIL import Image
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

lat = "40.702147"
lon = "-74.015794"
for zoom in range(1, 20): 
    response = requests.get("https://maps.googleapis.com/maps/api/staticmap?zoom=" + str(zoom) + "&size=1200x1200&maptype=satellite&markers=color:blue%7Clabel:S%7C" + lat + "," + lon + "&key=AIzaSyDJrwFDlj0KxrgP6W91C08IhDNJ1Zr8ANA", stream=True)
    with open('loaded_images/' + str(zoom) + '.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def rounded_rectangle(draw, xy, rad, fill=None):
    x0, y0, x1, y1 = xy
    draw.rectangle([ (x0, y0 + rad), (x1, y1 - rad) ], fill=fill)
    draw.rectangle([ (x0 + rad, y0), (x1 - rad, y1) ], fill=fill)
    draw.pieslice([ (x0, y0), (x0 + rad * 2, y0 + rad * 2) ], 180, 270, fill=fill)
    draw.pieslice([ (x1 - rad * 2, y1 - rad * 2), (x1, y1) ], 0, 90, fill=fill)
    draw.pieslice([ (x0, y1 - rad * 2), (x0 + rad * 2, y1) ], 90, 180, fill=fill)
    draw.pieslice([ (x1 - rad * 2, y0), (x1, y0 + rad * 2) ], 270, 360, fill=fill)
    
img_array = []
index = 1
for filename in glob.glob('loaded_images/*.png'):
    
    img = cv2.imread('loaded_images/' + str(index) + '.png')
    print('loaded_images/' + str(index) + '.png')
    height, width, layers = img.shape
    size = (width,height)
    
    if index < 19:
        for x in range(1, 20):
            alpha_photo = Image.open('loaded_images/' + str(index) + '.png')
            bg = Image.open('loaded_images/' + str(index+1) + '.png')
            alpha_photo.putalpha(256)
            bg.putalpha(256)
            calc_alpha = x/20.0
            result = Image.blend(alpha_photo, bg, alpha=calc_alpha)
            

#             mask = Image.new('L', result.size, 0)
#             draw = ImageDraw.Draw(mask)
#             rounded_rectangle(draw, (result.size[0]//4, result.size[1]//4, result.size[0]//4*3, result.size[1]//4*3), rad=40, fill=255)
#             blurred = result.filter(ImageFilter.GaussianBlur(20))
#             result.paste(blurred, mask=mask)
            
            open_cv_image = np.array(result.convert('RGB')) 
            open_cv_image = open_cv_image[:, :, ::-1].copy() 
            img_array.append(open_cv_image)
    index = index + 1
 
 
out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 60, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
