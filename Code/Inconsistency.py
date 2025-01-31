from interfaces.InconsistencyInterface import InconsistencyInterface
from Attribute import Attribute

class Inconsistency(InconsistencyInterface):
    """Représente une incohérence entre deux éléments XML."""
    def __init__(self, description: str, element: 'Element' = None, attribute: 'Attribute' = None, message: str = ""):
        """Initialise une incohérence avec une description, un élément, un attribut et un message."""
        self.description = description
        self.element = element
        self.attribute = attribute
        self.message = message

    def __str__(self) -> str:
        """Représentation textuelle simplifiée de l'instance."""
        return f"Inconsistency(description={self.description}, element={self.element}, attribute={self.attribute})"
