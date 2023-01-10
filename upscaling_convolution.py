#!/usr/bin/python3
import inspect
from numpy import *
from lib_interpolate import *
from PIL import Image, ImageDraw

#########################
# FUNCTION
#########################
def upcaling(filename,upscale_value):
    filter_size = 2 #6 #4 
    filter_fct  = nearest_neighbor_fct #better_quadratic_fct #lanczos_fct #smoothed_quadratic_fct   #bicubic_fct
    filter_name = "nearest_neighbor_fct" #"better_quadratic_fct" #"lanczos_fct" #"smoothed_quadratic_fct" #"bicubic_fct"

    with Image.open(filename) as im:
        # Create new img
        x_upscale_im_size = (im.size[0]*upscale_value,im.size[1])
        x_upscale_im      = Image.new('RGBA', x_upscale_im_size, (255,255,255,255))

        # Calc coordinates
        upscale_coordinates = list()
        calc_coordinates    = list()
        for y in range(x_upscale_im_size[1]):
            for x in range(x_upscale_im_size[0]):
                x_ = x / (upscale_value + 0.0)
                upscale_coordinates.append((x ,y))
                calc_coordinates.append((x_,y)) 

        # X interpolation
        for i, coordinate in enumerate(calc_coordinates):
            x,y   = upscale_coordinates[i]
            x_,y_ = coordinate

            # Calc frac
            x_frac = x_ - int(x_)
            y_frac = y_ - int(y_)

            # Skip y pixel to modify
            if y_frac != 0.0:
                continue

            # Ignore true pixel
            if x_frac == 0.0:
                tmp_pixel = im.getpixel((x_,y_))
                tmp_pixel = (tmp_pixel[0],tmp_pixel[1],tmp_pixel[2],255)
                x_upscale_im.putpixel((x,y),tmp_pixel)
                continue

            # Get coeffs
            conv_coeffs = convolution_get_coeffs(x_frac,filter_size,filter_fct)
            conv_pixels = convolution_get_pixels(int(x_),y_,im,filter_size,axis="x")

            # Convolution 1d
            tmp_pixel = convolution_1d_fct(conv_coeffs,conv_pixels)
            
            # Restore alpha
            tmp_pixel = (tmp_pixel[0],tmp_pixel[1],tmp_pixel[2],255)

            # Cast values
            tmp_pixel = tuple_cast(tmp_pixel)

            # Set pixel
            x_upscale_im.putpixel((x,y),tmp_pixel)


        # Create new img
        upscale_im_size   = (im.size[0]*upscale_value,im.size[1]*upscale_value)
        upscale_im        = Image.new('RGBA', upscale_im_size, (255,255,255,255))

        # Calc coordinates
        upscale_coordinates = list()
        calc_coordinates    = list()
        for y in range(upscale_im_size[1]):
            for x in range(upscale_im_size[0]):
                y_ = y / (upscale_value + 0.0)
                upscale_coordinates.append((x ,y))
                calc_coordinates.append((x,y_)) 

        # Y interpolation
        for i, coordinate in enumerate(calc_coordinates):
            x,y   = upscale_coordinates[i]
            x_,y_ = coordinate

            # Calc frac
            x_frac = x_ - int(x_)
            y_frac = y_ - int(y_)

            # Ignore true pixel
            if y_frac == 0.0:
                tmp_pixel = x_upscale_im.getpixel((x_,y_))
                tmp_pixel = (tmp_pixel[0],tmp_pixel[1],tmp_pixel[2],255)
                upscale_im.putpixel((x,y),tmp_pixel)
                continue

            # Get coeffs
            conv_coeffs = convolution_get_coeffs(y_frac,filter_size,filter_fct)
            conv_pixels = convolution_get_pixels(x_,int(y_),x_upscale_im,filter_size,axis="y")

            # Convolution 1d
            tmp_pixel = convolution_1d_fct(conv_coeffs,conv_pixels)
            
            # Restore alpha
            tmp_pixel = (tmp_pixel[0],tmp_pixel[1],tmp_pixel[2],255)

            # Cast values
            tmp_pixel = tuple_cast(tmp_pixel)

            # Set pixel
            upscale_im.putpixel((x,y),tmp_pixel)

        #x_upscale_im.show()
        upscale_im.show()
        upscale_im.save(os.path.splitext(filename)[0]+"_"+str(filter_name)+"_x"+str(upscale_value)+os.path.splitext(filename)[1])

#########################
# CREATE IMG
#########################
upcaling("tiger.png",8)
