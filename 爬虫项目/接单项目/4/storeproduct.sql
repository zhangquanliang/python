/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 5.7.22-log : Database - aliexpress
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`aliexpress` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `aliexpress`;

/*Table structure for table `storeproduct` */

DROP TABLE IF EXISTS `storeproduct`;

CREATE TABLE `storeproduct` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shopId` text,
  `storelink` text,
  `productName` text,
  `productLink` text,
  `productrank` text,
  `productPrice` text,
  `productDiscount` text,
  `productPriceOld` text,
  `orders` text,
  `category_title` text,
  `productPriceUnit` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1009871 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
