import cv2
import numpy as np
import argparse
from my_turtle import MyTurtle
from setting import Setting


def big_fernand(s):
    if s.blur > 0:
        intensity = s.blur
        if intensity % 2 == 0:
            intensity += 1
        s.image = cv2.blur(s.image, ksize=(intensity, intensity))
    gray_image = cv2.cvtColor(s.image, cv2.COLOR_BGR2GRAY)
    median_pix = np.median(gray_image)
    lower = int(max(0, 0.25 * median_pix))
    upper = int(min(255, 0.75 * median_pix))
    edges = cv2.Canny(s.image, threshold1=lower, threshold2=upper)
    ret, thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    formatted_contours = []
    for contour in contours:
        c = contour.squeeze()
        if c.ndim != 2:
            c = c.reshape(1, 2)
        formatted_contours.append(c)

    my_turtle = MyTurtle(thresh, formatted_contours)
    my_turtle.set_tracer_active(s.update_value)

    if s.mode == 1:  # imprimer le dessin
        my_turtle.hide_turtle()
        my_turtle.print()
    else:  # dessiner
        my_turtle.draw()


def main():
    console = argparse.ArgumentParser()
    console.add_argument('--path', type=str)
    console.add_argument('--blur', type=int, default=0)
    console.add_argument('--update', type=int, default=10)
    console.add_argument('--mode', type=str, choices=['Draw', 'Print'], default='Draw')
    args = console.parse_args()
    big_fernand(Setting(args))


main()
