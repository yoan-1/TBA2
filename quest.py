""" Define the Quest class"""

class Quest:
    """
    This class represents a quest in the game. A quest has a title, description,
    objectives, completion status, and optional rewards.
    
    Attributes:
        title (str): The title of the quest.
        description (str): The description of the quest.
        objectives (list): List of objectives to complete.
        is_completed (bool): Whether the quest is completed.
        is_active (bool): Whether the quest is currently active.
        reward (str): Optional reward for completing the quest.
    """


    def __init__(self, title, description, objectives=None, reward=None):
        """
        Initialize a new quest.
        
        Args:
            title (str): The title of the quest.
            description (str): The description of the quest.
            objectives (list): List of objectives (default: empty list).
            reward (str): Optional reward description.
            
        Examples:
        
        >>> quest = Quest("Test Quest", "A test quest", ["Objective 1", "Objective 2"], "Gold coin")
        >>> quest.title
        'Test Quest'
        >>> quest.is_active
        False
        >>> quest.is_completed
        False
        >>> len(quest.objectives)
        2
        """
        self.title = title
        self.description = description
        self.objectives = objectives if objectives is not None else []
        self.completed_objectives = []
        self.is_completed = False
        self.is_active = False
        self.reward = reward


    def activate(self):
        """
        Activate the quest.
        
        Examples:
        
        >>> quest = Quest("Adventure", "Go on an adventure")
        >>> quest.is_active
        False
        >>> quest.activate()
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Adventure
        📝 Go on an adventure
        <BLANKLINE>
        >>> quest.is_active
        True
        """
        self.is_active = True
        print(f"\n🗡️  Nouvelle quête activée: {self.title}")
        print(f"📝 {self.description}\n")


    def complete_objective(self, objective, player=None):
        """
        Mark an objective as completed.
        
        Args:
            objective (str): The objective to mark as completed.
            player: The player object (optional).
            
        Returns:
            bool: True if objective was found and completed, False otherwise.
            
        Examples:
        
        >>> quest = Quest("Hunt", "Hunt monsters", ["Kill 5 goblins", "Kill 3 orcs"])
        >>> quest.complete_objective("Kill 5 goblins")
        ✅ Objectif accompli: Kill 5 goblins
        True
        >>> len(quest.completed_objectives)
        1
        >>> quest.complete_objective("Kill 5 goblins")
        False
        >>> quest.complete_objective("Invalid objective")
        False
        """
        if objective in self.objectives and objective not in self.completed_objectives:
            self.completed_objectives.append(objective)
            print(f"✅ Objectif accompli: {objective}")

            # Check if all objectives are completed
            if len(self.completed_objectives) == len(self.objectives):
                self.complete_quest(player)

            return True
        return False


    def complete_quest(self, player=None):
        """
        Mark the quest as completed and give reward to player.
        
        Args:
            player: The player object to give the reward to (optional).
            
        Examples:
        
        >>> quest = Quest("Final Quest", "The last quest", ["Win"], "Trophy")
        >>> quest.is_completed
        False
        >>> quest.complete_quest() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🏆 Quête terminée: Final Quest
        🎁 Récompense: Trophy
        <BLANKLINE>
        >>> quest.is_completed
        True
        """
        if not self.is_completed:
            self.is_completed = True
            print(f"\n🏆 Quête terminée: {self.title}")
            if self.reward:
                print(f"🎁 Récompense: {self.reward}")
                if player:
                    player.add_reward(self.reward)
            print()


    def get_status(self):
        """
        Get the current status of the quest.
        
        Returns:
            str: A formatted string showing the quest status.
            
        Examples:
        
        >>> quest = Quest("Collect", "Collect items", ["Get sword", "Get shield"])
        >>> quest.get_status()
        '❓ Collect (Non activée)'
        >>> quest.activate()
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Collect
        📝 Collect items
        <BLANKLINE>
        >>> quest.get_status()
        '⏳ Collect (0/2 objectifs)'
        >>> quest.complete_objective("Get sword")
        ✅ Objectif accompli: Get sword
        True
        >>> quest.get_status()
        '⏳ Collect (1/2 objectifs)'
        """
        if not self.is_active:
            return f"❓ {self.title} (Non activée)"
        if self.is_completed:
            return f"✅ {self.title} (Terminée)"
        completed_count = len(self.completed_objectives)
        total_count = len(self.objectives)
        return f"⏳ {self.title} ({completed_count}/{total_count} objectifs)"


    def get_details(self, current_counts=None):
        """
        Get detailed information about the quest.
        
        Args:
            current_counts (dict): Optional dictionary with current counter values 
                                   (e.g., {"Se déplacer": 5})
        
        Returns:
            str: A formatted string with quest details.
            
        Examples:
        
        >>> quest = Quest("Travel", "Move around", ["Se déplacer 10 fois"], "Map")
        >>> details = quest.get_details({"Se déplacer": 5})
        >>> "Travel" in details
        True
        >>> "Progression: 5/10" in details
        True
        """
        details = f"\n📋 Quête: {self.title}\n"
        details += f"📖 {self.description}\n"

        if self.objectives:
            details += "\nObjectifs:\n"
            for objective in self.objectives:
                status = "✅" if objective in self.completed_objectives else "⬜"
                objective_text = self._format_objective_with_progress(objective, current_counts)
                details += f"  {status} {objective_text}\n"

        if self.reward:
            details += f"\n🎁 Récompense: {self.reward}\n"

        return details

    def _format_objective_with_progress(self, objective, current_counts):
        """
        Format an objective with progress information if available.
        
        Args:
            objective (str): The objective text.
            current_counts (dict): Dictionary with current counter values.
            
        Returns:
            str: Formatted objective text with progress if applicable.
        """
        if not current_counts:
            return objective

        for counter_name, current_count in current_counts.items():
            if counter_name not in objective:
                continue

            # Extract required count from objective
            required = self._extract_number_from_text(objective)
            if required is not None:
                return f"{objective} (Progression: {current_count}/{required})"

        return objective

    def _extract_number_from_text(self, text):
        """
        Extract the first number from a text string.
        
        Args:
            text (str): The text to search.
            
        Returns:
            int: The first number found, or None if no number exists.
        """
        for word in text.split():
            if word.isdigit():
                return int(word)
        return None


    def check_room_objective(self, room_name, player=None):
        """
        Check if visiting a specific room completes an objective.
        
        Args:
            room_name (str): The name of the room visited.
            player: The player object (optional).
            
        Returns:
            bool: True if an objective was completed, False otherwise.
            
        Examples:
        
        >>> quest = Quest("Explore", "Explore the castle", ["Visiter Castle"])
        >>> quest.check_room_objective("Castle")
        ✅ Objectif accompli: Visiter Castle
        <BLANKLINE>
        🏆 Quête terminée: Explore
        <BLANKLINE>
        True
        >>> quest.check_room_objective("Tower")
        False
        """
        room_objectives = [
            f"Visiter {room_name}",
            f"Explorer {room_name}",
            f"Aller à {room_name}",
            f"Entrer dans {room_name}"
        ]

        for objective in room_objectives:
            if self.complete_objective(objective, player):
                return True
        return False


    def check_action_objective(self, action, target=None, player=None):
        """
        Check if performing an action completes an objective.
        
        Args:
            action (str): The action performed (e.g., "parler", "prendre", "utiliser").
            target (str): Optional target of the action.
            player: The player object (optional).
            
        Returns:
            bool: True if an objective was completed, False otherwise.
            
        Examples:
        
        >>> quest = Quest("Talk", "Have a conversation", ["parler avec garde"])
        >>> quest.check_action_objective("parler", "garde") # doctest: +NORMALIZE_WHITESPACE
        ✅ Objectif accompli: parler avec garde
        <BLANKLINE>
        🏆 Quête terminée: Talk
        <BLANKLINE>
        True
        >>> quest.check_action_objective("courir", "vite")
        False
        """
        if target:
            objective_variations = [
                f"{action} {target}",
                f"{action} avec {target}",
                f"{action} le {target}",
                f"{action} la {target}"
            ]
        else:
            objective_variations = [action]

        for objective in objective_variations:
            if self.complete_objective(objective, player):
                return True
        return False


    def check_counter_objective(self, counter_name, current_count, player=None):
        """
        Check objectives that require counting (e.g., visit X rooms, collect Y items).
        
        Args:
            counter_name (str): The name of what is being counted.
            current_count (int): The current count.
            player: The player object (optional).
            
        Returns:
            bool: True if an objective was completed, False otherwise.
            
        Examples:
        
        >>> quest = Quest("Walker", "Walk a lot", ["Marcher 5 fois"])
        >>> quest.check_counter_objective("Marcher", 3)
        False
        >>> quest.check_counter_objective("Marcher", 5) # doctest: +ELLIPSIS
        ✅ Objectif accompli: Marcher 5 fois
        <BLANKLINE>
        🏆 Quête terminée: Walker
        <BLANKLINE>
        True
        """
        for objective in self.objectives:
            if counter_name in objective and objective not in self.completed_objectives:
                # Extract number from objective (e.g., "Visiter 3 lieux" -> 3)
                words = objective.split()
                for word in words:
                    if word.isdigit():
                        required_count = int(word)
                        if current_count >= required_count:
                            self.complete_objective(objective, player)
                            return True
        return False


    def __str__(self):
        """
        Return a string representation of the quest.
        
        Examples:
        
        >>> quest = Quest("String Test", "Test __str__", ["Task 1"])
        >>> str(quest)
        '❓ String Test (Non activée)'
        >>> quest.activate() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🗡️  Nouvelle quête activée: String Test
        📝 Test __str__
        <BLANKLINE>
        >>> str(quest)
        '⏳ String Test (0/1 objectifs)'
        """
        return self.get_status()


class QuestManager:
    """
    This class manages all quests in the game.
    
    Attributes:
        quests (list): List of all quests in the game.
        active_quests (list): List of currently active quests.
        player: Reference to the player object.
    """


    def __init__(self, player=None):
        """
        Initialize the quest manager.
        
        Args:
            player: The player object (optional, can be set later).
            
        Examples:
        
        >>> manager = QuestManager()
        >>> len(manager.quests)
        0
        >>> len(manager.active_quests)
        0
        """
        self.quests = []
        self.active_quests = []
        self.player = player


    def add_quest(self, quest):
        """
        Add a quest to the game.
        
        Args:
            quest (Quest): The quest to add.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Quest 1", "First quest")
        >>> manager.add_quest(quest)
        >>> len(manager.quests)
        1
        >>> manager.quests[0].title
        'Quest 1'
        """
        self.quests.append(quest)


    def activate_quest(self, quest_title):
        """
        Activate a quest by its title.
        
        Args:
            quest_title (str): The title of the quest to activate.
            
        Returns:
            bool: True if quest was found and activated, False otherwise.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Epic Quest", "An epic adventure")
        >>> manager.add_quest(quest)
        >>> manager.activate_quest("Epic Quest")
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Epic Quest
        📝 An epic adventure
        <BLANKLINE>
        True
        >>> len(manager.active_quests)
        1
        >>> manager.activate_quest("Unknown Quest")
        False
        """
        for quest in self.quests:
            if quest.title == quest_title and not quest.is_active:
                quest.activate()
                self.active_quests.append(quest)
                return True
        return False


    def complete_objective(self, objective_text):
        """
        Complete an objective in any active quest.
        
        Args:
            objective_text (str): The objective to complete.
            
        Returns:
            bool: True if objective was found and completed, False otherwise.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Manager Quest", "Test", ["Do something"])
        >>> manager.add_quest(quest)
        >>> manager.activate_quest("Manager Quest") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Manager Quest
        📝 Test
        <BLANKLINE>
        True
        >>> manager.complete_objective("Do something") # doctest: +NORMALIZE_WHITESPACE
        ✅ Objectif accompli: Do something
        <BLANKLINE>
        🏆 Quête terminée: Manager Quest
        <BLANKLINE>
        True
        >>> manager.complete_objective("Do nothing")
        False
        """
        for quest in self.active_quests:
            if quest.complete_objective(objective_text):
                # Remove completed quests from active list
                if quest.is_completed:
                    self.active_quests.remove(quest)
                return True
        return False


    def check_room_objectives(self, room_name):
        """
        Check all active quests for room-related objectives.
        
        Args:
            room_name (str): The name of the room visited.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Visit Places", "Visit rooms", ["Visiter Library"])
        >>> manager.add_quest(quest)
        >>> manager.activate_quest("Visit Places") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Visit Places
        📝 Visit rooms
        <BLANKLINE>
        True
        >>> manager.check_room_objectives("Library") # doctest: +NORMALIZE_WHITESPACE
        ✅ Objectif accompli: Visiter Library
        <BLANKLINE>
        🏆 Quête terminée: Visit Places
        <BLANKLINE>
        >>> len(manager.active_quests)
        0
        """
        for quest in self.active_quests[:]:  # Use slice to avoid modification during iteration
            quest.check_room_objective(room_name, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)


    def check_action_objectives(self, action, target=None):
        """
        Check all active quests for action-related objectives.
        
        Args:
            action (str): The action performed.
            target (str): Optional target of the action.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Actions", "Do actions", ["parler avec roi"])
        >>> manager.add_quest(quest)
        >>> manager.activate_quest("Actions") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Actions
        📝 Do actions
        <BLANKLINE>
        True
        >>> manager.check_action_objectives("parler", "roi") # doctest: +NORMALIZE_WHITESPACE
        ✅ Objectif accompli: parler avec roi
        <BLANKLINE>
        🏆 Quête terminée: Actions
        <BLANKLINE>
        >>> len(manager.active_quests)
        0
        """
        for quest in self.active_quests[:]:
            quest.check_action_objective(action, target, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)


    def check_counter_objectives(self, counter_name, current_count):
        """
        Check all active quests for counter-related objectives.
        
        Args:
            counter_name (str): The name of what is being counted.
            current_count (int): The current count.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Counter", "Count things", ["Compter 3 fois"])
        >>> manager.add_quest(quest)
        >>> manager.activate_quest("Counter") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Counter
        📝 Count things
        <BLANKLINE>
        True
        >>> manager.check_counter_objectives("Compter", 2)
        >>> len(manager.active_quests)
        1
        >>> manager.check_counter_objectives("Compter", 3) # doctest: +NORMALIZE_WHITESPACE
        ✅ Objectif accompli: Compter 3 fois
        <BLANKLINE>
        🏆 Quête terminée: Counter
        <BLANKLINE>
        >>> len(manager.active_quests)
        0
        """
        for quest in self.active_quests[:]:
            quest.check_counter_objective(counter_name, current_count, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)


    def get_active_quests(self):
        """
        Get all active quests.
        
        Returns:
            list: List of active quests.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Active Quest", "An active quest")
        >>> manager.add_quest(quest)
        >>> len(manager.get_active_quests())
        0
        >>> manager.activate_quest("Active Quest")
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Active Quest
        📝 An active quest
        <BLANKLINE>
        True
        >>> len(manager.get_active_quests())
        1
        """
        return self.active_quests


    def get_all_quests(self):
        """
        Get all quests.
        
        Returns:
            list: List of all quests.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest1 = Quest("Q1", "First")
        >>> quest2 = Quest("Q2", "Second")
        >>> manager.add_quest(quest1)
        >>> manager.add_quest(quest2)
        >>> len(manager.get_all_quests())
        2
        """
        return self.quests


    def get_quest_by_title(self, title):
        """
        Get a quest by its title.
        
        Args:
            title (str): The title of the quest.
            
        Returns:
            Quest: The quest if found, None otherwise.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest1 = Quest("Find Key", "Find the golden key")
        >>> quest2 = Quest("Open Door", "Open the locked door")
        >>> manager.add_quest(quest1)
        >>> manager.add_quest(quest2)
        >>> found = manager.get_quest_by_title("Find Key")
        >>> found.title
        'Find Key'
        >>> manager.get_quest_by_title("Unknown") is None
        True
        """
        for quest in self.quests:
            if quest.title == title:
                return quest
        return None


    def show_quests(self):
        """
        Display all quests and their status.
        
        Examples:
        
        >>> manager = QuestManager()
        >>> manager.show_quests()
        <BLANKLINE>
        Aucune quête disponible.
        <BLANKLINE>
        >>> quest = Quest("Display Quest", "Test display")
        >>> manager.add_quest(quest)
        >>> manager.show_quests() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        📋 Liste des quêtes:
        ❓ Display Quest (Non activée)
        <BLANKLINE>
        """
        if not self.quests:
            print("\nAucune quête disponible.\n")
            return

        print("\n📋 Liste des quêtes:")
        for quest in self.quests:
            print(f"  {quest.get_status()}")
        print()


    def show_quest_details(self, quest_title, current_counts=None):
        """
        Show detailed information about a specific quest.
        
        Args:
            quest_title (str): The title of the quest.
            current_counts (dict): Optional dictionary with current counter values.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Detail Quest", "Show details", ["Task"])
        >>> manager.add_quest(quest)
        >>> manager.show_quest_details("Detail Quest") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        📋 Quête: Detail Quest
        📖 Show details
        <BLANKLINE>
        Objectifs:
        ⬜ Task
        <BLANKLINE>
        >>> manager.show_quest_details("Unknown")
        <BLANKLINE>
        Quête 'Unknown' non trouvée.
        <BLANKLINE>
        """
        quest = self.get_quest_by_title(quest_title)
        if quest:
            print(quest.get_details(current_counts))
        else:
            print(f"\nQuête '{quest_title}' non trouvée.\n")
