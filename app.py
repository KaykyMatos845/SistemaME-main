from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
import csv
import os
import random
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

# Caminho para arquivos CSV
CLIENTES_CSV = 'clientes.csv'
PRODUTOS_CSV = 'produto.csv'
PEDIDOS_CSV = 'pedidos.csv'
PEDIDO_DETALHE_CSV = 'pedidodetalhe.csv'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cadastro-clientes', methods=['GET', 'POST'])
def cadastro_clientes():
    if request.method == 'POST':
        # Gerar ID único
        if os.path.isfile(CLIENTES_CSV):
            with open(CLIENTES_CSV, 'r') as file:
                reader = csv.reader(file)
                lines = list(reader)
                next_id = len(lines)
        else:
            next_id = 0
        cliente_id = f'cliente{next_id + 1}'

        # Captura dados do formulário
        cliente = {
            'ID': cliente_id,
            'Nome': request.form.get('nome'),
            'Telefone': request.form.get('telefone'),
            'Instagram': request.form.get('instagram'),
            'Email': request.form.get('email'),
            'Endereco': request.form.get('endereco'),
            'Tipo': request.form.get('tipo'),
            'Documento': request.form.get('documento'),
            'Inscricao Estadual': request.form.get('inscricao_estadual'),
            'Observacoes': request.form.get('obs')
        }

        # Salvar no CSV
        file_exists = os.path.isfile(CLIENTES_CSV)
        try:
            with open(CLIENTES_CSV, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=cliente.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(cliente)
        except Exception as e:
            print("Erro ao salvar os dados no arquivo CSV:", e)

        return redirect(url_for('home'))
    return render_template('cadastro_clientes.html')


@app.route('/cadastro-produtos', methods=['GET', 'POST'])
def cadastro_produtos():
    if request.method == 'POST':
        # Gerar ID único
        if os.path.isfile(PRODUTOS_CSV):
            with open(PRODUTOS_CSV, 'r') as file:
                reader = csv.reader(file)
                lines = list(reader)
                next_id = len(lines)
        else:
            next_id = 0
        produto_id = f'produto{next_id + 1}'

        # Captura dados do formulário
        produto = {
            'ID': produto_id,
            'Tipo': request.form.get('tipo'),
            'Descricao': request.form.get('descricao'),
            'PrecoVenda': request.form.get('preco_venda'),
            'CustoProducao': request.form.get('custo_producao')
        }

        # Salvar no CSV
        try:
            file_exists = os.path.isfile(PRODUTOS_CSV)
            with open(PRODUTOS_CSV, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=produto.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(produto)
        except Exception as e:
            print("Erro ao salvar os dados no arquivo CSV:", e)

        return redirect(url_for('home'))

    # Carregar tipos de produtos
    tipos_produto = []
    if os.path.isfile('tipo_produto.csv'):
        with open('tipo_produto.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                tipos_produto.append({
                    'ID': row['Id'],
                    'Descricao': row['descrição']
                })

    return render_template('cadastro_produtos.html', tipos_produto=tipos_produto)


@app.route('/cadastro-pedidos', methods=['GET', 'POST'])
def cadastro_pedidos():
    if request.method == 'POST':
        # Gerar número único para o pedido
        pedido_num = None
        existing_numbers = set()
        if os.path.isfile(PEDIDOS_CSV):
            with open(PEDIDOS_CSV, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_numbers.add(row['Numero'])
        while True:
            random_number = random.randint(1000, 9999)
            pedido_num = f"PED-{random_number}"
            if pedido_num not in existing_numbers:
                break

        # Obter informações do cliente
        cliente_id = request.form.get('cliente_id')
        cliente_nome = None
        if os.path.isfile(CLIENTES_CSV):
            with open(CLIENTES_CSV, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['ID'] == cliente_id:
                        cliente_nome = row['Nome']
                        break

        # Dados do pedido
        pedido = {
            'Numero': pedido_num,
            'ClienteID': cliente_id,
            'ClienteNome': cliente_nome,
            'DataPedido': request.form.get('data_pedido'),
            'DataEntrega': request.form.get('data_entrega'),
            'ValorPedido': request.form.get('valor_pedido'),
            'Situacao': request.form.get('situacao')
        }

        # Salvar pedido no CSV
        try:
            file_exists = os.path.isfile(PEDIDOS_CSV)
            with open(PEDIDOS_CSV, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=pedido.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(pedido)
        except Exception as e:
            print("Erro ao salvar os dados do pedido no arquivo CSV:", e)

        # Salvar detalhes dos produtos no CSV
        produtos_id = request.form.getlist('produto_id[]')
        produtos_descricao = request.form.getlist('produto_descricao[]')
        precos_venda = request.form.getlist('preco_venda[]')
        custos_producao = request.form.getlist('custo_producao[]')
        quantidades = request.form.getlist('quantidade[]')
        totais = request.form.getlist('total[]')

        try:
            file_exists = os.path.isfile(PEDIDO_DETALHE_CSV)
            with open(PEDIDO_DETALHE_CSV, mode='a', newline='') as file:
                fieldnames = ['NumeroPedido', 'ProdutoID', 'ProdutoDescricao', 'PrecoVenda', 'CustoProducao', 'Quantidade', 'Total']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                for i in range(len(produtos_id)):
                    detalhe = {
                        'NumeroPedido': pedido_num,
                        'ProdutoID': produtos_id[i],
                        'ProdutoDescricao': produtos_descricao[i],
                        'PrecoVenda': "{:.2f}".format(float(precos_venda[i])),
                        'CustoProducao': "{:.2f}".format(float(custos_producao[i])),
                        'Quantidade': int(quantidades[i]),
                        'Total': "{:.2f}".format(float(totais[i]))
                    }
                    writer.writerow(detalhe)
        except Exception as e:
            print("Erro ao salvar os detalhes do pedido no arquivo CSV:", e)

        return redirect(url_for('home'))

    # Carregar clientes e produtos
    clientes = []
    if os.path.isfile(CLIENTES_CSV):
        with open(CLIENTES_CSV, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                clientes.append(row)

    produtos = []
    if os.path.isfile(PRODUTOS_CSV):
        with open(PRODUTOS_CSV, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                produtos.append(row)

    return render_template('cadastro_pedidos.html', clientes=clientes, produtos=produtos)



@app.route('/get_produto/<produto_id>', methods=['GET'])
def get_produto(produto_id):
    if os.path.isfile(PRODUTOS_CSV):
        with open(PRODUTOS_CSV, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['ID'] == produto_id:
                    return jsonify({
                        'PrecoVenda': row['PrecoVenda'],
                        'CustoProducao': row['CustoProducao']
                    })
    return jsonify({})


@app.route('/produtos', methods=['GET'])
def buscar_produtos():
    query = request.args.get('q', '').lower()
    produtos = []

    with open(PRODUTOS_CSV, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if query in row['Descricao'].lower():
                produtos.append({
                    'ID': row['ID'],
                    'Descricao': row['Descricao'],
                    'PrecoVenda': row['PrecoVenda'],
                    'CustoProducao': row['CustoProducao']
                })

    return jsonify(produtos)


if __name__ == '__main__':
    app.run(debug=True)
