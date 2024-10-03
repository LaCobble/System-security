from abc import ABC, abstractmethod

class SecurityManagerInterface(ABC):
    @abstractmethod
    def check_access(self, user: str, file: str) -> bool:
        pass

    @abstractmethod
    def validate_integrity(self, file: str, expected_hash: str) -> bool:
        pass

    @abstractmethod
    def authenticate_user(self, user: str, password: str) -> bool:
        pass
