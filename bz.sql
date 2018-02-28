/*
Navicat MySQL Data Transfer

Source Server         : MySQL
Source Server Version : 50719
Source Host           : localhost:3306
Source Database       : bz

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2017-12-07 13:27:59
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for department
-- ----------------------------
DROP TABLE IF EXISTS `department`;
CREATE TABLE `department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dwzd` varchar(255) DEFAULT NULL COMMENT '单位驻地',
  `dwbh` varchar(255) DEFAULT NULL COMMENT '单位编号',
  `dwmc` varchar(255) DEFAULT NULL COMMENT '单位名称',
  `qtmc` varchar(255) DEFAULT NULL COMMENT '其他名称',
  `ldzs` varchar(255) DEFAULT NULL COMMENT '领导职数',
  `jb` varchar(255) DEFAULT NULL COMMENT '级别',
  `nsjg` varchar(255) DEFAULT NULL COMMENT '内设机构',
  `xz_bzs` varchar(255) DEFAULT NULL COMMENT '行政编制数',
  `xz_sjs` varchar(255) DEFAULT NULL COMMENT '行政实际数',
  `sy_bzs` varchar(255) DEFAULT NULL COMMENT '事业编制数',
  `sy_sjs` varchar(255) DEFAULT NULL COMMENT '事业实际数',
  `gq_bzs` varchar(255) DEFAULT NULL COMMENT '工勤编制数',
  `gq_sjs` varchar(255) DEFAULT NULL COMMENT '工勤实际数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for person
-- ----------------------------
DROP TABLE IF EXISTS `person`;
CREATE TABLE `person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dwzd` varchar(255) DEFAULT NULL COMMENT '单位驻地',
  `dwbh` varchar(255) DEFAULT NULL COMMENT '单位编号',
  `dwmc` varchar(255) DEFAULT NULL COMMENT '单位名称',
  `ssbm` varchar(255) DEFAULT NULL COMMENT '所属部门',
  `ryxm` varchar(255) DEFAULT NULL COMMENT '人员姓名',
  `ryxb` varchar(255) DEFAULT NULL COMMENT '人员性别',
  `bzlx` varchar(255) DEFAULT NULL COMMENT '编制类型',
  `bzqk` varchar(255) DEFAULT NULL COMMENT '编制情况',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
