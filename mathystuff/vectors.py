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

def angle_from_xy(x, y):
    deg = math.degrees(math.atan(y / x))
    if x > 0 and y > 0:
        return deg
    elif y > 0:
        deg += 180
    elif x > 0:
        deg += 360
    else:
        deg += 180
    return deg

def xy_from_magnitude_angle(magnitude, angle):
    rad = math.radians(angle)
    x = magnitude * math.cos(rad)
    y = magnitude * math.sin(rad)
    return x, y

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
    _magnitude = None
    _angle = None
    def __init__(self, **kwargs):
        self.initial = kwargs.get('initial', (0, 0))
        if not isinstance(self.initial, Point):
            self.initial = Point(*self.initial)
        self.terminal = kwargs.get('terminal')
        if self.terminal is not None:
            if not isinstance(self.terminal, Point):
                self.terminal = Point(*self.terminal)
        else:
            self.angle = kwargs.get('angle')
            self.magnitude = kwargs.get('magnitude')
    @property
    def magnitude(self):
        if self.terminal is None and self._angle is None:
            return None
        dt = self.terminal - self.initial
        dt **= 2
        return math.sqrt(dt.x + dt.y)
    @magnitude.setter
    def magnitude(self, value):
        self._magnitude = value
        if self._angle is not None:
            x, y = xy_from_magnitude_angle(self._magnitude, self._angle)
            self.terminal = self.initial + Point(x, y)
    @property
    def angle(self):
        if self.terminal is None and self._magnitude is None:
            return None
        terminal = self.terminal.copy()
        terminal -= self.initial
        return angle_from_xy(terminal.x, terminal.y)
    @angle.setter
    def angle(self, value):
        self._angle = value
        if self._magnitude is not None:
            x, y = xy_from_magnitude_angle(self._magnitude, self._angle)
            self.terminal = self.initial + Point(x, y)
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
    def __str__(self):
        return '({t.x: 5.2f}, {t.y: 5.2f}) {a: 6.2f} deg'.format(
            t=self.terminal, a=self.angle)

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

def plot_vector(v=None, name='', **kwargs):
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
        head_width=.5, fc=c, ec=c,
        length_includes_head=True, label='{}: {}'.format(name, str(v)),
    )

def main():
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    handles = []
    u = Vector(terminal=[1, -5])
    handles.append(plot_vector(u, ' u'))
    w = Vector(terminal=[8, 4])
    handles.append(plot_vector(w, ' w'))
    uw = u + w
    handles.append(plot_vector(uw, 'uw'))
    v = Vector(initial=[-1, -8], terminal=w.terminal.copy())
    handles.append(plot_vector(v, ' v'))
    uv = u + v
    handles.append(plot_vector(uv, 'uv'))
    y = Vector(magnitude=10, angle=225)
    handles.append(plot_vector(y, ' y'))
    legend = plt.legend(handles=handles, loc='upper left',
        prop={'family':'monospace', 'size':'small'})
    plt.show()

if __name__ == '__main__':
    main()
