
-- ==========================================
-- EXERCICIO 1.2
-- CRUD SQL COMPLETO
-- ==========================================

CREATE DATABASE IF NOT EXISTS banco_alertas;

USE banco_alertas;

-- CRIANDO TABELA
CREATE TABLE alertas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50),
    ip_origem VARCHAR(45),
    severidade ENUM('baixa','media','alta','critica'),
    status VARCHAR(20) DEFAULT 'aberto',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- A) INSERINDO 4 ALERTAS
INSERT INTO alertas (tipo, ip_origem, severidade)
VALUES
('Ataque DDoS', '192.168.1.20', 'critica'),
('Tentativa de invasao', '192.168.1.30', 'alta'),
('Acesso suspeito', '192.168.1.40', 'alta'),
('Varredura de portas', '192.168.1.50', 'media');

-- B) LISTANDO ALERTAS DE SEVERIDADE ALTA
SELECT *
FROM alertas
WHERE severidade = 'alta';

-- C) ATUALIZANDO ALERTA PARA RESOLVIDO
UPDATE alertas
SET status = 'resolvido'
WHERE id = 1;

-- D) CONTANDO ALERTAS POR SEVERIDADE
SELECT severidade, COUNT(*) AS total
FROM alertas
GROUP BY severidade;

-- E) APAGANDO ALERTAS COM MAIS DE 90 DIAS
DELETE FROM alertas
WHERE criado_em < NOW() - INTERVAL 90 DAY;

-- CONFERINDO RESULTADOS
SELECT * FROM alertas;
