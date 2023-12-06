import cv2

image = cv2.imread('./imgs/licorne.png')

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray_image,130,290)

ret, thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)

cv2.imwrite('etape1.jpg', thresh)
