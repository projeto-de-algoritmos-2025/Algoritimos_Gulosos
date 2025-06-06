import heapq
from typing import List, Tuple, Set, Dict, Optional
from dataclasses import dataclass
import time

from constantes import *

# Tipos personalizados
Labirinto = List[List[str]]
Posicao = Tuple[int, int]
Caminho = List[Posicao]
VizinhoCusto = Tuple[Posicao, int]  # (posição, custo)

@dataclass
class MetricasBusca:
    """Classe para armazenar as métricas de busca."""
    caminho_encontrado: bool
    custo_total: int  # Soma dos custos incluindo penalidades
    comprimento_caminho: int  # Número de passos sem contar recuos
    nos_visitados: int
    tempo_execucao: float
    distancia_heuristica: int
    algoritmo: str

def heuristica_manhattan(pos_a: Posicao, pos_b: Posicao) -> int:
    """Calcula a distância de Manhattan entre duas posições."""
    l1, c1 = pos_a
    l2, c2 = pos_b
    return abs(l1 - l2) + abs(c1 - c2)

def esta_dentro_limites(pos: Posicao, altura: int, largura: int) -> bool:
    """Verifica se uma posição está dentro dos limites do labirinto."""
    linha, coluna = pos
    return 0 <= linha < altura and 0 <= coluna < largura

def obter_vizinhos_com_custo(pos: Posicao, lab: Labirinto) -> List[VizinhoCusto]:
    """Retorna as posições vizinhas válidas e seus custos."""
    linha, coluna = pos
    vizinhos = []
    direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # direita, baixo, esquerda, cima
    
    for dl, dc in direcoes:
        nova_linha, nova_coluna = linha + dl, coluna + dc
        nova_pos = (nova_linha, nova_coluna)
        
        if esta_dentro_limites(nova_pos, len(lab), len(lab[0])):
            if lab[nova_linha][nova_coluna] != PAREDE:
                # Define o custo baseado no tipo de célula
                custo = CUSTO_BARREIRA if lab[nova_linha][nova_coluna] == BARREIRA else CUSTO_NORMAL
                vizinhos.append((nova_pos, custo))
    
    return vizinhos

def coletar_metricas(
    caminho: Optional[Caminho],
    custos_acumulados: Dict[Posicao, int],
    visitados: Set[Posicao],
    tempo_inicio: float,
    tempo_fim: float,
    pos_inicio: Posicao,
    pos_fim: Posicao,
    algoritmo: str
) -> MetricasBusca:
    """Coleta e retorna as métricas de busca."""
    custo_total = custos_acumulados.get(pos_fim, 0) if caminho else 0
    return MetricasBusca(
        caminho_encontrado=caminho is not None,
        custo_total=custo_total,
        comprimento_caminho=len(caminho) if caminho else 0,
        nos_visitados=len(visitados),
        tempo_execucao=tempo_fim - tempo_inicio,
        distancia_heuristica=heuristica_manhattan(pos_inicio, pos_fim),
        algoritmo=algoritmo
    )

def resolver_a_estrela(lab: Labirinto, inicio: Posicao, fim: Posicao) -> Tuple[Optional[Caminho], MetricasBusca]:
    """
    Implementa o algoritmo A* (A-Star).
    Retorna o caminho encontrado e as métricas da busca.
    """
    tempo_inicio = time.time()
    
    # Fila de prioridade: (f, g, posição)
    fronteira = [(heuristica_manhattan(inicio, fim), 0, inicio)]
    veio_de = {inicio: None}  # Dicionário para reconstruir o caminho
    custo_ate = {inicio: 0}  # g(n): custos acumulados
    visitados = {inicio}  # Conjunto de posições já visitadas
    
    while fronteira:
        _, g_atual, atual = heapq.heappop(fronteira)
        
        if atual == fim:
            # Reconstrói o caminho
            caminho = []
            pos_atual = atual
            while pos_atual:
                caminho.append(pos_atual)
                pos_atual = veio_de[pos_atual]
            caminho = list(reversed(caminho))
            
            tempo_fim = time.time()
            metricas = coletar_metricas(
                caminho, custo_ate, visitados, tempo_inicio, tempo_fim,
                inicio, fim, "A*"
            )
            return caminho, metricas
        
        # Explora os vizinhos
        for prox_pos, custo_movimento in obter_vizinhos_com_custo(atual, lab):
            novo_g = g_atual + custo_movimento
            
            if prox_pos not in custo_ate or novo_g < custo_ate[prox_pos]:
                visitados.add(prox_pos)
                custo_ate[prox_pos] = novo_g
                veio_de[prox_pos] = atual
                f = novo_g + heuristica_manhattan(prox_pos, fim)
                heapq.heappush(fronteira, (f, novo_g, prox_pos))
    
    tempo_fim = time.time()
    metricas = coletar_metricas(
        None, custo_ate, visitados, tempo_inicio, tempo_fim,
        inicio, fim, "A*"
    )
    return None, metricas

def resolver_guloso(lab: Labirinto, inicio: Posicao, fim: Posicao) -> Tuple[Optional[Caminho], MetricasBusca]:
    """
    Implementa o algoritmo de Busca Gulosa (Greedy Best-First Search).
    Retorna o caminho encontrado e as métricas da busca.
    """
    tempo_inicio = time.time()
    
    fronteira = [(heuristica_manhattan(inicio, fim), inicio)]
    veio_de = {inicio: None}  # Dicionário para reconstruir o caminho
    custo_ate = {inicio: 0}  # Para métricas
    visitados = {inicio}  # Conjunto de posições já visitadas
    
    while fronteira:
        _, atual = heapq.heappop(fronteira)
        
        if atual == fim:
            # Reconstrói o caminho e calcula o custo real
            caminho = []
            pos_atual = atual
            custo_total = 0
            pos_anterior = None
            
            while pos_atual:
                caminho.append(pos_atual)
                if pos_anterior:
                    # Calcula o custo real do movimento
                    custo = (CUSTO_BARREIRA if lab[pos_anterior[0]][pos_anterior[1]] == BARREIRA 
                            else CUSTO_NORMAL)
                    custo_total += custo
                pos_anterior = pos_atual
                pos_atual = veio_de[pos_anterior]
            
            caminho = list(reversed(caminho))
            custo_ate[fim] = custo_total
            
            tempo_fim = time.time()
            metricas = coletar_metricas(
                caminho, custo_ate, visitados, tempo_inicio, tempo_fim,
                inicio, fim, "Gulosa"
            )
            return caminho, metricas
        
        # Explora os vizinhos ignorando custos
        for prox_pos, _ in obter_vizinhos_com_custo(atual, lab):
            if prox_pos not in visitados:
                visitados.add(prox_pos)
                veio_de[prox_pos] = atual
                prioridade = heuristica_manhattan(prox_pos, fim)
                heapq.heappush(fronteira, (prioridade, prox_pos))
    
    tempo_fim = time.time()
    metricas = coletar_metricas(
        None, custo_ate, visitados, tempo_inicio, tempo_fim,
        inicio, fim, "Gulosa"
    )
    return None, metricas

def resolver_dfs(lab: Labirinto, inicio: Posicao, fim: Posicao) -> Tuple[Optional[Caminho], MetricasBusca]:
    """
    Implementa o algoritmo de Busca em Profundidade (DFS).
    Retorna o caminho encontrado e as métricas da busca.
    """
    tempo_inicio = time.time()
    
    pilha = [(inicio, [inicio])]  # (posição_atual, caminho_até_aqui)
    visitados = {inicio}
    custos_acumulados = {inicio: 0}  # Para métricas
    
    while pilha:
        atual, caminho = pilha.pop()
        
        if atual == fim:
            tempo_fim = time.time()
            metricas = coletar_metricas(
                caminho, custos_acumulados, visitados, tempo_inicio, tempo_fim,
                inicio, fim, "DFS"
            )
            return caminho, metricas
        
        # Explora os vizinhos
        for prox_pos, custo in obter_vizinhos_com_custo(atual, lab):
            linha, coluna = prox_pos
            if prox_pos not in visitados:
                visitados.add(prox_pos)
                novo_caminho = list(caminho)
                novo_caminho.append(prox_pos)
                custos_acumulados[prox_pos] = custos_acumulados[atual] + custo
                pilha.append((prox_pos, novo_caminho))
    
    tempo_fim = time.time()
    metricas = coletar_metricas(
        None, custos_acumulados, visitados, tempo_inicio, tempo_fim,
        inicio, fim, "DFS"
    )
    return None, metricas

def resolver_dijkstra(lab: Labirinto, inicio: Posicao, fim: Posicao) -> Tuple[Optional[Caminho], MetricasBusca]:
    """
    Implementa o algoritmo de Dijkstra.
    Retorna o caminho encontrado e as métricas da busca.
    """
    tempo_inicio = time.time()
    
    # Fila de prioridade: (custo_acumulado, posição)
    fronteira = [(0, inicio)]
    veio_de = {inicio: None}  # Dicionário para reconstruir o caminho
    custo_ate = {inicio: 0}  # Custos acumulados até cada posição
    visitados = {inicio}  # Conjunto de posições já visitadas
    
    while fronteira:
        custo_atual, atual = heapq.heappop(fronteira)
        
        if atual == fim:
            # Reconstrói o caminho
            caminho = []
            pos_atual = atual
            while pos_atual:
                caminho.append(pos_atual)
                pos_atual = veio_de[pos_atual]
            caminho = list(reversed(caminho))
            
            tempo_fim = time.time()
            metricas = coletar_metricas(
                caminho, custo_ate, visitados, tempo_inicio, tempo_fim,
                inicio, fim, "Dijkstra"
            )
            return caminho, metricas
        
        # Explora os vizinhos
        for prox_pos, custo_movimento in obter_vizinhos_com_custo(atual, lab):
            novo_custo = custo_atual + custo_movimento
            
            if prox_pos not in custo_ate or novo_custo < custo_ate[prox_pos]:
                visitados.add(prox_pos)
                custo_ate[prox_pos] = novo_custo
                veio_de[prox_pos] = atual
                heapq.heappush(fronteira, (novo_custo, prox_pos))
    
    tempo_fim = time.time()
    metricas = coletar_metricas(
        None, custo_ate, visitados, tempo_inicio, tempo_fim,
        inicio, fim, "Dijkstra"
    )
    return None, metricas 

def resolver_best_first_search(lab: Labirinto, inicio: Posicao, fim: Posicao) -> Tuple[Optional[Caminho], MetricasBusca]:
    """
    Implementa o algoritmo Best-First Search.
    Retorna o caminho encontrado e as métricas da busca.
    """
    tempo_inicio = time.time()
    
    # Fila de prioridade: (heurística + custo_acumulado/2, posição)
    fronteira = [(heuristica_manhattan(inicio, fim), inicio)]
    veio_de = {inicio: None}  # Dicionário para reconstruir o caminho
    custo_ate = {inicio: 0}  # Para métricas
    visitados = {inicio}  # Conjunto de posições já visitadas
    
    while fronteira:
        _, atual = heapq.heappop(fronteira)
        
        if atual == fim:
            # Reconstrói o caminho e calcula o custo real
            caminho = []
            pos_atual = atual
            custo_total = 0
            pos_anterior = None
            
            while pos_atual:
                caminho.append(pos_atual)
                if pos_anterior:
                    # Calcula o custo real do movimento
                    for vizinho, custo in obter_vizinhos_com_custo(pos_anterior, lab):
                        if vizinho == pos_atual:
                            custo_total += custo
                            break
                pos_anterior = pos_atual
                pos_atual = veio_de[pos_anterior]
            
            caminho = list(reversed(caminho))
            custo_ate[fim] = custo_total
            
            tempo_fim = time.time()
            metricas = coletar_metricas(
                caminho, custo_ate, visitados, tempo_inicio, tempo_fim,
                inicio, fim, "Best-First"
            )
            return caminho, metricas
        
        # Explora os vizinhos considerando tanto a heurística quanto o custo
        for prox_pos, custo_movimento in obter_vizinhos_com_custo(atual, lab):
            if prox_pos not in visitados:
                visitados.add(prox_pos)
                veio_de[prox_pos] = atual
                custo_ate[prox_pos] = custo_ate[atual] + custo_movimento
                
                # Combina heurística com custo acumulado para melhor estimativa
                h = heuristica_manhattan(prox_pos, fim)
                g = custo_ate[prox_pos]
                prioridade = h + g/2  # Dá mais peso à heurística que ao custo
                
                heapq.heappush(fronteira, (prioridade, prox_pos))
    
    tempo_fim = time.time()
    metricas = coletar_metricas(
        None, custo_ate, visitados, tempo_inicio, tempo_fim,
        inicio, fim, "Best-First"
    )
    return None, metricas 