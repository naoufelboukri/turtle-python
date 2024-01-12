import cv2
import numpy as np
import sys
import argparse
from my_turtle import MyTurtle
from setting import Setting


def big_fernand(s):
    if s.blur > 0:
        intensity = s.blur
        if intensity % 2 != 0:
            intensity += 1
        s.image = cv2.blur(s.image, ksize=(intensity, intensity))
    gray_image = cv2.cvtColor(s.image, cv2.COLOR_BGR2GRAY)
    median_pix = np.median(gray_image)
    lower = int(max(0, 0.25 * median_pix))
    upper = int(min(255, 0.75 * median_pix))
    edges = cv2.Canny(s.image, threshold1=lower, threshold2=upper)
    ret, thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)
    my_turtle = MyTurtle(thresh)
    my_turtle.set_tracer_active(s.update_value)
    my_turtle.hide_turtle()
    my_turtle.draw()


def main():
    console = argparse.ArgumentParser()
    console.add_argument('--blur', type=int)
    console.add_argument('--path', type=str)
    console.add_argument('--update', type=int)
    args = console.parse_args()
    big_fernand(Setting(args))


main()
