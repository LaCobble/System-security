# Script PowerShell pour executer tous les tests automatiquement

# Definition des fichiers de test
$XSD_BASE = "Mi.xsd"
$XSD_PRIME = "Mi_prime.xsd"
$XSD_DOUBLE_PRIME = "Mi_double_prime.xsd"
$XSD_EMPTY = "empty.xsd"
$XSD_INVALID = "invalid.xsd"
$XML_TEST = "test.xml"
$XML_INVALID = "invalid.xml"
$XSD_NOT_FOUND = "not_found.xsd"
$USER_NO_ACCESS = "user1"
$ADMIN_USER = "admin"
$EXISTING_USER = "alice"

# Verification de l'existence des fichiers avant execution
$files = @($XSD_BASE, $XSD_PRIME, $XSD_DOUBLE_PRIME, $XSD_EMPTY, $XSD_INVALID, $XML_TEST, $XML_INVALID)
foreach ($file in $files) {
    if (!(Test-Path $file)) {
        Write-Host "[ERREUR] Le fichier $file est introuvable. Test ignore." -ForegroundColor Red
    }
}

# Comparaison des fichiers XSD
Write-Host "`n=======================" -ForegroundColor Cyan
Write-Host "[INFO] Comparaison des fichiers XSD" -ForegroundColor Cyan
Write-Host "=======================`n" -ForegroundColor Cyan
python Main.py --compare $XSD_BASE $XSD_PRIME $ADMIN_USER
Write-Host "-----------------------------------"
python Main.py --compare $XSD_BASE $XSD_DOUBLE_PRIME $ADMIN_USER
Write-Host "-----------------------------------"
python Main.py --compare $XSD_PRIME $XSD_DOUBLE_PRIME $ADMIN_USER
Write-Host "-----------------------------------"

# Validation des fichiers XML
Write-Host "`n=======================" -ForegroundColor Yellow
Write-Host "[INFO] Validation XML/XSD" -ForegroundColor Yellow
Write-Host "=======================`n" -ForegroundColor Yellow
python Main.py --validate $XSD_BASE $XML_TEST $ADMIN_USER
Write-Host "-----------------------------------"
python Main.py --validate $XSD_BASE $XML_INVALID $ADMIN_USER
Write-Host "-----------------------------------"
python Main.py --validate $XSD_PRIME $XML_TEST $ADMIN_USER
Write-Host "-----------------------------------"

# Tests d'erreurs
Write-Host "`n=======================" -ForegroundColor Magenta
Write-Host "[INFO] Gestion des erreurs" -ForegroundColor Magenta
Write-Host "=======================`n" -ForegroundColor Magenta
python Main.py --compare $XSD_BASE $XSD_EMPTY $ADMIN_USER
Write-Host "-----------------------------------"
python Main.py --validate $XSD_INVALID $XML_TEST $ADMIN_USER
Write-Host "-----------------------------------"
if (!(Test-Path $XSD_NOT_FOUND)) {
    Write-Host "[ERREUR] Le fichier $XSD_NOT_FOUND est manquant. Test ignore." -ForegroundColor Red
}
Write-Host "-----------------------------------"

# Simulation d'un utilisateur sans acces
Write-Host "`n=======================" -ForegroundColor Red
Write-Host "[INFO] Test d'acces refuse" -ForegroundColor Red
Write-Host "=======================`n" -ForegroundColor Red
python Main.py --validate $XSD_BASE $XML_TEST $USER_NO_ACCESS
Write-Host "-----------------------------------"
python Main.py --compare $XSD_BASE $XSD_PRIME $USER_NO_ACCESS
Write-Host "-----------------------------------"

# Verification d'acces Admin
Write-Host "`n=======================" -ForegroundColor Green
Write-Host "[INFO] Verification d'acces Admin" -ForegroundColor Green
Write-Host "=======================`n" -ForegroundColor Green
python Main.py --validate $XSD_BASE $XML_TEST $ADMIN_USER
Write-Host "-----------------------------------"
python Main.py --compare $XSD_BASE $XSD_PRIME $ADMIN_USER
Write-Host "-----------------------------------"

# Ajout d'un nouvel utilisateur
Write-Host "`n=======================" -ForegroundColor Blue
Write-Host "[INFO] Ajout d'un nouvel utilisateur" -ForegroundColor Blue
Write-Host "=======================`n" -ForegroundColor Blue

# Demander le nom du nouvel utilisateur juste avant de donner le password
$NEW_USER = Read-Host "Entrez le nom du nouvel utilisateur"
python Main.py --add-user $NEW_USER
Write-Host "-----------------------------------"

# Ajout d'un utilisateur existant (test alice)
Write-Host "`n=======================" -ForegroundColor Blue
Write-Host "[INFO] Test d'ajout d'un utilisateur existant (Alice)" -ForegroundColor Blue
Write-Host "=======================`n" -ForegroundColor Blue
python Main.py --add-user $EXISTING_USER
Write-Host "-----------------------------------"

# Fin du test
Write-Host "`n=======================" -ForegroundColor Green
Write-Host "[INFO] Tous les tests ont ete executes !" -ForegroundColor Green
Write-Host "=======================`n" -ForegroundColor Green
