import unittest
from Inconsistency import Inconsistency
from Attribute import Attribute
from Element import Element

class TestInconsistency(unittest.TestCase):

    def setUp(self):
        """Configurer les incohérences pour les tests."""
        self.attribute = Attribute("name", "string", "")
        self.element = Element("parent", "string", 1, 1)

        self.inconsistency_full = Inconsistency(
            description="Attribut manquant",
            element=self.element,
            attribute=self.attribute
        )

        self.inconsistency_partial = Inconsistency(
            description="Nom différent"
        )

    def test_inconsistency_creation(self):
        """Teste la création d'une incohérence."""
        self.assertEqual(self.inconsistency_full.description, "Attribut manquant")
        self.assertEqual(self.inconsistency_full.element, self.element)
        self.assertEqual(self.inconsistency_full.attribute, self.attribute)

    def test_inconsistency_string_representation(self):
        """Teste la représentation sous forme de chaîne de l'incohérence."""
        expected_str = f"Inconsistency(description={self.inconsistency_full.description}, element={self.element}, attribute={self.attribute})"
        self.assertEqual(str(self.inconsistency_full), expected_str)

        expected_str_partial = "Inconsistency(description=Nom différent, element=None, attribute=None)"
        self.assertEqual(str(self.inconsistency_partial), expected_str_partial)

    def test_inconsistency_with_none_attributes(self):
        """Teste la création d'une incohérence avec des attributs None."""
        inconsistency_none = Inconsistency("Test sans attributs")
        self.assertIsNone(inconsistency_none.element)
        self.assertIsNone(inconsistency_none.attribute)

if __name__ == '__main__':
    unittest.main()
