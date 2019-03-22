from collections import OrderedDict
from .fixture import AppTestCase


class TestMatches(AppTestCase):

    ORDER = 4

    def test_matches_all(self):
        cases = [
            ("/matches/", 0, None, 2),
            ("/matches/1", 1, None, 2),
            ("/matches/ad", 0, "ad", 1),
            ("/matches/ad/1", 1, "ad", 1),
            ("/matches/tdm", 0, "tdm", 1),
            ("/matches/player/76561198260599288", 0, None, 1)
        ]
        for case in cases:
            uri = case[0]
            page = case[1]
            gametype = case[2]
            page_count = case[3]
            resp = self.test_cli.get(uri)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.template.name, "match_list.html")

            context = resp.context
            self.assertIn('request', context)
            self.assertIn('current_page', context)
            self.assertIn('gametype', context)
            self.assertIn('page_count', context)
            self.assertEqual(context['current_page'], page)
            self.assertEqual(context['gametype'], gametype)
            self.assertEqual(context['page_count'], page_count)

            sample_filename = "match_list_{}".format(cases.index(case)+1)
            self.assertEqual(
                context['matches'],
                self.read_json_sample(sample_filename)
            )

    def test_old_routes(self):
        assert 0
        resp = self.test_cli.get("/player/123/matches/blablabla/456/", allow_redirects=False)
        self.assertTrue(resp.headers['Location'].endswith("/matches/player/123/blablabla/456"))

        resp = self.test_cli.get("/player/123/matches/blablabla/456/", allow_redirects=False)
        self.assertTrue(resp.headers['Location'].endswith("/matches/player/123/blablabla/456"))