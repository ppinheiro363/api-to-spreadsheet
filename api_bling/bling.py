import requests
from typing import List, Dict
import time

from dotenv import load_dotenv
import os

class BlingAPI:
    def __init__(self) -> None:
        load_dotenv()
        self.apikey = os.getenv('BLING_KEY')
        self.url = 'https://bling.com.br/Api/v2/'

    def buscar_produto_codigo(self, codigo: str, estoque: str = None, loja: str = None, imagem: str = None) -> Dict:
        endpoint = f'{self.url}produto/{codigo}/json/'
        params = {
            'apikey': self.apikey,
            'estoque': estoque,
            'loja': loja,
            'imagem': imagem            
        }
        response = requests.get(endpoint, params=params )
        return response.json()
    
    def buscar_pagina_produtos(self, pagina: int, estoque: str = None, loja: str = None, imagem: str = None) -> Dict:
        endpoint = f'{self.url}produtos/page={pagina}/json/'
        params ={
            'apikey': self.apikey,
            'estoque': estoque,
            'loja': loja,
            'imagem': imagem
        }
        response = requests.get(endpoint, params=params)
        return response.json()
    
    def pegar_todos_produtos(self, estoque: str = None, loja: str = None, imagem: str = None) -> List[Dict]:
        print('Iniciando busca de produtos Bling.')
        pagina = 1
        produtos = []
        while True:
            print(f'Buscando itens da pagina {pagina}.')
            json_response = self.buscar_pagina_produtos(pagina, estoque, loja, imagem)
            if 'produtos' not in json_response['retorno']:
                print('Finalizado a busca de produtos no Bling.')
                break
            produtos.extend([produto['produto'] for produto in json_response['retorno']['produtos']])
            pagina += 1
            time.sleep(1)
        return produtos
    
    def busca_pagina_categoria(self, pagina: int) -> List[Dict]:
        endpoint = f'{self.url}categorias/page={pagina}/json/'
        params = {
            'apikey': self.apikey
        }
        response = requests.get(endpoint, params=params)
        return response.json()
    
    def listar_categorias(self) -> List[Dict]:
        print('Iniciando busca de categorias Bling.')
        pagina = 1
        categorias =[]
        while True:
            print(f'Buscando itens da pagina {pagina}.')
            response = self.busca_pagina_categoria(pagina)
            if 'categorias' not in response['retorno']:
                print('Finalizado a busca de categorias no Bling.')
                break
            categorias.extend([categoria['categoria'] for categoria in response[ 'retorno']['categorias']])
            pagina += 1
            time.sleep(1)
        return categorias
            
        
    
        
    
        
    
# {'retorno': {'erros': {'erro': {'cod': 3, 'msg': 'API Key invalida'}}}}