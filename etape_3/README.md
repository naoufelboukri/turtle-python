# Etape3

## Choix Dépendances

On utilise numpy car les opérations sur les tableaux sont implémentés en C, ce qui les rend très rapides.

On utilise opencv-python car le plug-in est hautement optimisé pour les opérations sur les images, ce qui permet une détection de contours rapide même pour des images de grande taille.

On utilise argparse pour récupérer les paramètres du dessin, à savoir le :
- blur (La valeur d'intensité supérieur à 0)
- path (Le chemin relatif du fichier)
- update (La valeur de rafraichissement du dessin)

Enfin, on utilise turtle qui est une bibliothèque graphique 'turtle' permettant de dessiner sur une feuille de papier.

## Lancer le programme

Pour lancer le programme, pusiqu'il faut gérer de plus en plus de paramètre, il faut désormais lancer le programme en initialisant les paramètres en argument de la ligne de commande.

Ainsi, le programme se lance de la manière suivante 

`python main.py --path=[path] --blur=[blur] --update=[update] --blur_type=[blur_type]`

| **Arguments**  | **Type** | **Explication**                                                    |
|:---------------|:---------|:-------------------------------------------------------------------|
| *"--path"*     | string   | Correspond au chemin relatif de l'image que l'on souhaite utiliser |
| *"--blur"*     | int      | Correspond à la valeur de flou que l'on souahaite mettre ( >= 0)   |
| *"--update"*   | int      | Correspond à la valeur de rafraichissement de la page ( >= 0)      |
| *"--blur_type"*| string   | Correspond au type de flou appliqué, les choix possibles sont "gaussian","box" et "bilateral" |

## Approche/logique

### 1. Initialisation des paramètres

#### a/ argparse

Comme dit précédemment, il nous faut gérer de plus en plus de paramètres pour le lancement de notre programme. Ainsi, désormais nous utilisons la librairie **argparse** pour récupérer l'ensemble des paramètres nécessaires au projet.

Cette bibliothèque va gérer les erreurs en cas de type non accepté et va aussi permettre de fournir une documentation sur le lancement du programme en cas d'argument manquant.

Pour initialiser **argparse**, nous procédons ainsi : 

```PYTHON
    console = argparse.ArgumentParser()
    console.add_argument('--blur', type=int)
    console.add_argument('--path', type=str)
    console.add_argument('--update', type=int)
    args = console.parse_args()

    # Pour récupérer une valeur
    # blur = args.blur
```

#### b/ Traiter les paramètres 

Par la suite, nous utilisons une classe Setting dans laquelle nous allons initialiser l'ensemble des paramètres et par la même occasion gérer les erreurs.

```PYTHON
# Initialiser les paramètres 
self.blur = arguments.blur
self.update_value = arguments.update
self.image = cv2.imread(arguments.path)
```

Par la suite, nous gérons les exceptions telles que l'existance de l'image à partir du chemin relatif fourni en argument et que les valeurs **blur** et **update** ne soient pas négatifs.

```PYTHON
# Si l'image n'est pas trouvée après son chargement, alors on lance une erreur
if self.image is None:
    print(f"Erreur : Ouverture du fichier impossible, vérifier le chemin")
    sys.exit(1)

try:
    # Fonction privée dans la classe setting
    upper_than_exception(self.blur, 'blur')
    upper_than_exception(self.update_value, 'update')
except ValueError as e:
    print(str(e))
    sys.exit(1)
```

Si tous les paramètres sont valides, nous continuons le programme, à l'inverse, nous informons l'utilisateur de l'erreur rencontrée.

### 2. Création de l'image binaire

Une fois les paramètres renseignés et valides, nous lançons la fonction des **étape 1-2** pour générer l'image binaire avec un flou si la valeur renseignée est supérieur à 0.

Pour générer le flou, nous regardons si la valeur du blur est supérieur à 0, auquel cas, on applique un flou gaussien pour réduire le bruit et améliorer la qualité de l'image. Nous vérifions que l'intensité est impaire car à la différence des valeurs pairs, elles possèdent un point central qui permet la symétrie du flou. On va donc vérifier au préalable si la valeur est paire et l'ajuster à la valeur n+1 pour qu'elle soit impaire (ex: si 2, alors intensité à 3)

```PYTHON
    if s.blur > 0:
        intensity = s.blur
        if intensity % 2 == 0:
            intensity += 1
        s.image = cv2.blur(s.image, ksize=(intensity, intensity))
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

Désormais nous possédons un tableau à 2 dimensions avec des valeurs comprisent entre 0 et 255 correspondant aux points de notre image.

Nous allons pouvoir utiliser ces données pour réaliser notre dessin avec la librairie **Turtle**.

### 3. Turtle

#### a/ Initialiser Turtle 

Désormais, avec notre image binaire **thresh**, nous créons notre objet MyTurtle pour initialiser les paramètres avant de commencer le dessin.

```PYTHON
my_turtle = MyTurtle(thresh)                    # Initialiser les paramètres de turtle
my_turtle.set_tracer_active(s.update_value)     # Initialiser la valeur de rafraichissement du dessin
my_turtle.hide_turtle()                         # Cacher le curseur
```

#### b/ Dessiner

Une fois l'objet MyTurtle initialisée, nous lançons sa méthode de dessin pour donner une impression d'impression du dessin (Le dessin se fait de haut en bas).

Pour se faire, nous récupérons dans un premier temps les lignes et les colonnes de l'image binaire **rows** et **columns**.
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
            self.t.forward(1)
    self.screen.update()
```


