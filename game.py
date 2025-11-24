# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from character import character

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
        
        # Setup rooms

       
        Salle_1 = Room("Salle 1", "dans la Salle 1. La course d'orientation débute !")
        self.rooms.append(Salle_1)
        Salle_3 = Room("Salle 1", "dans la Salle 1. La course d'orientation débute !")
        self.rooms.append(Salle_3)
        Couloir_1 = Room("Couloir 1", "dans le Couloir 1. Vous voyez des portes tout autour de vous.")
        self.rooms.append(Couloir_1)
        Couloir_2 =  Room("couloir 2", "dans le Couloir 2. Vous voyez des portes tout autour de vous.")
        self.rooms.append(Couloir_2)
        dehors = Room("dehors", "dehors.  ressant ici...")
        self.rooms.append(dehors)
        Rue = Room("Rue", "dans la rue de l'ESIEE. Vous voyez une grande allée et pleins d'endroits où aller")
        self.rooms.append(Rue)
        # Create exits for rooms

        Salle_1.exits = { "couloir" : Couloir_1, "rester dans la salle" : Salle_1, "O" : ""}
        Couloir_1.exits = {"aller à l'ext": dehors, "entrer dans la Salle 2" : "interdit", "aller dans la rue" : Rue}                  
        dehors.exits = {"retourner dans le couloir" : Couloir_1}
        Rue.exits={"aller dans le couloir 1" : Couloir_1, "aller dans le couloir 2" : Couloir_2}
        Couloir_2.exits={"aller dans a salle 3" :  Salle_3, "aller à l'ext": dehors, "aller dans la rue" : Rue}

 #setup des pnj/monstres 

        demogorgon=character("Démogorgon","grand, grosse bouche avec plein de dents", club_musique, "[je serai le président de tous les français]")
        pnj=character("jean bomber","une personne classique",cafetaria,"[Tu veux aller où?]")

        # Setup player and starting roomSFS

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = Salle_1

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

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
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
