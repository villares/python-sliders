class Slider:

    def __init__(self, low, high, default=None):
        """
        slider has range from low to high
        and is set to default in the middle
        if none is provided
        """
        self.low = low
        self.high = high
        if default is None:
            self.val = (low + high) / 2.
        else:
            self.val = default
        self.clicked = False
        self.label = ''  # blank label
        self.w, self.h = 120, 20

    def position(self, x, y):
        """slider's position on screen"""
        self.x = x
        self.y = y
        # the position of the rect you slide:
        self.rectx = self.x + map(self.val, self.low, self.high, 0, self.w)
        self.recty = self.y

    def value(self):
        """updates the slider and returns value"""
        pushStyle()
        pushMatrix()
        resetMatrix()
        rectMode(CENTER)
        # gray line behind slider
        strokeWeight(4)
        stroke(200)
        line(self.x, self.y, self.x + 120, self.y)
        # press mouse to move slider
        if mousePressed and dist(mouseX, mouseY, self.rectx, self.recty) < self.h:
            self.rectx = mouseX
        # constrain rectangle
        self.rectx = constrain(self.rectx, self.x, self.x + self.w)
        # draw rectangle
        strokeWeight(1)
        stroke(0)
        fill(255)
        rect(self.rectx, self.recty, self.w / 12, self.h)
        self.val = map(
            self.rectx, self.x, self.x + self.w, self.low, self.high)
        # draw label
        fill(0)
        textSize(10)
        textAlign(CENTER, CENTER)
        text(int(self.val), self.rectx, self.recty + self.h)
        # text label
        textAlign(LEFT, CENTER)
        text(self.label, self.x + self.w + self.h, self.y)
        popMatrix()
        popStyle()
        return self.val
