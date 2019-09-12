"""
Sliders + Arduino Examples
Grafos - Alexandre B A Villares 2018
"""

add_library('serial')  # import processing.serial.*;
add_library('arduino')  # import cc.arduino.*;

from graphs import *
from inputs import *

def setup():
    size(600, 600)
    frameRate(30)
    GIF_EXPORT = False
    # Ask user for Arduino port, uses only slider if none is selected`
    #  Slider.create_defaults(Arduino)
    Slider.create_defaults() # creates 4 sliders
    
    Ponto.SET = set()
    NUM_PONTOS = int(Slider.val(2) / 4)
    for _ in range(NUM_PONTOS):
        Ponto.SET.add(Ponto(width / 2, height / 2))

def draw():
    background(0)

    TAM_ARESTA = Slider.val(1) / 4
    NUM_PONTOS = int(Slider.val(2) / 4)
    VEL_MAX = Slider.val(3) / 128
    CONNECT_RATE = 0.5 + Slider.val(0) / 256  # % of connections

    # para cada ponto
    for ponto in Ponto.SET:
        ponto.desenha()  # desenha
        ponto.move(VEL_MAX)    # atualiza posição

    # checa arestas, se OK desenhar, se nãotem pontos removidos ou iguais
    pontos_com_arestas = set()  # para guardar pontos com aresta
    for aresta in Aresta.ARESTAS:
        if (aresta.p1 not in Ponto.SET) or (aresta.p2 not in Ponto.SET)\
                or (aresta.p1 is aresta.p2):  # arestas degeneradas
            Aresta.ARESTAS.remove(aresta)   # remove a aresta
        else:                # senão, tudo OK!
            aresta.desenha()  # desenha a linha
            aresta.puxa_empurra(TAM_ARESTA)  # altera a velocidade dos pontos
            # Adiciona ao conjunto de pontos com aresta
            pontos_com_arestas.update([aresta.p1, aresta.p2])

    pontos_sem_arestas = Ponto.SET - pontos_com_arestas
    # print(len(Ponto.SET), len(pontos_sem_arestas), len(pontos_com_arestas))
    # atualiza número de pontos
    quantidade_atual_de_pontos = len(Ponto.SET)
    if NUM_PONTOS > quantidade_atual_de_pontos:
        Ponto.SET.add(Ponto(random(width), random(height)))
    elif NUM_PONTOS < quantidade_atual_de_pontos - 2:
        if pontos_sem_arestas:
            # remove um ponto sem aresta
            Ponto.SET.remove(pontos_sem_arestas.pop())
        else:
            Ponto.SET.pop()  # remove um ponto qualquer
    # outra maneira de eliminar pontos solitários é criando arestas
    if pontos_sem_arestas:
        for ponto in pontos_sem_arestas:
            ponto.cria_arestas()
    # atualiza número de arestas
    if int((NUM_PONTOS) * CONNECT_RATE) > len(Aresta.ARESTAS) + 1:
        if pontos_sem_arestas:   # preferência por pontos solitários
            rnd_choice(list(pontos_sem_arestas)).cria_arestas()
        else:
            rnd_choice(list(Ponto.SET)).cria_arestas()
    elif int(NUM_PONTOS * CONNECT_RATE) < len(Aresta.ARESTAS) - 1:
        Aresta.ARESTAS.remove(rnd_choice(Aresta.ARESTAS))

    if keyPressed and key==" ":
        # Ponto.reset(int(Slider.val(2) / 4))
        Ponto.SET = set()
        for _ in range(NUM_PONTOS):
            Ponto.SET.add(Ponto(width / 2, height / 2))


    # Updates reading or draws sliders and checks mouse dragging
    Slider.update_all()

def mouseDragged():        # quando o mouse é arrastado
    for ponto in Ponto.SET:   # para cada Ponto checa distância do mouse
        if dist(mouseX, mouseY, ponto.x, ponto.y) < TAM_PONTO / 2:
            # move o Ponto para posição do mouse
            ponto.x, ponto.y = mouseX, mouseY
            ponto.vx = 0
            ponto.vy = 0

def keyPressed():
    global GIF_EXPORT
    if key == 'p':  # save PNG
        saveFrame("####.png")
    if key == 'h':
        Slider.help()

    Slider.keyPressed()

def keyReleased():
    Slider.keyReleased()
