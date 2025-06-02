# Labirinto com Algoritmos de Busca

**Conteúdo da Disciplina**: Algoritmos de Busca<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 21/1061897  |  Igor De Sousa Justino |
| 21/1061968  |  João Pedro Veras Gomes |

## Sobre 
Este projeto implementa um jogo de labirinto que compara diferentes algoritmos de resolução de labirintos gerados aleatoriamente. O labirinto é composto por muros e obstáculos com diferentes níveis de dificuldade. O projeto demonstra de forma prática a eficiência e características de diferentes algoritmos de busca na resolução de labirintos.

### Algoritmos Implementados
1. **A* (A-Star)**: Busca informada que combina heurística com custo do caminho para encontrar a solução ótima
2. **Dijkstra**: Algoritmo que encontra o caminho de menor custo considerando apenas os custos das células
3. **DFS (Busca em Profundidade)**: Explora um caminho até não poder mais avançar
4. **Busca Gulosa**: Algoritmo que sempre escolhe o movimento mais próximo do objetivo usando apenas heurística
5. **IDA* (Iterative Deepening A*)**: Combina DFS com A*, otimizando o uso de memória
6. **Best-First Search**: Algoritmo que balanceia heurística e custo do caminho, priorizando a direção do objetivo

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
- Biblioteca tabulate

### Comandos
```bash
# Clone o repositório
git clone 

# Entre na pasta do projeto
cd 

# Instale as dependências
pip install -r requirements.txt

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
- **Encontrou Solução**: Indica se o algoritmo encontrou um caminho válido
- **Comprimento do Caminho**: Número de passos na solução
- **Custo Total**: Soma dos custos de movimento (incluindo penalidades)
- **Nós Visitados**: Quantidade de posições exploradas
- **Tempo de Execução**: Tempo para encontrar a solução (em segundos)

### Regras do Jogo
- Colete todas as moedas antes de chegar ao final
- Barreiras causam recuo de 5 posições
- Cada movimento normal custa 1 ponto
- Cada colisão com barreira custa 6 pontos

### Características dos Algoritmos
- **A***: Garante o caminho ótimo, balanceando perfeitamente heurística e custo
- **Dijkstra**: Encontra o caminho de menor custo, ideal quando a heurística não é confiável
- **DFS**: Rápido, mas não garante o menor caminho
- **Busca Gulosa**: Rápido e direto ao objetivo, mas pode não encontrar o melhor caminho
- **IDA***: Combina eficiência de memória do DFS com otimalidade do A*
- **Best-First**: Balanceia velocidade e qualidade do caminho, priorizando a direção do objetivo
