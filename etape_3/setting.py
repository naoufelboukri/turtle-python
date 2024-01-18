import sys
import cv2


class Setting:
    def __init__(self, arguments):
        self.blur = arguments.blur
        self.update_value = arguments.update
        self.image = cv2.imread(arguments.path)
        self.blur_type = arguments.blur_type

        if self.image is None:
            print(f"Erreur : Ouverture du fichier impossible, vérifier le chemin")
            sys.exit(1)

        if self.blur_type is not None and self.blur_type != "gaussian" and \
        self.blur_type != "box" and self.blur_type != "bilateral":
            print(f"Erreur : Ce type de flou n'existe pas")
            sys.exit(1)

        try:
            upper_than_exception(self.blur, 'blur')
            upper_than_exception(self.update_value, 'update')
        except ValueError as e:
            print(str(e))
            sys.exit(1)


def upper_than_exception(value, name, limit=0):
    if value < limit:
        raise ValueError(f"Erreur: '{name}' doit être un entier supérireur ou égale à 0")
