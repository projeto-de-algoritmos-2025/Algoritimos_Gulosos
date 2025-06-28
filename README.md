# Visualizador de Algoritmos de Dividir e Conquistar

**Conteúdo da Disciplina**: Projetos e Algoritmos - Algoritmos de Dividir e Conquistar<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 21/1061897  |  Igor De Sousa Justino |
| 21/1061968  |  João Pedro Veras Gomes |

## Sobre 
Este projeto implementa um visualizador educacional que demonstra algoritmos clássicos de **Dividir e Conquistar** com execução passo a passo. O programa permite executar e visualizar o funcionamento de três algoritmos fundamentais, mostrando como os dados são divididos recursivamente, o processo de conquista dos subproblemas e a combinação dos resultados, além de contar operações e analisar complexidade.

## Algoritmos Implementados

1. **Contagem de Inversões**
   * Algoritmo que conta o número de inversões em um array utilizando a técnica de dividir e conquistar.
   * Utiliza o algoritmo de merge sort modificado para contar inversões durante o processo de merge.
   * **Complexidade**: O(n log n) tempo, O(n) espaço.
   * Mostra passo a passo as divisões do array e como as inversões são detectadas.
   * Útil para medir o quão "fora de ordem" um array está.

2. **Mediana das Medianas**
   * Algoritmo determinístico para encontrar a mediana de um conjunto não ordenado.
   * Divide o array em grupos de 5 elementos, encontra a mediana de cada grupo.
   * Recursivamente encontra a mediana das medianas para garantir boa pivotagem.
   * **Complexidade**: O(n) tempo no pior caso, O(log n) espaço.
   * Demonstra como garantir performance linear mesmo no pior caso.

3. **Par de Pontos Mais Próximos**
   * Encontra o par de pontos com menor distância euclidiana em um plano.
   * Divide os pontos pela coordenada x, resolve recursivamente em cada metade.
   * Combina as soluções verificando pontos próximos à linha divisória.
   * **Complexidade**: O(n log n) tempo, O(n) espaço.
   * Mostra como dividir problemas geométricos e combinar soluções eficientemente.

---

### Resumo Comparativo

| Algoritmo                    | Paradigma        | Complexidade Tempo | Complexidade Espaço | Comentário                                                    |
| ---------------------------- | ---------------- | ------------------ | ------------------- | ------------------------------------------------------------- |
| **Contagem de Inversões**    | Dividir/Conquistar | O(n log n)        | O(n)                | Eficiente para medir desordem em arrays.                     |
| **Mediana das Medianas**     | Dividir/Conquistar | O(n)              | O(log n)            | Garantia de tempo linear no pior caso.                       |
| **Par Mais Próximo**         | Dividir/Conquistar | O(n log n)        | O(n)                | Otimiza problemas geométricos com divisão inteligente.       |

## Instalação 
**Linguagem**: Python<br>
**Framework**: N/A<br>

### Pré-requisitos
- Python 3.6 ou superior
- Módulos padrão: math

### Comandos
```bash
# Clone o repositório
git clone https://github.com/projeto-de-algoritmos-2025/Dividir_Conquistar_Visualizador

# Entre na pasta do projeto
cd PA_4

# Execute o projeto
python main.py
```

## Uso 
Após executar o projeto, você terá acesso ao menu principal com as seguintes opções:

1. **Contagem de Inversões**: Analisa uma lista de números e conta inversões
2. **Mediana das Medianas**: Encontra a mediana usando algoritmo determinístico
3. **Par de Pontos Mais Próximos**: Encontra o par de pontos com menor distância
0. **Sair**: Encerra o programa

### Exemplos de Uso

#### Contagem de Inversões
```
Escolha uma opção: 1
Digite uma lista de números separados por espaço: 5 2 6 1
```
Saída: Mostra as divisões do array e conta as inversões encontradas

#### Mediana das Medianas
```
Escolha uma opção: 2
Digite uma lista de números separados por espaço: 3 1 4 1 5 9 2 6
```
Saída: Mostra grupos de 5 elementos e como a mediana é escolhida

#### Par de Pontos Mais Próximos
```
Escolha uma opção: 3
Digite os pontos no formato x y, um por linha. Linha vazia para terminar.
Exemplo: 1.5 2.3
0 0
1 1
2 2
3 0
(linha vazia para terminar)
```
Saída: Mostra divisões dos pontos e distâncias calculadas


### Conceitos de Dividir e Conquistar
Todos os algoritmos seguem o paradigma de **Dividir e Conquistar**:

1. **Dividir**: Quebrar o problema em subproblemas menores
2. **Conquistar**: Resolver os subproblemas recursivamente  
3. **Combinar**: Juntar as soluções dos subproblemas

### Métricas de Análise
Os algoritmos são analisados considerando:
- **Complexidade de Tempo**: Análise assintótica do número de operações
- **Complexidade de Espaço**: Memória utilizada durante a execução
- **Número de Divisões**: Quantas vezes o problema foi subdividido
- **Visualização Passo a Passo**: Como cada divisão e conquista acontece

### Características dos Algoritmos
- **Contagem de Inversões**: Demonstra como modificar merge sort para resolver problemas de contagem, mantendo a eficiência O(n log n).

- **Mediana das Medianas**: Algoritmo sofisticado que garante tempo linear no pior caso para seleção, diferente de quickselect que pode degradar para O(n²).

- **Par de Pontos Mais Próximos**: Mostra como dividir problemas geométricos de forma inteligente, evitando a comparação de todos os pares O(n²).
