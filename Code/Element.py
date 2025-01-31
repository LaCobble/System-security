from typing import List, Optional
from interfaces.ElementInterface import ElementInterface
from interfaces.AttributeInterface import AttributeInterface
from Inconsistency import Inconsistency

class Element(ElementInterface):
    """Représente un élément XML avec ses attributs et ses enfants."""
    def __init__(self, name: str, type: str, minOccurs: int, maxOccurs: int,
                attributes: List[AttributeInterface] = None,
                children: List['Element'] = None):
        """Initialise un élément avec un nom, un type, des contraintes et des attributs/enfants."""
        self.name = name
        self.type = type
        self.minOccurs = minOccurs
        self.maxOccurs = maxOccurs
        self.attributes = attributes if attributes is not None else []
        self.children = children if children is not None else []

    def __repr__(self):
        """Représentation officielle de l'instance pour le débogage."""
        return f"Element(name='{self.name}', type='{self.type}', attributes='{self.attributes}', children='{self.children}')"

    def __str__(self):
        """Représentation textuelle simplifiée de l'instance."""
        return f"Element '{self.name}' de type '{self.type}', attributes='{self.attributes}', children='{self.children}'"

    def validate_constraints(self) -> bool:
        """Valide les contraintes de l'élément."""
        if self.minOccurs < 0 or self.maxOccurs < self.minOccurs:
            return False
        return True

    def compare(self, other: 'Element', path="Root") -> List[Inconsistency]:
        """Compare l'élément actuel avec un autre élément."""
        inconsistencies = []

        if self.name != other.name:
            inconsistencies.append(Inconsistency(f"Nom différent : {self.name} vs {other.name} ({path})"))

        if self.type != other.type:
            inconsistencies.append(Inconsistency(f"Type différent pour {self.name} ({path}) : {self.type} vs {other.type}"))

        el1_attributes = {attr.name: attr for attr in self.attributes}
        el2_attributes = {attr.name: attr for attr in other.attributes}

        for attr_name, attr in el1_attributes.items():
            if attr_name not in el2_attributes:
                inconsistencies.append(Inconsistency(f"Attribut supprimé : {attr_name} dans {self.name} ({path})"))
            elif el2_attributes[attr_name].type != attr.type:
                inconsistencies.append(Inconsistency(f"Type d'attribut modifié : {attr_name} ({path}) {attr.type} vs {el2_attributes[attr_name].type}"))

        for attr_name in el2_attributes:
            if attr_name not in el1_attributes:
                inconsistencies.append(Inconsistency(f"Attribut ajouté : {attr_name} dans {self.name} ({path})"))

        el1_children = {child.name: child for child in self.children}
        el2_children = {child.name: child for child in other.children}

        for child_name, child in el1_children.items():
            if child_name in el2_children:
                inconsistencies.extend(child.compare(el2_children[child_name], path=f"{path}/{child_name}"))
            else:
                inconsistencies.append(Inconsistency(f"Élément supprimé : {child_name} dans {self.name} ({path})"))

        for child_name in el2_children:
            if child_name not in el1_children:
                inconsistencies.append(Inconsistency(f"Élément ajouté : {child_name} dans {self.name} ({path})"))

        return inconsistencies

    def to_xml(self) -> str:
        """Convertit l'élément en chaîne XML."""
        attributes_xml = ' '.join(f'{attr.name}="{attr.type}"' for attr in self.attributes)
        children_xml = ''.join(child.to_xml() for child in self.children) if self.children else ""
        if self.children:
            return f'<{self.name} {attributes_xml}>{children_xml}</{self.name}>'
        else:
            return f'<{self.name} {attributes_xml}/>'
