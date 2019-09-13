"""
Sliders + Arduino Examples
Grafos - Alexandre B A Villares 2018
"""

add_library('serial')  # import processing.serial.*;
add_library('arduino')  # import cc.arduino.*;

from random import choice
from graphs import Node, Edge, NODE_SIZE
from inputs import Slider

def setup():
    size(600, 600)
    frameRate(30)
    # Check github.com/villares/lousa-magica for hardware instructions
    # use: Slider.create_defaults(Arduino)
    # and it will ask user for Arduino port, but uses only sliders if none is selected
    Slider.create_defaults(Arduino) # creates 4 sliders
    
    Node.SET = set()
    num_nodes = int(Slider.val(2) / 4)
    for _ in range(num_nodes):
        Node.SET.add(Node(width / 2, height / 2))

def draw():
    background(0)

    tam_edge = Slider.val(1) / 4
    num_nodes = int(Slider.val(2) / 4)
    max_speed = Slider.val(3) / 128
    edge_rate = 0.5 + Slider.val(0) / 256  # % of connections

    # para cada node
    for node in Node.SET:
        node.desenha()  # desenha
        node.move(max_speed)    # atualiza posição

    # checa edges, se OK desenhar, se não tem nodes removidos ou iguais
    nodes_with_edges = set()  # para guardar nodes com edge
    for edge in Edge.EDGES:
        if (edge.p1 not in Node.SET) or (edge.p2 not in Node.SET)\
                or (edge.p1 is edge.p2):  # edges degeneradas
            Edge.EDGES.remove(edge)   # remove a edge
        else:                # senão, tudo OK!
            edge.desenha()  # desenha a linha
            edge.puxa_empurra(tam_edge)  # altera a velocidade dos nodes
            # Adiciona ao conjunto de nodes com edge
            nodes_with_edges.update([edge.p1, edge.p2])

    edgeless_nodes = Node.SET - nodes_with_edges
    # print(len(Node.SET), len(edgeless_nodes), len(nodes_with_edges))
    # atualiza número de nodes
    number_of_nodes = len(Node.SET)
    if num_nodes > number_of_nodes:
        Node.SET.add(Node(random(width), random(height)))
    elif num_nodes < number_of_nodes - 2:
        if edgeless_nodes:
            # remove um node sem edge
            Node.SET.remove(edgeless_nodes.pop())
        else:
            Node.SET.pop()  # remove um node qualquer
    # outra maneira de eliminar nodes solitários é criando edges
    if edgeless_nodes:
        for node in edgeless_nodes:
            node.create_edges()
    # atualiza número de edges
    if int((num_nodes) * edge_rate) > len(Edge.EDGES) + 1:
        if edgeless_nodes:   # preferência por nodes solitários
            choice(list(edgeless_nodes)).create_edges()
        else:
            choice(list(Node.SET)).create_edges()
    elif int(num_nodes * edge_rate) < len(Edge.EDGES) - 1:
        Edge.EDGES.remove(choice(Edge.EDGES))

    if keyPressed and key==" ":
        # Node.reset(int(Slider.val(2) / 4))
        Node.SET = set()
        for _ in range(num_nodes):
            Node.SET.add(Node(width / 2, height / 2))

    # Updates reading or draws sliders and checks mouse dragging
    Slider.update_all()

def mouseDragged():        # quando o mouse é arrastado
    for node in Node.SET:   # para cada Node checa distância do mouse
        if dist(mouseX, mouseY, node.x, node.y) < NODE_SIZE / 2:
            # move o Node para posição do mouse
            node.x, node.y = mouseX, mouseY
            node.vx = 0
            node.vy = 0

def keyPressed():
    global GIF_EXPORT
    if key == 'p':  # save PNG
        saveFrame("####.png")
    if key == 'h':
        Slider.help()

    Slider.keyPressed()

def keyReleased():
    Slider.keyReleased()
