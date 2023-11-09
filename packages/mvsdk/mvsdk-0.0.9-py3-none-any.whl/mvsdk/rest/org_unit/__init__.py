class OrgUnit:

    def __init__(self, mv_sdk, base_url: str, domain: str, **kwargs: dict):
        """
        Initialize the OrgUnit Domain
        """
        super()
        self.mv_sdk = mv_sdk
        self.base_url = base_url
        self.domain = domain

    def get_current(self, params=None, data=None, headers=None, auth=None, object_id=None,
                    object_action='current', domain_id=None, domain_action=None):
        """
        https://docs.mediavalet.com/#7bbaf6aa-9e15-44ef-bc66-493fa680baf5
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
