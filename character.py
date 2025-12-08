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

def __str__(self):
        return f"{self.name}: {self.description}, current_room, {self.msgs}"

if __name__ == "__main__":
    PNJ = character("PNJ", "un étudiant souriant", "La Rue", ["Salut à toi !"])
    print(PNJ)



def description_char():
    return f"\n vous êtes en face de {self.description_char}\n\n"