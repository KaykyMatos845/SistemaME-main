from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
import csv
import os
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro-clientes', methods=['GET', 'POST'])
def cadastro_clientes():
    if request.method == 'POST':
        # Gerar um ID único no formato cliente1, cliente2, etc.
        if os.path.isfile('clientes.csv'):
            with open('clientes.csv', 'r') as file:
                reader = csv.reader(file)
                lines = list(reader)
                next_id = len(lines)  # Contar o número de linhas no arquivo CSV
        else:
            next_id = 0
        cliente_id = f'cliente{next_id + 1}'
        
        # Lógica para lidar com dados do formulário enviados via POST
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
        
        # Verificar se os dados do formulário foram recebidos corretamente
        print("Dados recebidos do formulário:", cliente)
        
        # Verificar se o arquivo CSV já existe
        file_exists = os.path.isfile('clientes.csv')
        
        # Salvar os dados no arquivo CSV
        try:
            with open('clientes.csv', mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=cliente.keys())
                if not file_exists:
                    writer.writeheader()  # Escrever o cabeçalho se o arquivo não existir
                writer.writerow(cliente)
            print("Dados salvos no arquivo CSV com sucesso.")
        except Exception as e:
            print("Erro ao salvar os dados no arquivo CSV:", e)
        
        # Redirecionar para a página inicial após salvar os dados
        return redirect(url_for('home'))
    return render_template('cadastro_clientes.html')

@app.route('/cadastro-produtos', methods=['GET', 'POST'])
def cadastro_produtos():
    if request.method == 'POST':
        # Gerar um ID único no formato produto1, produto2, etc.
        if os.path.isfile('produto.csv'):
            with open('produto.csv', 'r') as file:
                reader = csv.reader(file)
                lines = list(reader)
                next_id = len(lines)  # Contar o número de linhas no arquivo CSV
        else:
            next_id = 0
        produto_id = f'produto{next_id + 1}'
        
        # Lógica para lidar com dados do formulário enviados via POST
        produto = {
            'ID': produto_id,
            'Tipo': request.form.get('tipo'),
            'Descricao': request.form.get('descricao'),
            'PrecoVenda': request.form.get('preco_venda'),
            'CustoProducao': request.form.get('custo_producao')
        }
        
        # Verificar se os dados do formulário foram recebidos corretamente
        print("Dados recebidos do formulário:", produto)
        
        # Verificar se o arquivo CSV já existe
        file_exists = os.path.isfile('produto.csv')
        
        # Salvar os dados no arquivo CSV
        try:
            with open('produto.csv', mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=produto.keys())
                if not file_exists:
                    writer.writeheader()  # Escrever o cabeçalho se o arquivo não existir
                writer.writerow(produto)
            print("Dados salvos no arquivo CSV com sucesso.")
        except Exception as e:
            print("Erro ao salvar os dados no arquivo CSV:", e)
        
        # Redirecionar para a página inicial após salvar os dados
        return redirect(url_for('home'))
    
    # Ler o arquivo tipo_produto.csv para preencher a lista suspensa
    tipos_produto = []
    if os.path.isfile('tipo_produto.csv'):
        with open('tipo_produto.csv', 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                tipos_produto.append(row)
    
    return render_template('cadastro_produtos.html', tipos_produto=tipos_produto)

@app.route('/cadastro-pedidos', methods=['GET', 'POST'])
def cadastro_pedidos():
    if request.method == 'POST':
        # Gerar um número de pedido único no formato 1.ano_atual
        if os.path.isfile('pedidos.csv'):
            with open('pedidos.csv', 'r') as file:
                reader = csv.reader(file)
                lines = list(reader)
                next_num = len(lines)  # Contar o número de linhas no arquivo CSV
        else:
            next_num = 0
        pedido_num = f'{next_num + 1}.{datetime.now().year}'
        
        # Obter o nome do cliente a partir do ID
        cliente_id = request.form.get('cliente_id')
        cliente_nome = None
        if os.path.isfile('clientes.csv'):
            with open('clientes.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['ID'] == cliente_id:
                        cliente_nome = row['Nome']
                        break
        
        # Lógica para lidar com dados do formulário enviados via POST
        pedido = {
            'Numero': pedido_num,
            'ClienteID': cliente_id,
            'ClienteNome': cliente_nome,
            'DataPedido': request.form.get('data_pedido'),
            'DataEntrega': request.form.get('data_entrega'),
            'ValorPedido': request.form.get('valor_pedido'),
            'Situacao': request.form.get('situacao')
        }
        
        # Verificar se os dados do formulário foram recebidos corretamente
        print("Dados recebidos do formulário:", pedido)
        
        # Verificar se o arquivo CSV já existe
        file_exists = os.path.isfile('pedidos.csv')
        
        # Salvar os dados no arquivo CSV
        try:
            with open('pedidos.csv', mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=pedido.keys())
                if not file_exists:
                    writer.writeheader()  # Escrever o cabeçalho se o arquivo não existir
                writer.writerow(pedido)
            print("Dados salvos no arquivo CSV com sucesso.")
        except Exception as e:
            print("Erro ao salvar os dados no arquivo CSV:", e)
        
        # Salvar os detalhes do pedido no arquivo pedidodetalhe.csv
        produtos = request.form.getlist('produto')
        quantidades = request.form.getlist('quantidade')
        precos_venda = request.form.getlist('preco_venda')
        custos_producao = request.form.getlist('custo_producao')
        totais = request.form.getlist('total')
        
        try:
            with open('pedidodetalhe.csv', mode='a', newline='') as file:
                fieldnames = ['NumeroPedido', 'ProdutoID', 'ProdutoDescricao', 'PrecoVenda', 'CustoProducao', 'Quantidade', 'Total']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if not os.path.isfile('pedidodetalhe.csv'):
                    writer.writeheader()  # Escrever o cabeçalho se o arquivo não existir
                for i in range(len(produtos)):
                    # Obter a descrição do produto a partir do ID
                    produto_descricao = None
                    if os.path.isfile('produto.csv'):
                        with open('produto.csv', 'r') as file:
                            reader = csv.DictReader(file)
                            for row in reader:
                                if row['ID'] == produtos[i]:
                                    produto_descricao = row['Descricao']
                                    break
                    detalhe = {
                        'NumeroPedido': pedido_num,
                        'ProdutoID': produtos[i],
                        'ProdutoDescricao': produto_descricao,
                        'PrecoVenda': precos_venda[i],
                        'CustoProducao': custos_producao[i],
                        'Quantidade': quantidades[i],
                        'Total': totais[i]
                    }
                    writer.writerow(detalhe)
            print("Detalhes do pedido salvos no arquivo CSV com sucesso.")
        except Exception as e:
            print("Erro ao salvar os detalhes do pedido no arquivo CSV:", e)
        
        # Redirecionar para a página inicial após salvar os dados
        return redirect(url_for('home'))
    
    # Ler o arquivo clientes.csv para preencher a lista suspensa
    clientes = []
    if os.path.isfile('clientes.csv'):
        with open('clientes.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                clientes.append(row)
    
    # Ler o arquivo produto.csv para preencher a lista suspensa de produtos
    produtos = []
    if os.path.isfile('produto.csv'):
        with open('produto.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                produtos.append(row)
    
    return render_template('cadastro_pedidos.html', clientes=clientes, produtos=produtos)

@app.route('/get_produto/<produto_id>', methods=['GET'])
def get_produto(produto_id):
    if os.path.isfile('produto.csv'):
        with open('produto.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['ID'] == produto_id:
                    return jsonify({
                        'PrecoVenda': row['PrecoVenda'],
                        'CustoProducao': row['CustoProducao']
                    })
    return jsonify({})
    return jsonify({})

@app.route('/produtos', methods=['GET'])
def buscar_produtos():
    query = request.args.get('q', '').lower()
    produtos = []

    with open('produto.csv', 'r') as file:
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