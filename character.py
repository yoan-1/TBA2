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
        """
        Redéfinit la représentation textuelle pour retourner "Nom : description" 
        comme demandé dans l'exercice.
        """
        return f"{self.name} : {self.description}"

    def get_description_char(self):
        """
        Retourne une description du personnage pour un affichage dans le jeu.
        """
        return f"\nVous êtes en face de {self.description}.\n"
    
    def move(self, game=None):
        # Determine whether to show debug for this character (Demogorgon only after player has 'monster_trunk')
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

        if random.choice([True, False]):
            possible_exits=[]
            #On regarde quelles sont les sorties possibles de la salle ds lequel est le PNJ
            for exit_room in getattr(self.current_room, 'exits', {}).values():
                # Only consider actual Room objects (ignore 'interdit' or other markers)
                if isinstance(exit_room, Room):
                    possible_exits.append(exit_room)
            if show_debug:
                print(f"DEBUG: {self.name} peut se déplacer à {len(possible_exits)} endroit(s).")
            #Le pnj peut se deplacer dans les salles de possible_exits 
            if possible_exits:
                old_room = self.current_room
                # pick a valid room (defensive: ensure it has characters attr)
                new_room = next((c for c in possible_exits if hasattr(c, 'characters')), None)
                if new_room is None:
                    return False

                if self.name.lower() in getattr(old_room, 'characters', {}):
                    try:
                        del old_room.characters[self.name.lower()]
                    except Exception:
                        pass

                new_room.characters[self.name.lower()] = self

                self.current_room= new_room

                if show_debug:
                    try:
                        print(f"DEBUG: {self.name} s'est déplacé de {old_room.name} vers {new_room.name}")
                    except Exception:
                        print(f"DEBUG: {self.name} s'est déplacé.")
                return True
            if show_debug:
                try:
                    print(f"DEBUG: {self.name} n'a pas pu se déplacer (aucune sortie).")
                except Exception:
                    print(f"DEBUG: {self.name} n'a pas pu se déplacer.")
            return True
        else:
            if show_debug:
                try:
                    print(f"DEBUG: {self.name} est resté dans {getattr(self.current_room, 'name', 'une salle')}")
                except Exception:
                    print(f"DEBUG: {self.name} est resté.")
            return False
        return False




if __name__ == "__main__":
    # Bloc de test corrigé
    PNJ = character("PNJ", "un étudiant souriant", "La Rue", ["Salut à toi !"]) 	
    print(PNJ)