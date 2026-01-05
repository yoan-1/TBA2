from game import Game

g = Game()
# Setup without user input by mocking input; Game.setup requests a name via input()
# Provide a default name by temporarily patching builtins.input
import builtins
orig_input = builtins.input
builtins.input = lambda prompt='': 'Tester'
try:
    g.setup()
finally:
    builtins.input = orig_input

# Find PNJs
dem = None
jean = None
for room in g.rooms:
    for p in list(room.characters.values()):
        import unicodedata
        norm = ''.join(c for c in unicodedata.normalize('NFD', p.name).lower() if unicodedata.category(c) != 'Mn')
        if 'demogorgon' in norm:
            dem = p
        if 'jean' in p.name.lower():
            jean = p

print('--- Before player has monster_trunk ---')
print('Player inventory:', list(g.player.inventory.keys()))
print('Demogorgon move() output:')
try:
    dem.move(g)
except Exception as e:
    print('ERROR during dem move:', e)
print('\nJean move() output:')
try:
    jean.move(g)
except Exception as e:
    print('ERROR during jean move:', e)

# Give player the monster_trunk
print('\n--- Granting monster_trunk to player and retrying ---')
g.player.inventory['monster_trunk'] = object()
print('Player inventory:', list(g.player.inventory.keys()))
print('Demogorgon move() output after giving monster_trunk:')
try:
    dem.move(g)
except Exception as e:
    print('ERROR during dem move after give:', e)


# Test taking the sac in Parking
print('\n--- Testing taking sac in Parking ---')
from actions import Actions
parking = None
club = None
for r in g.rooms:
    if r.name == 'Parking':
        parking = r
    if r.name == 'Club musique':
        club = r

if parking:
    print('Parking inventory before:', list(parking.inventory.keys()))
    # Move player to parking (simulate going there)
    g.player.current_room = parking
    g.player.history.append(parking)
    print('\nAttempting to take sac before visiting Club musique:')
    Actions.take(g, ['take', 'sac'], 1)
    print('Player inventory now:', list(g.player.inventory.keys()))

    print('\nSimulating visit to Club musique and retrying...')
    if club and club not in g.player.history:
        g.player.history.append(club)
    # Ensure player is in parking when retrying
    g.player.current_room = parking
    # Remove any pre-existing monster_trunk to test reveal
    if 'monster_trunk' in g.player.inventory:
        g.player.inventory.pop('monster_trunk')
    Actions.take(g, ['take', 'sac'], 1)
    print('Player inventory after taking sac:', list(g.player.inventory.keys()))
else:
    print('Parking room not found in game.rooms')
