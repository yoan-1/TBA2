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

    def talk(game, list_of_words, number_of_parameters=None):
        if len(list_of_words) < 2:
            print("\nOups.. réessaies encore !\n")
            return False

        character_name = list_of_words[1].lower()
        player = game.player
        current_room = player.current_room

        if current_room is None:
            print("\n Il n'y a personne à qui parler ici.\n")
            return False

        if not getattr(current_room, 'characters', {}) or character_name not in current_room.characters:
            print(f"\n Il n'y a pas de personnage nommé '{character_name}' ici.\n")
            return False

        character = current_room.characters[character_name]
        message = character.get_msg()
        print(f"\n{message}\n")
        return True

  



























































































