O projeto faz parte da Disciplina de Inteligência Artificial na FATEC SP. Temos que estudar um solucionador de jogo Sudoku utilizando um algoritmo com uma ou mais estratégias de busca apresentadas em sala. 
A estratégia escolhida foi a Busca A*.

Em sudoku.py:
**tabuleiro_data** e **jogo_data**:  têm matriz bidimensional, com listas bidimensionais, para representar o tabuleiro do jogo de Sudoku. **tabuleiro_data** é usado para armazenar o tabuleiro originalmente gerado.
**jogo_data é usado** para manter o estado atual do jogo conforme o jogador insere números.
**copia_tabuleiro** foi criado para copiar o **tabuleiro_data** com os números escondidos transformados em 0 para funcionar o algoritmo usado em solverAstar.py. 
**escondendo_numeros** é uma variável booleana que controla se os números no tabuleiro do Sudoku devem ser escondidos ou não.

Em solucionador.py:
A classe **Board** representa o estado do tabuleiro do Sudoku em uma determinada etapa do algoritmo de solução. É uma lista bidimensional.

**possible_vals**é  uma lista bidimensional que armazena os possíveis valores para cada célula do tabuleiro do Sudoku durante o processo de resolução.

Também foram usadas filas de prioridade (PriorityQueue), conjuntos (set), e operações com bits para manipulação de bits para controle de visitas e fila de prioridade para próximas jogadas.

Utilizamos o gerador de jogos do [Leonardo Nunes Armelim](https://github.com/Leonardo-Nunes-Armelim/Bytes_Universe/tree/main/Python/004_Sudoku) para a nossa base do jogo e o código A* do [Will Roever](https://github.com/wroever/sudoku-solver/blob/master/solver.py) adaptando ambos com algumas modificações para se adequar ao escopo da disciplina e se complementarem.

## Próximos passos antes da apresentação final da disciplina
- Criar botão que deixe o tabuleiro zerado para o jogador preencher com um tabuleiro que gostaria de resolver. Assim podendo clicar no botão de AI Solver e encontrar a solução.
- Resolver a visualização dos números preenchidos pela IA.  

