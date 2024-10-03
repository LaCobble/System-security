import json
import bcrypt
import getpass
import hashlib
import os
from interfaces.SecurityManagerInterface import SecurityManagerInterface

class SecurityManager(SecurityManagerInterface):
    def __init__(self, passwords_file: str = 'passwords.json'):
        try:
            with open(passwords_file, 'r') as f:
                self.stored_passwords = json.load(f)
        except FileNotFoundError:
            self.stored_passwords = {}

    def check_access(self, username: str, file: str) -> bool:
        """Vérifie si l'utilisateur a accès au fichier."""
        if username in self.stored_passwords:
            print(f"Access granted for {username} to file: {file}")
            return True
        else:
            print(f"Access denied for {username} to file: {file}")
            return False

    def validate_integrity(self, file: str, expected_hash: str) -> bool:
        """Valide l'intégrité d'un fichier en comparant son hachage."""
        if not os.path.isfile(file):
            print(f"File {file} does not exist.")
            return False

        # Calculer le hachage du fichier
        hasher = hashlib.sha256()
        with open(file, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)

        file_hash = hasher.hexdigest()

        # Comparer le hachage du fichier avec le hachage attendu
        if file_hash == expected_hash:
            print(f"File integrity validated for {file}.")
            return True
        else:
            print(f"File integrity compromised for {file}. Expected: {expected_hash}, Found: {file_hash}.")
            return False

    def authenticate_user(self, username: str) -> bool:
        """Authentifie l'utilisateur en demandant un mot de passe."""
        if username in self.stored_passwords:
            password = getpass.getpass(f"Enter password for {username}: ")
            stored_hashed_password = self.stored_passwords[username]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                print(f"User {username} authenticated successfully.")
                return True
            else:
                print(f"Failed authentication for user {username}.")
        else:
            print(f"User {username} not found.")
        return False

    def add_user(self, username: str):
        """Ajoute un nouvel utilisateur avec double vérification du mot de passe."""
        if username in self.stored_passwords:
            print(f"User {username} already exists.")
            return

        # Double saisie sécurisée du mot de passe pour confirmation
        password = getpass.getpass("Enter new password: ")
        confirm_password = getpass.getpass("Confirm new password: ")

        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            return

        # Hachage du mot de passe
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.stored_passwords[username] = hashed_password
        self._save_passwords()
        print(f"User {username} added successfully.")

    def _save_passwords(self):
        """Sauvegarde les mots de passe chiffrés dans le fichier."""
        with open('passwords.json', 'w') as f:
            json.dump(self.stored_passwords, f)
