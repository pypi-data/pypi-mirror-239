class User:

    def __init__(self, mv_sdk, base_url: str, domain: str, **kwargs: dict):
        """
        Initialize the User Domain
        """
        super()
        self.mv_sdk = mv_sdk
        self.base_url = base_url
        self.domain = domain

    def get_all(self, params=None, data=None, headers=None, auth=None, object_id=None,
                object_action='None', domain_id=None, domain_action=None):
        """
        https://docs.mediavalet.com/#1394a30d-dfba-4386-9a71-e6e0547ed5d2
        """
        headers = headers or {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

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

    def get_approvers(self, params=None, data=None, headers=None, auth=None, object_id=None,
                      object_action='approvers', domain_id=None, domain_action=None):
        """
        https://docs.mediavalet.com/#1394a30d-dfba-4386-9a71-e6e0547ed5d2
        """
        headers = headers or {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

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

    def get_current(self, params=None, data=None, headers=None, auth=None, object_id=None,
                    object_action='current', domain_id=None, domain_action=None):
        """
        https://docs.mediavalet.com/#52981a4a-aef1-46dc-bdd4-3b26315cc38e
        """
        headers = headers or {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

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

    def get_current_permissions(self, params=None, data=None, headers=None, auth=None, object_id=None,
                                object_action='current/permissions', domain_id=None, domain_action=None):
        """
        https://docs.mediavalet.com/#6d29bbec-0ace-411e-8d96-0a35305a8960
        """
        headers = headers or {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

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
