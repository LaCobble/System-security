import os
import xml.etree.ElementTree as ET
from AuditLogger import AuditLogger
import re

class XSDFile:
    """Représente un fichier XSD et fournit des méthodes pour valider un fichier XML par rapport à ce XSD."""
    def __init__(self, path, schema, version, security_manager, audit_logger, name=""):
        """
        Initialise un fichier XSD avec ses paramètres.

        Args:
            path (str): Chemin du fichier XSD.
            schema (str): Contenu du schéma XSD (optionnel).
            version (str): Version du fichier XSD.
            security_manager: Gestionnaire de sécurité.
            audit_logger: Gestionnaire de journalisation.
            name (str): Nom du fichier XSD.
        """
        self.path = path
        self.schema = schema
        self.version = version
        self.security_manager = security_manager
        self.audit_logger = audit_logger
        self.name = name
        self.root = None 
        self.root_element = None

    def load(self):
        """
        Charge le fichier XSD et initialise root_element.
        """
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Le fichier XSD {self.path} est introuvable.")

        if os.stat(self.path).st_size == 0:
            raise ValueError(f"Erreur : Le fichier XSD {self.path} est vide.")

        try:
            tree = ET.parse(self.path)
            self.root = tree.getroot()
            self.root_element = self.root
        except ET.ParseError as e:
            raise ValueError(f"Erreur de parsing du fichier XSD {self.path} : {e}")

    def remove_namespace(self, tag):
        """Supprime le namespace d'un élément XML."""
        return tag.split("}")[-1]

    def get_elements(self):
        """Retourne une liste des éléments définis dans le XSD."""
        if self.root is None:
            return []
        return [el.get("name") for el in self.root.findall(".//xs:element", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"}) if el.get("name")]

    def validate(self, xml_file):
        """
        Valide un fichier XML par rapport au XSD.

        Args:
            xml_file (XML): Instance de XML contenant les éléments du fichier XML.

        Returns:
            bool: True si la validation est réussie, False sinon.
        """
        if not self.security_manager.check_access("admin", self.path):
            self.audit_logger.log_error(f"Accès refusé au fichier XSD : {self.path}")
            return False

        try:
            xsd_elements = self.get_elements()
            xml_elements = xml_file.get_elements()

            validation_result = all(elem in xsd_elements for elem in xml_elements)

            if validation_result:
                self.audit_logger.log_event(f"Validation réussie pour {xml_file.path} contre {self.path}")
            else:
                self.audit_logger.log_error(f"Validation échouée : {xml_file.path} ne correspond pas à {self.path}")

            return validation_result

        except Exception as e:
            self.audit_logger.log_error(f"Erreur lors de la validation : {str(e)}")
            return False

    def compare(self, other_xsd):
        """Compare les éléments XSD et détecte les différences."""
        self_elements = set(self.get_elements())
        other_elements = set(other_xsd.get_elements())

        added = other_elements - self_elements
        removed = self_elements - other_elements

        inconsistencies = []
        for el in added:
            inconsistencies.append(f"Élément ajouté : {el}")
            self.audit_logger.log_event(f"Incohérence détectée : Élément ajouté : {el}")

        for el in removed:
            inconsistencies.append(f"Élément supprimé : {el}")
            self.audit_logger.log_event(f"Incohérence détectée : Élément supprimé : {el}")

        return inconsistencies

    def log_action(self, action):
        """
        Enregistre une action dans le journal des événements.

        Args:
            action (str): Message décrivant l'action à journaliser.
        """
        self.audit_logger.log(action)
