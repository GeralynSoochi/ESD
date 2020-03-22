-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ticket`
--
CREATE DATABASE IF NOT EXISTS `ticket` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ticket`;

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
CREATE TABLE IF NOT EXISTS `ticket` (
  `ticketid` int NOT NULL,
  `issueTitle` varchar(100) NOT NULL,
  `issueDetails` varchar(100) NOT NULL,
  `status` varchar(10) NOT NULL,
  `dateOpen` varchar(15) NOT NULL,
  `username` varchar(100) NOT NULL,
  PRIMARY KEY (`ticketid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `ticket` ADD CONSTRAINT `ticket_fk1` FOREIGN KEY (`username`) REFERENCES `account`.`account`(`username`) ON DELETE RESTRICT ON UPDATE RESTRICT;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
