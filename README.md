# TBA - Jeu d'Aventure Textuel avec Système de Quêtes

Cette branche contient une version du jeu d'aventure TBA (Text-Based Adventure) avec un système de quêtes intégré.

## Description

TBA est un jeu d'aventure textuel où le joueur explore différents lieux et accomplit des quêtes via des commandes textuelles.

**État actuel du projet (branche `tba-quests`) :**
- 6 lieux explorables
- Navigation par directions cardinales (N, E, S, O)
- **Système de quêtes complet** avec objectifs et récompenses
- Gestion des quêtes actives et complétées
- Suivi automatique de la progression des objectifs
- Statistiques de déplacement du joueur

Cette version introduit un système de quêtes qui enrichit considérablement l'expérience de jeu et sert de base pour des mécaniques plus complexes.

## Lancement du jeu

Pour démarrer le jeu, exécuter simplement :
```bash
python game.py
```

## Commandes disponibles

### Commandes de base
- `help` : Afficher l'aide et la liste des commandes
- `quit` : Quitter le jeu
- `go <direction>` : Se déplacer dans une direction (N, E, S, O)

### Commandes de quêtes
- `quests` : Afficher la liste de toutes les quêtes disponibles
- `quest <titre>` : Afficher les détails d'une quête spécifique
- `activate <titre>` : Activer une quête pour commencer à la suivre

## Système de Quêtes

Le système de quêtes permet de :
- Définir des objectifs à accomplir
- Suivre automatiquement la progression
- Gérer plusieurs quêtes simultanément
- Obtenir des récompenses à la completion

**Types d'objectifs disponibles :**
- Objectifs de visite : visiter un lieu spécifique
- Objectifs de compteur : effectuer une action un certain nombre de fois (ex: se déplacer 10 fois)

## Structuration

Le projet est organisé en 6 modules contenant chacun une ou plusieurs classes :

### Modules principaux

- **`game.py` / `Game`** : Gestion de l'état du jeu, de l'environnement et de l'interface avec le joueur
- **`room.py` / `Room`** : Propriétés génériques d'un lieu (nom, description, sorties)
- **`player.py` / `Player`** : Représentation du joueur avec gestion des déplacements et intégration du QuestManager
- **`command.py` / `Command`** : Structure des commandes avec leurs paramètres et actions associées
- **`actions.py` / `Actions`** : Méthodes statiques définissant toutes les actions exécutables (déplacements, gestion des quêtes, etc.)
- **`quest.py`** : 
  - `Quest` : Représentation d'une quête avec ses objectifs
  - `Objective` : Classe de base pour les objectifs
  - `RoomObjective` : Objectif de visite d'un lieu
  - `CounterObjective` : Objectif basé sur un compteur
  - `QuestManager` : Gestionnaire des quêtes du joueur

## Architecture

Le jeu utilise une architecture orientée objet avec gestion d'événements :

1. **Game** initialise le jeu et les quêtes disponibles
2. **Player** contient un `QuestManager` qui suit les quêtes actives
3. **QuestManager** vérifie automatiquement la progression lors des actions du joueur
4. **Objectives** définissent différents types de conditions à remplir
