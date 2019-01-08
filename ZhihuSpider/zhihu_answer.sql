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

 Date: 08/01/2019 17:51:57
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for zhihu_answer
-- ----------------------------
DROP TABLE IF EXISTS `zhihu_answer`;
CREATE TABLE `zhihu_answer` (
  `zhihu_answer_id` bigint(20) NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `author_token` varchar(255) DEFAULT NULL,
  `voteup_count` varchar(255) DEFAULT NULL,
  `content` longtext,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `crawl_time` datetime DEFAULT NULL,
  `crawl_update_time` datetime DEFAULT NULL,
  `zhihu_question_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`zhihu_answer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
