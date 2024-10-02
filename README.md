# Projet de Détection d'Incohérences entre Fichiers XSD et XML

## Introduction

Ce projet a pour but de détecter des incohérences entre deux itérations d'un fichier XSD (XML Schema Definition) et les fichiers XML qui s'y rapportent. En validant et en comparant les schémas et les documents XML, ce projet garantit l'intégrité des données et la conformité des fichiers XML aux spécifications définies.

## Objectifs

- Développer une application capable de charger des fichiers XSD et XML.
- Valider les fichiers XML par rapport aux définitions spécifiées dans les fichiers XSD.
- Identifier et signaler les incohérences détectées entre les différentes versions de fichiers XSD et XML.
- Fournir une interface utilisateur simple pour faciliter l'interaction avec l'application.

## Fonctionnalités

- Chargement des fichiers XSD et XML à partir du système de fichiers.
- Validation des documents XML pour vérifier leur conformité avec le schéma XSD.
- Comparaison des fichiers XSD pour détecter les modifications entre différentes versions.
- Rapport détaillé sur les incohérences trouvées, y compris la description, l'élément ou l'attribut concerné, et le niveau de gravité.