# MIT License
#
# Copyright (c) 2023 Dechin CHEN
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import sys
sys.path.insert(0, '..')
import numpy as np
from .np_functions import multiply, hamiltonian, transform
from hadder.parsers import read_pdb, gen_pdb


def rotate(pdb_in, pdb_out, o1, x1, m1):
    """ Rotate the coordinates in pdb input file.
    Args:
        pdb_in: The file path of input pdb file.
        pdb_out: The file path of output pdb file.
        o1: The new origin point under original axis.
        x1: The new x-axis.
        m1: A random point in new x-y plane but not along ox axis.

    Returns:
        new_crds: The new coordinates after rotation.
    """
    pdb_obj = read_pdb(pdb_in)
    crds = pdb_obj[6]
    atom_names = pdb_obj[5]
    res_names = pdb_obj[7]
    res_ids = pdb_obj[8]

    ox = np.array([1, 0, 0], np.float32)
    oy = np.array([0, 1, 0], np.float32)
    oz = np.array([0, 0, 1], np.float32)

    x = x1 - o1
    x /= np.linalg.norm(x)
    z = np.cross(x, m1 - o1)
    z /= np.linalg.norm(z)

    transform1 = transform(x, ox)
    transform1 /= np.linalg.norm(transform1)
    tz = hamiltonian(transform1, z)
    transform2 = transform(tz, oz)
    transform2 /= np.linalg.norm(transform2)
    t = multiply(transform2, transform1)

    new_crds = hamiltonian(t, crds - o1)[:, 1:]
    gen_pdb(new_crds, atom_names, res_names, res_ids, pdb_name=pdb_out)

    return new_crds
