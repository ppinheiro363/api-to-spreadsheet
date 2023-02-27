import requests
from typing import List, Dict

from dotenv import load_dotenv
import os

class VtrinaAPI:
    def __init__(self) -> None:
        load_dotenv()
        self.token = os.getenv('VTRINA_TOKEN')
        self.url = 'https://api.vtrina.com/api/'
        
    def busca_pagina_produto(self, pagina: str, size: int = 1000, active: str = 'Ativo', store: str = 'true') -> List[Dict]:
        endpoint = f'{self.url}Products/'
        headers = {
                'Content-Type': 'application/json',
                'x-access-token': self.token,
                }

        params ={
            'Size': size,
            'Page': pagina,
            'active': active,
            'store': store
        }
        response = requests.get(endpoint, headers = headers, params=params)
        return response.json()
    
    def lista_todos_produtos(self) -> List[Dict]:
        print('Iniciando busca de todos produtos Vtrina.')
        pagina = 1
        produtos =[]
        while True:
            print(f'Buscando itens da pagina {pagina}.')
            response = self.busca_pagina_produto(pagina)
            if not response:
                print('Finalizando a busca de produtos no Vtrina.')
                break
            produtos.extend(response)
            pagina += 1
        return produtos
    
    