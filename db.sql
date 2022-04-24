/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 5.6.17 : Database - orvba1
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`orvba1` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `orvba1`;

/*Table structure for table `account_info` */

DROP TABLE IF EXISTS `account_info`;

CREATE TABLE `account_info` (
  `account_id` int(11) NOT NULL AUTO_INCREMENT,
  `account_no` int(11) DEFAULT NULL,
  `account_holder_name` varchar(30) DEFAULT NULL,
  `IFSC code` int(11) DEFAULT NULL,
  `validity` date DEFAULT NULL,
  `account_holder_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `account_info` */

insert  into `account_info`(`account_id`,`account_no`,`account_holder_name`,`IFSC code`,`validity`,`account_holder_id`) values 
(2,123123,'workshop',123321,'2023-09-09',3);

/*Table structure for table `alert` */

DROP TABLE IF EXISTS `alert`;

CREATE TABLE `alert` (
  `alert_id` int(11) NOT NULL AUTO_INCREMENT,
  `alert_info` varchar(40) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`alert_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `alert` */

/*Table structure for table `chat` */

DROP TABLE IF EXISTS `chat`;

CREATE TABLE `chat` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `fid` int(11) DEFAULT NULL,
  `toid` int(11) DEFAULT NULL,
  `msg` varchar(500) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

/*Data for the table `chat` */

insert  into `chat`(`cid`,`fid`,`toid`,`msg`,`date`,`type`) values 
(1,8,5,'hai','2021-05-05','service_center'),
(2,8,5,'hlo','2021-05-05','service_center'),
(3,8,5,'fkgkg','2021-05-05','service_center'),
(4,8,5,'hi','2021-05-05','service_center'),
(5,8,5,'fjkh','2021-05-05','service_center'),
(6,8,5,'hh','2021-05-05','service_center'),
(7,8,5,'hlo','2021-05-05','service_center'),
(8,8,5,'hlo','2021-05-05','service_center'),
(9,8,5,'how r u','2021-05-05','service_center'),
(10,8,3,'hlo','2021-05-05','service_center'),
(11,10,3,'hii','2021-05-11','service_center'),
(12,2,5,'hii','2021-05-11','workshop'),
(13,2,3,'hi','2021-05-11','service_center'),
(14,2,5,'hi','2021-05-11','service_center'),
(15,3,10,'hii','2021-05-11','workshop'),
(16,10,3,'hey','2021-05-14','workshop'),
(17,3,0,'how r u','2021-05-14','workshop'),
(18,3,10,'how r u','2021-05-14','workshop'),
(19,10,3,'hii','2021-05-14','workshop'),
(20,10,4,'hello','2021-05-14','service_center'),
(21,10,5,'hii','2021-05-14','service_center'),
(22,4,10,'hii','2021-05-14','service_center'),
(23,10,5,'hii','2021-05-14','service_center'),
(24,10,5,'gg','2021-05-14','service_center'),
(25,4,10,'how r u','2021-05-14','service_center'),
(26,5,10,'how r u','2021-05-14','service_center');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` varchar(60) DEFAULT NULL,
  `complaint_info` varchar(50) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `w_sc_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `reply` varchar(40) DEFAULT NULL,
  `reply_date` date DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`complaint_id`,`subject`,`complaint_info`,`customer_id`,`w_sc_id`,`date`,`reply`,`reply_date`) values 
(1,'workshop','not good service',2,3,'2021-03-21','dfsgz','2021-05-11'),
(2,'service_center','bad service',2,4,'2021-03-21','fghxdfh','2021-05-11'),
(3,'service_center','bad',8,0,'2021-05-05','pending','0000-00-00'),
(4,'service_center','bad',8,0,'2021-05-05','pending','0000-00-00'),
(5,'service_center','jjzjznz',2,5,'2021-05-05','hjhj','0000-00-00'),
(6,'workshop','wat',8,3,'2021-05-05','pending','0000-00-00'),
(7,'workshop','skzkz',8,3,'2021-05-05','pending','0000-00-00'),
(8,'service_center','bad',8,5,'2021-05-05','pending','0000-00-00'),
(9,'workshop','damaged',10,3,'2021-05-11','asdasd','2021-05-11');

/*Table structure for table `crane` */

DROP TABLE IF EXISTS `crane`;

CREATE TABLE `crane` (
  `crane_id` int(11) NOT NULL AUTO_INCREMENT,
  `workshop_id` int(11) DEFAULT NULL,
  `owner_name` varchar(40) DEFAULT NULL,
  `crane_details` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`crane_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `crane` */

insert  into `crane`(`crane_id`,`workshop_id`,`owner_name`,`crane_details`) values 
(1,3,'Anusree','50ton');

/*Table structure for table `customer` */

DROP TABLE IF EXISTS `customer`;

CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(50) DEFAULT NULL,
  `photo` varchar(50) DEFAULT NULL,
  `contact_no` bigint(20) DEFAULT NULL,
  `email_id` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `customer` */

insert  into `customer`(`customer_id`,`customer_name`,`photo`,`contact_no`,`email_id`) values 
(2,'c',NULL,986543212,'efd'),
(8,'ss','/static/210505-152124.jpg',9632580744,'sou@gmail.com'),
(10,'sudhi','/static/210511-202649.jpg',9852147582,'d@gmail.com'),
(11,'a','/static/210514-121846.jpg',9632587412,'f@gmail.com');

/*Table structure for table `employee` */

DROP TABLE IF EXISTS `employee`;

CREATE TABLE `employee` (
  `employee__id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_no` int(11) DEFAULT NULL,
  `employee_name` varchar(40) DEFAULT NULL,
  `designation` varchar(40) DEFAULT NULL,
  `contact_no` bigint(20) DEFAULT NULL,
  `photo` varchar(40) DEFAULT NULL,
  `email_id` varchar(40) DEFAULT NULL,
  `service_center_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`employee__id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `employee` */

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `feedback_info` varchar(50) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `w_s_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `subject` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`feedback_id`,`feedback_info`,`customer_id`,`w_s_id`,`date`,`subject`) values 
(1,'good',2,3,'0000-00-00','workshop'),
(2,'bhxhf',8,4,'2021-05-05','service_center'),
(3,'nzjs',8,5,'2021-05-05','service_center'),
(4,'znzkk',8,5,'2021-05-05','service_center'),
(5,'bb mckv',8,5,'2021-05-05','service_center'),
(6,'very bad',8,3,'2021-05-05','service_center'),
(7,'great',10,3,'2021-05-11','service_center');

/*Table structure for table `location` */

DROP TABLE IF EXISTS `location`;

CREATE TABLE `location` (
  `location_id` int(11) NOT NULL AUTO_INCREMENT,
  `longitude` float DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `location` */

insert  into `location`(`location_id`,`longitude`,`latitude`,`place`,`id`) values 
(1,75.2712,12.4295,'Kallar',5),
(2,6767,767,NULL,3),
(3,75.2712,12.4295,'Kallar',3),
(4,0,0,'',8),
(5,0,0,'',2),
(6,75.4958,11.7802,'Thalassery',10),
(7,11.7785,75.4962,'Thalassery',11);

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`user_name`,`password`,`type`) values 
(1,'admin','admin','admin'),
(2,'c','c','customer'),
(3,'w','w','workshop'),
(4,'s','s','service_center'),
(5,'sc','sc','service_center'),
(6,'SDVSDV','ZZZ','workshop'),
(7,'aaa','a','pending'),
(8,'aaaa','aa','customer'),
(9,'aaa@gmail.com','as','pending'),
(10,'sudhi','123213','customer'),
(11,'g','g','customer');

/*Table structure for table `mechanic_info` */

DROP TABLE IF EXISTS `mechanic_info`;

CREATE TABLE `mechanic_info` (
  `mechanic_id` int(11) NOT NULL AUTO_INCREMENT,
  `mechanic_name` varchar(40) DEFAULT NULL,
  `workshop_id` int(11) NOT NULL,
  `place` varchar(40) DEFAULT NULL,
  `post` varchar(40) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `district` varchar(30) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `contact_no` bigint(20) DEFAULT NULL,
  `email_id` varchar(30) DEFAULT NULL,
  `specification` varchar(30) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`mechanic_id`,`workshop_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `mechanic_info` */

insert  into `mechanic_info`(`mechanic_id`,`mechanic_name`,`workshop_id`,`place`,`post`,`pin`,`district`,`state`,`contact_no`,`email_id`,`specification`,`type`) values 
(1,'rfsrdf',3,'sgsrg','srgdrg',671234,'rdrg','Meghalaya',9876543222,'abc@gmail.com','Puncher','Four Wheeler');

/*Table structure for table `offer_info` */

DROP TABLE IF EXISTS `offer_info`;

CREATE TABLE `offer_info` (
  `offer_id` int(11) NOT NULL AUTO_INCREMENT,
  `offer_info` varchar(40) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `service_center_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`offer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `offer_info` */

insert  into `offer_info`(`offer_id`,`offer_info`,`date`,`service_center_id`) values 
(6,'wq','2021-04-23',4),
(8,'30%','2021-05-06',4);

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `id` int(11) DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `p_status` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `payment` */

insert  into `payment`(`pid`,`id`,`amount`,`p_status`,`date`) values 
(1,8,1000,'paid','2021-05-06'),
(2,19,0,'pending','2021-05-06'),
(3,20,0,'pending','2021-05-11'),
(4,1,0,'pending','2021-05-16');

/*Table structure for table `rating` */

DROP TABLE IF EXISTS `rating`;

CREATE TABLE `rating` (
  `rating_id` int(11) NOT NULL AUTO_INCREMENT,
  `rating_details` int(11) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `w_s_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `subject` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`rating_id`)
) ENGINE=InnoDB AUTO_INCREMENT=349 DEFAULT CHARSET=latin1;

/*Data for the table `rating` */

insert  into `rating`(`rating_id`,`rating_details`,`customer_id`,`w_s_id`,`date`,`subject`) values 
(344,1,2,3,'0000-00-00','workshop'),
(345,2,8,3,'2021-05-05','workshop'),
(346,2,8,4,'2021-05-05','service_center'),
(347,3,10,3,'2021-05-11','workshop'),
(348,3,2,5,'2021-05-11','service_center');

/*Table structure for table `sc_request` */

DROP TABLE IF EXISTS `sc_request`;

CREATE TABLE `sc_request` (
  `request_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) DEFAULT NULL,
  `service_fun_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `sc_request` */

insert  into `sc_request`(`request_id`,`customer_id`,`service_fun_id`,`date`,`status`) values 
(1,10,2,'2012-04-03','approved'),
(2,8,2,'2021-05-05','pending');

/*Table structure for table `service_center_info` */

DROP TABLE IF EXISTS `service_center_info`;

CREATE TABLE `service_center_info` (
  `service_center_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_center_name` varchar(40) DEFAULT NULL,
  `place` varchar(40) DEFAULT NULL,
  `post` varchar(40) DEFAULT NULL,
  `pincode` int(11) DEFAULT NULL,
  `district` varchar(40) DEFAULT NULL,
  `state` varchar(40) DEFAULT NULL,
  `contact_no` bigint(20) DEFAULT NULL,
  `email_id` varchar(40) DEFAULT NULL,
  `license_no` varchar(40) DEFAULT NULL,
  UNIQUE KEY `service_center_id` (`service_center_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `service_center_info` */

insert  into `service_center_info`(`service_center_id`,`service_center_name`,`place`,`post`,`pincode`,`district`,`state`,`contact_no`,`email_id`,`license_no`) values 
(4,'sA','kannur','kannur',679675,'kannur','Andhra Pradesh',9865432145,'raw@gmail.com','764333'),
(5,'sc','kannur','kannur',679675,'kannur','Andhra Pradesh',9865432145,'raw@gmail.com','764333');

/*Table structure for table `service_function` */

DROP TABLE IF EXISTS `service_function`;

CREATE TABLE `service_function` (
  `service_fun_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_center_id` int(11) DEFAULT NULL,
  `service` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`service_fun_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `service_function` */

insert  into `service_function`(`service_fun_id`,`service_center_id`,`service`) values 
(2,4,'dsegdrgedr'),
(3,4,'asdd');

/*Table structure for table `spare_info` */

DROP TABLE IF EXISTS `spare_info`;

CREATE TABLE `spare_info` (
  `spare_id` int(11) NOT NULL AUTO_INCREMENT,
  `spare_parts` varchar(40) DEFAULT NULL,
  `workshop_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`spare_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `spare_info` */

insert  into `spare_info`(`spare_id`,`spare_parts`,`workshop_id`) values 
(2,'50ton',3);

/*Table structure for table `worker` */

DROP TABLE IF EXISTS `worker`;

CREATE TABLE `worker` (
  `worker_id` int(11) NOT NULL AUTO_INCREMENT,
  `worker_name` varchar(40) DEFAULT NULL,
  `department` varchar(40) DEFAULT NULL,
  `email_id` varchar(40) DEFAULT NULL,
  `contact_no` bigint(20) DEFAULT NULL,
  `photo` varchar(40) DEFAULT NULL,
  `service_center_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`worker_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `worker` */

insert  into `worker`(`worker_id`,`worker_name`,`department`,`email_id`,`contact_no`,`photo`,`service_center_id`) values 
(2,'anu','puncher','anu@gmail.com',9087654320,'/static/images/210506-194709.jpg',4);

/*Table structure for table `workshop` */

DROP TABLE IF EXISTS `workshop`;

CREATE TABLE `workshop` (
  `workshop_id` int(11) NOT NULL AUTO_INCREMENT,
  `workshop_name` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `district` varchar(30) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `contact_no` bigint(20) DEFAULT NULL,
  `email_id` varchar(50) DEFAULT NULL,
  `license_no` int(11) DEFAULT NULL,
  PRIMARY KEY (`workshop_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `workshop` */

insert  into `workshop`(`workshop_id`,`workshop_name`,`place`,`post`,`pin`,`district`,`state`,`contact_no`,`email_id`,`license_no`) values 
(3,'kalpana','sdgs','sdg',4332,'gfds','sdg',22423523,'gsf',43152345),
(6,'jeeva','SVDSFV','SDVDFV',0,'DVDFV','Andhra Pradesh',9876543222,'SDVSDV',0),
(9,'dreams','dvxdv','xvddxv',671234,'rpm','Andhra Pradesh',9876543222,'aaa@gmail.com',11);

/*Table structure for table `workshop_request` */

DROP TABLE IF EXISTS `workshop_request`;

CREATE TABLE `workshop_request` (
  `request_id` int(11) NOT NULL AUTO_INCREMENT,
  `request_info` varchar(30) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `workshop_id` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

/*Data for the table `workshop_request` */

insert  into `workshop_request`(`request_id`,`request_info`,`customer_id`,`workshop_id`,`date`,`status`) values 
(14,'repair',2,3,'2000-12-04 00:00:00','p'),
(15,'mg',8,0,'2021-05-05 00:00:00','pending'),
(16,'j jf',8,0,'2021-05-05 00:00:00','pending'),
(17,'ulul',8,0,'2021-05-05 00:00:00','pending'),
(18,'zmmzkz',8,0,'2021-05-05 00:00:00','pending'),
(19,'ssa',8,3,'2021-05-05 00:00:00','approved'),
(20,'help',10,3,'2021-05-11 00:00:00','approved');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
