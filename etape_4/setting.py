def bool(question):
    response = input(question + '(y : n)\n')
    return response == 'y'


class Setting:
    def __init__(self, path_file):
        print('# MONET MAKER #')
        self.path_file = path_file
        self.blur = bool('Appliquer un flou ? ')
        if self.blur:
            self.intensity = int(input("Indiquer une valeur d'intensité : \n"))
        self.mode = int(input("Choisir un mode de dessin (0: Dessin [Défaut] | 1 : Imprimer)\n"))
        self.update_value = int(input("Indiquer une valeur de rafraichissement : \n"))
