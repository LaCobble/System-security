import unittest
from Element import Element
from Attribute import Attribute

class TestElement(unittest.TestCase):

    def setUp(self):
        """Configurer les éléments pour les tests."""
        self.attribute1 = Attribute("id", "string", "")
        self.attribute2 = Attribute("name", "string", "length=50")
        self.child_element = Element("child", "string", 1, 1, [self.attribute1])
        self.parent_element = Element("parent", "string", 1, 1, [self.attribute2], [self.child_element])

    def test_validate_constraints_valid(self):
        """Teste la validation avec des valeurs valides."""
        self.assertTrue(self.parent_element.validate_constraints(), "Should be valid")

    def test_validate_constraints_invalid(self):
        """Teste la validation avec des valeurs invalides."""
        self.parent_element.minOccurs = -1  # Rendre invalide
        self.assertFalse(self.parent_element.validate_constraints(), "Should be invalid")

    def test_compare_different_name(self):
        """Teste la comparaison avec des noms différents."""
        other_element = Element("other", "string", 1, 1)
        inconsistencies = self.parent_element.compare(other_element)
        self.assertGreater(len(inconsistencies), 0, "Should have inconsistencies due to name mismatch")

    def test_compare_different_type(self):
        """Teste la comparaison avec des types différents."""
        other_element = Element("parent", "int", 1, 1)
        inconsistencies = self.parent_element.compare(other_element)
        self.assertGreater(len(inconsistencies), 0, "Should have inconsistencies due to type mismatch")

    def test_compare_different_minOccurs(self):
        """Teste la comparaison avec des minOccurs différents."""
        other_element = Element("parent", "string", 0, 1)
        inconsistencies = self.parent_element.compare(other_element)
        self.assertGreater(len(inconsistencies), 0, "Should have inconsistencies due to minOccurs mismatch")

    def test_compare_missing_attribute(self):
        """Teste la comparaison avec un attribut manquant."""
        other_element = Element("parent", "string", 1, 1, [self.attribute2])
        inconsistencies = self.parent_element.compare(other_element)
        self.assertGreater(len(inconsistencies), 0, "Should have inconsistencies due to missing attribute")

    def test_compare_missing_child(self):
        """Teste la comparaison avec un enfant manquant."""
        other_element = Element("parent", "string", 1, 1, [self.attribute2])
        inconsistencies = self.parent_element.compare(other_element)
        self.assertGreater(len(inconsistencies), 0, "Should have inconsistencies due to missing child")

    def test_to_xml(self):
        """Teste la conversion en chaîne XML."""
        expected_xml = '<parent name="string"><child id="string"/></parent>'
        self.assertEqual(self.parent_element.to_xml(), expected_xml, "XML representation is incorrect")

if __name__ == '__main__':
    unittest.main()
