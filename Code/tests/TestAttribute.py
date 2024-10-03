import unittest
from Attribute import Attribute

class TestAttribute(unittest.TestCase):

    def setUp(self):
        """Configurer les attributs pour les tests."""
        self.valid_attribute = Attribute("username", "string", "length=20")
        self.invalid_attribute = Attribute("long_username_exceeding_limit", "string", "length=20")
        self.attribute1 = Attribute("age", "int", "")
        self.attribute2 = Attribute("age", "int", "")
        self.different_attribute = Attribute("name", "string", "")

    def test_validate_valid_attribute(self):
        """Teste la validation d'un attribut valide."""
        self.assertTrue(self.valid_attribute.validate(), "Valid attribute should return True")

    def test_validate_invalid_attribute(self):
        """Teste la validation d'un attribut invalide."""
        self.assertFalse(self.invalid_attribute.validate(), "Invalid attribute should return False")

    def test_compare_same_attributes(self):
        """Teste la comparaison d'attributs identiques."""
        self.assertFalse(self.attribute1.compare(self.attribute2), "Identical attributes should return False")

    def test_compare_different_attributes(self):
        """Teste la comparaison d'attributs différents."""
        self.assertTrue(self.attribute1.compare(self.different_attribute), "Different attributes should return True")

    def test_to_xml(self):
        """Teste la conversion d'un attribut en chaîne XML."""
        expected_xml = 'username="string"'
        self.assertEqual(self.valid_attribute.to_xml(), expected_xml, "XML representation is incorrect")

if __name__ == '__main__':
    unittest.main()
