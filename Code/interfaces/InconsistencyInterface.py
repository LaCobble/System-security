from abc import ABC, abstractmethod

class InconsistencyInterface(ABC):
    @abstractmethod
    def __str__(self) -> str:
        """Retourne une représentation sous forme de chaîne de l'incohérence."""
        pass
