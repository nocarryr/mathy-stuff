from __future__ import division
import math
import numbers

import matplotlib.pyplot as plt

def magnitude_from_delta(dt_x, dt_y):
    return math.sqrt(dt_x ** 2 + dt_y ** 2)

def magnitude_from_points(init_x, init_y, terminal_x, terminal_y):
    # dt_x = abs(init_x) + abs(terminal_x)
    # dt_y = abs(init_y) + abs(terminal_y)
    dt_x = terminal_x - init_x
    dt_y = terminal_y - init_y
    return magnitude_from_delta(dt_x, dt_y)

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def copy(self):
        return Point(self.x, self.y)
    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)
    def __mul__(self, other):
        return Point(self.x*other.x, self.y*other.y)
    def __imul__(self, other):
        if isinstance(other, numbers.Number):
            self.x *= other
            self.y *= other
        else:
            self.x *= other.x
            self.y *= other.y
        return self
    def __div__(self, other):
        return Point(self.x/other.x, self.y/other.y)
    def __pow__(self, other):
        # if isinstance(other, numbers.Number):
        #     args = [pow(self.x, other), pow(self.y, other)]
        # else:
        #     args = [pow(self.x, other.x), pow(self.y, other.y)]
        # return Point(*args)
        p = self.copy()
        p **= other
        return p
    def __ipow__(self, other):
        if isinstance(other, numbers.Number):
            # self.x **= other
            # self.y **= other
            self.x = pow(self.x, other)
            self.y = pow(self.x, other)
        else:
            # self.x **= other.x
            # self.y **= other.y
            self.x = pow(self.x, other.x)
            self.y = pow(self.y, other.y)
        return self
    def __repr__(self):
        return str(self)
    def __str__(self):
        return '({self.x}, {self.y})'.format(self=self)

class Vector(object):
    def __init__(self, **kwargs):
        self.initial = kwargs.get('initial', (0, 0))
        if not isinstance(self.initial, Point):
            self.initial = Point(*self.initial)
        self.terminal = kwargs.get('terminal')
        if self.terminal is not None:
            if not isinstance(self.terminal, Point):
                self.terminal = Point(*self.terminal)
    @property
    def magnitude(self):
        dt = self.terminal - self.initial
        dt **= 2
        return math.sqrt(dt.x + dt.y)
    def copy(self):
        return Vector(initial=self.initial.copy(), terminal=self.terminal.copy())
    def __mul__(self, other):
        # This operates with 'other' as a scalar
        if not isinstance(other, numbers.Number):
            return NotImplemented
        v = self.copy()
        v *= other
        return v
    def __imul__(self, other):
        # This operates with 'other' as a scalar
        if not isinstance(other, numbers.Number):
            return NotImplemented
        self.terminal *= other
        return self
    def __add__(self, other):
        mag = other.magnitude
        other = other.copy()
        other.initial += self.terminal
        other.terminal += self.terminal
        print(mag, other.magnitude)
        assert other.magnitude == mag
        return Vector(initial=self.initial.copy(), terminal=other.terminal)
    def __sub__(self, other):
        mag = other.magnitude
        other = other.copy()
        other.initial = self.terminal - other.initial
        other.terminal = self.terminal - other.terminal
        print(mag, other.magnitude)
        assert other.magnitude == mag
        return Vector(initial=self.initial.copy(), terminal=other.terminal)

axes = None
def color_iter():
    colors = 'rgbcmykw'
    it = iter(colors)
    while True:
        try:
            c = next(it)
        except StopIteration:
            it = iter(colors)
            c = next(it)
        yield c
color = color_iter()

def plot_vector(v=None, **kwargs):
    global axes
    if axes is None:
        axes = plt.axes()
        axes.grid(True)
    if v is None:
        v = Vector(**kwargs)
    c = next(color)
    return axes.arrow(
        v.initial.x, v.initial.y,
        v.terminal.x, v.terminal.y,
        head_width=.05, fc=c, ec=c,
    )

def main():
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    u = Vector(terminal=[1, -5])
    plot_vector(u)
    w = Vector(terminal=[8, 4])
    plot_vector(w)
    uw = u + w
    plot_vector(uw)
    v = Vector(initial=[-1, -8], terminal=w.terminal.copy())
    plot_vector(v)
    uv = u + v
    plot_vector(uv)
    plt.show()

if __name__ == '__main__':
    main()
