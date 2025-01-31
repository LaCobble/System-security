from typing import List, Optional
from interfaces.XSDFileInterface import XSDFileInterface
from XML import XML
from Inconsistency import Inconsistency
from SecurityManager import SecurityManager
from AuditLogger import AuditLogger
from Element import Element
import xml.etree.ElementTree as ET
import os

class XSDFile(XML):
    def __init__(self, path: str, schema: str, version: str, 
                 security_manager: 'SecurityManager', 
                 audit_logger: 'AuditLogger', 
                 name: str = ""): 
        root_element = None
        namespaces = {}
        super().__init__(root_element, namespaces)

        self.path = path
        self.schema = schema
        self.version = version
        self.security_manager = security_manager
        self.audit_logger = audit_logger
        self.name = name

    def load(self):
        """Charge le fichier XSD et parse son contenu."""
        if os.stat(self.path).st_size == 0:
            raise ValueError(f"Erreur : Le fichier XSD {self.path} est vide.")            
            return
        
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if not first_line.startswith("<"):
                    raise ValueError(f"Erreur : Le fichier {self.path} n'est pas un fichier XSD valide.")

            tree = ET.parse(self.path)
            self.root = tree.getroot()
        except ET.ParseError as e:
            self.root = None
            raise ValueError(f"Erreur de parsing du XSD {self.path} : {e}")

    def validate(self, xml_file: XML) -> bool:
        """Valide un fichier XML contre ce schéma XSD."""
        valid = True  # Supposons que le fichier est valide par défaut
        xml_elements = xml_file.get_elements()
        xsd_elements = self.get_elements()

        # Vérification de la correspondance entre XML et XSD
        for xml_element in xml_elements:
            try:
                matching_xsd_element = next((xsd_element for xsd_element in xsd_elements if xsd_element.name == xml_element.name), None)

                if not matching_xsd_element:
                    print(f"❌ ERREUR : L'élément '{xml_element.name}' n'est pas défini dans le schéma XSD.")
                    valid = False
                    continue  # On continue pour vérifier les autres éléments

                if not matching_xsd_element.validate_constraints():
                    print(f"❌ ERREUR : L'élément '{xml_element.name}' ne respecte pas les contraintes définies dans le XSD.")
                    valid = False

            except Exception as e:
                print(f"❌ ERREUR INTERNE : {e}")
                valid = False

        return valid

    def get_elements(self) -> List[Element]:
        """Récupère tous les éléments définis dans le fichier XSD."""
        if self.root is None:
            return []
        
        namespaces = {'xs': 'http://www.w3.org/2001/XMLSchema'}
        elements = self.root.findall(".//xs:element", namespaces)

        unique_elements = {}
        for el in elements:
            name = el.get("name")
            if name and name not in unique_elements:
                min_occurs = el.get("minOccurs", "1")  # Valeur par défaut 1 si non spécifiée
                max_occurs = el.get("maxOccurs", "1")  # Valeur par défaut 1 si non spécifiée

                unique_elements[name] = Element(
                    name=name, 
                    type=el.get("type", "xs:string"), 
                    minOccurs=int(min_occurs) if min_occurs.isdigit() else min_occurs, 
                    maxOccurs=int(max_occurs) if max_occurs.isdigit() else max_occurs
                )

        return list(unique_elements.values())  # Retourner une liste sans doublons

    def compare(self, other_xsd: 'XSDFile') -> List[Inconsistency]:
        """Compare ce fichier XSD avec un autre et retourne les différences."""
        inconsistencies = []

        # Debug : Vérifier que les fichiers ont bien des éléments
        self_elements = self.get_elements()
        other_elements = other_xsd.get_elements()

        print("📌 DEBUG : Éléments dans", self.path)
        for el in self_elements:
            print(f"  - {el.name}")

        print("📌 DEBUG : Éléments dans", other_xsd.path)
        for el in other_elements:
            print(f"  - {el.name}")

        if self.root is None or other_xsd.root is None:
            return [Inconsistency(f"Erreur : un des fichiers XSD est vide ou invalide.", None, None)]

        if not self_elements or not other_elements:
            inconsistencies.append(Inconsistency("Erreur : un des fichiers XSD n'a pas été chargé correctement.", None, None))
            return inconsistencies

        # Comparaison des éléments
        for element in self_elements:
            if element.name not in [e.name for e in other_elements]:
                inconsistencies.append(Inconsistency(f"Élément supprimé : {element.name}", element, None))

        for element in other_elements:
            if element.name not in [e.name for e in self_elements]:
                inconsistencies.append(Inconsistency(f"Élément ajouté : {element.name}", element, None))

        return inconsistencies

    def log_action(self, action: str) -> None:
        """Enregistre une action via le AuditLogger."""
        self.audit_logger.log_event(action)

    def set_security(self, security_manager: SecurityManager, audit_logger: AuditLogger) -> None:
        """Définit le SecurityManager pour le XSDFile."""
        self.security_manager = security_manager
        self.audit_logger = audit_logger
        
    def set_schema(self, schema: str):
        """Définit le schéma pour le XSDFile."""
        self.schema = schema
    def set_version(self, version: str):
        """Définit la version pour le XSDFile."""
        self.version = version