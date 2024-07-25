# BOILER PLATE FOR TESTING FLASK APPLICATION

import unittest
from app import app, db
from sqlalchemy.sql import text

class DataBaseConnectionTestCase(unittest.TestCase):

    def setUp(self):
        print('DATABASE SETUP STARTED')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Msi_123@localhost:5432/portal_data_base'
        self.app = app.test_client()

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

if __name__ == '__main__':
    unittest.main()