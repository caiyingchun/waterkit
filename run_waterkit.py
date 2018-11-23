#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# WaterKit
#
# Launch waterkit
#

import argparse

from waterkit import utils
from waterkit.waterkit import Waterkit
from waterkit.autodock_map import Map
from waterkit.molecule import Molecule
from waterkit.water import Water


def cmd_lineparser():
    parser = argparse.ArgumentParser(description='waterkit')
    parser.add_argument("-i", "--mol", dest="mol_file", required=True,
                        action="store", help="receptor file")
    parser.add_argument("-x", "--wat", dest="wat_file", default=None,
                        action="store", help="xray water file")
    parser.add_argument("-m", "--fld", dest="fld_file", required=True,
                        action="store", help="autodock fld file")
    parser.add_argument("-l", "--layer", dest="n_layer", default=0, type=int,
                        action="store", help="number of layer to add")
    parser.add_argument("-n", "--sample", dest="n_sample", default=1, type=int,
                        action="store", help="number of sample")
    parser.add_argument("-c", "--choice", dest="how", default='boltzmann',
                        choices=['all', 'best', 'boltzmann'], action="store",
                        help="how water molecules are choosed")
    parser.add_argument("-o", "--output", dest="output_prefix", default='water',
                        action="store", help="prefix add to output files")
    return parser.parse_args()


def main():
    args = cmd_lineparser()
    mol_file = args.mol_file
    fld_file = args.fld_file
    wat_file = args.wat_file
    n_layer = args.n_layer
    n_sample = args.n_sample
    how = args.how
    output_prefix = args.output_prefix

    # Read PDBQT/MOL2 file, Waterfield file and AutoDock grid map
    molecule = Molecule.from_file(mol_file)
    ad_map = Map.from_fld(fld_file)

    if wat_file is not None:
        waters = Water.from_file(wat_file)
    else:
        waters = None

    # Go waterkit!!
    k = Waterkit()
    k.hydrate(molecule, ad_map, waters, n_layer, n_sample, how)

    # Write output files
    k.write_shells(output_prefix)
    k.write_shells(output_prefix, False)
    k.write_maps(output_prefix, ['OW'])

if __name__ == '__main__':
    main()
