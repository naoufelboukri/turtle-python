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
        if s.blur_type == "gaussian":
            s.image = cv2.GaussianBlur(s.image, (intensity, intensity), 0)
        elif s.blur_type == "box":
            s.image = cv2.blur(s.image, (intensity, intensity))
        elif s.blur_type == "bilateral":
            s.image = cv2.bilateralFilter(s.image, 9, intensity, intensity)
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
    console.add_argument('--blur_type', type=str)
    args = console.parse_args()
    big_fernand(Setting(args))


main()
