"""
Test module for booleans.
"""

import glob
import json
import os
import unittest

from geojson import Feature, Point, Polygon

from turfpy.boolean import (
    boolean_disjoint,
    boolean_intersects,
    boolean_point_in_polygon,
    boolean_within,
)


def load_json_file_sync(filepath):
    with open(filepath) as f:
        return json.load(f)


class TestTurfBooleanDisjoint(unittest.TestCase):
    def setUp(self):
        self.dirname = os.path.dirname(os.path.abspath(__file__))

    def test_true_fixtures(self):
        for filepath in glob.glob(
            os.path.join(
                self.dirname,
                "test_files/boolean_disjoint_test",
                "true",
                "**",
                "*.geojson",
            ),
            recursive=True,
        ):
            geojson = load_json_file_sync(filepath)
            feature1 = geojson["features"][0]
            feature2 = geojson["features"][1]
            result = boolean_disjoint(feature1, feature2)
            self.assertTrue(result, True)

    def test_false_fixtures(self):
        for filepath in glob.glob(
            os.path.join(
                self.dirname,
                "test_files/boolean_disjoint_test",
                "false",
                "**",
                "*.geojson",
            ),
            recursive=True,
        ):
            geojson = load_json_file_sync(filepath)
            feature1 = geojson["features"][0]
            feature2 = geojson["features"][1]
            result = boolean_disjoint(feature1, feature2)
            self.assertFalse(result, False)


class TestTurfBooleanIntersects(unittest.TestCase):
    def setUp(self):
        self.dirname = os.path.dirname(os.path.abspath(__file__))

    def test_true_fixtures(self):
        for filepath in glob.glob(
            os.path.join(
                self.dirname,
                "test_files/boolean_intersects_test",
                "true",
                "**",
                "*.geojson",
            ),
            recursive=True,
        ):
            geojson = load_json_file_sync(filepath)
            feature1 = geojson["features"][0]
            feature2 = geojson["features"][1]
            result = boolean_intersects(feature1, feature2)
            self.assertTrue(result, True)

    def test_false_fixtures(self):
        for filepath in glob.glob(
            os.path.join(
                self.dirname,
                "test_files/boolean_intersects_test",
                "false",
                "**",
                "*.geojson",
            ),
            recursive=True,
        ):
            geojson = load_json_file_sync(filepath)
            feature1 = geojson["features"][0]
            feature2 = geojson["features"][1]
            result = boolean_intersects(feature1, feature2)
            self.assertFalse(result, False)


class TestTurfBooleanWithin(unittest.TestCase):
    def setUp(self):
        self.dirname = os.path.dirname(os.path.abspath(__file__))

    def test_true_fixtures(self):
        for filepath in glob.glob(
            os.path.join(
                self.dirname,
                "test_files/boolean_within_test",
                "true",
                "**",
                "*.geojson",
            ),
            recursive=True,
        ):
            geojson = load_json_file_sync(filepath)

            feature1 = geojson["features"][0]
            feature2 = geojson["features"][1]
            result = boolean_within(feature1, feature2)
            self.assertTrue(result, True)

    def test_false_fixtures(self):
        for filepath in glob.glob(
            os.path.join(
                self.dirname,
                "test_files/boolean_within_test",
                "false",
                "**",
                "*.geojson",
            ),
            recursive=True,
        ):
            geojson = load_json_file_sync(filepath)
            feature1 = geojson["features"][0]
            feature2 = geojson["features"][1]
            result = boolean_within(feature1, feature2)
            self.assertFalse(result, False)


class TestTurfBooleanPointInPolygonFeatureCollection(unittest.TestCase):
    def test_simple_polygon(self):
        poly = Polygon([[[0, 0], [0, 100], [100, 100], [100, 0], [0, 0]]])
        pt_in = Point([50, 50])
        pt_out = Point([140, 150])

        self.assertTrue(
            boolean_point_in_polygon(Feature(geometry=pt_in), Feature(geometry=poly)),
            "point inside simple polygon",
        )
        self.assertFalse(
            boolean_point_in_polygon(Feature(geometry=pt_out), Feature(geometry=poly)),
            "point outside simple polygon",
        )

    def test_concave_polygon(self):
        concave_poly = Polygon(
            [[[0, 0], [50, 50], [0, 100], [100, 100], [100, 0], [0, 0]]]
        )
        pt_concave_in = Point([75, 75])
        pt_concave_out = Point([25, 50])

        self.assertTrue(
            boolean_point_in_polygon(
                Feature(geometry=pt_concave_in), Feature(geometry=concave_poly)
            ),
            "point inside concave polygon",
        )
        self.assertFalse(
            boolean_point_in_polygon(
                Feature(geometry=pt_concave_out), Feature(geometry=concave_poly)
            ),
            "point outside concave polygon",
        )

    def test_poly_with_hole(self):
        pt_in_hole = Point([-86.69208526611328, 36.20373274711739])
        pt_in_poly = Point([-86.72229766845702, 36.20258997094334])
        pt_outside_poly = Point([-86.75079345703125, 36.18527313913089])

        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/test_files/boolean_point_in_polygon_test/in/poly-with-hole.geojson"
        ) as f:
            poly_hole = json.load(f)

        self.assertFalse(
            boolean_point_in_polygon(Feature(geometry=pt_in_hole), poly_hole)
        )
        self.assertTrue(boolean_point_in_polygon(Feature(geometry=pt_in_poly), poly_hole))
        self.assertFalse(
            boolean_point_in_polygon(Feature(geometry=pt_outside_poly), poly_hole)
        )

    def test_multipolygon_with_hole(self):
        pt_in_hole = Point([-86.69208526611328, 36.20373274711739])
        pt_in_poly = Point([-86.72229766845702, 36.20258997094334])
        pt_in_poly2 = Point([-86.75079345703125, 36.18527313913089])
        pt_outside_poly = Point([-86.75302505493164, 36.23015046460186])

        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/test_files/boolean_point_in_polygon_test/in/multipoly-with-hole.geojson"
        ) as f:
            multi_poly_hole = json.load(f)

        self.assertFalse(
            boolean_point_in_polygon(Feature(geometry=pt_in_hole), multi_poly_hole)
        )
        self.assertTrue(
            boolean_point_in_polygon(Feature(geometry=pt_in_poly), multi_poly_hole)
        )
        self.assertTrue(
            boolean_point_in_polygon(Feature(geometry=pt_in_poly2), multi_poly_hole)
        )
        self.assertTrue(
            boolean_point_in_polygon(Feature(geometry=pt_in_poly), multi_poly_hole)
        )
        self.assertFalse(
            boolean_point_in_polygon(Feature(geometry=pt_outside_poly), multi_poly_hole)
        )
