from unittest.mock import patch
import unittest
from sqlalchemy import insert
from sqlalchemy import table
from sqlalchemy import create_engine

import os, inspect

class DataBaseManager:
    def __init__(self):
        self._table = table('test')
        self._engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        
    def add(self, value:str, extra_value:str):

        statement = (insert(self._table).values(name=value, extra = extra_value))
        statement.compile()
        
        with self._engine.connect() as conn:
            result = conn.execute(statement)
            conn.commit()
            
            


class UnitTestDataBaseManager(unittest.TestCase):

    @patch('__main__.insert')
    @patch('__main__.create_engine')
    @patch('__main__.table')

    def test_databasemanager_add(self, patch_table, patch_create_engine, patch_sqlalchemy_insert):
        
        #print("ATH", os.path.abspath(inspect.getfile(table)))
        patch_table.return_value = None
        dbm = DataBaseManager()
        
        # action!
        dbm.add('first', 'last')
        
        # using spies
        patch_sqlalchemy_insert.assert_called_once_with(dbm._table)
        patch_sqlalchemy_insert.return_value.values.assert_called_once_with(name='first', extra='last')
        patch_sqlalchemy_insert.return_value.values.return_value.compile.assert_called_once()
        patch_create_engine.return_value.connect.assert_called_once()


class IntegrationTest(unittest.TestCase):
    
    def setUp(self) -> None:
        # set up a testing evironment
        # we will create a database 
        self.dbm = DataBaseManager()
        
    def tearDown(self) -> None:
        # destroy testing environment for the database
        self.dbm.remove()

    def test_databasemanager_add(self):
        self.dbm.add("fist", "last")
        
        # check that dbm has saved correct entries
        self.dbm.get("first", "last")

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
