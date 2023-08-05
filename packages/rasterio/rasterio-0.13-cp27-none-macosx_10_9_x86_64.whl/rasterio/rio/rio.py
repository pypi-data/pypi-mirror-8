#!/usr/bin/env python

"""Rasterio command line interface"""

import functools
import json
import logging
import os.path
import pprint
import sys
import warnings

import click

import rasterio

from rasterio.rio.cli import cli
from rasterio.rio.info import info
from rasterio.rio.merge import merge


warnings.simplefilter('default')


def coords(obj):
    """Yield all coordinate coordinate tuples from a geometry or feature.
    From python-geojson package."""
    if isinstance(obj, (tuple, list)):
        coordinates = obj
    elif 'geometry' in obj:
        coordinates = obj['geometry']['coordinates']
    else:
        coordinates = obj.get('coordinates', obj)
    for e in coordinates:
        if isinstance(e, (float, int)):
            yield tuple(coordinates)
            break
        else:
            for f in coords(e):
                yield f


def write_features(file, collection,
        agg_mode='obj', expression='feature', use_rs=False,
        **dump_kwds):
    """Read an iterator of (feat, bbox) pairs and write to file using
    the selected modes."""
    # Sequence of features expressed as bbox, feature, or collection.
    if agg_mode == 'seq':
        for feat in collection():
            xs, ys = zip(*coords(feat))
            bbox = (min(xs), min(ys), max(xs), max(ys))
            if use_rs:
                file.write(u'\u001e')
            if expression == 'feature':
                file.write(json.dumps(feat, **dump_kwds))
            elif expression == 'bbox':
                file.write(json.dumps(bbox, **dump_kwds))
            else:
                file.write(
                    json.dumps({
                        'type': 'FeatureCollection',
                        'bbox': bbox,
                        'features': [feat]}, **dump_kwds))
            file.write('\n')
    # Aggregate all features into a single object expressed as 
    # bbox or collection.
    else:
        features = list(collection())
        if expression == 'bbox':
            file.write(json.dumps(collection.bbox, **dump_kwds))
        elif expression == 'feature':
            file.write(json.dumps(features[0], **dump_kwds))
        else:
            file.write(json.dumps({
                'bbox': collection.bbox,
                'type': 'FeatureCollection', 
                'features': features},
                **dump_kwds))
            file.write('\n')


# Commands are below.
#
# Command bodies less than ~20 lines, e.g. info() below, can go in this
# module. Longer ones, e.g. insp() shall call functions imported from
# rasterio.tool.

# Insp command.
@cli.command(short_help="Open a data file and start an interpreter.")
@click.argument('src_path', type=click.Path(exists=True))
@click.option('--mode', type=click.Choice(['r', 'r+']), default='r', help="File mode (default 'r').")
@click.pass_context
def insp(ctx, src_path, mode):
    import rasterio.tool

    verbosity = ctx.obj['verbosity']
    logger = logging.getLogger('rio')
    try:
        with rasterio.drivers(CPL_DEBUG=verbosity>2):
            with rasterio.open(src_path, mode) as src:
                rasterio.tool.main(
                    "Rasterio %s Interactive Inspector (Python %s)\n"
                    'Type "src.meta", "src.read_band(1)", or "help(src)" '
                    'for more information.' %  (
                        rasterio.__version__,
                        '.'.join(map(str, sys.version_info[:3]))),
                    src)
        sys.exit(0)
    except Exception:
        logger.exception("Failed. Exception caught")
        sys.exit(1)

# Bounds command.
@cli.command(short_help="Write bounding boxes to stdout as GeoJSON.")

# One or more files, the bounds of each are a feature in the collection
# object or feature sequence.
@click.argument('input', nargs=-1, type=click.Path(exists=True))

# Coordinate precision option.
@click.option('--precision', type=int, default=-1,
              help="Decimal precision of coordinates.")

# JSON formatting options.
@click.option('--indent', default=None, type=int,
              help="Indentation level for JSON output")
@click.option('--compact/--no-compact', default=False,
              help="Use compact separators (',', ':').")

# Geographic (default) or Mercator switch.
@click.option('--geographic', 'projected', flag_value='geographic',
              default=True,
              help="Output in geographic coordinates (the default).")
@click.option('--projected', 'projected', flag_value='projected',
              help="Output in projected coordinates.")
@click.option('--mercator', 'projected', flag_value='mercator',
              help="Output in Web Mercator coordinates.")

# JSON object (default) or sequence (experimental) switch.
@click.option('--json-obj', 'json_mode', flag_value='obj', default=True,
        help="Write a single JSON object (the default).")
@click.option('--x-json-seq', 'json_mode', flag_value='seq',
        help="Write a JSON sequence. Experimental.")

# Use ASCII RS control code to signal a sequence item (False is default).
# See http://tools.ietf.org/html/draft-ietf-json-text-sequence-05.
# Experimental.
@click.option('--x-json-seq-rs/--x-json-seq-no-rs', default=False,
        help="Use RS as text separator. Experimental.")

# GeoJSON feature (default), bbox, or collection switch. Meaningful only
# when --x-json-seq is used.
@click.option('--collection', 'output_mode', flag_value='collection',
              default=True,
              help="Output as a GeoJSON feature collection (the default).")
@click.option('--feature', 'output_mode', flag_value='feature',
              help="Output as sequence of GeoJSON features.")
@click.option('--bbox', 'output_mode', flag_value='bbox',
              help="Output as a GeoJSON bounding box array.")

@click.pass_context

def bounds(ctx, input, precision, indent, compact, projected, json_mode,
        x_json_seq_rs, output_mode):

    """Write bounding boxes to stdout as GeoJSON for use with, e.g.,
    geojsonio

    $ rio bounds *.tif | geojsonio

    """
    import rasterio.warp

    verbosity = ctx.obj['verbosity']
    logger = logging.getLogger('rio')
    dump_kwds = {'sort_keys': True}
    if indent:
        dump_kwds['indent'] = indent
    if compact:
        dump_kwds['separators'] = (',', ':')
    stdout = click.get_text_stream('stdout')

    # This is the generator for (feature, bbox) pairs.
    class Collection(object):

        def __init__(self):
            self._xs = []
            self._ys = []

        @property
        def bbox(self):
            return min(self._xs), min(self._ys), max(self._xs), max(self._ys)

        def __call__(self):
            for i, path in enumerate(input):
                with rasterio.open(path) as src:
                    bounds = src.bounds
                    xs = [bounds[0], bounds[2]]
                    ys = [bounds[1], bounds[3]]
                    if projected == 'geographic':
                        xs, ys = rasterio.warp.transform(
                            src.crs, {'init': 'epsg:4326'}, xs, ys)
                    if projected == 'mercator':
                        xs, ys = rasterio.warp.transform(
                            src.crs, {'init': 'epsg:3857'}, xs, ys)
                if precision >= 0:
                    xs = [round(v, precision) for v in xs]
                    ys = [round(v, precision) for v in ys]
                bbox = [min(xs), min(ys), max(xs), max(ys)]
                
                yield {
                    'type': 'Feature',
                    'bbox': bbox,
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [[
                            [xs[0], ys[0]],
                            [xs[1], ys[0]],
                            [xs[1], ys[1]],
                            [xs[0], ys[1]],
                            [xs[0], ys[0]] ]]},
                    'properties': {
                        'id': str(i), 'title': path} }

                self._xs.extend(bbox[::2])
                self._ys.extend(bbox[1::2])

    collection = Collection()

    # Use the generator defined above as input to the generic output 
    # writing function.
    try:
        with rasterio.drivers(CPL_DEBUG=verbosity>2):
            write_features(
                stdout, collection, agg_mode=json_mode,
                expression=output_mode, use_rs=x_json_seq_rs,
                **dump_kwds)
        sys.exit(0)
    except Exception:
        logger.exception("Failed. Exception caught")
        sys.exit(1)


def transform_geom(transformer, g, precision=-1):
    if g['type'] == 'Point':
        x, y = g['coordinates']
        xp, yp = transformer([x], [y])
        if precision >= 0:
            xp = [round(v, precision) for v in xp]
            yp = [round(v, precision) for v in yp]
        new_coords = list(zip(xp, yp))[0]
    if g['type'] in ['LineString', 'MultiPoint']:
        xp, yp = transformer(*zip(g['coordinates']))
        if precision >= 0:
            xp = [round(v, precision) for v in xp]
            yp = [round(v, precision) for v in yp]
        new_coords = list(zip(xp, yp))
    elif g['type'] in ['Polygon', 'MultiLineString']:
        new_coords = []
        for piece in g['coordinates']:
            xp, yp = transformer(*zip(*piece))
            if precision >= 0:
                xp = [round(v, precision) for v in xp]
                yp = [round(v, precision) for v in yp]
            new_coords.append(list(zip(xp, yp)))
    elif g['type'] == 'MultiPolygon':
        parts = g['coordinates']
        new_coords = []
        for part in parts:
            inner_coords = []
            for ring in part:
                xp, yp = transformer(*zip(*ring))
                if precision >= 0:
                    xp = [round(v, precision) for v in xp]
                    yp = [round(v, precision) for v in yp]
                inner_coords.append(list(zip(xp, yp)))
            new_coords.append(inner_coords)
    g['coordinates'] = new_coords
    return g


# Shapes command.
@cli.command(short_help="Write the shapes of features.")

@click.argument('input', type=click.Path(exists=True))

# Coordinate precision option.
@click.option('--precision', type=int, default=-1,
              help="Decimal precision of coordinates.")

# JSON formatting options.
@click.option('--indent', default=None, type=int,
              help="Indentation level for JSON output")
@click.option('--compact/--no-compact', default=False,
              help="Use compact separators (',', ':').")

# Geographic (default) or Mercator switch.
@click.option('--geographic', 'projected', flag_value='geographic',
              default=True,
              help="Output in geographic coordinates (the default).")
@click.option('--projected', 'projected', flag_value='projected',
              help="Output in projected coordinates.")

# JSON object (default) or sequence (experimental) switch.
@click.option('--json-obj', 'json_mode', flag_value='obj', default=True,
        help="Write a single JSON object (the default).")
@click.option('--x-json-seq', 'json_mode', flag_value='seq',
        help="Write a JSON sequence. Experimental.")

# Use ASCII RS control code to signal a sequence item (False is default).
# See http://tools.ietf.org/html/draft-ietf-json-text-sequence-05.
# Experimental.
@click.option('--x-json-seq-rs/--x-json-seq-no-rs', default=False,
        help="Use RS as text separator. Experimental.")

# GeoJSON feature (default), bbox, or collection switch. Meaningful only
# when --x-json-seq is used.
@click.option('--collection', 'output_mode', flag_value='collection',
              default=True,
              help="Output as a GeoJSON feature collection (the default).")
@click.option('--feature', 'output_mode', flag_value='feature',
              help="Output as sequence of GeoJSON features.")
@click.option('--bbox', 'output_mode', flag_value='bbox',
              help="Output as a GeoJSON bounding box array.")

@click.pass_context

def shapes(
        ctx, input, precision, indent, compact, projected, json_mode,
        x_json_seq_rs, output_mode):

    """Writes features of a dataset out as GeoJSON. It's intended for
    use with single-band rasters and reads from the first band.
    """
    import rasterio.features
    import rasterio.warp

    verbosity = ctx.obj['verbosity']
    logger = logging.getLogger('rio')
    dump_kwds = {'sort_keys': True}
    if indent:
        dump_kwds['indent'] = indent
    if compact:
        dump_kwds['separators'] = (',', ':')
    stdout = click.get_text_stream('stdout')

    # This is the generator for (feature, bbox) pairs.
    class Collection(object):

        def __init__(self):
            self._xs = []
            self._ys = []

        @property
        def bbox(self):
            return min(self._xs), min(self._ys), max(self._xs), max(self._ys)

        def __call__(self):
            with rasterio.open(input) as src:
                bounds = src.bounds
                xs = [bounds[0], bounds[2]]
                ys = [bounds[1], bounds[3]]
                if projected == 'geographic':
                    xs, ys = rasterio.warp.transform(
                        src.crs, {'init': 'epsg:4326'}, xs, ys)
                if precision >= 0:
                    xs = [round(v, precision) for v in xs]
                    ys = [round(v, precision) for v in ys]
                self._xs = xs
                self._ys = ys

                # To be used in the geographic case below.
                transformer = functools.partial(
                                rasterio.warp.transform,
                                src.crs,
                                {'init': 'epsg:4326'})
                
                for g, i in rasterio.features.shapes(
                                src.read(1), transform=src.affine):
                    if projected == 'geographic':
                        g = transform_geom(transformer, g, precision)
                    yield {
                        'type': 'Feature',
                        'id': str(i),
                        'properties': {'val': i},
                        'geometry': g }

    collection = Collection()

    # Use the generator defined above as input to the generic output 
    # writing function.
    try:
        with rasterio.drivers(CPL_DEBUG=verbosity>2):
            write_features(
                stdout, collection, agg_mode=json_mode,
                expression=output_mode, use_rs=x_json_seq_rs,
                **dump_kwds)
        sys.exit(0)
    except Exception:
        logger.exception("Failed. Exception caught")
        sys.exit(1)


# Transform command.
@cli.command(short_help="Transform coordinates.")
@click.argument('input', type=click.File('rb'))
@click.option('--src_crs', default='EPSG:4326', help="Source CRS.")
@click.option('--dst_crs', default='EPSG:4326', help="Destination CRS.")
@click.option('--interleaved', 'mode', flag_value='interleaved', default=True)
@click.option('--precision', type=int, default=-1,
              help="Decimal precision of coordinates.")
@click.pass_context
def transform(ctx, input, src_crs, dst_crs, mode, precision):
    import rasterio.warp

    verbosity = ctx.obj['verbosity']
    logger = logging.getLogger('rio')
    try:
        if mode == 'interleaved':
            coords = json.loads(input.read().decode('utf-8'))
            xs = coords[::2]
            ys = coords[1::2]
        else:
            raise ValueError("Invalid input type '%s'" % input_type)
        with rasterio.drivers(CPL_DEBUG=verbosity>2):
            if src_crs.startswith('EPSG'):
                src_crs = {'init': src_crs}
            elif os.path.exists(src_crs):
                with rasterio.open(src_crs) as f:
                    src_crs = f.crs
            if dst_crs.startswith('EPSG'):
                dst_crs = {'init': dst_crs}
            elif os.path.exists(dst_crs):
                with rasterio.open(dst_crs) as f:
                    dst_crs = f.crs
            xs, ys = rasterio.warp.transform(src_crs, dst_crs, xs, ys)
            if precision >= 0:
                xs = [round(v, precision) for v in xs]
                ys = [round(v, precision) for v in ys]
        if mode == 'interleaved':
            result = [0]*len(coords)
            result[::2] = xs
            result[1::2] = ys
        print(json.dumps(result))
        sys.exit(0)
    except Exception:
        logger.exception("Failed. Exception caught")
        sys.exit(1)


if __name__ == '__main__':
    cli()
