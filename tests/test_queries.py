from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from demo.queries.library import raw_query, sqlalchemy_query
from demo.sqlalchemy.model import Base, People
from demo.sqlalchemy.insert_names import insert_names


class TestQueries(TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        self.session = Session(bind=engine)
        insert_names(self.session)

    def test_raw_query_initial_data(self):
        """Expect result of 4 (Evans and Johnson)"""
        results = list(raw_query(self.session))
        self.assertEqual(len(results), 4)

    def test_raw_query_another_evans(self):
        """Expect result of 5 by adding another Evans"""
        new_evans = People(first_name='Sarah', last_name='Evans')
        self.session.add(new_evans)
        self.session.commit()
        results = list(raw_query(self.session))
        self.assertEqual(len(results), 5)

    def test_raw_query_delete_one_from_initial_data(self):
        """Expect only 2 after deleting a Johnson"""
        self.session.query(People).filter(People.first_name == 'Simon').filter(People.last_name == 'Johnson').delete()
        self.session.commit()
        results = list(raw_query(self.session))
        self.assertEqual(len(results), 2)

    def test_sqlachemy_query_initial_data(self):
        """Expect result of 4 (Evans and Johnson)"""
        results = list(sqlalchemy_query(self.session))
        self.assertEqual(len(results), 4)

    def test_sqlalchemy_query_another_evans(self):
        """Expect result of 5 by adding another Evans"""
        new_evans = People(first_name='Sarah', last_name='Evans')
        self.session.add(new_evans)
        self.session.commit()
        results = list(sqlalchemy_query(self.session))
        self.assertEqual(len(results), 5)

    def test_sqlalchemy_query_delete_one_from_initial_data(self):
        """Expect only 2 after deleting a Johnson"""
        self.session.query(People).filter(People.first_name == 'Simon').filter(People.last_name == 'Johnson').delete()
        self.session.commit()
        results = list(sqlalchemy_query(self.session))
        self.assertEqual(len(results), 2)
