# Fichier character.py (Corrigé)
import random

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


if __name__ == "__main__":
    # Bloc de test corrigé
    PNJ = character("PNJ", "un étudiant souriant", "La Rue", ["Salut à toi !"]) 	
    print(PNJ)