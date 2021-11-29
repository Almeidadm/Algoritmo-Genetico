# Algoritmo Genético para resolver o Problema do Caixeiro Viajante

Este repositório foi criado de forma que a implementação do algoritmo genético para resolução do caixeiro viajante. 

Para utilização deste código é necessário ter instalado Python3 e as seguintes bibliotecas: numpy, matplotlib, shutil e imageio.

A implementação utiliza como representação genética a ordem dos vértices visitados num percurso. Desta forma, podemos realizar mutações e cruzamentos de maneira que preserve a validez da solução. Foi escolhido um critério de seleção por roleta, ou *Wheel Roulette*, e método de cruzamento *Partially Mapped Crossover*, utilizando por fim o método de mutação *Reverse Sequence Mutation*.

O programa tem como parâmetros o problema no formato *.tsp*, o tamanho $n$ da população inicial, o número de gerações $m$ e taxa de mutação *r*. Além disto é possível gerar um GIF da solução encontrada e também um gráfico que avalia o comportamento do algoritmo.

Abaixo podemos ver um exemplo de execução do modelo.



```python
!python3 tsp_1.py --tsp_file=./problem/xqf131.tsp --population_size=100 --generation_number=5000 --mutation_rate=0.4
```

    current minimum: 942	gen:5000/50000
    Total time: 9.995372 s

O modelo responsável pelo resultado apresentado pode ser visto a seguinte da seguinte maneira:
file:///home/ddeam/Imagens/%C3%ADndice.png![image](https://user-images.githubusercontent.com/47041221/143793217-cf9fb321-d3a2-463c-8b49-057fd28022da.png)
Onde o vértice x apresenta o decorrer das iterações e o vértice y apresenta o melhor fitness da população naquele momento.

Podemos realizar uma análise de como a taxa de mutação interfere no desempenho da heurística.
Veja a seguir a comparação quando atribuímos os valores de mutação *r = {0.0, 0.2, 0.4, 0.6, 0.8, 0.99}*. Definindo *n=100* e *m=20000*, temos:
file:///home/ddeam/Imagens/%C3%ADndice1.png![image](https://user-images.githubusercontent.com/47041221/143793232-80ba2e51-efa7-48e5-8197-ad1d477ade4b.png)

É notável o péssimo desempenho de quando temos um modelo com taxa de mutação nula, em azul, enquanto que com taxa de mutação igual a 60% trouxe bons resultados, mas ainda assim não ótimos.

Agora, quando definimos *m=20000*, *r=0.6* e *n = {50, 100, 200, 500}* podemos vizualizar o seguinte comportamento:
file:///home/ddeam/Imagens/%C3%ADndice2.png![image](https://user-images.githubusercontent.com/47041221/143793240-50ff2b58-9a35-426a-a4a2-2d1cf06ce23d.png)

Onde notoriamente a população de cinquenta indivíduos convergiu bem melhor que a de 500.
