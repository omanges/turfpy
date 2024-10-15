"""
Test module for booleans.
"""
import os
import json
import glob
import unittest

from turfpy.boolean import (
    boolean_disjoint,
    boolean_intersects,
)

def load_json_file_sync(filepath):
    with open(filepath) as f:
        return json.load(f)


class TestTurfBooleanDisjoint(unittest.TestCase):
    def setUp(self):
        self.dirname = os.path.dirname(os.path.abspath(__file__))

    def test_true_fixtures(self):
        for filepath in glob.glob(os.path.join(self.dirname, "boolean_disjoint_test", "true", "**", "*.geojson"), recursive=True):
            geojson = load_json_file_sync(filepath)
            feature1 = geojson['features'][0]
            feature2 = geojson['features'][1]
            result = boolean_disjoint(feature1, feature2)
            self.assertTrue(result, True)

    def test_false_fixtures(self):
        for filepath in glob.glob(os.path.join(self.dirname, "boolean_disjoint_test", "false", "**", "*.geojson"), recursive=True):
            geojson = load_json_file_sync(filepath)
            feature1 = geojson['features'][0]
            feature2 = geojson['features'][1]
            result = boolean_disjoint(feature1, feature2)
            self.assertFalse(result, False)

class TestTurfBooleanIntersects(unittest.TestCase):
    def setUp(self):
        self.dirname = os.path.dirname(os.path.abspath(__file__))

    def test_true_fixtures(self):
        for filepath in glob.glob(os.path.join(self.dirname, "boolean_intersects_test", "true", "**", "*.geojson"), recursive=True):
            geojson = load_json_file_sync(filepath)
            feature1 = geojson['features'][0]
            feature2 = geojson['features'][1]
            result = boolean_intersects(feature1, feature2)
            self.assertTrue(result, True)

    def test_false_fixtures(self):
        for filepath in glob.glob(os.path.join(self.dirname, "boolean_intersects_test", "false", "**", "*.geojson"), recursive=True):
            geojson = load_json_file_sync(filepath)
            feature1 = geojson['features'][0]
            feature2 = geojson['features'][1]
            result = boolean_intersects(feature1, feature2)
            self.assertFalse(result, False)