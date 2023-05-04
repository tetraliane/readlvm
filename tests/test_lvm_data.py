import unittest
from readlvm import LvmData


class TestUnitTest(unittest.TestCase):
    def test_should_include_all_fields_in_yaml_output(self):
        lvm = LvmData(
            "Test title", {"Date": "2020/01/01"}, ["x", "y"], [["0", "2"], ["1", "3"]]
        )

        yaml = lvm.into_yaml()
        self.assertEqual(yaml["title"], "Test title")
        self.assertEqual(yaml["header"], {"Date": "2020/01/01"})
        self.assertEqual(yaml["data_labels"], ["x", "y"])
        self.assertEqual(yaml["data"], [["0", "2"], ["1", "3"]])

    def test_should_read_lvm_file(self):
        lvm = LvmData.read("tests/test_normal.lvm")
        self.assertEqual(lvm.title(), "Test 1")
        self.assertEqual(
            lvm.header(), {"Date": "2020/01/01", "Time": "12:34:56.7802109249124236187"}
        )
        self.assertEqual(lvm.data_labels(), ["index", "x", "y"])
        self.assertEqual(
            lvm.data(), [["0", "1", "1"], ["1", "2", "4"], ["2", "4", "16"]]
        )

    def test_lvm_file_may_lack_some_data(self):
        lvm = LvmData.read("tests/test_with_lack.lvm")
        self.assertEqual(lvm.title(), "Test 1")
        self.assertEqual(
            lvm.header(), {"Date": "2020/01/01", "Time": "12:34:56.7802109249124236187"}
        )
        self.assertEqual(lvm.data_labels(), ["index", "x", "y"])
        self.assertEqual(lvm.data(), [["", "1", "1"], ["1", "2", ""], ["", "4", ""]])

    def test_lvm_file_may_contain_comments(self):
        lvm = LvmData.read("tests/test_comment.lvm")
        self.assertEqual(lvm.title(), "Test 1")
        self.assertEqual(
            lvm.header(), {"Date": "2020/01/01", "Time": "12:34:56.7802109249124236187"}
        )
        self.assertEqual(lvm.data_labels(), ["index", "x", "y"])
        self.assertEqual(
            lvm.data(), [["0", "1", "1"], ["1", "2", "4"], ["2", "4", "16"]]
        )

    def test_lvm_file_may_empty_lines(self):
        lvm = LvmData.read("tests/test_empty_line.lvm")
        self.assertEqual(lvm.title(), "Test 1")
        self.assertEqual(
            lvm.header(), {"Date": "2020/01/01", "Time": "12:34:56.7802109249124236187"}
        )
        self.assertEqual(lvm.data_labels(), ["index", "x", "y"])
        self.assertEqual(
            lvm.data(), [["0", "1", "1"], ["1", "2", "4"], ["2", "4", "16"]]
        )

    def test_pick_up_single_row_and_compress_it(self):
        lvm = LvmData(
            "Test title",
            {"Date": "2020/01/01"},
            ["index", "x", "y"],
            [
                ["0", "0", "2"],
                ["1", "1", "3"],
                ["2", "1", "4"],
                ["3", "2", "5"],
                ["4", "3", "6"],
            ],
        )

        compressed = lvm.compress_data(1)
        self.assertEqual(compressed.data_labels(), ["x", "count_of_x"])
        self.assertEqual(compressed.data(), [["0", 1], ["1", 2], ["2", 1], ["3", 1]])
