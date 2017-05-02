# -*- encoding: utf-8
"""
Code for interacting with the Tumblr API.
"""

import requests


API_ENDPOINT = 'https://api.tumblr.com/v2'


# TODO: It should be possible to test this with Betamax.


# TODO: It should be possible to test this with Betamax.
class TumblrSession(requests.Session):
    """
    A variant of ``requests.Session`` that auto-inserts a Tumblr API key
    on outgoing responses.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        super().__init__()

    def get(self, *args, **kwargs):
        params = kwargs.get('params', {})
        params['api_key'] = self.api_key
        kwargs['params'] = params
        return super().get(*args, **kwargs)

    def get_posts(self, hostname, offset=0):
        """
        Gets a list of posts for the given name and offset.
        """
        url = f'{API_ENDPOINT}/blog/{hostname}/posts'
        print(f'Making request to {url}')

        resp = self.get(url, params={'offset': offset})
        print(f'Received {resp} from Tumblr API')

        if resp.status_code != 200:
            raise RuntimeError(
                f'Error from Tumblr API: {resp.status_code} ({resp.text})'
            )

        return resp.json()['response']['posts']


__all__ = ['TumblrSession']
