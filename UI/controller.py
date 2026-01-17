import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        dd_year = self._view.dd_year
        dd_shape = self._view.dd_shape
        years = self._model.get_years()
        shapes = self._model.get_shapes()

        for y in years:
            dd_year.options.append(ft.DropdownOption(key=y, text=y))

        for s in shapes:
            dd_shape.options.append(ft.DropdownOption(key=s, text=s))

        self._view.update()

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        selected_year = self._view.dd_year.value
        selected_shape = self._view.dd_shape.value
        graph, nodes, edges = self._model.build_graph(selected_year, selected_shape)

        self._view.lista_visualizzazione_1.controls.clear()
        txt1 = f'Numero di vertici: {nodes} Numero di archi: {edges}'
        self._view.lista_visualizzazione_1.controls.append(ft.Text(txt1))
        for s in graph:
            txt2 = f'Nodo {s}, somma su archi = {graph[s]}'
            self._view.lista_visualizzazione_1.controls.append(ft.Text(txt2))
        self._view.update()


    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
