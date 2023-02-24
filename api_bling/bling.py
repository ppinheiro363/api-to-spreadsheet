import requests
from typing import List, Dict
import time

class BlingAPI:
    def __init__(self, apikey: str) -> None:
        self.apikey = apikey
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
        endpoint = f'{self.url}produtos/{pagina}/json'
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
                print(json_response['retorno'])
            produtos.extend([produto['produto'] for produto in json_response['retorno']['produtos']])
            pagina += 1
            time.sleep(1)
        print(f'Busca de produtos Bling finalizada.')
        return produtos
    
        
    
# {'retorno': {'erros': {'erro': {'cod': 3, 'msg': 'API Key invalida'}}}}