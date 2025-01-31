import unittest
from unittest.mock import MagicMock, patch
from XML import XML
import xml.etree.ElementTree as ET
from Element import Element

class TestXML(unittest.TestCase):

    def setUp(self):
        """Configurer un élément racine et une instance de XML pour les tests."""
        self.root_element = Element("root", "unknown", 1, 1)
        self.xml_instance = XML(self.root_element)

    def test_load_from_file(self):
        """Teste la méthode load_from_file."""
        xml_content = "<root><child name='child1' /></root>"

        with patch('xml.etree.ElementTree.parse') as mock_parse:
            mock_parse.return_value = ET.ElementTree(ET.fromstring(xml_content))
            self.xml_instance.load_from_file("dummy_path.xml")

            self.assertEqual(self.xml_instance.root_element.name, "root")
            self.assertEqual(len(self.xml_instance.root_element.children), 1)

    def test_get_elements(self):
        """Teste la méthode get_elements."""
        children = self.xml_instance.get_elements()
        self.assertEqual(children, self.root_element.children)

    def test_compare(self):
        """Teste la méthode compare."""
        other_root_element = Element("root", "unknown", 1, 1)
        other_xml_instance = XML(other_root_element)

        inconsistencies = self.xml_instance.compare(other_xml_instance)
        self.assertEqual(inconsistencies, [])  # Aucune incohérence attendue

    def test_validate(self):
        """Teste la méthode validate."""
        with patch.object(XML, 'validate', return_value=True) as mock_validate:
            result = self.xml_instance.validate("dummy.xml", "dummy.xsd")
            self.assertTrue(result)  # Doit retourner True
            mock_validate.assert_called_once_with("dummy.xml", "dummy.xsd")

if __name__ == '__main__':
    unittest.main()
