import cv2
import numpy as np
import sys
from my_turtle import MyTurtle
from setting import Setting


def big_fernand(s):
    image = cv2.imread(s.path_file)
    if s.blur:
        image = cv2.blur(image, ksize=(s.intensity, s.intensity))
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    median_pix = np.median(gray_image)
    lower = int(max(0, 0.25 * median_pix))
    upper = int(min(255, 0.75 * median_pix))
    edges = cv2.Canny(image, threshold1=lower, threshold2=upper)
    ret, thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)
    my_turtle = MyTurtle(thresh)
    if s.mode == 1:
        # imprimer le dessin
        my_turtle.set_tracer_active(s.update_value)
        my_turtle.hide_turtle()
        my_turtle.print()
    else:
        # dessiner
        my_turtle.draw()


def main():
    path_file = sys.argv[1]
    if len(sys.argv) < 2:
        print('Argument manquant (fichier image source)')
    else:
        s = Setting(path_file)
        big_fernand(s)


main()
