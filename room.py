"""# Define the Room class."""

class Room:
    """The Room class represents a room in the game."""


    # Define the constructor.
    def __init__(self, name, description):
        """
        Initialize a Room with a name and description.
        
        >>> room = Room("Hall", "dans un grand hall")
        >>> room.name
        'Hall'
        >>> room.description
        'dans un grand hall'
        >>> room.exits
        {}
        """
        self.name = name
        self.description = description
        self.exits = {}


    # Define the get_exit method.
    def get_exit(self, direction):
        """
        Return the room in the given direction if it exists.
        
        >>> room1 = Room("Room1", "dans une pièce")
        >>> room2 = Room("Room2", "dans une autre pièce")
        >>> room1.exits["N"] = room2
        >>> room1.get_exit("N") == room2
        True
        >>> room1.get_exit("S") is None
        True
        """
        # Return the room in the given direction if it exists.
        if direction in self.exits:
            return self.exits[direction]
        return None


    # Return a string describing the room's exits.
    def get_exit_string(self):
        """
        Return a string describing the room's exits.
        
        >>> room1 = Room("Room1", "dans une pièce")
        >>> room2 = Room("Room2", "dans une autre pièce")
        >>> room3 = Room("Room3", "dans une troisième pièce")
        >>> room1.exits["N"] = room2
        >>> room1.exits["E"] = room3
        >>> room1.get_exit_string() # doctest: +ELLIPSIS
        'Sorties: ...
        """
        exit_string = "Sorties: "
        for _exit in self.exits:
            if self.exits.get(_exit) is not None:
                exit_string += _exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string


    # Return a long description of this room including exits.
    def get_long_description(self):
        """
        Return a long description of this room including exits.
        
        >>> room1 = Room("Hall", "dans un grand hall")
        >>> room2 = Room("Kitchen", "dans une cuisine")
        >>> room1.exits["N"] = room2
        >>> print(room1.get_long_description()) # doctest: +ELLIPSIS
        <BLANKLINE>
        Vous êtes dans un grand hall
        <BLANKLINE>
        Sorties: ...
        <BLANKLINE>
        """
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"
