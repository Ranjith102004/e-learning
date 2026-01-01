# EXPERIMENTAL: MongoEngine tests (optional)
# These tests exercise the example MongoEngine CourseDocument. They are
# experimental and optional — install `mongomock` to run in-memory or provide
# a running MongoDB instance for integration testing.

import os
import unittest

import mongoengine

try:
    import mongomock  # optional, used for in-memory MongoDB in tests
    MONGOMOCK_AVAILABLE = True
except Exception:
    MONGOMOCK_AVAILABLE = False

from apps.courses.mongo_models import CourseDocument, ModuleEmbedded, LessonEmbedded


class MongoCourseTestCase(unittest.TestCase):
    def setUp(self):
        # Connect to a test database. Prefer mongomock if available.
        if MONGOMOCK_AVAILABLE:
            # Use mongomock's MongoClient with mongoengine >=0.20 support
            mongoengine.connect(
                db='edutech_test_db',
                host='mongodb://localhost',
                mongo_client_class=mongomock.MongoClient,
            )
        else:
            # Fall back to a real MongoDB instance (ensure it's running)
            mongo_host = os.environ.get('MONGO_HOST', 'mongodb://localhost:27017/edutech_test_db')
            try:
                mongoengine.connect(host=mongo_host)
            except Exception as e:
                self.skipTest(f"Cannot connect to MongoDB for tests: {e}")

    def tearDown(self):
        # Drop test DB and disconnect
        try:
            conn = mongoengine.connection.get_db()
            conn.client.drop_database(conn.name)
        except Exception:
            pass
        mongoengine.disconnect()

    def test_create_and_query_course(self):
        lesson1 = LessonEmbedded(title='Intro', video_url='http://example.com/1', content='Lesson 1', order=1)
        lesson2 = LessonEmbedded(title='Advanced', video_url='http://example.com/2', content='Lesson 2', order=2)
        module = ModuleEmbedded(title='Module 1', order=1, lessons=[lesson1, lesson2])

        course = CourseDocument(
            instructor_id=1,
            title='Mongo Course',
            description='A course stored in MongoDB',
            price='19.99',
            is_published=True,
            modules=[module],
        )
        course.save()

        fetched = CourseDocument.objects.first()
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.title, 'Mongo Course')
        self.assertEqual(fetched.instructor_id, 1)
        self.assertTrue(fetched.is_published)
        self.assertEqual(len(fetched.modules), 1)
        self.assertEqual(len(fetched.modules[0].lessons), 2)


if __name__ == '__main__':
    unittest.main()
