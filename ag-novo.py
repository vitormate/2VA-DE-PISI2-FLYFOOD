import math
import random
import time

inicio = time.time()

random.seed(18)

# Valores iniciais
tamanho_populacao = 40
taxa_reproducao = 20
probabilidde_mutacao = 0.05
n_geracoes = 100


# Lendo arquivo
arquivo = open('matriz-1.txt', 'r')

nlinha, ncoluna = map(int, arquivo.readline().split())

coordenadas = {}
pontos = []

for i in range(nlinha):
    linha = arquivo.readline().split()
    for j in range(ncoluna):
        if linha[j] != '0':
            pontos.append(linha[j])
            coordenadas[linha[j]] = (i, j)

arquivo.close()
pontos.remove('R')

# Calculando quantos embaralhamentos serão feitos
n_elemento = math.ceil(tamanho_populacao / len(pontos))

def rota(pontos):
    rota = pontos.copy()

    random.shuffle(rota)

    return rota

# A função populacao_inicial aparentemente é extremamente ineficiente, ajuste
def populacao_inicial(lista):
    populacao = []

    for i in range(tamanho_populacao):
        
        populacao.append(rota(pontos))
    
    return populacao

# Fórmula para cacular a distância
def formula(x1, x2, y1, y2):
    res = abs(x2-x1) + abs(y2-y1)
    return res

# Cálculo da distância de um indivíduo(percurso)
def distancia(p):
    distancia = 0

    p = list(p)
    p.insert(0, 'R')
    p.append('R')

    for i in range(len(p)-1):
        distancia += formula(coordenadas[p[i]][0], coordenadas[p[i+1]][0],coordenadas[p[i]][1], coordenadas[p[i+1]][1])

    return distancia

# Calcula o fitness e ranqueia a população em ordem decrescente
def fitness(lista):
    lista_individuos_ordenada = []
    contador = 0

    for i in lista:
        contador += 1
        distancia = 0
        fit = 0

        for j in range(len(i)-1):
            distancia += formula(coordenadas[i[j]][0], coordenadas[i[j+1]][0],coordenadas[i[j]][1], coordenadas[i[j+1]][1])
            fit = 1 / distancia

        lista_individuos_ordenada.append([[fit], i])
    lista_rank = sorted(lista_individuos_ordenada)
    lista_rank.reverse()
    
    return lista_rank

# A partir da lista_rank da função fitness seleciona os pais escolhidos para o crossover
def torneio(populacao):
    for i in range(taxa_reproducao):
        x = random.randrange(0, len(populacao))
        y = random.randrange(0, len(populacao))
        
        valor1 = populacao[x][0]
        valor2 = populacao[y][0]
            
        if valor1 >= valor2:
            populacao.pop(y)
        else:
            populacao.pop(x)

    return populacao

# Receber a lista_rank da função fitness, passar os valores de fitness para porcentagem
# Selecionar os pais baseado na porcentagem e não no rank
def roleta(lista):
    lista_individuos_ordenada = []
    populacao = []
    contador = 0
    fit = 0

    for i in lista:
        contador += 1
        distancia = 0

        for j in range(len(i)-1):
            distancia += formula(coordenadas[i[1][j]][0], coordenadas[i[1][j+1]][0],coordenadas[i[1][j]][1], coordenadas[i[1][j+1]][1])
            fit += 1 / distancia
    
    for i, valor in enumerate(lista):
        x = (valor[0][0] * 100) / fit
        lista[i][0] = [x]

    contador = 0
    conta_lista = 0

    while contador < taxa_reproducao:
        r = random.random()

        individuo = lista[conta_lista]

        if r <= individuo[0][0]:
            populacao.append(individuo)
            contador += 1
        
        conta_lista += 1
        if conta_lista == len(lista):
            conta_lista = 0
    
    lista_individuos_ordenada = sorted(populacao)
    lista_individuos_ordenada.reverse()

    return lista_individuos_ordenada

# Faz o cruzamento entre os pais e gera novos filhos
def crossover(pais):
    for k in range(0, len(pais), 2):

        pai1 = pais[k][1]
        pai2 = pais[k+1][1]

        lista_aux = pai2[:]

        corte = random.randrange(1, len(pai1)-1)

        for i in range(corte):
            for j in range(len(pai1)):
                if j > corte-1:
                    if pai1[i] == lista_aux[j]:
                        lista_aux[i], lista_aux[j] = lista_aux[j], lista_aux[i]

        for z in range(corte):
            for j in range(len(pai2)):
                if j > corte-1:
                    if pai2[z] == pai1[j]:
                        pai1[z], pai1[j] = pai1[j], pai1[z]

        pais.pop(k)
        pais.insert(k, pai1)

        pais.pop(k+1)
        pais.insert(k+1, lista_aux)

        filhos = pais.copy()
        
    return filhos

# Mutação:
# Usar random.random() para gerar uma valor aleatório
# entre 0 e 1
# Usar taxa de mutação como 5% = 0.05
# A cada indivíduo um número aleatório será gerado
# se esse número for menor do que 0.05 aplicar a
# mutação
# A mutação será feita gerando dois número aleatórios
# distintos de 0 até len(individuo)-1 e ocorrerá
# a troca de posições
def mutacao(pais, filhos):
    populacao = pais + filhos
    nova_populacao = []
    x, y = 0, 0
    for i in populacao:
        r = random.random()

        ind = i
        if r <= probabilidde_mutacao:
            while x == y:
                x = random.randrange(1, len(i)-1)
                y = random.randrange(1, len(i)-1)
            
            ind[x], ind[y] = ind[y], ind[x]
        
        nova_populacao.append(ind)


    return nova_populacao

# Execução do algoritmo genético

geracao = 1
while geracao < n_geracoes:

    if geracao == 1:
        populacao = populacao_inicial(pontos)
        for i in populacao:
            i.insert(0, 'R')
            i.append('R')

    populacao_ranqueada = fitness(populacao)

    # Trocar entre as funções roleta e torneio aqui
    pais_escolhidos = torneio(populacao_ranqueada)

    # Tira o ranqueamento dos pais escolhidos para somar com lista filhos 
    # fazer a mutação e gerar nova população
    pais = []
    for i in pais_escolhidos:
        pais.append(i[1])
    
    filhos = crossover(pais_escolhidos)

    populacao = mutacao(pais, filhos)

    geracao += 1

ultima_geracao = fitness(populacao)

resposta = ultima_geracao[0][1]

dist = distancia(resposta)

resposta.pop()
resposta.pop(0)

print("O melhor percurso é: ", resposta)
print("Distância: ", dist, "quilômetros")

fim = time.time()

tempo = fim - inicio

print(tempo)
