# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# XODR_FILE='/dataset/opendrive/singlelaneroad.xodr'
XODR_FILE='/dataset/opendrive/borregasave.xodr'


# %%
import numpy as np
import math


def RotatePoint2D(point, rotation):
    sin = math.sin(rotation)
    cos = math.cos(rotation)
    mat = np.array(((cos, -sin), 
                    (sin, cos)))
    return np.matmul(mat, np.array(point))


def draw_line(line_sample):
    s = float(line_sample.get('s'))
    a = float(line_sample.get('x'))
    b = float(line_sample.get('y'))
    hdg = float(line_sample.get('hdg'))
    length = float(line_sample.get('length'))
    points = [RotatePoint2D((x, 0), hdg) + (a, b) 
              for x in np.arange(0, length, 0.05)]
    return np.array(points)


def draw_curve(curve_sample, U, V):
    s = float(curve_sample.get('s'))
    a = float(curve_sample.get('x'))
    b = float(curve_sample.get('y'))
    hdg = float(curve_sample.get('hdg'))
    length = float(curve_sample.get('length'))
    # paramPoly3
    aU = float(U[0])
    bU = float(U[1])
    cU = float(U[2])
    dU = float(U[3])
    aV = float(V[0])
    bV = float(V[1])
    cV = float(V[2])
    dV = float(V[3])
    
    points = [RotatePoint2D((aU + bU*p + cU*pow(p,2) + dU*pow(p,3), 
                             aV + bV*p + cV*pow(p,2) + dV*pow(p,3)), hdg) + (a, b) 
                             for p in np.arange(0, 1, 0.05)] 
    return np.array(points)

from matplotlib import pyplot as plt
from lxml import etree


class OpendriveParser(object):
    def __init__(self, file_dir):
        self.xml_root = self._read_xodr(file_dir)
        self.geometry = []

    def _read_xodr(self, file_dir):
        with open(file_dir, 'r') as f:
            return etree.parse(f).getroot()

    def parse(self):
        for child in self.xml_root:
            if child.tag == 'road':
                self._planeview(child)
    
    def _planeview(self, root):
        for child in root:
            if child.tag == 'planView':
                self._geometry(child)
    
    def _geometry(self, root):
        for child in root:
            if child.tag == 'geometry':
                if self._is_cubic(child):
                    U, V = self._get_paramPoly3(child)
                    g = ParamPoly3(child.get('s'), child.get('x'), child.get('y'), child.get('hdg'), child.get('length'),
                                   U[0], U[1], U[2], U[3], V[0], V[1], V[2], V[3])
                    self.geometry.append(g)
                else:
                    g = Line(child.get('s'), child.get('x'), child.get('y'), child.get('hdg'), child.get('length'))
                    self.geometry.append(g)

    def _is_cubic(self, root) -> bool:
        for child in root:
            if child.tag == 'paramPoly3':
                return True
            else:
                return False

    def _get_paramPoly3(self, root):
        for child in root:
            if child.tag =='paramPoly3':
                U = [child.get('aU'), child.get('bU'), child.get('cU'), child.get('dU')]
                V = [child.get('aV'), child.get('bV'), child.get('cV'), child.get('dV')]
                return U, V

def draw_line(line, plt):
    p1, p2 = line.get_points()
    plt.plot(p1, p2, linestyle='-', marker='')


def draw_param_poly(cubic, plt):
    xs, ys = cubic.get_points()

    c = Curve(cubic.x, cubic.y, cubic.hdg)
    x_li, y_li = [], []
    for p in zip(xs, ys):
        xi, yi = c.rel_to_abs(p)
        x_li.append(xi), y_li.append(yi)

    plt.plot(x_li, y_li, 'ro')


parser = OpendriveParser(XODR_FILE)
parser.parse()

for g in parser.geometry:
    if isinstance(g, Line):
        draw_line(g, plt)
    # elif isinstance(g, ParamPoly3):
    #     draw_param_poly(g, plt)
    # else:
    #     print('except geometry type')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('line')
plt.show()

