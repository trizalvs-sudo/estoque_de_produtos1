-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema estoque_produtos
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema estoque_produtos
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `estoque_produtos` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `estoque_produtos` ;

-- -----------------------------------------------------
-- Table `estoque_produtos`.`producao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `estoque_produtos`.`producao` (
  `id_producao` INT NOT NULL AUTO_INCREMENT,
  `nome_ingrediente` VARCHAR(255) NOT NULL,
  `unidade_medida` VARCHAR(10) NOT NULL,
  `custo_unitario` DECIMAL(10,2) NOT NULL,
  `data_cadastro` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `ativo` TINYINT(1) NULL DEFAULT '1',
  `estoque_atual` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `estoque_minimo` INT NOT NULL DEFAULT '5',
  PRIMARY KEY (`id_producao`))
ENGINE = InnoDB
AUTO_INCREMENT = 18
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `estoque_produtos`.`movimentos_estoque`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `estoque_produtos`.`movimentos_estoque` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_producao` INT NOT NULL,
  `tipo_movimento` ENUM('entrada', 'saida') NOT NULL,
  `quantidade` DECIMAL(10,2) NOT NULL,
  `data_movimento` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `custo_unitario` DECIMAL(10,2) NULL DEFAULT NULL,
  `observacao` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `id_producao` (`id_producao` ASC) VISIBLE,
  CONSTRAINT `movimentos_estoque_ibfk_1`
    FOREIGN KEY (`id_producao`)
    REFERENCES `estoque_produtos`.`producao` (`id_producao`))
ENGINE = InnoDB
AUTO_INCREMENT = 17
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `estoque_produtos`.`produto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `estoque_produtos`.`produto` (
  `id_produto` INT NOT NULL AUTO_INCREMENT,
  `nome_produto` VARCHAR(255) NOT NULL,
  `valor_produto` DECIMAL(10,2) NOT NULL,
  `quantidade` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `custo` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `data_cadastro` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `ativo` TINYINT(1) NULL DEFAULT '1',
  `categoria` VARCHAR(50) NULL DEFAULT 'Sem categoria',
  PRIMARY KEY (`id_produto`),
  UNIQUE INDEX `nome_produto` (`nome_produto` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 23
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `estoque_produtos`.`movimentos_produtos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `estoque_produtos`.`movimentos_produtos` (
  `id_movimento` INT NOT NULL AUTO_INCREMENT,
  `id_produto` INT NOT NULL,
  `tipo_movimento` ENUM('entrada', 'saida', 'venda') NOT NULL,
  `quantidade` DECIMAL(10,2) NOT NULL,
  `valor_unitario` DECIMAL(10,2) NULL DEFAULT NULL,
  `data_movimento` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `origem_movimento` ENUM('venda', 'baixa') NOT NULL DEFAULT 'venda',
  PRIMARY KEY (`id_movimento`),
  INDEX `id_produto` (`id_produto` ASC) VISIBLE,
  CONSTRAINT `movimentos_produtos_ibfk_1`
    FOREIGN KEY (`id_produto`)
    REFERENCES `estoque_produtos`.`produto` (`id_produto`))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `estoque_produtos`.`registro_vendas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `estoque_produtos`.`registro_vendas` (
  `id_venda` INT NOT NULL AUTO_INCREMENT,
  `id_produto` INT NOT NULL,
  `data_venda` DATE NOT NULL,
  `quantidade_vendida` DECIMAL(10,2) NOT NULL,
  `valor_venda_unitario` DECIMAL(10,2) NOT NULL,
  `valor_total` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_venda`),
  INDEX `id_produto` (`id_produto` ASC) VISIBLE,
  CONSTRAINT `registro_vendas_ibfk_1`
    FOREIGN KEY (`id_produto`)
    REFERENCES `estoque_produtos`.`produto` (`id_produto`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 22
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

INSERT INTO produto (nome_produto, categoria, quantidade, valor_produto, ativo) VALUES ('Mousse Chocolate', 'Mousses', 50, 8.0, 1);
INSERT INTO produto (nome_produto, categoria, quantidade, valor_produto, ativo) VALUES ('Mousse Morango', 'Mousses', 50, 8.0, 1);
INSERT INTO produto (nome_produto, categoria, quantidade, valor_produto, ativo) VALUES ('Mousse Maracujá', 'Mousses', 50, 8.0, 1);
INSERT INTO produto (nome_produto, categoria, quantidade, valor_produto, ativo) VALUES ('Mousse Limão', 'Mousses', 50, 8.0, 1);
INSERT INTO produto (nome_produto, categoria, quantidade, valor_produto, ativo) VALUES ('Pudim Leite Condensado', 'Sobremesas Geladas', 40, 5.5, 1);
INSERT INTO produto (nome_produto, categoria, quantidade, valor_produto, ativo) VALUES ('Pudim Chocolate', 'Sobremesas Geladas', 40, 5.5, 1);
INSERT INTO produto (nome_produto, categoria, quantidade, valor_produto, ativo) VALUES ('Pudim Coco', 'Sobremesas Geladas', 40, 5.5, 1);
INSERT INTO produto (nome_produto, categoria, quantidade, valor_produto, ativo) VALUES ('Pudim Caramelo', 'Sobremesas Geladas', 40, 5.5, 1);
INSERT INTO produto (nome_produto, categoria, quantidade, valor_produto, ativo) VALUES ('Bolo no Pote Chocolate', 'Bolos no pote', 30, 10.0, 1);
INSERT INTO produto (nome_produto, categoria, quantidade, valor_produto, ativo) VALUES ('Bolo no Pote Morango', 'Bolos no pote', 30, 10.0, 1);
INSERT INTO produto (nome_produto, categoria, quantidade, valor_produto, ativo) VALUES ('Bolo no Pote Doce de Leite', 'Bolos no pote', 30, 10.0, 1);
INSERT INTO produto (nome_produto, categoria, quantidade, valor_produto, ativo) VALUES ('Bolo no Pote Brigadeiro', 'Bolos no pote', 30, 10.0, 1);


INSERT INTO producao (id_producao, nome_ingrediente, unidade_medida, custo_unitario, data_cadastro, ativo, estoque_atual, estoque_minimo) VALUES
(5, 'morango', 'KG', 15.00, '2025-11-16 19:29:02', 1, 4.00, 5),
(6, 'açucar', 'KG', 4.00, '2025-11-16 19:29:43', 1, 5.00, 5),
(7, 'Chocolate em pó', 'KG', 20.00, '2025-11-16 19:30:08', 1, 3.00, 5),
(8, 'Leite condensado', 'UN', 7.00, '2025-11-16 19:30:54', 1, 10.00, 5),
(9, 'Creme de Leite', 'UN', 6.00, '2025-11-16 19:31:19', 1, 6.00, 5),
(10, 'Maracujá', 'UN', 2.50, '2025-11-16 19:32:24', 1, 20.00, 5),
(11, 'Limão', 'UN', 1.50, '2025-11-16 19:32:48', 1, 20.00, 5),
(12, 'Leite', 'LT', 4.00, '2025-11-16 19:33:11', 1, 8.00, 5),
(13, 'Gelatina', 'UN', 3.00, '2025-11-16 19:34:07', 1, 10.00, 5),
(14, 'Doce de Leite', 'UN', 13.00, '2025-11-16 19:34:26', 1, 5.00, 5),
(15, 'Chocolate granulado', 'UN', 8.00, '2025-11-16 19:34:54', 1, 5.00, 5),
(16, 'Amora', 'UN', 5.00, '2025-11-16 19:36:15', 1, 10.00, 5),
(17, 'Corante alimentício', 'UN', 7.00, '2025-11-16 19:37:04', 1, 100.00, 5);