from collections import OrderedDict
from .fixture import AppTestCase


class TestRatings(AppTestCase):

    ORDER = 5

    def test_ratings_ad(self):
        resp = self.test_cli.get("/ratings/ad")
        context = resp.context

        self.assertEqual(resp.status_code, 200)

        self.assertIn('request', context)
        self.assertIn('current_page', context)
        self.assertIn('response', context)
        self.assertIn('gametype', context)

        self.assertEqual(context['gametype'], 'ad')
        self.assertEqual(context['current_page'], 0)

        self.assertEqual(
            context['response'],
            self.read_json_sample("ratings_ad")
        )

    def test_ratings_ad_json(self):
        resp = self.test_cli.get("/ratings/ad/0.json")
        self.assertEqual(
            resp.json()['response'],
            self.read_json_sample("ratings_ad")
        )
