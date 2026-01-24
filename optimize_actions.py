"""Script pour optimiser actions.py pour Pylint."""
import re

def optimize_actions():
    """Optimiser actions.py pour Pylint."""
    with open('actions.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Ajouter un docstring de module
    if not content.startswith('"""'):
        module_docstring = '"""Module d\'actions pour le jeu.\n\nCe module contient la classe Actions avec toutes les commandes\nexécutables par le joueur.\n"""\n\n'
        # Trouver où commencent les commentaires actuels
        first_line_idx = content.find('#')
        if first_line_idx != -1:
            # Insérer le docstring avant les commentaires
            content = module_docstring + content
    
    # 2. Déplacer les imports en haut
    # Extraire MSG0 et MSG1
    msg0_match = re.search(r'MSG0 = "[^"]+"\n', content)
    msg1_match = re.search(r'MSG1 = "[^"]+"\n', content)
    
    # Trouver les imports
    from_item_match = re.search(r'from item import Item\n', content)
    import_uni_match = re.search(r'import unicodedata\n', content)
    
    if from_item_match and import_uni_match:
        # Retirer les imports de leur position actuelle
        content = content.replace('from item import Item\n', '')
        content = content.replace('import unicodedata\n', '')
        
        # Les ajouter après le docstring de module
        # Trouver la fin du docstring de module
        if content.startswith('"""'):
            end_docstring = content.find('"""\n', 3) + 4
            imports_section = 'import unicodedata\nfrom item import Item\n\n'
            content = content[:end_docstring] + imports_section + content[end_docstring:]
    
    # 3. Supprimer trailing whitespace
    lines = content.split('\n')
    lines = [line.rstrip() for line in lines]
    content = '\n'.join(lines)
    
    # 4. S'assurer qu'il y a une newline finale
    if not content.endswith('\n'):
        content += '\n'
    
    # 5. Ajouter docstring à la classe Actions
    content = content.replace(
        'class Actions:\n    # Cette méthode permet',
        'class Actions:\n    """Classe contenant toutes les actions disponibles pour le joueur."""\n\n    # Cette méthode permet'
    )
    
    # Écrire le fichier optimisé
    with open('actions.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Étape 1 : Docstring de module, imports et classe optimisés")

if __name__ == '__main__':
    optimize_actions()
