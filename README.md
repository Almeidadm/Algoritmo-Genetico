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
![image](https://user-images.githubusercontent.com/47041221/143791919-ebedf84d-4878-4e27-a219-0cc5ebfa0de6.png)

Onde o vértice x apresenta o decorrer das iterações e o vértice y apresenta o melhor fitness da população naquele momento.

Podemos realizar uma análise de como a taxa de mutação interfere no desempenho da heurística.
Veja a seguir a comparação quando atribuímos os valores de mutação *r = {0.0, 0.2, 0.4, 0.6, 0.8, 0.99}*. Definindo *n=100* e *m=20000*, temos:
![image](https://user-images.githubusercontent.com/47041221/143791935-b4a9cf61-2704-489f-93b1-f759014b8f1f.png)


É notável o péssimo desempenho de quando temos um modelo com taxa de mutação nula, em azul, enquanto que com taxa de mutação igual a 60% trouxe bons resultados, mas ainda assim não ótimos.

Agora, quando definimos *m=20000*, *r=0.6* e *n = {50, 100, 200, 500}* podemos vizualizar o seguinte comportamento:
![image](https://user-images.githubusercontent.com/47041221/143791941-8943b9d8-dc74-47e4-818f-25f019819a0a.png)
Onde notoriamente a população de cinquenta indivíduos convergiu bem melhor que a de 500.
