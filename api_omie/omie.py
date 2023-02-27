import requests

from typing import List, Dict

from dotenv import load_dotenv
import os

import math

class OmieAPI:
    def __init__(self) -> None:
        load_dotenv()
        self.app_key = os.getenv("OMIE_KEY")
        self.app_secret = os.getenv("OMIE_SECRET")
        self.url = 'https://app.omie.com.br/api/v1/geral/produtos/'
        
        
    def altera_produto(self, codigo, **kwargs) -> Dict:
        json_data = {
            'call': 'AlterarProduto',
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'param': [{
                'codigo_produto': None,
                'codigo_produto_integracao': None,
                'codigo': codigo,
                **kwargs
            }]}     
        return requests.post(self.url, json= json_data).json()
    
    def consulta_produto(self, codigo) -> Dict:
        json_data = {
            'call': 'ConsultarProduto',
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'param': [{
                'codigo_produto': None,
                'codigo_produto_integracao': None,
                'codigo': codigo                
            }]
        }
        return requests.post(self.url, json=json_data).json()
    
    def exclui_produto(self, codigo) -> Dict:
        json_data = {
            'call': 'ExcluirProduto',
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'param': [{
                'codigo_produto': None,
                'codigo_produto_integracao': None,
                'codigo': codigo
            }]
        }
        response = requests.post(self.url, json=json_data)
        return response.json()
    
    def inclui_produto(self, codigo, **kwargs) -> Dict:
        json_data = {
            'call': 'IncluirProduto',
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'param': [{
                'codigo_produto': None,
                'codigo_produto_integracao': None,
                'codigo': codigo,
                **kwargs
            }]
        }
        return requests.post(self.url, json=json_data).json()

    
    def lista_produto(self, **kwargs) -> Dict:
        json_data = {
            'call': 'ListarProdutos',
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'param': [{
                'apenas_importado_api':'N',
                'filtrar_apenas_omiepdv': 'N',
                'exibir_kit': 'S',
                **kwargs
            }]
        }
        return requests.post(self.url, json=json_data).json()

    def lista_produto_resumido(self, **kwargs) -> Dict:
        json_data = {
            'call': 'ListarProdutosResumido',
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'param': [{
                'apenas_importado_api':'N',
                'filtrar_apenas_omiepdv': 'N',
                'exibir_kit': 'S',                
                **kwargs
            }]
        }
        return requests.post(self.url, json=json_data).json()
    
    def listar_todos_produtos(self, por_pagina: int = 500) -> List[Dict[str, any]]:
        print('Listando produtos Omie.')
        produtos = []
        pagina = 1
        while True:
            print(f'Listando produtos da página {pagina}.')
            response = self.lista_produto(pagina=pagina, registros_por_pagina=por_pagina)
            total_paginas = response.get('total_de_paginas')
            produtos.extend(response.get('produto_servico_cadastro', []))
            if pagina >= total_paginas:
                break
            pagina += 1
        print('Listagem de produtos Omie finalizada.')
        return produtos
    
    

    def deleta_componentes_kit(self, codigo_produto, codigo_componente) -> Dict:
        self.url = 'https://app.omie.com.br/api/v1/geral/produtoskit/'
        json_data = {
            'call': 'AlterarComponentesKit',
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'param': [{
                'codigo_produto': codigo_produto,
                'componentes_kit':[
                    {
                     'acao_componente': 'E',
                     'codigo_componente': codigo_componente   
                    }
                ]
            }]
        }
        return requests.post(self.url, json=json_data).json()
    
    def extrair_componentes(self, dados_componentes):
        print("Listando os componentes dos Kits da Omie.")
        return [
            {
                'codigo': produto['codigo'], 
                'codigo_componente': componente['codigo_componente'], 
                'codigo_produto_componente': componente['codigo_produto_componente'], 
                'valor_unitario_componente': componente['valor_unitario_componente'],
                'quantidade_componente': componente['quantidade_componente'], 
                'local_estoque_componente': componente['local_estoque_componente']
            }
            for produto in dados_componentes
            for componente in produto.get('componentes_kit', [])
        ]
    
    def extrair_recomendacoes_fiscais(self, dados_produtos) -> list:
        return [
            {
                **{
                    'codigo': produto['codigo']}, 
                **produto['recomendacoes_fiscais']
                } 
            for produto in dados_produtos
            ]

        
   
    def extrair_imagens(self, dados_produtos) -> list:
        return [
            {
                'codigo': produto['codigo'], 
                'url_imagem': imagem['url_imagem']
                } 
            for produto in dados_produtos 
            if 'imagens' in produto for imagem in produto['imagens']
            ]
        
    def calcular_preco_custo(self, lista_produtos):
        # Cria um dicionário para fazer lookup dos valores unitários dos produtos
        valores_unitarios = {produto['codigo_produto']: produto['valor_unitario'] for produto in lista_produtos}
        
        # Define uma função auxiliar para calcular o preço de custo de um componente do kit
        def calcular_preco_custo_componente(componente):
            valor_unitario = valores_unitarios[componente['codigo_produto_componente']]
            return componente['quantidade_componente'] * valor_unitario

        # Define uma função auxiliar para calcular o preço de custo de um produto
        def calcular_preco_custo_produto(produto):
            if 'componentes_kit' in produto:
                # Se o produto for um kit, calcula o preço de custo dos componentes
                preco_custo_componentes = sum([calcular_preco_custo_componente(c) for c in produto['componentes_kit']])
                preco_custo = preco_custo_componentes
            else:
                # Se o produto não for um kit, o preço de custo é igual ao valor unitário
                preco_custo = produto['valor_unitario']
            return round(preco_custo, 2)

        # Calcula o preço de custo de cada produto e armazena em uma lista de dicionários
        precos_custo = [
            {'codigo': produto['codigo_produto'], 
             'custo_composicao': math.ceil(calcular_preco_custo_produto(produto)*100)/100
             } for produto in lista_produtos]
        
        return precos_custo

    def listar_familias(self) -> List:
        url = 'https://app.omie.com.br/api/v1/geral/familias/'
        categorias = []
        json_data = {
        'call': 'PesquisarFamilias',
        'app_key': '2402692597305',
        'app_secret': '3be3f1c474093fc3e307e81fa8476a7e',
        'param': [
            {
                'pagina': 1,
                'registros_por_pagina': 500,
                    },
                ],
            }
        response = requests.post(url, json=json_data).json()
        categorias.extend(response.get('famCadastro', []))
        return categorias
        
    
    
            
    

    

    

