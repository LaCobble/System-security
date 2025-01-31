import unittest
import os
import xml.etree.ElementTree as ET
from unittest.mock import MagicMock
from XSDFile import XSDFile
from AuditLogger import AuditLogger
from SecurityManager import SecurityManager

class TestXSDFile(unittest.TestCase):
    def setUp(self):
        """Initialisation des objets avant chaque test."""
        self.security_manager = MagicMock(spec=SecurityManager)
        self.audit_logger = MagicMock(spec=AuditLogger)
        self.audit_logger.log = MagicMock()
        self.temp_xsd_path = "test_temp.xsd"
        with open(self.temp_xsd_path, "w", encoding="utf-8") as f:
            f.write("""<?xml version="1.0"?>
            <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                <xs:element name="Person" type="xs:string"/>
                <xs:element name="FirstName" type="xs:string"/>
            </xs:schema>""")

        self.xsd_file = XSDFile(self.temp_xsd_path, "", "1.0", self.security_manager, self.audit_logger)
        self.xsd_file.load()

    def tearDown(self):
        """Suppression du fichier temporaire après chaque test."""
        if os.path.exists(self.temp_xsd_path):
            os.remove(self.temp_xsd_path)

    def test_load(self):
        """Teste la méthode load."""
        self.assertIsNotNone(self.xsd_file.root_element, "root_element doit être initialisé après le chargement.")

    def test_get_elements(self):
        """Teste la méthode get_elements."""
        elements = self.xsd_file.get_elements()

        self.assertIn("Person", elements)
        self.assertIn("FirstName", elements)

    def test_validate_success(self):
        """Teste la méthode validate avec succès."""
        mock_xml = MagicMock()
        mock_xml.get_elements.return_value = ["Person", "FirstName"]
        self.security_manager.check_access.return_value = True

        result = self.xsd_file.validate(mock_xml)

        self.assertTrue(result, "La validation devrait réussir.")

    def test_validate_access_denied(self):
        """Teste la méthode validate avec accès refusé."""
        mock_xml = MagicMock()
        self.security_manager.check_access.return_value = False

        result = self.xsd_file.validate(mock_xml)
        self.assertFalse(result)

    def test_compare(self):
        """Teste la méthode compare."""
        other_xsd = MagicMock()
        other_xsd.get_elements.return_value = ["Person", "FirstName", "LastName"]

        inconsistencies = self.xsd_file.compare(other_xsd)
        self.assertIn("Élément ajouté : LastName", inconsistencies)

    def test_log_action(self):
        """Teste la méthode log_action."""
        action = "Test action"
        self.xsd_file.log_action(action)
        self.audit_logger.log.assert_called_once_with(action)

if __name__ == "__main__":
    unittest.main()
