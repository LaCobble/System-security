from interfaces.XMLInterface import XMLInterface
from typing import List, Dict, Optional
from Attribute import Attribute
from Element import Element
import xml.etree.ElementTree as ET

class XML(XMLInterface):
    def __init__(self, root_element: 'Element', namespaces: Optional[Dict[str, str]] = None):
        self.root_element = root_element
        self.namespaces = namespaces if namespaces is not None else {}  # Correction ici

    def load_from_file(self, path):
        try:
            tree = ET.parse(path)
            return tree.getroot()  # Renvoie l'élément racine
        except ET.ParseError as e:
            print(f"Erreur d'analyse : {e}")
            return None
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier : {e}")
            return None

    def _element_from_xml(self, xml_element: ET.Element) -> 'Element':
        """Convertit un élément XML en une instance de Element."""
        name = xml_element.tag
        type = "unknown"
        minOccurs = 1
        maxOccurs = 1
        attributes = [Attribute(attr, "string", "") for attr in xml_element.attrib.keys()]
        children = [self._element_from_xml(child) for child in xml_element]
        return Element(name, type, minOccurs, maxOccurs, attributes, children)

    def validate(self) -> bool:
        """Valide l'instance XML par rapport à un fichier XSD."""
        # Logique de validation à implémenter selon les règles XSD
        return True  # Placeholder

    def get_elements(self) -> List['Element']:
        """Retourne la liste des éléments dans l'instance XML."""
        return self.root_element.children

    def compare(self, other: 'XML') -> List['Inconsistency']:
        """Compare l'instance actuelle avec une autre instance de XML."""
        inconsistencies = []
        inconsistencies.extend(self.root_element.compare(other.root_element))
        return inconsistencies
