# -*- coding: utf-8 -*-
# Horton is a Density Functional Theory program.
# Copyright (C) 2011-2013 Toon Verstraelen <Toon.Verstraelen@UGent.be>
#
# This file is part of Horton.
#
# Horton is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Horton is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
#--


import numpy as np
cimport numpy as np
np.import_array()

cimport ewald3d

cimport horton.cext


__all__ = [
    'pair_ewald',
    'setup_esp_cost_cube',
]


def setup_esp_cost_cube(np.ndarray[double, ndim=1] origin not None,
                        horton.cext.Cell grid_cell not None,
                        np.ndarray[long, ndim=1] shape not None,
                        horton.cext.Cell cell not None,
                        np.ndarray[double, ndim=3] vref not None,
                        np.ndarray[double, ndim=3] weights not None,
                        np.ndarray[double, ndim=2] centers not None,
                        np.ndarray[double, ndim=2] A not None,
                        np.ndarray[double, ndim=1] B not None,
                        np.ndarray[double, ndim=0] C not None,
                        double rcut, double alpha, double gcut):

    assert origin.flags['C_CONTIGUOUS']
    assert origin.shape[0] == 3
    assert shape.flags['C_CONTIGUOUS']
    assert shape.shape[0] == 3
    assert vref.flags['C_CONTIGUOUS']
    assert vref.shape[0] == shape[0]
    assert vref.shape[1] == shape[1]
    assert vref.shape[2] == shape[2]
    assert weights.flags['C_CONTIGUOUS']
    assert weights.shape[0] == shape[0]
    assert weights.shape[1] == shape[1]
    assert weights.shape[2] == shape[2]
    assert centers.flags['C_CONTIGUOUS']
    ncenter = centers.shape[0]
    assert ncenter > 0
    assert centers.shape[1] == 3
    assert A.flags['C_CONTIGUOUS']
    assert A.shape[0] == ncenter
    assert A.shape[1] == ncenter
    assert B.flags['C_CONTIGUOUS']
    assert B.shape[0] == ncenter
    assert C.flags['C_CONTIGUOUS']
    assert rcut > 0
    assert alpha > 0
    assert gcut > 0

    if cell.nvec == 3:
        ewald3d.setup_esp_cost_cube_ewald3d(<double*>origin.data, grid_cell._this,
            <long*>shape.data, cell._this, <double*>vref.data,
            <double*>weights.data, <double*>centers.data, <double*>A.data,
            <double*>B.data, <double*>C.data, ncenter, rcut, alpha, gcut)
    else:
        raise NotImplementedError


def pair_ewald(np.ndarray[double, ndim=1] delta not None,
                        horton.cext.Cell cell not None,
                        double rcut, double alpha, double gcut):

    assert delta.flags['C_CONTIGUOUS']
    assert delta.shape[0] == 3
    assert rcut > 0
    assert alpha > 0
    assert gcut > 0

    if cell.nvec == 3:
        return ewald3d.pair_ewald3d(<double*>delta.data, cell._this, rcut, alpha, gcut)
    else:
        raise NotImplementedError
