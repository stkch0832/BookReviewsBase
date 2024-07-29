from config import settings
import requests

api_key = settings.API_KEY

api_url = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?'

def get_api_data(params):
    params['format'] = 'json'
    params['applicationId'] = api_key
    api_response = requests.get(api_url, params=params)

    if api_response.status_code != 200:
        return None

    result = api_response.json()

    api_data = result['Items']
    return api_data
