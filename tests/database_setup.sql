# Creating tables
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `email` text COLLATE utf8_unicode_ci NOT NULL,
  `first_name` text COLLATE utf8_unicode_ci NOT NULL,
  `last_name` text COLLATE utf8_unicode_ci NOT NULL,
  `password_salt` text COLLATE utf8_unicode_ci NOT NULL,
  `password_hash` text COLLATE utf8_unicode_ci NOT NULL,
  `created` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

CREATE TABLE `data_packages` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `name` text COLLATE utf8_unicode_ci NOT NULL,
  `data` float NOT NULL,
  `valid_period` float NOT NULL,
  `price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

ALTER TABLE `data_packages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

CREATE TABLE `voice_packages` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `name` text COLLATE utf8_unicode_ci NOT NULL,
  `minutes` float NOT NULL,
  `valid_period` int(11) NOT NULL,
  `price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

ALTER TABLE `voice_packages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

CREATE TABLE `user_data_package` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `package_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL UNIQUE ,
  `package_name` text COLLATE utf8_unicode_ci NOT NULL,
  `data_used` float NOT NULL DEFAULT '0',
  `activated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `user_voice_package` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `package_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL UNIQUE ,
  `package_name` text COLLATE utf8_unicode_ci NOT NULL,
  `minutes_used` int(11) NOT NULL DEFAULT '0',
  `activated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `user_complaint_low_signal` (
  `id` int(11) NOT NULL PRIMARY KEY,
  `user_id` int(11) NOT NULL,
  `location` text COLLATE utf8_unicode_ci NOT NULL,
  `report` text COLLATE utf8_unicode_ci NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `user_complaint_no_signal` (
  `id` int(11) NOT NULL PRIMARY KEY,
  `user_id` int(11) NOT NULL,
  `location` text COLLATE utf8_unicode_ci NOT NULL,
  `report` text COLLATE utf8_unicode_ci NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `telecom_chatbot_messages` (
  `id` varchar(30) COLLATE utf8_unicode_ci NOT NULL PRIMARY KEY ,
  `user_id` int(11) NOT NULL,
  `message` text COLLATE utf8_unicode_ci NOT NULL,
  `isBot` tinyint(1) NOT NULL,
  `date_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `test_table` (
  `id` varchar(30) COLLATE utf8_unicode_ci NOT NULL PRIMARY KEY ,
  `text` text NOT NULL,
  `int` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


# Inserting values
INSERT INTO `users` (`user_id`, `email`, `first_name`, `last_name`, `password_salt`, `password_hash`, `created`) VALUES
(1, 'test@gmail.com', 'Test', 'User 1', '75b6e8243d6774daaea278f67fc2e9b7', 'e107271df14eeda28efe529996408353dbf381962a7405feda7424b185dc5102', '2020-05-11 11:50:15'),
(2, 'minullamahewage@gmail.com', 'Minul', 'Lamahewage', 'e73f301fd27168a9d5d3bdad489d6fbc', '333ad56eacf67af4b3eae42c47ad00dd54b905be2f554e646bc8679b52563155', '2020-05-15 07:50:30');

INSERT INTO `data_packages` (`id`, `name`, `data`, `valid_period`, `price`) VALUES
(1, 'D29', 200, 2, 29),
(2, 'D49', 400, 7, 49),
(3, 'D99', 1000, 21, 99),
(4, 'D199', 2000, 30, 199),
(5, 'D349', 4000, 30, 349),
(6, 'D499', 6000, 30, 499),
(7, 'D649', 8500, 30, 649);

INSERT INTO `voice_packages` (`id`, `name`, `minutes`, `valid_period`, `price`) VALUES
(1, 'V20', 30, 7, 20),
(2, 'V60', 100, 7, 60),
(3, 'V100', 200, 14, 100),
(4, 'V200', 400, 30, 200);

INSERT INTO `telecom_chatbot_messages` (`id`, `user_id`, `message`, `isBot`, `date_time`) VALUES
('2020-05-23T09:46:14.681Z', 2, 'Hi', 0, '2020-05-23 15:16:15'),
('2020-05-23T09:46:15.472007', 2, 'Hi there, how can I help you?\n\nHere are some of the things I can do.\n1. Activate, Change or Deactivate data or voice packages\n   Eg: I want to activate <package name> data package. I want to change my voice package. I want to deactivate my data package.\n\n2. Complain about the loss of signal or low signal\n   Eg: There is no signal. I am not getting any signal. Internet is slow. The signal is weak\n\n3. View usage data\n   Eg: View data usage. How many minutes do I have left? Show me my voice package usage\n\n4. View package information\n   Eg: Show me the details of data packages. Show me the details of <package name> package. Show me the details of packages\n', 1, '2020-05-23 15:16:15'),
('2020-05-23T09:46:46.591Z', 2, 'Hi', 0, '2020-05-23 15:16:47'),
('2020-05-23T09:46:47.234294', 2, 'Hi there, how can I help you?\n\nHere are some of the things I can do.\n1. Activate, Change or Deactivate data or voice packages\n   Eg: I want to activate <package name> data package. I want to change my voice package. I want to deactivate my data package.\n\n2. Complain about the loss of signal or low signal\n   Eg: There is no signal. I am not getting any signal. Internet is slow. The signal is weak\n\n3. View usage data\n   Eg: View data usage. How many minutes do I have left? Show me my voice package usage\n\n4. View package information\n   Eg: Show me the details of data packages. Show me the details of <package name> package. Show me the details of packages\n', 1, '2020-05-23 15:16:47'),
('2020-05-23T10:27:16.781Z', 2, 'Hi', 0, '2020-05-23 15:57:17');

INSERT INTO `user_data_package` (`package_id`, `user_id`, `package_name`, `data_used`, `activated_date`) VALUES
(1, 3, 1, 'D99', 0),
(2, 6, 2, 'D499', 0);

INSERT INTO `user_voice_package` (`package_id`, `user_id`, `package_name`, `minutes_used`, `activated_date`) VALUES
(1, 3, 1, 'V100', 0),
(2, 4, 2, 'V200', 0);







