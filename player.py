"""Module définissant la classe Player pour représenter le joueur."""
from quest import QuestManager


class Player:
    """Représente le joueur avec son inventaire, quêtes et historique.

    Attributes:
        name: Nom du joueur
        current_room: Salle actuelle où se trouve le joueur
        history: Liste des salles visitées
        inventory: Dictionnaire des objets possédés
        quest_manager: Gestionnaire des quêtes
        move_count: Nombre de déplacements effectués
        rewards: Liste des récompenses obtenues
        max_inventory_slots: Capacité maximale de l'inventaire
        dead: État du joueur (mort/vivant)
    """

    # Définit le constructeur.
    def __init__(self, name, inventory=None):
        self.name = name
        self.current_room = None
        self.history = []
        # Inventaire : dictionnaire item_name -> Item instance
        self.inventory = {} if inventory is None else inventory
        self.quest_manager = QuestManager()
        self.move_count = 0
        self.rewards = []
        # état de la conversation pour les commandes comme 'je m’appelle'
        self.conversation_with = None
        self.waiting_for_name = False
        self.custom_name = None
        # capacité maximale d'objets dans l'inventaire
        self.max_inventory_slots = 3
        # état du joueur (mort/vivant)
        self.dead = False

    def get_history(self):
        """Retourne l'historique des salles visitées (sauf la salle actuelle)."""
        # Si l'historique n'a qu'une seule pièce (la pièce actuelle), on ne liste rien.
        if len(self.history) <= 1:
            return "tu es toujours dans la pièce de départ!"

        # Exclure la dernière pièce (qui est la pièce actuelle)
        visited_rooms = self.history[:-1]

        history_string = "\nVous avez déjà visité les pièces suivantes:\n"
        for room in visited_rooms:
            # Nous utilisons la description de la pièce (ex: "un marécage sombre...")
            history_string += f"- {room.name}\n"
        return history_string

    def get_inventory(self):
        """Retourne une description de l'inventaire du joueur."""
        # S'il n'y a rien dans l'inventaire, on le signale.
        if len(self.inventory) == 0:
            return "Votre inventaire est vide."

        inventory_string = "\nVous disposez des items suivants:\n"
        for item in self.inventory.values():
            inventory_string += f"    - {item.name} : {item.description} ({item.weight} kg)\n"
        return inventory_string

    def add_reward(self, reward):
        self.rewards.append(reward)



    # Définissez la méthode de déplacement.
    def move(self, direction):
        # Obtenez la pièce suivante du dictionnaire des sorties de la pièce actuelle.
        next_room = self.current_room.exits.get(direction)

        # Si la pièce suivante est None, affiche un message d’erreur et renvoie False.
        if next_room is None:
            print("\nImpossible d'aller dans cette direction !\n")
            return False
        # Si la salle ciblée est une instance de Room et verrouillée
        try:
            locked = getattr(next_room, 'locked', False)
        except Exception:
            locked = False

        if locked:
            # Si le joueur possède une clé, proposer d'utiliser
            if 'clé' in (self.inventory or {}):
                choice = input("\nVous êtes face à une porte verrouillée. Voulez-vous utiliser la clé ?\n1-oui\n2-non\n> ").strip().lower()
                if "1" in choice or "oui" in choice:
                    try:
                        next_room.locked = False
                    except Exception:
                        pass
                    # Entrer dans la salle maintenant déverrouillée
                    self.current_room = next_room
                    self.history.append(self.current_room)
                    print(self.current_room.get_long_description())
                    return True
                else:
                    print("\nVous restez dans le couloir.\n")
                    print(self.current_room.get_long_description())
                    return False
            else:
                print("\nCette porte est fermée à clé.\n")
                return False

        # Réglez la pièce actuelle sur la pièce suivante.
        self.current_room = next_room

        self.history.append(self.current_room)

        print(self.current_room.get_long_description())
#
   #     history_output = self.get_history()
   #     if history_output:
   #         print(history_output)

        return True

    def back(self):
        if len(self.history) <= 1:
            print("\nVous ne pouvez pas aller en arrière, vous êtes dans la première salle")
            return False

        #retire la derniere salle de l'affichage
        self.history.pop()

        #le dernier élément de l'historique devient donc la piece actuelle
        self.current_room=self.history[-1]

        print(f"\nVous êtes revenu en arrière.")
        print(self.current_room.get_long_description())

        history_output = self.get_history()
        if history_output:
            print(history_output)

        return True

    def history(self, history):
        history = []
        history.append






