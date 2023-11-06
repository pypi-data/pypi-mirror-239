class Asset:

    def __init__(self, mv_sdk, base_url: str, domain: str):
        """
        Initialize the Asset Domain
        """
        super(Asset, self)
        self.mv_sdk = mv_sdk
        self.base_url = base_url
        self.domain = domain

    def get(self, params=None, data=None, headers=None, auth=None, object_id=None,
            domain_id=None, domain_action=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        return self.mv_sdk.request(
            'get',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            domain_id=domain_id,
            domain_action=domain_action
        )

    def put(self, params=None, data=None, headers=None, auth=None, profile_id=None,
            domain_id=None, domain_action=None):
        """

        """

    def get_related(self, params=None, data=None, headers=None, auth=None, object_id=None,
                    object_action='relatedassets', domain_id=None, domain_action=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        return self.mv_sdk.request(
            'get',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action
        )

    # --------------
    # ASSET ATTRIBUTES
    # --------------

    def create_attribute(self, params=None, data=None, headers=None, auth=None,
                         object_id=None, object_action='keywords', domain_id=None,
                         domain_action=None, bulk=None, sync=True):
        """

        """
        headers = headers or {}
        params = params or {}

        headers['Accept'] = "application/json"
        headers['Content-Type'] = "application/json"
        headers['Accept-Encoding'] = "gzip, deflate, br"
        headers['Connection'] = "keep-alive"

        if not sync:
            params['priority'] = 'low'
            params['runAsync'] = True

        return self.mv_sdk.request(
            'post',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action,
            bulk=bulk
        )

    def delete_attribute(self, params=None, data=None, headers=None, auth=None,
                       object_id=None, object_action='keyword', domain_id=None,
                       domain_action=None, bulk=None, sync=True):
        """

        """
        headers = headers or {}
        params = params or {}

        headers['Content-Type'] = 'application/json'

        if not sync:
            params['priority'] = 'low'
            params['runAsync'] = True

        return self.mv_sdk.request(
            'delete',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action,
            bulk=bulk
        )

    def get_attributes(self, params=None, data=None, headers=None, auth=None,
                     object_id=None, object_action='attributes', domain_id=None,
                     domain_action=None, bulk=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        return self.mv_sdk.request(
            'get',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action,
            bulk=bulk
        )

    # --------------
    # ASSET CATEGORIES
    # --------------

    def get_categories(self, params=None, data=None, headers=None, auth=None,
                       object_id=None, object_action='keywords', domain_id=None,
                       domain_action=None, bulk=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        return self.mv_sdk.request(
            'get',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action,
            bulk=bulk
        )

    # --------------
    # ASSET COMMENTS
    # --------------

    def get_comments(self, params=None, data=None, headers=None, auth=None,
                       object_id=None, object_action='comments', domain_id=None,
                       domain_action=None, bulk=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        return self.mv_sdk.request(
            'get',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action,
            bulk=bulk
        )

    # --------------
    # ASSET HISTORY
    # --------------

    def get_history(self, params=None, data=None, headers=None, auth=None,
                    object_id=None, object_action='history', domain_id=None,
                    domain_action=None, bulk=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        return self.mv_sdk.request(
            'get',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action,
            bulk=bulk
        )

    # --------------
    # ASSET KEYWORDS
    # --------------

    def create_keywords(self, params=None, data=None, headers=None, auth=None,
                        object_id=None, object_action='keywords', domain_id=None,
                        domain_action=None, bulk=None, sync=True):
        """

        """
        headers = headers or {}
        params = params or {}

        headers['Accept'] = "application/json"
        headers['Content-Type'] = "application/json"
        headers['Accept-Encoding'] = "gzip, deflate, br"
        headers['Connection'] = "keep-alive"

        if not sync:
            params['priority'] = 'low'
            params['runAsync'] = True

        return self.mv_sdk.request(
            'post',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action,
            bulk=bulk
        )

    def delete_keyword(self, params=None, data=None, headers=None, auth=None,
                       object_id=None, object_action='keyword', domain_id=None,
                       domain_action=None, bulk=None, sync=True):
        """

        """
        headers = headers or {}
        params = params or {}

        headers['Content-Type'] = 'application/json'

        if not sync:
            params['priority'] = 'low'
            params['runAsync'] = True

        return self.mv_sdk.request(
            'delete',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action,
            bulk=bulk
        )

    def get_keywords(self, params=None, data=None, headers=None, auth=None,
                     object_id=None, object_action='keywords', domain_id=None,
                     domain_action=None, bulk=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        return self.mv_sdk.request(
            'get',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action,
            bulk=bulk
        )

    # --------------
    # ASSET RENDITIONS
    # --------------

    def get_renditions(self, params=None, data=None, headers=None, auth=None,
                       object_id=None, object_action='renditions', domain_id=None,
                       domain_action=None, bulk=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        return self.mv_sdk.request(
            'get',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action,
            bulk=bulk
        )

    # --------------
    # ASSET VIDEO INTELLIGENCE
    # --------------

    def get_video_intelligence_status(self, params=None, data=None, headers=None, auth=None,
                       object_id=None, object_action='videoIntelligence/status', domain_id=None,
                       domain_action=None, bulk=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        return self.mv_sdk.request(
            'get',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action,
            bulk=bulk
        )
