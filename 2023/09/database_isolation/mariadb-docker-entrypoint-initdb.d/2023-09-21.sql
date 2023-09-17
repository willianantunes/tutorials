CREATE DATABASE IF NOT EXISTS `development` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE `development`;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
INSERT INTO `django_content_type` VALUES
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'auth','user'),
(5,'contenttypes','contenttype'),
(7,'core','account'),
(8,'core','transfer'),
(6,'sessions','session');
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add account',7,'add_account'),
(26,'Can change account',7,'change_account'),
(27,'Can delete account',7,'delete_account'),
(28,'Can view account',7,'view_account'),
(29,'Can add transfer',8,'add_transfer'),
(30,'Can change transfer',8,'change_transfer'),
(31,'Can delete transfer',8,'delete_transfer'),
(32,'Can view transfer',8,'view_transfer');
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
INSERT INTO `auth_user` VALUES
(1,'pbkdf2_sha256$600000$sf9NIllsSui9hmjcN7t6xR$rzVGsznm4sqzjLbOAG6V9yZYcHZam03IgsPP1N9nij8=','2023-09-22 00:21:08.661463',1,'admin','','','',1,1,'2023-09-22 00:20:55.111554');
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `core_account`
--

DROP TABLE IF EXISTS `core_account`;
CREATE TABLE `core_account` (
  `id` char(32) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `username` varchar(128) NOT NULL,
  `balance` decimal(10,4) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_account`
--

LOCK TABLES `core_account` WRITE;
/*!40000 ALTER TABLE `core_account` DISABLE KEYS */;
INSERT INTO `core_account` VALUES
('28f179b3d80f406f9297b45eafd82fdd','2023-09-22 00:20:55.386677','2023-09-22 00:20:55.386699','alyssa19',7000.0000),
('5188cebc7a144abbbd4e160e755fe992','2023-09-22 00:20:55.383975','2023-09-22 00:20:55.383992','thorntonnathan',5000.0000),
('5ab81c18145341c78b00ed19089f8445','2023-09-22 00:20:55.390079','2023-09-22 00:20:55.390100','martincaleb',9000.0000),
('5c1eadc16a574407b18e45ce62d576a6','2023-09-22 00:20:55.379299','2023-09-22 00:20:55.379321','davismary',2000.0000),
('8560c79ed9e440c68e9ec66401b2b931','2023-09-22 00:20:55.385359','2023-09-22 00:20:55.385376','stephenschristine',6000.0000),
('bad19496526b4cf3831ad4a8244eecf1','2023-09-22 00:20:55.377114','2023-09-22 00:20:55.377144','ysullivan',1000.0000),
('cd579443d51f423796c36f41dab3a42b','2023-09-22 00:20:55.388285','2023-09-22 00:20:55.388308','sbell',8000.0000),
('d1f25d2dd3f1443abefa4195db0bcd31','2023-09-22 00:20:55.382280','2023-09-22 00:20:55.382297','daviskatherine',4000.0000),
('d2c95cf730c147a0a7e2f12d06aedc8a','2023-09-22 00:20:55.391579','2023-09-22 00:20:55.391595','leecharlene',10000.0000),
('ef02dda2b0d442cc81b3ccee638d962f','2023-09-22 00:20:55.380703','2023-09-22 00:20:55.380722','lisa83',3000.0000);
UNLOCK TABLES;

--
-- Table structure for table `core_transfer`
--

DROP TABLE IF EXISTS `core_transfer`;
CREATE TABLE `core_transfer` (
  `id` char(32) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `amount` decimal(10,4) NOT NULL,
  `from_account_id` char(32) NOT NULL,
  `to_account_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_transfer_between_accounts` (`from_account_id`,`to_account_id`),
  KEY `core_transfer_to_account_id_8d5778e0_fk_core_account_id` (`to_account_id`),
  CONSTRAINT `core_transfer_from_account_id_662c7d12_fk_core_account_id` FOREIGN KEY (`from_account_id`) REFERENCES `core_account` (`id`),
  CONSTRAINT `core_transfer_to_account_id_8d5778e0_fk_core_account_id` FOREIGN KEY (`to_account_id`) REFERENCES `core_account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2023-09-22 00:20:54.302622'),
(2,'auth','0001_initial','2023-09-22 00:20:54.412391'),
(3,'admin','0001_initial','2023-09-22 00:20:54.457334'),
(4,'admin','0002_logentry_remove_auto_add','2023-09-22 00:20:54.463326'),
(5,'admin','0003_logentry_add_action_flag_choices','2023-09-22 00:20:54.468654'),
(6,'contenttypes','0002_remove_content_type_name','2023-09-22 00:20:54.493747'),
(7,'auth','0002_alter_permission_name_max_length','2023-09-22 00:20:54.509238'),
(8,'auth','0003_alter_user_email_max_length','2023-09-22 00:20:54.518941'),
(9,'auth','0004_alter_user_username_opts','2023-09-22 00:20:54.524481'),
(10,'auth','0005_alter_user_last_login_null','2023-09-22 00:20:54.540121'),
(11,'auth','0006_require_contenttypes_0002','2023-09-22 00:20:54.541331'),
(12,'auth','0007_alter_validators_add_error_messages','2023-09-22 00:20:54.547104'),
(13,'auth','0008_alter_user_username_max_length','2023-09-22 00:20:54.560418'),
(14,'auth','0009_alter_user_last_name_max_length','2023-09-22 00:20:54.570034'),
(15,'auth','0010_alter_group_name_max_length','2023-09-22 00:20:54.580089'),
(16,'auth','0011_update_proxy_permissions','2023-09-22 00:20:54.585858'),
(17,'auth','0012_alter_user_first_name_max_length','2023-09-22 00:20:54.594978'),
(18,'core','0001_initial','2023-09-22 00:20:54.630455'),
(19,'sessions','0001_initial','2023-09-22 00:20:54.641192');
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
INSERT INTO `django_session` VALUES
('388vg2kcvujx98hx5xgvimvad3a85nt5','.eJxVjDsOwjAQBe_iGln-fyjpcwZrvWtwANlSnFSIu0OkFNC-mXkvlmBba9pGWdJM7MwkO_1uGfBR2g7oDu3WOfa2LnPmu8IPOvjUqTwvh_t3UGHUb42agtTaRIcqkPDeoRXFRxIKkJQTytoo49UTGakLZDI2iugCgTFOevb-AMH_Nu0:1qjTuu:2yM0M7KEBee0GK5kXq4aOa9efPEORFWkI51o6SinjlU','2023-10-06 00:21:08.663326');
UNLOCK TABLES;
