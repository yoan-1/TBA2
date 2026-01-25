"""Module définissant la classe Character pour représenter les PNJ et monstres."""
import random
import unicodedata
from room import Room

DEBUG = True


class Character:
    """Représente un PNJ ou monstre avec nom, description et comportement.

    Attributes:
        name: nom du PNJ/monstre
        description: description du personnage
        current_room: salle où se trouve le PNJ
        msgs: liste des messages à afficher lors des interactions
        health: points de vie (défaut: 100)
    """

    def __init__(self, name, description, current_room, msgs):
        """Initialise un personnage avec ses attributs de base."""
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        # Il est courant d'ajouter une valeur de santé par défaut
        self.health = 100

    def __str__(self):
        """Retourne la représentation en chaîne du personnage."""
        return f"{self.name} : {self.description}"

    def get_description_char(self):
        """Retourne une description du personnage."""
        return f"\nVous êtes en face de {self.description}.\n"

    def move(self, game=None):
        """Déplace le personnage vers une salle aléatoire ou le fait rester."""
        # Déterminer s'il faut afficher le débogage pour ce personnage
        # (Demogorgon uniquement après que le joueur a 'monster_tracker')
        try:
            norm_name = ''.join(
                c for c in unicodedata.normalize('NFD', self.name).lower()
                if unicodedata.category(c) != 'Mn'
            )
        except (AttributeError, TypeError):
            norm_name = self.name.lower()
        is_demogorgon = 'demogorgon' in norm_name
        show_debug = DEBUG
        if is_demogorgon:
            try:
                player = getattr(game, 'player', None)
                inv = getattr(player, 'inventory', {}) if player else {}
                show_debug = 'monster_tracker' in inv
            except (AttributeError, TypeError):
                show_debug = False

        # Récupérer toutes les sorties possibles
        possible_exits = []
        for direction, exit_room in getattr(self.current_room, 'exits', {}).items():
            # Ne considérez que les objets réels de la pièce
            # (ignorez 'interdit' ou d'autres marqueurs)
            if isinstance(exit_room, Room):
                # Exclure le Club musique pour le Demogorgon
                try:
                    norm_name_exit = ''.join(
                        c for c in unicodedata.normalize('NFD',
                                                          exit_room.name.lower())
                        if unicodedata.category(c) != 'Mn'
                    )
                    if 'demogorgon' in norm_name and norm_name_exit == 'club musique':
                        continue  # Sauter le Club musique
                except (AttributeError, TypeError):
                    pass
                possible_exits.append(exit_room)
            elif show_debug:
                print(f"DEBUG: Sortie '{direction}' invalide ou None")

        # Créer une liste de choix : [rester, exit1, exit2, ...]
        # "rester" est représenté par None
        choices = [None] + possible_exits  # None = rester

        if show_debug:
            print(
                f"DEBUG: {self.name} a {len(choices)} option(s) : "
                f"{len(possible_exits)} sortie(s) ou rester."
            )

        # Choisir aléatoirement parmi toutes les options
        choice = random.choice(choices)

        # Si choice est None, le PNJ reste sur place
        if choice is None:
            if show_debug:
                try:
                    print(f"DEBUG: {self.name} est resté dans {self.current_room.name}")
                except (AttributeError, TypeError):
                    print(f"DEBUG: {self.name} est resté.")
            return False

        # Sinon, se déplacer vers la salle choisie
        new_room = choice

        # Vérifiez que la salle a bien l'attribut 'characters'
        if not hasattr(new_room, 'characters'):
            return False

        old_room = self.current_room
        if self.name.lower() in getattr(old_room, 'characters', {}):
            try:
                del old_room.characters[self.name.lower()]
            except (KeyError, AttributeError, TypeError):
                pass

        new_room.characters[self.name.lower()] = self
        self.current_room = new_room

        if show_debug:
            try:
                old_name = old_room.name
                new_name = new_room.name
                print(f"DEBUG: {self.name} s'est déplacé de {old_name} vers {new_name}")
            except (AttributeError, TypeError):
                print(f"DEBUG: {self.name} s'est déplacé.")
        return True


if __name__ == "__main__":
    # Bloc de test corrigé
    pnj = Character("PNJ", "un étudiant souriant", "La Rue", ["Salut à toi !"])
    print(pnj)