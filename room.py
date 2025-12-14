# Define the Room class.



    

class Room:

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.character = {}
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
        # S'il n'y a rien dans l'inventaire, on le signale.
        if len(self.inventory) == 0:
            return "Il n'y a rien ici."
        inventory_string = "\nOn observe les alentours... on voit : \n"
        for item in self.inventory.values():
            inventory_string += f"    - {item.name} : {item.description} ({item.weight} kg)\n"
        return inventory_string

    def look(self):
        """Affiche le contenu de la pièce."""
        print(self.get_inventory())
