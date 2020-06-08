import complaint_handler
from tests.integration.mock_db import MockDB


class TestComplaintHandler(MockDB):

    def test_report_no_signal(self):
        with self.mock_db_config:
            self.assertTrue(complaint_handler.report_no_signal(1, "Colombo"))
            
    def test_report_low_signal(self):
        with self.mock_db_config:
            self.assertTrue(complaint_handler.report_low_signal(1, "Colombo"))