# -*- encoding: utf-8
"""
Code for interacting with the Tumblr API.
"""

import collections

import requests


API_ENDPOINT = 'https://api.tumblr.com/v2'


Post = collections.namedtuple('Post', ['url', 'type', 'date'])


class TumblrResponse:
    """
    A wrapper around ``requests.Response`` that exposes a few convenience
    methods.
    """

    def __init__(self, resp):
        assert self.resp.status_code == 200
        self.resp = resp

    def untagged_posts(self):
        return [
            Post(url=p['post_url'], type=p['type'], date=p['date'])
            for p in self.resp.json()['response']['posts']
            if not p['tags']
        ]

    @property
    def status_code(self):
        return self.resp.status_code

    def post_count(self):
        """How many posts have been checked in this respons?"""
        return len(self.resp.json()['response']['posts'])

    def total_posts(self):
        """How many posts are there in total?"""
        return self.resp.json()['response']['total_posts']


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

        return TumblrResponse(resp)


__all__ = ['TumblrSession']
