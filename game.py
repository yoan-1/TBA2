"""Module définissant la classe Game - gestionnaire principal du jeu d'aventure."""

# Importation des modules
import sys
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from pathlib import Path

from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character
from quest import Quest
from item import Item


class Game:
    """Gestionnaire principal du jeu avec la logique, les salles et l'interface."""


    # Constructeur
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None


    # Configurer le jeu
    def setup(self, player_name=None):

        # Configurer les commandes

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command(
            "go",
            " <direction> : se déplacer dans une direction cardinale (N, E, S, O)",
            Actions.go,
            1
        )
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
        activate = Command(
            "activate",
            " <num> : activer une quête (utiliser le numéro)",
            Actions.activate,
            1,
            hidden=False
        )
        self.commands["activate"] = activate
        rewards = Command("rewards", " : afficher vos récompenses", Actions.rewards, 0)
        self.commands["rewards"] = rewards
        stay = Command("stay", " : rester sur place (fait avancer le monde)", Actions.stay, 0)
        self.commands["stay"] = stay

        # Configurer les salles


        Salle_1 = Room(
            "Salle 1",
            "dans la Salle 1. La course d'orientation débute !\n\n"
            "Professeur : Pensez à récupérer les consignes !"
        )
        self.rooms.append(Salle_1)
        Salle_3 = Room("Salle 3", "dans la Salle 3.")
        self.rooms.append(Salle_3)
        Couloir_1 = Room(
            "Couloir 1",
            "dans le Couloir 1. Vous voyez des portes tout autour de vous."
        )
        self.rooms.append(Couloir_1)
        # Salle 2 existe mais est initialement verrouillée
        Salle_2 = Room("Salle 2", "dans la Salle 2. La porte est verrouillée.")
        Salle_2.locked = True
        self.rooms.append(Salle_2)

        Couloir_2 = Room(
            "couloir 2",
            "dans le Couloir 2. Vous voyez des portes tout autour de vous."
        )
        self.rooms.append(Couloir_2)
        jardin = Room("Jardin", "dans le jardin de l'ESIEE.")
        self.rooms.append(jardin)
        Rue = Room(
            "Rue",
            "dans la rue de l'ESIEE. Vous voyez une grande allée "
            "et pleins d'endroits où aller"
        )
        self.rooms.append(Rue)
        Cafeteria = Room("Cafétéria", "dans la cafétéria.")
        self.rooms.append(Cafeteria)
        Club_musique = Room(
            "Club musique",
            "dans le club de musique. Une ambiance étrange survient..."
        )
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
        Parking.inventory['bouclier'] = Item(
            'bouclier',
            "un bouclier robuste que vous aviez laissé sur le parking",
            4.0
        )
        Parking_2 = Room(
            "Parking 2",
            "sur le parking. Vous voyez des voitures garées un peu partout."
        )
        self.rooms.append(Parking_2)
        # Le sac contenant le monster_trunk
        # (accessible si on a déjà visité le Club musique)
        Parking_2.inventory['sac'] = Item(
            'sac',
            "un sac à dos usé qui semble contenir quelque chose",
            1.0
        )

        # ############   ITEMS   ############
        # Le poids est à définir


        Club_musique.inventory['clé'] = Item('clé', "une petite clé dorée", 0.1)
        Salle_1.inventory['consignes'] = Item(
            'consignes',
            "Une feuille avec des consignes pour bien débuter "
            "la course d'orientation",
            0.2
        )
        Salle_1.inventory['consignes'].description = (
            "Une feuille indiquant les pièces à découvrir : "
            "Rue, Cafétaria, Club musique"
        )
        Salle_3.inventory['survêt'] = Item(
            'survêt',
            'On voit le survêtement rouge de Louis tahhh '
            'le tripaloski et les années 80',
            0.2
        )
        # Dans la Salle 2 se trouve une carte brillante montrant une croix indiquant
        # un emplacement dans le Jardin (la croix marque l'endroit où se trouve l'épée).
        Salle_2.inventory['carte'] = Item(
            'carte',
            "une carte brillante avec une croix marquant "
            "un emplacement dans le Jardin",
            0.1
        )
        # Placer l'épée dans le jardin à l'emplacement indiqué par la croix
        jardin.inventory['épée'] = Item(
            'épée',
            "une épée brillante plantée dans le sol, "
            "à l'endroit marqué d'une croix sur une carte",
            3.0
        )

        # Créer des sorties pour les rooms

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
        # Le Demogorgon sera créé et placé dans la Rue quand le joueur arrive au Club musique
        # Pour le moment, on crée juste la référence mais on ne la place nulle part
        demogorgon = Character(
            "Démogorgon",
            "grand, grosse bouche avec plein de dents",
            None,
            ["Je serai le président de tous les français"]
        )
        jean_bomber = Character(
            "jean bomber",
            "une personne classique",
            None,
            ["Salut !"]
        )

        # PLACEMENT DES PNJ
        # Le Démogorgon ne sera placé que quand le joueur entre dans le Club musique
        # Pour l'instant, on stocke juste la référence dans le jeu
        self.demogorgon = demogorgon
        self.demogorgon_spawned = False
        Cafeteria.characters[jean_bomber.name.lower()] = jean_bomber
        jean_bomber.current_room = Cafeteria


        # Configurer le lecteur et démarrer la salle de départ

        if player_name is None:
            player_name = input("\nEntre ton pseudo: ")
        self.player = Player(player_name, {})
        self.player.current_room = Salle_1
        self.player.history.append(self.player.current_room)
        self.player.quest_manager.player = self.player

        self._setup_quests()

    def _setup_quests(self):
        jean_bomber_quest = Quest(
            title="Trouver la cafétaria",
            description="Explorez tous les lieux de ce monde mystérieux.",
            objectives=["Aller à Cafétéria"],
            reward="Des sandwichs à gogo !"
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
            reward="1 km à pied, ça use, ça use..."
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

    # Jouer au jeu
    def play(self):
        """Lance la boucle principale du jeu en mode console."""
        self.setup()
        self.print_welcome()
        # Boucle jusqu’à ce que le jeu soit terminé
        while not self.finished:
            # Obtenir la commande du joueur
            # réinitialiser le drapeau déplacé par tour PNJ
            self._pnjs_moved = False
            self._should_move_pnjs = False
            self.process_command(input("> "))

            # Déplacer PNJ seulement si la commande l'autorise (go, stay) ET s'ils n'ont pas déjà bougé
            if getattr(self, '_should_move_pnjs', False) and not getattr(self, '_pnjs_moved', False):
                moved_pnjs = getattr(self, '_pnjs_moved_this_turn', set())  # Récupérer les PNJ déjà bougés ce tour
                for room in self.rooms:
                    for pnj in list(room.characters.values()):
                        if pnj.name.lower() != "jean bomber" and id(pnj) not in moved_pnjs:
                            try:
                                pnj.move(self)
                                # Marquer ce PNJ comme ayant bougé
                                moved_pnjs.add(id(pnj))
                            except TypeError:
                                pnj.move()
                                moved_pnjs.add(id(pnj))
                # Réinitialiser le set pour le prochain tour
                self._pnjs_moved_this_turn = set()
            else:
                # drapeau clair pour le prochain tour
                self._pnjs_moved = False
                self._pnjs_moved_this_turn = set()

    # Traiter la commande saisie par le joueur
    def process_command(self, command_string) -> None:
        """Traite et exécute une commande tapée par le joueur."""

        # Diviser la chaîne de commande en une liste de mots
        list_of_words = command_string.split(" ")

        # Assurer que command_word n'est pas vide
        if not list_of_words or not list_of_words[0]:
             return None

        command_word = list_of_words[0].lower()

        # Définir le flag pour savoir si les PNJ doivent se déplacer
        # Les PNJ se déplacent SEULEMENT après 'go' ou 'stay'
        self._should_move_pnjs = command_word in ('go', 'stay')

        # Si le joueur est mort, autorisez uniquement la fermeture
        try:
            if getattr(self.player, 'dead', False) and command_word != 'quit':
                print("\nVous êtes mort, vous ne pouvez plus faire que 'quit' pour quitter le jeu.\n")
                return None
        except Exception:
            pass

        # Si la commande n’est pas reconnue, afficher un message d’erreur
        if command_word not in self.commands.keys():
            # Ajout du message d'erreur
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
            return None

        # Si la commande est reconnue, exécutez-la
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Imprimer le message de bienvenue
    def print_welcome(self):
        """Affiche le message de bienvenue et les instructions."""
        print(
            f"\nBienvenue {self.player.name} dans ce jeu pédagogique "
            "qui te permettra de découvrir l'ESIEE !\n\n"
            "enfin.... on l'espère...\n\n"
        )
        print(
            "Rentrer 'help' te permettra d'afficher la liste "
            "des commandes nécessaires pour évoluer dans le jeu."
        )

        #
        print(self.player.current_room.get_long_description())


##############################
    # Créer un objet de jeu et jouer le jeu
##############################

class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        """Write message to the Text widget."""
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        """Flush method required by sys.stdout interface (no-op for Text widget)."""


class _InputRedirector:
    """Redirect input() calls to use the GUI entry field."""
    def __init__(self, gui):
        self.gui = gui
        self.waiting_for_input = False
        self.input_result = None

    def __call__(self, prompt=""):
        """Wait for user input via the entry field."""
        if prompt:
            # Display the prompt in the output
            print(prompt, end="")

        # Set flag that we're waiting for input
        self.waiting_for_input = True
        self.input_result = None

        # Wait for the user to submit input via the entry field
        self.gui.wait_variable(self.gui.input_ready_var)

        # Get the result
        result = self.input_result if self.input_result is not None else ""

        # Reset flags
        self.waiting_for_input = False
        self.input_result = None

        # Echo the response
        print(result)

        return result


class GameGUI(tk.Tk):
    """Tkinter GUI for the text-based adventure game.

    Layout layers:
    L3 (top): Split into left image area (600x400) and right buttons.
    L2 (middle): Scrolling terminal output.
    L1 (bottom): Command entry field.
    """

    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("TBA")
        self.geometry("900x700")  # Provide enough space
        self.minsize(900, 650)

        # Underlying game logic instance
        self.game = Game()

        # Ask player name via dialog (fallback to 'Joueur')
        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = "Joueur"
        self.game.setup(player_name=name)  # Pass name to avoid double prompt

        # Variable to signal when input is ready
        self.input_ready_var = tk.IntVar()
        self.input_redirector = None

        # Build UI layers
        self._build_layout()

        # Redirect stdout so game prints appear in terminal output area
        self.original_stdout = sys.stdout
        self.original_input = __builtins__.input
        sys.stdout = _StdoutRedirector(self.text_output)
        self.input_redirector = _InputRedirector(self)
        __builtins__.input = self.input_redirector

        # Print welcome text in GUI
        self.game.print_welcome()

        # Load initial room image
        self._update_room_image()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    # -------- Layout construction --------
    def _build_layout(self):
        # Configure root grid: 3 rows (L3, L2, L1)
        self.grid_rowconfigure(0, weight=0)  # Image/buttons fixed height
        self.grid_rowconfigure(1, weight=1)  # Terminal output expands
        self.grid_rowconfigure(2, weight=0)  # Entry fixed
        self.grid_columnconfigure(0, weight=1)

        # Ajout d'un panneau latéral à droite pour infos joueur
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=0)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)

        # Panneau d'infos joueur (droite)
        self.info_panel = ttk.Frame(main_frame, width=220)
        self.info_panel.grid(row=0, column=1, rowspan=3, sticky="ns", padx=(8,4), pady=6)
        self.info_panel.grid_propagate(False)
        self._build_info_panel()

        # L3 Top frame (image + boutons)
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6,3))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        # L3L Image area (left)
        image_frame = ttk.Frame(top_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT)
        image_frame.grid(row=0, column=0, sticky="nw", padx=(0,6))
        image_frame.grid_propagate(False)  # Keep requested size
        self.canvas = tk.Canvas(image_frame,
                                width=self.IMAGE_WIDTH,
                                height=self.IMAGE_HEIGHT,
                                bg="#222")
        self.canvas.pack(fill="both", expand=True)

        # Initialize image reference (will be loaded by _update_room_image)
        self._image_ref = None  # Keep reference to prevent garbage collection
        # Initial image will be loaded after welcome message

        # L3R Buttons area (right)
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.grid(row=0, column=1, sticky="ne")
        for i in range(10):
            buttons_frame.grid_rowconfigure(i, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=1)

        # Load button images (keep references to prevent garbage collection)
        assets_dir = Path(__file__).parent / 'assets'
        # Load pre-resized 50x50 PNG images for better quality
        self._btn_help = tk.PhotoImage(file=str(assets_dir / 'help-50.png'))
        self._btn_up = tk.PhotoImage(file=str(assets_dir / 'up-arrow-50.png'))
        self._btn_down = tk.PhotoImage(file=str(assets_dir / 'down-arrow-50.png'))
        self._btn_left = tk.PhotoImage(file=str(assets_dir / 'left-arrow-50.png'))
        self._btn_right = tk.PhotoImage(file=str(assets_dir / 'right-arrow-50.png'))
        self._btn_quit = tk.PhotoImage(file=str(assets_dir / 'quit-50.png'))

        # Command buttons
        tk.Button(buttons_frame,
                  image=self._btn_help,
                  command=lambda: self._send_command("help"),
                  bd=0).grid(row=0, column=0, sticky="ew", pady=2)
        # Movement buttons (N,E,S,O)
        move_frame = ttk.LabelFrame(buttons_frame, text="Déplacements")
        move_frame.grid(row=1, column=0, sticky="ew", pady=4)
        tk.Button(move_frame,
                  image=self._btn_up,
                  command=lambda: self._send_command("go N"),
                  bd=0).grid(row=0, column=0, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_left,
                  command=lambda: self._send_command("go O"),
                  bd=0).grid(row=1, column=0)
        tk.Button(move_frame,
                  image=self._btn_right,
                  command=lambda: self._send_command("go E"),
                  bd=0).grid(row=1, column=1)
        tk.Button(move_frame,
                  image=self._btn_down,
                  command=lambda: self._send_command("go S"),
                  bd=0).grid(row=2, column=0, columnspan=2)

        # Actions buttons (Take/Drop)
        actions_frame = ttk.LabelFrame(buttons_frame, text="Actions")
        actions_frame.grid(row=3, column=0, sticky="ew", pady=4)
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)
        ttk.Button(actions_frame,
                   text="📦 Take",
                   command=self._handle_take).grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(actions_frame,
                   text="🗑️ Drop",
                   command=self._handle_drop).grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        ttk.Button(actions_frame,
                   text="👁️ Look",
                   command=lambda: self._send_command("look")).grid(row=1, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(actions_frame,
                   text="💬 Speak",
                   command=self._handle_speak).grid(row=1, column=1, sticky="ew", padx=2, pady=2)
        ttk.Button(actions_frame,
                   text="⏸️ Stay",
                   command=lambda: self._send_command("stay")).grid(row=2, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(actions_frame,
                   text="🔙 Back",
                   command=lambda: self._send_command("back")).grid(row=2, column=1, sticky="ew", padx=2, pady=2)

        # Info buttons
        info_frame = ttk.LabelFrame(buttons_frame, text="Informations")
        info_frame.grid(row=5, column=0, sticky="ew", pady=4)
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        ttk.Button(info_frame,
                   text="🎒 Check",
                   command=lambda: self._send_command("check")).grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(info_frame,
                   text="📜 History",
                   command=lambda: self._send_command("history")).grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        ttk.Button(info_frame,
                   text="🎯 Quests",
                   command=lambda: self._send_command("quests")).grid(row=1, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(info_frame,
                   text="🏆 Rewards",
                   command=lambda: self._send_command("rewards")).grid(row=1, column=1, sticky="ew", padx=2, pady=2)
        ttk.Button(info_frame,
                   text="📋 Quest",
                   command=self._handle_quest).grid(row=2, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(info_frame,
                   text="✅ Activate",
                   command=self._handle_activate).grid(row=2, column=1, sticky="ew", padx=2, pady=2)

        # Quit button
        tk.Button(buttons_frame,
                  image=self._btn_quit,
                  command=lambda: self._send_command("quit"),
                  bd=0).grid(row=6, column=0, sticky="ew", pady=(8,2))

        # L2 Terminal output area (Text + Scrollbar)
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=3)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
        self.text_output = tk.Text(output_frame,
                                   wrap="word",
                                   yscrollcommand=scrollbar.set,
                                   state="disabled",
                                   bg="#111", fg="#eee")
        scrollbar.config(command=self.text_output.yview)
        self.text_output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # L1 Entry area
        entry_frame = ttk.Frame(main_frame)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=6, pady=(3,6))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()

    def _build_info_panel(self):
        # Titre
        ttk.Label(self.info_panel, text="Infos Joueur", font=("Helvetica", 13, "bold")).pack(pady=(0,8))

        # Sorties disponibles
        self.exits_label = ttk.Label(self.info_panel, text="Sorties disponibles :", font=("Helvetica", 10, "bold"))
        self.exits_label.pack(anchor="w")
        self.exits_text = tk.Text(self.info_panel, height=3, width=25, bg="#f0f0f0", fg="#000", font=("Helvetica", 9))
        self.exits_text.pack(fill="x", padx=2, pady=(0,8))
        self.exits_text.config(state="disabled")

        # Inventaire
        self.inv_label = ttk.Label(self.info_panel, text="Inventaire :", font=("Helvetica", 10, "bold"))
        self.inv_label.pack(anchor="w")
        self.inv_list = tk.Listbox(self.info_panel, height=5, width=25)
        self.inv_list.pack(fill="x", padx=2, pady=(0,8))
        # PNJ présents
        self.pnj_label = ttk.Label(self.info_panel, text="PNJ présents :", font=("Helvetica", 10, "bold"))
        self.pnj_label.pack(anchor="w")
        self.pnj_list = tk.Listbox(self.info_panel, height=3, width=25)
        self.pnj_list.pack(fill="x", padx=2, pady=(0,8))
        # Quêtes actives
        self.quest_label = ttk.Label(self.info_panel, text="Quêtes actives :", font=("Helvetica", 10, "bold"))
        self.quest_label.pack(anchor="w")
        self.quest_list = tk.Listbox(self.info_panel, height=5, width=25)
        self.quest_list.pack(fill="x", padx=2, pady=(0,8))
        # Rafraîchir à l'ouverture
        self._update_info_panel()

    def _update_info_panel(self):
        # Sorties disponibles
        self.exits_text.config(state="normal")
        self.exits_text.delete("1.0", tk.END)
        room = self.game.player.current_room if self.game.player else None
        if room and hasattr(room, 'exits') and room.exits:
            exits = []
            direction_symbols = {
                'N': '⬆️ Nord',
                'S': '⬇️ Sud',
                'E': '➡️ Est',
                'O': '⬅️ Ouest'
            }
            for direction, target_room in room.exits.items():
                if target_room is not None:
                    symbol = direction_symbols.get(direction, direction)
                    exits.append(f"{symbol}")
            if exits:
                self.exits_text.insert("1.0", "\n".join(exits))
            else:
                self.exits_text.insert("1.0", "Aucune sortie")
        else:
            self.exits_text.insert("1.0", "Aucune sortie")
        self.exits_text.config(state="disabled")

        # Inventaire
        self.inv_list.delete(0, tk.END)
        if self.game.player and self.game.player.inventory:
            for item in self.game.player.inventory.values():
                self.inv_list.insert(tk.END, f"{item.name} ({item.description})")
        # PNJ présents
        self.pnj_list.delete(0, tk.END)
        room = self.game.player.current_room if self.game.player else None
        if room and room.characters:
            for pnj in room.characters.values():
                self.pnj_list.insert(tk.END, pnj.name)
        # Quêtes actives
        self.quest_list.delete(0, tk.END)
        if self.game.player and hasattr(self.game.player, 'quest_manager'):
            for q in self.game.player.quest_manager.get_active_quests():
                self.quest_list.insert(tk.END, q.title)


    # -------- Image update --------
    def _update_room_image(self):
        """Update the canvas image based on the current room."""
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'

        # Use room-specific image if available, otherwise fallback
        if room.image:
            image_path = assets_dir / room.image
        else:
            image_path = assets_dir / 'scene.png'

        try:
            # Load new image
            self._image_ref = tk.PhotoImage(file=str(image_path))
            # Clear canvas and redraw image
            self.canvas.delete("all")
            self.canvas.create_image(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                image=self._image_ref
            )
        except (FileNotFoundError, tk.TclError):
            # Fallback to text if image not found or cannot be loaded
            self.canvas.delete("all")
            self.canvas.create_text(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                text=f"Image: {room.name}",
                fill="white",
                font=("Helvetica", 18)
            )


    # -------- Event handlers --------
    def _on_enter(self, _event=None):
        """Handle Enter key press in the entry field."""
        value = self.entry_var.get().strip()
        self.entry_var.set("")

        if not value:
            return

        # Check if we're waiting for input (from a prompt)
        if self.input_redirector and self.input_redirector.waiting_for_input:
            # Store the input result
            self.input_redirector.input_result = value
            # Signal that input is ready
            self.input_ready_var.set(1)
        else:
            # Normal command processing
            self._send_command(value)


    def _send_command(self, command):
        # Permettre uniquement 'quit' si le jeu est terminé
        if self.game.finished and command.strip().lower() != 'quit':
            print("Le jeu est terminé. Tapez 'quit' pour quitter.\n")
            return
        # Echo the command in output area
        print(f"> {command}\n")

        # Stocker la commande pour vérification ultérieure
        self._last_command = command.strip().lower()

        # Process command in a separate thread to avoid blocking the GUI
        import threading
        def process():
            self.game.process_command(command)
            # Schedule UI update on main thread
            self.after(0, self._update_after_command)

        thread = threading.Thread(target=process, daemon=True)
        thread.start()

    def _update_after_command(self):
        """Update UI after command execution."""
        self._update_room_image()
        self._update_info_panel()
        # Fermer la fenêtre uniquement si la commande était 'quit'
        if self.game.finished and getattr(self, '_last_command', '') == 'quit':
            self.after(600, self._on_close)

    def _handle_take(self):
        """Handle Take button - show dialog to select item from room."""
        if self.game.finished:
            return

        room = self.game.player.current_room
        if not room or not room.inventory:
            print("\nIl n'y a rien à prendre ici.\n")
            return

        # Create a dialog window for item selection
        dialog = tk.Toplevel(self)
        dialog.title("Prendre un objet")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(dialog, text="Choisissez un objet à prendre :", font=("Helvetica", 11, "bold")).pack(pady=10)

        # Listbox with scrollbar
        frame = ttk.Frame(dialog)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Helvetica", 10))
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        # Populate with room items
        items = list(room.inventory.keys())
        for item_name in items:
            item = room.inventory[item_name]
            desc = getattr(item, 'description', 'objet')
            listbox.insert(tk.END, f"{item_name} - {desc}")

        def on_select():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                item_name = items[idx]
                dialog.destroy()
                self._send_command(f"take {item_name}")
            else:
                print("\nAucun objet sélectionné.\n")

        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Prendre", command=on_select).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Annuler", command=dialog.destroy).pack(side="left", padx=5)

        # Double-click to select
        listbox.bind('<Double-Button-1>', lambda e: on_select())

    def _handle_drop(self):
        """Handle Drop button - show dialog to select item from inventory."""
        if self.game.finished:
            return

        player = self.game.player
        if not player.inventory:
            print("\nVotre inventaire est vide.\n")
            return

        # Create a dialog window for item selection
        dialog = tk.Toplevel(self)
        dialog.title("Déposer un objet")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(dialog, text="Choisissez un objet à déposer :", font=("Helvetica", 11, "bold")).pack(pady=10)

        # Listbox with scrollbar
        frame = ttk.Frame(dialog)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Helvetica", 10))
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        # Populate with player items
        items = list(player.inventory.keys())
        for item_name in items:
            item = player.inventory[item_name]
            desc = getattr(item, 'description', 'objet')
            listbox.insert(tk.END, f"{item_name} - {desc}")

        def on_select():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                item_name = items[idx]
                dialog.destroy()
                self._send_command(f"drop {item_name}")
            else:
                print("\nAucun objet sélectionné.\n")

        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Déposer", command=on_select).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Annuler", command=dialog.destroy).pack(side="left", padx=5)

        # Double-click to select
        listbox.bind('<Double-Button-1>', lambda e: on_select())

    def _handle_speak(self):
        """Handle Speak button - show dialog to select NPC."""
        if self.game.finished:
            return

        room = self.game.player.current_room
        if not room or not room.characters:
            print("\nIl n'y a personne ici avec qui parler.\n")
            return

        # Create a dialog window for NPC selection
        dialog = tk.Toplevel(self)
        dialog.title("Parler à un PNJ")
        dialog.geometry("400x250")
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(dialog, text="Choisissez un PNJ :", font=("Helvetica", 11, "bold")).pack(pady=10)

        # Listbox with scrollbar
        frame = ttk.Frame(dialog)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Helvetica", 10))
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        # Populate with NPCs
        npcs = list(room.characters.values())
        for npc in npcs:
            listbox.insert(tk.END, npc.name)

        def on_select():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                npc_name = npcs[idx].name
                dialog.destroy()
                self._send_command(f"speak {npc_name}")
            else:
                print("\nAucun PNJ sélectionné.\n")

        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Parler", command=on_select).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Annuler", command=dialog.destroy).pack(side="left", padx=5)

        # Double-click to select
        listbox.bind('<Double-Button-1>', lambda e: on_select())

    def _handle_quest(self):
        """Handle Quest button - show dialog to enter quest title."""
        if self.game.finished:
            return

        # Ask for quest title
        quest_title = simpledialog.askstring(
            "Détails de quête",
            "Entrez le titre de la quête :",
            parent=self
        )

        if quest_title:
            self._send_command(f"quest {quest_title}")

    def _handle_activate(self):
        """Handle Activate button - show dialog to enter quest number."""
        if self.game.finished:
            return

        # Ask for quest number
        quest_num = simpledialog.askstring(
            "Activer une quête",
            "Entrez le numéro de la quête à activer :",
            parent=self
        )

        if quest_num:
            self._send_command(f"activate {quest_num}")


    def _on_close(self):
        # Restore stdout, input and destroy window
        sys.stdout = self.original_stdout
        __builtins__.input = self.original_input
        self.destroy()


def main():
    """Entry point.

    If '--cli' is passed as an argument, start the classic console version.
    Otherwise launch the Tkinter GUI.
    Fallback to CLI if GUI cannot be initialized (e.g., headless environment).
    """
    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    try:
        app = GameGUI()
        app.mainloop()
    except tk.TclError as e:
        # Fallback to CLI if GUI fails (e.g., no DISPLAY, Tkinter not available)
        print(f"GUI indisponible ({e}). Passage en mode console.")
        Game().play()


if __name__ == "__main__":
    main()
