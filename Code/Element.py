from typing import List, Optional
from interfaces.ElementInterface import ElementInterface
from interfaces.AttributeInterface import AttributeInterface
from Inconsistency import Inconsistency

class Element(ElementInterface):
    def __init__(self, name: str, type: str, minOccurs: int, maxOccurs: int,
                attributes: List[AttributeInterface] = None,
                children: List['Element'] = None):
        self.name = name
        self.type = type
        self.minOccurs = minOccurs
        self.maxOccurs = maxOccurs
        self.attributes = attributes if attributes is not None else []
        self.children = children if children is not None else []
        
    def __repr__(self):
        return f"Element(name='{self.name}', type='{self.type}', attributes='{self.attributes}', children='{self.children}')"

    def __str__(self):
        return f"Element '{self.name}' de type '{self.type}', attributes='{self.attributes}', children='{self.children}'"

    def validate_constraints(self) -> bool:
        """Valide les contraintes de l'élément."""
        if self.minOccurs < 0 or self.maxOccurs < self.minOccurs:
            return False
        return True

    def compare(self, other: ElementInterface) -> List[Inconsistency]:
        """Compare l'élément actuel avec un autre élément."""
        inconsistencies = []

        if self.name != other.name:
            inconsistencies.append(Inconsistency(f"Nom différent : {self.name} vs {other.name}", self))

        if self.type != other.type:
            inconsistencies.append(Inconsistency(f"Type différent : {self.type} vs {other.type}", self))

        if self.minOccurs != other.minOccurs:
            inconsistencies.append(Inconsistency(f"minOccurs différent : {self.minOccurs} vs {other.minOccurs}", self))

        if self.maxOccurs != other.maxOccurs:
            inconsistencies.append(Inconsistency(f"maxOccurs différent : {self.maxOccurs} vs {other.maxOccurs}", self))

        # Comparer les attributs
        for attribute in self.attributes:
            if attribute not in other.attributes:
                inconsistencies.append(Inconsistency(f"Attribut manquant : {attribute.name}", self, attribute))

        # Comparer les enfants
        for child in self.children:
            if child not in other.children:
                inconsistencies.append(Inconsistency(f"Élément enfant manquant : {child.name}", self))

        return inconsistencies

    def to_xml(self) -> str:
        """Convertit l'élément en chaîne XML."""
        attributes_xml = ' '.join(f'{attr.name}="{attr.type}"' for attr in self.attributes)
        children_xml = ''.join(child.to_xml() for child in self.children) if self.children else ""
        if self.children:
            return f'<{self.name} {attributes_xml}>{children_xml}</{self.name}>'
        else:
            return f'<{self.name} {attributes_xml}/>'
