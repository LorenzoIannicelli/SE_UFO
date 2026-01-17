from database.dao import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._G = None
        self._list_states = []
        self._dict_states = {}
        self._state_sightings = {}


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

