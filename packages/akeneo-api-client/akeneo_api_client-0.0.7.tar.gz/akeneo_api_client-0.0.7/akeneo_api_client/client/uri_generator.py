import urllib.parse
from urllib.parse import urlencode


class UriGenerator:

    def __init__(self, base_uri):
        self.base_uri = base_uri.rstrip('/')

    def generate(self, path, uri_params=[], query_params={}):
        uri_params = tuple(map(lambda x: urllib.parse.quote(str(x)), uri_params))
        uri = self.base_uri + "/" + (path.lstrip('/') % uri_params)

        if len(query_params) > 0:
            url_parts = list(urllib.parse.urlparse(uri))
            url_parts[4] = urlencode(query_params)
            uri = urllib.parse.urlunparse(url_parts)

        return uri