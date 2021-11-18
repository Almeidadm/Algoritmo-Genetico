from math import sqrt
from random import randint, shuffle, random
from numpy import partition
import sys, getopt, traceback, os, re, shutil, imageio
import matplotlib.pyplot as plt

if(not os.path.exists("./Resultados/")):
    os.mkdir("./Resultados/")
if(not os.path.exists("./Resultados/Imagens")):
    os.mkdir("./Resultados/Imagens/")
if(not os.path.exists("./Resultados/GIF")):
    os.mkdir("./Resultados/GIF/")    
if(not os.path.exists("./Resultados/Tours")):
    os.mkdir("./Resultados/Tours/")      

class Files:

	def __init__(self):
		self.inputfile = ''
	def set_name(self):
		self.name = self.inputfile[:-4]
	def get_nodes(self):
		file = open(self.inputfile).read().split('\n')[8:-2]
		nodes = {}
		for node in file:
			node = node.split(' ')
			nodes[int(node[0])] = (int(node[1]), int(node[2]))
		return nodes
    
class Metrics:
	def __init__(self):
		self.population_size = 1
		self.generation_number = 1
		self.mutation_rate = 0.5

def get_arg(argv, metrics, files):
	try:
		opts, args = getopt.getopt(argv, 'h:t:k:n:m', ['tsp_file=', 'population_size=', 'generation_number=', 'mutation_rate=']) 
	except getopt.GetoptError:
		print("Unexpected error:", sys.exc_info()[0])
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print("\t --tsp_file <input doc.tsp>\n\t --population_size <integer [1,infty)>\n\t --generetions_number <integer [1,infty)>\n\t --mutation_rate <float [0,1]>\n")
   
		elif opt in ('-t','--tsp_file'):
			if arg[-4:] != ".tsp":
				print("Unexpected error: file does not fit to .tsp format\t")
				sys.exit(3)
			files.inputfile = arg
			files.set_name()
        
		elif opt in ("k","--population_size"):
			if int(arg) < 1:
				print("Unexpected error: pop_size out of range")
				sys.exit(4)
			metrics.population_size = int(arg)
            
		elif opt in ("n","--generation_number"):
			if int(arg) < 1:
				print("Unexpected error: gen_number out of range")
				sys.exit(4)
			metrics.generation_number = int(arg)
            
		elif opt in ("m","--mutation_rate"):
			if float(arg) > 1 or float(arg) < 0:
				print("Unexpected error: mutation_rate out of range")
				sys.exit(5)
			metrics.mutation_rate = float(arg)
  
# distancia entre os pontos
def euclidian_distance(p1, p2):
    return abs(sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 ))

# função a ser otimizada é o custo total do caminho
def fitness(seq, node):
    seq = [i+1 for i in seq]
    cost = 0
    for i in range(len(seq)-1):
        u = seq[i]
        v = seq[i+1]
        cost += euclidian_distance(node[u], node[v])
    u = seq[0]
    v = seq[-1]
    cost += euclidian_distance(node[u], node[v])
    return cost

# Partially Mapped Crossover
# https://user.ceng.metu.edu.tr/~ucoluk/research/publications/tspnew.pdf
def PMX(seq1, seq2):
    
    # crossover point mutation
    point = randint(1, len(seq1))
    
    new_1 = seq1.copy()
    new_2 = seq2.copy()
    
    for i in range(point):
        
        # primeiro filho
        idx = new_1.index(seq2[i])
        new_1[i], new_1[idx] = new_1[idx], new_1[i]
        
        # segundo filho
        idx = new_2.index(seq1[i])
        new_2[i], new_2[idx] = new_2[idx], new_2[i]
    
    return new_1, new_2

def new_population(s, k):
    
    population = [s]
    
    for _ in range(k-1):
        aux = s.copy()
        shuffle(aux)
        if aux not in population: # cria população de individuos diferentes entre si
            population.append(aux) 
        else:
            _ -= 1
    return population

# Roulette Wheel Selection
# https://www.researchgate.net/publication/259461147_Selection_Methods_for_Genetic_Algorithms
def rw_selection(prob):
    a = random()*1000
    for i in range(len(prob)):
        if a < prob[i]:
            return i-1
        
# individuo com menor fitness tem maior chance de serem escolhidos        
def set_probabilities(fitness_values):
    n = len(fitness_values)
    p = []
    for i in range(n):
        aux = 1/(n-1)
        aux *= 1 - (fitness_values[i] / sum(fitness_values))
        p.append(aux)
        
    prob = [p[0]*1000]
    
    for i in range(1, len(fitness_values)):
        prob.append((prob[-1] + p[i]*1000))
    
    return prob

# Reverse Sequence Mutation
# https://arxiv.org/pdf/1203.3099.pdf
def RSM(s, mutation_rate):
    op = random()
    if op > mutation_rate:
        return
    
    i = randint(0, len(s)-2)
    j = randint(i, len(s)-1)
    
    while(i < j):
        s[i], s[j] = s[j], s[i]
        i += 1
        j -= 1
    return
    
# algoritmo genético
def GA(nodes, k, m, mutation_rate):
    
    init = [i for i in range(131)]
    population = new_population(init, k)
    
    fit_values = [ fitness(s, nodes) for s in population ]
    prob = set_probabilities(fit_values)
    min_dist = min(fit_values)
    
    # m numero de gerações
    for _ in range(m):
        
        # seleciona dois pais
        i = rw_selection(prob)
        j = rw_selection(prob)
        
        if i == j: # garante que sejam diferentes
            _ -= 1
            continue
    
        # toma os novos filhos
        offspring1, offspring2 = PMX(population[i], population[j])
        
        # mutação nos filhos
        RSM(offspring1, mutation_rate)
        RSM(offspring2, mutation_rate)
        
        population.append(offspring1)
        fit_values.append(fitness(offspring1, nodes))
        
        population.append(offspring2)
        fit_values.append(fitness(offspring2, nodes))
        
        
        # remove os dois items menos ajustados
        for _ in range(2):
            aux = max(fit_values)
            idx = fit_values.index(aux)
            del fit_values[idx]
            del population[idx]
        
        prob = set_probabilities(fit_values)
        
    fit_min = min(fit_values)
    idx = fit_values.index(fit_min)
    
    return population[idx], fit_min
    
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def print_path(path, nodes, name):
    
    if name in os.listdir('./Resultados/Imagens/'):
            shutil.rmtree('./Resultados/Imagens/'+name)
    os.mkdir('./Resultados/Imagens/'+name) 
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for v in nodes:
        ax.plot(nodes[v][0], nodes[v][1], marker='.', color='blue')
    
    for i in range(1, len(path)):
        v = path[i]+1
        u = path[i-1]+1
        node_v = nodes[v]
        node_u = nodes[u]

        x_points = [node_v[0], node_u[0]]
        y_points = [node_v[1], node_u[1]]

        ax.plot(x_points, y_points, color='red')
        
        plt.savefig('./Resultados/Imagens/'+name+'/'+str(i))
    
    v = path[0]+1
    u = path[-1]+1

    node_v = nodes[v]
    node_u = nodes[u]

    x_points = [node_v[0], node_u[0]]
    y_points = [node_v[1], node_u[1]]

    ax.plot(x_points, y_points, color='red')

    plt.savefig('./Resultados/Imagens/'+name+'/'+str(i))
    
    images = []
    sorted_names = list(os.listdir('./Resultados/Imagens/'+name+'/'))
    sorted_names.sort(key=natural_keys)
    for filename in sorted_names:
        images.append(imageio.imread('./Resultados/Imagens/'+name+'/'+filename))
    imageio.mimsave('./Resultados/GIF/'+name+'_tour.gif', images, duration=0.2)
    
    plt.clf, plt.cla
            
def write_tour(filename, path, count):
    file = open('./Resultados/Tours/'+filename+'.tour', 'w')
    
    file.write('NAME: '+filename+'\n')
    file.write('COMMENT: Tour length {}\n'.format(count))
    file.write('TYPE: TOUR\n')
    file.write('DIMENSION: {}\n'.format(len(path)))
    file.write('TOUR_SECTION\n')
    
    for i in path:
        file.write(str(path[i])+'\n')
    file.write('-1\n')
    file.write('EOF')
    file.close()


if __name__ == "__main__":
    
    f = Files()
    m = Metrics()
    
    get_arg(sys.argv[1:], m, f)
    
    if f.inputfile == "":
    	print("Unexpected error: input file not founded\n")
    	sys.exit(1)
    
    nodes = f.get_nodes()
    
    path, cost = GA(nodes, m.population_size, m.generation_number, m.mutation_rate)
        
    write_tour(f.name, path, cost)
    
    print_path(path, nodes, f.name)
