# BOILER PLATE FOR TESTING FLASK APPLICATION

import unittest
from app import app, db

class DataBaseConnectionTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = ''
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_db_connect(self):
        """Test database connection"""
        with app.app_context():
            result = db.session.execute('SELECT 1')
            self.assertEqual(result.fetchone()[0], 1)

if __name__ == '__main__':
    unittest.main()