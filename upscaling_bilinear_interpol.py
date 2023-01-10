#!/usr/bin/python3
import inspect 
from numpy import *
from lib_interpolate import *
from PIL import Image, ImageDraw

#########################
# FUNCTION
#########################
def upcaling(filename,upscale_value):
    with Image.open(filename) as im:
        #im.rotate(45).show()
        #im.show()

        upscale_im_size = (im.size[0]*upscale_value,im.size[1]*upscale_value)
        upscale_im = Image.new('RGBA', upscale_im_size, (255,255,255,255))

        #upscale_im.show()
        #symbol_img.save(out_dir+'symbol.png')

        for y in range(upscale_im_size[1]):
            for x in range(upscale_im_size[0]):

                if x%upscale_value == 0 and y%upscale_value == 0:
                    tmp_pixel = ( im.getpixel((int(x/upscale_value),int(y/upscale_value)))[0],im.getpixel((int(x/upscale_value),int(y/upscale_value)))[1],im.getpixel((int(x/upscale_value),int(y/upscale_value)))[2], 255 )
                    upscale_im.putpixel((x,y),tmp_pixel)
                else:
                    tmp_pixel = bilinear_interpolation(x,y,x/upscale_value,y/upscale_value,im)
                    upscale_im.putpixel((x,y),tmp_pixel)

        upscale_im.show()
        upscale_im.save(os.path.splitext(filename)[0]+"_bilinear_interpol_x"+str(upscale_value)+os.path.splitext(filename)[1])

#########################
# CREATE IMG
#########################
upcaling("tiger.png",8)
