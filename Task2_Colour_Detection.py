#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 04:59:58 2021

@author: Swetha Sundari Vellaluru
Project 2: COLOUR DETECTION USING OPENCV
DEVSTACK SOLUTION INTERNSHIP
"""

"""
Colour detection identifies the images and its pixels that will match the colour and its range. 
So when we click on the colour, it will display the colour name, and R,G,B code. 
"""
#argparse is used for command line parsing
import argparse

#pandas is used for data analysis, here we are using for reading data, numerous data
import pandas as pd

#cv2 is nothing but opencv used for image processing, like face detection.
#here it performs the colour detection and returns the colour that is selected
import cv2


#initialising clicked as False
clicked_function = False
#now setting the RGB colours and xpos and ypos to 0
red = green = blue = xpos = ypos = 0

#REFERENCE : https://docs.python.org/3/howto/argparse.html
#the argument parser is used to command line parsing using the module
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('-i','--image',required=True, help= "Image Path")
args1 = vars(argument_parser.parse_args())
images_path1 = args1['image']

#loading image from the file and storing it in images
images_dim = cv2.imread(images_path1)

#dimensions of the image is given
dimensions_image = images_dim.shape
#height and width of the image is specified
height_image = images_dim.shape[0]
width_image = images_dim.shape[1]
#area of the image is specified
area_image = height_image*width_image

#looking at the dataset there are 6 columns and providing them a header
columns = ['colour','colourname','hexa_code','RED', 'BLUE', 'GREEN']

#reading the dataset using Pandas, by giving the column names, and header as None
data = pd.read_csv('colors.csv', names = columns, header = None)

#function to get the matching colour and also calculate the minimum distance
def get_colour_names(RED, BLUE, GREEN):
    #function that accepts infinity in lower and upper cases
    min = float('inf')
    #calling the colour name
    colour_name = ""
    #looping through the data and consider the RED,BLUE, GREEN values
    for j in range(len(data)):
        colours_data = abs(RED - int(data.loc[j, "RED"])) + abs(GREEN - int(data.loc[j, "GREEN"])) + abs(BLUE - int(data.loc[j, "BLUE"]))
        if colours_data <= min:
            min = colours_data
            colour_name = data.loc[j, "colourname"]
    return colour_name



#function to obtain the co ordinates i.e  x and y with the click
def draw_function(event1, x, y, flags, param):
    #leftbuttondown for every click
    if event1 == cv2.EVENT_LBUTTONDOWN:
        #declaring the global variables
        global blue, green, red, xpos, ypos, clicked_function
        clicked_function = True
        xpos = x
        ypos = y
        # x and y co-ordinates are passing to blue, green and red
        blue, green, red = images_dim[y, x]
        blue = int(blue)
        green = int(green)
        red = int(red)
        
if area_image<=662000:
    #image is passed to the namedwindow- it creates a window for videos and images
    cv2.namedWindow('image')
else:
    #creating window with the dimensions
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
 #setmousecallback uses opencv with events and coordinates
cv2.setMouseCallback('image', draw_function)

#reference : https://docs.opencv.org/3.4/db/d5b/tutorial_py_mouse_handling.html
while(1):
    #imshow fits the images to the size of the window, showing the image
    cv2.imshow("image", images_dim)
    #once we click on the image, the following operations start to perform
    if clicked_function:

        #providing the width and height of the display text when the output is clicked
        rec_end = (round(width_image*.745),round(height_image*.1))
        text_display = (round(width_image*.03),round(height_image*.08))

        #the text appears in the rectangle, and also setting the thickness to -1
        cv2.rectangle(images_dim, (20, 20), rec_end, (blue, green, red), -1)

        # Creating text string to display( Color name and RGB values )
        colour_text = get_colour_names(red, green ,blue) + ' RED=' + str(red) + ' GREEN=' + str(green) + ' BLUE=' + str(blue)

        # For very light colours we will display text in black colour
        #if the rgb colours are greater than 600, when we click on the colour, the text appears in black or white
        if red + green + blue >= 600:
            cv2.putText(images_dim, colour_text,text_display, cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0, 0, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(images_dim, colour_text, text_display, cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (255,255,255), 2, cv2.LINE_AA)
        #setting the clicked function to False
        clicked_function = False

    #when we click on esc key, the window closes.
    #0.FF is the code for ESC key
    if cv2.waitKey(20) & 0xFF == 27:
        break

#we use destroy the windows to close the output.
cv2.destroyAllWindows()