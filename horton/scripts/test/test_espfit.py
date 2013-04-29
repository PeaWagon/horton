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


import tempfile, shutil, os, h5py as h5

from horton import *
from horton.test.common import check_script
from horton.scripts.test.common import copy_files, check_files
from horton.scripts.espfit import *

def test_wdens():
    assert parse_wdens('fubar.cube') == ('fubar.cube', 2e-4, 1.0)
    assert parse_wdens('fubar.cube:2e-3') == ('fubar.cube', 2e-3, 1.0)
    assert parse_wdens('fubar.cube:2e-2:0.5') == ('fubar.cube', 2e-2, 0.5)

def test_wnear():
    assert parse_wnear('1:1.0') == {1: (1.0*angstrom, 0.5*angstrom)}
    assert parse_wnear('1:1.0:0.3') == {1: (1.0*angstrom, 0.3*angstrom)}
    assert parse_wnear(['1:1.0', '2:1.2']) == {1: (1.0*angstrom, 0.5*angstrom), 2: (1.2*angstrom, 0.6*angstrom)}
    assert parse_wnear(['1:1.0:0.3', '2:1.2:0.2']) == {1: (1.0*angstrom, 0.3*angstrom), 2: (1.2*angstrom, 0.2*angstrom)}

def test_wfar():
    assert parse_wfar('4.3') == (4.3*angstrom, 1.0*angstrom)
    assert parse_wfar('4.2:0.3') == (4.2*angstrom, 0.3*angstrom)


def test_scripts():
    # Generate some random system with random esp data
    natom = 5
    numbers = np.random.randint(1, 20, natom)
    coordinates = np.random.uniform(0, 10, (natom, 3))
    origin = np.zeros(3, float)
    grid_rvecs = np.identity(3, float)*1.0
    shape = np.array([10, 10, 10])
    pbc = np.ones(3, int)
    ui_grid = UniformIntGrid(origin, grid_rvecs, shape, pbc)
    cube_data = np.random.uniform(-1, 1, shape)
    props = {'ui_grid': ui_grid, 'cube_data': cube_data}
    sys = System(coordinates, numbers, props=props)

    # Write the cube file to the tmpdir and run scripts
    tmpdir = tempfile.mkdtemp('horton.scripts.test.test_espfit.test_scripts')
    try:
        sys.to_file(os.path.join(tmpdir, 'esp.cube'))
        check_script('horton-esp-cost.py esp.cube --wnear=0:1.0:0.5', tmpdir)
        check_files(tmpdir, ['esp.cube.h5'])
        check_script('horton-esp-fit.py esp.cube.h5:espfit/espfit_r1 default', tmpdir)
        check_script('horton-esp-test.py esp.cube.h5:espfit/espfit_r1 esp.cube.h5:espfit/espfit_r1/default', tmpdir)
        check_script('horton-esp-gen.py esp.cube.h5:espfit/espfit_r1/default --grid=1.2', tmpdir)
    finally:
        shutil.rmtree(tmpdir)
