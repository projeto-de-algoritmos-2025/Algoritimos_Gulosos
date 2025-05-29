import os
import sys
import termios
import tty
from typing import Optional, List, Tuple

from constantes import *
from algoritmos import Labirinto, Posicao, MetricasBusca
from labirinto import imprimir_labirinto

def limpar_tela() -> None:
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_key() -> str:
    """Lê uma única tecla do terminal sem necessidade de Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def imprimir_cabecalho_labirinto(numero_labirinto: int) -> None:
    """Imprime o cabeçalho do labirinto com cores."""
    print(f"\n{COR_TITULO}{'=' * 40}")
    print(f"LABIRINTO #{numero_labirinto}".center(40))
    print(f"{'=' * 40}{RESET_COR}")

def imprimir_metricas(metricas) -> None:
    """Imprime as métricas da busca com cores."""
    print(f"\n{COR_TITULO}{'=' * 40}")
    print(f"Resultados da Busca {metricas.algoritmo}")
    print(f"{'=' * 40}{RESET_COR}")
    
    encontrado = f"{COR_SUCESSO}Sim{RESET_COR}" if metricas.caminho_encontrado else f"{COR_ERRO}Não{RESET_COR}"
    print(f"✓ Caminho encontrado: {encontrado}")
    print(f"✓ Comprimento do caminho: {COR_DESTAQUE}{metricas.comprimento_caminho} passos{RESET_COR}")
    print(f"✓ Nós visitados: {COR_INFO}{metricas.nos_visitados}{RESET_COR}")
    print(f"✓ Tempo de execução: {COR_INFO}{metricas.tempo_execucao:.4f} segundos{RESET_COR}")
    print(f"✓ Distância heurística (Manhattan): {COR_INFO}{metricas.distancia_heuristica}{RESET_COR}")
    
    print(f"{COR_TITULO}{'=' * 40}{RESET_COR}")

def imprimir_placar(moedas_coletadas: int, total_moedas: int, passos: int) -> None:
    """Imprime o placar do jogo com cores."""
    print(f"\n{COR_TITULO}{'=' * 40}")
    print("PLACAR".center(40))
    print(f"{'=' * 40}{RESET_COR}")
    print(f"Moedas: {COR_DESTAQUE}{moedas_coletadas}/{total_moedas}{RESET_COR}")
    print(f"Passos: {COR_INFO}{passos}{RESET_COR}")
    print(f"{COR_TITULO}{'=' * 40}{RESET_COR}")

def jogar_manualmente(lab: List[List[str]], pos_inicio: Tuple[int, int], 
                     pos_fim: Tuple[int, int], total_moedas: int) -> None:
    """Permite jogar o labirinto manualmente."""
    from copy import deepcopy
    
    # Inicializa o estado do jogo
    lab_jogo = deepcopy(lab)
    pos_atual = pos_inicio
    movimentos = 0
    moedas_coletadas = 0
    historico_posicoes = [pos_inicio]
    
    print("\nUse WASD para mover, Q para sair")
    
    while True:
        # Limpa a tela
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Atualiza o labirinto
        char_atual = lab_jogo[pos_atual[0]][pos_atual[1]]
        if char_atual == MOEDA:
            moedas_coletadas += 1
            lab_jogo[pos_atual[0]][pos_atual[1]] = CAMINHO
            print("\nMoeda coletada!")
        
        # Mostra o jogador
        lab_jogo[pos_atual[0]][pos_atual[1]] = JOGADOR
        
        # Mostra o estado
        print(f"\nMovimentos: {movimentos}")
        print(f"Moedas: {moedas_coletadas}/{total_moedas}")
        imprimir_labirinto(lab_jogo)
        
        # Restaura o estado
        lab_jogo[pos_atual[0]][pos_atual[1]] = (CAMINHO if char_atual == MOEDA else char_atual)
        
        # Verifica vitória
        if pos_atual == pos_fim and moedas_coletadas == total_moedas:
            print(f"\nParabéns! Você venceu em {movimentos} movimentos!")
            break
        
        # Lê movimento
        movimento = get_key().lower()
        
        if movimento == 'q':
            print("\nJogo encerrado!")
            break
        
        # Processa movimento
        nova_pos = pos_atual
        if movimento == CIMA and pos_atual[0] > 0:
            nova_pos = (pos_atual[0] - 1, pos_atual[1])
        elif movimento == BAIXO and pos_atual[0] < len(lab) - 1:
            nova_pos = (pos_atual[0] + 1, pos_atual[1])
        elif movimento == ESQUERDA and pos_atual[1] > 0:
            nova_pos = (pos_atual[0], pos_atual[1] - 1)
        elif movimento == DIREITA and pos_atual[1] < len(lab[0]) - 1:
            nova_pos = (pos_atual[0], pos_atual[1] + 1)
        
        # Verifica movimento
        if lab[nova_pos[0]][nova_pos[1]] != PAREDE:
            pos_atual = nova_pos
            historico_posicoes.append(pos_atual)
            
            if lab[nova_pos[0]][nova_pos[1]] == BARREIRA:
                print("\nBarreira! Recuando...")
                recuo = min(RECUO_BARREIRA, len(historico_posicoes) - 1)
                for _ in range(recuo):
                    historico_posicoes.pop()
                pos_atual = historico_posicoes[-1]
                movimentos += CUSTO_BARREIRA
            else:
                movimentos += CUSTO_NORMAL 