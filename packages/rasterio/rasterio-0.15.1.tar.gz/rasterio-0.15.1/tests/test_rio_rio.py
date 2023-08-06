import click
from click.testing import CliRunner


import rasterio
from rasterio.rio import rio


def test_insp():
    runner = CliRunner()
    result = runner.invoke(
        rio.insp,
        ['tests/data/RGB.byte.tif'])
    assert result.exit_code == 0


def test_insp_err():
    runner = CliRunner()
    result = runner.invoke(
        rio.insp,
        ['tests'])
    assert result.exit_code == 1


def test_bounds_defaults():
    runner = CliRunner()
    result = runner.invoke(
        rio.bounds,
        ['tests/data/RGB.byte.tif'])
    assert result.exit_code == 0
    assert 'FeatureCollection' in result.output


def test_bounds_err():
    runner = CliRunner()
    result = runner.invoke(
        rio.bounds,
        ['tests'])
    assert result.exit_code == 1


def test_bounds_obj_bbox():
    runner = CliRunner()
    result = runner.invoke(
        rio.bounds,
        ['tests/data/RGB.byte.tif', '--bbox', '--precision', '2'])
    assert result.exit_code == 0
    assert result.output.strip() == '[-78.9, 23.56, -76.6, 25.55]'


def test_bounds_compact():
    runner = CliRunner()
    result = runner.invoke(
        rio.bounds,
        ['tests/data/RGB.byte.tif', '--bbox', '--precision', '2', '--compact'])
    assert result.exit_code == 0
    assert result.output.strip() == '[-78.9,23.56,-76.6,25.55]'


def test_bounds_indent():
    runner = CliRunner()
    result = runner.invoke(
        rio.bounds,
        ['tests/data/RGB.byte.tif', '--bbox', '--indent', '2', '--precision', '2'])
    assert result.exit_code == 0
    assert len(result.output.split('\n')) == 7


def test_bounds_obj_bbox_mercator():
    runner = CliRunner()
    result = runner.invoke(
        rio.bounds,
        ['tests/data/RGB.byte.tif', '--bbox', '--mercator', '--precision', '3'])
    assert result.exit_code == 0
    assert result.output.strip() == '[-8782900.033, 2700489.278, -8527010.472, 2943560.235]'


def test_bounds_obj_bbox_projected():
    runner = CliRunner()
    result = runner.invoke(
        rio.bounds,
        ['tests/data/RGB.byte.tif', '--bbox', '--projected', '--precision', '3'])
    assert result.exit_code == 0
    assert result.output.strip() == '[101985.0, 2611485.0, 339315.0, 2826915.0]'


def test_bounds_seq():
    runner = CliRunner()
    result = runner.invoke(
        rio.bounds,
        ['tests/data/RGB.byte.tif', 'tests/data/RGB.byte.tif', '--x-json-seq', '--bbox', '--precision', '2'])
    assert result.exit_code == 0
    assert result.output == '[-78.9, 23.56, -76.6, 25.55]\n[-78.9, 23.56, -76.6, 25.55]\n'
    assert '\x1e' not in result.output


def test_bounds_seq_rs():
    runner = CliRunner()
    result = runner.invoke(
        rio.bounds,
        ['tests/data/RGB.byte.tif', 'tests/data/RGB.byte.tif', '--x-json-seq', '--x-json-seq-rs', '--bbox', '--precision', '2'])
    assert result.exit_code == 0
    assert result.output == '\x1e[-78.9, 23.56, -76.6, 25.55]\n\x1e[-78.9, 23.56, -76.6, 25.55]\n'



def test_bounds_obj_feature():
    runner = CliRunner()
    result = runner.invoke(
        rio.bounds,
        ['tests/data/RGB.byte.tif', '--feature', '--precision', '6'])
    assert result.exit_code == 0
    assert result.output.strip() == '{"bbox": [-78.898133, 23.564991, -76.599438, 25.550874], "geometry": {"coordinates": [[[-78.898133, 23.564991], [-76.599438, 23.564991], [-76.599438, 25.550874], [-78.898133, 25.550874], [-78.898133, 23.564991]]], "type": "Polygon"}, "properties": {"id": "0", "title": "tests/data/RGB.byte.tif"}, "type": "Feature"}'


def test_transform_err():
    runner = CliRunner()
    result = runner.invoke(
        rio.transform,
        [], "[-78.0]")
    assert result.exit_code == 1


def test_transform_point():
    runner = CliRunner()
    result = runner.invoke(
        rio.transform,
        ['--dst_crs', 'EPSG:32618', '--precision', '2'],
        "[-78.0, 23.0]", catch_exceptions=False)
    assert result.exit_code == 0
    assert result.output.strip() == '[192457.13, 2546667.68]'


def test_transform_point_dst_file():
    runner = CliRunner()
    result = runner.invoke(
        rio.transform,
        ['--dst_crs', 'tests/data/RGB.byte.tif', '--precision', '2'],
        "[-78.0, 23.0]")
    assert result.exit_code == 0
    assert result.output.strip() == '[192457.13, 2546667.68]'


def test_transform_point_src_file():
    runner = CliRunner()
    result = runner.invoke(
        rio.transform,
        ['--src_crs', 'tests/data/RGB.byte.tif', '--precision', '2'],
        "[192457.13, 2546667.68]")
    assert result.exit_code == 0
    assert result.output.strip() == '[-78.0, 23.0]'


def test_transform_point_2():
    runner = CliRunner()
    result = runner.invoke(
        rio.transform,
        ['[-78.0, 23.0]', '--dst_crs', 'EPSG:32618', '--precision', '2'])
    assert result.exit_code == 0
    assert result.output.strip() == '[192457.13, 2546667.68]'


def test_transform_point_multi():
    runner = CliRunner()
    result = runner.invoke(
        rio.transform,
        ['--dst_crs', 'EPSG:32618', '--precision', '2'],
        "[-78.0, 23.0]\n[-78.0, 23.0]", catch_exceptions=False)
    assert result.exit_code == 0
    assert result.output.strip() == '[192457.13, 2546667.68]\n[192457.13, 2546667.68]'
