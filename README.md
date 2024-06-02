O projeto faz parte da Disciplina de Inteligência Artificial na FATEC SP e foi realizado em dupla. 
O objetivo deste projeto era estudar o desenvolvimento de um solucionador de jogo Sudoku e utilizar um algoritmo com uma ou mais estratégias de busca apresentadas em sala. 

## Video de demonstração


https://github.com/thalitacolofatti/sudoku-solver/assets/62973671/945050eb-fa84-4f78-b83e-11fc8186b2be


A estratégia escolhida por nós foi a Busca A*.

O algoritmo A* (A-star) é um algoritmo de busca heurística que utiliza uma função de avaliação: 
            𝑓(𝑛) = 𝑔(𝑛) + ℎ(𝑛)
- g(𝑛): Custo real do caminho desde o estado inicial até o estado 𝑛.
- ℎ(𝑛): Heurística que estima o custo do estado 𝑛 até o estado objetivo.

O algoritmo explora os estados do tabuleiro de acordo com a prioridade definida pela função de avaliação. Ele utiliza uma fila de prioridade para selecionar o próximo estado a ser explorado, garantindo que o estado mais promissor (aquele com menor distância estimada para a solução) seja explorado primeiro.

No contexto do desenvolvimento de nosso jogo Sudoku, temos:

 - Espaço de Busca: O estado do tabuleiro em qualquer ponto do tempo.
 - Função de Avaliação (f): É a soma do custo do caminho até o momento (g) e a heurística (h). g é implicitamente a profundidade da recursão, e h é o número de células vazias.
 - Heurística: A heurística usada é o número de células vazias no tabuleiro, que nos dá uma estimativa de quão longe estamos de completar o Sudoku.
 - Fila de Prioridades: Usa uma fila de prioridades (heapq) para sempre expandir o estado com a menor heurística primeiro.

Esses componentes juntos fazem com que a abordagem siga a técnica A*, onde os estados são explorados com base em uma combinação do custo atual e uma estimativa do custo restante, priorizando aqueles que parecem mais promissores.

A versão final foi adaptada usando classes (encapsulamento) para simplificar o código, permitindo soluções mais eficientes. Abaixo seguem considerações pertinentes à disciplina e às solicitações da professora:

### astar.py

**Estrutura de Dados presentes**: 
 - **Lista de Listas (matriz)** para representação do tabuleiro (com cada lista interna representando uma linha do tabuleiro) e seus estados; 
 - **Tuplas** para atribuir as coordenadas das células vazias (linha, coluna);
 - **Fila de prioridade** implementada com a biblioteca `heapq` para gerenciar os estados do tabuleiro com base na heurística (priorizando o menor valor);
 - **Conjunto `set()`**  para rastrear as tentativas já visitadas e evitar reprocessamento.

**Soluções presentes**:

1. **Heurística ou busca informada**: A função heurística `heuristic` calcula a heurística de um tabuleiro, que nesse caso é o número de células vazias. Esta função guia a busca A* priorizando estados com menos células vazias.
2. **Fila de Prioridade `heapq`**: Os estados do tabuleiro são armazenados em uma fila de prioridade `queue`, onde estados com menor valor heurístico são processados primeiro.
3. **Estados Visitados**: Utiliza um conjunto `set` para manter o controle dos estados já visitados, evitando repetição de estados.
4. **Método`is_valid_move`**: verifica se um número pode ser colocado em uma determinada posição do tabuleiro sem violar as regras do Sudoku (sem repetir na linha, coluna ou bloco 3x3)
5. **Método `solve`**: Este método processa a fila de prioridade e seleciona o estado com o menor valor heurístico, expandindo os estados mais promissores. Verifica se é um estado final (sem células vazias e, se não for, gera novos estados possíveis a partir dele). Para cada estado, tenta colocar um número válido em uma célula vazia e gera novos estados, que são adicionados à fila de prioridade.
6. **Deepcopy**: Utiliza `deepcopy` para criar novos estados do tabuleiro ao tentar diferentes números.

### backtracking.py

**Estrutura de Dados presentes**: Lista de Listas (matriz) para representação do tabuleiro e tuplas para armazenar as coordenadas das células vazias (linha, coluna).

**Soluções presentes**:

1. **Escolha**: O algoritmo tenta colocar um número em uma célula vazia.
2. **Restrições**: Verifica se a inserção do número é válida conforme as regras do Sudoku.
3. **Exploração Sequencial**: Chama recursivamente `solve_backtracking` para tentar resolver o restante do tabuleiro com o novo número inserido. 
4. **Backtracking**: explora um caminho por vez. Tenta preencher uma célula (tenta todos os valores possíveis para uma célula, um de cada vez), verifica se a solução é válida e, se não for, volta atrás (backtrack) removendo o número para tentar o próximo valor possível.
5. **Recursão e Retrocesso**: Utiliza recursão para explorar possíveis soluções e retrocede (backtrack) quando encontra um impasse, desfazendo os últimos passos.

O processo é repetido até que todo o tabuleiro seja preenchido ou as possibilidades sejam esgotadas.

**jogoSudoku.py** -> Loop do jogo
**selection.py** -> Encapsulamento do desenho dos botões
**tabuleiro.py** -> implementação do tabuleiro seu desenho, suas funcionalidades e interações com os demais encapsulamentos

______________________

Primeira versão (arquivada na pasta versaoAntiga) foi implementada nos arquivos sudoku.py, solucionador.py e blankBoard.py com estruturas abaixo mencionadas
sudoku.py:
- **tabuleiro_data** e **jogo_data**:  têm matriz bidimensional, com listas bidimensionais, para representar o tabuleiro do jogo de Sudoku.
- **tabuleiro_data** é usado para armazenar o tabuleiro originalmente gerado.
- **jogo_data é usado** para manter o estado atual do jogo conforme o jogador insere números.
- **copia_tabuleiro** foi criado para copiar o **tabuleiro_data** com os números escondidos transformados em 0 para funcionar o algoritmo usado em solverAstar.py. 
- **escondendo_numeros** é uma variável booleana que controla se os números no tabuleiro do Sudoku devem ser escondidos ou não.

solucionador.py:
- A classe **Board** representa o estado do tabuleiro do Sudoku em uma determinada etapa do algoritmo de solução. É uma lista bidimensional.

- **possible_vals** é  uma lista bidimensional que armazena os possíveis valores para cada célula do tabuleiro do Sudoku durante o processo de resolução.

Também foram usadas filas de prioridade (PriorityQueue), conjuntos (set), e operações com bits para manipulação de bits para controle de visitas e fila de prioridade para próximas jogadas.

blankBoard.py foi criado como teste para gerar um tabuleiro em branco para que o jogador insira um tabuleiro conhecido e possa usar o botão solucionador com A*.
________________________

Utilizamos como base os códigos do [Leonardo Nunes Armelim](https://github.com/Leonardo-Nunes-Armelim/Bytes_Universe/tree/main/Python/004_Sudoku) (primeira versão) e do video do [AtiByte] (https://youtu.be/kayFasm5hUg?si=hwYhbehHGWO-KOCj) (versão final) para gerar o jogo e o código do algoritmo A* do [Will Roever](https://github.com/wroever/sudoku-solver/blob/master/solver.py) na primeira versão com modificações para se adequar ao escopo da disciplina. Este último código foi adaptado e parte dele foi reaproveitada sem utilizar manipulação de bits na versão final.

Efeitos sonoros do [Pixabay](https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=40956).
