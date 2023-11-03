
from skymap_eofactory_data.data import Data
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from dotenv import load_dotenv

load_dotenv()

class Vector(Data):
    # region: access eof data from hub
    def _get_data(self, endpoint, workspace_id=None, region=None, params=None):
        params = params or {}
        params['region'] = region if region is not None else self.parameters['region']
        workspace_id = self.parameters['workspace_id'] if workspace_id is None else workspace_id
        result = self._get(f'/workspaces/{workspace_id}{endpoint}', params)
        return result['data']

    def all(self, workspace_id=None, region=None, page=-1, order_by='created_at', order='desc', search=''):
        params = {
            'page': page,
            'order_by': order_by,
            'order': order,
            'search': search
        }
        endpoint = '/vector_folders' if page == -1 else '/vector_folders/v2'
        return self._get_data(endpoint, workspace_id, region, params)

    def info(self, id, workspace_id=None, region=None):
        return self._get_data(f'/vectors/{id}', workspace_id, region)

    #TODO: file_name is exist?
    # type: geojson, kml, shp (zip), kmz, gml    (kmz: error 500 internal server)
    def download(self, id, type='geojson', file_name='', file_path=None, workspace_id=None, region=None):
        info_image = self.info(id, workspace_id=None, region=None)
        url = info_image['path']

        # change to type vector download
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        # Update the value of the "file_type" parameter
        query_params['file_type'] = [type]
        # Reconstruct the modified URL
        modified_query = urlencode(query_params, doseq=True)
        modified_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, modified_query, parsed_url.fragment))

        response = self._get(modified_url, type=None)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful

        file_name = id + f'.{type}'
        if file_path is None:
            default_directory = 'vectors_downloaded'
            os.makedirs(default_directory, exist_ok=True)
            file_path = os.path.join(default_directory, file_name)
        else:
            os.makedirs(file_path, exist_ok=True) 
            file_path = os.path.join(file_path, file_name) #path: path/to/directory

        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        return 'vector downloaded to ' + file_path

    def folders(self):
        pass

    def vectors(self):
        pass

    #TODO: get geometry?
    def view(self, id):
        pass

    # endregion

    # region: store data from hub to eof
    def store(self, file_path, file_name=None, workspace_id=None, region=None):
        workspace_id = self.parameters['workspace_id'] if workspace_id is None else workspace_id
        url = f'/workspaces/{workspace_id}/vectors/upload'
        params = {
            'region': region if region is not None else self.parameters['region']
        }
        payload = {
            'name': file_name if file_name is not None else file_path.split('/')[-1].split('.')[0]
        }
        files = {"files[0]": open(file_path, "rb")}
        result_upload_vector = self._post(url, params=params, datas=payload, files=files)

        return result_upload_vector
    # endregion