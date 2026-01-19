import random
import unicodedata
from room import Room
DEBUG = True

class character :
#permet de représenter des PNJ, ou tout type d'être qui ne sont pas le personnage personnage
    def __init__(self,name,description, current_room, msgs):
#name: nom des monstres/pnj
#health: vie des monstres
#current_room: là où se trouve le PNJ
#msgs :ste des messages à afficher lorsque le joueur interroge le PNJ
        self.name=name
        self.description=description
        self.current_room=current_room
        self.msgs=msgs
        # Il est courant d'ajouter une valeur de santé par défaut
        self.health = 100 

    def __str__(self):
        return f"{self.name} : {self.description}"

    def get_description_char(self):
        return f"\nVous êtes en face de {self.description}.\n"
    
    def move(self, game=None):
        # Déterminer s'il faut afficher le débogage pour ce personnage (Demogorgon uniquement après que le joueur a 'monster_trunk')
        try:
            norm_name = ''.join(c for c in unicodedata.normalize('NFD', self.name).lower() if unicodedata.category(c) != 'Mn')
        except Exception:
            norm_name = self.name.lower()
        is_demogorgon = 'demogorgon' in norm_name
        show_debug = DEBUG
        if is_demogorgon:
            try:
                player = getattr(game, 'player', None)
                inv = getattr(player, 'inventory', {}) if player else {}
                show_debug = 'monster_trunk' in inv
            except Exception:
                show_debug = False

        # Récupérer toutes les sorties possibles
        possible_exits = []
        for direction, exit_room in getattr(self.current_room, 'exits', {}).items():
            # Ne considérez que les objets réels de la pièce (ignorez 'interdit' ou d'autres marqueurs)
            if isinstance(exit_room, Room):
                # Exclure le Club musique pour le Demogorgon
                try:
                    norm_name_exit = ''.join(c for c in unicodedata.normalize('NFD', exit_room.name.lower()) if unicodedata.category(c) != 'Mn')
                    if 'demogorgon' in norm_name and norm_name_exit == 'club musique':
                        continue  # Sauter le Club musique
                except Exception:
                    pass
                possible_exits.append(exit_room)
            elif show_debug:
                print(f"DEBUG: Sortie '{direction}' invalide ou None")
        
        # Créer une liste de choix : [rester, exit1, exit2, ...]
        # "rester" est représenté par None
        choices = [None] + possible_exits  # None = rester
        
        if show_debug:
            print(f"DEBUG: {self.name} a {len(choices)} option(s) : {len(possible_exits)} sortie(s) ou rester.")
        
        # Choisir aléatoirement parmi toutes les options
        choice = random.choice(choices)
        
        # Si choice est None, le PNJ reste sur place
        if choice is None:
            if show_debug:
                try:
                    print(f"DEBUG: {self.name} est resté dans {self.current_room.name}")
                except Exception:
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
            except Exception:
                pass

        new_room.characters[self.name.lower()] = self
        self.current_room = new_room

        if show_debug:
            try:
                print(f"DEBUG: {self.name} s'est déplacé de {old_room.name} vers {new_room.name}")
            except Exception:
                print(f"DEBUG: {self.name} s'est déplacé.")
        return True




if __name__ == "__main__":
    # Bloc de test corrigé
    PNJ = character("PNJ", "un étudiant souriant", "La Rue", ["Salut à toi !"]) 
    print(PNJ)
