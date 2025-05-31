# Labirinto com Algoritmos de Busca

**Conteúdo da Disciplina**: Algoritmos Gulosos<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 21/1061897  |  Igor De Sousa Justino |
| 21/1061968  |  João Pedro Veras Gomes |

## Sobre 
Este projeto implementa um jogo de labirinto que compara diferentes algoritmos de resolução de labirintos gerados aleatoriamente. O labirinto é composto por muros e obstáculos com diferentes níveis de dificuldade. O projeto demonstra de forma prática a vantagem do uso de algoritmos gulosos para otimização da computação de soluções de labirintos.

### Algoritmos Implementados
1. **A* (A-Star)**: Busca informada que usa heurística para encontrar o caminho mais curto
2. **Busca Gulosa**: Algoritmo que sempre escolhe o movimento mais próximo do objetivo
3. **DFS (Busca em Profundidade)**: Explora um caminho até não poder mais avançar
4. **IDA* (Iterative Deepening A*)**: Combina DFS com A*, otimizando o uso de memória

## Screenshots
- Tela inicial do jogo
- Labirinto em execução
- Comparação entre algoritmos

## Instalação 
**Linguagem**: Python<br>
**Framework**: N/A<br>

### Pré-requisitos
- Python 3.6 ou superior
- Biblioteca colorama

### Comandos
```bash
# Clone o repositório
git clone 

# Entre na pasta do projeto
cd 

# Instale as dependências
pip install colorama

# Execute o projeto
python main.py
```

## Uso 
Após executar o projeto, você terá acesso ao menu principal com as seguintes opções:

1. **Gerar Novo Labirinto**: Cria um novo labirinto para jogar
2. **Sair**: Encerra o programa

Ao gerar um novo labirinto, você pode:
- Jogar manualmente usando as teclas WASD
- Ver soluções usando diferentes algoritmos
- Comparar o desempenho dos algoritmos

### Controles do Jogo
- **W**: Mover para cima
- **A**: Mover para a esquerda
- **S**: Mover para baixo
- **D**: Mover para a direita
- **Q**: Sair do jogo

### Elementos do Jogo
- ✖ (Verde): Ponto de início
- 🏁 (Vermelho): Ponto de chegada
- ◎ (Amarelo): Jogador
- ★ (Amarelo): Moedas para coletar
- ⦰ (Magenta): Barreiras (causam recuo)
- ▓ (Azul): Paredes do labirinto

## Outros 
### Métricas de Comparação
Os algoritmos são comparados usando as seguintes métricas:
- **Comprimento do Caminho**: Número de passos na solução
- **Custo Total**: Soma dos custos de movimento (incluindo penalidades)
- **Nós Visitados**: Quantidade de posições exploradas
- **Tempo de Execução**: Tempo para encontrar a solução (em segundos)

### Regras do Jogo
- Colete todas as moedas antes de chegar ao final
- Barreiras causam recuo de 5 posições
- Cada movimento normal custa 1 ponto
- Cada colisão com barreira custa 6 pontos 
>>>>>>> f217235 (arquivos)
