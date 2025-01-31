# 📌 Test Scenarios for XML/XSD Comparison & Validation

## **1️⃣ Comparaison des fichiers XSD**  

| **Test** | **Commande** | **Résultat attendu** |
|----------|------------|----------------------|
| ✅ **Comparer `Mi.xsd` et `Mi_prime.xsd`** | `python Main.py --compare Mi.xsd Mi_prime.xsd admin` | Différences affichées (ajouts) |
| ✅ **Comparer `Mi.xsd` et `Mi_double_prime.xsd`** | `python Main.py --compare Mi.xsd Mi_double_prime.xsd admin` | Différences affichées (modifications, suppressions) |
| ✅ **Comparer `Mi_prime.xsd` et `Mi_double_prime.xsd`** | `python Main.py --compare Mi_prime.xsd Mi_double_prime.xsd admin` | Différences affichées |

---

## **2️⃣ Validation d'un XML contre un XSD**  

| **Test** | **Commande** | **Résultat attendu** |
|----------|------------|----------------------|
| ✅ **Valider un XML conforme (`test.xml`) avec `Mi.xsd`** | `python Main.py --validate Mi.xsd test.xml admin` | "✅ Validation réussie" |
| ❌ **Tester un XML invalide (`invalid.xml`) avec `Mi.xsd`** | `python Main.py --validate Mi.xsd invalid.xml admin` | "❌ Échec de validation" |
| ❌ **Tester un XML avec `Mi_prime.xsd` (vérifier les ajouts)** | `python Main.py --validate Mi_prime.xsd test.xml admin` | "❌ Échec si `test.xml` ne contient pas les ajouts" |

---

## **3️⃣ Gestion des erreurs et fichiers problématiques**  

| **Test** | **Commande** | **Résultat attendu** |
|----------|------------|----------------------|
| ❌ **Comparer un XSD vide (`empty.xsd`)** | `python Main.py --compare Mi.xsd empty.xsd admin` | "❌ Erreur : fichier XSD vide" |
| ❌ **Valider avec un fichier XSD invalide (`invalid.xsd`)** | `python Main.py --validate invalid.xsd test.xml admin` | "❌ Erreur de parsing XSD" |
| ❌ **Valider un XML avec un XSD manquant (`not_found.xsd`)** | `python Main.py --validate not_found.xsd test.xml admin` | "❌ Fichier introuvable" |

---

## **4️⃣ Test d'accès refusé pour un utilisateur non autorisé**  

| **Test** | **Commande** | **Résultat attendu** |
|----------|------------|----------------------|
| ❌ **Un utilisateur sans droits essaie de valider un XML** | `python Main.py --validate Mi.xsd test.xml user1` | "❌ Accès refusé" |
| ❌ **Un utilisateur sans droits essaie de comparer des XSD** | `python Main.py --compare Mi.xsd Mi_prime.xsd user1` | "❌ Accès refusé" |

---

## **5️⃣ Vérification d'accès Admin**  

| **Test** | **Commande** | **Résultat attendu** |
|----------|------------|----------------------|
| ✅ **Admin valide un XML** | `python Main.py --validate Mi.xsd test.xml admin` | "✅ Validation réussie" |
| ✅ **Admin compare deux XSD** | `python Main.py --compare Mi.xsd Mi_prime.xsd admin` | Différences affichées |

---

## **6️⃣ Ajout d'un nouvel utilisateur**  

| **Test** | **Commande** | **Résultat attendu** |
|----------|------------|----------------------|
| ✅ **Ajouter un utilisateur (`new_user`)** | `python Main.py --add-user new_user` | "✅ Utilisateur ajouté avec succès" |

---

## **📌 Exécution des tests : Exemples de commandes**  

### 🔹 Comparaison de fichiers XSD  
```powershell
python Main.py --compare Mi.xsd Mi_prime.xsd admin
