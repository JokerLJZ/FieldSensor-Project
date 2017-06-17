"""A MicroSoft Office access class."""
# -*- coding: utf-8 -*-
import os

import pypyodbc
import win32com.client

__author__ = 'JokerLiu'


class Access(object):
    """A access database class using PyPyodbc module."""

    def __init__(self, filename="TestDataBase"):
        """__init__ docstring."""
        if isinstance(filename, str):
            dbfile = os.getcwd() + "\\" + filename
        else:
            raise TypeError("Wrong access name type input which is not string")
        conn = ("DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                "DBQ=%s;" % dbfile)
        try:
            self.conn = pypyodbc.connect(conn)
        except pypyodbc.Error:
            oAccess = win32com.client.Dispatch('Access.Application')
            DbFile = r"%s" % dbfile
            dbLangGeneral = ';LANGID=0x0409;CP=1252;COUNTRY=0'
            dbVersion = 64
            oAccess.DBEngine.CreateDatabase(DbFile, dbLangGeneral, dbVersion)
            oAccess.Quit()
            del oAccess
            self.conn = pypyodbc.connect(conn)
        self.cursor = self.GetCursor()

    def GetCursor(self):
        """Return the cursor of access connection."""
        cursor = self.conn.cursor()
        return cursor

    def SetAutoCommit(self, state=True):
        """Set the autocommit status, the defalt state is True."""
        self.conn.autocommit = state

    def ConnClose(self):
        """Close the connection of database."""
        self.conn.close()

    def Execute(self, command=None):
        """Execute the sql command to manipulate the access database.

           ==============  ===========================================
           **Argument:**
           command         Defalt is None, input should be sql string.
           ==============  ===========================================
        """
        if not isinstance(command, str):
            raise TypeError("Sql command must be string.")
        self.cursor.execute(command)
        self.Commit()

    def Commit(self):
        """Commit the sql change."""
        self.cursor.commit()

    def CreateTable(self, tablename=None, columnnamelist=None, typelist=None):
        """
           Create the test table with typelist.

           Return True is success. Return False is failed to create

           ==============  =================================================
           **Argument:**
           tablename        Defalt is TestTable, input should be sql string.
           tablenamelist    Defalt is None, input should be string or list.
           typelist         Defalt is None, input should be a sql type list,
                            and lenth of which must be same as tablenamelist,
                            or left with None then type will set to varchar.
           ==============  =================================================
        """
        if not self.IsTableExist(tablename):
            self.Execute("CREATE TABLE %s" % tablename)

        elif tablename is None:
            raise ValueError("No tablename input, please check the input.")
        else:
            pass
        if columnnamelist is None:
            print("No table name would be create.")
            return False
        if typelist is None:
            typelist = ["VARCHAR(30)" for i in range(columnnamelist.__len__())]
            dic = dict(zip(columnnamelist, typelist))
        else:
            if len(columnnamelist) == len(typelist):
                dic = dict(zip(columnnamelist, typelist))
            else:
                raise ValueError("Wrong typelist input.")
                return False
        columnnamelist = list(columnnamelist)
        for obj in columnnamelist:
            if not self.IsColumnExist(tablename, str(obj)):
                self.cursor.execute("ALTER TABLE %s ADD %s %s"
                                    % (tablename, str(obj), str(dic[obj])))
                self.Commit()
            else:
                pass

    def CreateSerial(self, date="NOW()"):
        """Create the serial """
        if not self.IsTableExist("TestDate"):
            sql = "CREATE TABLE TestDate(TestSeriesNo AUTOINCREMENT \
                   PRIMARY KEY, TestDate datetime)"
            self.Execute(sql)
            sql = "INSERT INTO TestDate (TestDate) VALUES (%s)" % date
            self.Execute(sql)
        else:
            sql = "INSERT INTO TestDate (TestDate) VALUES (%s)" % date
            self.Execute(sql)
        sql = "SELECT LAST(TestSeriesNo) FROM TestDate"
        return self.cursor.execute(sql).fetchone()[0]

    def GetTableContent(self, tablename=None, columnname=None):
        """Get all table content, return a list group.

           ==============  ===================================================
           **Argument:**
           tablename        Defalt is None, str required.
           columnname       Defalt is None, a sql colume name string required.
           ==============  ===================================================
        """
        self.cursor.execute("SELECT %s FROM %s" % (columnname, tablename))
        content = list(map(list, self.cursor.fetchall()))
        return content

    def GetTableName(self):
        """Return the table name list."""
        table_name = [row[2] for row in self.cursor.tables(tableType='TABLE')]
        return table_name

    def GetColumnName(self, tablename=None):
        """Return a column list of the specific table.

           ==============  =================================================
           **Argument:**
           tablename        Defalt is None, str required.
           ==============  =================================================
        """
        if self.IsTableExist(tablename):
            column_name = [row[3] for row in
                           self.cursor.columns(table=tablename)]
        else:
            print("Wrong table name input in GetColumnName function.")
            column_name = None
        return column_name

    def IsTableExist(self, tablename=None):
        """
           Check the table in the database or not, return True or False.

           ==============  =================================================
           **Argument:**
           tablename        Defalt is None, str required.
           ==============  =================================================
        """
        if tablename in self.GetTableName():
            return True
        else:
            return False

    def IsTableContentExist(self, tablename=None):
        """
           Check the tablecontent is exist or not, return True or False.

           ==============  =================================================
           **Argument:**
           tablename        Defalt is None, str required.
           ==============  =================================================
        """
        sql = "SELECT COUNT(*) FROM %s" % tablename
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        if count == 0:
            return False
        else:
            return True

    def IsColumnExist(self, tablename=None, columnname=None):
        """
           Check the column in the table or not, return True or False.

           ==============  =================================================
           **Argument:**
           tablename        Defalt is None, str required.
           columnname       Defalt is None, str required.
           ==============  =================================================
        """
        if columnname in self.GetColumnName(tablename):
            return True
        else:
            return False


if __name__ == "__main__":
    db = Access("/TestResult/Database/TestDB.accdb")
    column = ("Frequency__MHz, Field__V_per_m, FieldResult__V_per_m,"
              " TestSeries")
    db.CreateTable(
        tablename="场强线性度",
        columnnamelist=column.split(", "),
        typelist=["DOUBLE", "DOUBLE", "DOUBLE", "DOUBLE"])
    serial = db.CreateSerial()
    db.cursor.execute(
        "INSERT INTO 场强线性度 (%s) VALUES (%f, %f, %f, %f)"
        % (column, "1800.0", "20.0", 21.0, serial))
    db.Commit()
    # sql = ""
    # db.Execute(sql)
