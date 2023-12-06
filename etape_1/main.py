import cv2
import numpy as np

pathFile = './../imgs/lion.jpg'

image = cv2.imread(pathFile)

blurred_img = cv2.blur(image,ksize=(5,5))

gray_image = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)

median_pix = np.median(gray_image)

lower = int(max(0 ,0.25*median_pix))
upper = int(min(255,0.75*median_pix))

edges = cv2.Canny(image=blurred_img, threshold1=lower,threshold2=upper)


ret, thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)

cv2.imwrite('etape1.jpg', thresh)
