from typing import List, Optional
from interfaces.XSDFileInterface import XSDFileInterface
from XML import XML
from Inconsistency import Inconsistency
from SecurityManager import SecurityManager
from AuditLogger import AuditLogger
from Element import Element

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
        if not self.path:
            raise ValueError("Le chemin du fichier est invalide.")
        self.load_from_file(self.path)

    def validate(self, xml_file: XML) -> bool:
        """Valide le schéma XSD par rapport à des règles définies."""
        valid = bool()
        xml_elements = xml_file.get_elements()
        xsd_elements = self.get_elements()
        for xml_element in xml_elements:
            matching_xsd_element = next((xsd_element for xsd_element in xsd_elements if xsd_element.name == xml_element.name))
            if not matching_xsd_element:
                print(f"L'élément {xml_element.name} n'est pas défini dans le schéma XSD.")
                valid = False
            if not matching_xsd_element.validate_constraints():
                print(f"L'élément {xml_element.name} ne correspond pas à sa description dans le schéma XSD.")
                valid = False
            valid = True
        return valid

    def get_elements(self) -> List['Element']:
        """Retourne la liste des éléments définis dans le XSD."""
        # On peut envisager d'utiliser la méthode de la classe parente
        return super().get_elements()  # Appel à la méthode de la classe parente

    def compare(self, other: 'XSDFile') -> List[Inconsistency]:
        """Va comparer le fichier XSD à un autre fichier XSD passé en paramètre"""
        inconsistencies = []
        # Comparaison des noms
        if self.name != other.name:
            inconsistencies.append(Inconsistency("Les noms ne correspondent pas."))
            print('Les noms ne correspondent pas')
        # Comparaison des éléments racines
        if self.root_element.name != other.root_element.name:
            inconsistencies.append(Inconsistency(f"Les noms des éléments racines ne correspondent pas: {self.root_element.name} vs {other.root_element.name}"))
        # Comparaison des enfants de l'élément racine
        self_children = {child.name: child for child in self.root_element.children}
        other_children = {child.name: child for child in other.root_element.children}
        # Vérification des éléments manquants dans l'un ou l'autre XSD
        for child_name in set(self_children.keys()).union(other_children.keys()):
            if child_name not in self_children:
                inconsistencies.append(Inconsistency(f"L'élément '{child_name}' est manquant dans le premier fichier XSD."))
                print(f"L'élément '{child_name}' est manquant dans le premier fichier XSD.")
            elif child_name not in other_children:
                inconsistencies.append(Inconsistency(f"L'élément '{child_name}' est manquant dans le second fichier XSD."))
                (f"L'élément '{child_name}' est manquant dans le second fichier XSD.")
            else:
                # Comparaison des propriétés des éléments
                self_child = self_children[child_name]
                other_child = other_children[child_name]

                if self_child.type != other_child.type:
                    inconsistencies.append(Inconsistency(f"Les types de l'élément '{child_name}' diffèrent: {self_child.type} vs {other_child.type}"))
                    print(f"Les types de l'élément '{child_name}' diffèrent: {self_child.type} vs {other_child.type}")
                if self_child.minOccurs != other_child.minOccurs:
                    inconsistencies.append(Inconsistency(f"Différence sur l'occurence minimum pour l'élément '{child_name}': {self_child.minOccurs} vs {other_child.minOccurs}"))
                    print(f"Différence sur l'occurence minimum pour l'élément '{child_name}': {self_child.minOccurs} vs {other_child.minOccurs}")
                if self_child.maxOccurs != other_child.maxOccurs:
                    inconsistencies.append(Inconsistency(f"Différence sur l'occurence maximum pour l'élément '{child_name}': {self_child.maxOccurs} vs {other_child.maxOccurs}"))
                    print(f"Différence sur l'occurence maximum pour l'élément '{child_name}': {self_child.maxOccurs} vs {other_child.maxOccurs}")
                # Comparaison des attributs
                self_attributes = {attr.name: attr for attr in self_child.attributes}
                other_attributes = {attr.name: attr for attr in other_child.attributes}
                for attr_name in set(self_attributes.keys()).union(other_attributes.keys()):
                    if attr_name not in self_attributes:
                        inconsistencies.append(Inconsistency(f"L'attribut '{attr_name}' est manquant dans l'élément '{child_name}' du premier fichier XSD."))
                        print(f"L'attribut '{attr_name}' est manquant dans l'élément '{child_name}' du premier fichier XSD.")
                    elif attr_name not in other_attributes:
                        inconsistencies.append(Inconsistency(f"L'attribut '{attr_name}' est manquant dans l'élément '{child_name}' du second fichier XSD."))
                        print(f"L'attribut '{attr_name}' est manquant dans l'élément '{child_name}' du second fichier XSD.")
                    else:
                        self_attr = self_attributes[attr_name]
                        other_attr = other_attributes[attr_name]

                        if self_attr.type != other_attr.type:
                            inconsistencies.append(Inconsistency(f"Les types de l'attribut '{attr_name}' dans l'élément '{child_name}' diffèrent: {self_attr.type} vs {other_attr.type}"))
                            print(f"Les types de l'attribut '{attr_name}' dans l'élément '{child_name}' diffèrent: {self_attr.type} vs {other_attr.type}")

                        if self_attr.restrictions != other_attr.restrictions:
                            inconsistencies.append(Inconsistency(f"Les restrictions de l'attribut '{attr_name}' dans l'élément '{child_name}' diffèrent: {self_attr.restrictions} vs {other_attr.restrictions}"))
                            print(f"Les restrictions de l'attribut '{attr_name}' dans l'élément '{child_name}' diffèrent: {self_attr.restrictions} vs {other_attr.restrictions}")
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