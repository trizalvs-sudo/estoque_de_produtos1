from flask import render_template, request, redirect, url_for
from main import app, get_connection
from datetime import datetime
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


@app.route("/")
def home():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM produto ORDER BY ativo DESC, id_produto")
        produtos = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS total FROM produto")
        total = cursor.fetchone()
        total_produtos = total["total"] if total else 0

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM movimentos_produtos 
            WHERE origem_movimento = 'venda'
        """)
        total = cursor.fetchone()
        total_vendas = total["total"] if total else 0

        cursor.execute("""
            SELECT COALESCE(SUM(quantidade * COALESCE(valor_unitario, 0)), 0) AS receita
            FROM movimentos_produtos
            WHERE origem_movimento = 'venda'
        """)
        total = cursor.fetchone()
        receita_total = total["receita"] if total else 0

        
    conn.close()
    return render_template(
        'index.html', produtos=produtos, 
        total_produtos=total_produtos,
        total_vendas=total_vendas,
        receita_total=receita_total)


@app.route("/produtos", methods=["GET", "POST"])
def produtos():
    conn = get_connection()
    if request.method == "POST":
        nome_produto = request.form.get("nomeProduto")
        quantidade = request.form.get("quantidade")
        valor_unitario = request.form.get("valorUnitario")
        categoria = request.form.get("categoria")

        quantidade = float(quantidade)
        valor_unitario = float(valor_unitario)
        valor_total = valor_unitario * quantidade
        data_cadastro = datetime.now()

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO produto (nome_produto, valor_produto, quantidade, custo, data_cadastro, categoria) 
                VALUES (%s, %s, %s, %s, %s, %s)""", (nome_produto, valor_unitario, quantidade, valor_total, data_cadastro, categoria))
            conn.commit()

    return render_template("produto.html")


@app.route("/editar-produto/<int:id>")
def editar_produto(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM produto WHERE id_produto = %s", (id,))
        produto = cursor.fetchone()
    conn.close()

    return render_template("editar-produto.html", produto=produto)

@app.route("/update_produto", methods=["POST"])
def update_produto():
    id_produto = request.form["id_produto"]
    nome = request.form["nome_produto"]
    quantidade = float(request.form["quantidade"])
    valor_unitario = float(request.form["valor_unitario"])
    categoria = request.form.get("categoria")
    custo = quantidade * valor_unitario

    conn = get_connection()
    with conn.cursor() as cursor:

        # primeira consulta pra validar se aquele item já n existe
        cursor.execute("""
            SELECT COUNT(*) AS total FROM produto  
            WHERE nome_produto = %s AND id_produto != %s""",
            (nome, id_produto))
        resultado = cursor.fetchone()

        if resultado["total"] > 0:
            conn.close()

            # retornando pra mesma tela mas com a mensagem de erro
            return render_template(
                "editar-produto.html",
                produto={
                    "id_produto": id_produto,
                    "nome_produto": nome,
                    "quantidade": quantidade,
                    "valor_produto": valor_unitario
                },
                erro="Já existe um produto com esse nome!"
            )
        
        # atualização de fato (se tiver tudo certo)
        cursor.execute("""
            UPDATE produto
            SET nome_produto = %s,
                quantidade = %s,
                valor_produto = %s,
                custo = %s,
                categoria = %s
            WHERE id_produto = %s
        """, (nome, quantidade, valor_unitario, custo, categoria, id_produto))
        conn.commit()
    conn.close()

    return redirect("/")


# rota feita
@app.route("/desativar-produto/<int:id>")
def desativar_produto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE produto SET ativo = FALSE WHERE id_produto = %s", (id,))
    conn.commit()
    cursor.close()
    return redirect("/")

@app.route("/ativar_produto/<int:id>")
def ativar_produto(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE produto SET ativo = TRUE WHERE id_produto = %s", (id,))
        conn.commit()
    return redirect("/")



@app.route("/entrada_produto/<int:id_produto>", methods=["POST"])
def entrada_produto(id_produto):
    conn = get_connection()

    quantidade = float(request.form["quantidade"])
    valor_unitario = float(request.form["valor_unitario"])
    observacao = request.form.get("observacao", "")

    with conn.cursor() as cursor:
        # registrar movimentação
        cursor.execute("""
            INSERT INTO movimentos_produtos (id_produto, tipo_movimento, quantidade, valor_unitario)
            VALUES (%s, 'entrada', %s, %s)
        """, (id_produto, quantidade, valor_unitario))

        # atualizar estoque do produto
        cursor.execute("""
            UPDATE produto
            SET quantidade = quantidade + %s
            WHERE id_produto = %s
        """, (quantidade, id_produto))

        conn.commit()
    conn.close()

    return redirect("/produtos")

@app.route("/baixa", methods=["GET", "POST"])
def baixa():
    conn = get_connection()

    if request.method == 'GET':
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_produto, nome_produto FROM produto WHERE ativo = 1")
            produtos = cursor.fetchall()
        conn.close()

        return render_template("baixa.html", produtos=produtos)

    id_produto = request.form.get("id_produto")
    quantidade = request.form.get("quantidade_baixa")
    data_movimento = datetime.now()

    if not id_produto:
        conn.close()
        return "Erro: selecione um produto", 400

    quantidade = float(quantidade)


    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO movimentos_produtos (
                id_produto, tipo_movimento, quantidade, valor_unitario, origem_movimento, data_movimento
            ) VALUES (%s, 'saida', %s, NULL, 'baixa', %s)""", (id_produto, quantidade, data_movimento))

        cursor.execute("""
            UPDATE produto
            SET quantidade = quantidade - %s
            WHERE id_produto = %s
        """, (quantidade, id_produto))

        conn.commit()
    conn.close()

    return redirect("/")





@app.route("/venda", methods=["GET", "POST"])
def venda():
    conn = get_connection()
    if request.method == "POST":
        id_produto = request.form.get("id_produto")
        quantidade_vendida = float(request.form.get("quantidade"))
        valor_venda_unitario = float(request.form.get("valorUnitario"))
        valor_total = valor_venda_unitario * quantidade_vendida
        data_venda = datetime.now()

        with conn.cursor() as cursor:
            # SELECT pra diminuir a quantidade na outra tabela
            cursor.execute("SELECT quantidade, valor_produto FROM produto WHERE id_produto = %s", (id_produto,))
            produto = cursor.fetchone()

            if not produto:
                print("Produto não encontrado!")    
                return redirect(url_for("venda"))

            estoque_atual = float(produto["quantidade"])
            valor_unitario_produto = float(produto["valor_produto"])

            if estoque_atual < quantidade_vendida:
                print("Estoque insuficiente para a venda!")
                return redirect(url_for("venda"))

            novo_estoque = estoque_atual - quantidade_vendida
            novo_custo = valor_unitario_produto * novo_estoque

            cursor.execute(
                "UPDATE produto SET quantidade = %s, custo=%s WHERE id_produto = %s",
                (novo_estoque, novo_custo, id_produto)
            )

            cursor.execute("""
                INSERT INTO movimentos_produtos 
                    (id_produto, tipo_movimento, quantidade, valor_unitario, origem_movimento, data_movimento)
                VALUES 
                    (%s, 'saida', %s, %s, 'venda', %s)
            """, (id_produto, quantidade_vendida, valor_venda_unitario, data_venda))

            cursor.execute("""
                INSERT INTO registro_vendas (id_produto, data_venda, quantidade_vendida, valor_venda_unitario, 
                valor_total)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_produto, data_venda,  quantidade_vendida, valor_venda_unitario, valor_total))
            conn.commit()

            conn.close()

        return redirect(url_for("venda"))

    with conn.cursor() as cursor:
        cursor.execute("SELECT id_produto, nome_produto FROM produto WHERE ativo = TRUE")
        produtos = cursor.fetchall()
    conn.close()
    return render_template("venda.html", produtos=produtos)


# todas as rotas de ingredientes já estão feitas (não mexer daqui para baixo)
# ----------------------------------------------------------------------------
@app.route("/ingredientes")
def ingredientes():
    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM producao")
        ingredientes = cursor.fetchall()

        total_itens = len(ingredientes)

        cursor.execute("""
            SELECT COALESCE(SUM(custo_unitario * estoque_atual), 0) AS total
            FROM producao
        """)    
        resultado = cursor.fetchone()
        total_custo = next(iter(resultado.values())) if resultado else 0

        cursor.execute("""
            SELECT COUNT(*) FROM producao
            WHERE estoque_atual = 0 OR estoque_atual < estoque_minimo
        """)
        resultado = cursor.fetchone()
        itens_baixo_estoque = next(iter(resultado.values())) if resultado else 0
    conn.close()

    return render_template("ingredientes.html", ingredientes=ingredientes, total_itens=total_itens, total_custo=total_custo,
        itens_baixo_estoque=itens_baixo_estoque)


@app.route("/add_ingrediente", methods=["GET", "POST"])
def add_ingrediente():
    conn = get_connection()
    if request.method == "POST":
        nome_ingrediente = request.form.get("nome_ingrediente")
        unidade_medida = request.form.get("unidade_medida")
        custo_unitario = request.form.get("custo_unitario")
        estoque = float(request.form["estoque_atual"])

        custo_unitario = float(custo_unitario)
        data_cadastro = datetime.now()

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO producao (nome_ingrediente, unidade_medida, custo_unitario, data_cadastro, estoque_atual) 
                VALUES (%s, %s, %s, %s, %s)""", (nome_ingrediente, unidade_medida, custo_unitario, data_cadastro, estoque))
            
            id_novo = cursor.lastrowid

            if estoque > 0:
                cursor.execute("""
                    INSERT INTO movimentos_estoque 
                        (id_producao, tipo_movimento, quantidade, custo_unitario, observacao)
                    VALUES (%s, 'entrada', %s, %s, %s)
                """, (id_novo, estoque, custo_unitario, 'Estoque inicial'))
            conn.commit()
        conn.close()

    return render_template("add-ingrediente.html")


# duas rotas: essa pra carregar o template e as informações
@app.route("/editar_ingrediente/<int:id_producao>")
def edit_ingrediente(id_producao):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM producao WHERE id_producao = %s", (id_producao,))
        ingrediente = cursor.fetchone()
    cursor.close()

    return render_template("editar-ingrediente.html", ingrediente=ingrediente)


# essa para atualização do banco de dados
@app.route("/update_ingrediente", methods=["POST"])
def update_ingrediente():
    conn = get_connection()
    if request.method == "POST":
        id_producao = request.form["id_producao"]
        nome = request.form["nome_ingrediente"]
        unidade = request.form["unidade_medida"]
        custo = request.form["custo_unitario"]
        estoque = request.form["estoque_atual"]

        with conn.cursor() as cursor:
            cursor.execute(""" 
                UPDATE producao
                SET nome_ingrediente = %s,
                    unidade_medida = %s,
                    custo_unitario = %s,
                    estoque_atual = %s
                WHERE id_producao = %s
            """, (nome, unidade, custo, estoque, id_producao))
            conn.commit()
        cursor.close()

        return redirect("/ingredientes")


@app.route("/desativar_ingrediente/<int:id_producao>", methods=["GET", "POST"])
def desativar_ingrediente(id_producao):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE producao SET ativo = 0 WHERE id_producao = %s", (id_producao,))
    conn.commit()
    cursor.close()
    return redirect("/ingredientes")

@app.route("/ativar_ingrediente/<int:id_producao>")
def ativar_ingrediente(id_producao):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE producao SET ativo = 1 WHERE id_producao = %s", (id_producao,))
        conn.commit()
    conn.close()
    return redirect("/ingredientes")


# as duas rotas seguintes servem para facilitar a criação de relatórios
@app.route("/entrada_estoque/<int:id_producao>", methods=["POST"])
def entrada_estoque(id_producao):
    conn = get_connection()

    if request.method == "POST":
        quantidade = float(request.form["quantidade"])
        custo_unitario = float(request.form["custo_unitario"])
        observacao = request.form.get("observacao", "")

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO movimentos_estoque (id_producao, tipo_movimento, quantidade, custo_unitario, observacao)
                VALUES (%s, 'entrada', %s, %s, %s)
            """, (id_producao, quantidade, custo_unitario, observacao))

            cursor.execute("""
                UPDATE producao
                SET estoque_atual = estoque_atual + %s
                WHERE id_producao = %s
            """, (quantidade, id_producao))

            conn.commit()
        conn.close()
    return redirect("/ingredientes")


@app.route("/saida_estoque/<int:id_producao>", methods=["POST"])
def saída_estoque(id_producao):
    conn = get_connection()
    if request.method == "POST":
        quantidade = float(request.form["quantidade"])
        observacao = request.form.get("observacao", "")

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO movimentos_estoque (id_producao, tipo_movimento, quantidade, observacao)
                VALUES (%s, 'saida', %s, %s)
            """, (id_producao, quantidade, observacao))

            cursor.execute("""
                UPDATE producao
                SET estoque_atual = estoque_atual - %s
                WHERE id_producao = %s
            """, (quantidade, id_producao))

            conn.commit()
        conn.close()
    return redirect("/ingredientes")


@app.route("/graficos")
def graficos():
    conn = get_connection()
    with conn.cursor() as cursor:
        
        # gráfico de evolução de estoque 
        cursor.execute("""
            SELECT 
                DATE(data_movimento) AS dia,
                SUM(
                    CASE 
                        WHEN origem_movimento IN ('venda', 'baixa') THEN -quantidade
                        WHEN origem_movimento IN ('compra', 'ajuste_entrada') THEN quantidade
                        ELSE 0
                    END
                ) AS quantidade_ajustada
            FROM movimentos_produtos
            GROUP BY DATE(data_movimento)
            ORDER BY dia;

        """)
        evolucao = cursor.fetchall()

        # gráfico de categorias
        cursor.execute("""
            SELECT categoria AS nome_categoria,
            SUM(quantidade) AS total_categoria
            FROM produto WHERE ativo = 1
            GROUP BY categoria
            ORDER BY total_categoria DESC
        """)
        categorias = cursor.fetchall()

        # gráfico curva ABC 
        cursor.execute("""
            SELECT 
                p.nome_produto AS nome,
                (p.quantidade * p.valor_produto) AS custo_total
            FROM produto p
            WHERE p.ativo = 1;
        """)
        curva = cursor.fetchall()

        # gráfico vendas
        cursor.execute("""
            SELECT 
                p.nome_produto,
                SUM(v.quantidade_vendida) AS total_vendido
            FROM registro_vendas v
            JOIN produto p ON p.id_produto = v.id_produto
            WHERE p.ativo = 1
            GROUP BY p.nome_produto
            ORDER BY total_vendido DESC;
        """)

        vendas = cursor.fetchall()

    pasta = "static/graficos"
    os.makedirs(pasta, exist_ok=True)


    if evolucao:
        datas = []
        valores_acumulados = []

        saldo = 0  

        for r in evolucao:
            data = str(r["dia"])
            delta = float(r["quantidade_ajustada"] or 0)

            saldo += delta  # acumula o movimento

            datas.append(data)
            valores_acumulados.append(saldo)

        plt.figure(figsize=(8,4))
        plt.plot(datas, valores_acumulados, marker="o")
        plt.xticks(rotation=45)
        plt.title("Evolução Acumulada do Estoque")
        plt.tight_layout()
        plt.savefig(f"{pasta}/evolucao.png")
        plt.close()


    if categorias:
        nomes = [l['nome_categoria'] for l in categorias]
        valores = [float(l['total_categoria'] or 0) for l in categorias]

        plt.figure(figsize=(8,4))
        plt.bar(nomes, valores)
        plt.title("Estoque por Categoria")
        plt.tight_layout()
        plt.savefig(f"{pasta}/categorias.png")
        plt.close()

    if curva:
        dados = sorted(curva, key=lambda x: x["custo_total"], reverse=True)
        nomes = [d["nome"] for d in dados]
        custos = [float(d["custo_total"] or 0) for d in dados]

        soma_total = sum(custos)
        porcentagens = [(c / soma_total) * 100 for c in custos]
        acumulado = []
        soma = 0
        for p in porcentagens:
            soma += p
            acumulado.append(soma)

        plt.figure(figsize=(8,4))
        plt.plot(nomes, acumulado, marker="o")
        plt.xticks(rotation=45)
        plt.title("Curva ABC — Custos de Estoque (%)")
        plt.tight_layout()
        plt.savefig(f"{pasta}/curva_abc.png")
        plt.close()
    
    if vendas:
        nomes = [linha.get("nome_produto", "Desconhecido") for linha in vendas]
        totais = [float(linha.get("total_vendido") or 0) for linha in vendas]

        plt.figure(figsize=(10,6))
        plt.bar(nomes, totais)
        plt.xticks(rotation=45, ha="right")
        plt.title("Vendas por Produto")
        plt.xlabel("Produto")
        plt.ylabel("Quantidade Vendida")
        plt.tight_layout()

        plt.savefig("static/graficos/vendas.png")
        plt.close()
    else:
        print("Nenhuma venda encontrada. Gráfico não gerado.")

    return render_template("graficos.html")