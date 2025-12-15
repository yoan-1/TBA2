
class Item:
    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"

if __name__ == "__main__":
    Item("sword", "une épée au fil tranchant comme un rasoir", 2)
    print(sword)

