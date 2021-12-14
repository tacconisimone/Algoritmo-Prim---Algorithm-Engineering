#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:01:54 2021

@author: simonetac
"""

try:
    import networkx as nx
except:
    raise

import fibonacci     #https://github.com/danielborowski/fibonacci-heap-python/blob/master/fib-heap.py
import random
import pandas as pd
from time import process_time

count=0

#GENERAZIONE GRAFO
def generazione_grafo_nondiretto(n, m, seed=None):
    """
    Parametri
    ----------
    n : int
        Il numero di nodi.
    m : int
        Il numero di archi.
    seed : integer, random_state, or None (default)
        Indicatore dello stato della generazione del numero casuaele.
    """
    G = nx.Graph()
    G.add_nodes_from(range(n))
    if n == 1:
        return G
    max_edges = n * (n - 1)
    max_edges /= 2.0
    if m >= max_edges:
        return nx.complete_graph(n, create_using=G)
    nlist = list(G)
    edge_count = 0
    while edge_count < m:
        # generate random edge,u,v
        u = random.choice(nlist)
        v = random.choice(nlist)
        if u == v or G.has_edge(u, v):
            continue
        else:
            G.add_edge(u, v)
            edge_count = edge_count + 1
    return G


#ALGORITMO DI PRIM

def algoritmo_prim(G,radice):
    global count
    
    heapHandles = [None] * G.number_of_nodes()
    node_weight = []    #lista che contiene il nodo e weight
    inMST=[0] * G.number_of_nodes()

    fibheap = fibonacci.FibonacciHeap()   #creo un heap di fibonacci basato sul minimo vuoto

    heapHandles[radice] = fibheap.insert((0, radice))
    inMST[radice] = 1    
    genitore = [-1] * G.number_of_nodes()
    costo=0

    while fibheap.total_nodes > 0:

        #count+=1
        corrente = fibheap.extract_min()

        assert corrente is not None

        vertex = corrente.key[1]
        vertex_priority = corrente.key[0]
        
        node_weight.append((vertex,vertex_priority))
        costo += vertex_priority
        inMST[vertex]=2
        for vicino in G.adj[vertex]:

            if inMST[vicino] != 2:

                if inMST[vicino] == 0:
                    count += 1
                    inMST[vicino] = 1
                    heapHandles[vicino] = fibheap.insert((G.edges[vertex, vicino]['weight'], vicino))
                    #print(heapHandles[vicino])
                    genitore[vicino] = vertex
                    #print(genitore[vicino])

                else:
                    assert inMST[vicino] == 1
                    key=heapHandles[vicino].key[0]
                    assert vicino == heapHandles[vicino].key[1]
                    if G.edges[vertex, vicino]['weight'] < key:
                        count+=1
                        fibheap.decrease_key(heapHandles[vicino], (G.edges[vertex, vicino]['weight'], vicino))
                        genitore[vicino] = vertex
                        assert heapHandles[vicino].key[0] == G.edges[vertex, vicino]['weight']

    return node_weight[1:len(node_weight)+1],costo


#MAIN

vertici= input('Inserisci il numero di vertici del grafo: ')
archi= input('Inserisci il numero di archi del grafo: ')

numero_vertici=int(vertici)
numero_archi=int(archi)

G=generazione_grafo_nondiretto(numero_vertici,numero_archi)
#E=G.number_of_edges()
#print(numero_vertici,numero_archi,E)
#print(G.edges)
for (u, v) in G.edges():
    G.edges[u,v]['weight'] = random.randint(1,9)
    #print(u,v,G.edges[u,v]['weight'])


inizio=random.randint(0,numero_vertici-1)
#print(inizio)  
tempo=[]

inizio_alg=process_time()
T_nodo_peso,costo=algoritmo_prim(G,inizio)
tempo_alg=process_time()-inizio_alg
#print (count)
#print (T_nodo_peso)

valori=[]

try:
    df = pd.read_csv("risultati.csv", usecols=["Numero vertici", "Numero archi", "Costo totale del MST", "Numero di operazioni dominanti", "tempo di CPU"])
except:
     df = pd.DataFrame(valori, columns = ['Numero vertici' , 'Numero archi', 'Costo totale del MST', 'Numero di operazioni dominanti', 'tempo di CPU'])
     df.to_csv('risultati.csv', index=True)
     
df=df.append({'Numero vertici' : int(numero_vertici), 'Numero archi' : int(numero_archi), 'Costo totale del MST' : int(costo), 'Numero di operazioni dominanti' : int(count), 'tempo di CPU' : tempo_alg} , ignore_index=True)
df.to_csv('risultati.csv', index=True)
