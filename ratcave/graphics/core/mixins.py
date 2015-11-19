__author__ = 'nickdg'

import numpy as np
from . import _transformations as transformations


class Color(object):

    def __init__(self, r, g, b, a=1.):
        """Color object, defines rgba attributes"""
        self.r, self.g, self.b, self.a = r, g, b, a

    @property
    def rgb(self):
        return self.r, self.g, self.b

    @rgb.setter
    def rgb(self, value):
        self.r, self.g, self.b = value

    @property
    def rgba(self):
        return self.r, self.g, self.b, self.a

    @rgba.setter
    def rgba(self, value):
        self.r, self.g, self.b, self.a = value


class Physical(object):


    def __init__(self, position=(0., 0., 0.), rotation=(0., 0., 0.), scale=1.):
        """XYZ Position, Scale and XYZEuler Rotation Class.

        Args:
            position (list): (x, y, z) translation values.
            rotation (list): (x, y, z) rotation values
            scale (float): uniform scale factor. 1 = no scaling.
        """
        self.position = list(position)
        self.rotation = list(rotation)
        self.scale = scale

    @property
    def model_matrix(self):
        """The 4x4 model matrix."""

        # Set Model and Normal Matrices
        trans_mat = transformations.translation_matrix(self.position)

        rot_x_mat = transformations.rotation_matrix(np.radians(self.rotation[0]), [1, 0, 0])
        rot_y_mat = transformations.rotation_matrix(np.radians(self.rotation[1]), [0, 1, 0])
        rot_z_mat = transformations.rotation_matrix(np.radians(self.rotation[2]), [0, 0, 1])
        rot_mat = np.dot(np.dot(rot_z_mat,rot_y_mat), rot_x_mat)

        scale_mat = transformations.scale_matrix(self.scale)

        return np.dot(np.dot(trans_mat, rot_mat), scale_mat)

    @property
    def normal_matrix(self):
        """The 4x4 normal matrix, which is the inverse of the transpose of the model matrix."""
        return np.linalg.inv(self.model_matrix.T)

    @property
    def view_matrix(self):
        """The 4x4 view matrix."""
        # Set View Matrix
        trans_mat = transformations.translation_matrix([-el for el in self.position])

        rot_x_mat = transformations.rotation_matrix(np.radians(-self.rotation[0]), [1, 0, 0])
        rot_y_mat = transformations.rotation_matrix(np.radians(-self.rotation[1]), [0, 1, 0])
        rot_z_mat = transformations.rotation_matrix(np.radians(-self.rotation[2]), [0, 0, 1])
        rot_mat = np.dot(np.dot(rot_x_mat, rot_y_mat), rot_z_mat)

        try:
            return np.dot(rot_mat, trans_mat)
        except:
            import pdb
            pdb.set_trace()

