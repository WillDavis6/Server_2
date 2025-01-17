# BOILER PLATE FOR TESTING FLASK APPLICATION

import unittest
from app import app, db
from sqlalchemy.sql import text
from sqlalchemy import inspect, create_engine
from ignore_DO_NOT_UPLOAD import db_url, expected_tables, table_column_list, table_column_type_list
class DataBaseConnectionTestCase(unittest.TestCase):

    def setUp(self):
        
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
        self.app = app.test_client()
        self.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        self.inspector = inspect(self.engine)

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_db_connect(self):
        """Test database connection"""
        with app.app_context():
            result = db.session.execute(text('SELECT 1'))
            self.assertEqual(result.fetchone()[0], 1)

    def test_tables_exist(self):
        
        # Get list of tables from database
        actual_tables = self.inspector.get_table_names()
        for table in expected_tables:
            self.assertIn(table, actual_tables, f"Table {table} does not exist in the database")

    
    def test_tables_columns_and_types(self):
        actual_tables = self.inspector.get_table_names()

        for column_names, column_type, table_name in zip(table_column_list, table_column_type_list, actual_tables):
            #Find Tables in Database
        
            #Find Columns in table found with match
            columns = self.inspector.get_columns(table_name)
            
            #Iterate over columns to look for
            for name, column_type_z in zip(column_names, column_type) :
                #Search for match between columns to look for and what was found in database
                column = next((col for col in columns if col['name'] == name), None)

                #Test if column exists
                self.assertIsNotNone(column, f"Column {name} does not exist in {table_name}")
             

                #Test if column type is correct
                column_type = column['type']
                self.assertTrue(isinstance(column_type, column_type_z), f"Column {name}, is not of the type {column_type}")
            
            
    def test_table_relationships(self):
        foreign_keys = self.inspector.get_foreign_keys('nacelle_5005_joggle_ref')
        related_tables = [fk['referred_table'] for fk in foreign_keys]
        self.assertIn('a10_5005_joggle', related_tables, "Table 'a10_5005_joggle' does not have a foreign key")

    def test_primary_keys(self):
        table_name = 'a10_5005_joggle'
        expected_pks = ['joggle_id']
        primary_keys = self.inspector.get_pk_constraint(table_name)['constrained_columns']
        self.assertEqual(primary_keys, expected_pks, f"Primary keys {primary_keys} do not match expected {expected_pks}")

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Server 2', response.data)

    def test_404_error(self):
        response = self.app.get('/non_existent_page')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)
    
    


if __name__ == '__main__':
    unittest.main()