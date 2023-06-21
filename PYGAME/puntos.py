class Puntaje:
    def __init__(self):
        self.puntos = 0

    def aumentar(self,aumento):
        self.puntos += aumento
    def restar(self,resta):
        self.puntos -= resta
    def obtener(self):
        return self.puntos