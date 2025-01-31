import logging
from interfaces.AuditLoggerInterface import AuditLoggerInterface

class AuditLogger(AuditLoggerInterface):
    """Implémentation d'un logger pour enregistrer des événements et des erreurs."""
    def __init__(self):
        """Initialise le logger."""
        self.logger = logging.getLogger("AuditLogger")
        logging.basicConfig(level=logging.DEBUG)

    def log_event(self, event: str) -> None:
        """Logique pour enregistrer un événement."""
        self.logger.info(f"Event logged: {event}")

    def log_error(self, error: str) -> None:
        """Logique pour enregistrer une erreur."""
        self.logger.error(f"Error logged: {error}")
