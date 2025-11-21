"""Game class"""

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from quest import Quest

class Game:
    """The Game class manages the overall game state and flow."""


    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None


    # Setup the game
    def setup(self, player_name=None):
        """Initialize the game with rooms, commands, and quests."""
        self._setup_commands()
        self._setup_rooms()
        self._setup_player(player_name)
        self._setup_quests()


    def _setup_commands(self):
        """Initialize all game commands."""
        self.commands["help"] = Command("help"
                                        , " : afficher cette aide"
                                        , Actions.help
                                        , 0)
        self.commands["quit"] = Command("quit"
                                        , " : quitter le jeu"
                                        , Actions.quit
                                        , 0)
        self.commands["go"] = Command("go"
                                      , "<N|E|S|O> : se déplacer dans une direction cardinale"
                                      , Actions.go
                                      , 1)
        self.commands["quests"] = Command("quests"
                                          , " : afficher la liste des quêtes"
                                          , Actions.quests
                                          , 0)
        self.commands["quest"] = Command("quest"
                                         , " <titre> : afficher les détails d'une quête"
                                         , Actions.quest
                                         , 1)
        self.commands["activate"] = Command("activate"
                                            , " <titre> : activer une quête"
                                            , Actions.activate
                                            , 1)
        self.commands["rewards"] = Command("rewards"
                                           , " : afficher vos récompenses"
                                           , Actions.rewards
                                           , 0)


    def _setup_rooms(self):
        """Initialize all rooms and their exits."""
        # Create rooms
        s = "dans une forêt enchantée, avec une brise légère à travers la cime des arbres."
        forest = Room("Forest", s)

        s = "dans une immense tour en pierre qui s'élève au dessus des nuages."
        tower = Room("Tower", s)

        s = "dans une grotte profonde et sombre. Des voix proviennent des profondeurs."
        cave = Room("Cave", s)

        s = "dans un chalet au toit de chaume. Une épaisse fumée verte sort de la cheminée."
        cottage = Room("Cottage", s)

        s = "dans un marécage vaseux, sombre et ténébreux. L'eau bouillonne."
        swamp = Room("Swamp", s)

        s = "dans un château fort avec un pont levis et des tours à la flèche en or massif."
        castle = Room("Castle", s)

        # Add rooms to game
        for room in [forest, tower, cave, cottage, swamp, castle]:
            self.rooms.append(room)

        # Create exits
        forest.exits = {"N": cave, "E": tower, "S": castle, "O": None}
        tower.exits = {"N": cottage, "E": None, "S": swamp, "O": forest}
        cave.exits = {"N": None, "E": cottage, "S": forest, "O": None}
        cottage.exits = {"N": None, "E": None, "S": tower, "O": cave}
        swamp.exits = {"N": tower, "E": None, "S": None, "O": castle}
        castle.exits = {"N": forest, "E": swamp, "S": None, "O": None}


    def _setup_player(self, player_name=None):
        """Initialize the player."""
        if player_name is None:
            player_name = input("\nEntrez votre nom: ")

        self.player = Player(player_name)
        self.player.current_room = self.rooms[4]  # swamp


    def _setup_quests(self):
        """Initialize all quests."""
        exploration_quest = Quest(
            title="Grand Explorateur",
            description="Explorez tous les lieux de ce monde mystérieux.",
            objectives=["Visiter Forest"
                        , "Visiter Tower"
                        , "Visiter Cave"
                        , "Visiter Cottage"
                        , "Visiter Castle"],
            reward="Titre de Grand Explorateur"
        )

        travel_quest = Quest(
            title="Grand Voyageur",
            description="Déplacez-vous 10 fois entre les lieux.",
            objectives=["Se déplacer 10 fois"],
            reward="Bottes de voyageur"
        )

        discovery_quest = Quest(
            title="Découvreur de Secrets",
            description="Découvrez les trois lieux les plus mystérieux.",
            objectives=["Visiter Cave"
                        , "Visiter Tower"
                        , "Visiter Castle"],
            reward="Clé dorée"
        )

        # Add quests to player's quest manager
        self.player.quest_manager.add_quest(exploration_quest)
        self.player.quest_manager.add_quest(travel_quest)
        self.player.quest_manager.add_quest(discovery_quest)


    # Play the game
    def play(self):
        """Main game loop."""

        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))


    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        """Process the command entered by the player."""

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands:
            msg1 = f"\nCommande '{command_word}' non reconnue."
            msg2 = " Entrez 'help' pour voir la liste des commandes disponibles.\n"
            print(msg1 + msg2)
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)


    # Print the welcome message
    def print_welcome(self):
        """Print the welcome message."""

        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")

        print(self.player.current_room.get_long_description())


def main():
    """Create a game object and play the game"""
    Game().play()


if __name__ == "__main__":
    main()
