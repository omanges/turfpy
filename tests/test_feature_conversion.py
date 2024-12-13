"""
Test module for feature conversions.
"""

import json
import os
import unittest
from pathlib import Path

from turfpy.feature_conversion import polygon_to_line

# Define directories
current_dir = Path(__file__).resolve().parent
directories = {
    "in": current_dir / "test_files/feature_conversion_polygon_to_line_test" / "in",
    "out": current_dir / "test_files/feature_conversion_polygon_to_line_test" / "out",
}

# Load fixtures
fixtures = []
for filename in os.listdir(directories["in"]):
    filepath = directories["in"] / filename
    with open(filepath, "r") as file:
        geojson = json.load(file)
    fixtures.append(
        {
            "filename": filename,
            "name": Path(filename).stem,
            "geojson": geojson,
        }
    )


class TestPolygonToLine(unittest.TestCase):
    def test_polygon_to_linestring(self):
        for fixture in fixtures:
            name = fixture["name"]
            filename = fixture["filename"]
            geojson = fixture["geojson"]

            # Perform the conversion
            results = polygon_to_line(geojson)

            # Load the expected results
            with open(directories["out"] / filename, "r") as file:
                expected_results = json.load(file)

            # Assert the results are as expected
            self.assertEqual(results, expected_results, name)
