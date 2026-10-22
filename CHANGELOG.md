# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `requirements.txt` (`bcrypt`), portfolio README in English, MIT license, contribution guide, code of conduct and security policy.
- Continuous integration (byte-compilation, unit tests, secret scan) and a release workflow.

### Changed

- The sample `Code/passwords.json` now holds a placeholder hash instead of a real one.

### Removed

- Compiled `__pycache__` files that had been committed by mistake.

## [1.0.0] - 2024-10-03

First tagged version: the project as submitted.

### Added

- Metamodel and detailed UML class diagram (StarUML sources, images and written descriptions).
- Python prototype: XML and XSD documents, elements, attributes, inconsistencies, security manager (bcrypt authentication, access control, SHA-256 integrity) and audit logger, each behind an abstract interface.
- Unit tests for every class.

[Unreleased]: https://github.com/LaCobble/System-security/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/LaCobble/System-security/releases/tag/v1.0.0
