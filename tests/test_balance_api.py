from .fixture import AppTestCase

STEAM_IDS_TDM_PLAYERS = "+".join(
    [
        "76561198273556024",  # trig
        "76561198256352933",  # om3n
        "76561198256203867",  # prestij
        "76561198257561075",  # antonio_by
    ]
)

STEAM_IDS_AD_PLAYERS = "+".join(
    [
        "76561198043212328",  # shire
        "76561198257384619",  # HanzoHasashiSan
        "76561197985202252",  # carecry
        "76561198308265738",  # lookaround
        "76561198257327401",  # Jalepeno
        "76561198005116094",  # Xaero
        "76561198077231066",  # Mike_Litoris
        "76561198346199541",  # Zigurun
        "76561198257338624",  # indie
    ]
)


class TestBalanceApi(AppTestCase):

    maxDiff = None

    def assert_balance_api_data_equal(self, first: dict, second: dict):
        self.assertIn("playerinfo", first)
        self.assertIn("playerinfo", second)
        self.assertDictEqual(first["playerinfo"], second["playerinfo"])

        self.assertIn("players", first)
        self.assertIn("players", second)
        self.assert_lists_have_same_elements(first["players"], second["players"])

        self.assertIn("deactivated", first)
        self.assertIn("deactivated", second)
        self.assert_lists_have_same_elements(
            first["deactivated"], second["deactivated"]
        )

        self.assertIn("untracked", first)
        self.assertIn("untracked", second)
        self.assert_lists_have_same_elements(first["untracked"], second["untracked"])

    def test_bigger_numbers(self):
        response = self.get(
            "/elo/bn/" + STEAM_IDS_AD_PLAYERS,
            200
        )
        self.assert_balance_api_data_equal(
            response.json(), self.read_json_sample("balance_api_ad_bigger_numbers")
        )

    def test_simple_ad_only_players(self):
        self.assert_balance_api_data_equal(
            self.get("/elo/" + STEAM_IDS_AD_PLAYERS).json(),
            self.read_json_sample("balance_api_ad_only_players"),
        )

    def test_simple_tdm_only_players(self):
        self.assert_balance_api_data_equal(
            self.get("/elo/" + STEAM_IDS_TDM_PLAYERS).json(),
            self.read_json_sample("balance_api_tdm_only_players"),
        )

    def test_map_based_tdm(self):
        response = self.get(
            "/elo/map_based/" + STEAM_IDS_TDM_PLAYERS + "+76561198125710191",
            200,
            headers={"X-QuakeLive-Map": "hiddenfortress"},
        )

        self.assert_balance_api_data_equal(
            response.json(), self.read_json_sample("balance_api_tdm_hiddenfortress")
        )

    def test_map_based_ad(self):
        response = self.get(
            "/elo/map_based/"
            + STEAM_IDS_AD_PLAYERS
            + "+76561198257183089",  # played dividedcrossings at least 2 times
            200,
            headers={"X-QuakeLive-Map": "dividedcrossings"},
        )

        self.assert_balance_api_data_equal(
            response.json(), self.read_json_sample("balance_api_ad_dividedcrossings")
        )

    def test_map_based_map_not_exists(self):
        def set_games_zero(data: dict):
            for key, value in data.items():
                if isinstance(value, list):
                    data[key] = [set_games_zero(x) for x in value]
                elif isinstance(value, dict):
                    data[key] = set_games_zero(value)
                elif key == "games":
                    data[key] = 0

            return data

        response = self.get(
            "/elo/map_based/" + STEAM_IDS_AD_PLAYERS,
            200,
            headers={"X-QuakeLive-Map": "this_map_does_not_exist"},
        )

        ratings_data = response.json()

        self.assert_balance_api_data_equal(
            ratings_data,
            set_games_zero(self.read_json_sample("balance_api_ad_only_players")),
        )
