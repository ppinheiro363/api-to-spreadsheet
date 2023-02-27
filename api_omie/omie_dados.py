from omie import OmieAPI

omie_todos_produtos = OmieAPI().listar_todos_produtos()
omie_componentes_kit = OmieAPI().extrair_componentes(omie_todos_produtos)
omie_preco_custo = OmieAPI().calcular_preco_custo(omie_todos_produtos)
