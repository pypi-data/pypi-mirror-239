from mvsdk.api import PathBuilder, APIRequester


class Client(object):
    """
    A client for accessing the MVAPI.
    """
    def __init__(self, auth_url: str = None, base_url: str = None):

        self.auth_url = auth_url or 'login.mediavalet.com'
        self.base_url = base_url or 'mv-api-usva.mediavalet.net'

        # Domains
        self._asset = None
        self._attribute = None
        self._bulk = None
        self._category = None
        self._connect = None
        self._direct_link = None
        self._keyword = None
        self._keyword_group = None

    def request(self, method, base_url, domain, object_id=None,
                object_action=None, domain_id=None, domain_action=None,
                params=None, data=None, headers=None, auth=None, bulk=None, **kwargs):

        headers = headers or {}
        params = params or {}
        data = data or {}
        method = method.upper()
        bulk = bulk or False

        headers['User-Agent'] = 'MediaValetSDK/0.0.4'
        headers['Host'] = base_url or self.base_url
        if auth:
            headers['Authorization'] = f'Bearer {auth}'

        uri, url = PathBuilder(base_url=base_url, domain=domain, object_id=object_id,
                               object_action=object_action, domain_id=domain_id,
                               domain_action=domain_action, params=params).build()

        if bulk:
            return {
                'method': method,
                'uri': uri,
                'headers': headers,
                'data': data
            }

        api = APIRequester(url=url, headers=headers, data=data, **kwargs)

        if method == 'GET':
            response = api.get()
        elif method == 'POST':
            response = api.post()
        elif method == 'DELETE':
            response = api.delete()
        else:
            response = {'status_code': "405", 'json': "Verb not allowed"}

        return response

    @property
    def asset(self):
        """
        Access the MVAPI Asset API
        """
        if self._asset is None:
            from mvsdk.rest.asset import Asset
            self._asset = Asset(self, self.base_url, 'asset')
        return self._asset

    @property
    def attribute(self):
        """
        Access the MVAPI Attribute API
        """
        if self._attribute is None:
            from mvsdk.rest.attribute import Attribute
            self._attribute = Attribute(self, self.base_url, 'attribute')
        return self._attribute

    @property
    def bulk(self):
        """
        Access the MVAPI Bulk API
        """
        if self._bulk is None:
            from mvsdk.rest.bulk import Bulk
            self._bulk = Bulk(self, self.base_url, 'bulk')
        return self._bulk

    @property
    def category(self):
        """
        Access the MVAPI Category API
        """
        if self._category is None:
            from mvsdk.rest.category import Category
            self._category = Category(self, self.base_url, 'category')
        return self._category

    @property
    def connect(self):
        """
        Access the MVAPI Connect API
        """
        if self._connect is None:
            from mvsdk.rest.connect import Connect
            self._connect = Connect(self, self.auth_url, 'connect')
        return self._connect
    
    @property
    def direct_link(self):
        """
        Access the MVAPI DirectLink API
        """
        if self._direct_link is None:
            from mvsdk.rest.direct_link import DirectLink
            self._direct_link = DirectLink(self, self.base_url, 'direct_link')
        return self._direct_link

    @property
    def keyword(self):
        """
        Access the MVAPI Keyword API
        """
        if self._keyword is None:
            from mvsdk.rest.keyword import Keyword
            self._keyword = Keyword(self, self.base_url, 'keyword')
        return self._keyword

    @property
    def keyword_group(self):
        """
        Access the MVAPI KeywordGroup API
        """
        if self._keyword_group is None:
            from mvsdk.rest.keyword_group import KeywordGroup
            self._keyword_group = KeywordGroup(self, self.base_url, 'keyword_group')
        return self._keyword_group
