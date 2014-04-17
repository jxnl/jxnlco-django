import datetime
from django.test import TestCase
from blog.models import Entry, Term


class BlogPostTestCase(TestCase):

    fixtures = ['blog_test_data.json']

    def test_posts_have_style(self):
        first_post = Entry.objects.get(id=1)
        second_post = Entry.objects.get(id=2)
        self.assertEqual(first_post.style, 'making')
        self.assertEqual(second_post.style, 'writing')

    def test_posts_have_html(self):
        first_post = Entry.objects.get(id=1)
        second_post = Entry.objects.get(id=2)
        self.assertEqual(first_post.content_html, '<h1 id="title">title</h1>')
        self.assertEqual(
            second_post.content_html, '<p><strong>title</strong></p>')

    def test_posts_autoslug(self):
        first_post = Entry.objects.get(id=1)
        second_post = Entry.objects.get(id=2)
        self.assertEqual(first_post.slug, 'iiiiii11-jason')
        self.assertEqual(second_post.slug, 'test-one-two')

    def test_post_has_url(self):
        first_post = Entry.objects.get(id=2)
        self.assertEqual(first_post.urllink, '/writing/2/test-one-two/')


class TermTestCase(TestCase):

    fixtures = ['blog_test_data.json']

    def test_term_has_name(self):
        term = Term.objects.get(id=1)
        self.assertEqual(term.name, "test_term")

    def test_term_has_desc(self):
        term = Term.objects.get(id=1)
        self.assertEqual(term.desc, "test_desc")

    def test_term_has_start(self):
        term = Term.objects.get(id=1)
        self.assertEqual(term.start, datetime.date.today())

    def test_term_has_posts(self):
        term = Term.objects.get(id=2)
        posts = term.posts.all()
        # Notice that this also tests that most recent post is at [0]
        self.assertEqual(posts[0], Entry.objects.get(id=3))
        self.assertEqual(posts[1], Entry.objects.get(id=2))
