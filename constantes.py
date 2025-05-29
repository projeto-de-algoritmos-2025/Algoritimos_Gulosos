from colorama import Fore, Back, Style

# Dimensões do labirinto
LARGURA_LAB = 80
ALTURA_LAB = 20

# Caracteres do labirinto com cores
PAREDE = f'{Fore.LIGHTBLUE_EX}▓{Style.BRIGHT}{Style.RESET_ALL}'  # Parede azul brilhante
CAMINHO = ' '  # Espaço em branco
INICIO = f'{Fore.LIGHTGREEN_EX}✖{Style.BRIGHT}{Style.RESET_ALL}'  # Início verde brilhante
FIM = f'{Fore.LIGHTRED_EX}🏁{Style.BRIGHT}{Style.RESET_ALL}'  # Fim vermelho brilhante
JOGADOR = f'{Fore.LIGHTYELLOW_EX}◎{Style.BRIGHT}{Style.RESET_ALL}'  # Jogador amarelo brilhante
CAMINHO_SOLUCAO = f'{Fore.LIGHTRED_EX}*{Style.BRIGHT}{Style.RESET_ALL}'  # Solução vermelho brilhante
VISITADO_BUSCA = f'{Fore.WHITE}·{Style.BRIGHT}{Style.RESET_ALL}'  # Visitados branco brilhante
MOEDA = f'{Fore.LIGHTYELLOW_EX}★{Style.BRIGHT}{Style.RESET_ALL}'  # Moeda amarelo brilhante
BARREIRA = f'{Fore.LIGHTMAGENTA_EX}⦰{Style.BRIGHT}{Style.RESET_ALL}'  # Barreira magenta brilhante

# Custos de movimento
CUSTO_NORMAL = 1
CUSTO_BARREIRA = 6  # 1 passo + 5 de penalidade
RECUO_BARREIRA = 5  # Quantidade de passos para recuar

# Direções de movimento
CIMA = 'w'
BAIXO = 's'
ESQUERDA = 'a'
DIREITA = 'd'

# Cores para o placar e mensagens
COR_TITULO = Fore.LIGHTCYAN_EX
COR_DESTAQUE = Fore.LIGHTYELLOW_EX
COR_ERRO = Fore.LIGHTRED_EX
COR_SUCESSO = Fore.LIGHTGREEN_EX
COR_INFO = Fore.LIGHTWHITE_EX
RESET_COR = Style.RESET_ALL 