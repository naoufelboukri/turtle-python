# Etape5

## Choix Dépendances

On utilise numpy car les opérations sur les tableaux sont implémentés en C, ce qui les rend très rapides.

On utilise opencv-python car le plug-in est hautement optimisé pour les opérations sur les images, ce qui permet une détection de contours rapide même pour des images de grande taille.

On utilise argparse pour récupérer les paramètres du dessin, à savoir le :
- blur (La valeur d'intensité supérieur à 0)
- path (Le chemin relatif du fichier)
- update (La valeur de rafraichissement du dessin)
- blur_type (le flou choisi par l'utilisateur)
- mode (Choisir le mode entre l'étape 3 - imprimer | l'étape 4 - dessiner)

On utilise scikit-learn pour la méthode des k-moyens

Enfin, on utilise turtle qui est une bibliothèque graphique 'turtle' permettant de dessiner sur une feuille de papier.

## Lancer le programme

Pour lancer le programme, pusiqu'il faut gérer de plus en plus de paramètre, il faut désormais lancer le programme en initialisant les paramètres en argument de la ligne de commande.

Ainsi, le programme se lance de la manière suivante 

`python main.py --path=[path] --blur=[blur] --update=[update] --blur_type=[blur_type]  --mode=[mode]`

| **Arguments** | **Type** | **Explication**                                                    | ** Défaut ** |
|:--------------|:---------|:-------------------------------------------------------------------|:-------------|
| *"--path"*    | string   | Correspond au chemin relatif de l'image que l'on souhaite utiliser | OBLIGATOIRE  |
| *"--blur"*    | int      | Correspond à la valeur de flou que l'on souahaite mettre ( >= 0)   | 0            |
| *"--update"*  | int      | Correspond à la valeur de rafraichissement de la page ( >= 0)      | 10           |
| *"--blur_type"*| string   | Correspond au type de flou appliqué, les choix possibles sont "gaussian","box" et "bilateral" | 'box' |
| *"--mode"*    | string   | Mode de dessin entre l'étape 3 et 4 *(Dessin ou Imprimante)*       | 'draw'       |
| *"--number_colors"*    | int   | Nombre de couleurs choisies par l'utilisateur      | 10       |


## Approche/logique

### 1. Initialisation des paramètres

#### a/ argparse

Comme dit précédemment, il nous faut gérer de plus en plus de paramètres pour le lancement de notre programme. Ainsi, désormais nous utilisons la librairie **argparse** pour récupérer l'ensemble des paramètres nécessaires au projet.

Cette bibliothèque va gérer les erreurs en cas de type non accepté et va aussi permettre de fournir une documentation sur le lancement du programme en cas d'argument manquant.

Pour initialiser **argparse**, nous procédons ainsi : 

```PYTHON
    console = argparse.ArgumentParser()
    console.add_argument('--path', type=str)
    console.add_argument('--update', type=int, default=10)
    console.add_argument('--blur', type=int, default=0)
    console.add_argument('--blur_type', type=str, choices=['box', 'gaussian', 'bilateral'], default='box')
    console.add_argument('--mode', type=str, choices=['Draw', 'Print'], default='Draw')
    console.add_argument('--number_colors', type=int, default=10 )
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
self.mode = arguments.mode
```

Par la suite, nous gérons les exceptions telles que l'existence de l'image à partir du chemin relatif fourni en argument, l'existence du flou choisi et que les valeurs **blur** et **update** ne soient pas négatifs.

```PYTHON
# Si l'image n'est pas trouvée après son chargement, alors on lance une erreur
if self.image is None:
    print(f"Erreur : Ouverture du fichier impossible, vérifier le chemin")
    sys.exit(1)

try:
    # Fonction privée dans la classe setting
    upper_than_exception(self.blur, 'blur')
    upper_than_exception(self.update_value, 'update')
    upper_than_exception(self.number_colors, 'number_colors',1)
except ValueError as e:
    print(str(e))
    sys.exit(1)
```

Si tous les paramètres sont valides, nous continuons le programme, à l'inverse, nous informons l'utilisateur de l'erreur rencontrée.

### 2. Création de l'image binaire

Une fois les paramètres renseignés et valides, nous lançons la fonction des **étape 1-2** pour générer l'image binaire avec un flou si la valeur renseignée est supérieur à 0.

Pour générer le flou, nous regardons si la valeur du blur est supérieur à 0, auquel cas, on applique le flou choisi pour réduire le bruit et améliorer la qualité de l'image. Nous vérifions que l'intensité est impaire car à la différence des valeurs pairs, elles possèdent un point central qui permet la symétrie du flou. On va donc vérifier au préalable si la valeur est paire et l'ajuster à la valeur n+1 pour qu'elle soit impaire (ex: si 2, alors intensité à 3)

Après avoir testé chaque type de flou, nous constatons que le meilleur mis en place est le flou de type **box** suivant la difficulté de l'image.
```PYTHON
    if s.blur > 0:
        intensity = s.blur
        if intensity % 2 != 0:
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

#### b / Récupérer les contours de l'image

A la différence de l'étape 3, cette fois-ci nous devons isoler les contours pour pouvoir faire notre dessin et par la suite appliquer l'algorithme des plus proches voisins à nos résultats.
Pour ce faire, nous utilisons la méthode de **open_cv** : **findContours()** sur l'image binaire générée.

Ensuite nous allons reformatter les valeurs retournées pour nos opérations de traitements d'image.

```PYTHON
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
formatted_contours = []
    for contour in contours:
        c = contour.squeeze()
        if c.ndim != 2:
            c = c.reshape(1, 2)
        formatted_contours.append(c)
```

#### c.2/ Dessiner (Etape 4)

Pour faire notre dessin à partir des contours générés, nous récupérons d'abord le premier contours du tableau, puis nous allons boucler sur chacun d'entre eux en dessinant le contour. Nous passons au suivant en utilisant l'algorithme du voisin le plus proche.

```PYTHON
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def search_nearest_neighbor(contours, ept):
    distance = []
    for contour in contours:
        distance.append(euclidean_distance(contour[0], ept))
        distance.append(euclidean_distance(contour[-1], ept))
    return distance.index(min(distance)) // 2
```

___ 
#### c.1/ Imprimer (Etape 3)

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
            self.t.dot(1)
    self.screen.update()
```

#### d/ Application des couleurs (Etape 5)

Après avoir dessiné les contours, nous allons maintenant appliqué les couleurs.

Dans un premier temps, on appele la fonction color_image pour créér la nouvelle image. Puis, on dessine comme avec un pinceau en appelant la fonction draw_background.
```PYTHON
current_contour = self.draw_contour(self.contours.pop(0),original_image)
        background =  color_image(original_image,formatted_contours)
        while len(self.contours) > 0:
            current_contour = self.draw_contour(self.contours.pop(search_nearest_neighbor(self.contours, current_contour)), original_image)
            self.screen.update()       
        self.draw_background(background)
        turtle.exitonclick()
```

Dans un premier temps, on utilise la méthode des k plus proche voisins en utilisant n clusters (n : nombre de couleurs choisies, par défaut 10)pour définir les clusters.
Ensuite on renvoie une liste de n élements qui représentent les points de chaque cluster où chaque point a comme information en premier argument ses coordonnés et en deuxième argument sa couleur dominante(la couleur avec le plus grand nombre d'occurrences).

```PYTHON
def color_image(path,formatted_contours, number_colors, mode):
    image = cv2.imread(path)
    image2 = Image.open(path).convert('RGB')
    formatted_contours = np.concatenate(formatted_contours)
    number_of_clusters = number_colors
    pixel_tab = image.reshape(-1, 3)
    tableau = []
    for y in range(image2.height):
        for x in range(image2.width):
            tableau.append(image2.getpixel((x,y)))

    kmeans = KMeans(n_clusters=number_of_clusters, n_init=1,random_state=42)
    kmeans.fit(pixel_tab) 
    max_colors = [[0, 0, 0] for _ in range(number_colors)]
    colors = [ [] for _ in range(number_colors)]
    strong_colors = kmeans.cluster_centers_.astype(int)
    for i, _ in enumerate(pixel_tab):
        colors[kmeans.labels_[i]].append(tableau[i])
        pixel_tab[i] = strong_colors[kmeans.labels_[i]]       
    for i in range(len(colors)):
        max_colors[i] =  scipy_mode(colors[i]).mode[0].tolist()   
    image_reshape = pixel_tab.reshape(image.shape)
    for k in range(len(formatted_contours)):
        image_reshape[formatted_contours[k][1]][formatted_contours[k][0]][0] = 0
        image_reshape[formatted_contours[k][1]][formatted_contours[k][0]][1] = 0   
        image_reshape[formatted_contours[k][1]][formatted_contours[k][0]][2] = 0
    result = [[] for _ in range(number_colors)]
    for y in range(image_reshape.shape[1]):
        for x in range(image_reshape.shape[0]):
            for i in range(len(strong_colors)):
                if strong_colors[i][0] == image_reshape[x][y][0] and strong_colors[i][1] == image_reshape[x][y][1] and strong_colors[i][2] == image_reshape[x][y][2]:
                    result[i].append([[x,y],max_colors[i]])
                    image_reshape[x][y] = max_colors[i]
                    break
    if mode == 'Print':
        return image_reshape
    else:
        return result
```
Ensuite on appele la fonction draw_background où on dessine couleur par couleur (actual_background représente la liste des points du cluster actuel). On appelle search_nearest_neighbor_background qui nous donne une liste de points dans un rayon de 20 pixels pour simuler le pinceau et optimiser le temps d'exécution.

```PYTHON
crayon , actual_background = search_nearest_neighbor_background(actual_background,actual_background.pop(index))
               for j in range(len(crayon)-1) :
                   current_point = crayon[j]
                   y = current_point[0][1] - columns // 2
                   x = rows // 2 - current_point[0][0]
                   self.t.goto(y, x)
                   self.t.pendown()
                   self.t.forward(1)
                   self.t.penup()
               index = len(actual_background)-1
               if len(actual_background) > 0:
                   current_point = actual_background[index]  
```

