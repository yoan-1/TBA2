# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from character import character 
from quest import Quest 
from item import Item
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
        speak = Command("speak", " <nom_pnj> : parler à un PNJ", Actions.speak, 1)
        self.commands["speak"] = speak
        # commande `je m'appelle` retirée — gestion du nom se fait via dialogue interne
        take = Command("take", " <item> : prendre un item présent dans la pièce", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <item> : reposer un item depuis votre inventaire", Actions.drop, 1)
        self.commands["drop"] = drop
        history = Command("history", " : afficher les pièces déjà visitées", Actions.history, 0)
        self.commands["history"] = history
        quests = Command("quests", " : afficher la liste des quêtes", Actions.quests, 0)
        self.commands["quests"] = quests
        quest = Command("quest", " <titre> : afficher les détails d'une quête", Actions.quest, 1)
        self.commands["quest"] = quest
        activate = Command("activate", " <num> : activer une quête (utiliser le numéro)", Actions.activate, 1, hidden=False)
        self.commands["activate"] = activate
        rewards = Command("rewards", " : afficher vos récompenses", Actions.rewards, 0)
        self.commands["rewards"] = rewards
        stay = Command("stay", " : rester sur place (fait avancer le monde)", Actions.stay, 0)
        self.commands["stay"] = stay
        
        # Setup rooms

        
        Salle_1 = Room("Salle 1", "dans la Salle 1. La course d'orientation débute !\n\nProfesseur : Pensez à récupérer les consignes !")
        self.rooms.append(Salle_1)
        Salle_3 = Room("Salle 3", "dans la Salle 3.")
        self.rooms.append(Salle_3)
        Couloir_1 = Room("Couloir 1", "dans le Couloir 1. Vous voyez des portes tout autour de vous.")
        self.rooms.append(Couloir_1)
        # Salle 2 existe mais est initialement verrouillée
        Salle_2 = Room("Salle 2", "dans la Salle 2. La porte est verrouillée.")
        Salle_2.locked = True
        self.rooms.append(Salle_2)

        Couloir_2 = Room("couloir 2", "dans le Couloir 2. Vous voyez des portes tout autour de vous.")
        self.rooms.append(Couloir_2)
        jardin = Room("Jardin", "dans le jardin de l'ESIEE.")
        self.rooms.append(jardin)
        Rue = Room("Rue", "dans la rue de l'ESIEE. Vous voyez une grande allée et pleins d'endroits où aller")
        self.rooms.append(Rue)
        Cafeteria = Room("Cafétéria", "dans la cafétéria.")
        self.rooms.append(Cafeteria)
        Club_musique = Room("Club musique", "dans le club de musique. Une ambiance étrange survient...")
        self.rooms.append(Club_musique)
        Marcel = Room("Marcel Dassault", "Vous êtes dans la salle Marcel Dassault.")
        self.rooms.append(Marcel)
        Escaliers1= Room("Escalier 1", "dans l'escalier 1.")
        self.rooms.append(Escaliers1)
        Escaliers2= Room("Escalier 2", "dans l'escalier 2.")
        self.rooms.append(Escaliers2)
        Parking= Room("Parking", "sur le parking. Vous voyez des voitures garées un peu partout.")
        self.rooms.append(Parking) 
        # Le joueur a pu laisser quelque chose sur le parking (bouclier)
        Parking.inventory['bouclier'] = Item('bouclier', "un bouclier robuste que vous aviez laissé sur le parking", 4.0)
        Parking_2= Room("Parking 2", "sur le parking. Vous voyez des voitures garées un peu partout.")
        self.rooms.append(Parking_2)
        # Le sac contenant le monster_trunk (accessible si on a déjà visité le Club musique)
        Parking_2.inventory['sac'] = Item('sac', "un sac à dos usé qui semble contenir quelque chose", 1.0)

        # ############   ITEMS   ############
        # Le poids est à définir
       
       
        Club_musique.inventory['clé'] = Item('clé', "une petite clé dorée", 0.1)
        Salle_1.inventory['consignes'] = Item('consignes', "Une feuille avec des consignes pour bien débuter la course d'orientation", 0.2)
        Salle_1.inventory['consignes'].description = "Une feuille indiquant les pièces à découvrir : Rue, Cafétaria, Club musique"
        Salle_3.inventory['survêt'] = Item('survêt', 'On voit le survêtement rouge de Louis tahhh le tripaloski et les années 80', 0.2)
        # Dans la Salle 2 se trouve une carte brillante montrant une croix indiquant
        # un emplacement dans le Jardin (la croix marque l'endroit où se trouve l'épée).
        Salle_2.inventory['carte'] = Item('carte', "une carte brillante avec une croix marquant un emplacement dans le Jardin", 0.1)
        # Placer l'épée dans le jardin à l'emplacement indiqué par la croix
        jardin.inventory['épée'] = Item('épée', "une épée brillante plantée dans le sol, à l'endroit marqué d'une croix sur une carte", 3.0)

        # Create exits for rooms

        Salle_1.exits = { "N" : Couloir_1}
        # La sortie nord du Couloir 1 mène à Salle 2, mais Salle 2 est verrouillée au départ
        Couloir_1.exits = {"O": jardin, "N" : Salle_2, "E" : Rue, "S" : Escaliers1}             
        jardin.exits = {"E" : Couloir_1}
        Rue.exits={"O" : Couloir_1, "E" : Couloir_2, "S" : Cafeteria}
        Couloir_2.exits={"N" : Salle_3, "O": jardin, "E" : Rue, "S" : Escaliers2}
        # Connecter Salle 2 au Couloir 1
        Salle_2.exits = {"S": Couloir_1}
        Salle_3.exits={"S" : Couloir_2} 
        Cafeteria.exits={"N" : Rue} 
        Club_musique.exits={"N" : Parking_2}
        Escaliers1.exits={"N" : Couloir_1, "S" : Parking}
        Escaliers2.exits={"N" : Couloir_2, "S" : Parking}  
        Parking.exits={"N" : Escaliers1, "O" : Escaliers2, "S" : Club_musique}
        Parking_2.exits={"N" : Escaliers1, "O" : Escaliers2}
        Marcel.exits={"N": Rue, "S": Rue}

        # ############ SETUP DES PNJ/MONSTRES ############
        
        # NOTE : current_room doit être défini plus tard lors du placement
        demogorgon = character("Démogorgon", "grand, grosse bouche avec plein de dents", None, ["Je serai le président de tous les français"])
        jean_bomber = character("jean bomber", "une personne classique", None, ["Salut !"])

        # PLACEMENT DES PNJClub_musique
        # Place le Démogorgon dans le Couloir 1
        Club_musique.characters[demogorgon.name.lower()] = demogorgon
        demogorgon.current_room = Club_musique
        Cafeteria.characters[jean_bomber.name.lower()] = jean_bomber
        jean_bomber.current_room = Cafeteria


        # Setup player and starting roomSFS

        self.player = Player(input("\nEntre ton pseudo: "), {})
        self.player.current_room = Salle_1
        self.player.history.append(self.player.current_room)
        self.player.quest_manager.player = self.player
        
        self._setup_quests()

    def _setup_quests(self):
        """Initialize all quests."""
        jean_bomber_quest = Quest(
            title="Trouver la cafétaria",
            description="Explorez tous les lieux de ce monde mystérieux.",
            objectives=["Aller à Cafétéria"],
            reward="Go tabasser un sandwich"
        )

        
        # 1) Quête d'item : récupérer une clé dans le club musique
        key_quest = Quest(
            title="Récupérer la clé du Club musique",
            description="Récupérer la clé située dans le Club musique.",
            objectives=["take clé"],
            reward=Item('clé', "Une clé en récompense", 0.1)
        )

        # 2) Quête de déplacement : atteindre le Club musique
        travel_to_club = Quest(
            title="Atteindre le Club musique",
            description="Allez jusqu'au Club musique.",
            objectives=["Aller à Club musique"],
            reward=Item('guitare', "Une guitare acoustique", 2.0)
        )

        # 3) Quête d'interaction : interagir avec Jean Bomber (PNJ)
        map_reward = Item('Carte', "Carte indiquant : Le club musique est au parking en passant par les escaliers", 0.05)
        interact_jean = Quest(
            title="Parler à jean bomber",
            description="Parlez à Jean Bomber dans la Cafétéria.",
            objectives=["speak jean bomber"],
            reward=map_reward
        )
    
        
        aller_dehors = Quest(
            title="Aller dehors",
            description="Sortez dehors.", 
            objectives=["Aller à dehors"], 
            reward="Sortie réussie"
            )
        
        se_rendre_rue = Quest(
            title="Se rendre dans la Rue", 
            description="Allez dans la Rue.", 
            objectives=["Aller à Rue"], 
            reward="Gros ampoule au pied après avoir traversé la Rue mskn"
            )
        
        self.player.quest_manager.add_quest(se_rendre_rue)
        self.player.quest_manager.add_quest(jean_bomber_quest)
        jean_bomber_quest.activation_rooms = ['Cafétéria']
        self.player.quest_manager.add_quest(travel_to_club)
        self.player.quest_manager.add_quest(key_quest)
        self.player.quest_manager.add_quest(interact_jean)
        self.player.quest_manager.add_quest(aller_dehors)
        

        # Les quêtes suivantes s'activent en récupérant l'objet 'consignes'
        for q in self.player.quest_manager.get_all_quests():
            if q.title in ("Se rendre dans la Rue", "Trouver la cafétaria", "Atteindre le Club musique"):
                q.activation_items = ['consignes']

        # La activation de la quête 'Parler à jean bomber' se fera explicitement
        # lors de la commande `look` en Cafétéria (pour éviter activation à l'entrée).

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            # reset per-turn PNJ moved flag
            self._pnjs_moved = False
            self.process_command(input("> "))

            # Move PNJ only if they haven't been moved already by a command (eg. `stay`)
            if not getattr(self, '_pnjs_moved', False):
                for room in self.rooms:
                    for pnj in list(room.characters.values()):
                        if pnj.name.lower() != "jean bomber":
                            try:
                                pnj.move(self)
                            except TypeError:
                                pnj.move()
            else:
                # clear flag for next turn
                self._pnjs_moved = False

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        # Assurer que command_word n'est pas vide
        if not list_of_words or not list_of_words[0]:
             return None
             
        command_word = list_of_words[0].lower()

        # If the player is dead, only allow quitting
        try:
            if getattr(self.player, 'dead', False) and command_word != 'quit':
                print("\nVous êtes mort, vous ne pouvez plus faire que 'quit' pour quitter le jeu.\n")
                return None
        except Exception:
            pass

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
        print(f"\nBienvenue {self.player.name} dans ce jeu pédagogique qui te permettra de découvrir l'ESIEE !\n\nenfin.... on l'espère...\n\n")
        print("Rentrer 'help' te permettra d'afficher la liste des commandes nécessaires pour évoluer dans le jeu.")
        
        #
        print(self.player.current_room.get_long_description())
       

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()