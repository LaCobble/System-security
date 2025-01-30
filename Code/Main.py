import sys
import argparse
from typing import List
from XSDFile import XSDFile
from XML import XML
from SecurityManager import SecurityManager
from AuditLogger import AuditLogger
from Inconsistency import Inconsistency
import xml.etree.ElementTree as ET

class XMLValidationApp:
    def __init__(self):
        self.security_manager = SecurityManager()
        self.audit_logger = AuditLogger()

    def validate_xml_against_xsd(self, xsd_path: str, xml_path: str) -> List[Inconsistency]:
        """
        Valide un fichier XML par rapport à un fichier XSD.
        
        Args:
            xsd_path (str): Chemin du fichier XSD
            xml_path (str): Chemin du fichier XML
        
        Returns:
            List[Inconsistency]: Liste des incohérences détectées
        """
        try:
            # Vérification des accès
            if not self.security_manager.check_access('admin', xsd_path):
                self.audit_logger.log_error(f"Accès refusé au fichier XSD : {xsd_path}")

            # Charger le XSD
            xsd_file = XSDFile(xsd_path, '', '1.0', self.security_manager, self.audit_logger)
            xsd_file.load()
            # Charger le XML
            xml_file = XML(None)
            xml_file.load_from_file(xml_path)
            # Validation
            if not xsd_file.validate(xml_file):
                self.audit_logger.log_error(f"Échec de validation pour {xsd_path} ou {xml_path}")
                print(f"Échec de validation pour {xsd_path} ou {xml_path}")
            else:
                self.audit_logger.log_event(f"Fichier {xml_path} validé avec succès !")
                print(f"Fichier {xml_file} validé avec succès !")
        except Exception as e:
            self.audit_logger.log_error(f"Erreur lors de la validation : {str(e)}")

    def compare_xsd_versions(self, xsd_path1: str, xsd_path2: str) -> List[Inconsistency]:
        """
        Compare deux versions de fichiers XSD.
        
        Args:
            xsd_path1 (str): Chemin du premier fichier XSD
            xsd_path2 (str): Chemin du second fichier XSD
        
        Returns:
            List[Inconsistency]: Liste des incohérences détectées
        """
        try:
            # Charger les XSD
            xsd_file1 = XSDFile(
                path=xsd_path1, 
                schema='', 
                version='1.0', 
                security_manager=self.security_manager, 
                audit_logger=self.audit_logger,
                name=xsd_path1
            )
            xsd_file2 = XSDFile(
                path=xsd_path2, 
                schema='', 
                version='1.0', 
                security_manager=self.security_manager, 
                audit_logger=self.audit_logger,
                name=xsd_path2
            )
            xsd_file1.load()
            xsd_file2.load()
            # Comparer les XSD
            inconsistencies = xsd_file1.compare(xsd_file2)
            
            # Journaliser les incohérences
            for inc in inconsistencies:
                self.audit_logger.log_error(str(inc))

            return inconsistencies

        except Exception as e:
            self.audit_logger.log_error(f"Erreur lors de la comparaison des XSD : {str(e)}")
            return []

def main():
    parser = argparse.ArgumentParser(description='Outil de validation et comparaison de fichiers XSD et XML')
    parser.add_argument('--validate', nargs=2, metavar=('XSD', 'XML'), help='Valider un fichier XML contre un XSD')
    parser.add_argument('--compare', nargs=2, metavar=('XSD1', 'XSD2'), help='Comparer deux fichiers XSD')

    args = parser.parse_args()

    app = XMLValidationApp()

    if args.validate:
        xsd_path, xml_path = args.validate
        app.validate_xml_against_xsd(xsd_path, xml_path)

    elif args.compare:
        xsd_path1, xsd_path2 = args.compare
        inconsistencies = app.compare_xsd_versions(xsd_path1, xsd_path2)
        print(inconsistencies)
        if len(inconsistencies) == 0:
            print("Aucune différence détectée")
        else: 
            print("Différences entre les versions XSD :")
            for inc in inconsistencies:
                print(str(inc))

    else:
        parser.print_help()

if __name__ == '__main__':
    main()