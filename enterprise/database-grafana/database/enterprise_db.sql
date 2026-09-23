/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.6-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: enterprise_db
-- ------------------------------------------------------
-- Server version	11.8.6-MariaDB-0+deb13u1 from Debian

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `backup_jobs`
--

DROP TABLE IF EXISTS `backup_jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `backup_jobs` (
  `job_name` varchar(120) DEFAULT NULL,
  `target_server` varchar(80) DEFAULT NULL,
  `backup_path` varchar(200) DEFAULT NULL,
  `last_status` varchar(50) DEFAULT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_jobs`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `backup_jobs` WRITE;
/*!40000 ALTER TABLE `backup_jobs` DISABLE KEYS */;
INSERT INTO `backup_jobs` VALUES
('grafana_config_backup','10.10.4.108','/srv/backups/grafana/','completed','Contains Grafana migration and dashboard notes.'),
('enterprise_inventory_backup','10.10.4.108','/srv/backups/db/','completed','Contains Level 4 asset inventory.'),
('idmz_access_migration','10.10.35.120','/srv/backups/idmz/','pending review','SRA migration is pending final validation.'),
('scada_readonly_session','10.10.3.10','/srv/backups/ot/','restricted','SCADA should only be accessed through jump server.');
/*!40000 ALTER TABLE `backup_jobs` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `flags`
--

DROP TABLE IF EXISTS `flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `flags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `flag_name` varchar(80) DEFAULT NULL,
  `flag_value` varchar(120) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flags`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `flags` WRITE;
/*!40000 ALTER TABLE `flags` DISABLE KEYS */;
INSERT INTO `flags` VALUES
(1,'flag_7','flag{enterprise_database_recon_complete}','Recovered from internal backup inventory database.');
/*!40000 ALTER TABLE `flags` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `network_assets`
--

DROP TABLE IF EXISTS `network_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `network_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(50) DEFAULT NULL,
  `ip_address` varchar(50) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `zone` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `network_assets`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `network_assets` WRITE;
/*!40000 ALTER TABLE `network_assets` DISABLE KEYS */;
INSERT INTO `network_assets` VALUES
(1,'l4-backup01','10.10.4.107','Backup Server','Stores migration notes and backup exports.','Level 4 - Enterprise'),
(2,'l4-grafana-db01','10.10.4.108','DB / Grafana Server','Internal monitoring and backup inventory system.','Level 4 - Enterprise'),
(3,'sra-gateway','10.10.35.120','Jump servers','Access to OT assets must be performed through this gateway.','Level 3.5 - IDMZ'),
(4,'scada-ops','10.10.3.10','SCADA Operations Server','Reachable only through approved SRA sessions.','Level 3 - Operations'),
(5,'io-server','10.10.3.20','I/O Server','Collects data from lower-level control systems.','Level 3 - Operations');
/*!40000 ALTER TABLE `network_assets` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `remote_access_notes`
--

DROP TABLE IF EXISTS `remote_access_notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `remote_access_notes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_name` varchar(100) DEFAULT NULL,
  `access_method` varchar(100) DEFAULT NULL,
  `target` varchar(50) DEFAULT NULL,
  `allowed_from` varchar(100) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `remote_access_notes`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `remote_access_notes` WRITE;
/*!40000 ALTER TABLE `remote_access_notes` DISABLE KEYS */;
INSERT INTO `remote_access_notes` VALUES
(1,'SRA Gateway','HTTPS','10.10.35.120:443','Level 4 Enterprise Workstations','Enterprise users must authenticate through the SRA portal.'),
(2,'Grafana Monitoring','HTTP','10.10.4.108:3000','Level 4 Enterprise','Temporary admin account still active.'),
(3,'SCADA Operations','jump server Session','10.10.3.10','jump server only','Direct access from Enterprise is blocked.'),
(4,'I/O Server','SRA Session','10.10.3.20','jump server only','Used for plant data collection.');
/*!40000 ALTER TABLE `remote_access_notes` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `service_accounts`
--

DROP TABLE IF EXISTS `service_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service` varchar(50) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password_hint` varchar(100) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_accounts`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `service_accounts` WRITE;
/*!40000 ALTER TABLE `service_accounts` DISABLE KEYS */;
INSERT INTO `service_accounts` VALUES
(1,'grafana','admin','default credentials were not rotated','Temporary Grafana admin account created during migration.'),
(2,'mariadb','backup_reader','stored in backup migration notes','Read-only account for backup inventory review.'),
(3,'sra','plant_maintenance','check Grafana IDMZ migration dashboard','Maintenance account used for remote OT access.'),
(4,'scada','operator_view','managed through jump server sessions only','Direct Enterprise access should be blocked.');
/*!40000 ALTER TABLE `service_accounts` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Dumping events for database 'enterprise_db'
--

--
-- Dumping routines for database 'enterprise_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-09-23 17:12:40
