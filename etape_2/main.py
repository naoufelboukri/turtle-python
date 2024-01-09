import cv2
import numpy as np
import sys

def big_fernand_with_blur(pathFile, intensity):
    image = cv2.imread(pathFile)
    if intensity % 2 != 0:
      intensity += 1
    blurred_img = cv2.blur(image,ksize=(intensity, intensity))
    gray_image = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)
    median_pix = np.median(gray_image)
    lower = int(max(0 ,0.25*median_pix))
    upper = int(min(255,0.75*median_pix))
    edges = cv2.Canny(image=blurred_img, threshold1=lower,threshold2=upper)
    ret, thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('etape2.jpg', thresh)
    cv2.waitKey(0)

def big_fernand(pathFile):
    image = cv2.imread(pathFile)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    median_pix = np.median(gray_image)
    lower = int(max(0 ,0.25*median_pix))
    upper = int(min(255,0.75*median_pix))
    edges = cv2.Canny(image, threshold1=lower,threshold2=upper)
    ret, thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('etape2.jpg', thresh)
    cv2.waitKey(0)
    
def main():
    if len(sys.argv) < 2:
      print('Argument manquant (fichier image source)\n')
    else:
      while True:
        response = input('Appliquez un flou ? (y pour oui, n pour non)\n')
        if response == "y":       
          try:
            intensity= int(input('Indiquez une valeur d\'intensité\n'))
          except ValueError:
            print("Erreur: Entrez un nombre entier\n")
            continue
          big_fernand_with_blur(sys.argv[1], intensity)
          break
        elif response == "n":
          big_fernand(sys.argv[1])
          break
        else:
          print("Choix non valide. Veuillez répondre par 'oui' ou 'non'.\n")
main()
