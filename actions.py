# Description : Le module d’actions.

# Le module actions contient les fonctions appelées lorsqu’une commande est exécutée.
# Chaque fonction prend 3 paramètres :
# - jeu : l’objet du jeu
# - list_of_words : la liste des mots dans la commande
# - number_of_parameters : le nombre de paramètres attendus par la commande
# Les fonctions renvoient True si la commande a été exécutée avec succès, False sinon.
# Les fonctions affichent un message d’erreur si le nombre de paramètres est incorrect.
# Le message d’erreur est différent en fonction du nombre de paramètres attendus par la commande.


# Le message d’erreur est stocké dans les variables MSG0 et MSG1 et formaté avec la variable command_word, le premier mot de la commande.
# La variable MSG0 est utilisée lorsque la commande ne prend aucun paramètre.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# La variable MSG1 est utilisée lorsque la commande prend 1 paramètre.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

from item import Item
import unicodedata

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # Si le nombre de paramètres est incorrect, affiche un message d’erreur et renvoie False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Obtenez la direction à partir de la liste de mots.
        direction = list_of_words[1]
        # déterminer la pièce suivante pour vérifier si elle a été visitée avant
        next_room = None
        if player.current_room and isinstance(player.current_room.exits, dict):
            next_room = player.current_room.exits.get(direction)

        was_visited = False
        if next_room is not None and next_room in player.history:
            was_visited = True

        # Bloquer la sortie de la Salle_1 si le joueur n'a pas la carte
        try:
            current_name = player.current_room.name if player.current_room else None
            if current_name == 'Salle 1' and next_room is not None:
                inv = getattr(player, 'inventory', {}) or {}
                if 'consignes' not in inv:
                    print("\nPensez à prendre les consignes avant de sortir de cette salle !\n")
                    return False
        except Exception:
            pass

        # Déplacez le lecteur dans la direction spécifiée par le paramètre.
        moved = player.move(direction)
        if moved:
            # Mettre à jour le compteur de déplacements
            player.move_count += 1
            # Si c'est la première découverte de la salle, activer les quêtes liées
            if not was_visited:
                player.quest_manager.activate_quests_for_room(player.current_room.name)

            # Vérifier les objectifs liés aux pièces visitées (pour les quêtes actives)
            player.quest_manager.check_room_objectives(player.current_room.name)
            # Vérifier les objectifs de type compteur (ex: Se déplacer X fois)
            player.quest_manager.check_counter_objectives("Se déplacer", player.move_count)
            # Si le joueur possède un 'monster_trunk', afficher la position actuelle du monstre
            try:
                inv = getattr(player, 'inventory', {}) or {}
                if 'monster_trunk' in inv:
                    dem_pos = None
                    for r in getattr(game, 'rooms', []) or []:
                        for cname in getattr(r, 'characters', {}).keys():
                            try:
                                norm = ''.join(c for c in unicodedata.normalize('NFD', cname).lower() if unicodedata.category(c) != 'Mn')
                            except Exception:
                                norm = cname.lower()
                            if 'demogorgon' in norm:
                                dem_pos = r.name
                                break
                        if dem_pos:
                            break
                    if dem_pos:
                        print(f"\n[monster_trunk] Le monstre est actuellement à : {dem_pos}")
            except Exception:
                pass
            # Si le monstre est dans la même pièce, proposer une confrontation
            try:
                chars = getattr(player.current_room, 'characters', {}) or {}
                if any('demogorgon' in (''.join(c for c in unicodedata.normalize('NFD', n).lower() if unicodedata.category(c) != 'Mn')) for n in chars.keys()):
                    choice = input("\nVoulez-vous engager le combat ?\n1-oui\n2-non\n> ").strip().lower()
                    # si le joueur refuse -> il est terrassé et ne peut plus jouer (sauf quit)
                    if '2' in choice or 'non' in choice:
                        print("\nVous avez hésité et le monstre vous a terrassé. Vous êtes mort.")
                        try:
                            player.dead = True
                        except Exception:
                            pass
                        return moved
                    # si le joueur accepte
                    if '1' in choice or 'oui' in choice:
                        inv = getattr(player, 'inventory', {}) or {}
                        # victoire si le joueur a le bouclier
                        if 'bouclier' in inv:
                            try:
                                key = next(n for n in chars.keys() if 'demogorgon' in (''.join(c for c in unicodedata.normalize('NFD', n).lower() if unicodedata.category(c) != 'Mn')))
                                del player.current_room.characters[key]
                            except Exception:
                                pass
                            try:
                                player.add_reward("Tuer le Démogorgon")
                            except Exception:
                                pass
                            print("\nLe bouclier amortit les coups et vous parvenez à porter l'estoc final.\n"
                                  "Une lumière éblouissante envahit la pièce...")
                            print("\nQuand vous rouvrez les yeux, vous êtes étendu au sol au même endroit.\n"
                                  "Autour de vous, des gens s'agitent comme si tout cela n'avait été qu'un rêve.\n"
                                  "Était-ce un songe ? Vous vous relevez, encore étourdi.")
                            return moved
                        else:
                            print("\nVous vous jetez sur le monstre, mais il est bien trop fort.\n"
                                  "Vous vous en sortez de justesse, épuisé. Vous vous rappelez alors avoir laissé quelque chose sur le Parking qui pourrait vous aider (un bouclier).\n"
                                  "Revenez au Parking pour récupérer ce bouclier avant de l'affronter à nouveau.")
                        # ne pas supprimer le monstre, permettre de partir
            except Exception:
                pass
        return moved

    def stay(game, list_of_words, number_of_parameters):
        """
        Stay in the current room for one turn while NPCs (including monsters) move.
        This lets the world advance without the player changing room.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Déplacer PNJ/monstres maintenant (simuler un passage de tour)
        try:
            for room in getattr(game, 'rooms', []) or []:
                for pnj in list(getattr(room, 'characters', {}).values()):
                    if pnj.name.lower() != "jean bomber":
                        try:
                            pnj.move(game)
                        except TypeError:
                            pnj.move()
        except Exception:
            pass

        # Marquez que les PNJ ont déjà déménagé ce tour pour que Game.play ne les déplace pas à nouveau
        try:
            game._pnjs_moved = True
        except Exception:
            pass

        player = game.player
        # Si le joueur a un monster_trunk, révélez la position du monstre après le mouvement
        try:
            inv = getattr(player, 'inventory', {}) or {}
            if 'monster_trunk' in inv:
                dem_pos = None
                for r in getattr(game, 'rooms', []) or []:
                    for cname in getattr(r, 'characters', {}).keys():
                        try:
                            norm = ''.join(c for c in __import__('unicodedata').normalize('NFD', cname).lower() if __import__('unicodedata').category(c) != 'Mn')
                        except Exception:
                            norm = cname.lower()
                        if 'demogorgon' in norm:
                            dem_pos = r.name
                            break
                    if dem_pos:
                        break
                if dem_pos:
                    print(f"\n[monster_trunk] Le monstre est actuellement à : {dem_pos}")
        except Exception:
            pass

        # Si le monstre est maintenant dans la même pièce, proposez une confrontation
        try:
            chars = getattr(player.current_room, 'characters', {}) or {}
            if any('demogorgon' in (''.join(c for c in __import__('unicodedata').normalize('NFD', n).lower() if __import__('unicodedata').category(c) != 'Mn')) for n in chars.keys()):
                choice = input("\nVoulez-vous engager le combat ?\n1-oui\n2-non\n> ").strip().lower()
                if '2' in choice or 'non' in choice:
                    print("\nVous avez hésité et le monstre vous a terrassé. Vous êtes mort.")
                    try:
                        player.dead = True
                    except Exception:
                        pass
                    return True
                if '1' in choice or 'oui' in choice:
                    inv = getattr(player, 'inventory', {}) or {}
                    if 'bouclier' in inv:
                        try:
                            key = next(n for n in chars.keys() if 'demogorgon' in (''.join(c for c in __import__('unicodedata').normalize('NFD', n).lower() if __import__('unicodedata').category(c) != 'Mn')))
                            del player.current_room.characters[key]
                        except Exception:
                            pass
                        try:
                            player.add_reward("Tuer le Démogorgon")
                        except Exception:
                            pass
                        print("\nLe bouclier amortit les coups et vous parvenez à porter l'estoc final.\n"
                              "Une lumière éblouissante envahit la pièce...")
                        print("\nQuand vous rouvrez les yeux, vous êtes étendu au sol au même endroit.\n"
                              "Autour de vous, des gens s'agitent comme si tout cela n'avait été qu'un rêve.\n"
                              "Était-ce un songe ? Vous vous relevez, encore étourdi.")
                        return True
                    else:
                        print("\nVous vous jetez sur le monstre, mais il est bien trop fort.\n"
                              "Vous vous en sortez de justesse, épuisé. Vous vous rappelez alors avoir laissé quelque chose sur le Parking qui pourrait vous aider (un bouclier).\n"
                              "Revenez au Parking pour récupérer ce bouclier avant de l'affronter à nouveau.")
        except Exception:
            pass

        return True

    def quit(game, list_of_words, number_of_parameters):
        
        l = len(list_of_words)
        # Si le nombre de paramètres est incorrect, affiche un message d’erreur et renvoie False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Définissez l’attribut terminé de l’objet du jeu sur True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        
        # Si le nombre de paramètres est incorrect, affiche un message d’erreur et renvoie False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Afficher la liste des commandes disponibles (ignorer les commandes masquées)
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            if getattr(command, 'hidden', False):
                continue
            print("\t- " + str(command))
        print()
        return True

    def back(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        # Si le nombre de paramètres est incorrect, affiche un message d’erreur et renvoie False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        player = game.player
        return player.back()

    def inventory(game, list_of_words, number_of_parameters):
        
        l = len(list_of_words)
        # Si le nombre de paramètres est incorrect, affiche un message d’erreur et renvoie False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Afficher l’inventaire du joueur.
        player = game.player
        print(player.get_inventory())
        return True

    def look(game, list_of_words, number_of_parameters):
        
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        current_room = player.current_room
        if current_room is None:
            print("Il n'y a rien ici.")
            return False

        print(current_room.get_inventory())
        # Activer les quêtes liées à cette salle (si configuré)
        try:
            game.player.quest_manager.activate_quests_for_room(current_room.name)
        except Exception:
            pass
        # Activation spéciale: si on fait `look` dans la Cafétéria, activer la quête
        # 'Parler à jean bomber' (ne doit pas s'activer simplement en entrant)
        try:
            if current_room.name == 'Cafétéria':
                game.player.quest_manager.activate_quest("Parler à jean bomber")
        except Exception:
            pass
        # Vérifier les objectifs liés à l'action 'look' (ex: "look Cafétéria")
        player.quest_manager.check_action_objectives("look", current_room.name)
        return True

    def speak(game, list_of_words, number_of_parameters):
        
        l = len(list_of_words)
        # Si aucun paramètre n’est fourni ou si l’utilisation est incorrecte, demandez à réessayer
        if l < number_of_parameters + 1:
            print("Réessayes")
            return False

        player = game.player
        current_room = player.current_room
        pnj_name = " ".join(list_of_words[1:]).lower()

        # S’il n’y a pas de place ou si le PNJ n’est pas présent ou non communicatif, demandez à réessayer
        if current_room is None:
            print("Réessayes")
            return False

        if not hasattr(current_room, 'characters') or pnj_name not in current_room.characters:
            print("Réessayes")
            return False

        pnj = current_room.characters[pnj_name]
        if not getattr(pnj, 'msgs', None):
            print("Réessayes")
            return False

        print(f"\nVous parlez à {pnj.name}.")
        print(f"{pnj.name} dit : {pnj.msgs[0]}")

        # Logique spéciale pour jean_bomber
        if pnj.name.lower() == "jean bomber":
            # assurez-vous que PNJ a talk_count
            if not hasattr(pnj, 'talk_count'):
                pnj.talk_count = 0

            pnj.talk_count += 1

            # Premier dialogue (premier contact)
            if pnj.talk_count == 1:
             
                conversation_active = True
                numero_de_reponse = "Que voulez-vous répondre ? Entrer le numéro correspondant \nou 'au revoir' pour quitter la conversation."
                
                message_index = 1  # Prochain message
                additional_msgs = ["C'est génial, tu es musicien ?",
                                   "Génial ! Le club musique est au parking en passant par les escaliers.", 
                                   "Je vois. Cette année t'auras plein de temps pour apprendre à jouer\nd'un instrument de musique, mais ne néglige pas tes cours !!",
                                   "En voilà quelqu'un bien pressé ! Tu devrais aller au club trico ça va te calmer !!",
                                   "Oui bien sûr ! Le club musique est au parking en passant par les escaliers."]
                while conversation_active:
                    if message_index == 1:
                        print(f"\n{numero_de_reponse}")
                        print("1. Salut ! Je souhaite aller au club musique")
                    elif message_index == 2:
                        print(f"Que voulez-vous lui répondre ?")
                        print("1. Oui")
                        print("2. Non")

                    elif message_index == 3:
                        print(f"Que voulez-vous lui répondre ?")
                        print("1. Super ! Sais-tu où se trouve le club musique ?")
                    else:
                        print(f"Que voulez-vous lui répondre ?")
                        print("1. au revoir")
                    choice = input("> ").strip().lower()
                    if "au revoir" in choice:
                        print(f"\n{pnj.name} est partit.")
                        conversation_active = False
                    elif message_index == 1 and ("1" in choice or "club" in choice or "musique" in choice):
                        print(f"{pnj.name} dit : {additional_msgs[0]}")
                        message_index += 1
                    elif message_index == 2 and ("1" in choice or "ui" in choice):
                        print(f"{pnj.name} dit : {additional_msgs[1]}")
                        message_index += 1
                        print(f"\nVous avez quitté la conversation avec {pnj.name}.")
                        conversation_active = False
                        message_index = 0
                    elif message_index == 2 and ("2" in choice or "on" in choice):
                        print(f"{pnj.name} dit : {additional_msgs[2]}")
                        message_index += 1
                    elif message_index == 3 and ("1" in choice or "uper" in choice):
                        print(f"{pnj.name} dit : {additional_msgs[3]}")
                        print(f"\nVous avez quitté la conversation avec {pnj.name}.")
                        conversation_active = False
                        message_index = 0

            else:
                # deuxième fois que l'on parle à Jean Bomber -> nouvelle logique
                print("\nJean Bomber dit : Alors tu t'es décidé à aller au club ?")
                print("1. Oui, merci !")
                print("2. Je ne trouve toujours pas...")
                choice = input("> ").strip().lower()
                if "1" in choice or "oui" in choice:
                    print("Jean Bomber : Alors bonne chance, à bientôt !")
                else:
                    # chemin où Jean propose d'emmener le joueur
                    print("Jean Bomber : Cherche bien et tu finiras par trouver. Tu t'appelles comment d'ailleurs ?")
                    print(f"je m'appelle {player.name}")
                        
                    print("\nJean Bomber : ça marche ! Moi c'est Jean Bomber ! Laisse moi t'y emmener. Bon, je t'explique. Pour rentrer dans la salle musique, c'est un peu spécial. Il faut que tu fonces dans la forte pour qu'elle s'ouvre correctement.  A toi de jouer !")
                    # trouver la salle Marcel Dassault
                    target = None
                    for r in game.rooms:
                        if r.name == 'Marcel Dassault':
                            target = r
                            break
                    if target:
                        player.current_room = target
                        player.history.append(target)
                        # déplacer jean bomber dans cette salle si présent ailleurs
                        for room in game.rooms:
                            if 'jean bomber' in getattr(room, 'characters', {}):
                                pnj_obj = room.characters.pop('jean bomber')
                                target.characters['jean bomber'] = pnj_obj
                                pnj_obj.current_room = target
                                break
                        print("\nVous foncez pour ouvrir la porte comme vous a indiqué jean bomber à qui vous faites confiance... la porte s'ouvre à la volée et vous trébuchez sur un carton rempli de cours de statistiques. Vous vous étendez de tout votre long devant 200 élèves interloqués de votre soudaine apparition...")
                        print(f"Jean Bomber : C'est ici le club musique {player.name}")
                        print("La conversation s'achève.")
                        print("1. S'excuser et écouter le cours")
                        print("2. Repartir péniblement")
                        ch = input("> ").strip().lower()
                        if "1" in ch or "s'excuser" in ch or "ecouter" in ch or "écouter" in ch:
                            print("Vous vous excusez et décidez d'écouter le cours.")
                        else:
                            print("Vous repartez péniblement.")
                    else:
                        print("Impossible de trouver la salle 'Marcel Dassault'.")
                    
        elif 'au revoir' in low:
            print(f"\n{pnj.name} est partit.")

        else:
            print("Réponse non valide. Répondez 'je m'appelle <prénom>' ou 'au revoir'.")

            # activer la quête de récupération de la clé après la conversation
            if hasattr(pnj, 'talk_count') and pnj.talk_count >= 2:
                try:
                    game.player.quest_manager.activate_quest("Récupérer la clé du Club musique")
                except Exception:
                    pass

        # Vérifier les objectifs de quête
        player.quest_manager.check_action_objectives("speak", pnj_name)

        return True

    def history(game, list_of_words, number_of_parameters):
        """Affiche l'historique des salles visitées par le joueur."""
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        history_output = player.get_history()
        if history_output:
            print(history_output)
        return True
    #Prend un item
    def _take_simple(game, list_of_words):
    
        
        if len(list_of_words) < 2:
            print("\nOups.. réessaies encore !\n")
            return False

        item_name = list_of_words[1]
        player = game.player
        current_room = player.current_room

        if current_room is None:
            print("\nIl n'y a rien ici.\n")
            return False

        if not getattr(current_room, 'inventory', {}) or item_name not in current_room.inventory:
            print(f"\nIl n'y a pas d'item nommé '{item_name}' ici.\n")
            return False

        # Logique spéciale : 'sac' contient 'monster_trunk' mais ne peut être pris que
        # si le joueur a déjà visité le 'Club musique'.
        if item_name == 'sac':
            visited_club = False
            for r in getattr(player, 'history', []) or []:
                try:
                    if getattr(r, 'name', '').lower() == 'club musique':
                        visited_club = True
                        break
                except Exception:
                    continue
            if not visited_club:
                print("\nVous ne pouvez pas prendre ce sac pour l'instant.\n")
                return False

        # Déplacer l'item de la pièce vers l'inventaire du joueur
        # Si l'inventaire est plein, demander de déposer un item pour faire de la place
        try:
            max_slots = getattr(player, 'max_inventory_slots', None)
        except Exception:
            max_slots = None
        if max_slots is not None and len(player.inventory) >= max_slots:
            # cas spécial: si l'item à prendre est le bouclier, forcer dépôt d'un item
            if item_name == 'bouclier':
                print("\nVotre inventaire est plein. Choisissez un item à déposer pour récupérer le bouclier :")
                items = list(player.inventory.keys())
                for i, n in enumerate(items, start=1):
                    print(f"{i}. {n}")
                choice = input("> ").strip()
                try:
                    idx = int(choice) - 1
                    if idx < 0 or idx >= len(items):
                        print("\nChoix invalide. Annulation de la prise du bouclier.")
                        return False
                    # déposer l'item choisi dans la pièce
                    to_drop = items[idx]
                    dropped_item = player.inventory.pop(to_drop)
                    if getattr(current_room, 'inventory', None) is None:
                        current_room.inventory = {}
                    current_room.inventory[to_drop] = dropped_item
                    print(f"\nVous avez déposé '{to_drop}' pour faire de la place.")
                except ValueError:
                    print("\nChoix invalide. Annulation de la prise du bouclier.")
                    return False
            else:
                print("\nVotre inventaire est plein. Vous ne pouvez pas prendre cet item.")
                return False

        item = current_room.inventory.pop(item_name)
        if player.inventory is None:
            player.inventory = {}
        player.inventory[item_name] = item
        print(f"\nVous avez pris l'item '{item_name}'.\n")
        # Si nous venons de prendre le sac, révélez le monster_trunk à l’intérieur
        if item_name == 'sac':
            try:
                if 'monster_trunk' not in player.inventory:
                    mt = Item('monster_trunk', "un objet étrange en cuir qui semble permettre de localiser un monstre", 2.0)
                    player.inventory['monster_trunk'] = mt
                    print("En fouillant le sac vous trouvez un objet appelé 'monster_trunk'.\n")
                    # Message indiquant l'objectif principal et le fonctionnement du monster_trunk
                    try:
                        print("\nOBJECTIF: Tuer le monstre qui rôde.\n"
                              "Votre 'monster_trunk' vous permettra de localiser le monstre en temps réel.")
                    except Exception:
                        pass
            except Exception:
                pass
        # Message narratif spécial si le joueur prend l'épée
        if item_name == 'épée':
            try:
                print("\nUn frisson parcourt votre échine. L'épée vibre dans vos mains et\n"
                      "vous réalisez que vous n'êtes plus tout à fait dans la même dimension.\n"
                      "Quelque chose rôde peut-être... Préparez-vous à l'affronter.")
            except Exception:
                pass
        # Vérifier les objectifs liés aux actions (ex: prendre un item)
        player.quest_manager.check_action_objectives("take", item_name)
        # Activer les quêtes qui se déclenchent en prenant cet item
        try:
            player.quest_manager.activate_quests_for_item(item_name)
        except Exception:
            pass
        return True
    #repose un item
    def _drop_simple(game, list_of_words):
        
        if len(list_of_words) < 2:
            print("\nOups.. réessaies encore !\n")
            return False

        item_name = list_of_words[1]
        player = game.player
        current_room = player.current_room

        if player.inventory is None or item_name not in player.inventory:
            print(f"\nVous n'avez pas d'item nommé '{item_name}'.\n")
            return False

        # Retirer de l'inventaire du joueur et ajouter à la pièce
        item = player.inventory.pop(item_name)
        if current_room is None:
            print("\nIl n'y a pas de pièce ici pour déposer l'item.\n")
            return False

        if getattr(current_room, 'inventory', None) is None:
            current_room.inventory = {}
        current_room.inventory[item_name] = item
        print(f"\nVous avez déposé l'item '{item_name}' ici.\n")
        return True

    # Wrappers compatibles avec l’API existante (game, list_of_words, number_of_parameters)
    def take(game, list_of_words, number_of_parameters=None):
        return Actions._take_simple(game, list_of_words)

    def drop(game, list_of_words, number_of_parameters=None):
        return Actions._drop_simple(game, list_of_words)

    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        # Si le nombre de paramètres est incorrect, affiche un message d’erreur et renvoie False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Afficher toutes les quêtes
        game.player.quest_manager.show_quests()
        return True
    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        # Si le nombre de paramètres est incorrect, affiche un message d’erreur et renvoie False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Obtenir le titre de la quête dans la liste des mots (joindre tous les mots après la commande)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Afficher les détails de la quête
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True

    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
            # Si le nombre de paramètres est incorrect, affiche un message d’erreur et renvoie False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Attendez-vous à un identifiant numérique pour la quête
        param = list_of_words[1]
        try:
            quest_id = int(param)
        except ValueError:
            print(f"\nLe paramètre doit être le numéro de la quête (ex: activate 2).\n")
            return False

        # Activer la quête par id
        success = game.player.quest_manager.activate_quest_by_id(quest_id)
        if not success:
            print(f"\nQuête avec l'id {quest_id} non trouvée ou déjà activée.\n")
        return success

    @staticmethod
    def je(game, list_of_words, number_of_parameters):
        # validation minimale
        if len(list_of_words) < 3:
            print("\nUsage: je m'appelle <prenom>\n")
            return False

        player = game.player
        # modèle de vérification : le deuxième jeton peut être « m’appelle » ou « mappelle »
        if list_of_words[1].lower() not in ("m'appelle", "mappelle"):
            print("\nUsage: je m'appelle <prenom>\n")
            return False

        name = " ".join(list_of_words[2:]).strip()
        if not name:
            print("\nIndiquez un prénom après 'je m'appelle'.\n")
            return False

        player.custom_name = name
        player.waiting_for_name = False
        # trouvez le PNJ avec lequel nous conversons
        pnj_name = player.conversation_with
        player.conversation_with = None

        # répondre en tant que Jean Bomber si pertinent
        if pnj_name == 'jean bomber' or pnj_name == 'jean bomber':
            print(f"\nJean Bomber : ça marche ! Moi c'est Jean Bomber !")
            print("Jean Bomber : Laisse moi t'y emmener")
            # trouver la chambre de Marcel Dassault
            target = None
            for r in game.rooms:
                if r.name == 'Marcel Dassault':
                    target = r
                    break
            if target:
                # déplacer le joueur à Marcel
                player.current_room = target
                player.history.append(target)
                # déplacez Jean Bomber dans cette pièce également s’il est présent quelque part
                for room in game.rooms:
                    if 'jean bomber' in getattr(room, 'characters', {}):
                        pnj = room.characters.pop('jean bomber')
                        target.characters['jean bomber'] = pnj
                        pnj.current_room = target
                        break
                # récit
                print("\nVous foncez pour ouvrir la porte comme vous a indiqué jean bomber à qui vous faites confiance... la porte s'ouvre à la volée et vous trébuchez sur un carton rempli de cours de statistiques. Vous vous étendez de tout votre long devant 200 élèves interloqués de votre soudaine apparition...")
                print(f"Jean Bomber : C'est ici le club musique {player.custom_name}")
                print("La conversation s'achève.")
                # proposer choix
                print("1. S'excuser et écouter le cours")
                print("2. Repartir péniblement")
                ch = input("> ").strip().lower()
                if "1" in ch or "s'excuser" in ch or "ecouter" in ch or "écouter" in ch:
                    print("Vous vous excusez et décidez d'écouter le cours.")
                else:
                    print("Vous repartez péniblement.")
            else:
                print("Impossible de trouver la salle 'Marcel Dassault'.")

        return True

    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        # Si le nombre de paramètres est incorrect, affiche un message d’erreur et renvoie False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Afficher les récompenses
        game.player.quest_manager.show_rewards()
        # Si le joueur a tué le Demogorgon, montrez l’accomplissement et terminez la partie
        try:
            rewards = getattr(game.player, 'rewards', []) or []
            if "Tuer le Démogorgon" in rewards:
                print("\nAccomplissement : Vous avez tué le Démogorgon.\n"
                      "Vous vous demandez si tout cela n'était qu'un rêve...\n"
                      "Le jeu se termine ici.")
                game.finished = True
        except Exception:
            pass
        return True