#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Generate companion files for experimentA of the idr0065 study. This script
# assumes the following layout for the original data:
#
#  <microscopic_slide>/        All data associated with a microscopic slide
#    pheno/                    Phenotypic acquisition
#      metadata.txt            Metadata for the phenotyping acquisition
#      Pos101/                 Position on a microscopyic slide
#        fluor/                Fluorescence timelapse images
#        phase/                Phase timelapse images
#    geno/                     Genotypic acqusition
#      Pos101/                 Position on the microscopyic slide
#        1_cy5_fluor/          Fluorescence acquisition (11 cycles)
#        2_cy3_fluor/          Fluorescence acquisition (11 cycles)
#        3_TxR_fluor/          Fluorescence acquisition (11 cycles)
#        4_fam_flour/          Fluorescence acquisition (11 cycles)
#        phase/                Phase acquisition (11 cycles)

import argparse
import logging

from ome_model.experimental import Image, create_companion
import os
from os.path import join, dirname
import subprocess


def write_companion():

    SIZE_T = 419
    SIZE_C = 3
    logging.info("Generating phenotypic metadata files")
    image = Image(
        "Sample 1", 658, 658, 658, SIZE_C, SIZE_T, order="XYZCT",
        type="uint16")
    image.add_channel("TagBFP", -1)
    image.add_channel("GFP", -1)
    image.add_channel("GFP", -1)

    # Phase images
    for t in range(SIZE_T):
        for c in range(SIZE_C):
            filename = "tif/tp%04g_c%03g_a0000.tif" % (t, c)
            image.add_tiff(filename, c=c, z=0, t=t, planeCount=658)

    # Generate companion OME-XML file
    companion_file = join(
        "experimentA", "companions", 'image.companion.ome')
    if not os.path.exists(dirname(companion_file)):
        os.makedirs(dirname(companion_file))
        logging.info("Created %s" % dirname(companion_file))
    create_companion(images=[image], out=companion_file)

    # Indent XML for readability
    proc = subprocess.Popen(
        ['xmllint', '--format', '-o', companion_file, companion_file],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    (output, error_output) = proc.communicate()
    logging.info("Created %s" % companion_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()

    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(len(levels)-1, args.verbose)]
    logger = logging.basicConfig(
        level=level, format="%(asctime)s %(levelname)s %(message)s")

    write_companion()
