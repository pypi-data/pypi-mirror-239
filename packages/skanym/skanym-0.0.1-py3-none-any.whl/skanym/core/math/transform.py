from __future__ import annotations
import numpy as np
import quaternion
import warnings

from skanym.core.math.constants import LOW_A_TOL, LOW_R_TOL


class Transform:
    """A class to represent a Transformation in 3D space composed by
    a translation and a rotation.

    np.quaternion is used to represent quaternions.

    Here are a few static values to declare common quaternions:

    - quaternion.one = np.quaternion(1, 0, 0, 0) -> identity quaternion

    - quaternion.x = np.quaternion(0, 1, 0, 0) -> 180 degree rotation around x axis

    - quaternion.y = np.quaternion(0, 0, 1, 0) -> 180 degree rotation around y axis

    - quaternion.z = np.quaternion(0, 0, 0, 1) -> 180 degree rotation around z axis

    Attributes
    ----------
    pos : ndarray (float)
        1D array containing the 3 values for the position in this order [x, y, z].
    orient : numpy quaternion
        Quaternion object defining the orientation.

        More info on numpy quaternion here: https://quaternion.readthedocs.io/en/latest/#
    identity : Transform
        Static attribute for the identity transform.

    Notes
    ----------
    Scale is not supported.
    """

    def __init__(self, pos=np.zeros(3), orient=quaternion.one):
        """**Default constructor for the Transform class.**

        Parameters
        ----------
        pos : (float) ndarray, optional
            1D array containing the 3 values for the transform's position, by default [0, 0, 0].
        orient : np.quaternion, optional
            Quaternion object defining the transform's orientation, by default identity quaternion.
        """
        self.pos = pos
        self.orient = orient
        if not self.quaternion_is_unit():
            warnings.warn(
                "Transform built with non unit quaternion. A normalization might be necessary. See Transform.normalize_quaternion().",
                stacklevel=2,
            )

    @classmethod
    def from_matrix(cls, matrix=np.eye(4)):
        """Transform constructor from 4x4 transform matrix.

        Parameters
        ----------
        matrix : (float) ndarray, optional
            4x4 transformation matrix from which to extract position vector and orientation quaternion, by default 4x4 identity matri).

        Returns
        -------
        Transform
            Transform object.
        """
        matrix = np.array(matrix)
        if matrix.shape != (4, 4) and matrix.shape != (3, 3):
            raise (
                IndexError(
                    "Improper array shape for extracing Quaternion. Expected array of shape (4,4) or (3,3) instead of {}".format(
                        matrix.shape
                    )
                )
            )

        diagonal = matrix[0][0] + matrix[1, 1] + matrix[2, 2]
        if diagonal > 0:
            w4 = np.sqrt(diagonal + 1) * 2
            w = w4 / 4
            x = (matrix[2, 1] - matrix[1, 2]) / w4
            y = (matrix[0, 2] - matrix[2, 0]) / w4
            z = (matrix[1, 0] - matrix[0, 1]) / w4
        elif (matrix[0, 0] > matrix[1, 1]) and (matrix[0, 0] > matrix[2, 2]):
            x4 = np.sqrt(1 + matrix[0, 0] - matrix[1, 1] - matrix[2, 2]) * 2
            w = (matrix[2, 1] - matrix[1, 2]) / x4
            x = x4 / 4
            y = (matrix[0, 1] + matrix[1, 0]) / x4
            z = (matrix[0, 2] + matrix[2, 0]) / x4
        elif matrix[1, 1] > matrix[2, 2]:
            y4 = np.sqrt(1 + matrix[1, 1] - matrix[0, 0] - matrix[2, 2]) * 2
            w = (matrix[0, 2] - matrix[2, 0]) / y4
            x = (matrix[0, 1] + matrix[1, 0]) / y4
            y = y4 / 4
            z = (matrix[1, 2] + matrix[2, 1]) / y4
        else:
            z4 = np.sqrt(1 + matrix[2, 2] - matrix[0, 0] - matrix[1, 1]) * 2
            w = (matrix[1, 0] - matrix[0, 1]) / z4
            x = (matrix[0, 2] + matrix[2, 0]) / z4
            y = (matrix[1, 2] + matrix[2, 1]) / z4
            z = z4 / 4

        v = matrix[0:3, 3]
        q = np.quaternion(w, x, y, z)
        return cls(v, q)

    def as_matrix(self):
        """Returns the 4x4 transformation matrix for the transform.

        Returns
        -------
        ndarray (float)
            4x4 transformation matrix.

        Note
        ----
        The matrix is in column-major order.
        """
        t_matrix = np.eye(4)
        t_matrix[0:3, 0:3] = quaternion.as_rotation_matrix(self.orient)

        t_matrix[0:3, 3] = self.pos
        return t_matrix

    def normalize_quaternion(self):
        """Normalizes the quaternion of the transform."""
        self.orient = self.orient.normalized()

    def quaternion_is_unit(self):
        """Checks if the quaternion for the transform's orientation is unitary.

        Returns
        -------
        bool
            True if the quaternion is unitary, False otherwise.
        """
        return np.isclose(
            np.linalg.norm(quaternion.as_float_array(self.orient)),
            1,
            rtol=LOW_R_TOL,
            atol=LOW_A_TOL,
        )

    def inversed(self):
        """Returns the inverse of the transform.

        Returns
        -------
        Transform
            Inverse transform.
        """
        return Transform.from_matrix(np.linalg.inv(self.as_matrix()))

    def multiply_by(self, other: Transform):
        """Generates a Transform that is the result of the multiplication of two transforms.

        Parameters
        ----------
        other : Transform
            Transform to multiply by.

        Returns
        -------
        Transform
            Resulting Transform. Corresponds to a transformation by the second matrix (other) followed by a transformation by the first matrix (self).
        """
        self_orient_norm = np.linalg.norm(quaternion.as_float_array(self.orient))
        other_orient_norm = np.linalg.norm(quaternion.as_float_array(other.orient))
        if not np.allclose(
            [self_orient_norm, other_orient_norm],
            [1.0, 1.0],
            rtol=LOW_R_TOL,
            atol=LOW_A_TOL,
        ):
            warnings.warn(
                "Transform multiplication attempted with non unit quaternions. This can lead to erroneous results.",
                stacklevel=2,
            )

        return Transform.from_matrix(np.matmul(self.as_matrix(), other.as_matrix()))

    def translate(self, pos_vector: np.ndarray):
        """Translates the transform by the given position vector.

        Parameters
        ----------
        pos_vector : ndarray (float)
            1D array containing the 3 values for the translation.

        Returns
        -------
        Transform
            Translated transform.
        """
        translation_transform = Transform(pos=pos_vector)
        return self.multiply_by(translation_transform)

    def rotate_quaternion(self, q):
        """Rotates the transform by the given quaternion.

        Parameters
        ----------
        quaternion : np.quaternion
            Quaternion to rotate by.

        Returns
        -------
        Transform
            Rotated transform.
        """
        rotation_transform = Transform(orient=q)
        return self.multiply_by(rotation_transform)

    @classmethod
    def quaternion_as_exp_map(self, q):
        """Returns the quaternion as an exponential map.
        If the quaternion is within a tolerance of the identity quaternion,
        the exponential map is approximated to be the vector part of the quaternion.

        Returns
        -------
        ndarray (float)
            1D array containing the 3 values for the exponential map.
        """
        return quaternion.as_rotation_vector(q)
        
        # Custom method (DEPRECATED)
        # norm = np.sqrt(self.orient.x**2 + self.orient.y**2 + self.orient.z**2)

        # if np.isclose(norm, 0, rtol=LOW_R_TOL, atol=LOW_A_TOL):
        #     return np.array([self.orient.x, self.orient.y, self.orient.z])
        # else:
        #     halfangle = np.arctan2(norm, self.orient.w)
        #     return halfangle * (np.array([self.orient.x, self.orient.y, self.orient.z]) / norm)
    
    @classmethod
    def quaternion_from_exp_map(self, exp_map):
        """Returns the quaternion from an exponential map.
        If the exponential map norm is within a tolerance of 0,
        the real part (w) of the quaternion is approximated to be 1, before normalization.

        Parameters
        ----------
        exp_map : ndarray (float)
            1D array containing the 3 values for the exponential map.

        Returns
        -------
        np.quaternion
            Quaternion corresponding to the exponential map.
        """

        return quaternion.from_rotation_vector(exp_map)
    
        # Custom method (DEPRECATED)
        halfangle = np.sqrt(exp_map[0]**2 + exp_map[1]**2 + exp_map[2]**2)

        if np.isclose(halfangle, 0, rtol=LOW_R_TOL, atol=LOW_A_TOL):
            return np.quaternion(1, exp_map[0], exp_map[1], exp_map[2]).normalized()
        else:
            c = np.cos(halfangle)
            s = np.sin(halfangle) / halfangle
            return np.quaternion(c, s * exp_map[0], s * exp_map[1], s * exp_map[2]).normalized()
 
    @classmethod
    def quaternion_distance(self, q1, q2):
        """
        Calculate the distance between two quaternions.

        Parameters:
        q1 (numpy.ndarray): The first quaternion as a numpy array [w, x, y, z].
        q2 (numpy.ndarray): The second quaternion as a numpy array [w, x, y, z].

        Returns:
        float: The quaternion distance between q1 and q2.
        """
        # Calculate the dot product between the two quaternions
        dot_product = np.dot(quaternion.as_float_array(q1), quaternion.as_float_array(q2))

        # The quaternion distance
        distance = 1 - dot_product**2

        return distance

    @staticmethod
    def lerp(t1: Transform, t2: Transform, progress: float):
        """Linear interpolation between two transforms.

        Parameters
        ----------
        t1 : Transform
            First transform.
        t2 : Transform
            Second transform.
        progress : float
            Progress between 0 and 1.

        Returns
        -------
        Transform
            Transform linearly interpolated between t1 and t2.
        """
        px = np.interp(progress, [0, 1], [t1.pos[0], t2.pos[0]])
        py = np.interp(progress, [0, 1], [t1.pos[1], t2.pos[1]])
        pz = np.interp(progress, [0, 1], [t1.pos[2], t2.pos[2]])
        p = np.array([px, py, pz])
        return Transform(p, quaternion.slerp(t1.orient, t2.orient, 0, 1, progress))

    def __eq__(self, other):
        """Equality operator for Transform objects.

        Parameters
        ----------
        other : Transform
            Transform object to compare to.

        Returns
        -------
        Bool
            True if the 3 values for positions and the 4 values for quaternions are "equal" to each other. False otherwise.

        Note
        ----
        Equality for floating point values is defined as being within a tolerance.
        Tolerance values are defined in the constants.py file.
        Lower tolerance values are used here for more accurate equality.
        """
        if not isinstance(other, Transform):
            return NotImplemented
        return np.allclose(
            self.as_matrix(), other.as_matrix(), rtol=LOW_R_TOL, atol=LOW_A_TOL
        )

    def __matmul__(self, other: Transform):
        """Matrix multiplication operator for Transform objects.

        Overrides the default matrix multiplication operator `@` for Transform objects.

        Parameters
        ----------
        other : Transform
            Transform object to multiply by.

        Returns
        -------
        Transform
            Resulting transform.
        """
        return self.multiply_by(other)

    def __repr__(self):
        return f"Transform({str(self.pos)}, {(self.orient)})"


identity = Transform()


if __name__ == "__main__":
    r1 = np.array([-0.6782, 0.0142, 0.0279])
    r2 = np.array([0.1054, -0.0562, 0.0417])

    q1 = Transform.quaternion_from_exp_map(r1)
    q2 = Transform.quaternion_from_exp_map(r2)
    t1 = Transform(orient=q1)
    t2 = Transform(orient=q2)

    print(quaternion.as_float_array(q1).round(3))
    v1 = quaternion.as_float_array(quaternion.from_rotation_vector(r1))
    print(v1.round(3))  
    print() 
    print(quaternion.as_float_array(q2).round(3))
    v2 = quaternion.as_float_array(quaternion.from_rotation_vector(r2))
    print(v2.round(3))
    # print(quaternion.as_rotation_vector(q2))
    # print(t2.quaternion_as_exp_map())
    # print(Transform.quaternion_from_exp_map(t2.quaternion_as_exp_map()))