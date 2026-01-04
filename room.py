# Define the Room class.
class Room:

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.characters = {}
        # Inventory: dictionnaire item_name -> Item instance
        self.inventory = {}

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
        content_lines = []
    # 1. Lister les ITEMS
        for item in self.inventory.values():
            # Utilise __str__ de Item : "- nom : description (poids kg)"
            content_lines.append(f"- {item}") 

        # 2. Lister les PERSONNAGES
        # Utilise l'attribut characters corrigé
        for PNJ in self.characters.values():
            # Utilise __str__ de Character : "- Nom : description"
            content_lines.append(f"On voit : {PNJ}")

        if not content_lines:
            return "Il n'y a rien ni personne ici."
            
        return "\n".join(content_lines)