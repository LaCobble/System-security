from abc import ABC, abstractmethod
from typing import List
from Inconsistency import Inconsistency

class ElementInterface(ABC):
    @abstractmethod
    def validate_constraints(self) -> bool:
        """Valide les contraintes de l'élément."""
        pass

    @abstractmethod
    def compare(self, other: 'IElement') -> List[Inconsistency]:
        """Compare l'élément actuel avec un autre élément."""
        pass

    @abstractmethod
    def to_xml(self) -> str:
        """Convertit l'élément en chaîne XML."""
        pass
