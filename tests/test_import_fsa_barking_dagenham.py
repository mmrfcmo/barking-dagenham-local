import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.request import Request

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "import_fsa_barking_dagenham.py"
SPEC = importlib.util.spec_from_file_location("fsa_importer", MODULE_PATH)
importer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(importer)


class FsaImporterTests(unittest.TestCase):
    def test_normalise_preserves_source_and_stages_unverified(self):
        row = importer.normalise({
            "FHRSID": 12345,
            "BusinessName": "  Example Café  ",
            "BusinessType": "Restaurant/Cafe/Canteen",
            "AddressLine1": "1 High Street",
            "AddressLine2": "",
            "AddressLine3": "Barking",
            "AddressLine4": "",
            "PostCode": "ig11 8aa",
            "RatingValue": "5",
            "RatingDate": "2026-08-01",
        }, "2026-10-29T00:00:00+00:00")
        self.assertEqual(row["name"], "Example Café")
        self.assertEqual(row["slug"], "example-caf-12345")
        self.assertEqual(row["postcode"], "IG11 8AA")
        self.assertEqual(row["fhrs_id"], "12345")
        self.assertEqual(row["verification_status"], "unverified")
        self.assertEqual(row["listing_status"], "draft")
        self.assertTrue(row["source_url"].endswith("/12345"))

    def test_clean_collapses_whitespace(self):
        self.assertEqual(importer.clean("  Example   Business\nLtd "), "Example Business Ltd")

    def test_default_authority_is_barking_and_dagenham(self):
        # The public FSA authority landing page for Barking and Dagenham uses ID 501.
        self.assertEqual(importer.BOROUGH, "Barking and Dagenham")
        self.assertEqual(importer.DEFAULT_AUTHORITY_ID, 501)

    def test_main_writes_csv_and_does_not_publish(self):
        payload = {"establishments": [{
            "FHRSID": 7,
            "BusinessName": "Sample Cafe",
            "BusinessType": "Restaurant/Cafe/Canteen",
            "AddressLine1": "2 Station Road",
            "AddressLine2": "",
            "AddressLine3": "Barking",
            "AddressLine4": "",
            "PostCode": "IG11 7AA",
            "RatingValue": "4",
            "RatingDate": "2026-01-01",
        }], "meta": {"totalPages": 1}}
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "batch.csv"
            with patch.object(importer, "request_page", return_value=payload):
                with patch("sys.argv", ["importer", "--limit", "1", "--output", str(output)]):
                    self.assertEqual(importer.main(), 0)
            with output.open(newline="", encoding="utf-8-sig") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["name"], "Sample Cafe")
            self.assertEqual(rows[0]["listing_status"], "draft")
            self.assertEqual(rows[0]["verification_status"], "unverified")


if __name__ == "__main__":
    unittest.main()
