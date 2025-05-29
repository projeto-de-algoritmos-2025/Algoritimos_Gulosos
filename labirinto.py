import random
from typing import List, Tuple, Optional

from constantes import *
from algoritmos import Labirinto, Posicao, Caminho, esta_dentro_limites

def imprimir_labirinto(lab: Labirinto) -> None:
    """Imprime o labirinto no terminal."""
    for linha in lab:
        print("".join(linha))
    print("█" * len(lab[0]))

def existe_caminho(lab: Labirinto, inicio: Posicao, destino: Posicao, considerar_barreiras: bool = False) -> bool:
    """Verifica se existe um caminho entre dois pontos no labirinto."""
    if inicio == destino:
        return True
        
    visitados = {inicio}
    fila = [inicio]
    
    while fila:
        atual = fila.pop(0)
        
        for dl, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # direita, baixo, esquerda, cima
            prox_lin = atual[0] + dl
            prox_col = atual[1] + dc
            prox_pos = (prox_lin, prox_col)
            
            if (esta_dentro_limites(prox_pos, len(lab), len(lab[0])) and
                prox_pos not in visitados):
                
                # Se estamos considerando barreiras, elas são tratadas como paredes
                if considerar_barreiras:
                    if lab[prox_lin][prox_col] in [PAREDE, BARREIRA]:
                        continue
                else:
                    if lab[prox_lin][prox_col] == PAREDE:
                        continue
                
                if prox_pos == destino:
                    return True
                    
                visitados.add(prox_pos)
                fila.append(prox_pos)
    
    return False

def adicionar_caminhos_extras(lab: Labirinto, chance_remover_parede: float = 0.3) -> None:
    """
    Adiciona caminhos extras ao labirinto removendo algumas paredes aleatoriamente.
    
    Args:
        lab: O labirinto a ser modificado
        chance_remover_parede: Probabilidade de remover uma parede (entre 0 e 1)
    """
    altura = len(lab)
    largura = len(lab[0])
    
    # Percorre o labirinto procurando paredes que podem ser removidas
    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            if lab[i][j] == PAREDE:
                # Conta quantos caminhos existem ao redor desta parede
                caminhos_adjacentes = 0
                paredes_adjacentes = 0
                
                for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    if lab[i + di][j + dj] == CAMINHO:
                        caminhos_adjacentes += 1
                    elif lab[i + di][j + dj] == PAREDE:
                        paredes_adjacentes += 1
                
                # Só remove a parede se:
                # 1. Tiver pelo menos 2 paredes adjacentes (para manter estrutura)
                # 2. Tiver no máximo 2 caminhos adjacentes (para evitar muito espaço aberto)
                # 3. Passar no teste de probabilidade
                if (paredes_adjacentes >= 2 and caminhos_adjacentes <= 2 and 
                    random.random() < chance_remover_parede):
                    lab[i][j] = CAMINHO

def marcar_caminho_no_labirinto(lab_original: Labirinto, caminho: Caminho, char_caminho: str = CAMINHO_SOLUCAO) -> Labirinto:
    """Marca o caminho encontrado no labirinto."""
    lab_copia = [linha[:] for linha in lab_original]
    
    for l, c in caminho:
        if lab_copia[l][c] not in {INICIO, FIM}:
            lab_copia[l][c] = char_caminho
    
    return lab_copia

def gerar_labirinto_prim(altura: int, largura: int, num_moedas: int = 5) -> Tuple[Labirinto, Posicao, Posicao, List[Posicao]]:
    """
    Gera um labirinto usando o algoritmo de Prim modificado.
    Retorna o labirinto, as posições de início e fim e as posições das moedas.
    
    Args:
        altura: Altura do labirinto
        largura: Largura do labirinto
        num_moedas: Número de moedas a serem colocadas
    """
    # Inicializa o labirinto com paredes
    lab = [[PAREDE for _ in range(largura)] for _ in range(altura)]
    
    # Escolhe uma célula inicial (sempre em posição ímpar para manter a estrutura)
    lin_atual = random.randrange(1, altura - 1, 2)
    col_atual = random.randrange(1, largura - 1, 2)
    lab[lin_atual][col_atual] = CAMINHO
    
    # Lista de muros fronteira (muro, célula_adjacente)
    muros_fronteira = []
    
    def adicionar_muros_fronteira(lin: int, col: int) -> None:
        """Adiciona muros adjacentes à célula atual à lista de fronteira."""
        direcoes = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # direita, baixo, esquerda, cima
        for dl, dc in direcoes:
            lin_adj = lin + dl
            col_adj = col + dc
            if esta_dentro_limites((lin_adj, col_adj), altura, largura):
                # O muro está entre a célula atual e a adjacente
                lin_muro = lin + dl // 2
                col_muro = col + dc // 2
                muros_fronteira.append((lin_muro, col_muro, lin_adj, col_adj))
    
    # Adiciona os muros iniciais
    adicionar_muros_fronteira(lin_atual, col_atual)
    
    # Enquanto houver muros na fronteira
    while muros_fronteira:
        # Escolhe um muro aleatório
        idx_muro = random.randrange(len(muros_fronteira))
        lin_m, col_m, lin_a, col_a = muros_fronteira.pop(idx_muro)
        
        # Se a célula adjacente ainda for parede
        if lab[lin_a][col_a] == PAREDE:
            # Remove o muro (transforma em caminho)
            lab[lin_m][col_m] = CAMINHO
            lab[lin_a][col_a] = CAMINHO
            # Adiciona os novos muros fronteira
            adicionar_muros_fronteira(lin_a, col_a)
    
    # Adiciona caminhos extras para tornar o labirinto mais aberto
    adicionar_caminhos_extras(lab, chance_remover_parede=0.4)  # Aumentei a chance de remover paredes
    
    # Escolhe pontos de início e fim aleatoriamente entre os caminhos disponíveis
    caminhos_disponiveis = [(i, j) for i in range(altura) for j in range(largura) 
                           if lab[i][j] == CAMINHO]
    
    # Tenta encontrar pontos de início e fim que tenham um caminho válido entre eles
    max_tentativas = 50
    for _ in range(max_tentativas):
        inicio, fim = random.sample(caminhos_disponiveis, 2)
        if existe_caminho(lab, inicio, fim):
            break
    else:
        # Se não encontrou após várias tentativas, cria um caminho direto
        inicio = random.choice(caminhos_disponiveis)
        fim = random.choice(caminhos_disponiveis)
        caminho_direto = criar_caminho_direto(lab, inicio, fim)
    
    # Adiciona barreiras com menor frequência e conta colisões
    colisoes_barreiras = 0
    chance_barreira = 0.05  # Reduzido ainda mais
    max_barreiras = (altura * largura) // 40  # Limita o número máximo de barreiras
    barreiras_adicionadas = 0
    
    caminhos_para_barreiras = [(i, j) for i in range(altura) for j in range(largura) 
                              if lab[i][j] == CAMINHO]
    random.shuffle(caminhos_para_barreiras)
    
    for i, j in caminhos_para_barreiras:
        if barreiras_adicionadas >= max_barreiras:
            break
            
        if random.random() < chance_barreira:
            # Testa se ainda existe caminho considerando barreiras como bloqueios
            lab[i][j] = BARREIRA
            if not existe_caminho(lab, inicio, fim, considerar_barreiras=True):
                # Se não existir caminho, desfaz a barreira e conta colisão
                lab[i][j] = CAMINHO
                colisoes_barreiras += 1
            else:
                barreiras_adicionadas += 1
    
    print(f"Total de colisões de barreiras: {colisoes_barreiras}")
    print(f"Total de barreiras adicionadas: {barreiras_adicionadas}")
    
    # Marca início e fim no labirinto
    lab[inicio[0]][inicio[1]] = INICIO
    lab[fim[0]][fim[1]] = FIM
    
    # Gerar moedas em posições acessíveis
    posicoes_moedas = []
    caminhos_disponiveis = [(i, j) for i in range(altura) for j in range(largura) 
                           if lab[i][j] == CAMINHO]
    random.shuffle(caminhos_disponiveis)
    
    # Tenta colocar moedas garantindo que todas sejam acessíveis
    for _ in range(min(num_moedas, len(caminhos_disponiveis))):
        for pos_candidata in caminhos_disponiveis[:]:
            # Verifica se é possível alcançar a moeda do início
            if existe_caminho(lab, inicio, pos_candidata):
                lab[pos_candidata[0]][pos_candidata[1]] = MOEDA
                posicoes_moedas.append(pos_candidata)
                caminhos_disponiveis.remove(pos_candidata)
                break
    
    return lab, inicio, fim, posicoes_moedas

def criar_caminho_direto(lab: Labirinto, inicio: Posicao, fim: Posicao) -> None:
    """Cria um caminho direto entre dois pontos no labirinto."""
    x1, y1 = inicio
    x2, y2 = fim
    
    # Primeiro move horizontalmente
    for y in range(min(y1, y2), max(y1, y2) + 1):
        lab[x1][y] = CAMINHO
    
    # Depois move verticalmente
    for x in range(min(x1, x2), max(x1, x2) + 1):
        lab[x][y2] = CAMINHO 