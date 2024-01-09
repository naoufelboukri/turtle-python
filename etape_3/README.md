# Etape3

## Choix Dépendances

On utilise numpy car les opérations sur les tableaux sont implémentés en C, ce qui les rend très rapides.

On utilise opencv-python car le plug-in est hautement optimisé pour les opérations sur les images, ce qui permet une détection de contours rapide même pour des images de grande taille.

On utilise enfin turtle qui est une bibliothèque graphique 'turtle' permettant de dessiner sur une feuille de papier.

## Approche/logique

Pour cette étape, nous commençons par initialiser les paramètres de Turtle, à savoir :
- Le chemin du fichier
- Initialiser le flou
- Si oui, définir son intensité
- Indiquer une valeur de rafraîchissement du dessin

Une fois tous ces paramètres renseignés, nous exécutons le programme. Ce dernier reprend l'ensemble des instructions des étapes précédentes pour générer une image binaire.
L'image binaire est la suivante et est générée grâce à la fonction suivante :

```PYTHON
ret, thresh = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)
```

Ainsi, nous retrouvons notre image binaire en **thresh**, il s'agit dont d'un tableau à deux dimensions représentant notre image où, chaque point correspondra à une couleur ayant une valeur allant de 0 à 255.

Cette image sera notre point d'appuie afin de réaliser notre image avec Turtle. Nous avons donc à partir de cela créé un objet MyTutle pour initialiser tous les paramètres et enfin générer le dessin avec la méthode **draw()**.

```PYTHON
my_turtle = MyTurtle(thresh)                    # Initialiser les paramètres de turtle
my_turtle.set_tracer_active(s.update_value)     # Initialiser la valeur de rafraichissement du dessin
my_turtle.hide_turtle()                         # Cacher le curseur
```

## Le dessin

Pour faire le dessin, nous récupérons dans un premier temps les lignes et les colonnes de l'image binaire **rows** et **columns**.
Ensuite nous faisons une boucle pour chacune d'entre elles, nous récupérons la valeur x et y qui correspond à l'interpretation des valeurs numériques pour le dessin et se calcul de cette manière.

```commandline
x = colonne - colonne // 2
y = lignes // 2 - ligne 
```

Par défaut nous laissons le stylo levé pour ne pas faire de dessin, cependant, chaque fois que la valeur du pixel est égale à 0, alors nous descendons le stylo pour dessiner et nous mettons un point.

Nous exécutons cette fonction pour chaque point pour avoir enfin le dessin.

Enfin nous exécutons la fonction update dans chaque ligne car sans elle, le dessin serait très long et suivant la compléxité de ce dernier il peut prendre beaucoup de temps. Ainsi, notre dessin se rafraichira tous les n points dessinés.
n correspondant à la valeur d'update écrit au paramétrage de la fonction.
```PYTHON
for row in range(rows):
    for column in range(columns):
        x = column - columns // 2
        y = rows // 2 - row
        self.t.penup()
        self.t.goto(x, y)
        if self.img[row, column] == 0:
            self.t.pendown()
            self.t.dot(1)
    self.screen.update()
```


