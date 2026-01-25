"""Module définissant la classe Room pour représenter les salles du jeu."""

class Room:
    """Représente une salle dans le jeu avec ses sorties, objets et personnages."""

    def __init__(self, name, description):
        """Initialise une salle avec nom et description."""
        self.name = name
        self.description = description
        self.exits = {}
        # Objets présents dans la salle (nom -> Item)
        self.inventory = {}
        # Personnages (PNJ) présents dans la salle (nom-minuscule -> Character)
        self.characters = {}
        # Indique si la porte d'entrée vers cette salle est verrouillée
        self.locked = False
        # Nom du fichier image pour l'interface graphique (optionnel)
        self.image = None

    def get_exit(self, direction):
        """Retourne la salle dans la direction donnée ou None."""
        # L'accès direct au mapping des sorties est suffisant ; cette méthode était inutilisée.
        return self.exits.get(direction)

    def get_exit_string(self):
        """Retourne une chaîne formatée avec les sorties disponibles."""
        exit_string = "🧭 : "
        for direction in self.exits:
            if self.exits.get(direction) is not None:
                exit_string += direction + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    def get_long_description(self):
        """Retourne une description longue de la salle avec les sorties."""
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        """Retourne une chaîne formatée montrant les objets et personnages présents."""
        lines = []
        # Objets
        for item in self.inventory.values():
            try:
                weight = getattr(item, 'weight', '?')
                lines.append(
                    f"- {item.name} : {item.description} ({weight} kg)"
                )
            except (AttributeError, TypeError):
                lines.append(f"- {str(item)}")

        # Personnages
        for pnj in self.characters.values():
            try:
                lines.append(f"On voit : {pnj}")
            except (AttributeError, TypeError):
                lines.append(f"On voit : {str(pnj)}")

        if not lines:
            return "\nIl n'y a rien ni personne ici.\n"
        return "\n" + "\n".join(lines) + "\n"