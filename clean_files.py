"""Nettoyer les espaces blancs dans quest.py et player.py."""

def clean_file(filename):
    """Supprime les espaces en fin de ligne."""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(filename, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line.rstrip() + '\n')
    
    print(f"✓ {filename} nettoyé")

clean_file('quest.py')
clean_file('player.py')
