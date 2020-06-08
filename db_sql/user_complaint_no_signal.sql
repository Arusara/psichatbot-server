-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 03, 2020 at 06:20 AM
-- Server version: 8.0.13-4
-- PHP Version: 7.2.24-0ubuntu0.18.04.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `IlYy99NiBs`
--

-- --------------------------------------------------------

--
-- Table structure for table `user_complaint_no_signal`
--

CREATE TABLE `user_complaint_no_signal` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `location` text COLLATE utf8_unicode_ci NOT NULL,
  `report` text COLLATE utf8_unicode_ci NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `user_complaint_no_signal`
--

INSERT INTO `user_complaint_no_signal` (`id`, `user_id`, `location`, `report`, `date`) VALUES
(1, 2, 'Colombo', 'User has reported loss of signal. \nUser ID: 2\nLocation: Colombo', '2020-05-19 14:47:50'),
(2, 2, 'Colombo', 'User has reported loss of signal. \nUser ID: 2\nLocation: Colombo', '2020-05-23 14:48:24');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user_complaint_no_signal`
--
ALTER TABLE `user_complaint_no_signal`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user_complaint_no_signal`
--
ALTER TABLE `user_complaint_no_signal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
