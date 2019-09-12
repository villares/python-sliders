# -*- coding: utf-8 -*-
from random import choice

TAM_PONTO = 30  # TAM_PONTO dos nodes 

class Node():
    VEL_MAX = 5
    SET = set()

    " nodes num grafo, creates Edges with other nodes "

    def __init__(self, x, y, cor=color(0)):
        VEL_MAX = Node.VEL_MAX
        self.x = x
        self.y = y
        self.z = 0  # for compatibility with PVector only...
        self.vx = random(-VEL_MAX, VEL_MAX)
        self.vy = random(-VEL_MAX, VEL_MAX)
        colorMode(HSB)
        self.cor = color(random(256), 255, 255)
        self.create_edges()

    def __getitem__(self,i):
        """ only to make a node PVector-like :) """
        return (self.x, self.y, self.z)[i]

    def desenha(self):
        noStroke()
        fill(150, 50)
        ellipse(self.x, self.y, TAM_PONTO, TAM_PONTO)

    def move(self, VEL_MAX):
        Node.VEL_MAX = VEL_MAX
        self.x += self.vx
        self.y += self.vy
        if not (0 < self.x < width):
            self.vx = -self.vx
        if not (0 < self.y < height):
            self.vy = -self.vy
        self.vx = self.limit(self.vx, VEL_MAX)
        self.vy = self.limit(self.vy, VEL_MAX)

    def create_edges(self):
            lista_nodes = list(Node.SET)
            if len(lista_nodes) > 1:
                rnd_node = choice(lista_nodes)
                while rnd_node == self:
                    rnd_node = choice(lista_nodes)
            
                Edge.EDGES.append(Edge(rnd_node, self))

    def limit(self, v, v_max):
        if v > v_max:
            return v_max
        elif v < -v_max:
            return -v_max
        else:
            return v


class Edge():

    """ EDGES contain 2 Nodes """            

    EDGES = []

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def desenha(self):
        strokeWeight(1)
        stroke(lerpColor(self.p1.cor, self.p2.cor, 0.5))
        line(self.p1.x, self.p1.y, self.p2.x, self.p2.y)
        noStroke()
        fill(self.p1.cor)
        ellipse(self.p1.x, self.p1.y, TAM_PONTO / 4, TAM_PONTO / 4)
        fill(self.p2.cor)
        ellipse(self.p2.x, self.p2.y, TAM_PONTO / 4, TAM_PONTO / 4)

    def puxa_empurra(self, TAM_BARRA):
        d = dist(self.p1.x, self.p1.y, self.p2.x, self.p2.y)
        delta = TAM_BARRA - d
        dir = PVector.sub(self.p1, self.p2)
        dir.mult(delta / 1000)
        self.p1.vx = self.p1.vx + dir.x
        self.p1.vy = self.p1.vy + dir.y
        self.p2.vx = self.p2.vx - dir.x
        self.p2.vy = self.p2.vy - dir.y
