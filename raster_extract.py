#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Nyi Nyi Nyan Lin
@organizations: Yangon Binarhaus
@contact: nyinyinyanlin.mm@gmail.com
@license: GNU GPL v3.0
@copyright: © 2021 Nyi Nyi Nyan Lin
@version: 1.0.0
@status: Development
@todo: Implement exceptions and error handling mechanism. Change the script to fully moduler format.
@summary: Python script to extract raster information of an area or region of interest from multiple rasters (GeoTIFF) using Polygon data from a Shapefile as boundary. A shapefile and directory for rasters must be given as input. The script is solely based on rasterio fiona for raster and fiona for shapefile manipulations.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import glob, sys, os.path, itertools
import fiona
import rasterio, rasterio.mask
from colorama import init, Fore, Style
init() # This is to init colorama in case the script is run on Win32

RASTER_EXTENSION = ".tif"
ERROR_CODE = Fore.RED + "[ERROR]" + Style.RESET_ALL
WARNING_CODE = Fore.YELLOW + "[WARNING]" + Style.RESET_ALL
INFO_CODE = Fore.GREEN + "[INFO]" + Style.RESET_ALL

# Preprocessing entered arguments, filenames and paths
arg_names = ['command','shp_filename','raster_dir','output_dir']
args = dict(itertools.zip_longest(arg_names,sys.argv))

print("\n\n"+__doc__+"\n\n")

if args["shp_filename"] is None:
    print("{} No input shapefile is provided. Program exiting.".format(ERROR_CODE))
    exit()

if args["raster_dir"]:
    args["raster_dir"] = os.path.join(args["raster_dir"])
else:
    args["raster_dir"] = ""
    print("{} No raster input directory is provided. Using present working directory as input folder.\n".format(WARNING_CODE))

if args["output_dir"]:
    args["output_dir"] = os.path.join(args["output_dir"])
    if not os.path.exists(args["output_dir"]):
        os.makedirs(args["output_dir"])
        print("{} Provided output directory does not exist.\n\tIt will be created by the program.\n".format(WARNING_CODE))
else:
    args["output_dir"] = ""
    print("{} No output directory is provided. Using present working directory as output folder.\n".format(WARNING_CODE))

# Open and load provided input files
if os.path.exists(args["shp_filename"]):
    print("{} Opening Shapefile: {}".format(INFO_CODE, args["shp_filename"]))

    with fiona.open(args["shp_filename"], "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
        print("{} Shapefile loaded successfully!\n".format(INFO_CODE))

    # List raster files in input directory
    raster_files = glob.glob("{}*{}".format(args["raster_dir"],RASTER_EXTENSION))
    if len(raster_files) == 0:
        print("{} No raster file is found in the provided input directory to be processed.\n\tTerminating the program!\n".format(ERROR_CODE))
        exit()

    print("{} Listed {} raster files from provided input folder: {}\n".format(INFO_CODE,len(raster_files),args["raster_dir"]))
    
    c = 0
    for raster_file in raster_files:
        c = c + 1
        print("{} Currently processing: {}".format(INFO_CODE,raster_file))

        # Open raster file and mask with shape
        with rasterio.open(raster_file) as raster:
            out_mask, transform = rasterio.mask.mask(raster, shapes, filled=True, all_touched=True)
            out_meta = raster.meta
            out_meta.update({"driver": "GTiff",
                            "height": out_mask.shape[1],
                            "width": out_mask.shape[2],
                            "compress":"lzw"})

            # Export processed raster
            export_raster = "{}{}_{}".format(os.path.join(args["output_dir"],""),os.path.splitext(os.path.basename(args["shp_filename"]))[0],os.path.basename(raster_file))
            with rasterio.open(export_raster, "w", **out_meta) as dest:
                dest.write(out_mask)
                print("{} Successfully processed and exported: {}\n\tFinished {} out of {} rasters.\n".format(INFO_CODE,export_raster,c,len(raster_files)))

    print("{} Successfully processed and exported {} raster files.".format(INFO_CODE,len(raster_files)))
else:
    print("{} Entered shapefile doesn't exist\n".format(ERROR_CODE))