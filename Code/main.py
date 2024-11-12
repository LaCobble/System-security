# main.py
from XSDFile import XSDFile
from SecurityManager import SecurityManager
from AuditLogger import AuditLogger
from Inconsistency import Inconsistency

def scenario_1(security_manager, audit_logger):
    """Scénario 1 : Chargement et comparaison réussis avec des fichiers identiques"""
    try:
        xsd_file_1 = XSDFile("./xsd_file_1.xsd", "schema1", "1.0", security_manager, audit_logger, name="Schema1")
        xsd_file_2 = XSDFile("./xsd_file_2.xsd", "schema1", "1.0", security_manager, audit_logger, name="Schema1")

        # Chargement des fichiers
        xsd_file_1.load()
        xsd_file_2.load()

        # Validation des fichiers
        if not xsd_file_1.validate() or not xsd_file_2.validate():
            print("Validation failed. Access denied.")
            return

        # Comparaison des fichiers
        inconsistencies = xsd_file_1.compare(xsd_file_2)

        # Affichage des incohérences
        if inconsistencies:
            print("Inconsistencies found:")
            for inconsistency in inconsistencies:
                print(f"- {inconsistency}")
        else:
            print("No inconsistencies found, files are identical.")

    except Exception as e:
        print(f"Error during processing: {e}")

def scenario_2(security_manager, audit_logger):
    """Scénario 2 : Chargement échoué avec un fichier XSD non trouvé"""
    try:
        # Remplacez le chemin par un fichier XSD invalide
        xsd_file_3 = XSDFile("invalid_path_to_xsd.xsd", "schema3", "1.0", security_manager, audit_logger, name="Schema3")
        xsd_file_3.load()  # Cela devrait provoquer une erreur de chemin

    except Exception as e:
        print(f"Expected error for invalid path: {e}")

def scenario_3(security_manager, audit_logger):
    """Scénario 3 : Incohérences détectées"""
    try:
        # Remplacez les chemins par des fichiers XSD qui présentent des incohérences
        xsd_file_3 = XSDFile("xsd_file_1.xsd", "schema3", "1.0", security_manager, audit_logger, name="Schema3")
        xsd_file_4 = XSDFile("xsd_file_3.xsd", "schema4", "1.0", security_manager, audit_logger, name="Schema4")

        # Chargement des fichiers
        xsd_file_3.load()
        xsd_file_4.load()

        # Validation des fichiers
        if not xsd_file_3.validate() or not xsd_file_4.validate():
            print("Validation failed. Access denied.")
            return

        # Comparaison des fichiers
        inconsistencies = xsd_file_3.compare(xsd_file_4)

        # Affichage des incohérences
        if inconsistencies:
            print("Inconsistencies found:")
            for inconsistency in inconsistencies:
                print(f"- {inconsistency}")
        else:
            print("No inconsistencies found, files are identical.")

    except Exception as e:
        print(f"Error during processing: {e}")

def main():
    # Configuration des objets nécessaires
    security_manager = SecurityManager()
    audit_logger = AuditLogger()

    # Menu pour choisir le scénario
    print("Choisissez un scénario:")
    print("1: Chargement et comparaison réussis (fichiers identiques)")
    print("2: Chargement échoué (fichier non trouvé)")
    print("3: Incohérences détectées")

    choice = input("Entrez votre choix (1-3): ")

    if choice == '1':
        scenario_1(security_manager, audit_logger)
    elif choice == '2':
        scenario_2(security_manager, audit_logger)
    elif choice == '3':
        scenario_3(security_manager, audit_logger)
    else:
        print("Choix invalide. Veuillez entrer un numéro entre 1 et 3.")

if __name__ == "__main__":
    main()
