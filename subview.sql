/*
Navicat MySQL Data Transfer

Source Server         : 192.168.4.9
Source Server Version : 50638
Source Host           : 192.168.4.9:3306
Source Database       : subview

Target Server Type    : MYSQL
Target Server Version : 50638
File Encoding         : 65001

Date: 2018-03-30 17:59:51
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for actionlog
-- ----------------------------
DROP TABLE IF EXISTS `actionlog`;
CREATE TABLE `actionlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `reason` varchar(600) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_actionlog_create_time` (`create_time`),
  KEY `ix_actionlog_update_time` (`update_time`),
  CONSTRAINT `actionlog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of actionlog
-- ----------------------------

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `role_id` (`role_id`),
  KEY `ix_admin_create_time` (`create_time`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('1', 'BluePay', 'pbkdf2:sha256:50000$uexmBXk8$f5d5e842cda8564c6a47ee12405c85c549b45c899c2057e6b0344568ad7e1e79', '1', '2018-03-15 17:10:05');
INSERT INTO `admin` VALUES ('2', 'Blue', 'pbkdf2:sha256:50000$Q1PfCIux$b3274efe75097d006a8271bc074c683a74f73001a1aba265f9b783a3bb83ef4a', '1', '2018-03-28 17:16:28');
INSERT INTO `admin` VALUES ('3', 'copy.chen', 'pbkdf2:sha256:50000$UNOwhNrD$c9b6da4e4f0800b5370d1f1b958e3a0be86b0c4a98a0ba7d923b2808da3444c6', '1', '2018-03-28 17:17:54');
INSERT INTO `admin` VALUES ('4', 'anter', 'pbkdf2:sha256:50000$rxwIA197$ea3b4a366a231845cbf9ac3793f0d38cfc037564296b11e9e95e03763f86a47d', '1', '2018-03-28 17:18:52');
INSERT INTO `admin` VALUES ('9', 'alvin', 'pbkdf2:sha256:50000$Ho2nkb0C$bc9392827c23ca349d66f38ab0c409ebf5b47ea6674d102f5fd89a2b10e9ef76', '1', '2018-03-28 17:26:24');
INSERT INTO `admin` VALUES ('11', 'kun', 'pbkdf2:sha256:50000$jx3qbufq$a9b375d75bf83867b09b6fab98310ae6c244930b1b51accc3a4856c1b2ae85c3', '1', '2018-03-28 17:26:55');
INSERT INTO `admin` VALUES ('12', 'yong', 'pbkdf2:sha256:50000$ywynMuzK$153b7a0018ad03d537086a64194e50f023ec83051afe485a2de2877d49128d1b', '1', '2018-03-28 17:27:31');
INSERT INTO `admin` VALUES ('13', 'angela', 'pbkdf2:sha256:50000$yP6V0YZl$3f0fd8b6ecad024feb9033d4e3c1db44ea28097f70131eb49227e85df505a7b9', '1', '2018-03-28 17:27:47');
INSERT INTO `admin` VALUES ('14', 'wang', 'pbkdf2:sha256:50000$t5WG0J2e$00985327978ba918f65e115b0cd955e44ae71db7721575bfd55a32fe90408f30', '1', '2018-03-28 17:27:58');
INSERT INTO `admin` VALUES ('15', 'renyu', 'pbkdf2:sha256:50000$Nmw2ZL8X$2c02f42a9efc3f16054f92847158ccbba922fa8f31ff48c3ed9209e0447b0396', '1', '2018-03-28 17:29:47');
INSERT INTO `admin` VALUES ('16', 'local2', 'pbkdf2:sha256:50000$aFfL8ITe$ca9b383f4818d2a4ee55568a2330af6473fc1fab42cc0898dbb3b2eada881198', '2', '2018-03-28 17:30:20');

-- ----------------------------
-- Table structure for adminlog
-- ----------------------------
DROP TABLE IF EXISTS `adminlog`;
CREATE TABLE `adminlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_adminlog_create_time` (`create_time`),
  KEY `ix_adminlog_update_time` (`update_time`),
  CONSTRAINT `adminlog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of adminlog
-- ----------------------------
INSERT INTO `adminlog` VALUES ('1', '1', '127.0.0.1', '2018-03-15 18:52:57', '2018-03-15 18:52:57');
INSERT INTO `adminlog` VALUES ('2', '1', '127.0.0.1', '2018-03-15 20:01:00', '2018-03-15 20:01:00');
INSERT INTO `adminlog` VALUES ('3', '1', '127.0.0.1', '2018-03-15 20:07:41', '2018-03-15 20:07:41');
INSERT INTO `adminlog` VALUES ('4', '1', '127.0.0.1', '2018-03-19 11:34:39', '2018-03-19 11:34:39');
INSERT INTO `adminlog` VALUES ('5', '1', '127.0.0.1', '2018-03-19 11:34:48', '2018-03-19 11:34:48');
INSERT INTO `adminlog` VALUES ('6', '1', '127.0.0.1', '2018-03-19 11:35:21', '2018-03-19 11:35:21');
INSERT INTO `adminlog` VALUES ('7', '1', '127.0.0.1', '2018-03-19 11:35:49', '2018-03-19 11:35:49');
INSERT INTO `adminlog` VALUES ('8', '1', '127.0.0.1', '2018-03-19 11:36:39', '2018-03-19 11:36:39');
INSERT INTO `adminlog` VALUES ('9', '1', '127.0.0.1', '2018-03-19 11:37:49', '2018-03-19 11:37:49');
INSERT INTO `adminlog` VALUES ('10', '1', '127.0.0.1', '2018-03-19 11:41:02', '2018-03-19 11:41:02');
INSERT INTO `adminlog` VALUES ('11', '1', '127.0.0.1', '2018-03-22 14:15:43', '2018-03-22 14:15:43');
INSERT INTO `adminlog` VALUES ('12', '1', '127.0.0.1', '2018-03-23 10:00:05', '2018-03-23 10:00:05');
INSERT INTO `adminlog` VALUES ('13', '1', '127.0.0.1', '2018-03-28 15:09:51', '2018-03-28 15:09:51');
INSERT INTO `adminlog` VALUES ('14', '1', '127.0.0.1', '2018-03-28 19:04:17', '2018-03-28 19:04:17');
INSERT INTO `adminlog` VALUES ('15', '1', '127.0.0.1', '2018-03-29 09:03:29', '2018-03-29 09:03:29');
INSERT INTO `adminlog` VALUES ('16', '1', '127.0.0.1', '2018-03-29 11:44:59', '2018-03-29 11:44:59');
INSERT INTO `adminlog` VALUES ('17', '1', '127.0.0.1', '2018-03-29 11:47:17', '2018-03-29 11:47:17');
INSERT INTO `adminlog` VALUES ('18', '1', '127.0.0.1', '2018-03-29 11:47:46', '2018-03-29 11:47:46');

-- ----------------------------
-- Table structure for auth
-- ----------------------------
DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  KEY `ix_auth_update_time` (`update_time`),
  KEY `ix_auth_create_time` (`create_time`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth
-- ----------------------------
INSERT INTO `auth` VALUES ('1', '汇总流水', '/', '2018-03-28 19:04:52', '2018-03-28 19:04:52');
INSERT INTO `auth` VALUES ('2', '按天流水', '/day/', '2018-03-28 19:12:33', '2018-03-28 19:12:33');
INSERT INTO `auth` VALUES ('3', ' 获取当天数据', '/get_day_data/', '2018-03-28 19:12:52', '2018-03-28 19:12:52');
INSERT INTO `auth` VALUES ('4', '重点流水', '/charge/', '2018-03-28 19:13:14', '2018-03-28 19:13:14');
INSERT INTO `auth` VALUES ('5', '定时任务日志', '/jobs/', '2018-03-28 19:13:37', '2018-03-28 19:13:37');
INSERT INTO `auth` VALUES ('6', 'ES查询', '/elastics/', '2018-03-28 19:13:51', '2018-03-28 19:13:51');
INSERT INTO `auth` VALUES ('7', '调整收入', '/adjust/', '2018-03-28 19:14:09', '2018-03-28 19:14:09');
INSERT INTO `auth` VALUES ('8', '获取调整收入数据', '/get_adjust_data/', '2018-03-28 19:14:30', '2018-03-28 19:14:30');
INSERT INTO `auth` VALUES ('9', '管理员列表', '/admin/list/<int:page>/', '2018-03-28 19:14:54', '2018-03-28 19:22:49');
INSERT INTO `auth` VALUES ('10', '添加管理员', '/admin/add/', '2018-03-28 19:15:05', '2018-03-28 19:22:32');
INSERT INTO `auth` VALUES ('11', '编辑管理员', '/admin/edit/<int:id>/', '2018-03-28 19:15:23', '2018-03-28 19:15:23');
INSERT INTO `auth` VALUES ('12', '权限添加', '/auth/add/', '2018-03-28 19:15:37', '2018-03-28 19:15:37');
INSERT INTO `auth` VALUES ('13', '权限列表', '/auth/list/<int:page>/', '2018-03-28 19:15:50', '2018-03-28 19:15:50');
INSERT INTO `auth` VALUES ('16', '角色管理', '/role/list/<int:page>/', '2018-03-28 20:21:49', '2018-03-28 20:21:49');
INSERT INTO `auth` VALUES ('18', '角色添加', '/role/add/', '2018-03-28 20:23:47', '2018-03-28 20:23:47');
INSERT INTO `auth` VALUES ('19', '角色编辑', '/role/edit/<int:id>/', '2018-03-28 20:24:12', '2018-03-28 20:24:12');
INSERT INTO `auth` VALUES ('20', '角色删除', '/role/del/<int:id>/', '2018-03-28 20:25:30', '2018-03-28 20:25:30');
INSERT INTO `auth` VALUES ('21', '权限编辑', '/auth/edit/<int:id>/', '2018-03-28 20:27:39', '2018-03-28 20:27:39');

-- ----------------------------
-- Table structure for backup_log
-- ----------------------------
DROP TABLE IF EXISTS `backup_log`;
CREATE TABLE `backup_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `backup_time` varchar(64) NOT NULL COMMENT '备份时间',
  `func_name` varchar(64) NOT NULL COMMENT '函数名称',
  `used_time` varchar(64) NOT NULL COMMENT '使用时间',
  `cdr_file_max_time` varchar(64) NOT NULL DEFAULT '0' COMMENT '备份最大时间点',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of backup_log
-- ----------------------------

-- ----------------------------
-- Table structure for bluecoins_log
-- ----------------------------
DROP TABLE IF EXISTS `bluecoins_log`;
CREATE TABLE `bluecoins_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `data` varchar(200) NOT NULL COMMENT '请求参数',
  `url` varchar(200) NOT NULL COMMENT '执行URL',
  `name` varchar(200) NOT NULL COMMENT '使用时间',
  `result` varchar(200) NOT NULL DEFAULT '' COMMENT '响应结果',
  `filename` varchar(180) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of bluecoins_log
-- ----------------------------
INSERT INTO `bluecoins_log` VALUES ('1', 'cardType=1&channel=0&transactionId=bestbMRdhxhEdqac&customerId=66qem5Qu&producerId=1&currency=THB&amount=50&cardNote=bestbMRdhxhEdqac66qem5Qu&validity=360', '6434a05569def092b2286cee7c475b14', 'BluePay', 'cardNo:6437937526832855 | 50', 'F:\\PycharmProjects\\subview\\app\\static/bluecoins/2018033017_50.txt', '2018-03-30 17:53:57', '2018-03-30 17:53:57');
INSERT INTO `bluecoins_log` VALUES ('2', 'cardType=1&channel=0&transactionId=bestzd1APPG9bqFv&customerId=668HHhGM&producerId=1&currency=THB&amount=50&cardNote=bestzd1APPG9bqFv668HHhGM&validity=360', '75bbdf73b96ca62d831b400a5c0174b6', 'BluePay', 'cardNo:6437937526832855 | 50', 'F:\\PycharmProjects\\subview\\app\\static/bluecoins/2018033017_50.txt', '2018-03-30 17:53:58', '2018-03-30 17:53:58');

-- ----------------------------
-- Table structure for cdr_file_hour
-- ----------------------------
DROP TABLE IF EXISTS `cdr_file_hour`;
CREATE TABLE `cdr_file_hour` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hour_time` varchar(16) NOT NULL,
  `amount` varchar(32) NOT NULL,
  `actiontype` varchar(5) NOT NULL,
  `producer_id` varchar(12) NOT NULL,
  `currency` varchar(5) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `numbers` varchar(12) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of cdr_file_hour
-- ----------------------------

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `auths` varchar(600) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_role_create_time` (`create_time`),
  KEY `ix_role_update_time` (`update_time`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('1', '超级管理员', '1,2,3,4,5,6,7,8,9,10,11,12,13,16,18,19,20,21', '2018-03-15 17:10:05', '2018-03-28 20:28:34');
INSERT INTO `role` VALUES ('2', 'ES 管理员', '6', '2018-03-28 19:55:25', '2018-03-28 19:55:25');
