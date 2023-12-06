# Approche/logique

## Approche/logique

Dans un premier temps, on charge l'image souhaité qui est ici dans le dossier img. 
```PYTHON
pathFile = './../imgs/lion.jpg'
```

Le path est dans la variable pathFile et on charge l'image à l'aide de la bibliothèque opencv dans la variable image.

On applique un flou gaussien pour réduire le bruit et améliorer la qualité de l'image.

Ensuite, on convertit l'image en niveaux de gris.

On calcule la médiane des valeurs de gris.

On calcule les seuils inférieurs et supérieurs pour l'algorithme Canny. Ces valeurs ont été calculées en entrainant le modèle sur plusierus images.

Maintenant, on détecte les contours dont on a besoin grâce à l'algorithme Canny d'opencv avec les seuils calculés.

On convertit l'image en contours noirs sur fond blanc à l'aide d'un seuillage binaire inversé .

Pour finir, on créé la nouvelle image dans ce dossier qu'on nomme 'etape1.jpg'.
