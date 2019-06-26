-- MySQL Script generated by MySQL Workbench
-- Tue 25 Jun 2019 05:49:28 PM CEST
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema chainrace
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema chainrace
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `chainrace` DEFAULT CHARACTER SET utf8 ;
USE `chainrace` ;

-- -----------------------------------------------------
-- Table `chainrace`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chainrace`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ids` VARCHAR(128) NOT NULL,
  `username` VARCHAR(64) NOT NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(32) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `chainrace`.`model`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chainrace`.`model` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `path` TEXT NOT NULL,
  `stat_end_time` FLOAT NOT NULL COMMENT 'AWS stat',
  `stat_percentage` FLOAT NOT NULL COMMENT 'AWS stats ',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chainrace`.`vehicule`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chainrace`.`vehicule` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ids` VARCHAR(128) NOT NULL,
  `pac` VARCHAR(128) NOT NULL COMMENT 'Password entered in the Raspberry chip so the car can communicate with the server endpoint.',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chainrace`.`user_has_vehicule`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chainrace`.`user_has_vehicule` (
  `user_id` INT NOT NULL,
  `vehicule_id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `vehicule_id`),
  INDEX `fk_user_has_vehicule_vehicule1_idx` (`vehicule_id` ASC),
  INDEX `fk_user_has_vehicule_user_idx` (`user_id` ASC));


-- -----------------------------------------------------
-- Table `chainrace`.`model_update`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chainrace`.`model_update` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(2) NOT NULL COMMENT 'AW = awaiting\nOK = updated\nKO = failed',
  `user_id` INT NOT NULL,
  `vehicule_id` INT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `model_id` INT NOT NULL,
  PRIMARY KEY (`id`, `user_id`, `vehicule_id`, `model_id`),
  INDEX `fk_model_update_user_has_vehicule1_idx` (`user_id` ASC, `vehicule_id` ASC),
  INDEX `fk_model_update_model1_idx` (`model_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chainrace`.`model_add`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chainrace`.`model_add` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  `model_id` INT NOT NULL,
  PRIMARY KEY (`id`, `user_id`, `model_id`),
  INDEX `fk_model_add_user1_idx` (`user_id` ASC),
  INDEX `fk_model_add_model1_idx` (`model_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chainrace`.`contest`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chainrace`.`contest` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ids` VARCHAR(128) NOT NULL,
  `name` VARCHAR(128) NULL,
  `starts_at` TIMESTAMP NOT NULL,
  `ends_at` TIMESTAMP NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chainrace`.`race`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chainrace`.`race` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `contest_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `vehicule_id` INT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`, `contest_id`, `user_id`, `vehicule_id`),
  INDEX `fk_race_contest1_idx` (`contest_id` ASC),
  INDEX `fk_race_user_has_vehicule1_idx` (`user_id` ASC, `vehicule_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chainrace`.`user_has_contest`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chainrace`.`user_has_contest` (
  `user_id` INT NOT NULL,
  `contest_id` INT NOT NULL,
  `type` VARCHAR(2) NOT NULL COMMENT 'JO = joined\nCR = created',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `contest_id`),
  INDEX `fk_user_has_contest_contest1_idx` (`contest_id` ASC),
  INDEX `fk_user_has_contest_user1_idx` (`user_id` ASC));


-- -----------------------------------------------------
-- Table `chainrace`.`stats`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chainrace`.`stats` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL COMMENT 'started_at, ended_at, stopped_at',
  `value` INT NOT NULL,
  `race_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_stats_race1_idx` (`race_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chainrace`.`wallet`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chainrace`.`wallet` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `public_key` TEXT NOT NULL,
  `address` TEXT NOT NULL,
  `passphrase` TEXT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chainrace`.`user_has_wallet`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chainrace`.`user_has_wallet` (
  `user_id` INT NOT NULL,
  `wallet_id` INT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `wallet_id`),
  INDEX `fk_user_has_wallet_wallet1_idx` (`wallet_id` ASC),
  INDEX `fk_user_has_wallet_user1_idx` (`user_id` ASC));


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;