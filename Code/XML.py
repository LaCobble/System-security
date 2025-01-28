from interfaces.XMLInterface import XMLInterface
from typing import List, Dict, Optional
from Attribute import Attribute
from Element import Element
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element as EL
from Inconsistency import Inconsistency

class XML(XMLInterface):
    def __init__(self, root_element: 'Element', namespaces: Optional[Dict[str, str]] = None):
        self.root_element = root_element
        self.namespaces = namespaces if namespaces is not None else {}  # Correction ici

    def load_from_file(self, path: str) -> None:
        """Charge un fichier XML à partir d'un chemin spécifié."""
        tree = ET.parse(path)
        root = tree.getroot()
        self.root_element = self._element_from_xml(root)  # Assurez-vous que cela initialise root_element

    def _element_from_xml(self, xml_element: EL) -> Element:
        """Convertit un élément XML en une instance de Element."""
        name = xml_element
        type = "unknown"
        minOccurs = 1
        maxOccurs = 1
        attributes = [Attribute(attr, "string", "") for attr in xml_element.attrib.keys()]
        children = [self._element_from_xml(child) for child in xml_element]
        return Element(name, type, minOccurs, maxOccurs, attributes, children)

    def validate(self, xml_path: str, xsd_path: str) -> bool:
        """Valide l'instance XML par rapport à un fichier XSD."""
        pass

    def get_elements(self) -> List['Element']:
        """Retourne la liste des éléments dans l'instance XML."""
        return self.root_element.children

    def compare(self, other: 'XML') -> List['Inconsistency']:
        """Compare l'instance actuelle avec une autre instance de XML."""
        inconsistencies = []
        inconsistencies.extend(self.root_element.compare(other.root_element))
        return inconsistencies
