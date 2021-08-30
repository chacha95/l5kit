import xml.etree.ElementTree as ET
import numpy as np
import math


def RotatePoint2D(point, rotation):
    sin = math.sin(rotation)
    cos = math.cos(rotation)
    mat = np.array(((cos, -sin), (sin, cos)))

    return np.matmul(mat, np.array(point))


def draw_line(line_sample):
    parameters = line_sample.attrib
    s = float(parameters['s'])
    a = float(parameters['x'])
    b = float(parameters['y'])
    hdg = float(parameters['hdg'])
    length = float(parameters['length'])
    points = [RotatePoint2D((x, 0), hdg) + (a, b) 
              for x in np.arange(0, length, 0.05)]
    return np.array(points)


def draw_curve(curve_sample):
    parameters = curve_sample.attrib
    s = float(parameters['s'])
    a = float(parameters['x'])
    b = float(parameters['y'])
    hdg = float(parameters['hdg'])
    length = float(parameters['length'])
    parameters = curve_sample[0].attrib
    aU = float(parameters['aU'])
    bU = float(parameters['bU'])
    cU = float(parameters['cU'])
    dU = float(parameters['dU'])
    aV = float(parameters['aV'])
    bV = float(parameters['bV'])
    cV = float(parameters['cV'])
    dV = float(parameters['dV'])
    
    points = [RotatePoint2D((aU + bU*p + cU*pow(p,2) + dU*pow(p,3), 
               aV + bV*p + cV*pow(p,2) + dV*pow(p,3)), hdg) + (a,b)
              for p in np.arange(0, 1, 0.05)] 
    return np.array(points)


def draw_road_ref(pV_sample):
    points = list()
    points = np.array(points)
    for geo in pV_sample:
        if 'line' in geo[0].tag:
            points = np.append(points, draw_line(geo)).reshape(-1,2)
    
        elif 'paramPoly3' in geo[0].tag:
            points = np.append(points, draw_curve(geo)).reshape(-1,2)

    return points


def rasterize(points, SCALE_PARAMETER):
    MARGIN = 2
    cv_points = (points + (np.abs(np.min(points[:,0])), np.abs(np.min(points[:,1])))) * SCALE_PARAMETER
    canbus = np.zeros((int(np.max(cv_points[:,0]))+MARGIN, int(np.max(cv_points[:,1]))+MARGIN)).astype(np.uint8)
    for point in cv_points:
        coord = np.round(point).astype(np.int)
        canbus[coord[0]][coord[1]] = 1
    return canbus