import os
import subprocess

from processo import Processo
#importando a classe

##############################################  Funções  #############################################################################


#pega a lista de processos e verifica qual será o tempo máximo de duração do algoritmo
def duracao_max(lista_processos):
    duracao = 0
    for i in range(len(lista_processos)):
        duracao += lista_processos[i].duracao

    return duracao

# pega o processo de menor tempo de duracao
def menor_processo(lista_processos):
    if not lista_processos:
        print("lista vazia!")
    else:
        menor_duracao = lista_processos[0].duracao   
        processo_menor_duracao = lista_processos[0]

        for processo in lista_processos:
            if processo.duracao < menor_duracao:
                processo_menor_duracao = processo
                menor_duracao = processo.duracao 

        return processo_menor_duracao  

# algoritmo sjf
def shortest_job_first(lista_processos):

    if not lista_processos:
        print("Lista invalida")
    else:
        tempo_max = duracao_max(lista_processos) 
        cont_tempo = 0

        lista_prontas = []

        while cont_tempo < tempo_max:
            
            for processo in lista_processos:
                if processo.criacao == cont_tempo:
                    lista_prontas.append(processo)

            ##encontrar o processo com menor tempo
            menor_duracao_pronto = menor_processo(lista_prontas)
            
            for i in range(len(lista_processos)):
                print(f"P{i+1} |",end="")
    
            cont_tempo+=1       
##############################################  Main  #############################################################################
numero_processos = int(input("Entre com o total de processos: "))
lista_processos = []

# leitura dos processos;

for i in range(numero_processos):
    criacao = int(input(f"Qual o momento de criação do processo {i+1}?\n"))
    duracao = int(input(f"Qual a duração do processo {i+1}?\n"))
    prioridade = int(input(f"Qual a prioridade do processo {i+1}?\n"))

    processo_temp = Processo(criacao, duracao, prioridade)
    lista_processos.append(processo_temp)

    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

'''
#teste unitario para ver se foram adicionados os processos corretamente

for i in range(numero_processos):
    print(f"Processo[{i+1}]")
    
    print("Criacao: ",lista_processos[i].criacao)
    print("Duracao: ",lista_processos[i].duracao)
    print("Prioridade: ",lista_processos[i].prioridade)
'''

shortest_job_first(lista_processos)