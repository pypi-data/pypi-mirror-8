# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from fields import ManyToManyHistoryField
from datetime import datetime
from models import ManyToManyHistoryVersion
import time

'''
Example model from Django docs: https://docs.djangoproject.com/en/dev/topics/db/examples/many_to_many/
'''

class Publication(models.Model):
    title = models.CharField(max_length=30)


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = ManyToManyHistoryField(Publication, cache=True)
    publications_no_cache = ManyToManyHistoryField(Publication, related_name='articles_no_cache')


'''
Test class
'''

class ManyToManyHistoryTest(TestCase):

    def test_m2m_fields_and_methods(self):
        self.assertItemsEqual([field.name for field in Article._meta.get_field('publications').rel.through._meta.local_fields], [u'id', 'time_from', 'time_to', 'article', 'publication'])

    def test_m2m_history_features(self):

        p1 = Publication.objects.create(title='Pub1')
        p2 = Publication.objects.create(title='Pub2')
        p3 = Publication.objects.create(title='Pub3')

        article = Article.objects.create(headline='Article1')
        state_time1 = datetime.now()
        # we need to use sleep here to pass travis mysql tests, becouse Django + mysql doesn't support storing microseconds
        # and as result our state_timeX will be equal
        time.sleep(1)

        article.publications = [p1, p2]
        state_time2 = article.publications.last_update_time()
        self.assertItemsEqual(article.publications.all(), [p1, p2])
        self.assertEqual(article.publications.count(), 2)
        self.assertEqual(article.publications.through.objects.count(), 2)
        time.sleep(1)

        article.publications = [p3]
        state_time3 = article.publications.last_update_time()
        self.assertItemsEqual(article.publications.all(), [p3])
        self.assertEqual(article.publications.count(), 1)
        self.assertEqual(article.publications.through.objects.count(), 3)
        time.sleep(1)

        article.publications.add(p2, p1)
        state_time4 = article.publications.last_update_time()
        self.assertItemsEqual(article.publications.all(), [p1, p2, p3])
        self.assertEqual(article.publications.count(), 3)
        self.assertEqual(article.publications.through.objects.count(), 5)
        time.sleep(1)

        article.publications.remove(p2, p1)
        state_time5 = article.publications.last_update_time()
        self.assertItemsEqual(article.publications.all(), [p3])
        self.assertEqual(article.publications.count(), 1)
        self.assertEqual(article.publications.through.objects.count(), 5)
        time.sleep(1)

        article.publications = [p1, p2]
        state_time6 = article.publications.last_update_time()
        self.assertItemsEqual(article.publications.all(), [p1, p2])
        self.assertEqual(article.publications.count(), 2)
        self.assertEqual(article.publications.through.objects.count(), 7)
        time.sleep(1)

        article.publications.clear()
        state_time7 = article.publications.last_update_time()
        self.assertItemsEqual(article.publications.all(), [])
        self.assertEqual(article.publications.count(), 0)
        self.assertEqual(article.publications.through.objects.count(), 7)
        time.sleep(1)

        # test of history
        self.assertItemsEqual(article.publications.were_at(state_time1), [])
        self.assertItemsEqual(article.publications.were_at(state_time2), [p1, p2])
        self.assertItemsEqual(article.publications.were_at(state_time3), [p3])
        self.assertItemsEqual(article.publications.were_at(state_time4), [p1, p2, p3])
        self.assertItemsEqual(article.publications.were_at(state_time5), [p3])
        self.assertItemsEqual(article.publications.were_at(state_time6), [p1, p2])
        self.assertItemsEqual(article.publications.were_at(state_time7), [])

        # test of added_at and removed
        self.assertItemsEqual(article.publications.added_at(state_time2), [p1, p2])
        self.assertItemsEqual(article.publications.removed_at(state_time2), [])
        self.assertItemsEqual(article.publications.added_at(state_time3), [p3])
        self.assertItemsEqual(article.publications.removed_at(state_time3), [p1, p2])
        self.assertItemsEqual(article.publications.added_at(state_time4), [p1, p2])
        self.assertItemsEqual(article.publications.removed_at(state_time4), [])
        self.assertItemsEqual(article.publications.added_at(state_time5), [])
        self.assertItemsEqual(article.publications.removed_at(state_time5), [p1, p2])
        self.assertItemsEqual(article.publications.added_at(state_time6), [p1, p2])
        self.assertItemsEqual(article.publications.removed_at(state_time6), [p3])
        self.assertItemsEqual(article.publications.added_at(state_time7), [])
        self.assertItemsEqual(article.publications.removed_at(state_time7), [p1, p2])

        # test different arguments
        self.assertItemsEqual(article.publications.were_at(state_time4, only_pk=True), map(lambda o: o.pk, article.publications.were_at(state_time4)))
        with self.assertRaises(ValueError):
            article.publications.were_at(state_time5, unique=False)

        # test versions
        self.assertEqual(ManyToManyHistoryVersion.objects.count(), 6)
        for i in range(2, 8):
            state_time = locals()['state_time%d' % i]
            version = article.publications.versions.get(time=state_time)
            self.assertItemsEqual(version.items,    article.publications.were_at(state_time))
            self.assertItemsEqual(version.added,    article.publications.added_at(state_time))
            self.assertItemsEqual(version.removed,  article.publications.removed_at(state_time))
            self.assertEqual(version.count,         article.publications.were_at(state_time).count())
            self.assertEqual(version.added_count,   article.publications.added_at(state_time).count())
            self.assertEqual(version.removed_count, article.publications.removed_at(state_time).count())

        article.publications_no_cache = [p1, p2]
        self.assertEqual(ManyToManyHistoryVersion.objects.count(), 6)

    def test_m2m_default_features(self):
        '''
        Build-in test from https://docs.djangoproject.com/en/dev/topics/db/examples/many_to_many/
        '''
        p1 = Publication(title='The Python Journal')
        p1.save()
        p2 = Publication(title='Science News')
        p2.save()
        p3 = Publication(title='Science Weekly')
        p3.save()

        a1 = Article(headline='Django lets you build Web apps easily')
        a1.save()
        a1.publications.add(p1)

        a2 = Article(headline='NASA uses Python')
        a2.save()
        a2.publications.add(p1, p2)
        a2.publications.add(p3)
        a2.publications.add(p3)
        with self.assertRaises(TypeError):
            a2.publications.add(a1)

        p4 = a2.publications.create(title='Highlights for Children')
        self.assertItemsEqual(a1.publications.all(), [p1])
        self.assertItemsEqual(a2.publications.all(), [p4, p2, p3, p1])

        self.assertItemsEqual(p2.article_set.all(), [a2])
        self.assertItemsEqual(p1.article_set.all(), [a1, a2])
        self.assertItemsEqual(Publication.objects.get(id=4).article_set.all(), [a2])

        self.assertItemsEqual(Article.objects.filter(publications__id=1), [a1, a2])
        self.assertItemsEqual(Article.objects.filter(publications__pk=1), [a1, a2])
        self.assertItemsEqual(Article.objects.filter(publications=1), [a1, a2])
        self.assertItemsEqual(Article.objects.filter(publications=p1), [a1, a2])

        self.assertItemsEqual(Article.objects.filter(publications__title__startswith="Science"), [a2, a2])
        self.assertItemsEqual(Article.objects.filter(publications__title__startswith="Science").distinct(), [a2])
        self.assertEqual(Article.objects.filter(publications__title__startswith="Science").count(), 2)
        self.assertEqual(Article.objects.filter(publications__title__startswith="Science").distinct().count(), 1)

        self.assertItemsEqual(Article.objects.filter(publications__in=[1,2]).distinct(), [a1, a2])
        self.assertItemsEqual(Article.objects.filter(publications__in=[p1,p2]).distinct(), [a1, a2])

        self.assertItemsEqual(Publication.objects.filter(id=1), [p1])
        self.assertItemsEqual(Publication.objects.filter(pk=1), [p1])
        self.assertItemsEqual(Publication.objects.filter(article__headline__startswith="NASA"), [p4, p3, p2, p1])

        self.assertItemsEqual(Publication.objects.filter(article__id=1), [p1])
        self.assertItemsEqual(Publication.objects.filter(article__pk=1), [p1])
        self.assertItemsEqual(Publication.objects.filter(article=1), [p1])
        self.assertItemsEqual(Publication.objects.filter(article=a1), [p1])

        self.assertItemsEqual(Publication.objects.filter(article__in=[1,2]).distinct(), [p1, p2, p3, p4])
        self.assertItemsEqual(Publication.objects.filter(article__in=[a1,a2]).distinct(), [p1, p2, p3, p4])
        self.assertItemsEqual(Article.objects.exclude(publications=p2), [a1])

        p1.delete()
        self.assertItemsEqual(Publication.objects.all(), [p2, p3, p4])
        a1 = Article.objects.get(pk=1)
        self.assertItemsEqual(a1.publications.all(), [])

        a2.delete()
        self.assertItemsEqual(Article.objects.all(), [a1])
        self.assertItemsEqual(p2.article_set.all(), [])

        a4 = Article(headline='NASA finds intelligent life on Earth')
        a4.save()
        p2.article_set.add(a4)
        p2.article_set.all()
        self.assertItemsEqual(p2.article_set.all(), [a4])
        self.assertItemsEqual(a4.publications.all(), [p2])

        new_article = p2.article_set.create(headline='Oxygen-free diet works wonders')
        self.assertItemsEqual(p2.article_set.all(), [a4, new_article])
        a5 = p2.article_set.all()[1]
        self.assertItemsEqual(a5.publications.all(), [p2])

        # Removing Publication from an Article:
        self.assertItemsEqual(p2.article_set.all(), [a4, a5])
        a4.publications.remove(p2)
        self.assertItemsEqual(p2.article_set.all(), [a5])
        self.assertItemsEqual(a4.publications.all(), [])

        # And from the other end:
        p2.article_set.remove(a5)
        self.assertItemsEqual(p2.article_set.all(), [])
        self.assertItemsEqual(a5.publications.all(), [])

        # Relation sets can be assigned. Assignment clears any existing set members:
        self.assertItemsEqual(a4.publications.all(), [])
        a4.publications = [p3]
        self.assertItemsEqual(a4.publications.all(), [p3])

        # Relation sets can be cleared:
        p2.article_set.clear()
        self.assertItemsEqual(p2.article_set.all(), [])

        # And you can clear from the other end:
        p2.article_set.add(a4, a5)
        self.assertItemsEqual(p2.article_set.all(), [a4, a5])
        self.assertItemsEqual(a4.publications.all(), [p2, p3])
        a4.publications.clear()
        self.assertItemsEqual(a4.publications.all(), [])
        self.assertItemsEqual(p2.article_set.all(), [a5])

        # Recreate the Article and Publication we have deleted:
        p1 = Publication(title='The Python Journal')
        p1.save()
        a2 = Article(headline='NASA uses Python')
        a2.save()
        a2.publications.add(p1, p2, p3)

        # Bulk delete some Publications - references to deleted publications should go:
        Publication.objects.filter(title__startswith='Science').delete()
        self.assertItemsEqual(Publication.objects.all(), [p4, p1])
        self.assertItemsEqual(Article.objects.all(), [a1, a2, a4, a5])
        self.assertItemsEqual(a2.publications.all(), [p1])

        # Bulk delete some articles - references to deleted objects should go:
        q = Article.objects.filter(headline__startswith='Django')
        self.assertItemsEqual(q, [a1])
        q.delete()

        # After the delete(), the QuerySet cache needs to be cleared, and the referenced objects should be gone:
        self.assertItemsEqual(q, [])
        self.assertItemsEqual(p1.article_set.all(), [a2])

        # An alternate to calling clear() is to assign the empty set:
        p1.article_set = []
        self.assertItemsEqual(p1.article_set.all(), [])

        a2.publications = [p1, p4]
        self.assertItemsEqual(a2.publications.all(), [p1, p4])
        a2.publications = []
        self.assertItemsEqual(a2.publications.all(), [])