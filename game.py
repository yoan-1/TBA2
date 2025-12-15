# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
# CORRECTION D'IMPORTATION : La classe se nomme character, pas Character
from character import character 
from item import Item
from game import DEBUG
DEBUG  = True
class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
        check = Command("check", " : afficher votre inventaire", Actions.inventory, 0)
        self.commands["check"] = check
        back = Command("back"," : Vous permet de revenir en arrière", Actions.back, 0)
        self.commands["back"] = back
        look = Command("look"," : regarder autour de soi", Actions.look, 0) 
        self.commands["look"] = look
        take = Command("take", " <item> : prendre un item présent dans la pièce", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <item> : reposer un item depuis votre inventaire", Actions.drop, 1)
        self.commands["drop"] = drop
        history = Command("history", " : afficher les pièces déjà visitées", Actions.history, 0)
        self.commands["history"] = history
        
        # Setup rooms

        
        Salle_1 = Room("Salle 1", "dans la Salle 1. La course d'orientation débute !")
        self.rooms.append(Salle_1)
        Salle_3 = Room("Salle 3", "dans la Salle 3.")
        self.rooms.append(Salle_3)
        Couloir_1 = Room("Couloir 1", "dans le Couloir 1. Vous voyez des portes tout autour de vous.")
        self.rooms.append(Couloir_1)
        Couloir_2 = Room("couloir 2", "dans le Couloir 2. Vous voyez des portes tout autour de vous.")
        self.rooms.append(Couloir_2)
        dehors = Room("dehors", "dehors")
        self.rooms.append(dehors)
        Rue = Room("Rue", "dans la rue de l'ESIEE. Vous voyez une grande allée et pleins d'endroits où aller")
        self.rooms.append(Rue)
        Cafeteria = Room("Cafétéria", "dans la cafétéria. Il y a plein de tables et de chaises ici ainsi qu'une personne")
        self.rooms.append(Cafeteria)
        Club_musique = Room("Club musique", "dans le club de musique. Une ambiance étrange survient...Regardez autour de vous!") 
        self.rooms.append(Club_musique) 
        Escaliers1= Room("Escalier 1", "dans l'escalier 1.")
        self.rooms.append(Escaliers1)
        Escaliers2= Room("Escalier 2", "dans l'escalier 2.")
        self.rooms.append(Escaliers2)
        Parking= Room("Parking", "sur le parking. Vous voyez des voitures garées un peu partout.")
        self.rooms.append(Parking) 

        # ############   ITEMS   ############
        # Le poids est à définir
        # Ajouter un item 'clé' dans la pièce 'dehors'
        dehors.inventory['key'] = Item('key', 'une clé en fer', 0.1)
        Salle_1.inventory['consignes'] = Item('consignes', "Une feuille avec des consignes pour bien débuter la course d'orientation", 0.2)
        Salle_3.inventory['survêt'] = Item('survêt', 'On voit le survêtement rouge de Louis tahhh le tripaloski et les années 80', 0.2)

        # Create exits for rooms

        Salle_1.exits = { "N" : Couloir_1}
        Couloir_1.exits = {"O": dehors, "N" : "interdit", "E" : Rue, "S" : Escaliers1}             
        dehors.exits = {"E" : Couloir_1}
        Rue.exits={"O" : Couloir_1, "E" : Couloir_2, "S" : Cafeteria}
        Couloir_2.exits={"N" : Salle_3, "O": dehors, "E" : Rue, "S" : Escaliers2}
        Salle_3.exits={"S" : Couloir_2} 
        Cafeteria.exits={"N" : Rue} 
        Club_musique.exits={"W" : Rue}
        Escaliers1.exits={"N" : Couloir_1, "S" : Parking}
        Escaliers2.exits={"N" : Couloir_2, "S" : Parking}  
        Parking.exits={"N" : Escaliers2, "O" : Escaliers1, "S" : Club_musique}

        # ############ SETUP DES PNJ/MONSTRES ############
        
        # NOTE : current_room doit être défini plus tard lors du placement
        demogorgon = character("Démogorgon", "grand, grosse bouche avec plein de dents", None, ["Je serai le président de tous les français"])
        jean_bomber = character("jean bomber", "une personne classique", None, ["Tu veux aller où?"])

        # PLACEMENT DES PNJClub_musique
        # Place le Démogorgon dans le Couloir 1
        Club_musique.characters[demogorgon.name.lower()] =demogorgon
        demogorgon.current_room = Club_musique
        
        # Place Jean Bomber dans la Rue
        Cafeteria.characters[jean_bomber.name.lower()] = Cafeteria
        jean_bomber.current_room = Cafeteria


        # Setup player and starting roomSFS

        self.player = Player(input("\nEntrez votre nom: "), {})
        self.player.current_room = Salle_1
        self.player.history.append(self.player.current_room)

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        # Assurer que command_word n'est pas vide
        if not list_of_words or not list_of_words[0]:
             return None
             
        command_word = list_of_words[0].lower()

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            # Ajout du message d'erreur
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
            return None
            
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()