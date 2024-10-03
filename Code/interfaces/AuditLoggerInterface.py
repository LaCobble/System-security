from abc import ABC, abstractmethod

class AuditLoggerInterface(ABC):
    @abstractmethod
    def log_event(self, event: str) -> None:
        """Journalise un événement."""
        pass

    @abstractmethod
    def log_error(self, error: str) -> None:
        """Journalise une erreur ou un problème."""
        pass