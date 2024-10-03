from abc import ABC, abstractmethod
from typing import List

class XSDFileInterface(ABC):
    @abstractmethod
    def load(self) -> None:
        """Charge le fichier XSD à partir du chemin spécifié."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Valide le schéma par rapport à des règles définies."""
        pass

    @abstractmethod
    def compare(self, other: 'XSDFile') -> List[str]:
        """Compare l'instance actuelle avec une autre instance de XSDFile et retourne une liste d'incohérences."""
        pass

    @abstractmethod
    def log_action(self, action: str) -> None:
        """Enregistre une action via l'AuditLogger."""
        pass
