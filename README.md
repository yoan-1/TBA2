# TBA - Jeu d'Aventure Textuel - Interface graphique

Ce repository contient la une version minimale du jeu d'aventure TBA (Text-Based Adventure) avec une interface graphique.

## Description

TBA est un jeu d'aventure textuel avec interface graphique (Tkinter) où le joueur explore différents lieux et interagit avec l'environnement via des commandes textuelles.

**État actuel du projet :**
- 6 lieux explorables
- Navigation par directions cardinales (N, E, S, O)
- Interface graphique avec Tkinter
- Système de commandes extensible
- Images et icônes pour améliorer l'expérience visuelle

Cette version sert à introduire la notion d'interface graphique, et doit être utilisée pour améliorer le jeu que vous êtes en train de développer.

## Prérequis

- Python 3.x
- Tkinter (inclus avec Python)

## Installation

Pour récupérer la branche :

```bash
git fetch upstream
git switch tba-tk
```

## Lancement du jeu

Pour démarrer le jeu, exécuter simplement :
```bash
python game.py
```

Le jeu s'ouvrira dans une fenêtre graphique avec une interface utilisateur.

On peut toujours exécuter le jeu dans un terminal:
```bash
python game.py --cli
```

## Commandes disponibles

Les commandes disponibles sont les commandes initiales :

- `help` : Afficher l'aide et la liste des commandes
- `quit` : Quitter le jeu
- `go <direction>` : Se déplacer dans une direction (N, E, S, O)

Il faut intégrer les commandes additionnelles

## Structure du projet initial

Le projet est organisé en 5 modules Python, chacun contenant une classe principale :

### Modules principaux

- **`game.py` / `Game`** : Classe qui gère l'état du jeu
- **`game.py` / `GameGUI`** : Classe qui gère l'interface graphique Tkinter
- **`room.py` / `Room`** : Définit les propriétés génériques d'un lieu (nom, description, sorties, image)
- **`player.py` / `Player`** : Représente le joueur, gère sa position actuelle et ses déplacements
- **`command.py` / `Command`** : Structure les commandes disponibles avec leurs paramètres et actions associées
- **`actions.py` / `Actions`** : Contient les méthodes statiques qui définissent les actions exécutables (déplacements, aide, quitter)

### Dossier assets

Le dossier `assets/` contient les ressources graphiques :
- Icônes de navigation (flèches directionnelles)
- Icônes d'aide et de sortie

On peut modifier les sources SVG avec ``Inkscape`` et convertir en PNG avec ``convert``.

## Architecture

Le jeu utilise une architecture orientée objet :

1. **Game** initialise et orchestre le jeu
2. **Room** représente chaque lieu avec ses connexions
3. **Player** garde la trace de la position du joueur
4. **Command** encapsule les commandes utilisateur
5. **Actions** implémente les interactions avec le joueur


