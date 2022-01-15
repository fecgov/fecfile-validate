import json
import unittest

from validate import app


class BaseDatabaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # app_step_3.config.update({
        #     'DATABASE_NAME': TESTING_DATABASE_NAME
        # })
        # cls.db = sqlite3.connect(TESTING_DATABASE_NAME)
        # cls.db.execute(CREATE_BOOK_TABLE_QUERY)
        # cls.db.commit()
        pass

    @classmethod
    def tearDownClass(cls):
        # os.remove(TESTING_DATABASE_NAME)
        pass

    def setUp(self):
        # self.app = self.APP.test_client()
        # self.db.execute("DELETE FROM book;")
        # self.db.commit()
        pass


class Step3TestCase(BaseDatabaseTestCase):
    APP = app

    # noinspection SpellCheckingInspection
    def test_validate_parameters(self):
        # Preconditions
        resp = self.app.get('/book')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        # Precondition: no books in the DB
        content = json.loads(resp.get_data(as_text=True))
        self.assertEqual(len(content), 0)

        # Test
        post_data = {
            'title': 'Ulysses',
            'author_id': 2
        }
        resp = self.app.post('/book',
                             data=json.dumps(post_data),
                             content_type='application/json')

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.content_type, 'application/json')

        # Postconditions
        resp = self.app.get('/book')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        # Postcondtion: 2 books
        content = json.loads(resp.get_data(as_text=True))
        self.assertEqual(len(content), 1)

        # Postcondtion: Books correct ID incremented
        ulysses = content[0]

        self.assertEqual(ulysses, {
            'id': 1,
            'title': 'Ulysses',
            'author_id': 2
        })

    def test_book_creation_incorrect_parameters(self):
        # Forget the title argument
        post_data = {
            'author_id': 2
        }
        resp = self.app.post('/book',
                             data=json.dumps(post_data),
                             content_type='application/json')

        self.assertEqual(resp.status_code, 400)
        self.assertTrue('title' in resp.get_data(as_text=True))

    def test_book_creation_incorrect_content_type(self):
        # Forget the title argument
        post_data = {
            'author_id': 2,
            'title': 'Ulysses'
        }
        resp = self.app.post('/book',
                             data=json.dumps(post_data))

        self.assertEqual(resp.status_code, 400)
        self.assertTrue('Content Type' in resp.get_data(as_text=True))
