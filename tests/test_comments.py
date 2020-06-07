import unittest
from app.models import Comments, User
from app import db


class CommentsTest(unittest.TestCase):
    def setUp(self):

        self.new_comment = Comment(
            id=1, comment='Test comment', user=self.user_rose, pitch_id=self.new_pitch)

    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment, 'Test comment')
        self.assertEquals(self.new_comment.user, self.user_rose)
        self.assertEquals(self.new_comment.pitch_id, self.new_pitch)


class CommentTest(unittest.TestCase):
    def setUp(self):
        self.user_rose = User(
            username='rose', password='cairo', email='test@test.com')
        self.new_pitch = Pitch(
            id=1, title='Test', content='This is a test pitchapp', user_id=self.user_rose.id)
        self.new_comment = Comment(
            id=1, comment='This is a test comments', user_id=self.user_rose.id, pitch_id=self.new_pitch.id)

    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()
        Comment.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment, 'This is a test comments')
        self.assertEquals(self.new_comment.user_id, self.user_rose.id)
        self.assertEquals(self.new_comment.pitch_id, self.new_pitch.id)

    def test_save_comment(self):
        self.new_comment.save()
        self.assertTrue(len(Comment.query.all()) > 0)

    def test_get_comment(self):
        self.new_comment.save()
        got_comment = Comment.get_comment(1)
        self.assertTrue(get_comment is not None)