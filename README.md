This script depends on the following Python libraries

- Fiona (for shapefile processing)
- RasterIO (for raster processing)
- GDAL (for geoprocessing functions)
- Numpy (for numerical operations)
- Colorama (for console output styling)

Above mentioned packages can be installed by running `pip install -r requirements.txt` in the cloned folder. However, please notice that the dependencies are installed for Python3.8 running on Windows x64. If you are using different version of Python or CPU architecture, for example, ARM or x86, please install appropriate versions (wheels) of libraries/packages stated in `requirements.txt`.

A shapefile should be provided which will be processed against a number of raster files with `.tif` extension collected in an input folder. Processed files can be exported into an output folder. The script can be run by executing the following command.

`python raster_extract.py shapefilename.shp path_to_directory_of/input/tiff_files output_directory`

where you can replace the respective file and path names. Please notice that the script will process all raster files that can be found in the input folder/directory. If you do not provide any input folder path or output folder path, current working directory will be used in both cases.