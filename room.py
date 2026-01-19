# Define the Room class.
class Room:

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        # Items present in the room (name -> Item)
        self.inventory = {}
        # Characters (PNJ) present in the room (lower-name -> Character)
        self.characters = {}
        # Indique si la porte d'entrée vers cette salle est verrouillée
        self.locked = False
        # Image file name for GUI (optional)
        self.image = None

    def get_exit(self, direction):
        # Direct access to exits mapping is sufficient; this helper was unused.
        return self.exits.get(direction)

    def get_exit_string(self):
        exit_string = "🧭 : "
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    def get_long_description(self):
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        """Return a formatted string showing items and characters present."""
        lines = []
        # Items
        for item in self.inventory.values():
            try:
                lines.append(f"- {item.name} : {item.description} ({getattr(item, 'weight', '?')} kg)")
            except Exception:
                lines.append(f"- {str(item)}")

        # Characters
        for pnj in self.characters.values():
            try:
                lines.append(f"On voit : {pnj}")
            except Exception:
                lines.append(f"On voit : {str(pnj)}")

        if not lines:
            return "\nIl n'y a rien ni personne ici.\n"
        return "\n" + "\n".join(lines) + "\n"
