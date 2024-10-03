from interfaces.AttributeInterface import AttributeInterface

class Attribute(AttributeInterface):
    def __init__(self, name: str, type: str, restrictions: str):
        self.name = name
        self.type = type
        self.restrictions = restrictions

    def validate(self) -> bool:
        """Valide l'attribut en fonction de ses restrictions."""
        if 'length' in self.restrictions:
            max_length = int(self.restrictions.split('=')[1])
            if len(self.name) > max_length:
                return False
        return True

    def compare(self, other: AttributeInterface) -> bool:
        """Compare l'attribut actuel avec un autre attribut."""
        return self.name != other.name or self.type != other.type

    def to_xml(self) -> str:
        """Convertit l'attribut en chaîne XML."""
        return f"{self.name}=\"{self.type}\""
