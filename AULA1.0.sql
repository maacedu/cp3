
-- ==========================================
-- EXERCICIO 1.1
-- MODELAGEM DE BANCO DE VULNERABILIDADES
-- ==========================================

CREATE DATABASE IF NOT EXISTS banco_vulnerabilidades;

USE banco_vulnerabilidades;

-- TABELA DE ATIVOS
CREATE TABLE ativos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ip VARCHAR(45) NOT NULL,
    tipo VARCHAR(50),
    criticidade ENUM('baixa', 'media', 'alta', 'critica')
);

-- TABELA DE VULNERABILIDADES
CREATE TABLE vulnerabilidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cve_id VARCHAR(30) NOT NULL UNIQUE,
    descricao TEXT,
    severidade ENUM('baixa', 'media', 'alta', 'critica'),
    cvss DECIMAL(3,1)
);

-- TABELA DE RELACIONAMENTO
CREATE TABLE ativo_vulnerabilidade (
    ativo_id INT,
    vuln_id INT,
    status VARCHAR(20) DEFAULT 'aberta',
    detectada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (ativo_id, vuln_id),

    FOREIGN KEY (ativo_id) REFERENCES ativos(id),
    FOREIGN KEY (vuln_id) REFERENCES vulnerabilidades(id)
);

-- INSERINDO ATIVO
INSERT INTO ativos (nome, ip, tipo, criticidade)
VALUES ('SRV-WEB01', '192.168.1.10', 'Servidor Web', 'alta');

-- INSERINDO VULNERABILIDADE
INSERT INTO vulnerabilidades
(cve_id, descricao, severidade, cvss)
VALUES
('CVE-2024-001', 'Vulnerabilidade de teste', 'alta', 8.5);

-- RELACIONANDO ATIVO E VULNERABILIDADE
INSERT INTO ativo_vulnerabilidade (ativo_id, vuln_id)
VALUES (1, 1);

-- CONSULTANDO RESULTADOS
SELECT * FROM ativos;

SELECT * FROM vulnerabilidades;

SELECT * FROM ativo_vulnerabilidade;
