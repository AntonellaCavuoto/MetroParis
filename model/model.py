from datetime import datetime

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()  # uso _ così che il grafo non venga modificato dall'esterno
        self._idMapFermate = {}  # mappa di fermate con id
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def buildGraph(self):
        # aggiungo i nodi
        self._grafo.add_nodes_from(self._fermate)
        self.addEdges3()

    def addEdges1(self):
        """Aggiungo gli archi con doppio ciclo,
        e testando se per ogni coppia esiste una connessione"""
        for u in self._fermate:
            for v in self._fermate:
                if u != v and DAO.hasConnessione(u, v):  # se esiste una connessione tra u e v
                    self._grafo.add_edge(u, v)
                    print("Aggiungo arco fra", u, "e", v)

    def addEdges2(self):
        """ Ciclo solo una volta e faccio una query per trovare tutti i vicini
        """
        for u in self._fermate:
            for con in DAO.getVicini(u):
                v = self._idMapFermate[con.id_stazA]
                self._grafo.add_edge(u, v)

    def addEdges3(self):  # più veloce
        """
        Faccio una query unica che prende tutti gli archi e poi ciclo qui
        """
        allEdges = DAO.getAllEdges()
        for edge in allEdges:
            u = self._idMapFermate[edge.id_stazP]
            v = self._idMapFermate[edge.id_stazA]
            self._grafo.add_edge(u, v)

    def getNumNodi(self):
        return len(self._grafo.nodes)  # numero di fermate

    def getNumArchi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate
