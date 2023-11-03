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
from quaternion.np_functions import multiply, hamiltonian, transform
from hadder.parsers import read_pdb, gen_pdb


# pdb_name = '1ox5_average.mc.pdb'
pdb_name = '1gpw_average.mc.pdb'
pdb_out = pdb_name.replace('mc', 'out')
pdb_obj = read_pdb(pdb_name)
crds = pdb_obj[6]
atom_names = pdb_obj[5]
res_names = pdb_obj[7]
res_ids = pdb_obj[8]

ox = np.array([1, 0, 0], np.float32)
oy = np.array([0, 1, 0], np.float32)
oz = np.array([0, 0, 1], np.float32)

# o1 = np.array([57.492, 19.142, 20.385], np.float32)
# x1 = np.array([56.536, 6.920, 15.611], np.float32)
# m1 = np.array([67.224, 39.124, 17.261], np.float32)

o1 = np.array([42.882, 32.025, 38.245], np.float32)
x1 = np.array([38.326, 24.174, 48.484], np.float32)
m1 = np.array([53.187, 51.701, 33.301], np.float32)

x = x1-o1
x /= np.linalg.norm(x)
z = np.cross(x, m1-o1)
z /= np.linalg.norm(z)

# transform1 = transform(ox, x)
# transform1 /= np.linalg.norm(transform1)
# tz = hamiltonian(transform1, oz)
# transform2 = transform(tz, z)
# transform2 /= np.linalg.norm(transform2)
# t = multiply(transform2, transform1)

transform1 = transform(x, ox)
transform1 /= np.linalg.norm(transform1)
tz = hamiltonian(transform1, z)
transform2 = transform(tz, oz)
transform2 /= np.linalg.norm(transform2)
t = multiply(transform2, transform1)

new_crds = hamiltonian(t, crds-o1)[:, 1:]

gen_pdb(new_crds[None], atom_names, res_names, res_ids, pdb_name=pdb_out)
