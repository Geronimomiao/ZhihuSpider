/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50724
 Source Host           : localhost:3306
 Source Schema         : article_spider

 Target Server Type    : MySQL
 Target Server Version : 50724
 File Encoding         : 65001

 Date: 08/01/2019 17:52:19
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for zhihu_question
-- ----------------------------
DROP TABLE IF EXISTS `zhihu_question`;
CREATE TABLE `zhihu_question` (
  `zhihu_question_id` bigint(20) NOT NULL,
  `title` varchar(200) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `url` varchar(300) DEFAULT NULL,
  `crawl_time` datetime DEFAULT NULL,
  `crawl_update_time` datetime DEFAULT NULL,
  `answer_nums` varchar(40) DEFAULT NULL,
  `topics` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`zhihu_question_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
