-- Criação inicial do banco de dados e tabelas básicas
CREATE DATABASE IF NOT EXISTS url_shortener;
USE url_shortener;

-- Tabela para URLs encurtadas
CREATE TABLE IF NOT EXISTS urls (
  id INT AUTO_INCREMENT PRIMARY KEY,
  original_url VARCHAR(500) NOT NULL,
  short_code VARCHAR(10) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para Usuários (para JWT)
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL
  email VARCHAR(255) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);