-- Criação inicial do banco de dados e tabelas básicas
CREATE DATABASE IF NOT EXISTS url_shortener;
USE url_shortener;

-- (Opcional) tabela inicial de teste
CREATE TABLE IF NOT EXISTS urls (
  id INT AUTO_INCREMENT PRIMARY KEY,
  original_url VARCHAR(500) NOT NULL,
  short_code VARCHAR(10) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
