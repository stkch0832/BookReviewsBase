import os
import unittest
from unittest.mock import patch
from app.views.api_views import api_url, get_api_data

class GetApiDataViewTests(unittest.TestCase):
    @patch('app.views.api_views.requests.get')
    def test_34_get_api_data_success(self, mock_get):
        """
        APIにアクセスし、レスポンスが正常値であった場合
        """
        mock_response = unittest.mock.Mock()
        expected_data = {'Items': [{'title': 'test_title'}]}
        mock_response.json.return_value = expected_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        params = {'title': 'test'}
        result = get_api_data(params)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'test_title')

        expected_params = {
            'title': 'test',
            'format': 'json',
            'applicationId': os.getenv('API_KEY')
        }
        mock_get.assert_called_once_with(api_url, params=expected_params)

    @patch('app.views.api_views.requests.get')
    def test_35_get_api_data_faire(self, mock_get):
        """
        APIにアクセスし、レスポンスが異常値であった場合
        """
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        params = {'title': 'test'}
        result = get_api_data(params)

        self.assertIsNone(result)

        expected_params = {
            'title': 'test',
            'format': 'json',
            'applicationId': os.getenv('API_KEY')
        }
        mock_get.assert_called_once_with(api_url, params=expected_params)

    @patch('app.views.api_views.requests.get')
    def test_36_get_api_data_empty_params(self, mock_get):
        """
        APIにアクセスし、入力パラメータがblankであった場合
        """
        mock_response = unittest.mock.Mock()
        expected_data = {'Items': []}
        mock_response.json.return_value = expected_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        params = {}
        result = get_api_data(params)

        self.assertEqual(result, expected_data['Items'])

        expected_params = {
            'format': 'json',
            'applicationId': os.getenv('API_KEY')
        }
        mock_get.assert_called_once_with(api_url, params=expected_params)

if __name__ == '__main__':
    unittest.main()
