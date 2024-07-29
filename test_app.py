# BOILER PLATE FOR TESTING FLASK APPLICATION

import unittest
from app import app, db
from sqlalchemy.sql import text
from sqlalchemy import inspect, create_engine
from ignore_DO_NOT_UPLOAD import db_url, expected_tables

class DataBaseConnectionTestCase(unittest.TestCase):

    def setUp(self):
        print('DATABASE SETUP STARTED')
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
        with app.app_context():
            # Get list of tables from database
            actual_tables = self.inspector.get_table_names()
            for table in expected_tables:
                self.assertIn(table, actual_tables, f"Table {table} does not exist in the database")

    def test_table_columns(self):
        with app.app_context():
            actual_tables = self.inspector.get_table_names()
            for table_name in expected_tables:
                table = next((tab for tab in actual_tables if tab['name'] == table_name), None)
                columns = self.inspector.get_columns(table)
                column = next((col for col in columns if col['name'] == column_name), None)


if __name__ == '__main__':
    unittest.main()