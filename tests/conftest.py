"""
Configuration de base pour les tests pytest
"""
import pytest
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

@pytest.fixture
def root_dir():
    """Retourne le répertoire racine du projet"""
    return ROOT_DIR

@pytest.fixture
def modules_dir(root_dir):
    """Retourne le répertoire des modules"""
    return root_dir

