import random
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
    
    def move(self):
        if random.choice([True, False]):
           
            possible_exits=[]
       #On regarde quelles sont les sorties possibles de la salle ds lequel est le PNJ
            for exit_room in self.current_room.exits.values():
                if exit_room is not None and exit_room != "interdit":
                    possible_exits.append(exit_room)
            if DEBUG:
                print(f"DEBUG: {self.name} peut se déplacer à {len(possible_exits)} endroit(s).")
       #Le pnj peut se deplacer dans les salles de possible_exits 
            if possible_exits:
                old_room = self.current_room
                new_room = random.choice(possible_exits)

                if self.name.lower() in old_room.characters:
                    del old_room.characters[self.name.lower()]

                new_room.characters[self.name.lower()] = self

                self.current_room= new_room

                return True
            if DEBUG:
                print(f"DEBUG: {self.name} s'est déplacé de {old_room.name} vers {new_room.name}")
            return True
        else:
            if DEBUG:
                print(f"DEBUG: {self.name} est resté dans {self.current_room.name}")
            return False
        return False
    
    def get_msg(self):
        if self.msgs:                           #seulement si la liste de messages n'est pas vide
            return self.msgs.pop(0)

        return f"{self.name} n'a rien à dire."  # C'est le message que le joueur reçoit si le PNJ n'a pas de messages à dire.

        




if __name__ == "__main__":
    # Bloc de test corrigé
    PNJ = character("PNJ", "un étudiant souriant", "La Rue", ["Salut à toi !"]) 	
    print(PNJ)