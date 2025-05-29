from typing import Optional, List, Dict
from tabulate import tabulate

from constantes import *
from algoritmos import Labirinto, Posicao, MetricasBusca
from labirinto import (
    gerar_labirinto_prim, 
    marcar_caminho_no_labirinto, 
    imprimir_labirinto
)
from algoritmos import resolver_guloso, resolver_dfs, resolver_ida_estrela, resolver_a_estrela
from interface import (
    imprimir_cabecalho_labirinto, 
    imprimir_metricas,
    jogar_manualmente
)

def comparar_algoritmos(lab: Labirinto, inicio: Posicao, fim: Posicao) -> None:
    """Compara todos os algoritmos disponíveis e mostra uma tabela com os resultados."""
    algoritmos = {
        "A*": resolver_a_estrela,
        "Guloso": resolver_guloso,
        "DFS": resolver_dfs,
        "IDA*": resolver_ida_estrela
    }
    
    resultados = []
    
    # Executa cada algoritmo
    for nome, func in algoritmos.items():
        caminho, metricas = func(lab, inicio, fim)
        resultados.append({
            "Algoritmo": nome,
            "Encontrou Solução": "Sim" if metricas.caminho_encontrado else "Não",
            "Custo Total": metricas.custo_total,
            "Comprimento": metricas.comprimento_caminho,
            "Nós Visitados": metricas.nos_visitados,
            "Tempo (s)": f"{metricas.tempo_execucao:.4f}"
        })
    
    # Cria a tabela
    headers = ["Algoritmo", "Encontrou Solução", "Custo Total", "Comprimento", "Nós Visitados", "Tempo (s)"]
    table = [[r[h] for h in headers] for r in resultados]
    
    print("\nComparação dos Algoritmos:")
    print(tabulate(table, headers=headers, tablefmt="grid"))

def mostrar_menu_algoritmos() -> None:
    """Mostra o menu de algoritmos disponíveis."""
    print("\nAlgoritmos Disponíveis:")
    print("1. A* (A-Star)")
    print("2. Busca Gulosa")
    print("3. DFS (Busca em Profundidade)")
    print("4. IDA* (Iterative Deepening A*)")
    print("5. Voltar")

def main() -> None:
    """Função principal do jogo."""
    labirinto_atual: Optional[Labirinto] = None
    pos_inicio: Optional[Posicao] = None
    pos_fim: Optional[Posicao] = None
    total_moedas: int = 0
    contador_labirintos: int = 0

    while True:
        print("\n" + "=" * 80)  # Linha separadora
        if contador_labirintos > 0:
            print(f"LABIRINTO #{contador_labirintos}".center(80))
        else:
            print("NENHUM LABIRINTO GERADO".center(80))
        print("=" * 80)  # Linha separadora
        print("MENU PRINCIPAL".center(80))
        print("=" * 80 + "\n")  # Linha separadora

        print("Opções disponíveis:")
        print("1. Gerar Novo Labirinto")
        print("2. Sair")

        escolha = input("\nEscolha uma opção: ")
        print("\n" + "-" * 80)  # Linha separadora

        if escolha == "1":
            contador_labirintos += 1
            imprimir_cabecalho_labirinto(contador_labirintos)
            print("\nGerando novo labirinto...")
            labirinto_atual, pos_inicio, pos_fim, posicoes_moedas = gerar_labirinto_prim(ALTURA_LAB, LARGURA_LAB, 5)
            total_moedas = len(posicoes_moedas)
            print("\nLabirinto gerado:")
            imprimir_labirinto(labirinto_atual)

            # Submenu após gerar labirinto
            while True:
                print("\nOpções do Labirinto:")
                print("1. Jogar Manualmente")
                print("2. Ver Algoritmos Disponíveis")
                print("3. Comparar Todos os Algoritmos")
                print("4. Voltar ao Menu Principal")

                sub_escolha = input("\nEscolha uma opção: ")

                if sub_escolha == "1" and labirinto_atual:
                    imprimir_cabecalho_labirinto(contador_labirintos)
                    print("\nJogando manualmente...")
                    jogar_manualmente(labirinto_atual, pos_inicio, pos_fim, total_moedas)
                
                elif sub_escolha == "2":
                    while True:
                        mostrar_menu_algoritmos()
                        alg_escolha = input("\nEscolha um algoritmo (ou 5 para voltar): ")
                        
                        if alg_escolha == "1" and labirinto_atual:
                            print("\nResolvendo com A*...")
                            caminho, metricas = resolver_a_estrela(labirinto_atual, pos_inicio, pos_fim)
                            imprimir_metricas(metricas)
                            if caminho:
                                print("\nSolução encontrada:")
                                lab_resolvido = marcar_caminho_no_labirinto(labirinto_atual, caminho)
                                imprimir_labirinto(lab_resolvido)
                        
                        elif alg_escolha == "2" and labirinto_atual:
                            print("\nResolvendo com Busca Gulosa...")
                            caminho, metricas = resolver_guloso(labirinto_atual, pos_inicio, pos_fim)
                            imprimir_metricas(metricas)
                            if caminho:
                                print("\nSolução encontrada:")
                                lab_resolvido = marcar_caminho_no_labirinto(labirinto_atual, caminho)
                                imprimir_labirinto(lab_resolvido)
                        
                        elif alg_escolha == "3" and labirinto_atual:
                            print("\nResolvendo com DFS...")
                            caminho, metricas = resolver_dfs(labirinto_atual, pos_inicio, pos_fim)
                            imprimir_metricas(metricas)
                            if caminho:
                                print("\nSolução encontrada:")
                                lab_resolvido = marcar_caminho_no_labirinto(labirinto_atual, caminho)
                                imprimir_labirinto(lab_resolvido)
                        
                        elif alg_escolha == "4" and labirinto_atual:
                            print("\nResolvendo com IDA*...")
                            caminho, metricas = resolver_ida_estrela(labirinto_atual, pos_inicio, pos_fim)
                            imprimir_metricas(metricas)
                            if caminho:
                                print("\nSolução encontrada:")
                                lab_resolvido = marcar_caminho_no_labirinto(labirinto_atual, caminho)
                                imprimir_labirinto(lab_resolvido)
                        
                        elif alg_escolha == "5":
                            break
                        
                        else:
                            print("\nOpção inválida!")
                
                elif sub_escolha == "3" and labirinto_atual:
                    comparar_algoritmos(labirinto_atual, pos_inicio, pos_fim)
                
                elif sub_escolha == "4":
                    break
                
                else:
                    print("\nOpção inválida!")

        elif escolha == "2":
            print("\nSaindo...")
            break
        else:
            print("\nOpção inválida!")

if __name__ == "__main__":
    main() 