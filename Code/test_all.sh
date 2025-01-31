#!/bin/bash

# Script Bash pour executer tous les tests automatiquement

# Definition des fichiers de test
XSD_BASE="Mi.xsd"
XSD_PRIME="Mi_prime.xsd"
XSD_DOUBLE_PRIME="Mi_double_prime.xsd"
XSD_EMPTY="empty.xsd"
XSD_INVALID="invalid.xsd"
XML_TEST="test.xml"
XML_INVALID="invalid.xml"
XSD_NOT_FOUND="not_found.xsd"
USER_NO_ACCESS="user1"
ADMIN_USER="admin"
EXISTING_USER="alice"

# Verification de l'existence des fichiers avant execution
files=("$XSD_BASE" "$XSD_PRIME" "$XSD_DOUBLE_PRIME" "$XSD_EMPTY" "$XSD_INVALID" "$XML_TEST" "$XML_INVALID")
for file in "${files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "\033[31m[ERREUR] Le fichier $file est introuvable. Test ignore.\033[0m"
    fi
done

# Comparaison des fichiers XSD
echo -e "\n\033[36m=======================\n[INFO] Comparaison des fichiers XSD\n=======================\033[0m"
python3 Main.py --compare "$XSD_BASE" "$XSD_PRIME" "$ADMIN_USER"
echo "-----------------------------------"
python3 Main.py --compare "$XSD_BASE" "$XSD_DOUBLE_PRIME" "$ADMIN_USER"
echo "-----------------------------------"
python3 Main.py --compare "$XSD_PRIME" "$XSD_DOUBLE_PRIME" "$ADMIN_USER"
echo "-----------------------------------"

# Validation des fichiers XML
echo -e "\n\033[33m=======================\n[INFO] Validation XML/XSD\n=======================\033[0m"
python3 Main.py --validate "$XSD_BASE" "$XML_TEST" "$ADMIN_USER"
echo "-----------------------------------"
python3 Main.py --validate "$XSD_BASE" "$XML_INVALID" "$ADMIN_USER"
echo "-----------------------------------"
python3 Main.py --validate "$XSD_PRIME" "$XML_TEST" "$ADMIN_USER"
echo "-----------------------------------"

# Tests d'erreurs
echo -e "\n\033[35m=======================\n[INFO] Gestion des erreurs\n=======================\033[0m"
python3 Main.py --compare "$XSD_BASE" "$XSD_EMPTY" "$ADMIN_USER"
echo "-----------------------------------"
python3 Main.py --validate "$XSD_INVALID" "$XML_TEST" "$ADMIN_USER"
echo "-----------------------------------"
if [ ! -f "$XSD_NOT_FOUND" ]; then
    echo -e "\033[31m[ERREUR] Le fichier $XSD_NOT_FOUND est manquant. Test ignore.\033[0m"
fi
echo "-----------------------------------"

# Simulation d'un utilisateur sans acces
echo -e "\n\033[31m=======================\n[INFO] Test d'acces refuse\n=======================\033[0m"
python3 Main.py --validate "$XSD_BASE" "$XML_TEST" "$USER_NO_ACCESS"
echo "-----------------------------------"
python3 Main.py --compare "$XSD_BASE" "$XSD_PRIME" "$USER_NO_ACCESS"
echo "-----------------------------------"

# Verification d'acces Admin
echo -e "\n\033[32m=======================\n[INFO] Verification d'acces Admin\n=======================\033[0m"
python3 Main.py --validate "$XSD_BASE" "$XML_TEST" "$ADMIN_USER"
echo "-----------------------------------"
python3 Main.py --compare "$XSD_BASE" "$XSD_PRIME" "$ADMIN_USER"
echo "-----------------------------------"

# Ajout d'un nouvel utilisateur
echo -e "\n\033[34m=======================\n[INFO] Ajout d'un nouvel utilisateur\n=======================\033[0m"

# Demander le nom du nouvel utilisateur juste avant de donner le password
read -p "Entrez le nom du nouvel utilisateur : " NEW_USER
python3 Main.py --add-user "$NEW_USER"
echo "-----------------------------------"

# Ajout d'un utilisateur existant (test alice)
echo -e "\n\033[34m=======================\n[INFO] Test d'ajout d'un utilisateur existant (Alice)\n=======================\033[0m"
python3 Main.py --add-user "$EXISTING_USER"
echo "-----------------------------------"

# Fin du test
echo -e "\n\033[32m=======================\n[INFO] Tous les tests ont ete executes !\n=======================\033[0m"
