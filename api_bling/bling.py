import requests
import time
from typing import Dict, List

from dotenv import load_dotenv
import os


class BlingAPI:
    def __init__(self) -> None:
        load_dotenv()
        self.api_key = os.getenv('BLING_KEY')
        self.url = 'https://bling.com.br/Api/v2/'

    def _get(self, endpoint: str, params: Dict) -> Dict:
        """Método privado que realiza a chamada GET na API do Bling."""
        response = requests.get(endpoint, params=params)
        return response.json()

    def buscar_produto_por_codigo(self, codigo: str, estoque: str = None, loja: str = None, imagem: str = None) -> Dict:
        """Busca um produto no Bling pelo código informado."""
        endpoint = f'{self.url}produto/{codigo}/json/'
        params = {
            'apikey': self.api_key,
            'estoque': estoque,
            'loja': loja,
            'imagem': imagem            
        }
        return self._get(endpoint, params)

    def buscar_pagina_de_produtos(self, pagina: int, estoque: str = None, loja: str = None, imagem: str = None) -> Dict:
        """Busca uma página de produtos no Bling."""
        endpoint = f'{self.url}produtos/page={pagina}/json/'
        params ={
            'apikey': self.api_key,
            'estoque': estoque,
            'loja': loja,
            'imagem': imagem
        }
        return self._get(endpoint, params)

    def pegar_todos_produtos(self, estoque: str = None, loja: str = None, imagem: str = None) -> List[Dict]:
        """Busca todos os produtos do Bling."""
        print('Iniciando busca de produtos Bling.')
        pagina = 1
        produtos = []
        while True:
            print(f'Buscando itens da página {pagina}.')
            json_response = self.buscar_pagina_de_produtos(pagina, estoque, loja, imagem)
            if 'produtos' not in json_response['retorno']:
                print('Finalizada a busca de produtos no Bling.')
                break
            produtos.extend([produto['produto'] for produto in json_response['retorno']['produtos']])
            pagina += 1
            time.sleep(1)
        return produtos

    def buscar_pagina_de_categorias(self, pagina: int) -> Dict:
        """Busca uma página de categorias no Bling."""
        endpoint = f'{self.url}categorias/page={pagina}/json/'
        params = {
            'apikey': self.api_key
        }
        return self._get(endpoint, params)

    def listar_categorias(self) -> List[Dict]:
        """Busca todas as categorias do Bling."""
        print('Iniciando busca de categorias Bling.')
        pagina = 1
        categorias =[]
        while True:
            print(f'Buscando itens da página {pagina}.')
            response = self.buscar_pagina_de_categorias(pagina)
            if 'categorias' not in response['retorno']:
                print('Finalizada a busca de categorias no Bling.')
                break
            categorias.extend([categoria['categoria'] for categoria in response['retorno']['categorias']])
            pagina += 1
            time.sleep(1)
        return categorias
