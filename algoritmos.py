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

def resolver_ida_estrela(lab: Labirinto, inicio: Posicao, fim: Posicao) -> Tuple[Optional[Caminho], MetricasBusca]:
    """
    Implementa o algoritmo IDA* (Iterative Deepening A*).
    Retorna o caminho encontrado e as métricas da busca.
    """
    tempo_inicio = time.time()
    visitados = {inicio}  # Para métricas
    custos_acumulados = {inicio: 0}  # Para métricas
    
    def busca_recursiva(atual: Posicao, g: int, limite: int, caminho: List[Posicao], 
                       visitados_atual: Set[Posicao]) -> Tuple[Optional[Caminho], float]:
        """
        Função recursiva do IDA*.
        Retorna (caminho, novo_limite) se não encontrou solução,
        ou (caminho, -1) se encontrou solução.
        """
        f = g + heuristica_manhattan(atual, fim)
        
        # Se o custo total excede o limite, retorna o f como novo limite
        if f > limite:
            return None, f
        
        # Se chegou ao destino, retorna o caminho
        if atual == fim:
            return caminho, -1
        
        proximo_limite = float('inf')
        
        # Explora os vizinhos
        for prox_pos, custo in obter_vizinhos_com_custo(atual, lab):
            if prox_pos not in visitados_atual:
                visitados.add(prox_pos)  # Para métricas
                visitados_atual.add(prox_pos)
                novo_caminho = caminho + [prox_pos]
                custos_acumulados[prox_pos] = custos_acumulados[atual] + custo
                
                resultado, novo_limite = busca_recursiva(
                    prox_pos, g + custo, limite, novo_caminho, visitados_atual
                )
                
                if resultado is not None:
                    return resultado, -1
                
                if novo_limite < proximo_limite:
                    proximo_limite = novo_limite
                
                visitados_atual.remove(prox_pos)
        
        return None, proximo_limite
    
    # Começa com limite = h(inicio)
    limite = heuristica_manhattan(inicio, fim)
    caminho_inicial = [inicio]
    
    while True:
        resultado, novo_limite = busca_recursiva(inicio, 0, limite, caminho_inicial, {inicio})
        
        if resultado is not None:
            # Encontrou o caminho
            tempo_fim = time.time()
            metricas = coletar_metricas(
                resultado, custos_acumulados, visitados, tempo_inicio, tempo_fim,
                inicio, fim, "IDA*"
            )
            return resultado, metricas
        
        if novo_limite == float('inf'):
            # Não há caminho possível
            tempo_fim = time.time()
            metricas = coletar_metricas(
                None, custos_acumulados, visitados, tempo_inicio, tempo_fim,
                inicio, fim, "IDA*"
            )
            return None, metricas
        
        # Atualiza o limite para a próxima iteração
        limite = novo_limite 