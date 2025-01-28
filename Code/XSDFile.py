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
                 name: str = ""):  # Ajoutez un paramètre name
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
        xml_element = self.load_from_file(self.path)
        #self.root_element = self._element_from_xml(xml_element)

    def validate(self) -> bool:
        """Valide le schéma XSD par rapport à des règles définies."""
        # Utiliser les vérifications de sécurité si nécessaire
        if not self.security_manager.check_access(self.path):
            return False

        # Logique de validation ici
        return True  # Placeholder

    def get_elements(self) -> List['Element']:
        """Retourne la liste des éléments définis dans le XSD."""
        # On peut envisager d'utiliser la méthode de la classe parente
        return super().get_elements()  # Appel à la méthode de la classe parente

    def compare(self, other: 'XSDFile') -> List[Inconsistency]:
        inconsistencies = []
        if self.name != other.name:
            inconsistencies.append(Inconsistency("Les noms ne correspondent pas."))
        return inconsistencies

    def log_action(self, action: str) -> None:
        """Enregistre une action via le AuditLogger."""
        self.audit_logger.log(action)

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