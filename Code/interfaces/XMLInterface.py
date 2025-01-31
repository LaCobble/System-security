from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

class XMLInterface(ABC):
    @abstractmethod
    def load_from_file(self, path: str) -> None:
        """Charge un fichier XML à partir d'un chemin spécifié."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Valide l'instance XML par rapport à un fichier XSD."""
        pass

    @abstractmethod
    def get_elements(self) -> List['Element']:
        """Retourne la liste des éléments dans l'instance XML."""
        pass

    @abstractmethod
    def compare(self, other: 'XMLInterface') -> List['Inconsistency']:
        """Compare l'instance actuelle avec une autre instance de XML."""
        pass
