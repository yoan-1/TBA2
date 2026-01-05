"""Define the Player class."""

class Player():
    """The Player class represents the player in the game."""


    def __init__(self, name):
        """
        Initialize a new player.
        
        Args:
            name (str): The name of the player.
            
        Examples:
        
        >>> player = Player("Alice")
        >>> player.name
        'Alice'
        """
        self.name = name
        self.current_room = None
      # Define the move method.


    def move(self, direction):
        """
        Move the player in the specified direction.
        
        Args:
            direction (str): The direction to move (N, E, S, O).
            
        Returns:
            bool: True if the move was successful, False otherwise.
            
        Examples:
        
        >>> from room import Room
        >>> player = Player("Dave")
        >>> room1 = Room("Room1", "in room 1")
        >>> room2 = Room("Room2", "in room 2")
        >>> room3 = Room("Room3", "in room 3")
        >>> room1.exits = {"N": room2, "E": None, "S": None, "O": None}
        >>> room2.exits = {"S": room1, "E": room3, "S": None, "O": None}
        >>> player.current_room = room1
        >>> player.move("N")
        <BLANKLINE>
        Vous êtes in room 2
        <BLANKLINE>
        Sorties: E
        <BLANKLINE>
        True
        >>> player.current_room.name
        'Room2'
        >>> player.move("E")
        <BLANKLINE>
        Vous êtes in room 3
        <BLANKLINE>
        Sorties:
        <BLANKLINE>
        True
        """
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())

        return True
