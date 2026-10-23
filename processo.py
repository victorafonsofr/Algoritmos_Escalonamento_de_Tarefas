from itertools import count

class Processo:

    id_increment = count(1)
    
    def __init__(self, criacao, duracao, prioridade):
        self.id = next(self.id_increment)
        self.criacao = criacao
        self.duracao = duracao
        self.prioridade = prioridade
        self.executando = False # flag para verificar se o processo está sendo executado ou não
    