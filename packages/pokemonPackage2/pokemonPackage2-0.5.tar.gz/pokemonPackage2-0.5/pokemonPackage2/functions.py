import pandas as pd

class pokemonFunctions:
    def __init__(self, filename):
        self.filename = filename
        self.data = pd.read_csv(filename)

    def get_grupos_pokemon(self):
        return self.data['Grupo']

    def get_altura_media_grupo(self,grupo):
        return self.data.query('Grupo == @grupo')['Peso medio']

    def get_peso_medio_grupo(self,grupo):
        return self.data.query('Grupo == @grupo')['Altura media']
