"""Script complet pour optimiser actions.py pour Pylint."""
import re

def fix_actions():
    """Optimiser actions.py."""
    with open('actions.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Nettoyer trailing whitespace
    lines = [line.rstrip() + '\n' if line.strip() else '\n' for line in lines]
    
    # Rejoindre pour manipuler tout le contenu
    content = ''.join(lines)
    
    # 1. Ajouter docstring de module au début
    if not content.startswith('"""'):
        docstring = '"""Module d\'actions pour le jeu.\n\nCe module contient la classe Actions avec toutes les commandes\nexécutables par le joueur.\n"""\n\n'
        content = docstring + content
    
    # 2. Déplacer imports après le docstring de module
    # Supprimer les imports actuels
    content = re.sub(r'\nfrom item import Item\n', '\n', content)
    content = re.sub(r'\nimport unicodedata\n', '\n', content)
    
    # Trouver la fin du docstring de module
    if content.startswith('"""'):
        end_idx = content.find('"""\n', 4) + 4
        # Insérer imports
        imports = '\nimport unicodedata\nfrom item import Item\n'
        content = content[:end_idx] + imports + content[end_idx:]
    
    # 3. Ajouter docstring à la classe
    content = content.replace(
        '\nclass Actions:\n    # Cette méthode permet',
        '\n\nclass Actions:\n    """Classe contenant toutes les actions disponibles pour le joueur."""\n\n    # Cette méthode permet'
    )
    
    # 4. Ajouter docstrings aux méthodes manquantes
    # quit
    content = content.replace(
        '    def quit(game, list_of_words, number_of_parameters):\n        \n        l = len',
        '    def quit(game, list_of_words, number_of_parameters):\n        """Termine le jeu."""\n        l = len'
    )
    
    # help
    content = content.replace(
        '    def help(game, list_of_words, number_of_parameters):\n        \n        # Si le nombre',
        '    def help(game, list_of_words, number_of_parameters):\n        """Affiche la liste des commandes disponibles."""\n        # Si le nombre'
    )
    
    # back
    content = content.replace(
        '    def back(game, list_of_words, number_of_parameters):\n        l = len(list_of_words)',
        '    def back(game, list_of_words, number_of_parameters):\n        """Retourne à la salle précédente."""\n        l = len(list_of_words)'
    )
    
    # inventory
    content = content.replace(
        '    def inventory(game, list_of_words, number_of_parameters):\n        \n        l = len(list_of_words)',
        '    def inventory(game, list_of_words, number_of_parameters):\n        """Affiche l\'inventaire du joueur."""\n        l = len(list_of_words)'
    )
    
    # look
    content = content.replace(
        '    def look(game, list_of_words, number_of_parameters):\n        \n        l = len(list_of_words)',
        '    def look(game, list_of_words, number_of_parameters):\n        """Affiche le contenu de la salle actuelle."""\n        l = len(list_of_words)'
    )
    
    # speak
    content = content.replace(
        '    def speak(game, list_of_words, number_of_parameters):\n        \n        l = len(list_of_words)',
        '    def speak(game, list_of_words, number_of_parameters):\n        """Parle avec un PNJ."""\n        l = len(list_of_words)'
    )
    
    # take
    content = content.replace(
        '    def take(game, list_of_words, number_of_parameters=None):\n        return Actions._take_simple',
        '    def take(game, list_of_words, number_of_parameters=None):\n        """Prend un objet dans la salle."""\n        return Actions._take_simple'
    )
    
    # drop
    content = content.replace(
        '    def drop(game, list_of_words, number_of_parameters=None):\n        return Actions._drop_simple',
        '    def drop(game, list_of_words, number_of_parameters=None):\n        """Dépose un objet de l\'inventaire."""\n        return Actions._drop_simple'
    )
    
    # _take_simple
    content = content.replace(
        '    def _take_simple(game, list_of_words):\n    \n        \n        if len(list_of_words)',
        '    def _take_simple(game, list_of_words):\n        """Implémentation interne de take."""\n        if len(list_of_words)'
    )
    
    # _drop_simple
    content = content.replace(
        '    def _drop_simple(game, list_of_words):\n        \n        if len(list_of_words)',
        '    def _drop_simple(game, list_of_words):\n        """Implémentation interne de drop."""\n        if len(list_of_words)'
    )
    
    # quests
    content = content.replace(
        '    @staticmethod\n    def quests(game, list_of_words, number_of_parameters):\n        # Si le nombre',
        '    @staticmethod\n    def quests(game, list_of_words, number_of_parameters):\n        """Affiche toutes les quêtes."""\n        # Si le nombre'
    )
    
    # quest
    content = content.replace(
        '    @staticmethod\n    def quest(game, list_of_words, number_of_parameters):\n        # Si le nombre',
        '    @staticmethod\n    def quest(game, list_of_words, number_of_parameters):\n        """Affiche les détails d\'une quête."""\n        # Si le nombre'
    )
    
    # activate
    content = content.replace(
        '    @staticmethod\n    def activate(game, list_of_words, number_of_parameters):\n            # Si le nombre',
        '    @staticmethod\n    def activate(game, list_of_words, number_of_parameters):\n        """Active une quête par son ID."""\n        # Si le nombre'
    )
    
    # je
    content = content.replace(
        '    @staticmethod\n    def je(game, list_of_words, number_of_parameters):\n        # validation minimale',
        '    @staticmethod\n    def je(game, list_of_words, number_of_parameters):\n        """Commande spéciale pour indiquer son prénom."""\n        # validation minimale'
    )
    
    # rewards
    content = content.replace(
        '    @staticmethod\n    def rewards(game, list_of_words, number_of_parameters):\n        # Si le nombre',
        '    @staticmethod\n    def rewards(game, list_of_words, number_of_parameters):\n        """Affiche les récompenses obtenues."""\n        # Si le nombre'
    )
    
    # 5. S'assurer qu'il y a une newline finale
    if not content.endswith('\n'):
        content += '\n'
    
    # 6. Corriger quelques lignes trop longues spécifiques
    # Ligne 13 originale
    content = content.replace(
        '# Le message d\'erreur est stocké dans les variables MSG0 et MSG1 et formaté avec la variable command_word, le premier mot de la commande.',
        '# Le message d\'erreur est stocké dans les variables MSG0 et MSG1 et formaté\n# avec la variable command_word, le premier mot de la commande.'
    )
    
    # Ligne 87
    content = content.replace(
        '                if player.current_room.name == \'Club musique\' and not getattr(game, \'demogorgon_spawned\', False):',
        '                room_name = player.current_room.name\n                if room_name == \'Club musique\' and not getattr(\n                    game, \'demogorgon_spawned\', False):'
    )
    
    # Ligne 89
    content = content.replace(
        '                    for room in getattr(game, \'rooms\', []) or []:',
        '                    rooms_list = getattr(game, \'rooms\', []) or []\n                    for room in rooms_list:'
    )
    
    # Ligne 103
    content = content.replace(
        '                        # Marquer le Demogorgon comme ayant déjà bougé ce tour pour éviter un double déplacement',
        '                        # Marquer le Demogorgon comme ayant déjà bougé\n                        # ce tour pour éviter un double déplacement'
    )
    
    # Ligne 126
    content = content.replace(
        '            player.quest_manager.activate_quests_for_room(player.current_room.name)',
        '            room_name_val = player.current_room.name\n            player.quest_manager.activate_quests_for_room(\n                room_name_val)'
    )
    
    # Ligne 130 
    content = content.replace(
        '            player.quest_manager.check_counter_objectives("Se déplacer", player.move_count)',
        '            player.quest_manager.check_counter_objectives(\n                "Se déplacer", player.move_count)'
    )
    
    # Écrire le résultat
    with open('actions.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Optimisations appliquées à actions.py")

if __name__ == '__main__':
    fix_actions()
