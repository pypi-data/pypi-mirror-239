"""
Morfeus lab
The University of Texas
MD Anderson Cancer Center
Author - Mark Hickey
Email - mshickey@mdanderson.org


Description:

"""

import zipfile
import numpy as np
from PIL import ImageColor
import xml.etree.ElementTree as ET


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)


def color_avg(color_list, p1, p2, p3):
    p2rgb = None
    p3rgb = None
    p1hex = color_list[int(p1)]
    p1rgb = hex_to_rgb(p1hex)
    if isinstance(p2, int):
        p2hex = color_list[int(p2)]
        p2rgb = hex_to_rgb(p2hex)
    if isinstance(p3, int):
        p3hex = color_list[int(p3)]
        p3rgb = hex_to_rgb(p3hex)
    if p2rgb is not None and p3rgb is not None:
        rgbAvg = np.average(np.array(p1rgb), np.array(p2rgb), np.array(p3rgb))
    elif p2rgb is not None:
        rgbAvg = np.average(np.array(p1rgb), np.array(p2rgb))
    else:
        rgbAvg = p1rgb
    hexAvg = rgb_to_hex(rgbAvg[0], rgbAvg[1], rgbAvg[2])

    return hexAvg


def reader_3mf(path, mesh=None):
    namespace = {"3mf": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02",
                 "m": "http://schemas.microsoft.com/3dmanufacturing/material/2015/02"}

    archive = zipfile.ZipFile(path, "r")
    root = ET.parse(archive.open("3D/3dmodel.model"))
    color_list = list()
    colors = root.findall('.//m:color', namespace)
    if colors:
        for color in colors:
            color_list.append(color.get("color", 0))

    obj_meshs = list()
    objects = root.findall("./3mf:resources/3mf:object", namespace)

    centroid = []
    for c, obj in enumerate(objects):
        if not obj.findall(".//3mf:mesh", namespace):
            continue
        obj_meshs.append(dict())

        objectid = obj.get("id")
        obj_meshs[c]["objectid"] = objectid

        vertex_list = []
        triangle_list = []
        obj_meshs[c]["Mesh"] = list()
        obj_meshs[c]["Color"] = list()
        obj_meshs[c]["Center"] = list()
        # for vertex in object.mesh.vertices.vertex:
        for vertex in obj.findall(".//3mf:vertex", namespace):
            vertex_list.append([vertex.get("x"), vertex.get("y"), vertex.get("z")])
        print('Number of vertices: ' + str(len(vertex_list)))

        triangles = obj.findall(".//3mf:triangle", namespace)
        # for triangle in object.mesh.triangles.triangle:
        for triangle in triangles:
            v1 = int(triangle.get("v1"))
            v2 = int(triangle.get("v2"))
            v3 = int(triangle.get("v3"))
            triangle_list.append([v1, v2, v3])
            p1 = (triangle.get("p1"))
            p2 = (triangle.get("p2"))
            p3 = (triangle.get("p3"))
            tricolor = color_avg(color_list, p1, p2, p3)
            obj_meshs[c]["Mesh"].append([float(vertex_list[v1][0]), float(vertex_list[v1][1]), float(vertex_list[v1][2])])
            obj_meshs[c]["Mesh"].append([float(vertex_list[v2][0]), float(vertex_list[v2][1]), float(vertex_list[v2][2])])
            obj_meshs[c]["Mesh"].append([float(vertex_list[v3][0]), float(vertex_list[v3][1]), float(vertex_list[v3][2])])
            obj_meshs[c]["Color"].append(tricolor)
            cent_x = (float(vertex_list[v1][0]) + float(vertex_list[v2][0]) + float(vertex_list[v3][0])) / 3.0
            cent_y = (float(vertex_list[v1][1]) + float(vertex_list[v2][1]) + float(vertex_list[v3][1])) / 3.0
            cent_z = (float(vertex_list[v1][2]) + float(vertex_list[v2][2]) + float(vertex_list[v3][2])) / 3.0
            centroid.append([cent_x, cent_y, cent_z, tricolor])
            obj_meshs[c]["Center"].append([cent_x, cent_y, cent_z])

    tri_color = [[c[0], c[1], c[2]] + list(ImageColor.getcolor(c[3], "RGB")[0:3]) for c in centroid]

    point_color = None
    if mesh is not None:
        faces = mesh.faces.reshape(int(len(mesh.faces)/4), 4)[:, 1:]
        point_color = np.zeros((len(mesh.points), 3))
        for ii, f in enumerate(faces):
            point_color[f[0]] = tri_color[ii][3:]
            point_color[f[1]] = tri_color[ii][3:]
            point_color[f[2]] = tri_color[ii][3:]

    return tri_color, point_color


if __name__ == '__main__':
    pass
