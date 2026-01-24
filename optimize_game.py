"""Script pour optimiser game.py pour Pylint."""

def clean_trailing_whitespace(filename):
    """Supprime les espaces blancs en fin de ligne."""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = [line.rstrip() + '\n' for line in lines]
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    print(f"✓ Espaces blancs supprimés dans {filename}")

if __name__ == '__main__':
    clean_trailing_whitespace('game.py')
