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
    # Gera uma lista de adjacência vazia para cada nó
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

    # Array de distâncias, índice 0 = ponto inicial
    distancia = [np.inf for _ in range(nos_totais)]
    distancia[0] = 0

    # Lista de adjacência para estradas
    grafo = inicializar_grafo(nos_totais)

    for estrada in estradas:
        Xi, Yi, Li = estrada
        adicionar_aresta(grafo, Xi, Yi, Li)

    # Bellman-Ford: relax
    for i in range(1, nos_totais - 1):
        for no in grafo:
            for vizinho in grafo[no]:
                destino, peso = vizinho
                if distancia[no] + peso < distancia[destino]:
                    distancia[destino] = distancia[no] + peso

    # Super-corrida
    super_distancia = copy.deepcopy(distancia)

    # Para cada uso da bota
    for k in range(1, K):
        for no in grafo:
            for vizinho in grafo[no]:
                destino, peso = vizinho
                # Considerar apenas estradas dentro do limite de distância
                if peso < L:
                    if super_distancia[no] < np.inf:
                        super_distancia[destino] = min(
                            super_distancia[destino], super_distancia[no]
                        )

    # O destino é o castelo em A + B, retornando o tempo mínimo
    return super_distancia[A + B]


if __name__ == "__main__":
    T = input("Insira o número de casos teste: ")
    for t in range(T - 1):
        A, B, M, L, K = map(
            int,
            input(
                "Insira, separados por espaço, os valores numéricos para vilas, castelos, estradas, distância máxima de super-pulo e super-pulos disponíveis: "
            ).split(),
        )
        estradas = []
        for m in range(M - 1):
            Xi, Yi, Li = map(
                int,
                input(
                    f"Insira, separados por espaço, os valores numéricos para a origem, destino e peso da estrada ${m}: "
                ),
            )
            estradas.append((Xi, Yi, Li))

        resultado = bellman_ford(A, B, M, L, K, estradas)
        print(resultado)
