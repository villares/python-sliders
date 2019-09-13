# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from javax.swing import JOptionPane

"""
This will switch between Arduino (Firmata) variable input and
nice sliders based on Peter Farell's Sliders htts://twitter.com/hackingmath
https://github.com/hackingmath/python-sliders http://farrellpolymath.com/
"""

class Slider:

    sliders = []
    firmata = None

    def __init__(self, low, high, default):
        '''slider has range from low to high
        and is set to default'''
        self.low = low
        self.high = high
        self.val = default
        self.clicked = False
        self.up, self.down = False, False
        self.sliders.append(self)

    def position(self, x, y):
        '''slider's position on screen'''
        self.x = x
        self.y = y
        # the position of the rect you slide:
        self.rectx = self.x + map(self.val, self.low, self.high, 0, 120)
        self.recty = self.y - 10

    def update(self, display=True):
        '''updates the slider'''
            # key usage
        if self.up:
            self.rectx += 1
        if self.down:
            self.rectx -= 1
            #draw
        if display:
            pushStyle()
            rectMode(CENTER)
            # black translucid rect behind slider
            fill(0, 100)
            noStroke()
            rect(self.x + 60, self.y, 130, 20)
            # gray line behind slider
            strokeWeight(4)
            stroke(200)
            line(self.x, self.y, self.x + 120, self.y)
            # press mouse to move slider
            if (self.x < mouseX < self.x + 120 and
                    self.y < mouseY < self.y + 20):
                fill(250)
                textSize(10)
                text(str(int(self.val)), self.rectx, self.recty + 35)
                if mousePressed:
                    self.rectx = mouseX
            # constrain rectangle
            self.rectx = constrain(self.rectx, self.x, self.x + 120)
            # draw rectangle
            noStroke()
            fill(255)
            rect(self.rectx, self.recty + 10, 10, 20)
            self.val = map(self.rectx, self.x, self.x + 120, self.low, self.high)
            popStyle()

    @classmethod
    def keyPressed(cls):
        if key == 'a':
            cls.sliders[0].down = True
        if key == 'd':
            cls.sliders[0].up = True
        if key == 's':
            cls.sliders[1].down = True
        if key == 'w':
            cls.sliders[1].up = True
        if keyCode == LEFT:
            cls.sliders[2].down = True
        if keyCode == RIGHT:
            cls.sliders[2].up = True
        if keyCode == DOWN:
            cls.sliders[3].down = True
        if keyCode == UP:
            cls.sliders[3].up = True

    @classmethod
    def keyReleased(cls):
        if key == 'a':
            cls.sliders[0].down = False
        if key == 'd':
            cls.sliders[0].up = False
        if key == 's':
            cls.sliders[1].down = False
        if key == 'w':
            cls.sliders[1].up = False
        if keyCode == LEFT:
            cls.sliders[2].down = False
        if keyCode == RIGHT:
            cls.sliders[2].up = False
        if keyCode == DOWN:
            cls.sliders[3].down = False
        if keyCode == UP:
            cls.sliders[3].up = False

     # TODO: Better key reading
    #     KEY_PAIRS = ((ord('A'), ord('D')),
    #                  (ord('W'), ord('S')),
    #                  (LEFT, RIGHT),
    #                  (UP, DOWN),
    #                  )
        
    @classmethod               
    def update_all(cls, display=True):
        for i, slider in enumerate(cls.sliders):
            slider.update(display)
            if cls.firmata_port:
                a = slider.analog(cls.analog_pins[i])
                slider.rectx = map(a, 0, 1023, slider.x, slider.x + 120)


    @classmethod               
    def val(cls,n):
        return cls.sliders[n].val

    @classmethod               
    def create_defaults(cls, Arduino=None):
        if Arduino:
            cls.setup_firmata(Arduino)
        # start, end, default
        A = Slider(0, 1023, 128)
        B = Slider(0, 1023, 128)
        C = Slider(0, 1023, 128)
        D = Slider(0, 1023, 128)
        A.position(40, height - 70)
        B.position(40, height - 30)
        C.position(width - 140, height - 70)
        D.position(width - 140, height - 30)
        
    @classmethod
    def help(cls):
            message = """    Teclas:
            'h' para esta ajuda
            'p' para salvar uma imagem
            'a' (-) ou 'd' (+) para o slider 1
            's' (-) ou 'w' (+) para o slider 2
             ←(-) ou  → (+) para o slider 3
             ↓  (-) ou  ↑  (+) para o slider 4
            [barra de espaço] para limpar o desenho"""
            ok = JOptionPane.showMessageDialog(None, message)
            

    def analog(cls, pin):
        if cls.firmata_port is not None:
            return cls.arduino.analogRead(pin)

    def digital(cls, pin=13):
        space_pressed = keyPressed and key == ' '
        if cls.firmata_port is not None:
            if pin == 13:
                return cls.arduino.digitalRead(13) or space_pressed
            else:
                return arduino.digitalRead(pin)
        else:
            return space_pressed
        
    @classmethod            
    def setup_firmata(cls, Arduino, analog_pins=(1, 2, 3, 4)):
        cls.firmata_port = cls.select_port(Arduino)
        println("Firmata port selected: {}".format(cls.firmata_port))
        if cls.firmata_port is not None:
            cls.analog_pins = analog_pins
            cls.arduino = Arduino(this, Arduino.list()[cls.firmata_port], 57600)
                
    @classmethod            
    def select_port(cls, Arduino):
        port_list = [str(num) + ": " + port for num, port
                     in enumerate(Arduino.list())]
        if not port_list:
            port_list.append(None)
        return option_pane("O seu Arduino está conectado?",
                                  "Escolha a porta ou pressione Cancel\npara usar 'sliders':",
                                  port_list,
                                  0)  # index for default option


def option_pane(title, message, options, default=None, index_only=True):

    if default == None:
        default = options[0]
    elif index_only:
        default = options[default]

    selection = JOptionPane.showInputDialog(
        frame,
        message,
        title,
        JOptionPane.INFORMATION_MESSAGE,
        None,  # for Java null
        options,
        default)  # must be in options, otherwise 1st is shown
    if selection:
        if index_only:
            return options.index(selection)
        else:
            return selection
