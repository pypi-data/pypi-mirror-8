Warping and reprojecting raster data
====================================

Beginning in version 0.7, rasterio enables reprojection of raster data.
Given source and destination arrays and affine transformation and coordinate
reference systems for each, `rasterio.warp.reproject()` will map elements in
the destination array to those of the source array.



