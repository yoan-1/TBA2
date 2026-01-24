"""Supprimer les lignes vides finales."""
with open('game.py', 'r', encoding='utf-8') as f:
    content = f.read().rstrip()

with open('game.py', 'w', encoding='utf-8') as f:
    f.write(content + '\n')

print("✓ Lignes vides finales supprimées")
