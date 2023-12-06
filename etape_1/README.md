# Etape1

## Approche/logique

Dans un premier temps, on charge l'image souhaité qui est ici dans le dossier img. 

Le path est dans la variable pathFile et on charge l'image à l'aide de la bibliothèque opencv dans la variable image.

```PYTHON
pathFile = './../imgs/lion.jpg'
image = cv2.imread(pathFile)
```

On applique un flou gaussien pour réduire le bruit et améliorer la qualité de l'image.

```PYTHON
blurred_img = cv2.blur(image,ksize=(5,5))
```

Ensuite, on convertit l'image en niveaux de gris.

```PYTHON
gray_image = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)
```

On calcule la médiane des valeurs de gris.

```PYTHON
median_pix = np.median(gray_image)
```

On calcule les seuils inférieurs et supérieurs pour l'algorithme Canny. Ces valeurs ont été calculées en entrainant le modèle sur plusierus images.

```PYTHON
lower = int(max(0 ,0.25*median_pix))
upper = int(min(255,0.75*median_pix))
```

Maintenant, on détecte les contours dont on a besoin grâce à l'algorithme Canny d'opencv avec les seuils calculés.

```PYTHON
edges = cv2.Canny(image=blurred_img, threshold1=lower,threshold2=upper)
```

On convertit l'image en contours noirs sur fond blanc à l'aide d'un seuillage binaire inversé .

```PYTHON
ret, thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)
```

Pour finir, on créé la nouvelle image dans ce dossier qu'on nomme 'etape1.jpg'.

```PYTHON
cv2.imwrite('etape1.jpg', thresh)
```
