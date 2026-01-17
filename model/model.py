import copy
from database.dao import DAO
import networkx as nx
from geopy import distance


class Model:
    def __init__(self):
        self._G = None
        self._list_states = []
        self._dict_states = {}
        self._state_sightings = {}

        self._best_path = None
        self._max_distance = None
        self._distances = None


    def get_years(self):
        return DAO.read_years()

    def get_shapes(self):
        return DAO.read_shapes()

    def build_graph(self, year, shape):
        self._G = nx.Graph()
        self._list_states = DAO.read_all_states()

        for s in self._list_states:
            self._dict_states[s.id] = s

        self._G.add_nodes_from(self._list_states)
        self._state_sightings = DAO.read_all_sightings(year, shape)

        for s in self._list_states:
            if s.id not in self._state_sightings:
                self._state_sightings[s.id] = 0

        for s in self._list_states:
            for s1_id in s.neighbors:
                s1 = self._dict_states[s1_id]
                if self._G.has_edge(s, s1):
                    continue
                else :
                    weight = self._state_sightings[s.id] + self._state_sightings[s1.id]
                    self._G.add_edge(s, s1, weight=weight)
                    print(f'nodo aggiunto: {s} {s1}')

        result = {}
        for s in self._G:
            result[s] = 0
            for s1 in self._G.neighbors(s):
                result[s] += self._G[s][s1]['weight']

        return result, self._G.number_of_nodes(), self._G.number_of_edges()

    def calculate_path(self):
        self._best_path = []
        self._max_distance = 0
        self._distances = []

        for s in self._G:
            self._ricorsione([s], [], 0, 0)

        return self._best_path, self._G, self._max_distance, self._distances

    def _ricorsione(self, parziale, distances, current, last_edge):
        disponibili = self.search_disponibili(parziale[-1], last_edge)
        if not disponibili:
            if current > self._max_distance:
                self._best_path = copy.deepcopy(parziale)
                self._max_distance = current
                self._distances = copy.deepcopy(distances)
            return

        s = parziale[-1]
        for s1 in disponibili:
            parziale.append(s1)
            d = distance.geodesic((s.lat, s.lng), (s1.lat, s1.lng)).km
            distances.append(d)
            new_value = current + d
            last_edge = self._G[s][s1]['weight']

            self._ricorsione(parziale, distances, new_value, last_edge)

            parziale.pop()
            distances.pop()

    def search_disponibili(self, n, last):
        result = []
        for n1 in self._G.neighbors(n):
            if self._G[n][n1]['weight'] > last:
                result.append(n1)

        return result