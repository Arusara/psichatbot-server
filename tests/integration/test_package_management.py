import package_management
from tests.integration.mock_db import MockDB


class TestPackageManagement(MockDB):
    def test_activate_data_package(self):
        with self.mock_db_config:
            self.assertEqual(package_management.activate_data_package("D99", 3),
                             "D99 package has been successfully activated. You now have 1000.0MB remaining")
            self.assertEqual(package_management.activate_data_package("D99", 1),
                             "You have already activated a data package. Please opt to change your package instead.")

    def test_change_data_package(self):
        with self.mock_db_config:
            self.assertEqual(package_management.change_data_package("D99", 1),
                             "Your data package has been successfully changed to D99. You now have 1000.0MB remaining.")
            self.assertEqual(package_management.change_data_package("D49", 4),
                             "You have no currently activated data package."
                             " Please opt to activate a new package instead.""")

    def test_deactivate_data_package(self):
        with self.mock_db_config:
            self.assertEqual(package_management.deactivate_data_package(2),
                             "Your data package has been successfully deactivated.")
            self.assertEqual(package_management.deactivate_data_package(4),
                             "You have no currently activated data packages.")

    def test_activate_voice_package(self):
        with self.mock_db_config:
            self.assertEqual(package_management.activate_voice_package("V100", 3),
                             "V100 package has been successfully activated. You now have 200.0 minutes remaining.")
            self.assertEqual(package_management.activate_voice_package("V100", 1),
                             "You have already activated a voice package. Please opt to change your package instead.")

    def test_change_voice_package(self):
        with self.mock_db_config:
            self.assertEqual(package_management.change_voice_package("V20", 1),
                             "Your voice package has been successfully changed to V20."
                             " You now have 30.0 minutes remaining.")
            self.assertEqual(package_management.change_voice_package("V20", 4),
                             "You have no currently activated voice package."
                             " Please opt to activate a new package instead.")

    def test_deactivate_voice_package(self):
        with self.mock_db_config:
            self.assertEqual(package_management.deactivate_voice_package(2),
                             "Your voice package has been successfully deactivated.")
            self.assertEqual(package_management.deactivate_voice_package(4),
                             "You have no currently activated voice packages.")

    def test_check_data_package_name(self):
        with self.mock_db_config:
            self.assertTrue(package_management.check_data_package_name("D199"))
            self.assertFalse(package_management.check_data_package_name("D300"))
            self.assertFalse(package_management.check_data_package_name(""))

    def test_get_data_packages(self):
        with self.mock_db_config:
            self.assertDictEqual(package_management.get_data_packages()[0],
                                 {
                                     'id': 1,
                                     'name': 'D29',
                                     'data': 200.0,
                                     'valid_period': 2.0,
                                     'price': 29.0
                                 })

    def test_get_data_package(self):
        with self.mock_db_config:
            self.assertDictEqual(package_management.get_data_package("D29"),
                                 {
                                     'id': 1,
                                     'name': 'D29',
                                     'data': 200.0,
                                     'valid_period': 2.0,
                                     'price': 29.0
                                 })

    def test_check_data_package_already_activated(self):
        with self.mock_db_config:
            self.assertTrue(package_management.check_data_package_already_activated(1))
            self.assertFalse(package_management.check_data_package_already_activated(4))

    def test_check_voice_package_name(self):
        with self.mock_db_config:
            self.assertTrue(package_management.check_voice_package_name("V100"))
            self.assertFalse(package_management.check_voice_package_name("V500"))
            self.assertFalse(package_management.check_voice_package_name(""))

    def test_get_voice_packages(self):
        with self.mock_db_config:
            self.assertDictEqual(package_management.get_voice_packages()[0],
                                 {
                                     'id': 1,
                                     'name': 'V20',
                                     'minutes': 30.0,
                                     'valid_period': 7,
                                     'price': 20.0
                                 })

    def test_get_voice_package(self):
        with self.mock_db_config:
            self.assertDictEqual(package_management.get_voice_package("V20"),
                                 {
                                     'id': 1,
                                     'name': 'V20',
                                     'minutes': 30.0,
                                     'valid_period': 7,
                                     'price': 20.0
                                 })

    def test_check_voice_package_already_activated(self):
        with self.mock_db_config:
            self.assertTrue(package_management.check_voice_package_already_activated(1))
            self.assertFalse(package_management.check_voice_package_already_activated(4))

    def test_get_data_usage_data(self):
        with self.mock_db_config:
            self.assertEqual(package_management.get_data_usage_data(1),
                             "Active data package: D99\n"
                             "Remaining data: 1000.0MB\n"
                             "Remaining days: 20 days 23 hours 60 minutes")

    def test_get_voice_usage_data(self):
        with self.mock_db_config:
            self.assertEqual(package_management.get_voice_usage_data(1),
                             "Active voice package: V20\n"
                             "Remaining talk time: 30 minutes\n"
                             "Remaining days: 6 days 23 hours 60 minutes"
                             )
