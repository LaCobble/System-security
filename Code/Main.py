import sys
import argparse
import getpass
import json
import os
from typing import List
from XSDFile import XSDFile
from XML import XML
from SecurityManager import SecurityManager
from AuditLogger import AuditLogger
import xml.etree.ElementTree as ET

PASSWORD_FILE = "passwords.json"

class XMLValidationApp:
    """Application de validation de fichiers XML et XSD avec gestion des utilisateurs."""
    def __init__(self):
        """Initialise l'application avec un SecurityManager et un AuditLogger."""
        self.security_manager = SecurityManager()
        self.audit_logger = AuditLogger()

    def validate_xml_against_xsd(self, xsd_path: str, xml_path: str, user: str):
        """Valide un fichier XML par rapport à un fichier XSD avec gestion des accès utilisateurs."""
        if not self.security_manager.check_access(user, xsd_path):
            print(f"🚫 Accès refusé pour {user} au fichier {xsd_path}")
            self.audit_logger.log_error(f"Accès refusé pour {user} au fichier {xsd_path}")
            return

        try:
            print(f"\n🔍 Début de la validation : {xml_path} contre {xsd_path}")

            print(f"📂 Chargement du fichier XSD : {xsd_path}")
            xsd_file = XSDFile(xsd_path, '', '1.0', self.security_manager, self.audit_logger)
            xsd_file.load()
            print(f"✅ Fichier XSD chargé avec succès : {xsd_file.path}")

            print(f"📂 Chargement du fichier XML : {xml_path}")
            xml_file = XML(None)
            xml_file.load_from_file(xml_path)
            print(f"✅ Fichier XML chargé avec succès")

            print(f"⚖️  Lancement de la validation...")
            if not xsd_file.validate(xml_file):
                print(f"❌ Échec de validation : {xsd_path} ❌ {xml_path}")
                self.audit_logger.log_error(f"Échec de validation : {xsd_path} ❌ {xml_path}")
            else:
                print(f"✅ Validation réussie : {xml_path} respecte {xsd_path}")
                self.audit_logger.log_event(f"Validation réussie : {xml_path} respecte {xsd_path}")

        except Exception as e:
            error_details = str(e)
            self.audit_logger.log_error(f"Erreur lors de la validation : {error_details}")
            print(f"❌ Erreur lors de la validation : {error_details}")

    def compare_xsd_versions(self, xsd_path1: str, xsd_path2: str, user: str):
        """Compare deux versions de fichiers XSD et vérifie les droits d'accès."""
        if not self.security_manager.check_access(user, xsd_path1) or not self.security_manager.check_access(user, xsd_path2):
            print(f"🚫 Accès refusé pour {user} à {xsd_path1} ou {xsd_path2}")
            self.audit_logger.log_error(f"Accès refusé pour {user} à {xsd_path1} ou {xsd_path2}")
            return

        try:
            print(f"\n🔍 Début de la comparaison : {xsd_path1} vs {xsd_path2}")
            xsd_file1 = XSDFile(xsd_path1, '', '1.0', self.security_manager, self.audit_logger)
            xsd_file1.load()
            xsd_file2 = XSDFile(xsd_path2, '', '1.0', self.security_manager, self.audit_logger)
            xsd_file2.load()

            print(f"⚖️  Lancement de la comparaison...")
            inconsistencies = xsd_file1.compare(xsd_file2)

            if inconsistencies:
                print("\n🔎 Différences détectées :")
                for inc in inconsistencies:
                    print(f"- {inc}")  # ✅ Correction : Affichage direct de l'incohérence
                    self.audit_logger.log_event(f"Incohérence détectée : {inc}")
            else:
                print("✅ Aucune différence détectée.")
                self.audit_logger.log_event(f"Aucune incohérence entre {xsd_path1} et {xsd_path2}")

        except Exception as e:
            error_details = str(e)
            self.audit_logger.log_error(f"Erreur lors de la comparaison des XSD : {error_details}")
            print(f"❌ Erreur lors de la comparaison : {error_details}")

    def add_user(self, username: str):
        """Ajoute un nouvel utilisateur via le SecurityManager."""
        try:
            self.security_manager.add_user(username)
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout de l'utilisateur {username} : {e}")
            self.audit_logger.log_error(f"Erreur lors de l'ajout de {username}: {str(e)}")

    def remove_user(self, username: str):
        """Supprime un utilisateur existant."""
        users = self.load_users()
        if username in users:
            del users[username]
            self.save_users(users)
            print(f"✅ Utilisateur {username} supprimé avec succès.")
        else:
            print(f"❌ L'utilisateur {username} n'existe pas.")

    def load_users(self):
        """Charge les utilisateurs depuis le fichier JSON."""
        if not os.path.exists(PASSWORD_FILE):
            return {}
        with open(PASSWORD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_users(self, users):
        """Sauvegarde les utilisateurs dans le fichier JSON."""
        with open(PASSWORD_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Outil de validation et comparaison de fichiers XSD et XML avec gestion des utilisateurs')
    parser.add_argument('--validate', nargs=3, metavar=('XSD', 'XML', 'USER'), help='Valider un fichier XML contre un XSD avec utilisateur')
    parser.add_argument('--compare', nargs=3, metavar=('XSD1', 'XSD2', 'USER'), help='Comparer deux fichiers XSD avec utilisateur')
    parser.add_argument('--add-user', metavar='USERNAME', help='Ajouter un nouvel utilisateur')
    parser.add_argument('--remove-user', metavar='USERNAME', help='Supprimer un utilisateur')

    args = parser.parse_args()
    app = XMLValidationApp()

    if args.validate:
        xsd_path, xml_path, user = args.validate
        app.validate_xml_against_xsd(xsd_path, xml_path, user)
    elif args.compare:
        xsd_path1, xsd_path2, user = args.compare
        app.compare_xsd_versions(xsd_path1, xsd_path2, user)
    elif args.add_user:
        app.add_user(args.add_user)
    elif args.remove_user:
        app.remove_user(args.remove_user)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
