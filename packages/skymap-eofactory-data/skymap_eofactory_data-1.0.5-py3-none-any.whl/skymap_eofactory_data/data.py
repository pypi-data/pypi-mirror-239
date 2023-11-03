import os
import requests
from dotenv import load_dotenv

load_dotenv()

EOF_URL = 'https://apitestphp.eofactory.ai/api'
token_fake = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQ3MCwibmFtZSI6IlR14bqlbiBOZ3V54buFbiBWxINuIiwiZW1haWwiOiJudnQxMjA3MjAxQGdtYWlsLmNvbSIsImNvdW50cnkiOm51bGwsInBpY3R1cmUiOm51bGwsImlhdCI6MTY5ODk5NDg3NiwiZXhwIjoxNzAxNTg2ODc2fQ.oooUwpfzpVTEegFor_Cyul-gcmxmDcuIX0BGcFCfRVGBIXG-EkYRC7uY8MUlT6izj0r043fjNzWcte9dwEPXdw'
workspace_id_fake = 'e7f0c230-118a-4d16-8672-f3da211ff4e6'

class Data:
    def __init__(
        self, 
        url='',  
        headers=None, 
        parameters=None, 
        **kwargs
    ):
        self.url = url if ('http' in url) else EOF_URL
        # self.url = url if ('http' in url) else os.getenv("EOF_URL")
        self.headers = headers
        self.parameters = parameters
        self.kwargs = kwargs

    @classmethod
    def open(
        cls,
        url='',
        headers={'Authorization': f'Bearer {token_fake}', "Content-Type":"application/json"},
        parameters={'workspace_id': workspace_id_fake, 'region': 'test'},
        # headers={'Authorization': f'Bearer {os.getenv("EOF_TOKEN")}', "Content-Type":"application/json"},
        # parameters={'workspace_id': {os.getenv("WORKSPACE_ID")}, 'region': {os.getenv("REGION")}},
    ) -> "Data":
        client: Data = cls(
            url=url, 
            headers=headers, 
            parameters=parameters
        )

        return client
    
    def _get(self, url, params={}, config={}, type='json'):
        try:
            print('self', self.headers, self.parameters, self.url)
            api_url = url if ('http' in url) else f'{self.url}{url}'
            response = requests.get(api_url, headers=self.headers, params=params)

            return response.json() if type == 'json' else response
        except Exception as e:
            print('request get error:', e)
    
    def _post(self, url, params={}, datas={}, config={}, type='json', files={}):
        try:
            api_url = url if ('http' in url) else f'{self.url}{url}' 
            if bool(files):
                headers = {
                    'Authorization': self.headers['Authorization']
                }
                response = requests.post(api_url, headers=headers, params=params, data=datas, files=files)
            else:
                headers = self.headers
                response = requests.post(api_url, headers=headers, params=params, json=datas, files=files)

            return response.json() if type == 'json' else response
        except Exception as e:
            print('request post error:', e)

    def workspaces(self, region=None):
        params = {
            'region': region if region is not None else self.parameters['region']
        }
        result = self._get('/workspaces', params)
        return result['data']
    