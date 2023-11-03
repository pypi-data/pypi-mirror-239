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


import numpy as np


def multiply(t1, t2):
    if isinstance(t1, (int, float)):
        t1 = np.array([t1], np.float32)
    if isinstance(t2, (int, float)):
        t2 = np.array([t2], np.float32)
    # (1,)x(1,)->(1,)
    # (1,)x(3,)->(3,)
    # (1,)x(4,)->(3,)
    # (1,)x(B,3)->(B,3)
    # (1,)x(B,4)->(B,3)
    if t1.size == 1 or t2.size == 1:
        return t1 * t2
    if t1.shape[-1] == 3 and t2.shape[-1] == 3:
        # (3,)x(3,)->(4,)
        if t1.ndim == 1 and t2.ndim == 1:
            s = np.dot(t1, t2)
        # (3,)x(B,3)->(B,4)
        elif t1.ndim == 1 and t2.ndim == 2:
            s = np.einsum('j,ij->i', t1, t2)[..., None]
        # (B,3)x(3,)->(B,4)
        elif t1.ndim == 2 and t2.ndim == 1:
            s = np.einsum('ij,j->i', t1, t2)[..., None]
        # (B,3)x(B,3)->(B,4)
        elif t1.ndim == 2 and t2.ndim == 2:
            s = np.einsum('ij,ij->i', t1, t2)[..., None]
        v = np.cross(t1, t2, axisc=-1)
        return np.hstack((-s, v))
    if t1.shape[-1] == 4 or t2.shape[-1] == 4:
        # (3,)x(4,)->(4,)
        if t1.shape[-1] == 3 and t1.ndim == 1 and t2.ndim == 1:
            st2 = t2[0]
            s = np.dot(t1, t2[1:])
            v = np.cross(t1, t2[1:], axisc=-1) + st2 * t1
        # (4,)x(3,)->(4,)
        elif t2.shape[-1] == 3 and t1.ndim == 1 and t2.ndim == 1:
            st1 = t1[0]
            s = np.dot(t1[1:], t2)
            v = np.cross(t1[1:], t2, axisc=-1) + st1 * t2
        # (4,)x(4,)->(4,)
        elif t1.ndim == 1 and t2.ndim == 1:
            st1 = t1[0]
            st2 = t2[0]
            s = np.dot(t1[1:], t2[1:]) - st1 * st2
            v = np.cross(t1[1:], t2[1:], axisc=-1) + st1 * t2[1:] + st2 * t1[1:]
        # (B,3)x(4,)->(B,4)
        # (B,4)x(4,)->(B,4)
        elif t1.ndim == 2 and t2.ndim == 1:
            if t1.shape[-1] == 3:
                t1 = np.pad(t1, ((0, 0), (1, 0)), mode='constant', constant_values=0)
            t2 = np.pad(t2[None], ((0, t1.shape[0] - 1), (0, 0)), mode='wrap')
            st1 = t1[:, [0]]
            st2 = t2[:, [0]]
            s = np.einsum('ij,ij->i', t1[:, 1:], t2[:, 1:])[..., None] - st1 * st2
            v = np.cross(t1[:, 1:], t2[:, 1:], axisc=-1) + st1 * t2[:, 1:] + st2 * t1[:, 1:]
        # (B,3)x(B,4)->(B,4)
        # (B,4)x(B,3)->(B,4)
        # (B,4)x(B,4)->(B,4)
        elif t1.ndim == 2 and t2.ndim == 2:
            if t1.shape[-1] == 3:
                t1 = np.pad(t1, ((0, 0), (1, 0)), mode='constant', constant_values=0)
            if t2.shape[-1] == 3:
                t2 = np.pad(t2, ((0, 0), (1, 0)), mode='constant', constant_values=0)
            st1 = t1[:, [0]]
            st2 = t2[:, [0]]
            s = np.einsum('ij,ij->i', t1[:, 1:], t2[:, 1:])[..., None] - st1 * st2
            v = np.cross(t1[:, 1:], t2[:, 1:], axisc=-1) + st1 * t2[:, 1:] + st2 * t1[:, 1:]
        return np.hstack((-s, v))
    return 0


def add(t1, t2):
    if isinstance(t1, (int, float)):
        t1 = np.array([t1], np.float32)
    if isinstance(t2, (int, float)):
        t2 = np.array([t2], np.float32)
    # (D,)+(D,)->(4,)
    if t1.ndim == 1 and t2.ndim == 1:
        if t1.shape[-1] == 1:
            t1 = np.pad(t1, ((0, 3)), mode='constant', constant_values=0)
        elif t1.shape[-1] == 3:
            t1 = np.pad(t1, ((1, 0)), mode='constant', constant_values=0)
        if t2.shape[-1] == 1:
            t2 = np.pad(t2, ((0, 3)), mode='constant', constant_values=0)
        elif t2.shape[-1] == 3:
            t2 = np.pad(t2, ((1, 0)), mode='constant', constant_values=0)
    # (B,D)+(D,)->(B,4)
    # (D,)+(B,D)->(B,4)
    # (B,D)+(B,D)->(B,4)
    if t1.ndim == 2 or t2.ndim == 2:
        # (D,)->(B,D)
        if t1.ndim == 1:
            t1 = np.pad(t1[None], ((0, t2.shape[0]-1), (0, 0)), mode='wrap')
        if t2.ndim == 1:
            t2 = np.pad(t2[None], ((0, t1.shape[0]-1), (0, 0)), mode='wrap')
        # (B,D)->(B,4)
        if t1.shape[-1] == 1:
            t1 = np.pad(t1, ((0, 0), (0, 3)), mode='constant', constant_values=0)
        elif t1.shape[-1] == 3:
            t1 = np.pad(t1, ((0, 0), (1, 0)), mode='constant', constant_values=0)
        if t2.shape[-1] == 1:
            t2 = np.pad(t2, ((0, 0), (0, 3)), mode='constant', constant_values=0)
        elif t2.shape[-1] == 3:
            t2 = np.pad(t2, ((0, 0), (1, 0)), mode='constant', constant_values=0)
    return t1 + t2


def inverse(t):
    if isinstance(t, (int, float)):
        t = np.array([t, 0, 0, 0], np.float32)
    # (D,)->(4,)
    if t.ndim == 1:
        if t.shape[-1] == 1:
            return t
        if t.shape[-1] == 3:
            return -t
        s = t[[0]]
        v = -t[1:]
    # (B,D)->(B,4)
    if t.ndim == 2:
        if t.shape[-1] == 1:
            t = np.pad(t, ((0, 0), (0, 3)), mode='constant', constant_values=0)
        if t.shape[-1] == 3:
            t = np.pad(t, ((0, 0), (1, 0)), mode='constant', constant_values=0)
        s = t[:, [0]]
        v = -t[:, 1:]
    return np.hstack((s, v))


def hamiltonian(t1, t2):
    if isinstance(t1, (int, float)):
        t1 = np.array([t1, 0, 0, 0], np.float32)
    if isinstance(t2, (int, float)):
        t2 = np.array([t2, 0, 0, 0], np.float32)
    # (D,)+(D,)->(4,)
    if t1.ndim == 1 and t2.ndim == 1:
        if t1.shape[-1] == 1:
            t1 = np.pad(t1, ((0, 3)), mode='constant', constant_values=0)
        elif t1.shape[-1] == 3:
            t1 = np.pad(t1, ((1, 0)), mode='constant', constant_values=0)
        if t2.shape[-1] == 1:
            t2 = np.pad(t2, ((0, 3)), mode='constant', constant_values=0)
        elif t2.shape[-1] == 3:
            t2 = np.pad(t2, ((1, 0)), mode='constant', constant_values=0)
    # (B,D)+(D,)->(B,4)
    # (D,)+(B,D)->(B,4)
    # (B,D)+(B,D)->(B,4)
    if t1.ndim == 2 or t2.ndim == 2:
        # (D,)->(B,D)
        if t1.ndim == 1:
            t1 = np.pad(t1[None], ((0, t2.shape[0] - 1), (0, 0)), mode='wrap')
        if t2.ndim == 1:
            t2 = np.pad(t2[None], ((0, t1.shape[0] - 1), (0, 0)), mode='wrap')
        # (B,D)->(B,4)
        if t1.shape[-1] == 1:
            t1 = np.pad(t1, ((0, 0), (0, 3)), mode='constant', constant_values=0)
        elif t1.shape[-1] == 3:
            t1 = np.pad(t1, ((0, 0), (1, 0)), mode='constant', constant_values=0)
        if t2.shape[-1] == 1:
            t2 = np.pad(t2, ((0, 0), (0, 3)), mode='constant', constant_values=0)
        elif t2.shape[-1] == 3:
            t2 = np.pad(t2, ((0, 0), (1, 0)), mode='constant', constant_values=0)
    it1 = inverse(t1)
    op1 = multiply(t2, it1)
    return multiply(t1, op1)


def transform(t1, t2):
    if isinstance(t1, (int, float)):
        t1 = np.array([t1], np.float32)
    if isinstance(t2, (int, float)):
        t2 = np.array([t2], np.float32)
    # (D,)+(D,)->(4,)
    if t1.ndim == 1 and t2.ndim == 1:
        if t1.shape[-1] == 1:
            t1 = np.pad(t1, ((0, 3)), mode='constant', constant_values=0)
        elif t1.shape[-1] == 3:
            t1 = np.pad(t1, ((1, 0)), mode='constant', constant_values=0)
        if t2.shape[-1] == 1:
            t2 = np.pad(t2, ((0, 3)), mode='constant', constant_values=0)
        elif t2.shape[-1] == 3:
            t2 = np.pad(t2, ((1, 0)), mode='constant', constant_values=0)
        # (1,)
        s_1 = t1[[0]]
        # (3,)
        v_1 = t1[1:]
        v_2 = t2[1:]
        u = np.cross(v_1, v_2, axisc=-1)
        qs = np.zeros_like(s_1)
        qv = np.zeros_like(v_1)
        qs += np.linalg.norm(v_1, axis=-1, keepdims=True) * np.linalg.norm(v_2, axis=-1, keepdims=True)
        qs += np.dot(v_1, v_2)[..., None]
        qv += u
        q = np.hstack((qs, qv))
    # (B,D)+(D,)->(B,4)
    # (D,)+(B,D)->(B,4)
    # (B,D)+(B,D)->(B,4)
    if t1.ndim == 2 or t2.ndim == 2:
        # (D,)->(B,D)
        if t1.ndim == 1:
            t1 = np.pad(t1[None], ((0, t2.shape[0] - 1), (0, 0)), mode='wrap')
        if t2.ndim == 1:
            t2 = np.pad(t2[None], ((0, t1.shape[0] - 1), (0, 0)), mode='wrap')
        # (B,D)->(B,4)
        if t1.shape[-1] == 1:
            t1 = np.pad(t1, ((0, 0), (0, 3)), mode='constant', constant_values=0)
        elif t1.shape[-1] == 3:
            t1 = np.pad(t1, ((0, 0), (1, 0)), mode='constant', constant_values=0)
        if t2.shape[-1] == 1:
            t2 = np.pad(t2, ((0, 0), (0, 3)), mode='constant', constant_values=0)
        elif t2.shape[-1] == 3:
            t2 = np.pad(t2, ((0, 0), (1, 0)), mode='constant', constant_values=0)
        # (B,1)
        s_1 = t1[:, [0]]
        # (B,3)
        v_1 = t1[:, 1:]
        v_2 = t2[:, 1:]
        u = np.cross(v_1, v_2, axisc=-1)
        qs = np.zeros_like(s_1)
        qv = np.zeros_like(v_1)
        qs += np.linalg.norm(v_1, axis=-1, keepdims=True) * np.linalg.norm(v_2, axis=-1, keepdims=True)
        qs += np.einsum('ij,ij->i', v_1, v_2)[..., None]
        qv += u
        q = np.hstack((qs, qv))
    return q / np.linalg.norm(q, axis=-1)


if __name__ == '__main__':
    a = np.array([1, 2, 3, 4], np.float32)
    b = np.array([3, 1, 0, 5], np.float32)
    print (add(a, b))
    print (multiply(a, b))
    c = np.array([0.5, 0.5, 0.5, 0.5], np.float32)
    d = np.array([1, 2, 3], np.float32)
    print (hamiltonian(c, d))
    print (hamiltonian(inverse(c), hamiltonian(c, d)))
    x = np.array([1, 0, 0], np.float32)
    y = np.array([0, 0, 1], np.float32)
    z = np.array([np.sqrt(3) / 3, np.sqrt(3) / 3, np.sqrt(3) / 3], np.float32)
    print (transform(x, y))
    print (hamiltonian(transform(x, y), x))
    print(transform(x, z))
    print(hamiltonian(transform(x, z), x))