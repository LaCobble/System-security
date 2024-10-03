from abc import ABC, abstractmethod

class AttributeInterface(ABC):
    @abstractmethod
    def validate(self) -> bool:
        """Valide l'attribut en fonction de ses restrictions."""
        pass

    @abstractmethod
    def compare(self, other: 'AttributeInterface') -> bool:
        """Compare l'attribut actuel avec un autre attribut."""
        pass

    @abstractmethod
    def to_xml(self) -> str:
        """Convertit l'attribut en chaîne XML."""
        pass
