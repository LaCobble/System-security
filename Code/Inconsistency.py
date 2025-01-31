from interfaces.InconsistencyInterface import InconsistencyInterface
from Attribute import Attribute

class Inconsistency(InconsistencyInterface):
    def __init__(self, description: str, element: 'Element' = None, attribute: 'Attribute' = None, message: str = ""):
        self.description = description
        self.element = element
        self.attribute = attribute
        self.message = message

    def __str__(self) -> str:
        return f"Inconsistency(description={self.description}, element={self.element}, attribute={self.attribute})"

    def __repr__(self):
        return f"Inconsistency(description={self.description}, element={self.element}, attribute={self.attribute})"