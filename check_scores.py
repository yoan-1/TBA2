"""Script pour afficher les scores Pylint de chaque fichier."""
import subprocess

files = ["room.py", "item.py", "command.py", "character.py", "player.py", "quest.py"]

print("=== SCORES PYLINT PAR FICHIER ===\n")

for file in files:
    result = subprocess.run(
        ["pylint", file],
        capture_output=True,
        text=True
    )
    
    for line in result.stdout.split('\n'):
        if 'rated' in line:
            print(f"{file:20} : {line.strip()}")
            break
