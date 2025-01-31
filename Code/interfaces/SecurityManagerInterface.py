from abc import ABC, abstractmethod

class SecurityManagerInterface(ABC):
    @abstractmethod
    def check_access(self, user: str, file: str) -> bool:
        """Vérifie si l'utilisateur a accès au fichier."""
        pass

    @abstractmethod
    def validate_integrity(self, file: str, expected_hash: str) -> bool:
        """Vérifie l'intégrité du fichier."""
        pass

    @abstractmethod
    def authenticate_user(self, user: str, password: str) -> bool:
        """Authentifie l'utilisateur."""
        pass
