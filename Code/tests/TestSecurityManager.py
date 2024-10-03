import unittest
import os
import hashlib
import json
from unittest import mock
from SecurityManager import SecurityManager

class TestSecurityManager(unittest.TestCase):

    def setUp(self):
        self.password = 'p@ssword'

        # Supprimer le fichier de mots de passe s'il existe
        if os.path.isfile('passwords.json'):
            os.remove('passwords.json')

        # Créer un nouveau fichier
        with open('passwords.json', 'w') as f:
            f.write('{}')

        self.manager = SecurityManager('passwords.json')

        # Ajout d'un utilisateur avec un mot de passe connu
        with mock.patch('getpass.getpass', side_effect=[self.password, self.password]):
            self.manager.add_user("testuser")

        # Création d'un fichier de test
        with open('test_file.txt', 'wb') as f:
            f.write(b'This is a test file.')

    def tearDown(self):
        # Supprimer le fichier temporaire après le test
        if os.path.isfile('test_file.txt'):
            os.remove('test_file.txt')

    def test_add_user_and_authenticate(self):
        """Teste l'ajout d'un utilisateur et son authentification avec un prompt."""
        with mock.patch('getpass.getpass', side_effect=[self.password, self.password]):
            self.manager.add_user("testuser")

            # Vérifiez le contenu de passwords.json pour voir si l'utilisateur a été ajouté correctement
            with open('passwords.json', 'r') as f:
                passwords = json.load(f)
                print("Stored passwords:", passwords)  # Affiche les mots de passe stockés

            self.assertTrue(self.manager.authenticate_user("testuser"))

    def test_authenticate_unknown_user(self):
        """Teste l'authentification d'un utilisateur inconnu."""
        self.assertFalse(self.manager.authenticate_user("unknown_user"))

    def test_authenticate_with_wrong_password(self):
        """Teste l'authentification avec un mot de passe incorrect."""
        # Simuler l'authentification de l'utilisateur avec un mot de passe incorrect
        with mock.patch('getpass.getpass', return_value='wrong_password'):
            self.assertFalse(self.manager.authenticate_user("testuser"))

    def test_check_access(self):
        """Teste la vérification d'accès à un fichier."""
        self.assertTrue(self.manager.check_access("testuser", "test_file.txt"))
        self.assertFalse(self.manager.check_access("unknown_user", "test_file.txt"))

    def test_validate_integrity(self):
        """Teste la validation de l'intégrité d'un fichier."""
        # Calculer le hachage attendu pour le fichier de test
        hasher = hashlib.sha256()
        with open('test_file.txt', 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        expected_hash = hasher.hexdigest()

        self.assertTrue(self.manager.validate_integrity('test_file.txt', expected_hash))
        self.assertFalse(self.manager.validate_integrity('test_file.txt', 'invalidhash'))

if __name__ == '__main__':
    unittest.main()
