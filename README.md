D'Mousse — Sistema de Vendas e Controle de Estoque

D'Mousse é um sistema web desenvolvido como trabalho acadêmico, simulando um site de vendas de doces em potes com controle completo de produtos, estoque, movimentações além de interface moderna utilizando Flask e Bootstrap.

**Tecnologias Utilizadas**

- Python 3 + Flask
- HTML5 / CSS3
- Bootstrap 5
- JavaScript
- MySQL

Instalação e Execução do Projeto:

**1 - Clone o repositório**
git clone https://github.com/Samuel-Anjos/estoque_de_produtos.git

**2 - Crie o ambiente virtual**

python -m venv venv
venv\Scripts\activate

**3 - Instale as dependências**
pip install -r requirements.txt

**4 - Configure o arquivo .env**

Crie um arquivo chamado .env na raiz do projeto e adicione:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=SUA_SENHA
DB_NAME=SEU_BANCO
DB_PORT=3306


**5 - Configure o banco de dados**

Abra seu MySQL Workbench ou similar
Crie um banco com o nome definido no .env

Importe o arquivo:
projeto.sql

**6 - teste o programa**
rode e teste

O site é bem intuitívo, pode servir para futuras expansões quem sabe ♥️

**Autores:**

- Samuel Silva dos Anjos
- Beatriz Alves de Sousa
- Davi Silva Freire
- Enzo Danilo dos Santos Ribeiro
- Guilherme Brito da Silva
