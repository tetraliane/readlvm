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
        with open("tests/test_normal.lvm", "r") as f:
            lvm = LvmData.read(f)
        self.assertEqual(lvm.title(), "Test 1")
        self.assertEqual(
            lvm.header(), {"Date": "2020/01/01", "Time": "12:34:56.7802109249124236187"}
        )
        self.assertEqual(lvm.data_labels(), ["index", "x", "y"])
        self.assertEqual(
            lvm.data(), [["0", "1", "1"], ["1", "2", "4"], ["2", "4", "16"]]
        )

    def test_lvm_file_may_lack_some_data(self):
        with open("tests/test_with_lack.lvm", "r") as f:
            lvm = LvmData.read(f)
        self.assertEqual(lvm.title(), "Test 1")
        self.assertEqual(
            lvm.header(), {"Date": "2020/01/01", "Time": "12:34:56.7802109249124236187"}
        )
        self.assertEqual(lvm.data_labels(), ["index", "x", "y"])
        self.assertEqual(lvm.data(), [["", "1", "1"], ["1", "2", ""], ["", "4", ""]])

    def test_lvm_file_may_contain_comments(self):
        with open("tests/test_comment.lvm", "r") as f:
            lvm = LvmData.read(f)
        self.assertEqual(lvm.title(), "Test 1")
        self.assertEqual(
            lvm.header(), {"Date": "2020/01/01", "Time": "12:34:56.7802109249124236187"}
        )
        self.assertEqual(lvm.data_labels(), ["index", "x", "y"])
        self.assertEqual(
            lvm.data(), [["0", "1", "1"], ["1", "2", "4"], ["2", "4", "16"]]
        )

    def test_lvm_file_may_empty_lines(self):
        with open("tests/test_empty_line.lvm", "r") as f:
            lvm = LvmData.read(f)
        self.assertEqual(lvm.title(), "Test 1")
        self.assertEqual(
            lvm.header(), {"Date": "2020/01/01", "Time": "12:34:56.7802109249124236187"}
        )
        self.assertEqual(lvm.data_labels(), ["index", "x", "y"])
        self.assertEqual(
            lvm.data(), [["0", "1", "1"], ["1", "2", "4"], ["2", "4", "16"]]
        )

    def test_pick_up_columns(self):
        lvm = LvmData(
            "Test title",
            {"Date": "2020/01/01"},
            ["index", "x", "y"],
            [["0", "2", "4"], ["1", "3", "8"]],
        )
        lvm.pick_cols([0, 2])
        self.assertEqual(lvm.data_labels(), ["index", "y"])
        self.assertEqual(lvm.data(), [["0", "4"], ["1", "8"]])
