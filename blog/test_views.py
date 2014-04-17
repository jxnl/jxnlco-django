import datetime
from django.test import TestCase
from blog.models import Entry, Term


class PostViewTestCase(TestCase):

    fixtures = ['blog_test_data.json']

    def test_entry_context(self):
        resp = self.client.get('/writing/2/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('entry' in resp.context)
        self.assertEqual(Entry.objects.get(id=2), resp.context['entry'])

    def test_entry_has_next_prev_posts(self):
        resp = self.client.get('/writing/2/')
        self.assertTrue('next' in resp.context)
        self.assertTrue('prev' in resp.context)
        self.assertTrue(Entry.objects.get(id=3), resp.context['next'])
        self.assertTrue(Entry.objects.get(id=1), resp.context['prev'])

    def test_entry_no_prev_post(self):
        resp = self.client.get('/writing/1/')
        self.assertTrue('next' in resp.context)
        self.assertTrue('prev' not in resp.context)
        self.assertTrue(Entry.objects.get(id=2), resp.context['next'])
        self.assertEqual(Entry.objects.get(id=1), resp.context['entry'])

    def test_entry_no_next_post(self):
        resp = self.client.get('/writing/3/')
        self.assertTrue('next' not in resp.context)
        self.assertTrue('prev' in resp.context)
        self.assertTrue(Entry.objects.get(id=2), resp.context['prev'])
        self.assertEqual(Entry.objects.get(id=3), resp.context['entry'])

    def test_no_entry(self):
        resp = self.client.get('/writing/9/')
        self.assertEqual(resp.status_code, 404)


class PostListViewTestCase(TestCase):

    fixtures = ['blog_test_data.json']

    def test_has_term(self):
        resp = self.client.get('/blog/')
        self.assertTrue('cur_term' in resp.context)
        self.assertEqual(Term.objects.get(id=2), resp.context['cur_term'])

    def test_term_has_posts(self):
        resp = self.client.get('/blog/')
        self.assertEqual(Entry.objects.get(id=2),
                         resp.context['cur_term'].posts.all()[1])
        self.assertEqual(Entry.objects.get(id=3),
                         resp.context['cur_term'].posts.all()[0])


class ArchiveViewTestCase(TestCase):

    def setUp(self):
        Term.objects.create(
            id=1,
            name='test_term',
            desc='test_desc',
            start=datetime.date.today(),)

        Entry.objects.create(id=1,
                             title="iiIIii!!11 jason",
                             content_md='# title',
                             style='making',
                             start_date=datetime.date.today(),)

        Term.objects.create(
            id=2,
            name='test_term2',
            desc='test_desc2',
            start=datetime.date.today() +
            datetime.timedelta(days=2),)

        Entry.objects.create(id=2,
                             title="test one two",
                             content_md='**title**',
                             style='writing',
                             start_date=datetime.date.today() +
                             datetime.timedelta(days=2),)

        Entry.objects.create(id=3,
                             title="another",
                             content_md='**title**',
                             style='writing',
                             start_date=datetime.date.today() +
                             datetime.timedelta(days=3),)

    def test__term(self):
        resp = self.client.get('/archive/')
        self.assertTrue('terms' in resp.context)
