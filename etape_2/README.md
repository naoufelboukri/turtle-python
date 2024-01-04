# Etape2

## Choix Dépendances

On utilise numpy car les opérations sur les tableaux sont implémentés en C, ce qui les rend très rapides.

On utilise opencv-python car le plug-in est hautement optimisé pour les opérations sur les images, ce qui permet une détection de contours rapide même pour des images de grande taille.


## Approche/logique

Dans un premier temps, on charge l'image souhaité passé en argument.

```PYTHON
big_fernand(sys.argv[1])
```

On applique un flou gaussien pour réduire le bruit et améliorer la qualité de l'image. On choisit un noyau de taille donnée en paramètre de la fonction par l'utilisateur. Privilégier des valeurs impaires pour avoir un effet de flou centré

```PYTHON
blurred_img = cv2.blur(image,ksize=(intensity, intensity))
```

Ensuite, on convertit l'image en niveaux de gris.

```PYTHON
gray_image = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)
```

On calcule la médiane des valeurs de gris. La médiane est moins sensible aux valeurs aberrantes que la moyenne. Si une image a des zones très lumineuses ou très sombres, la médiane peut être une mesure plus robuste pour caractériser la luminosité de l'image.

```PYTHON
median_pix = np.median(gray_image)
```

On calcule les seuils inférieurs et supérieurs pour l'algorithme Canny. Ces valeurs ont été calculées en entrainant le modèle sur plusieurs images. En prenant 25% et 75% de la médiane, ceci crée une plage de valeurs autour de la médiane qui peut être considérée comme représentative de l'intensité des contours dans l'image.

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

Pour finir, on créé la nouvelle image dans ce dossier qu'on nomme 'etape2.jpg'.

```PYTHON
cv2.imwrite('etape2.jpg', thresh)
```
## Execution du programme

Argument à saisir: le chemin de l'image

```PYTHON
py main.py ../imgs/lion.jpg
```