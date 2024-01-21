import cv2
import sys

class Setting:
    def __init__(self, arguments):
        self.blur = arguments.blur
        self.update_value = arguments.update
        self.image = cv2.imread(arguments.path)
        self.mode = arguments.mode
        self.blur_type = arguments.blur_type
        self.number_colors = arguments.number_colors
        self.path = arguments.path

        if self.image is None:
            print(f"Erreur : Ouverture du fichier impossible, vérifier le chemin")
            sys.exit(1)

        try:
            upper_than_exception(self.blur, 'blur')
            upper_than_exception(self.update_value, 'update')
            upper_than_exception(self.number_colors, 'number_colors',1)
        except ValueError as e:
            print(str(e))
            sys.exit(1)


def upper_than_exception(value, name, limit=0):
    if value < limit and limit == 0:
        raise ValueError(f"Erreur: '{name}' doit être un entier supérireur ou égale à 0")
    elif value < limit and limit == 1:
        raise ValueError(f"Erreur: '{name}' doit être un entier strictement supérireur à 0")
