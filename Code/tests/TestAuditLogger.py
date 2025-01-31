import unittest
from AuditLogger import AuditLogger

class TestAuditLogger(unittest.TestCase):

    def setUp(self):
        """Initialise un logger pour les tests."""
        self.logger = AuditLogger()

    def test_log_event(self):
        """Teste la méthode log_event."""
        with self.assertLogs(self.logger.logger, level='INFO') as log:
            self.logger.log_event("Test Event")
            self.assertIn("INFO:AuditLogger:Event logged: Test Event", log.output)

    def test_log_error(self):
        """Teste la méthode log_error."""
        with self.assertLogs(self.logger.logger, level='ERROR') as log:
            self.logger.log_error("Test Error")
            self.assertIn("ERROR:AuditLogger:Error logged: Test Error", log.output)

if __name__ == '__main__':
    unittest.main()
