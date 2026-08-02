-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: mini_digi
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailaddress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_emailaddress_user_id_email_987c8728_uniq` (`user_id`,`email`),
  KEY `account_emailaddress_email_03be32b2` (`email`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
INSERT INTO `account_emailaddress` VALUES (1,'ali.alipour4576@gmail.com',0,1,2);
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_address_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailconfirmation`
--

LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add email address',7,'add_emailaddress'),(26,'Can change email address',7,'change_emailaddress'),(27,'Can delete email address',7,'delete_emailaddress'),(28,'Can view email address',7,'view_emailaddress'),(29,'Can add email confirmation',8,'add_emailconfirmation'),(30,'Can change email confirmation',8,'change_emailconfirmation'),(31,'Can delete email confirmation',8,'delete_emailconfirmation'),(32,'Can view email confirmation',8,'view_emailconfirmation'),(33,'Can add social account',9,'add_socialaccount'),(34,'Can change social account',9,'change_socialaccount'),(35,'Can delete social account',9,'delete_socialaccount'),(36,'Can view social account',9,'view_socialaccount'),(37,'Can add social application',10,'add_socialapp'),(38,'Can change social application',10,'change_socialapp'),(39,'Can delete social application',10,'delete_socialapp'),(40,'Can view social application',10,'view_socialapp'),(41,'Can add social application token',11,'add_socialtoken'),(42,'Can change social application token',11,'change_socialtoken'),(43,'Can delete social application token',11,'delete_socialtoken'),(44,'Can view social application token',11,'view_socialtoken'),(45,'Can add category',12,'add_category'),(46,'Can change category',12,'change_category'),(47,'Can delete category',12,'delete_category'),(48,'Can view category',12,'view_category'),(49,'Can add product',14,'add_product'),(50,'Can change product',14,'change_product'),(51,'Can delete product',14,'delete_product'),(52,'Can view product',14,'view_product'),(53,'Can add newsletter',13,'add_newsletter'),(54,'Can change newsletter',13,'change_newsletter'),(55,'Can delete newsletter',13,'delete_newsletter'),(56,'Can view newsletter',13,'view_newsletter'),(57,'Can add cart',15,'add_cart'),(58,'Can change cart',15,'change_cart'),(59,'Can delete cart',15,'delete_cart'),(60,'Can view cart',15,'view_cart'),(61,'Can add cart item',16,'add_cartitem'),(62,'Can change cart item',16,'change_cartitem'),(63,'Can delete cart item',16,'delete_cartitem'),(64,'Can view cart item',16,'view_cartitem'),(65,'Can add order',17,'add_order'),(66,'Can change order',17,'change_order'),(67,'Can delete order',17,'delete_order'),(68,'Can view order',17,'view_order'),(69,'Can add order item',18,'add_orderitem'),(70,'Can change order item',18,'change_orderitem'),(71,'Can delete order item',18,'delete_orderitem'),(72,'Can view order item',18,'view_orderitem'),(73,'Can add user profile',19,'add_userprofile'),(74,'Can change user profile',19,'change_userprofile'),(75,'Can delete user profile',19,'delete_userprofile'),(76,'Can view user profile',19,'view_userprofile'),(77,'Can add product image',20,'add_productimage'),(78,'Can change product image',20,'change_productimage'),(79,'Can delete product image',20,'delete_productimage'),(80,'Can view product image',20,'view_productimage'),(81,'Can add ticket',21,'add_ticket'),(82,'Can change ticket',21,'change_ticket'),(83,'Can delete ticket',21,'delete_ticket'),(84,'Can view ticket',21,'view_ticket'),(85,'Can add ticket attachment',22,'add_ticketattachment'),(86,'Can change ticket attachment',22,'change_ticketattachment'),(87,'Can delete ticket attachment',22,'delete_ticketattachment'),(88,'Can view ticket attachment',22,'view_ticketattachment'),(89,'Can add ticket message',23,'add_ticketmessage'),(90,'Can change ticket message',23,'change_ticketmessage'),(91,'Can delete ticket message',23,'delete_ticketmessage'),(92,'Can view ticket message',23,'view_ticketmessage'),(93,'Can add profile',24,'add_profile'),(94,'Can change profile',24,'change_profile'),(95,'Can delete profile',24,'delete_profile'),(96,'Can view profile',24,'view_profile'),(97,'Can add product variant',25,'add_productvariant'),(98,'Can change product variant',25,'change_productvariant'),(99,'Can delete product variant',25,'delete_productvariant'),(100,'Can view product variant',25,'view_productvariant'),(101,'Can add notification',26,'add_notification'),(102,'Can change notification',26,'change_notification'),(103,'Can delete notification',26,'delete_notification'),(104,'Can view notification',26,'view_notification'),(105,'Can add comment',27,'add_comment'),(106,'Can change comment',27,'change_comment'),(107,'Can delete comment',27,'delete_comment'),(108,'Can view comment',27,'view_comment');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1200000$g5vkbJrNYVFik2p8ibDePd$eiPEPw14wjJI5Wxb9MKmogq8aK1ZeC4LOAvnD7IOMDs=','2026-07-20 10:45:21.000000',1,'admin','Max','Miller','programmers378@gmail.com',1,1,'2026-07-19 13:47:52.000000'),(2,'pbkdf2_sha256$1200000$Gewp9joYZf582QBoAKlbU6$hfhlMoOpF8R2oNnOtM988PwoqUdLdcOzdVCMe/ZVPCM=','2026-07-27 21:30:54.229019',0,'max','Max','Miller','ali.alipour4576@gmail.com',0,1,'2026-07-27 21:30:52.423706');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart_cart`
--

DROP TABLE IF EXISTS `cart_cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart_cart` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `cart_cart_user_id_9b4220b9_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_cart`
--

LOCK TABLES `cart_cart` WRITE;
/*!40000 ALTER TABLE `cart_cart` DISABLE KEYS */;
INSERT INTO `cart_cart` VALUES (1,'2026-07-19 13:49:12.812892',1),(2,'2026-07-29 22:14:36.331408',2);
/*!40000 ALTER TABLE `cart_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart_cartitem`
--

DROP TABLE IF EXISTS `cart_cartitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart_cartitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `cart_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cart_cartitem_product_id_b24e265a_fk_shop_product_id` (`product_id`),
  KEY `cart_cartitem_cart_id_370ad265` (`cart_id`),
  CONSTRAINT `cart_cartitem_cart_id_370ad265_fk_cart_cart_id` FOREIGN KEY (`cart_id`) REFERENCES `cart_cart` (`id`),
  CONSTRAINT `cart_cartitem_product_id_b24e265a_fk_shop_product_id` FOREIGN KEY (`product_id`) REFERENCES `shop_product` (`id`),
  CONSTRAINT `cart_cartitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_cartitem`
--

LOCK TABLES `cart_cartitem` WRITE;
/*!40000 ALTER TABLE `cart_cartitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `cart_cartitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_notification`
--

DROP TABLE IF EXISTS `dashboard_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `notification_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `link` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `dashboard_notification_user_id_e4f6848c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `dashboard_notification_user_id_e4f6848c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_notification`
--

LOCK TABLES `dashboard_notification` WRITE;
/*!40000 ALTER TABLE `dashboard_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_profile`
--

DROP TABLE IF EXISTS `dashboard_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bio` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `avatar` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `address_line1` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address_line2` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `state` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `zip_code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `dashboard_profile_user_id_3e392fce_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_profile`
--

LOCK TABLES `dashboard_profile` WRITE;
/*!40000 ALTER TABLE `dashboard_profile` DISABLE KEYS */;
INSERT INTO `dashboard_profile` VALUES (1,'','','','2026-07-27 21:41:36.508045','2026-07-27 21:41:36.508096',1,'','','','',''),(2,'+09031960860','','','2026-07-27 21:41:36.572364','2026-07-28 22:30:38.058028',2,'sdfsdf','sfsfsdfsf','Tehran','OH','1234567788');
/*!40000 ALTER TABLE `dashboard_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-07-20 18:57:19.663435','12','Django for Beginners',2,'[{\"changed\": {\"fields\": [\"Name fr\", \"Description fr\", \"Name ru\", \"Description ru\", \"Name de\", \"Description de\", \"Name es\", \"Description es\", \"Slug\"]}}]',14,1),(2,'2026-07-27 21:28:27.326350','1','admin',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\"]}}]',4,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (7,'account','emailaddress'),(8,'account','emailconfirmation'),(1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(15,'cart','cart'),(16,'cart','cartitem'),(5,'contenttypes','contenttype'),(26,'dashboard','notification'),(24,'dashboard','profile'),(19,'dashboard','userprofile'),(17,'orders','order'),(18,'orders','orderitem'),(27,'reviews','comment'),(6,'sessions','session'),(12,'shop','category'),(13,'shop','newsletter'),(14,'shop','product'),(20,'shop','productimage'),(25,'shop','productvariant'),(9,'socialaccount','socialaccount'),(10,'socialaccount','socialapp'),(11,'socialaccount','socialtoken'),(21,'support','ticket'),(22,'support','ticketattachment'),(23,'support','ticketmessage');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-07-19 13:21:23.460270'),(2,'auth','0001_initial','2026-07-19 13:21:24.330231'),(3,'account','0001_initial','2026-07-19 13:21:24.639986'),(4,'account','0002_email_max_length','2026-07-19 13:21:24.670380'),(5,'account','0003_alter_emailaddress_create_unique_verified_email','2026-07-19 13:21:24.715328'),(6,'account','0004_alter_emailaddress_drop_unique_email','2026-07-19 13:21:24.770998'),(7,'account','0005_emailaddress_idx_upper_email','2026-07-19 13:21:24.810504'),(8,'account','0006_emailaddress_lower','2026-07-19 13:21:24.879243'),(9,'account','0007_emailaddress_idx_email','2026-07-19 13:21:24.986047'),(10,'account','0008_emailaddress_unique_primary_email_fixup','2026-07-19 13:21:25.010178'),(11,'account','0009_emailaddress_unique_primary_email','2026-07-19 13:21:25.038522'),(12,'admin','0001_initial','2026-07-19 13:21:25.213855'),(13,'admin','0002_logentry_remove_auto_add','2026-07-19 13:21:25.228914'),(14,'admin','0003_logentry_add_action_flag_choices','2026-07-19 13:21:25.254965'),(15,'contenttypes','0002_remove_content_type_name','2026-07-19 13:21:25.394142'),(16,'auth','0002_alter_permission_name_max_length','2026-07-19 13:21:25.479761'),(17,'auth','0003_alter_user_email_max_length','2026-07-19 13:21:25.524387'),(18,'auth','0004_alter_user_username_opts','2026-07-19 13:21:25.542212'),(19,'auth','0005_alter_user_last_login_null','2026-07-19 13:21:25.626689'),(20,'auth','0006_require_contenttypes_0002','2026-07-19 13:21:25.629597'),(21,'auth','0007_alter_validators_add_error_messages','2026-07-19 13:21:25.659599'),(22,'auth','0008_alter_user_username_max_length','2026-07-19 13:21:25.754831'),(23,'auth','0009_alter_user_last_name_max_length','2026-07-19 13:21:25.844799'),(24,'auth','0010_alter_group_name_max_length','2026-07-19 13:21:25.876660'),(25,'auth','0011_update_proxy_permissions','2026-07-19 13:21:25.893796'),(26,'auth','0012_alter_user_first_name_max_length','2026-07-19 13:21:25.977799'),(27,'shop','0001_initial','2026-07-19 13:21:26.136902'),(28,'shop','0002_product_image','2026-07-19 13:21:26.199577'),(29,'shop','0003_category_image','2026-07-19 13:21:26.259349'),(30,'shop','0004_product_available','2026-07-19 13:21:26.337493'),(31,'shop','0005_newsletter_category_name_fr_category_name_ru_and_more','2026-07-19 13:21:26.781738'),(32,'shop','0006_product_color_product_favorited_by_and_more','2026-07-19 13:21:27.357409'),(33,'cart','0001_initial','2026-07-19 13:21:27.686908'),(34,'cart','0002_alter_cartitem_unique_together','2026-07-19 13:21:27.721621'),(35,'cart','0003_alter_cartitem_unique_together','2026-07-19 13:21:27.805637'),(36,'dashboard','0001_initial','2026-07-19 13:21:27.942807'),(37,'orders','0001_initial','2026-07-19 13:21:28.233203'),(38,'orders','0002_order_orders_orde_created_0e92de_idx','2026-07-19 13:21:28.279404'),(39,'orders','0003_remove_order_orders_orde_created_0e92de_idx','2026-07-19 13:21:28.318482'),(40,'sessions','0001_initial','2026-07-19 13:21:28.367988'),(41,'shop','0007_category_name_de_category_name_es_and_more','2026-07-19 13:21:28.994217'),(42,'shop','0008_remove_product_shop_produc_availab_388fee_idx_and_more','2026-07-19 13:21:29.704944'),(43,'shop','0009_product_color_size_favorites','2026-07-19 13:21:30.203594'),(44,'socialaccount','0001_initial','2026-07-19 13:21:30.598455'),(45,'socialaccount','0002_token_max_lengths','2026-07-19 13:21:30.671159'),(46,'socialaccount','0003_extra_data_default_dict','2026-07-19 13:21:30.698731'),(47,'socialaccount','0004_app_provider_id_settings','2026-07-19 13:21:30.904167'),(48,'socialaccount','0005_socialtoken_nullable_app','2026-07-19 13:21:31.092703'),(49,'socialaccount','0006_alter_socialaccount_extra_data','2026-07-19 13:21:31.207161'),(50,'shop','0010_add_de_es_translations','2026-07-20 11:05:31.502216'),(52,'shop','0011_product_meta_description_product_meta_title_and_more','2026-07-20 15:45:50.832474'),(53,'shop','0012_product_meta_description_product_meta_title_and_more','2026-07-20 19:14:58.563589'),(54,'shop','0013_remove_de_es_ru_fr_columns','2026-07-20 19:14:58.567330'),(55,'support','0001_initial','2026-07-20 22:44:47.100811'),(56,'shop','0012_remove_product_description_fr_and_more','2026-07-21 21:19:38.493239'),(57,'shop','0012_remove_category_name_de_remove_category_name_es_and_more','2026-07-21 21:29:21.653098'),(58,'dashboard','0002_profile_delete_userprofile','2026-07-24 21:11:38.445974'),(59,'shop','0013_productvariant','2026-07-24 21:23:15.181773'),(60,'shop','0014_product_food_pairing_product_tasting_notes','2026-07-27 20:22:17.206476'),(61,'dashboard','0003_add_notification','2026-07-28 13:47:13.734457'),(62,'dashboard','0004_rename_phone_number_profile_phone_and_more','2026-07-28 22:27:09.522317'),(63,'reviews','0001_initial','2026-07-29 21:54:42.752909'),(64,'shop','0015_productvariant_is_default_alter_product_slug_and_more','2026-07-30 19:04:04.265125'),(65,'shop','0016_remove_product_image','2026-07-30 19:17:49.841919'),(66,'shop','0017_alter_productvariant_image','2026-08-02 14:41:24.702838');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1bs3sw47lz9f9bcjk0tcmrkbnsd5j94r','.eJxVj8tOxDAMRf_F6yrKq23SJXu-AKHKSVwaoMmoSQVoNP9OA7OZneVzfeR7BfQ-H6nOeNSVUo0ea8xp3qiuORSYXq7wP8MEFyzlK-8BOsAKkxiN1oOxSjFutVGj7uAotCfc6Exj2GKC22sHf_K5oTk2j4CHnUP_QamB8I7pLTOfU92jYy3C7rSw5xzo8-mefRCsWNbz2iiHOijHh14S-vO1RWszBC4XL7gX1KM0JphR654LK50ckZREoxdL1tsmLVRK60_fl7j_wMRvvzi3X80:1wlRsz:-v-9I-2gNM9tdvnWtkT3SNgxWXig8ON5XuHg8FRfsoo','2026-08-02 13:48:53.124012'),('8u51xyishy3rfxzeeu3b9wuyilmmux7p','.eJxVj8FOxSAQRf9l1g0BCi106d4vMKYZYGpRCy-FRs3L-3eLvs3bTeaee5J7BfQ-H6nOeNSVUo0ea8xp3qiuORSYXq7wf8MEFyzlK-8BOsAKkxiN0kr1UjDNtdZSd3AU2hNudNIYtpjg9trBn3xu0RybR8DDz6H_oNSC8I7pLTOfU92jYw1h97Sw5xzo8-nOPghWLOvZNr1DFXrHBy0JvRrMopQZApeLF9wL0iiNCWZUSnNhpZMjUi_RqMWS9bZJC5XS9tP3Je4_50bJ7cD57RdmrWDp:1wllUv:niXkGtknHsiH7k8_PyZn1ftmrR7a8tTFg66u2caJ2tM','2026-08-03 10:45:21.651608'),('tnfd1mq88wr0bdb6tbogc9c47ci4eg67','.eJxVjcsKwjAQRf8laynm1abuFP9AXIfJdEKDMYU0EUT8d1vppsv7OvfDAHGqqdgX5eADDZaeECI7pRrjgVmoZbR1pmzDwE5MsJ3nAB-U1gBiXO1mwzX_zhbPzXlRlEpAKGFKl221Q40wj-tBi7pTwimplSGDR_SqE3ogJ8BL50WHuieunOLSgeKIII0wLe-56EHoBYo1Z0r4Xmj325V9f2HHTIQ:1wpCpN:2tNV1rvgLtz59_Ppv_Nu0lsNU8Q5wSjrj6rHwoZWX5Y','2026-08-12 22:32:41.045212');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_order`
--

DROP TABLE IF EXISTS `orders_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `total_price` decimal(12,0) NOT NULL,
  `is_paid` tinyint(1) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_order_user_id_e9b59eb1_fk_auth_user_id` (`user_id`),
  CONSTRAINT `orders_order_user_id_e9b59eb1_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_order`
--

LOCK TABLES `orders_order` WRITE;
/*!40000 ALTER TABLE `orders_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_orderitem`
--

DROP TABLE IF EXISTS `orders_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `price` decimal(12,0) NOT NULL,
  `order_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` (`order_id`),
  KEY `orders_orderitem_product_id_afe4254a_fk_shop_product_id` (`product_id`),
  CONSTRAINT `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`),
  CONSTRAINT `orders_orderitem_product_id_afe4254a_fk_shop_product_id` FOREIGN KEY (`product_id`) REFERENCES `shop_product` (`id`),
  CONSTRAINT `orders_orderitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_orderitem`
--

LOCK TABLES `orders_orderitem` WRITE;
/*!40000 ALTER TABLE `orders_orderitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews_comment`
--

DROP TABLE IF EXISTS `reviews_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews_comment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rating` smallint unsigned DEFAULT NULL,
  `body` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `parent_id` bigint DEFAULT NULL,
  `product_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reviews_comment_parent_id_f100a641_fk_reviews_comment_id` (`parent_id`),
  KEY `reviews_comment_product_id_6701f4e9_fk_shop_product_id` (`product_id`),
  KEY `reviews_comment_user_id_1d319c7d_fk_auth_user_id` (`user_id`),
  CONSTRAINT `reviews_comment_parent_id_f100a641_fk_reviews_comment_id` FOREIGN KEY (`parent_id`) REFERENCES `reviews_comment` (`id`),
  CONSTRAINT `reviews_comment_product_id_6701f4e9_fk_shop_product_id` FOREIGN KEY (`product_id`) REFERENCES `shop_product` (`id`),
  CONSTRAINT `reviews_comment_user_id_1d319c7d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `reviews_comment_chk_1` CHECK ((`rating` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews_comment`
--

LOCK TABLES `reviews_comment` WRITE;
/*!40000 ALTER TABLE `reviews_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews_comment_dislikes`
--

DROP TABLE IF EXISTS `reviews_comment_dislikes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews_comment_dislikes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comment_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reviews_comment_dislikes_comment_id_user_id_d9e220c9_uniq` (`comment_id`,`user_id`),
  KEY `reviews_comment_dislikes_user_id_479c4533_fk_auth_user_id` (`user_id`),
  CONSTRAINT `reviews_comment_disl_comment_id_c75a9476_fk_reviews_c` FOREIGN KEY (`comment_id`) REFERENCES `reviews_comment` (`id`),
  CONSTRAINT `reviews_comment_dislikes_user_id_479c4533_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews_comment_dislikes`
--

LOCK TABLES `reviews_comment_dislikes` WRITE;
/*!40000 ALTER TABLE `reviews_comment_dislikes` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews_comment_dislikes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews_comment_likes`
--

DROP TABLE IF EXISTS `reviews_comment_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews_comment_likes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comment_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reviews_comment_likes_comment_id_user_id_c00d83a9_uniq` (`comment_id`,`user_id`),
  KEY `reviews_comment_likes_user_id_e300dd9d_fk_auth_user_id` (`user_id`),
  CONSTRAINT `reviews_comment_likes_comment_id_09ac1db4_fk_reviews_comment_id` FOREIGN KEY (`comment_id`) REFERENCES `reviews_comment` (`id`),
  CONSTRAINT `reviews_comment_likes_user_id_e300dd9d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews_comment_likes`
--

LOCK TABLES `reviews_comment_likes` WRITE;
/*!40000 ALTER TABLE `reviews_comment_likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews_comment_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shop_category`
--

DROP TABLE IF EXISTS `shop_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shop_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_category`
--

LOCK TABLES `shop_category` WRITE;
/*!40000 ALTER TABLE `shop_category` DISABLE KEYS */;
INSERT INTO `shop_category` VALUES (37,'Electronics','electronics','categories/cat-1.jpg'),(38,'Clothing','clothing','categories/cat-2.jpg'),(39,'Home & Kitchen','home','categories/cat-3.jpg'),(40,'Books','books','categories/cat-4.jpg');
/*!40000 ALTER TABLE `shop_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shop_newsletter`
--

DROP TABLE IF EXISTS `shop_newsletter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shop_newsletter` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `shop_newsle_created_4f12cc_idx` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_newsletter`
--

LOCK TABLES `shop_newsletter` WRITE;
/*!40000 ALTER TABLE `shop_newsletter` DISABLE KEYS */;
INSERT INTO `shop_newsletter` VALUES (1,'sdfsdfsdfqe@gmail.com','2026-07-19 13:49:06.668984',1);
/*!40000 ALTER TABLE `shop_newsletter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shop_product`
--

DROP TABLE IF EXISTS `shop_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shop_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(12,0) NOT NULL,
  `stock` int unsigned NOT NULL,
  `created` datetime(6) NOT NULL,
  `category_id` bigint NOT NULL,
  `available` tinyint(1) NOT NULL,
  `color` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `size` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `favorites_count` int unsigned NOT NULL,
  `meta_description` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `meta_title` varchar(70) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(220) COLLATE utf8mb4_unicode_ci NOT NULL,
  `food_pairing` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `tasting_notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shop_product_slug_30bd2d5d_uniq` (`slug`),
  KEY `shop_product_category_id_14d7eea8_fk_shop_category_id` (`category_id`),
  CONSTRAINT `shop_product_category_id_14d7eea8_fk_shop_category_id` FOREIGN KEY (`category_id`) REFERENCES `shop_category` (`id`),
  CONSTRAINT `shop_product_chk_1` CHECK ((`stock` >= 0)),
  CONSTRAINT `shop_product_chk_2` CHECK ((`favorites_count` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_product`
--

LOCK TABLES `shop_product` WRITE;
/*!40000 ALTER TABLE `shop_product` DISABLE KEYS */;
INSERT INTO `shop_product` VALUES (109,'Laptop ASUS','Powerful laptop for work/gaming',25000000,15,'2026-08-02 14:41:35.317017',37,1,'','',0,'','','laptop-asus','Roasted duck, mushroom risotto, Parmesan...','Deep ruby with purple reflections. Silky texture...'),(110,'iPhone 15','Latest Apple smartphone',45000000,8,'2026-08-02 14:41:35.338822',37,1,'','',0,'','','iphone-15','Seafood, grilled fish, fresh goat cheese...','Pale straw yellow with citrus and white flowers...'),(111,'Samsung TV 55\"','4K Smart TV',32000000,5,'2026-08-02 14:41:35.363043',37,1,'','',0,'','','samsung-tv-55','Grilled ribeye, lamb rack, aged cheeses...','Intense ruby red with blackberry and vanilla...'),(112,'Wireless Mouse','Ergonomic wireless mouse',450000,50,'2026-08-02 14:41:35.378832',37,1,'','',0,'','','wireless-mouse','Hard cheeses, dried meats, dark chocolate...','Pale straw yellow with citrus and white flowers...'),(113,'Men\'s Jacket','Winter warm jacket',1200000,30,'2026-08-02 14:41:35.397032',38,1,'','',0,'','','mens-jacket','Hard cheeses, dried meats, dark chocolate...','Pale straw yellow with citrus and white flowers...'),(114,'Women\'s Dress','Summer collection dress',890000,25,'2026-08-02 14:41:35.416229',38,1,'','',0,'','','womens-dress','Spicy dishes, BBQ ribs, blue cheese...','Golden amber with dried fruit and honey...'),(115,'Running Shoes','Lightweight sports shoes',2100000,20,'2026-08-02 14:41:35.506123',38,1,'','',0,'','','running-shoes','Roasted duck, mushroom risotto, Parmesan...','Golden amber with dried fruit and honey...'),(116,'Coffee Maker','Automatic espresso machine',5600000,12,'2026-08-02 14:41:35.534721',39,1,'','',0,'','','coffee-maker','Spicy dishes, BBQ ribs, blue cheese...','Pale straw yellow with citrus and white flowers...'),(117,'Blender','High-speed kitchen blender',3200000,18,'2026-08-02 14:41:35.554087',39,1,'','',0,'','','blender','Hard cheeses, dried meats, dark chocolate...','Intense ruby red with blackberry and vanilla...'),(118,'Cookware Set','10-piece non-stick set',4500000,10,'2026-08-02 14:41:35.569161',39,1,'','',0,'','','cookware-set','Hard cheeses, dried meats, dark chocolate...','Pale straw yellow with citrus and white flowers...'),(119,'Python Programming','Learn Python programming',350000,40,'2026-08-02 14:41:35.578108',40,1,'','',0,'','','python-programming','Grilled ribeye, lamb rack, aged cheeses...','Intense ruby red with blackberry and vanilla...'),(120,'Django for Beginners','Build web apps with Django',280000,35,'2026-08-02 14:41:35.587105',40,1,'','',0,'','','django-for-beginners','Grilled ribeye, lamb rack, aged cheeses...','Golden amber with dried fruit and honey...');
/*!40000 ALTER TABLE `shop_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shop_product_favorited_by`
--

DROP TABLE IF EXISTS `shop_product_favorited_by`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shop_product_favorited_by` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shop_product_favorited_by_product_id_user_id_dc8c9b32_uniq` (`product_id`,`user_id`),
  KEY `shop_product_favorited_by_user_id_4d837568_fk_auth_user_id` (`user_id`),
  CONSTRAINT `shop_product_favorited_by_product_id_1afd4b2b_fk_shop_product_id` FOREIGN KEY (`product_id`) REFERENCES `shop_product` (`id`),
  CONSTRAINT `shop_product_favorited_by_user_id_4d837568_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_product_favorited_by`
--

LOCK TABLES `shop_product_favorited_by` WRITE;
/*!40000 ALTER TABLE `shop_product_favorited_by` DISABLE KEYS */;
/*!40000 ALTER TABLE `shop_product_favorited_by` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shop_productvariant`
--

DROP TABLE IF EXISTS `shop_productvariant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shop_productvariant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sku` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `size` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `stock` int unsigned NOT NULL,
  `price_override` decimal(12,0) DEFAULT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `product_id` bigint NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku` (`sku`),
  KEY `shop_productvariant_product_id_3268ff6d_fk_shop_product_id` (`product_id`),
  CONSTRAINT `shop_productvariant_product_id_3268ff6d_fk_shop_product_id` FOREIGN KEY (`product_id`) REFERENCES `shop_product` (`id`),
  CONSTRAINT `shop_productvariant_chk_1` CHECK ((`stock` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=209 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_productvariant`
--

LOCK TABLES `shop_productvariant` WRITE;
/*!40000 ALTER TABLE `shop_productvariant` DISABLE KEYS */;
INSERT INTO `shop_productvariant` VALUES (181,NULL,'','silver',15,NULL,'products/laptop-asus/default.jpg',1,109,1),(182,NULL,'','gray',15,NULL,'products/laptop-asus/variant_2.jpg',1,109,0),(183,NULL,'','gold',15,NULL,'products/laptop-asus/variant_3.jpg',1,109,0),(184,NULL,'','black',8,NULL,'products/iphone-15/default.jpg',1,110,1),(185,NULL,'','white',8,NULL,'products/iphone-15/variant_2.jpg',1,110,0),(186,NULL,'','gold',8,NULL,'products/iphone-15/variant_3.jpg',1,110,0),(187,NULL,'','gray',5,NULL,'products/samsung-tv-55/default.jpg',1,111,1),(188,NULL,'','black',5,NULL,'products/samsung-tv-55/variant_2.jpg',1,111,0),(189,NULL,'','black',50,NULL,'products/wireless-mouse/default.jpg',1,112,1),(190,NULL,'','white',50,NULL,'products/wireless-mouse/variant_2.jpg',1,112,0),(191,NULL,'','red',50,NULL,'products/wireless-mouse/variant_3.jpg',1,112,0),(192,NULL,'S','black',30,NULL,'products/mens-jacket/default.jpg',1,113,1),(193,NULL,'M','black',30,NULL,'products/mens-jacket/variant_2.jpg',1,113,0),(194,NULL,'L','black',30,NULL,'products/mens-jacket/variant_3.jpg',1,113,0),(195,NULL,'M','blue',30,NULL,'products/mens-jacket/variant_4.jpg',1,113,0),(196,NULL,'M','red',25,NULL,'products/womens-dress/default.jpg',1,114,1),(197,NULL,'S','blue',25,NULL,'products/womens-dress/variant_2.jpg',1,114,0),(198,NULL,'L','green',25,NULL,'products/womens-dress/variant_3.jpg',1,114,0),(199,NULL,'42','white',20,NULL,'products/running-shoes/default.jpg',1,115,1),(200,NULL,'42','black',20,NULL,'products/running-shoes/variant_2.jpg',1,115,0),(201,NULL,'44','white',20,NULL,'products/running-shoes/variant_3.jpg',1,115,0),(202,NULL,'','silver',12,NULL,'products/coffee-maker/default.jpg',1,116,1),(203,NULL,'','black',12,NULL,'products/coffee-maker/variant_2.jpg',1,116,0),(204,NULL,'','white',18,NULL,'products/blender/default.jpg',1,117,1),(205,NULL,'','black',18,NULL,'products/blender/variant_2.jpg',1,117,0),(206,NULL,'','stainless',10,NULL,'products/cookware-set/default.jpg',1,118,1),(207,NULL,'','',40,NULL,'products/python-programming/default.jpg',1,119,1),(208,NULL,'','',35,NULL,'products/django-for-beginners/default.jpg',1,120,1);
/*!40000 ALTER TABLE `shop_productvariant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uid` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` json NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialaccount`
--

LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `client_id` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `secret` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `key` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `provider_id` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `settings` json NOT NULL DEFAULT (_utf8mb4'{}'),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp`
--

LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int NOT NULL AUTO_INCREMENT,
  `token` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `token_secret` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int NOT NULL,
  `app_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialtoken`
--

LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `support_ticket`
--

DROP TABLE IF EXISTS `support_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `support_ticket` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subject` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `support_ticket_user_id_d7c9336a_fk_auth_user_id` (`user_id`),
  CONSTRAINT `support_ticket_user_id_d7c9336a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `support_ticket`
--

LOCK TABLES `support_ticket` WRITE;
/*!40000 ALTER TABLE `support_ticket` DISABLE KEYS */;
INSERT INTO `support_ticket` VALUES (1,'ادامه کار','open','2026-07-20 23:11:09.996175','2026-07-20 23:11:09.996207',1),(2,'sdfs','open','2026-07-22 20:33:44.830453','2026-07-22 20:33:44.830480',1),(3,'qq','open','2026-07-22 21:04:12.199115','2026-07-22 21:04:12.199153',1),(4,'qq','open','2026-07-22 21:04:24.349739','2026-07-22 21:04:24.349766',1),(5,'qq','open','2026-07-22 21:04:30.344946','2026-07-22 21:04:30.344971',1),(6,'qq','open','2026-07-22 21:04:57.756896','2026-07-22 21:04:57.756930',1);
/*!40000 ALTER TABLE `support_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `support_ticketattachment`
--

DROP TABLE IF EXISTS `support_ticketattachment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `support_ticketattachment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `message_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `support_ticketattach_message_id_09887e4b_fk_support_t` (`message_id`),
  CONSTRAINT `support_ticketattach_message_id_09887e4b_fk_support_t` FOREIGN KEY (`message_id`) REFERENCES `support_ticketmessage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `support_ticketattachment`
--

LOCK TABLES `support_ticketattachment` WRITE;
/*!40000 ALTER TABLE `support_ticketattachment` DISABLE KEYS */;
INSERT INTO `support_ticketattachment` VALUES (1,'tickets/attachments/views.py','2026-07-20 23:11:10.030047',1);
/*!40000 ALTER TABLE `support_ticketattachment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `support_ticketmessage`
--

DROP TABLE IF EXISTS `support_ticketmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `support_ticketmessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_staff_reply` tinyint(1) NOT NULL,
  `body` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `ticket_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `support_ticketmessage_ticket_id_70fe8f82_fk_support_ticket_id` (`ticket_id`),
  CONSTRAINT `support_ticketmessage_ticket_id_70fe8f82_fk_support_ticket_id` FOREIGN KEY (`ticket_id`) REFERENCES `support_ticket` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `support_ticketmessage`
--

LOCK TABLES `support_ticketmessage` WRITE;
/*!40000 ALTER TABLE `support_ticketmessage` DISABLE KEYS */;
INSERT INTO `support_ticketmessage` VALUES (1,0,'sfsdfs','2026-07-20 23:11:10.000460',1),(2,0,'dfgdfgdfgdg','2026-07-20 23:30:43.411888',1),(3,0,'dgdfg','2026-07-22 16:13:00.103518',1),(4,0,'dgdfg','2026-07-22 16:14:38.383854',1),(5,0,'dgdfg','2026-07-22 16:32:57.272915',1),(6,0,'sdfsd','2026-07-22 20:33:45.350119',2),(7,0,'qqqqq','2026-07-22 21:04:12.203240',3),(8,0,'qqqqq','2026-07-22 21:04:24.353907',4),(9,0,'qqqqq','2026-07-22 21:04:30.349118',5),(10,0,'qqqqq','2026-07-22 21:04:57.766705',6),(11,0,'aaaaa','2026-07-27 21:23:46.838667',4);
/*!40000 ALTER TABLE `support_ticketmessage` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-02 18:31:19
