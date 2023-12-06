Dans un premier temps, on charge l'image souhaité qui est ici dans le dossier img. 
L'image est 'licorne.png' comme dans l'exemple de cette étape.
Le path est dans la variable pathFile et on charge l'image à l'aide de la bibliothèque opencv dans la variable image.

Ensuite, on convertit l'image en niveaux de gris à l'aide d'opencv qu'on stocke dans la variable gray_image.

Maintenant, on détecte les contours dont on a besoin grâce à l'algorithme Canny d'opencv en ajustant les valeurs de seuil.

On convertit l'image en contours noirs sur fond blanc à l'aide de la fonction threshold d'opencv.

Pour finir, on créé la nouvelle image dans ce dossier.
