__author__ = 'Benjamin S. Murphy'
__version__ = '0.2.0'
__doc__ = """Code by Benjamin S. Murphy
bscott.murphy@gmail.com

Dependencies:
    NumPy
    SciPy
    MatPlotLib

Modules:
    ok: Contains class OrdinaryKriging, which is a convenience class
        for easy access to 2D Ordinary Kriging.
    uk: Contains class UniversalKriging, which  provides more control over
        2D kriging by utilizing drift terms. Supported drift terms
        currently include point-logarithmic, regional linear, and external
        z-scalar.
    kriging_tools: Contains a set of functions to work with *.asc files.
    variogram_models: Contains the definitions for the implemented variogram
        models. Note that the utilized formulas are as presented in Kitanidis,
        so the exact definition of the range (specifically, the associated
        scaling of that value) may differ slightly from other sources.
    core: Contains the backbone functions of the package that are called by
        both the OrdinaryKriging class and the UniversalKriging class.
        The functions were consolidated here in order to reduce redundancy
        in the code.

References:
    P.K. Kitanidis, Introduction to Geostatistcs: Applications in Hydrogeology,
    (Cambridge University Press, 1997) 272 p.
    
Copyright (C) 2014 Benjamin S. Murphy

This file is part of PyKrige.

PyKrige is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

PyKrige is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, go to <https://www.gnu.org/>.
"""
