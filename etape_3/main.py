import cv2
import numpy as np
import sys
import turtle
from random import random

class CustomTurtle(turtle.Turtle):
    def __init__(self, *args, **kwargs):
        screen = turtle.Screen()
        screen.bgcolor('#FFF')
        screen.title('etape_3')
        super().__init__(*args, **kwargs)

    def exit_on_click(self):
        turtle.exitonclick()


def get_segments(ls):
    pc = ls[0]
    i = 0
    segments = []
    while i < len(ls):
        while ls[i] == pc:
            i += 1
            if i >= len(ls):
                break
            segments.append((pc, i - 1))
            if i < len(ls):
                pc = ls[i]
            else:
                break

            i += 1

        return segments


def takeInformation(img):
    rows, columns = img.shape
    points = []
    for i in range(rows):
        for j in range(columns):
            if img[i,j] < 128:
                x = j - columns // 2
                y = rows // 2 - i
                points.append((x,y))

    return points

def draw2(points):
    t = turtle.Turtle()
    t.speed(0)

    for point in points:
        t.goto(point[0], point[1])
        t.pendown()
        t.dot(2)  # Dessiner un petit point à chaque position
        t.penup()

    turtle.done()


def draw(img):
    t = turtle.Turtle()
    t.speed(0)
    rows, columns = img.shape

    for i in range(rows):
        for j in range(columns):
            pixel_value = img[i,j]
            x = j - columns // 2
            y = rows // 2 - i
            t.goto(x, y)

            if pixel_value < 128:
                if not t.isdown():
                    t.pendown()
            else:
                if t.isdown():
                    t.penup()

        t.penup()
        t.goto(0, t.ycor() - 1)
    turtle.done()

def big_fernand_with_blur(pathFile, intensity):
    image = cv2.imread(pathFile)
    blurred_img = cv2.blur(image, ksize=(intensity, intensity))
    gray_image = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)
    median_pix = np.median(gray_image)
    lower = max(0, 0.25 * median_pix)
    upper = int(min(255, 0.75 * median_pix))
    edges = cv2.Canny(image=blurred_img, threshold1=lower, threshold2=upper)
    ret, thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)
    points = takeInformation(thresh)
    draw2(points)


def big_fernand(pathFile):
    image = cv2.imread(pathFile)
    rows, columns, channels = image.shape
    turtle.setup(columns, rows)
    turtle.pensize(10)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    median_pix = np.median(gray_image)
    lower = int(max(0, 0.25 * median_pix))
    upper = int(min(255, 0.75 * median_pix))
    edges = cv2.Canny(image, threshold1=lower, threshold2=upper)
    ret, thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)
    points = takeInformation(thresh)
    draw2(points)
    # for y in range(rows):
    #     for x in range(columns):
    #         pixel = thresh[y, x]
    #         turtle.penup()
    #         turtle.goto(x, rows - y)
    #         turtle.pendown()
    #         turtle.dot(1, (pixel / 255, pixel / 255, pixel / 255))
    #         turtle.update()


def main():
    if len(sys.argv) < 2:
        print('Argument manquant (fichier image source)')
    else:
        response = input('Appliquez un flou ? (y pour oui, n pour non)\n')
        if response == 'y':
            intensity = int(input('Indiquez une valeur d\'intensité\n'))
            big_fernand_with_blur(sys.argv[1], intensity)
        else:
            big_fernand(sys.argv[1])


main()
