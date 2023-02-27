from api_omie.omie import OmieAPI
from api_bling.bling import BlingAPI
from api_vtrina.vtrina import VtrinaAPI

from gspread_config.scope import atualiza_planilha


class InsereOmieProdutos:
    def __init__(self) -> None:
        self.omie = OmieAPI()
        self.omie_todos_produtos = self.omie.listar_todos_produtos()
        self.planilha = 'Novo Gspread Teste'
        self.insere_produtos_omie()
        self.insere_kits_omie()
        self.insere_preco_custo()
        self.insere_familias()

    def insere_produtos_omie(self) -> None:
        return atualiza_planilha(self.planilha, 'produtos_omie', self.omie_todos_produtos)

    def insere_kits_omie(self) -> None:
        return atualiza_planilha(self.planilha, 'kits_omie', self.omie.extrair_componentes(self.omie_todos_produtos))

    def insere_preco_custo(self) -> None:
        return atualiza_planilha(self.planilha, 'preco_custo', self.omie.calcular_preco_custo(self.omie_todos_produtos))
    
    def insere_familias(self) -> None:
        return atualiza_planilha(self.planilha, 'familias_omie', self.omie.listar_familias())


class InsereBlingProdutos:
    def __init__(self) -> None:
        self.bling = BlingAPI()
        self.bling_todos_produtos = self.bling.pegar_todos_produtos()
        self.planilha = 'Novo Gspread Teste'
        self.insere_produtos_bling()
        self.insere_categoria()

    def insere_produtos_bling(self) -> None:
        return atualiza_planilha(self.planilha, 'produtos_bling', self.bling_todos_produtos)
    
    def insere_categoria(self) -> None:
        return atualiza_planilha(self.planilha, 'categorias_bling', self.bling.listar_categorias())
    

class InsereVtrinaProdutos:
    def __init__(self) -> None:
        self.vtrina = VtrinaAPI()
        self.planilha = 'Novo Gspread Teste'
        self.insere_produtos_vtrina()
    
    def insere_produtos_vtrina(self) -> None:
        return atualiza_planilha(self.planilha, 'produtos_vtrina', self.vtrina.lista_todos_produtos())

# start = InsereOmieProdutos()

# start2 =  InsereBlingProdutos()

start3 = InsereVtrinaProdutos()

