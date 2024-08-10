import numpy as np
import copy

"""
VILAS = A
CASTELOS = B
ESTRADAS = M
DISTANCIA MAXIMA = L
USOS DA BOTA = K
"""


def inicializar_grafo(tamanho):
    grafo = [[] for _ in range(tamanho)]
    return grafo


def adicionar_aresta(grafo, origem, destino, peso):
    aresta = (destino, peso)
    grafo[origem].append(aresta)
    aresta_reversa = (origem, peso)
    grafo[destino].append(aresta_reversa)


def bellman_ford(A, B, M, L, K, estradas):
    # Inicializando constante
    nos_totais = A + B + 1

    # Array de distâncias, índice 1 = ponto inicial (Village 1)
    distancia = [np.inf for _ in range(nos_totais)]
    distancia[1] = 0  # Starting point (Village 1)

    # Lista de adjacência para estradas
    grafo = inicializar_grafo(nos_totais)

    for estrada in estradas:
        Xi, Yi, Li = estrada
        adicionar_aresta(grafo, Xi, Yi, Li)

    # Bellman-Ford: relax
    for i in range(nos_totais - 1):
        for no in range(1, nos_totais):  # Iterate over valid node indices
            for vizinho in grafo[no]:
                destino, peso = vizinho
                if distancia[no] + peso < distancia[destino]:
                    distancia[destino] = distancia[no] + peso

    # Super-corrida
    super_distancia = copy.deepcopy(distancia)

    # Para cada uso da bota
    for k in range(K):
        nova_super_distancia = copy.deepcopy(super_distancia)
        for no in range(1, nos_totais):  # Iterate over valid node indices
            # Considerar apenas nós alcançáveis
            if super_distancia[no] < np.inf:  # Corrected condition
                for vizinho in grafo[no]:
                    destino, peso = vizinho
                    # Considerar apenas estradas dentro do limite de distância
                    if peso <= L:  # Change to <= to include the edge
                        nova_super_distancia[destino] = min(
                            nova_super_distancia[destino], nova_super_distancia[no]
                        )
        super_distancia = nova_super_distancia  # No need to deepcopy here

    # O destino é o castelo em A + B, retornando o tempo mínimo
    return super_distancia[A + B]


if __name__ == "__main__":
    T = int(input("Insira o número de casos teste: "))
    for t in range(T):
        A, B, M, L, K = map(
            int,
            input(
                "Insira, separados por espaço, os valores numéricos para vilas, castelos, estradas, distância máxima de super-pulo e super-pulos disponíveis: "
            ).split(),
        )
        estradas = []
        for m in range(M):
            entrada = input(
                f"Insira, separados por espaço, os valores numéricos para a origem, destino e peso da estrada {m}: "
            ).split()
            Xi, Yi, Li = map(int, entrada)
            estradas.append((Xi, Yi, Li))

        resultado = bellman_ford(A, B, M, L, K, estradas)
        print(resultado)
