#!/bin/bash

# Forcer l'encodage UTF-8 pour éviter les erreurs d'affichage
export LANG=C.UTF-8

# Définition des fichiers de test
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

# Définition des couleurs
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"
MAGENTA="\e[35m"
NC="\e[0m" # Reset color

# Vérification des fichiers avant exécution
echo -e "\n${CYAN}======================="
echo -e "[INFO] Verification des fichiers de test"
echo -e "=======================${NC}\n"

FILES=("$XSD_BASE" "$XSD_PRIME" "$XSD_DOUBLE_PRIME" "$XSD_EMPTY" "$XSD_INVALID" "$XML_TEST" "$XML_INVALID")

for FILE in "${FILES[@]}"; do
    if [[ ! -f "$FILE" ]]; then
        echo -e "${RED}[ERREUR] Le fichier $FILE est introuvable. Test ignore.${NC}"
    else
        echo -e "${GREEN}[OK] Fichier trouve : $FILE${NC}"
    fi
done

# Comparaison des fichiers XSD
echo -e "\n${CYAN}======================="
echo -e "[INFO] Comparaison des fichiers XSD"
echo -e "=======================${NC}\n"

python3 Main.py --compare "$XSD_BASE" "$XSD_PRIME" "$ADMIN_USER"
echo "-----------------------------------"
python3 Main.py --compare "$XSD_BASE" "$XSD_DOUBLE_PRIME" "$ADMIN_USER"
echo "-----------------------------------"
python3 Main.py --compare "$XSD_PRIME" "$XSD_DOUBLE_PRIME" "$ADMIN_USER"
echo "-----------------------------------"

# Validation des fichiers XML
echo -e "\n${YELLOW}======================="
echo -e "[INFO] Validation XML/XSD"
echo -e "=======================${NC}\n"

python3 Main.py --validate "$XSD_BASE" "$XML_TEST" "$ADMIN_USER"
echo "-----------------------------------"
python3 Main.py --validate "$XSD_BASE" "$XML_INVALID" "$ADMIN_USER"
echo "-----------------------------------"
python3 Main.py --validate "$XSD_PRIME" "$XML_TEST" "$ADMIN_USER"
echo "-----------------------------------"

# Tests d'erreurs
echo -e "\n${MAGENTA}======================="
echo -e "[INFO] Gestion des erreurs"
echo -e "=======================${NC}\n"

python3 Main.py --compare "$XSD_BASE" "$XSD_EMPTY" "$ADMIN_USER"
echo "-----------------------------------"
python3 Main.py --validate "$XSD_INVALID" "$XML_TEST" "$ADMIN_USER"
echo "-----------------------------------"

if [[ ! -f "$XSD_NOT_FOUND" ]]; then
    echo -e "${RED}[ERREUR] Le fichier $XSD_NOT_FOUND est manquant. Verifiez le chemin ou utilisez un fichier valide.${NC}"
fi
echo "-----------------------------------"

# Simulation d'un utilisateur sans accès
echo -e "\n${RED}======================="
echo -e "[INFO] Test d'acces refuse"
echo -e "=======================${NC}\n"

python3 Main.py --validate "$XSD_BASE" "$XML_TEST" "$USER_NO_ACCESS"
echo "-----------------------------------"
python3 Main.py --compare "$XSD_BASE" "$XSD_PRIME" "$USER_NO_ACCESS"
echo "-----------------------------------"

# Vérification d'accès Admin
echo -e "\n${GREEN}======================="
echo -e "[INFO] Verification d'acces Admin"
echo -e "=======================${NC}\n"

python3 Main.py --validate "$XSD_BASE" "$XML_TEST" "$ADMIN_USER"
echo "-----------------------------------"
python3 Main.py --compare "$XSD_BASE" "$XSD_PRIME" "$ADMIN_USER"
echo "-----------------------------------"

# Ajout d'un nouvel utilisateur
echo -e "\n${BLUE}======================="
echo -e "[INFO] Ajout d'un nouvel utilisateur"
echo -e "=======================${NC}\n"

read -p "Entrez le nom du nouvel utilisateur: " NEW_USER
python3 Main.py --add-user "$NEW_USER"
echo "-----------------------------------"

# Ajout d'un utilisateur existant (test alice)
echo -e "\n${BLUE}======================="
echo -e "[INFO] Test d'ajout d'un utilisateur existant (Alice)"
echo -e "=======================${NC}\n"

echo -e "${YELLOW}L'utilisateur Alice existe deja. Voulez-vous ecraser l'ancien mot de passe ? (o/n)${NC}"
read -p "Reponse: " CHOICE

if [[ "$CHOICE" == "o" ]]; then
    echo -e "${RED}[INFO] Suppression de l'utilisateur Alice...${NC}"
    python3 Main.py --remove-user "$EXISTING_USER"
    echo -e "${GREEN}✅ Utilisateur Alice supprime avec succes.${NC}"
    echo -e "${GREEN}[INFO] Creation d'un nouvel utilisateur Alice...${NC}"
    python3 Main.py --add-user "$EXISTING_USER"
else
    echo -e "${GREEN}[INFO] Operation annulee.${NC}"
fi
echo "-----------------------------------"

# Fin du test
echo -e "\n${GREEN}======================="
echo -e "[INFO] Tous les tests ont ete executes avec succes !"
echo -e "=======================${NC}"
