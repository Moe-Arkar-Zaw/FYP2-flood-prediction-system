

-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: flood_system_db
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alerts`
--

DROP TABLE IF EXISTS `alerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alerts` (
  `alert_id` int NOT NULL AUTO_INCREMENT,
  `prediction_id` int DEFAULT NULL,
  `alert_message` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`alert_id`),
  KEY `prediction_id` (`prediction_id`),
  CONSTRAINT `alerts_ibfk_1` FOREIGN KEY (`prediction_id`) REFERENCES `flood_predictions` (`prediction_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alerts`
--

LOCK TABLES `alerts` WRITE;
/*!40000 ALTER TABLE `alerts` DISABLE KEYS */;
INSERT INTO `alerts` VALUES (1,1,'Severe flooding detected! Avoid area.'),(2,9,'Water level rising in Downtown'),(3,23,'This street has water level of 0.87 (severe). Please avoid this street.'),(4,40,'This is latest condition. water level is 0.84. avoid this street.'),(5,41,'alert condition for this street.'),(6,42,'please avoid this area'),(7,44,'Arif is handome with 0.11 m'),(8,47,'Jalan Sekerat 1'),(9,48,'sultanah 1'),(10,55,'rahim is handsome');
/*!40000 ALTER TABLE `alerts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `areas`
--

DROP TABLE IF EXISTS `areas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `areas` (
  `area_id` int NOT NULL AUTO_INCREMENT,
  `area_name` varchar(100) NOT NULL,
  `center_lat` decimal(21,18) DEFAULT NULL,
  `center_lon` decimal(21,18) DEFAULT NULL,
  `radius` float DEFAULT NULL,
  `severity_level` enum('normal','alert','severe') DEFAULT NULL,
  PRIMARY KEY (`area_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `areas`
--

LOCK TABLES `areas` WRITE;
/*!40000 ALTER TABLE `areas` DISABLE KEYS */;
INSERT INTO `areas` VALUES (1,'Downtown',6.121462506009170000,100.366356110398830000,800,'alert'),(2,'City Entrance(Plaza Tol Alor Setar Selatan)',6.082667080009222000,100.374066125236470000,800,'normal'),(3,'City Exit(Alor Setar Utara toll plaza)',6.138226920986917000,100.393952406771120000,800,'severe'),(4,'Others',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `areas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flood_predictions`
--

DROP TABLE IF EXISTS `flood_predictions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flood_predictions` (
  `prediction_id` int NOT NULL AUTO_INCREMENT,
  `video_id` int DEFAULT NULL,
  `street_id` int DEFAULT NULL,
  `water_level` float DEFAULT NULL,
  `severity` enum('normal','alert','severe') DEFAULT 'normal',
  `prediction_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`prediction_id`),
  KEY `video_id` (`video_id`),
  KEY `street_id` (`street_id`),
  CONSTRAINT `flood_predictions_ibfk_1` FOREIGN KEY (`video_id`) REFERENCES `videos` (`video_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `flood_predictions_ibfk_2` FOREIGN KEY (`street_id`) REFERENCES `streets` (`street_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flood_predictions`
--

LOCK TABLES `flood_predictions` WRITE;
/*!40000 ALTER TABLE `flood_predictions` DISABLE KEYS */;
INSERT INTO `flood_predictions` VALUES (1,1,1,0.01,'normal','2025-11-20 14:42:59'),(2,2,2,0.2,'alert','2025-11-20 14:42:59'),(3,3,3,0.01,'normal','2025-11-20 14:42:59'),(4,4,4,0.6,'severe','2025-11-20 14:42:59'),(5,5,5,0.7,'severe','2025-11-20 14:42:59'),(6,6,6,0.02,'normal','2025-11-20 14:42:59'),(7,7,7,0.2,'alert','2025-11-20 14:42:59'),(8,8,8,0.3,'alert','2025-11-20 06:43:21'),(9,8,8,0.72,'severe','2025-11-20 08:17:34'),(10,22,9,0.39,'alert','2025-12-02 16:07:18'),(11,22,9,0.96,'severe','2025-12-02 16:07:30'),(12,22,9,0.04,'normal','2025-12-02 16:07:34'),(13,25,2,0.91,'severe','2025-12-02 16:11:17'),(14,26,4,0.52,'alert','2025-12-02 16:31:14'),(15,26,4,0.43,'alert','2025-12-02 16:32:03'),(16,26,4,0.02,'normal','2025-12-02 16:32:19'),(17,26,4,0.33,'alert','2025-12-02 16:32:24'),(18,26,4,0.74,'severe','2025-12-02 16:32:31'),(19,26,4,0.62,'severe','2025-12-02 16:32:36'),(20,26,4,0.31,'alert','2025-12-02 16:32:40'),(21,26,4,0.76,'severe','2025-12-02 16:32:44'),(22,26,4,0.49,'alert','2025-12-02 16:32:48'),(23,26,4,0.87,'severe','2025-12-02 16:32:52'),(24,27,7,0.57,'alert','2025-12-02 16:33:10'),(25,27,7,0.32,'alert','2025-12-02 16:33:29'),(26,28,9,0.18,'normal','2025-12-02 16:46:10'),(27,28,9,0.77,'severe','2025-12-02 16:46:18'),(28,28,9,0.9,'severe','2025-12-02 16:46:48'),(29,28,9,0.02,'normal','2025-12-02 16:47:06'),(30,28,9,0.53,'alert','2025-12-02 16:47:25'),(31,28,9,0.11,'normal','2025-12-02 16:47:44'),(32,29,12,0.48,'alert','2025-12-02 16:49:16'),(33,33,12,0.4,'alert','2025-12-02 17:08:26'),(34,33,12,0.36,'alert','2025-12-02 17:09:56'),(35,33,12,0.95,'severe','2025-12-02 17:09:59'),(36,33,12,0.34,'alert','2025-12-02 17:10:03'),(37,33,12,0.27,'normal','2025-12-02 17:13:04'),(38,34,6,0.97,'severe','2025-12-04 07:33:08'),(39,36,9,0.52,'alert','2025-12-04 14:17:16'),(40,36,9,0.84,'severe','2025-12-04 14:17:35'),(41,37,7,0.35,'alert','2025-12-04 14:18:51'),(42,38,4,0.6,'severe','2025-12-04 14:21:51'),(43,39,7,0.61,'severe','2025-12-05 08:28:27'),(44,39,7,0.11,'normal','2025-12-05 08:28:45'),(45,39,7,0.93,'severe','2025-12-05 08:32:24'),(46,39,7,0.77,'severe','2025-12-05 08:39:29'),(47,40,6,0.95,'severe','2025-12-06 08:25:39'),(48,41,9,0.79,'severe','2025-12-06 08:26:36'),(49,42,12,0.81,'severe','2025-12-06 08:28:41'),(50,45,12,0.11,'normal','2025-12-06 08:29:19'),(51,46,6,0.38,'alert','2025-12-06 08:29:33'),(52,48,7,0.37,'alert','2025-12-06 09:42:30'),(53,49,9,0.82,'severe','2025-12-06 09:45:44'),(54,50,10,0.42,'alert','2025-12-06 09:46:03'),(55,51,1,0.98,'severe','2025-12-07 10:13:43'),(56,52,1,0.24,'normal','2025-12-07 10:23:25'),(57,53,1,0.63,'severe','2025-12-08 12:59:00'),(58,54,2,0.57,'alert','2025-12-08 13:03:13'),(59,55,1,0.71,'severe','2025-12-08 13:15:13'),(60,56,1,0.66,'severe','2025-12-08 13:15:36'),(61,57,2,0.13,'normal','2025-12-08 13:15:53'),(62,58,2,0.52,'alert','2025-12-08 21:31:56'),(63,59,1,0.94,'severe','2025-12-08 23:18:38'),(64,60,2,0.15,'normal','2025-12-08 23:18:52'),(65,61,6,0.82,'severe','2025-12-08 23:19:06'),(66,62,7,0.29,'normal','2025-12-08 23:19:19'),(67,63,1,0.08,'normal','2025-12-09 00:22:05'),(68,64,2,0.49,'alert','2025-12-09 00:22:15'),(69,65,6,0.09,'normal','2025-12-09 00:22:25'),(70,66,7,0.39,'alert','2025-12-09 00:22:36'),(71,67,1,0.43,'alert','2025-12-09 00:23:56'),(72,68,2,0.26,'normal','2025-12-09 00:24:05'),(73,69,6,0.88,'severe','2025-12-09 00:24:16'),(74,70,7,0.55,'alert','2025-12-09 00:24:26'),(75,71,1,0.65,'severe','2025-12-09 01:12:55'),(76,72,2,0.14,'normal','2025-12-09 01:13:13'),(77,73,6,0.7,'severe','2025-12-09 01:13:29'),(78,74,7,0.65,'severe','2025-12-09 01:13:43'),(79,75,1,0.2,'normal','2025-12-09 10:28:21'),(80,76,1,0.5,'alert','2025-12-09 10:35:35'),(81,77,2,0.22,'normal','2025-12-09 10:35:53'),(82,78,6,0.11,'normal','2025-12-09 10:36:14'),(83,79,7,0.77,'severe','2025-12-09 10:36:26');
/*!40000 ALTER TABLE `flood_predictions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `routes`
--

DROP TABLE IF EXISTS `routes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `routes` (
  `route_id` int NOT NULL AUTO_INCREMENT,
  `start_street_id` int DEFAULT NULL,
  `end_street_id` int DEFAULT NULL,
  `distance` double DEFAULT NULL,
  `route_start_lat` decimal(21,18) DEFAULT NULL,
  `route_start_lon` decimal(21,18) DEFAULT NULL,
  `route_end_lat` decimal(21,18) DEFAULT NULL,
  `route_end_lon` decimal(21,18) DEFAULT NULL,
  PRIMARY KEY (`route_id`),
  KEY `start_street_id` (`start_street_id`),
  KEY `end_street_id` (`end_street_id`),
  CONSTRAINT `routes_ibfk_1` FOREIGN KEY (`start_street_id`) REFERENCES `streets` (`street_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `routes_ibfk_2` FOREIGN KEY (`end_street_id`) REFERENCES `streets` (`street_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `routes`
--

LOCK TABLES `routes` WRITE;
/*!40000 ALTER TABLE `routes` DISABLE KEYS */;
INSERT INTO `routes` VALUES (1,1,2,156.2100067138672,6.122134339959826000,100.364946326093100000,6.121538437323077000,100.366225761899930000),(5,2,7,173.02999877929688,6.121538437323077000,100.366225761899930000,6.123036314824084000,100.366649704485410000),(6,7,6,156.11000061035156,6.123036314824084000,100.366649704485410000,6.123449616860846000,100.365300291152480000),(7,6,1,151.39999389648438,6.123449616860846000,100.365300291152480000,6.122134339959826000,100.364946326093100000);
/*!40000 ALTER TABLE `routes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shelters`
--

DROP TABLE IF EXISTS `shelters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shelters` (
  `shelter_id` int NOT NULL AUTO_INCREMENT,
  `shelter_name` varchar(150) NOT NULL,
  `shelter_lat` decimal(21,18) DEFAULT NULL,
  `shelter_lon` decimal(21,18) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `capacity` int DEFAULT '0',
  PRIMARY KEY (`shelter_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shelters`
--

LOCK TABLES `shelters` WRITE;
/*!40000 ALTER TABLE `shelters` DISABLE KEYS */;
INSERT INTO `shelters` VALUES (1,'SK Langgar',6.145813465118408000,100.431701660156250000,'256, Kampung Limbong, Alor Setar, Kedah',140),(2,'SMK Alor Merah',6.161590099334717000,100.372657775878900000,'Mentaloon, 05250 Alor Setar, Kedah',123);
/*!40000 ALTER TABLE `shelters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `streets`
--

DROP TABLE IF EXISTS `streets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `streets` (
  `street_id` int NOT NULL AUTO_INCREMENT,
  `street_name` varchar(150) NOT NULL,
  `area_id` int DEFAULT NULL,
  `street_start_lat` decimal(21,18) DEFAULT NULL,
  `street_start_lon` decimal(21,18) DEFAULT NULL,
  `street_end_lat` decimal(21,18) DEFAULT NULL,
  `street_end_lon` decimal(21,18) DEFAULT NULL,
  `current_severity` enum('normal','alert','severe') DEFAULT 'normal',
  `street_label_lat` decimal(21,18) DEFAULT NULL,
  `street_label_lon` decimal(21,18) DEFAULT NULL,
  `base_street_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`street_id`),
  KEY `area_id` (`area_id`),
  CONSTRAINT `streets_ibfk_1` FOREIGN KEY (`area_id`) REFERENCES `areas` (`area_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `streets`
--

LOCK TABLES `streets` WRITE;
/*!40000 ALTER TABLE `streets` DISABLE KEYS */;
INSERT INTO `streets` VALUES (1,'Jln Tunku Abdul Rahman Putra_1',1,6.122134339959826000,100.364946326093100000,6.121538437323077000,100.366225761899930000,'alert',6.121819604305942000,100.365498835060280000,'Jln Tunku Abdul Rahman Putra'),(2,'Darul Aman Hwy_1',1,6.121538437323077000,100.366225761899930000,6.123036314824084000,100.366649704485410000,'normal',6.122401075667511000,100.366632748991750000,'Darul Aman Hwy'),(3,'Darul Aman Hwy_2',1,6.121538437323077000,100.366225761899930000,6.120699614797440000,100.365977768054100000,'normal',6.121035631695115000,100.366187012197910000,'Darul Aman Hwy'),(4,'Jalan Kampung Perak_1',1,6.120699614797440000,100.365977768054100000,6.121585969014566000,100.363188452551370000,'severe',6.121089953639393000,100.364760274365410000,'Jalan Kampung Perak'),(5,'Jalan Kampung Perak_2',1,6.120699614797440000,100.365977768054100000,6.120372207538504000,100.366702835987140000,'severe',6.120523024727904500,100.366366369897260000,'Jalan Kampung Perak'),(6,'Jalan Sekerat',1,6.123449616860846000,100.365300291152480000,6.122134339959826000,100.364946326093100000,'normal',6.122932220123484000,100.365123274118400000,'Jalan Sekerat'),(7,'Jalan Mahdali',1,6.123036314824084000,100.366649704485410000,6.123449616860846000,100.365300291152480000,'severe',6.123297656868467000,100.365893316969230000,'Jalan Mahdali'),(8,'Jalan Kampung Baru',1,6.120372207538504000,100.366702835987140000,6.121545100326656600,100.367362311582870000,'severe',6.121038385942406500,100.367088714588480000,'Jalan Kampung Baru'),(9,'Sultanah Bahiyah Hwy',2,6.083496527908438000,100.377037647324700000,6.081190192031245400,100.369868615857330000,'severe',6.081867646932055000,100.372330867772890000,'Sultanah Bahiyah Hwy'),(10,'Jalan Sultanah',3,6.138708052292078000,100.392176023757440000,6.137267962687690000,100.396821609617330000,'alert',6.138073383934018000,100.394380789677560000,'Jalan Sultanah'),(11,'Jln Langgar_1',3,6.138708052292078000,100.392176023757440000,6.140671105733055000,100.392699647390190000,NULL,6.139929723735738000,100.392286539737330000,'Jln Langgar'),(12,'Jln Langgar_2',3,6.138708052292078000,100.392176023757440000,6.135256672616981000,100.390303291582410000,'normal',6.137043484004012000,100.391091869361360000,'Jln Langgar'),(13,'Lorong Jaya 1/1',3,6.136631944932986000,100.392926854360900000,6.137309321702987000,100.392014903338700000,NULL,6.137090619410449000,100.392556706121330000,'Lorong Jaya 1/1'),(14,'Lorong Jaya 2_1',3,6.137309321702987000,100.392014903338700000,6.137711992082988000,100.392623761419980000,NULL,6.137665421953863000,100.392126593343020000,'Lorong Jaya 2'),(15,'Lorong Jaya 2_2',3,6.137309321702987000,100.392014903338700000,6.136826602470432000,100.391797641086270000,NULL,6.137194328619997000,100.391918284506990000,'Lorong Jaya 2'),(16,'Lorong Jaya 3_1',3,6.136826602470432000,100.391797641086270000,6.137046367685618000,100.391212822186330000,NULL,6.136927939842979000,100.391491828121470000,'Lorong Jaya 3'),(17,'Jalan Permai 15_1',3,6.138464566688811000,100.395220648467760000,6.139445959298311000,100.394770037374440000,NULL,6.139013974123764000,100.395032856410510000,'Jalan Permai 15'),(18,'Jalan Permai 15_2',3,6.139445959298311000,100.394770037374440000,6.140603360232388000,100.392742287411380000,NULL,6.139819354491759000,100.393605971219840000,'Jalan Permai 15');
/*!40000 ALTER TABLE `streets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `user_role` enum('admin','public') DEFAULT 'public',
  `profile_image_url` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'MOE ARIF RAHIM','admin@example.com','$2b$12$KOTKwXsDDpE/RI34GVctq.atMTahFbqnaDJHJFtUZxb1HL3gngZN2','admin','/static/profile_image_uploads/flood_group_photo.jpg'),(2,'user1','user1@example.com','$2b$12$nUcRwPaAztCJ2njEnLRgf.DZXMFnBGLZX48r0qOayb4r7qtW8HjBm','public',NULL),(3,'moeuser','moe@example.com','$2b$12$UnhwUFd2N6VzgpPjPC2ng.oQec47VpYOaoaObjjxD49.cr8wJ2yde','public',NULL),(4,'arif','arif@example.com','$2b$12$/6.J3eW6Y4DuxeHkShyH2.lZET8VYXPkb/V3TCeeE8hXPMKgDlv/S','public',NULL),(5,'rahim','rahim@example.com','$2b$12$B4FCfZsH5Xrk8LMCDiR2oeUJfoEJj1DSj9fEt1Z49VLK.Zrwmv.0u','public',NULL),(6,'MoeArkarZawZaw','moe.zaw@student.aiu.edu.my','$2b$12$quw3SNUXZ7DGPuth6A9ouu5VhsAE1nExwbNj2y5QZ.pAwaqoTIBfy','public',NULL),(7,'moearkararkar','moe.arkar@gmail.com','$2b$12$G3vtxlp/661FZ0Z0nIMYG.FHI8gFhYOtC47YVMhK2/gh92UybKaCe','public',NULL),(8,'rahimarif','rahim.arif@gmail.com','$2b$12$zqmfXsMc2ZpyQt6.or9B2OgZANDXsSsQSikXmWegAm/cf3H9hRZia','public',NULL),(9,'moearif','moearif@gmail.com','$2b$12$If97w34/PhIgeojMJQKI2.79mrcIaTdGY5HpH0Cz9EBzb8wf2G1lO','public','/static/profile_image_uploads/Screenshot_2025-10-20_200550.png'),(10,'user01','user@gmail.com','$2b$12$s8COxZreaAtwv1ecVLvAFeVlGSStjYlSjuVuW4jefGh3bfwu8z6UC','public',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `videos`
--

DROP TABLE IF EXISTS `videos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `videos` (
  `video_id` int NOT NULL AUTO_INCREMENT,
  `street_id` int DEFAULT NULL,
  `video_path` varchar(255) NOT NULL,
  `upload_timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`video_id`),
  KEY `street_id` (`street_id`),
  CONSTRAINT `videos_ibfk_1` FOREIGN KEY (`street_id`) REFERENCES `streets` (`street_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `videos`
--

LOCK TABLES `videos` WRITE;
/*!40000 ALTER TABLE `videos` DISABLE KEYS */;
INSERT INTO `videos` VALUES (1,1,'static/uploads/jalan_merdeka.mp4','2025-11-19 18:17:43'),(2,2,'static/uploads/jalan_utama.mp4','2025-11-19 18:17:43'),(3,3,'static/uploads/jalan_merdeka.mp4','2025-11-19 18:17:43'),(4,4,'static/uploads/jalan_utama.mp4','2025-11-19 18:17:43'),(5,5,'static/uploads/jalan_merdeka.mp4','2025-11-19 18:17:43'),(6,6,'static/uploads/jalan_utama.mp4','2025-11-19 18:17:43'),(7,7,'static/uploads/jalan_merdeka.mp4','2025-11-19 18:17:43'),(8,8,'data/uploads/sample.mp4','2025-01-10 12:30:00'),(9,1,'data/uploads\\sample.mp4','2025-11-28 10:30:00'),(10,1,'data/uploads\\flood_postman_test.mp4','2025-12-02 18:36:00'),(11,7,'data/uploads\\flood_postman_test.mp4','2025-12-02 20:30:00'),(12,11,'data/uploads\\flood_postman_test.mp4','2025-12-02 23:06:00'),(13,11,'data/uploads\\flood_postman_test.mp4','2025-12-02 23:26:00'),(14,2,'data/uploads\\flood_postman_test.mp4','2025-12-02 23:35:00'),(15,12,'data/uploads\\flood_postman_test.mp4','2025-12-02 23:39:00'),(16,2,'data/uploads\\flood_postman_test.mp4','2025-12-02 23:39:00'),(17,11,'data/uploads\\flood_postman_test.mp4','2025-12-02 23:40:00'),(18,9,'data/uploads\\flood_postman_test.mp4','2025-12-02 23:41:00'),(19,4,'data/uploads\\flood_postman_test.mp4','2025-12-02 23:46:00'),(20,2,'data/uploads\\flood_postman_test.mp4','2025-12-02 23:53:00'),(21,1,'data/uploads\\flood_postman_test.mp4','2025-12-02 23:54:00'),(22,9,'data/uploads\\flood_postman_test.mp4','2025-12-03 00:06:00'),(23,9,'data/uploads\\flood_postman_test.mp4','2025-12-03 00:08:00'),(24,10,'data/uploads\\flood_postman_test.mp4','2025-12-03 00:09:00'),(25,2,'data/uploads\\flood_postman_test.mp4','2025-12-03 00:10:00'),(26,4,'data/uploads\\flood_postman_test.mp4','2025-12-03 00:30:00'),(27,7,'data/uploads\\flood_postman_test.mp4','2025-12-03 00:32:00'),(28,9,'data/uploads\\flood_postman_test.mp4','2025-12-03 00:45:00'),(29,12,'data/uploads\\flood_postman_test.mp4','2025-12-03 00:48:00'),(30,8,'data/uploads\\flood_postman_test.mp4','2025-12-03 00:55:00'),(31,10,'data/uploads\\flood_postman_test.mp4','2025-12-03 01:01:00'),(32,10,'data/uploads\\flood_postman_test.mp4','2025-12-03 01:03:00'),(33,12,'data/uploads\\flood_postman_test.mp4','2025-12-03 01:07:00'),(34,6,'data/uploads\\flood_postman_test.mp4','2025-12-04 15:32:00'),(35,9,'data/uploads\\Screen_Recording_2025-11-15_120253.mp4','2025-12-04 15:32:00'),(36,9,'data/uploads\\flood_postman_test.mp4','2025-12-04 22:17:00'),(37,7,'data/uploads\\flood_postman_test.mp4','2025-12-04 22:18:00'),(38,4,'data/uploads\\flood_postman_test.mp4','2025-12-04 22:21:00'),(39,7,'data/uploads\\flood_postman_test.mp4','2025-12-05 16:26:00'),(40,6,'data/uploads\\flood_postman_test.mp4','2025-12-06 16:25:00'),(41,9,'data/uploads\\flood_postman_test.mp4','2025-12-06 16:26:00'),(42,12,'data/uploads\\flood_postman_test.mp4','2025-12-06 16:28:00'),(43,6,'data/uploads\\flood_postman_test.mp4','2025-12-06 16:28:00'),(44,9,'data/uploads\\flood_postman_test.mp4','2025-12-06 16:28:00'),(45,12,'data/uploads\\flood_postman_test.mp4','2025-12-06 16:29:00'),(46,6,'data/uploads\\flood_postman_test.mp4','2025-12-06 16:29:00'),(47,11,'data/uploads\\flood_postman_test.mp4','2025-12-06 17:36:00'),(48,7,'data/uploads\\flood_postman_test.mp4','2025-12-06 17:42:00'),(49,9,'data/uploads\\flood_postman_test.mp4','2025-12-06 17:45:00'),(50,10,'data/uploads\\flood_postman_test.mp4','2025-12-06 17:45:00'),(51,1,'data/uploads\\flood_postman_test.mp4','2025-12-07 18:12:00'),(52,1,'data/uploads\\flood_postman_test.mp4','2025-12-07 18:23:00'),(53,1,'data/uploads\\flood_postman_test.mp4','2025-12-08 20:57:00'),(54,2,'data/uploads\\flood_postman_test.mp4','2025-12-08 21:02:00'),(55,1,'data/uploads\\flood_postman_test.mp4','2025-12-08 21:15:00'),(56,1,'data/uploads\\flood_postman_test.mp4','2025-12-08 21:15:00'),(57,2,'data/uploads\\flood_postman_test.mp4','2025-12-08 21:15:00'),(58,2,'data/uploads\\flood_postman_test.mp4','2025-12-08 21:31:00'),(59,1,'data/uploads\\flood_postman_test.mp4','2025-12-08 23:18:00'),(60,2,'data/uploads\\flood_postman_test.mp4','2025-12-08 23:18:00'),(61,6,'data/uploads\\flood_postman_test.mp4','2025-12-08 23:18:00'),(62,7,'data/uploads\\flood_postman_test.mp4','2025-12-08 23:19:00'),(63,1,'data/uploads\\flood_postman_test.mp4','2025-12-09 00:21:00'),(64,2,'data/uploads\\flood_postman_test.mp4','2025-12-09 00:22:00'),(65,6,'data/uploads\\flood_postman_test.mp4','2025-12-09 00:22:00'),(66,7,'data/uploads\\flood_postman_test.mp4','2025-12-09 00:22:00'),(67,1,'data/uploads\\flood_postman_test.mp4','2025-12-09 00:23:00'),(68,2,'data/uploads\\flood_postman_test.mp4','2025-12-09 00:23:00'),(69,6,'data/uploads\\flood_postman_test.mp4','2025-12-09 00:24:00'),(70,7,'data/uploads\\flood_postman_test.mp4','2025-12-09 00:24:00'),(71,1,'data/uploads\\flood_postman_test.mp4','2025-12-09 01:12:00'),(72,2,'data/uploads\\flood_postman_test.mp4','2025-12-09 01:12:00'),(73,6,'data/uploads\\flood_postman_test.mp4','2025-12-09 01:13:00'),(74,7,'data/uploads\\flood_postman_test.mp4','2025-12-09 01:13:00'),(75,1,'data/uploads\\flood_postman_test.mp4','2025-12-09 10:27:00'),(76,1,'data/uploads\\flood_postman_test.mp4','2025-12-09 10:35:00'),(77,2,'data/uploads\\flood_postman_test.mp4','2025-12-09 10:35:00'),(78,6,'data/uploads\\flood_postman_test.mp4','2025-12-09 10:35:00'),(79,7,'data/uploads\\flood_postman_test.mp4','2025-12-09 10:36:00');
/*!40000 ALTER TABLE `videos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'flood_system_db'
--

--
-- Dumping routines for database 'flood_system_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-09 15:08:06
