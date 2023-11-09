class UserGroup:

    def __init__(self, mv_sdk, base_url: str, domain: str, **kwargs: dict):
        """
        Initialize the UserGroup Domain
        """
        super()
        self.mv_sdk = mv_sdk
        self.base_url = base_url
        self.domain = domain

    def get(self, params=None, data=None, headers=None, auth=None, object_id=None,
            object_action='None', domain_id=None, domain_action=None):
        """
        https://docs.mediavalet.com/#cd61e1a5-63a8-4238-9740-7961b89ef22b
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
