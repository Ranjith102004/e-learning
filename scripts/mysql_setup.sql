-- MySQL setup script for the project
-- Run as a privileged user (root) if creating the DB and user

-- Create database if missing
CREATE DATABASE IF NOT EXISTS `edutech_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- DROP the user if you want a fresh recreate (optional)
-- DROP USER IF EXISTS 'edutech_user'@'localhost';

-- Create (or ensure) the user and set password
CREATE USER IF NOT EXISTS 'edutech_user'@'localhost' IDENTIFIED BY 'strongpassword123';

-- Grant privileges
GRANT ALL PRIVILEGES ON `edutech_db`.* TO 'edutech_user'@'localhost';
FLUSH PRIVILEGES;

-- Notes:
-- 1) Replace 'strongpassword123' with a secure password you remember.
-- 2) Run: mysql -u root -p < scripts/mysql_setup.sql
