"""检查演练资料的读取契约和关联锚点。"""
import csv
from pathlib import Path
import unittest

INPUTS = Path(__file__).resolve().parent.parent / "samples"

HEADERS = {'circles': ('wave', 'circle', 'roster', 'capacity', 'fixed_recipients', 'holdout'), 'links': ('wave', 'left', 'right', 'posting', 'dir'), 'designs': ('wave', 'level', 'fraction', 'min_circles', 'max_circles', 'seed', 'cutoff'), 'assignment': ('wave', 'circle', 'level', 'people_assigned'), 'contacts': ('wave', 'person', 'serving_circle', 'posting', 'kind', 'at'), 'placements': ('wave', 'reporting_circle', 'person', 'employer', 'placement_id', 'posting', 'result', 'at'), 'amendments': ('change', 'wave', 'kind', 'left', 'right', 'found_after', 'recorded')}
REFERENCES = [('assignment', 'circle', 'circles', 'circle'), ('placements', 'posting', 'links', 'posting'), ('assignment', 'level', 'designs', 'level')]
EXAMPLES = [['circles', 'wave', 'W2', 5], ['placements', 'placement_id', 'P1', 2], ['contacts', 'kind', 'forwarded', 2]]


class SampleInputContract(unittest.TestCase):
    def read(self, table):
        with (INPUTS / f"{table}.csv").open(encoding="utf-8", newline="") as source:
            reader = csv.DictReader(source, strict=True)
            self.assertEqual(tuple(reader.fieldnames), HEADERS[table])
            rows = list(reader)
        self.assertTrue(rows, table)
        for row in rows:
            self.assertNotIn(None, row, table)
            self.assertNotIn(None, row.values(), table)
        return rows

    def test_csv_readable_with_documented_columns(self):
        for table in HEADERS:
            with self.subTest(table=table):
                self.read(table)

    def test_cross_source_example_references(self):
        for source, source_field, target, target_field in REFERENCES:
            with self.subTest(source=source, field=source_field, target=target):
                available = {row[target_field] for row in self.read(target)}
                actual = {value for row in self.read(source)
                          for value in row[source_field].split("|") if value}
                self.assertTrue(actual)
                self.assertEqual(actual - available, set())

    def test_example_revisions_and_overlaps_are_present(self):
        for table, field, example, expected in EXAMPLES:
            with self.subTest(table=table, field=field, example=example):
                found = sum((row[field] == example if "|" in example else example in row[field].split("|")) for row in self.read(table))
                self.assertEqual(found, expected)


if __name__ == "__main__":
    unittest.main()
