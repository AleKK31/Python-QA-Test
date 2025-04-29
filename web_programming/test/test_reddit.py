import unittest
from unittest.mock import patch
from web_programming.reddit import get_subreddit_data
import requests

# Rodar: python3 -m unittest web_programming.test.test_reddit
# Para aumentar a cobertura e achar problemas ou erros
#  - a função get_subreddit_data não tem tratamento para lidar com dados incompletos

class TestGetSubredditData(unittest.TestCase):
    @patch("web_programming.reddit.requests.get")
    def test_valid_response(self, mock_get):
        # Simula uma resposta válida da API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": {
                "children": [
                    {"data": {"title": "Test Title", "url": "http://test.url", "selftext": "Test Text"}}
                ]
            }
        }

        result = get_subreddit_data("learnpython", limit=1, wanted_data=["title", "url", "selftext"])
        expected = {0: {"title": "Test Title", "url": "http://test.url", "selftext": "Test Text"}}
        self.assertEqual(result, expected)

    @patch("web_programming.reddit.requests.get")
    def test_invalid_search_term(self, mock_get):
        # Testa termos inválidos
        with self.assertRaises(ValueError) as context:
            get_subreddit_data("learnpython", wanted_data=["invalid_term"])
        self.assertIn("Invalid search term", str(context.exception))

    @patch("web_programming.reddit.requests.get")
    def test_rate_limit_error(self, mock_get):
        # Simula um erro 429 (rate limit)
        mock_get.return_value.status_code = 429
        with self.assertRaises(requests.HTTPError):
            get_subreddit_data("learnpython")

    @patch("web_programming.reddit.requests.get")
    def test_no_wanted_data(self, mock_get):
        # Testa quando `wanted_data` não é fornecido
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": {
                "children": [
                    {"data": {"title": "Test Title", "url": "http://test.url", "selftext": "Test Text"}}
                ]
            }
        }

        result = get_subreddit_data("learnpython", limit=1)
        self.assertIn(0, result)  # Verifica se o ID 0 está presente no resultado

    @patch("web_programming.reddit.requests.get")
    def test_zero_limit(self, mock_get):
        # Testa quando o limite é 0 (deve retornar um dicionário vazio)
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": {"children": []}}
        result = get_subreddit_data("learnpython", limit=0)
        self.assertEqual(result, {})

    @patch("web_programming.reddit.requests.get")
    def test_high_limit(self, mock_get):
        # Simula uma resposta com muitos posts
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": {"children": [{"data": {"title": f"Title {i}"}} for i in range(100)]}
        }
        result = get_subreddit_data("learnpython", limit=100, wanted_data=["title"])
        self.assertEqual(len(result), 100)

    @patch("web_programming.reddit.requests.get")
    def test_connection_error(self, mock_get):
        # Simula um erro de conexão
        mock_get.side_effect = requests.ConnectionError
        with self.assertRaises(requests.ConnectionError):
            get_subreddit_data("learnpython")

    @patch("web_programming.reddit.requests.get")
    def test_timeout_error(self, mock_get):
        # Simula um erro de timeout
        mock_get.side_effect = requests.Timeout
        with self.assertRaises(requests.Timeout):
            get_subreddit_data("learnpython")

    @patch("web_programming.reddit.requests.get")
    def test_incomplete_data(self, mock_get):
        # Simula uma resposta com dados incompletos
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": {"children": [{"data": {"title": "Test Title"}}]}  # Sem "url" ou "selftext"
        }
        result = get_subreddit_data("learnpython", limit=1, wanted_data=["title", "url"])
        self.assertEqual(result, {0: {"title": "Test Title"}})  # "url" deve estar ausente

    @patch("web_programming.reddit.requests.get")
    def test_mixed_valid_and_invalid_terms(self, mock_get):
        # Testa termos válidos e inválidos misturados
        with self.assertRaises(ValueError) as context:
            get_subreddit_data("learnpython", wanted_data=["title", "invalid_term"])
        self.assertIn("Invalid search term", str(context.exception))

    @patch("web_programming.reddit.requests.get")
    def test_different_age_values(self, mock_get):
        # Simula uma resposta válida da API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": {"children": [{"data": {"title": "Test Title"}}]}
        }
        for age in ["new", "top", "hot"]:
            result = get_subreddit_data("learnpython", age=age, wanted_data=["title"])
            self.assertEqual(result, {0: {"title": "Test Title"}})


if __name__ == "__main__":
    unittest.main()