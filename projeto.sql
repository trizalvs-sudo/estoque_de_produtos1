-- --------------------------------------------------------
-- TABELA 1: produto (Catálogo e Estoque Principal)
-- Inclui o campo 'custo' que usamos para lucro bruto.
-- --------------------------------------------------------
CREATE TABLE produto (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome_produto VARCHAR(255) NOT NULL UNIQUE,
    valor_produto DECIMAL(10, 2) NOT NULL,
    quantidade DECIMAL(10, 2) NOT NULL DEFAULT 0.00, 
    custo DECIMAL(10, 2) NOT NULL DEFAULT 0.00,       
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------
-- TABELA 2: producao (Ingredientes/Matérias-Primas)
-- Tabela independente para gerenciar o custo das matérias-primas.
-- --------------------------------------------------------
CREATE TABLE producao (
    id_producao INT AUTO_INCREMENT PRIMARY KEY,
    nome_ingrediente VARCHAR(255) NOT NULL,
    unidade_medida VARCHAR(10) NOT NULL,
    custo_unitario DECIMAL(10, 2) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------
-- TABELA 3: registro_vendas (Vendas Realizadas)
-- Armazena o registro de vendas, com chave estrangeira para 'produto'.
-- --------------------------------------------------------
CREATE TABLE registro_vendas (
    id_venda INT AUTO_INCREMENT PRIMARY KEY,
    id_produto INT NOT NULL,
    data_venda DATE NOT NULL,
    quantidade_vendida DECIMAL(10, 2) NOT NULL,
    valor_venda_unitario DECIMAL(10, 2) NOT NULL,
    custo_venda_unitario DECIMAL(10, 2) NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);