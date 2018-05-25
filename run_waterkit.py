#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# WaterKit
#
# Launch waterkit
#

import argparse
import imp
import os
import sys

from waterkit.waterkit import utils
from waterkit.waterkit import Waterkit
from waterkit.autodock_map import Map
from waterkit.molecule import Molecule
from waterkit.waterfield import Waterfield


def cmd_lineparser():
    parser = argparse.ArgumentParser(description='waterkit')
    parser.add_argument("-i", "--mol", dest="mol_file", required=True,
                        action="store", help="molecule file")
    parser.add_argument("-m", "--map", dest="map_file", required=True,
                        action="store", help="autodock map file")
    parser.add_argument("-o", "--output", dest="output_file", default='water',
                        action="store", help="prefix add to output files")
    parser.add_argument("-f", "--waterfield", dest="waterfield_file", default=None,
                         action="store", help="waterfield file")
    parser.add_argument("-w", "--watermap", dest="water_map_file", default=None,
                        action="store", help="water autodock map file")
    return parser.parse_args()

def main():
    args = cmd_lineparser()
    mol_file = args.mol_file
    map_file = args.map_file
    waterfield_file = args.waterfield_file
    output_file = args.output_file
    water_map_file = args.water_map_file

    # Read PDBQT/MOL2 file, Waterfield file and AutoDock grid map
    molecule = Molecule(mol_file)
    ad_map = Map(map_file)

    d = imp.find_module('waterkit')[1]

    if waterfield_file is None:
        waterfield_file = os.path.join(d, 'data/waterfield.par')

    if water_map_file is None:
        water_map_file = os.path.join(d, 'data/water/maps.fld')

    waterfield = Waterfield(waterfield_file)
    water_map = Map(water_map_file)

    # Go waterkit!!
    k = Waterkit(waterfield, water_map)
    k.hydrate(molecule, ad_map, n_layer=-1)

    # Write output files
    k.write_waters(output_file)
    ad_map.to_map(['HD', 'Lp', 'OW'], output_file)

if __name__ == '__main__':
    main()