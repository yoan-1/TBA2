# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1]
        # Move the player in the direction specified by the parameter.
        player.move(direction)
        return True

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    def back(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        player = game.player
        return player.back()

    def inventory(game, list_of_words, number_of_parameters):
        """
        Display the player's inventory.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> inventory(game, ["inventory"], 0)
        True
        >>> inventory(game, ["inventory", "N"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Display the player's inventory.
        player = game.player
        print(player.get_inventory())
        return True

    def look(game, list_of_words, number_of_parameters):
        """
        Affiche le contenu de la pièce courante (items présents).
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        current_room = player.current_room
        if current_room is None:
            print("Il n'y a rien ici.")
            return False

        print(current_room.get_inventory())
        return True

    def speak(game, list_of_words, number_of_parameters):
        """
        Parler à un PNJ dans la pièce actuelle.
        """
        l = len(list_of_words)
        if l < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        current_room = player.current_room
        pnj_name = " ".join(list_of_words[1:]).lower()

        if current_room is None:
            print("\nIl n'y a personne ici.\n")
            return False

        if not hasattr(current_room, 'characters') or pnj_name not in current_room.characters:
            print(f"\nIl n'y a pas de PNJ nommé '{pnj_name}' ici.\n")
            return False

        pnj = current_room.characters[pnj_name]
        print(f"\nVous parlez à {pnj.name}.")
        if pnj.msgs:
            print(f"{pnj.name} dit : {pnj.msgs[0]}")
        else:
            print(f"{pnj.name} n'a rien à dire.")
            # Vérifier les objectifs de quête
            player.quest_manager.check_action_objectives("speak", pnj_name)
            return True

        # Logique spéciale pour jean_bomber
        if pnj.name.lower() == "jean bomber":
            conversation_active = True
            numéro_de_réponse = "Que voulez-vous répondre ? Entrer le numéro correspondant \nou 'au revoir' pour quitter la conversation."
            
            message_index = 1  # Prochain message
            additional_msgs = ["C'est génial, tu es musicien ?",
                               "Génial ! Le club musique est au parking en passant par les escaliers.", 
                               "Je vois. Cette année t'auras plein de temps pour apprendre à jouer\nd'un instrument de musique, mais ne néglige pas tes cours !!",
                               "En voilà quelqu'un bien pressé ! Tu devrais aller au club trico ça va te calmer !!",
                               "Oui bien sûr ! Le club musique est au parking en passant par les escaliers."]
            while conversation_active:
                if message_index == 1:
                    print(f"\n{numéro_de_réponse}")
                    print("1. Salut ! Je souhaite aller au club musique")
                elif message_index == 2:
                    print(f"Que voulez-vous lui répondre ?")
                    print("1. Oui")
                    print("2. Non")
                    print("3. Peu importe, je souhaite uniquement connaître l'emplacement du club musique")
                elif message_index == 3:
                    print(f"Que voulez-vous lui répondre ?")
                    print("1. Super ! Sais-tu où se trouve le club musique ?")
                else:
                    print(f"Que voulez-vous lui répondre ?")
                    print("1. au revoir")
                choice = input("> ").strip().lower()
                if "au revoir" in choice:
                    print(f"\n{pnj.name} est partit.")
                    conversation_active = False
                elif message_index == 1 and ("1" in choice or "club" in choice or "musique" in choice):
                    print(f"{pnj.name} dit : {additional_msgs[0]}")
                    message_index += 1
                elif message_index == 2 and ("1" in choice or "ui" in choice):
                    print(f"{pnj.name} dit : {additional_msgs[1]}")
                    message_index += 1
                    print(f"\nVous avez quitté la conversation avec {pnj.name}.")
                    conversation_active = False
                    message_index = 0
                elif message_index == 2 and ("2" in choice or "on" in choice):
                    print(f"{pnj.name} dit : {additional_msgs[2]}")
                    message_index += 1
                elif message_index == 2 and ("3" in choice or "peu importe" in choice):
                    print(f"{pnj.name} dit : {additional_msgs[3]}")
                    print(f"\nVous quittez la conversation avec {pnj.name}.")
                    conversation_active = False
                    message_index = 0
                elif message_index == 3 and ("1" in choice or "uper" in choice):
                    print(f"{pnj.name} dit : {additional_msgs[4]}")
                    print(f"\nVous avez quitté la conversation avec {pnj.name}.")
                    conversation_active = False
                    message_index = 0

            else :
                True

        # Vérifier les objectifs de quête
        player.quest_manager.check_action_objectives("speak", pnj_name)

        return True

    def history(game, list_of_words, number_of_parameters):
        """Affiche l'historique des salles visitées par le joueur."""
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        history_output = player.get_history()
        if history_output:
            print(history_output)
        return True
    #Prend un item
    def _take_simple(game, list_of_words):
    
        
        if len(list_of_words) < 2:
            print("\nOups.. réessaies encore !\n")
            return False

        item_name = list_of_words[1]
        player = game.player
        current_room = player.current_room

        if current_room is None:
            print("\nIl n'y a rien ici.\n")
            return False

        if not getattr(current_room, 'inventory', {}) or item_name not in current_room.inventory:
            print(f"\nIl n'y a pas d'item nommé '{item_name}' ici.\n")
            return False

        # Déplacer l'item de la pièce vers l'inventaire du joueur
        item = current_room.inventory.pop(item_name)
        if player.inventory is None:
            player.inventory = {}
        player.inventory[item_name] = item
        print(f"\nVous avez pris l'item '{item_name}'.\n")
        return True
    #repose un item
    def _drop_simple(game, list_of_words):
        
        if len(list_of_words) < 2:
            print("\nOups.. réessaies encore !\n")
            return False

        item_name = list_of_words[1]
        player = game.player
        current_room = player.current_room

        if player.inventory is None or item_name not in player.inventory:
            print(f"\nVous n'avez pas d'item nommé '{item_name}'.\n")
            return False

        # Retirer de l'inventaire du joueur et ajouter à la pièce
        item = player.inventory.pop(item_name)
        if current_room is None:
            print("\nIl n'y a pas de pièce ici pour déposer l'item.\n")
            return False

        if getattr(current_room, 'inventory', None) is None:
            current_room.inventory = {}
        current_room.inventory[item_name] = item
        print(f"\nVous avez déposé l'item '{item_name}' ici.\n")
        return True

    # Wrappers compatibles avec l'API existante (game, list_of_words, number_of_parameters)
    def take(game, list_of_words, number_of_parameters=None):
        return Actions._take_simple(game, list_of_words)

    def drop(game, list_of_words, number_of_parameters=None):
        return Actions._drop_simple(game, list_of_words)

    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Trouver Henri à la cafétaria (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True

    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True

    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Explorateur"], 1)
        <BLANKLINE>
        Quête 'Grand Explorateur' activée !
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Activate the quest
        game.player.quest_manager.activate_quest(quest_title)
        return True

    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Show the player's rewards.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Récompenses obtenues:
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show rewards
        game.player.quest_manager.show_rewards()
        return True


  



























































































