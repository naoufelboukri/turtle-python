import cv2
import numpy as np
import sys
import turtle

def big_fernand_with_blur(pathFile, intensity):
    turtle.speed(0)
    image = cv2.imread(pathFile)
    rows, columns, channels = image.shape
    turtle.setup(columns, rows)
    blurred_img = cv2.blur(image,ksize=(intensity, intensity))
    gray_image = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)
    median_pix = np.median(gray_image)
    lower = max(0 ,0.25*median_pix)
    upper = int(min(255,0.75*median_pix))
    edges = cv2.Canny(image=blurred_img, threshold1=lower,threshold2=upper)
    ret, thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)
    for y in range(rows):
      for x in range(columns):
        pixel = float(thresh[y, x])
        turtle.penup()
        turtle.goto(x, rows - y)
        turtle.dot(1, (pixel / 255, pixel / 255, pixel / 255))
        turtle.update()

def big_fernand(pathFile):
    image = cv2.imread(pathFile)
    rows, columns, channels = image.shape
    turtle.setup(columns, rows)
    turtle.pensize(10)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    median_pix = np.median(gray_image)
    lower = int(max(0 ,0.25*median_pix))
    upper = int(min(255,0.75*median_pix))
    edges = cv2.Canny(image, threshold1=lower,threshold2=upper)
    ret, thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)
    for y in range(rows):
      for x in range(columns):
        pixel = thresh[y, x]
        turtle.penup()
        turtle.goto(x, rows - y)
        turtle.pendown()
        turtle.dot(1, (pixel / 255, pixel / 255, pixel / 255))
        turtle.update()
    
def main():
    if len(sys.argv) < 2:
      print('Argument manquant (fichier image source)')
    else:
      response = input('Appliquez un flou ? (y pour oui, n pour non)\n')
      if response == 'y':
        intensity= int(input('Indiquez une valeur d\'intensité\n'))
        big_fernand_with_blur(sys.argv[1], intensity)
      else:
        big_fernand(sys.argv[1])

main()
