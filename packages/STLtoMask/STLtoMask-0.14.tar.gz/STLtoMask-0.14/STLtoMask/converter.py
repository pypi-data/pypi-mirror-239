"""
Morfeus lab
The University of Texas
MD Anderson Cancer Center
Author - Caleb O'Connor
Email - csoconnor@mdanderson.org

Description:
    Create a 3D image based off of an STL file and user defined spacing. Additional, options exist for rotating the
    mesh, adding a 3MF file to create a "color-intensity" on the surface of the image, and flipping the iamge and
    mesh along the vertical axial plane.

    Required inputs:
        - STL file input
        - Output directory
        - Spacing in [x, y, z]

    Optional inputs:
        - 3MF file used to add different intensities to the mask based on the color surface of the mesh. The module
          assumes the STL and 3MF have the same nodes/triangles.
        - Rotation allows the mesh to be rotated, this is useful for medical images where the user will want the mesh to
          have the correct orientation along the z-axis (head-toe or toe-head). This module is for when the user
          already knows what rotations to apply, if unknown I suggest testing in pyvista with different rotation and
          plotting the results.
        - Flip the mask and mesh along the vertical plane in the axial plane.

    Note:
        Adding a color file will greatly increase the computation time. Difficult to approximate total time be roughly
        45 minutes for 1,000,000 node mesh.

"""

import os
import cv2
import time

import numpy as np
import pyvista as pv
import SimpleITK as sitk

from STLtoMask.color_reader import reader_3mf


def export_images(mask, final_mesh, expand_bounds, spacing, output_path):
    """
    Export mask and STL file (in case it has been edited). The mask is converted to an image and origin/spacing are
    added. Both files are checked to make sure they don't exist, if they do the file is renamed with a number added to
    the end.

    Note: This is added to the end of the MHD file "ElementNumberOfChannels", this is a RayStation requirement.

    :param mask: output mask
    :param final_mesh: output mesh
    :param expand_bounds: mask origin
    :param spacing: output mask spacing
    :param output_path: output directory
    :return:
    """
    image = sitk.GetImageFromArray(np.short(mask))
    image.SetSpacing(spacing)
    image.SetOrigin([expand_bounds[0], expand_bounds[2], expand_bounds[4]])

    n = 0
    mhd_file = 'MaskFromSTL'
    while os.path.exists(os.path.join(output_path, mhd_file + '.mhd')):
        n += 1
        mhd_file = 'MaskFromSTL_' + '0' + str(n)

    n = 0
    stl_file = 'ReferenceSTL'
    while os.path.exists(os.path.join(output_path, stl_file + '.stl')):
        n += 1
        stl_file = 'ReferenceSTL_' + '0' + str(n)

    sitk.WriteImage(image, os.path.join(output_path, mhd_file + '.mhd'))
    time.sleep(3)
    file = open(os.path.join(output_path, mhd_file + '.mhd'), "a")
    file.write("ElementNumberOfChannels = 1" + "\n")
    file.close()

    final_mesh.save(os.path.join(output_path, stl_file + '.stl'))


def create_boundary(bounds, spacing):
    """
    expand_bounds:
    Takes the original bounding box and expands it by 5*spacing on both ends (so for 1 mm spacing on each direction the
    box would be expanded by 5 mm in all direction.

    slice_location:
    A list containing each z-slice coordinate.

    dim:
    A list that represents the size of the mask in [z, x, y]

    :param bounds: mesh boundary box, represents the min-max [xi, xf, yi, yf, zi, zf] coordinates to box the entire STL
    :param spacing: size the output mask will be
    :return:
    """
    expand_bounds = [int(bounds[0] - 5 * spacing[0]), int(bounds[1] + 5 * spacing[0]),
                     int(bounds[2] - 5 * spacing[1]), int(bounds[3] + 5 * spacing[1]),
                     int(bounds[4] - 5 * spacing[2]), int(bounds[5] + 5 * spacing[2])]

    slice_location = [i for i in range(expand_bounds[4], expand_bounds[5], spacing[2])]
    dim = [len(slice_location), expand_bounds[1] - expand_bounds[0] + 1, expand_bounds[3] - expand_bounds[2] + 1]

    return expand_bounds, slice_location, dim


def add_color(mask, mesh, point_color, spacing):
    """
    Takes any mask coordinate that has a 0 adjacent to it, this is a rough estimate for the mask surface. The surface
    coordinates are transformed back to physical coordinates i.e millimeters. A distance calculation is performed
    against all the points on the mesh surface, the shortest distance is used as the color index for the point in the
    mask.

    :param mask:
    :param mesh:
    :param point_color:
    :param spacing:
    :return:
    """
    points = np.asarray(mesh.points)
    org_bounds = np.round(mesh.bounds, 2)
    expand_bounds, slice_location, dim = create_boundary(org_bounds, spacing)

    coord = []
    for ii, s in enumerate(slice_location):
        if np.sum(mask[ii, :, :]) > 0:
            for jj in range(dim[2]):
                for kk in range(dim[1]):
                    if mask[ii, jj, kk] == 1:
                        if np.sum(mask[ii-1:ii+2, jj-1:jj+2, kk-1:kk+2]) < 27:
                            coord.append([ii, jj, kk])

    for ii, c in enumerate(coord):
        location = [(c[2] * spacing[0]) + expand_bounds[0],
                    (c[1] * spacing[1]) + expand_bounds[2],
                    slice_location[c[0]]]
        point_sub = points - location
        dist = np.sqrt(point_sub[:, 0]**2 + point_sub[:, 1]**2 + point_sub[:, 2]**2)
        point_idx = np.argmin(dist)
        color_sum = np.round(10*np.sum(point_color[point_idx])/(255+255+255))
        mask[c[0], c[1], c[2]] = color_sum

    return mask


def create_mask(temp_mesh, spacing):
    """
    Two main parts when converting an unstructured dataset to a structured one:
    1) The mesh needs to be sliced to create contours, for this case the mesh is sliced at equal spaced coordinates
       determined by input spacing criteria (calculated in the create_boundary function). Pyvista's slice feature is
       used for this. The x-y coordinates are then converted to grid coordinates.
       Example:
        A x coordinate is at 10 mm, the expand_bounds minimum value is 1 mm, and the spacing is 2 mm. Where would the x
        coordinate exist on the new structured grid?
            10-1 = the x is 9 mm from the start but the grid will be in 2 mm cuts, so it will be at 4.5.
        If the spacing was 1mm then the x would be in the 9th block. You can think of it as city blocks, the blocks
        themselves have a physical distance but people will often say 3 blocks down the road.

    2) This converts the contours into a filled mask at the 2D level, so the process is done slice-by-slice then
       combined to create a 3D mask. This is performed using opencv-python (cv2) fillPoly.

    :param temp_mesh: input STL
    :param spacing: size the output mask will be
    :return:
    """
    com = temp_mesh.center
    org_bounds = np.round(temp_mesh.bounds, 2)
    expand_bounds, slice_location, dim = create_boundary(org_bounds, spacing)

    contours = []
    for s in slice_location:
        if org_bounds[4] < s < org_bounds[5]:
            hold_contour = temp_mesh.slice(normal='z', origin=[com[0], com[1], s])
            contours.append((np.asarray(hold_contour.points)[:, 0:2] -
                             (expand_bounds[0], expand_bounds[2]))/(spacing[0:2]))
        else:
            contours.append([])

    mask = np.zeros((dim[0], dim[2], dim[1]))
    for ii, s in enumerate(slice_location):
        if len(contours[ii]) > 0:
            frame = np.zeros((dim[2], dim[1]))
            # noinspection PyTypeChecker
            cv2.fillPoly(frame,  np.array([contours[ii]], dtype=np.int32), 1)
            mask[ii, :, :] = mask[ii, :, :] + frame

    return mask, expand_bounds


def mesh_rotation(temp_mesh, rotation):
    """
    Gets the rotation order as a list (rotation_order) and the amount per each rotation (rotation_amount). Loops 3 times
    if rotation_amount is not zero then a rotation is performed using pyvistas rotate_ function. The inplace=True means
    the variable itself will be updated.

    :param temp_mesh: input STL
    :param rotation: dictionary explaining rotation order and amount, example: {'zxy': [50, -7, 0]}
    :return:
    """
    rotation_order = list(rotation.keys())[0]
    rotation_amount = rotation[rotation_order]
    for ii in range(3):
        if rotation_amount[ii] != 0:
            if rotation_order[ii] == 'x':
                temp_mesh.rotate_x(rotation_amount[ii], point=temp_mesh.center, inplace=True)
            elif rotation_order[ii] == 'y':
                temp_mesh.rotate_y(rotation_amount[ii], point=temp_mesh.center, inplace=True)
            else:
                temp_mesh.rotate_z(rotation_amount[ii], point=temp_mesh.center, inplace=True)

    return temp_mesh


def stl_to_mask(input_path, output_path, spacing, three_mf=None, rotation=None, flip=False):
    """
    This is the main function that reads in the STL, calls mesh_rotation function for applying rotations if they exist,
    create_mask for making the mask, lastly if a 3MF file then color intensity is applied to the surface of the mask.

    There is a flip feature which will flip the mask and mesh along the vertical plane in the axial plane.

    :param input_path: path to STL file
    :param output_path: path where the
    :param spacing: mask output spacing as a list [1, 1, 1] (x, y, z)
    :param three_mf: 3mf file to add intensity to the mask
    :param rotation: rotation in dictionary form indicating order ex: {yxz: [10, 30, 0}, meaning rotate y=10 degrees
                     then x=30 degrees
    :param flip: flips axial plane along the vertical line
    :return:
    """
    reader = pv.get_reader(input_path)
    org_mesh = reader.read()

    if rotation is not None:
        mesh = mesh_rotation(org_mesh, rotation)
    else:
        mesh = org_mesh

    mask, expand_bounds = create_mask(mesh, spacing)

    if three_mf is not None:
        tri_color, point_color = reader_3mf(three_mf, org_mesh)
        final_mask = add_color(mask, mesh, point_color, spacing)
    else:
        final_mask = mask

    if flip:
        flip_mask = np.flip(final_mask, 2)
        flip_mesh = mesh.reflect((1, 0, 0), point=mesh.center)
        export_images(flip_mask, flip_mesh, expand_bounds, spacing, output_path)
    else:
        export_images(final_mask, mesh, expand_bounds, spacing, output_path)


if __name__ == "__main__":
    pass

