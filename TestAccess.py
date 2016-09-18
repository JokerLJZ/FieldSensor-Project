"""Test the AccessODBC module."""
import unittest
import os

from Access import Access

__author__ = 'JokerLiu'


class TestAccess(unittest.TestCase):
    """Test the access funcion."""

    def setUp(self):
        """Initial the test, create database."""
        self.accdb = Access("Test.accdb")
        self.mdb = Access("Test.mdb")
        self.accdb.CreateTable(tablename="TestTable",
                               columnnamelist=["TestColumn"],
                               typelist=["VARCHAR(30)"])
        self.mdb.CreateTable(tablename="TestTable",
                             columnnamelist=["TestColumn"],
                             typelist=["VARCHAR(30)"])

    def tearDown(self):
        """End the test with remove test database."""
        self.accdb.ConnClose()
        self.mdb.ConnClose()
        os.remove("Test.accdb")
        os.remove("Test.mdb")

    def testCreateTable(self):
        """Test create table function."""
        self.assertEqual(self.accdb.IsTableExist("TestTable"), True)
        self.assertEqual(self.mdb.IsTableExist("TestTable"), True)

    def testCreateColumn(self):
        """Test create column in table function."""
        self.assertEqual(
            self.accdb.IsColumnExist(tablename="TestTable",
                                     columnname="TestColumn"), True)
        self.assertEqual(
            self.mdb.IsColumnExist(tablename="TestTable",
                                   columnname="TestColumn"), True)


if __name__ == "__main__":
    unittest.main()
