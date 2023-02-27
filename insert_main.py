from api_omie.omie import OmieAPI
from api_bling.bling import BlingAPI
from api_vtrina.vtrina import VtrinaAPI

from gspread_config.scope import atualiza_planilha

import datetime


class ColetaDadosAPIs:
    def __init__(self) -> None:
        self.omie = OmieAPI()
        self.bling = BlingAPI()
        self.vtrina = VtrinaAPI()

    def coletar_dados(self):
        omie_todos_produtos = self.omie.listar_todos_produtos()
        kits_omie = self.omie.extrair_componentes(omie_todos_produtos)
        preco_custo = self.omie.calcular_preco_custo(omie_todos_produtos)
        familias_omie = self.omie.listar_familias()
        bling_todos_produtos = self.bling.pegar_todos_produtos()
        categorias_bling = self.bling.listar_categorias()
        produtos_vtrina = self.vtrina.lista_todos_produtos()
        marketplaces_vtrina = self.vtrina.lista_marketplace()

        return {
            'omie_todos_produtos': omie_todos_produtos,
            'kits_omie': kits_omie,
            'preco_custo': preco_custo,
            'familias_omie': familias_omie,
            'bling_todos_produtos': bling_todos_produtos,
            'categorias_bling': categorias_bling,
            'produtos_vtrina': produtos_vtrina,
            'marketplaces_vtrina': marketplaces_vtrina,
        }


class AtualizaPlanilha:
    def __init__(self) -> None:
        self.planilha = 'Dados de API - Todos os Sistemas'

    def atualizar(self, dados):
        atualiza_planilha(self.planilha, 'produtos_omie', dados['omie_todos_produtos'])
        atualiza_planilha(self.planilha, 'kits_omie', dados['kits_omie'])
        atualiza_planilha(self.planilha, 'preco_custo', dados['preco_custo'])
        atualiza_planilha(self.planilha, 'familias_omie', dados['familias_omie'])
        atualiza_planilha(self.planilha, 'produtos_bling', dados['bling_todos_produtos'])
        atualiza_planilha(self.planilha, 'categorias_bling', dados['categorias_bling'])
        atualiza_planilha(self.planilha, 'produtos_vtrina', dados['produtos_vtrina'])
        atualiza_planilha(self.planilha, 'marketplaces_vtrina', dados['marketplaces_vtrina'])


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    coletor = ColetaDadosAPIs()
    dados = coletor.coletar_dados()

    atualizador = AtualizaPlanilha()
    atualizador.atualizar(dados)
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print(f"Tempo decorrido: {elapsed_time.total_seconds():.2f} segundos")

