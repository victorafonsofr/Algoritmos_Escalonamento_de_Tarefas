import os
import subprocess
from operator import attrgetter

from processo import Processo
# importando a classe

#quanto maior o número, maior a prioridade.
MAIOR_NUMERO_MAIOR_PRIORIDADE = True

##############################################  Funções  #############################################################################


# calcula o tempo máximo que a simulação pode durar: maior criação + soma das durações
def duracao_max(lista_processos):
    duracao = 0
    for p in lista_processos:
        duracao += p.duracao
    return max(p.criacao for p in lista_processos) + duracao


# comeco do diagrama de tempo (uma coluna por processo)
def imprime_cabecalho(lista_processos):
    print("\ntempo  ", end="")
    for p in lista_processos:
        print(f"P{p.id:<3}", end="") # so pra lembrar, o :<3 formata o texto pra esquerda com 3 caracteres
    print()


# imprime uma linha do diagrama de tempo
def imprime_linha(t, lista_processos, rodando, restante):
    print(f"{t:>3}-{t+1:<3}  ", end="")
    for p in lista_processos:
        if p is rodando:
            print("##  ", end="")
        elif p.criacao <= t and restante[p.id] > 0:
            print("--  ", end="")
        else:
            print("    ", end="")
    print() # pula a liha


# calculosa
def imprime_medias(lista_processos, termino):
    soma_vida = 0
    soma_espera = 0
    print("\nProcesso|Criação|Duração|Término|Vida|Espera")
    for p in lista_processos:
        vida = termino[p.id] - p.criacao
        espera = vida - p.duracao
        soma_vida += vida
        soma_espera += espera
        print(f"P{p.id} {p.criacao} {p.duracao} {termino[p.id]} {vida} {espera}")

    n = len(lista_processos)
    print(f"\nTempo médio de vida:   {soma_vida / n:.2f}")
    print(f"Tempo médio de espera: {soma_espera / n:.2f}")


#o primeiro da lista ordenada é o mais prioritário.
def chave_prioridade(p):
    sinal = -1 if MAIOR_NUMERO_MAIOR_PRIORIDADE else 1
    return (sinal * p.prioridade, p.criacao, p.id)

def shortest_job_first(lista_processos):
    if not lista_processos:
        print("Lista invalida")
        return

    tempo_max = duracao_max(lista_processos)
    restante = {p.id: p.duracao for p in lista_processos}  # tempo que falta de cada processo
    termino = {}
    lista_prontas = []
    rodando = None
    cont_tempo = 0

    print("\n=== SJF (Shortest Job First) ===")
    imprime_cabecalho(lista_processos)

    while len(termino) < len(lista_processos) and cont_tempo < tempo_max:

        #processos novos entram na fila de prontos se o tempo (timer) for igual ao instante de criacao
        for p in lista_processos:
            if p.criacao == cont_tempo:
                lista_prontas.append(p)

        if rodando is None and lista_prontas:
            lista_prontas.sort(key=attrgetter('duracao', 'criacao', 'id'))
            rodando = lista_prontas.pop(0)

        imprime_linha(cont_tempo, lista_processos, rodando, restante)

        if rodando is not None:
            restante[rodando.id] -= 1
            if restante[rodando.id] == 0:
                termino[rodando.id] = cont_tempo + 1
                rodando = None  # libera o processador

        cont_tempo += 1

    imprime_medias(lista_processos, termino)

def prioridade_com_preempcao(lista_processos):
    if not lista_processos:
        print("Lista invalida")
        return

    tempo_max = duracao_max(lista_processos)
    restante = {p.id: p.duracao for p in lista_processos} #cria um dicionario para acessar valores mais facilmente
    termino = {}
    lista_prontas = []
    rodando = None
    cont_tempo = 0

    print("\n=== Prioridade com preempção ===")
    imprime_cabecalho(lista_processos)

    while len(termino) < len(lista_processos) and cont_tempo < tempo_max:

        #processos que chegam agora entram na fila de prontos
        for p in lista_processos:
            if p.criacao == cont_tempo:
                lista_prontas.append(p)

        #preempção
        if rodando is not None:
            lista_prontas.append(rodando)
            rodando = None

        #escolhe o de maior prioridade entre todos os prontos
        if lista_prontas:
            lista_prontas.sort(key=chave_prioridade)
            rodando = lista_prontas.pop(0)

        imprime_linha(cont_tempo, lista_processos, rodando, restante)

        #executa 1 unidade de tempo
        if rodando is not None:
            restante[rodando.id] -= 1
            if restante[rodando.id] == 0:
                termino[rodando.id] = cont_tempo + 1
                rodando = None  # terminou, libera o processador

        cont_tempo += 1

    imprime_medias(lista_processos, termino)

def menu(lista_processos):
    while True:
        print("\n========== MENU ==========")
        print("1 - Shortest Job First (SJF)")
        print("3 - Por prioridade, com preempção")
        print("0 - Sair")
        opcao = input("Escolha o algoritmo: ").strip()

        if opcao == "1":
            shortest_job_first(lista_processos)
        elif opcao == "3":
            prioridade_com_preempcao(lista_processos)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

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

menu(lista_processos)
