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
        back = Command("back"," : revenir en arrière", Actions.back, 0)
        self.commands["back"] = back
        inventory = Command("inventory", " : afficher votre inventaire", Actions.inventory, 0)
        self.commands["inventory"] = inventory
        
        # Setup rooms

       
        Salle_1 = Room("Salle 1", "dans la Salle 1. La course d'orientation débute !")
        self.rooms.append(Salle_1)
        Salle_3 = Room("Salle 3", "dans la Salle 3. Il n'y a rien d'interressant ici...")
        self.rooms.append(Salle_3)
        Couloir_1 = Room("Couloir 1", "dans le Couloir 1. Vous voyez des portes tout autour de vous.")
        self.rooms.append(Couloir_1)
        Couloir_2 =  Room("couloir 2", "dans le Couloir 2. Vous voyez des portes tout autour de vous.")
        self.rooms.append(Couloir_2)
        dehors = Room("dehors", "dehors. Il n'y a rien d'interessant ici...")
        self.rooms.append(dehors)
        Rue = Room("Rue", "dans la rue de l'ESIEE. Vous voyez une grande allée et pleins d'endroits où aller")
        self.rooms.append(Rue)
        Cafeteria = Room("Cafetaria","dans la cafétaria. Il y a un étudiant en face de vous.")
        self.rooms.append(Cafeteria)
        Escaliers1 = Room("Escaliers","dans les escaliers. Vous voyez un parking mais également le lieu du club musique")
        self.rooms.append(Escaliers1)
        Escaliers2 = Room("Escaliers","dans les escaliers. Vous vous trouvez dans le couloir 2")
        self.rooms.append(Escaliers2)
        Club_musique = Room("Club_musique", "arrivé au club musique. Après avoir refermé la porte, l'ambiance semble devenir étrange")
        self.rooms.append(Club_musique)

        # Create exits for rooms

        Salle_1.exits = { "N" : Couloir_1}
        Couloir_1.exits = {"O": dehors, "N" : "interdit", "E" : Rue}                  
        dehors.exits = {"E" : Couloir_1}
        Rue.exits = {"O" : Couloir_1, "E" : Couloir_2, "S" : Cafeteria}
        Couloir_2.exits = {"S" :  Salle_3, "O": dehors, "E" : Rue}
        Cafeteria.exists = {"N" : Rue}
        Escaliers1.exits = 

        # Setup player and starting roomSFS

        self.player = Player(input("\nEntrez votre nom: "), [])
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

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
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
