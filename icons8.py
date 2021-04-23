import requests

GET_URL = 'https://api-icons.icons8.com/publicApi/icons/icon'
SEARCH_URL = 'https://search.icons8.com/api/iconsets/v5/search'

class Icons8Api:
    def __init__(self, token):
        self.token = token

    def search(self, keyword, platform):
        request_model = requests.models.PreparedRequest()
        params = {
            'term': keyword,
            'token': self.token,
            'platform': platform,
            'amount':  1
        }
        request_model.prepare_url(SEARCH_URL, params)
        return requests.get(request_model.url).json()['icons'][0]['id']

    def get(self, id):
        request_model = requests.models.PreparedRequest()
        params = {
            'id': id,
            'token': self.token
        }
        request_model.prepare_url(GET_URL, params)
        return requests.get(request_model.url).json()['icon']['svg']