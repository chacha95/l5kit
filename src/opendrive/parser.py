from lxml import etree
from draw import draw_curve, draw_line

import numpy as np


def str_parse(s: str, separator: str, keyword: str) -> str:
    li = s.split(separator)
    for e in li:
        if e == keyword:
            return True
    return False


def is_cubic(parent) -> bool:
    for child in parent:
        if str_parse(child.tag, '}', 'paramPoly3'):
            return True
        else:
            return False


def get_paramPoly3(parent):
    for child in parent:
        if str_parse(child.tag, '}', 'paramPoly3'):
            U = [child.get('aU'), child.get('bU'), child.get('cU'), child.get('dU')]
            V = [child.get('aV'), child.get('bV'), child.get('cV'), child.get('dV')]
            return U, V
            

class OpendriveParser:
    def __init__(self, file_dir):
        with open(file_dir, 'r') as f:
            self.xml_root = etree.parse(f).getroot()
        self._road = np.array([])
    
    @property
    def road(self):
        return self._road

    def __call__(self):
        for child in self.xml_root:
            if str_parse(child.tag, '}', 'road'):
                self._planeview(child)
    
    def _planeview(self, parent):
        for child in parent:
            if str_parse(child.tag, '}', 'planView'):
                self._geometry(child)
    
    def _geometry(self, parent):
        for child in parent:
            if str_parse(child.tag, '}', 'geometry'):
                if is_cubic(child):
                    U, V = get_paramPoly3(child)
                    geo = draw_curve(child, U, V)
                else:
                    geo = draw_line(child)
                self._road = np.append(self._road, geo).reshape(-1, 2)