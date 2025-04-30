from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()  # uso _ così che il grafo non venga modificato dall'esterno
        self._idMapFermate = {}  # mappa di fermate con id
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, source)
        # Parto dalla fermata passata e prendo prima la fermata a sx e poi quella a dx e così via
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi[1:]  # il primo è il nodo source

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        # Parto dal vicino alfabeticamente più piccolo e va avanti da lì
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi[1:]  # il primo è il nodo source

    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source)
        res = []
        for u, v in archi:
            res.append(v)
        return res

    def getDFSNodesFromEdges(self, source):
        archi = nx.dfs_edges(self._grafo, source)
        res = []
        for u, v in archi:
            res.append(v)
        return res

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesati2()

    def addEdgesPesati(self):
        self._grafo.clear_edges()
        """ Simile ad addEdges3, ma aggiungo contatore che sommi il numero di volte che incontro un arco
        altrimenti creo l'arco con peso = 1"""
        allEdges = DAO.getAllEdges()
        for edge in allEdges:
            u = self._idMapFermate[edge.id_stazP]
            v = self._idMapFermate[edge.id_stazA]
            if self._grafo.has_edge(u, v):
                self._grafo[u][v]["weight"] += 1
            else:
                self._grafo.add_edge(u, v, weight=1)

    # altriemnti posso modificare query
    # SELECT id_stazP, id_stazA, count(*) as n
    # FROM connessione c
    # group by id_stazP, id_stazA
    # order by n desc

    def addEdgesPesati2(self):
        self._grafo.clear_edges()
        """ Simile ad addEdges3, ma aggiungo contatore che sommi il numero di volte che incontro un arco
        altrimenti creo l'arco con peso = 1"""
        allEdgesPesati = DAO.getAllEdgesPesati()
        for edge in allEdgesPesati:
            self._grafo.add_edge(
                self._idMapFermate[edge[0]],
                self._idMapFermate[edge[1]],
                weight=edge[2])

    def getArchiPesoMaggiore(self):
        edges = self._grafo.edges(data = True)  # mi servono anche i pesi
        result = []
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1])["weight"] > 1:
                result.append(e)
        return result

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
