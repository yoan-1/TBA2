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
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None

    def get_exit_string(self):
        exit_string = "Vos choix possibles sont : "
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
        for pnj in self.characters.values():
            # Utilise __str__ de Character : "- Nom : description"
            content_lines.append(f"-on voit : {pnj}")

        if not content_lines:
            return "Il n'y a rien ici."
            
        return "\n".join(content_lines)