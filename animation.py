
import time
import random
import contextlib
import os
with contextlib.redirect_stdout(None):
    import pygame


pygame.init()
pygame.font.init()
comicsans = pygame.font.SysFont('Comic Sans MS', 30)

animators = []

def remap(value, src, dst):

    s0, s1 = src
    t0, t1 = dst
    S = s1 - s0
    T = t1 - t0
    return t0 + ((value - s0) / S) * T

class meta(type):
    def __new__(cls,*args,**kwargs):
        t = type.__new__(cls,*args,**kwargs)
        if t.__name__ != "SortingAlgorithm":
            animators.append(t)
        return t

class SortingAlgorithm(metaclass=meta):
    """
    supposed to be subclassed.

    subclass should provide sort() function and optionally an initialize() function

    you can optionally also supply a display function to make custom graphics.
    the window surface is stored in self.window

    be aware:
    either supply a regular update() call or use the swap, get() and set() methods
    they will also update the screen

    the getstack functionality highlights gotten and set indices. if this fails turn it of with setgetstack(False)
    """

    def __init__(self, *args):

        self.scramble(*args)

        self._linewidth = 9
        self._lineheightmultiplier = 5

        self._backgroundcolor = (255, 255, 255)
        self._drawcolor = (0, 0, 0)

        self.getstack = []
        self.getstackenabled = True

        self.done = False

        self.window = pygame.display.set_mode(
            (
                self._linewidth*len(self.array)
                if self._linewidth*len(self.array) > 640
                else 640,
                len(self.array)
                if self._lineheightmultiplier*len(self.array) > 480
                else 480
            )
        )

        if hasattr(self, "initialize"):
            self.initialize()
        else:
            self.fit()


    def setgetstack(self, enabled=None):
        if enabled:
            self.getstackenabled = enabled
        return self.getstackenabled

    def backgroundcolor(self, color=None):
        if color:
            self._backgroundcolor = color
        return self._backgroundcolor

    def drawcolor(self, color=None):
        if color:
            self._drawcolor = color
        return self._drawcolor

    def linewidth(self, width=None):
        if width:
            self._linewidth = width
        return self._linewidth

    def lineheightmultiplier(self, height=None):
        if height:
            self._lineheightmultiplier = height
        return self._lineheightmultiplier

    def resize(self, w=None, h=None):
        if w == None:
            w = self.window.get_width()
        if h == None:
            h = self.window.get_height()

        if w < self._linewidth*len(self.array):
            w = self._linewidth*len(self.array)

        if h < len(self.array)*self._lineheightmultiplier:
            h = len(self.array)*self._lineheightmultiplier

        self.window = pygame.display.set_mode((w, h))

    def fit(self):
        self.resize(0, 0)

    def write(self, text):
        textsurface = comicsans.render(text, False, (0,0,0))
        w = textsurface.get_width()
        h = textsurface.get_height()
        x = self.window.get_width()//2 - w//2
        y = self.window.get_height()//2 - h//2
        self.window.blit(textsurface,(x,y))


    def display(self):
        width = self.linewidth()

        for index, i in enumerate(self.array):
            color = self.drawcolor()
            if self.getstackenabled:
                if index in self.getstack:
                    color = (
                        (len(self.getstack) - self.getstack.index(index)) *
                        (255/len(self.getstack)),
                        self.drawcolor()[1],
                        self.drawcolor()[2]
                    )

            pygame.draw.line(
                self.window,
                color,
                (
                    index*width,
                    self.window.get_height()-(i*self.lineheightmultiplier())),
                (index*width, self.window.get_height()),
                width
            )
        if self.done:
            if hasattr(self,"shutdown"):
                self.shutdown()



    def scramble(self, start, end=0, seed=0):
        if end == 0:
            end = start
            start = 0
        self.array = list(range(start, end))
        random.shuffle(self.array)

    def sleep(self, seconds):
        millis = int(round(time.time() * 1000))
        while True:
            self.update()
            if int(round(time.time() * 1000)) > millis + int(seconds*1000):
                break

    def update(self):
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        self.window.fill((255, 255, 255))
        self.display()
        pygame.display.flip()

    def run(self):
        self.update()
        self.sort()
        self.done = True
        try:
            while True:
                self.update()
        except KeyboardInterrupt:
            return

    def quit(self):
        pygame.quit()
        exit()
        return

    def sort(self):
        raise NotImplemented

    def popgetstack(self):
        if self.getstack:
            self.getstack.pop()

    def swap(self, a, b, update=True):
        self.array[a], self.array[b] = self.array[b], self.array[a]

        if a in self.getstack:
            self.getstack[self.getstack.index(a)] = b
        if b in self.getstack:
            self.getstack[self.getstack.index(b)] = a
        if update:
            self.update()

    def get(self, index, getstack=True, update=True):
        if getstack:
            self.getstack.append(index)
        if update:
           self.update()
        return self.array[index]

    def set(self, index, value, getstack=True, update=True):
        if getstack and self.getstack:
            self.getstack.pop()
    
        self.array[index] = value
        if update:
            self.update()
