import xml.etree.ElementTree as ET
import numpy as np
import math


def RotatePoint2D(point, rotation):
    sin = math.sin(rotation)
    cos = math.cos(rotation)
    mat = np.array(((cos, -sin), (sin, cos)))

    return np.matmul(mat, np.array(point))


def draw_line(node):
    s = float(node.get('s'))
    a = float(node.get('x'))
    b = float(node.get('y'))
    hdg = float(node.get('hdg'))
    length = float(node.get('length'))
    points = [RotatePoint2D((x, 0), hdg) + (a, b) 
              for x in np.arange(0, length, 0.05)]
    return np.array(points)


def draw_curve(node, U, V):
    s = float(node.get('s'))
    a = float(node.get('x'))
    b = float(node.get('y'))
    hdg = float(node.get('hdg'))
    length = float(node.get('length'))
    aU = float(U[0])
    bU = float(U[1])
    cU = float(U[2])
    dU = float(U[3])
    aV = float(V[0])
    bV = float(V[1])
    cV = float(V[2])
    dV = float(V[3]) 
    
    points = [RotatePoint2D((aU + bU*p + cU*pow(p,2) + dU*pow(p,3), 
               aV + bV*p + cV*pow(p,2) + dV*pow(p,3)), hdg) + (a,b)
              for p in np.arange(0, 1, 0.05)] 
    return np.array(points)


# def rasterize(points, SCALE_PARAMETER):
#     MARGIN = 2
#     cv_points = (points + (np.abs(np.min(points[:,0])), np.abs(np.min(points[:,1])))) * SCALE_PARAMETER
#     canbus = np.zeros((int(np.max(cv_points[:,0]))+MARGIN, int(np.max(cv_points[:,1]))+MARGIN)).astype(np.uint8)
#     for point in cv_points:
#         coord = np.round(point).astype(np.int)
#         canbus[coord[0]][coord[1]] = 1
#     return canbus