import unittest
from unittest.mock import MagicMock, patch
from XSDFile import XSDFile
from XML import XML

class TestXSDFile(unittest.TestCase):

    def setUp(self):
        """Configurer une instance de XSDFile pour les tests."""
        self.security_manager = MagicMock()
        self.audit_logger = MagicMock()

        # Simulez le chargement d'un fichier XML
        self.xsd_file = XSDFile(
            path="dummy_path.xsd",
            schema="<schema></schema>",
            version="1.0",
            security_manager=self.security_manager,
            audit_logger=self.audit_logger,
            name="dummy_file"
        )

        # Utiliser patch pour simuler load_from_file
        with patch.object(XML, 'load_from_file') as mock_load_from_file:
            # Simuler un élément XML valide
            mock_xml_element = MagicMock()
            mock_xml_element.tag = "root"  # Simuler un tag valide
            mock_load_from_file.return_value = mock_xml_element

            # Charger le fichier XSD fictif
            self.xsd_file.load()  # Cela devrait maintenant initialiser root_element

    def test_load(self):
        """Teste la méthode load."""
        with patch.object(XML, 'load_from_file') as mock_load_from_file:
            # Simuler un élément XML valide
            mock_xml_element = MagicMock()
            mock_xml_element.tag = "root"  # Simuler un tag valide
            mock_load_from_file.return_value = mock_xml_element

            self.xsd_file.load()  # Appel de la méthode load

            # Vérifiez que root_element n'est pas None après le chargement
            self.assertIsNotNone(self.xsd_file.root_element, "root_element doit être initialisé après le chargement.")

            # Assurez-vous que la méthode de chargement du parent a été appelée
            mock_load_from_file.assert_called_once_with(self.xsd_file.path)

    def test_validate_access_denied(self):
        """Teste la méthode validate avec accès refusé."""
        self.security_manager.check_access.return_value = False

        result = self.xsd_file.validate()
        self.assertFalse(result)

    def test_validate_success(self):
        """Teste la méthode validate avec succès."""
        self.security_manager.check_access.return_value = True

        result = self.xsd_file.validate()
        self.assertTrue(result)

    def test_get_elements(self):
        """Teste la méthode get_elements."""
        elements = self.xsd_file.get_elements()
        self.assertEqual(elements, self.xsd_file.root_element.children)

    def test_compare(self):
        """Teste la méthode compare."""
        other_xsd_file = XSDFile(
            path="other_path.xsd",
            schema="<schema></schema>",
            version="1.0",
            security_manager=self.security_manager,
            audit_logger=self.audit_logger,
            name="dummy_file"  # Utilisez le même nom
        )

        # Assurez-vous que les deux XSDFile ont des attributs compatibles pour le test
        self.xsd_file.schema = other_xsd_file.schema
        self.xsd_file.version = other_xsd_file.version
        self.xsd_file.name = other_xsd_file.name  # Assurez-vous que le nom est également le même

        inconsistencies = self.xsd_file.compare(other_xsd_file)
        self.assertEqual(inconsistencies, [])  # Aucune incohérence attendue

    def test_log_action(self):
        """Teste la méthode log_action."""
        action = "Validation effectuée"
        self.xsd_file.log_action(action)

        self.audit_logger.log.assert_called_once_with(action)

if __name__ == '__main__':
    unittest.main()
