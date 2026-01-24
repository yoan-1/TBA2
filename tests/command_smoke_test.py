# Script de test automatique pour vérifier les commandes du jeu
# Usage: python3 tests/command_smoke_test.py

from game import Game
import builtins
from item import Item
from actions import Actions

# Préparer des réponses simulées pour les appels à input
sim_responses = [
    'Tester',            # pseudo
    '1', '1', '1',      # choix génériques
    "je m'appelle Test",
    'au revoir'
]
input_iter = iter(sim_responses * 10)
input_backup = builtins.input
builtins.input = lambda prompt='': next(input_iter, '')

try:
    g = Game(); g.setup()
    player = g.player
    # Donner une carte pour permettre les déplacements lors des tests
    player.inventory = player.inventory or {}
    player.inventory['carte'] = Item('carte', 'Carte de test', 0.1)

    results = []
    for cmd in list(g.commands.values()):
        word = cmd.command_word
        try:
            if cmd.number_of_parameters == 0:
                g.process_command(word)
                g.process_command(word + ' extra')
            elif cmd.number_of_parameters == 1:
                if word == 'go':
                    g.process_command('go N')
                    g.process_command('go')
                    g.process_command('go X')
                elif word == 'speak':
                    g.process_command('go N'); g.process_command('go E'); g.process_command('go S')
                    g.process_command('speak jean bomber')
                    g.process_command('speak')
                    g.process_command('speak nobody')
                    # move back to start for further tests
                    g.process_command('go N'); g.process_command('go O'); g.process_command('go S')
                elif word == 'take':
                    g.process_command('take carte')
                    g.process_command('take')
                    g.process_command('take nothing')
                elif word == 'drop':
                    g.process_command('drop carte')
                    g.process_command('drop')
                    g.process_command('drop nothing')
                elif word == 'quest':
                    g.process_command('quest')
                    Actions.quest(g, ['quest', 'Trouver', 'la', 'cafétaria'], 1)
                elif word == 'activate':
                    g.process_command('activate 1')
                    g.process_command('activate')
                else:
                    g.process_command(f"{word} test")
                    g.process_command(word)
            elif cmd.number_of_parameters == 2:
                g.process_command("je m'appelle Toto")
                g.process_command('je')
            results.append((word, 'ok'))
        except Exception as e:
            results.append((word, f'error: {e}'))

    print('\nRésultats du test de fumée des commandes:')
    for r in results:
        print(' -', r[0], ':', r[1])

finally:
    builtins.input = input_backup

# Sortir avec un code non-zéro si erreur
errors = [r for r in results if not r[1].startswith('ok')]
if errors:
    print('\nErreurs détectées:', errors)
    raise SystemExit(1)
else:
    print('\nTous les tests ont réussi.')
