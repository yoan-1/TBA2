"""Module définissant la classe Command pour représenter les commandes du jeu."""


class Command:
    """Représente une commande du jeu avec son mot-clé, aide et action associée."""

    # Le constructeur de la commande.
    def __init__(self, command_word, help_string, action,
                 number_of_parameters, hidden=False):
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters
        self.hidden = hidden

    # La représentation en chaîne de la commande.
    def __str__(self):
        return self.command_word + self.help_string