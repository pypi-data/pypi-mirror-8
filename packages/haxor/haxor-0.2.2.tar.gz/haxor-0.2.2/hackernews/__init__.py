#!/usr/bin/env python

"""
haxor
Unofficial Python wrapper for official Hacker News API

@author avinash sajjanshetty
@email a@sajjanshetty.com
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
import json
import sys

import requests

from .settings import supported_api_versions

__all__ = [
    'User',
    'Item',
    'HackerNews',
    'InvalidAPIVersion',
    'InvalidItemID',
    'InvalidUserID']


class InvalidItemID(Exception):
    pass


class InvalidUserID(Exception):
    pass


class InvalidAPIVersion(Exception):
    pass


class HTTPError(Exception):
    pass


class HackerNews(object):

    def __init__(self, version='v0'):
        """
        Args:
            version (string): specifies Hacker News API version. Default is `v0`.

        Raises:
          InvalidAPIVersion: If Hacker News version is not supported.

        """
        try:
            self.base_url = supported_api_versions[version]
        except KeyError:
            raise InvalidAPIVersion

    def _get(self, url):
        """Internal method used for GET requests

        Args:
            url (string): URL to send GET.

        Returns:
            requests' response object

        Raises:
          HTTPError: If HTTP request failed.

        """
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            return response
        else:
            raise HTTPError

    def _get_page(self, page):
        return self._get('{0}{1}.json'.format(self.base_url, page))

    def _get_page_param(self, page, param):
        return self._get('{0}{1}/{2}.json'.format(self.base_url, page, param))

    def get_item(self, item_id):
        """Returns Hacker News `Item` object.

        Args:
            item_id (int or string): Unique item id of Hacker News story, comment etc.

        Returns:
            `Item` object representing Hacker News item.

        Raises:
          InvalidItemID: If corresponding Hacker News story does not exist.

        """

        response = self._get_page_param('item', item_id).json()

        if not response:
            raise InvalidItemID

        return Item(response)

    def get_user(self, user_id):
        """Returns Hacker News `User` object.

        Args:
            user_id (string): unique user id of a Hacker News user.

        Returns:
            `User` object representing a user on Hacker News.

        Raises:
          InvalidUserID: If no such user exists on Hacker News.

        """
        response = self._get_page_param('user', user_id).json()

        if not response:
            raise InvalidUserID

        return User(response)

    def top_stories(self, limit=None):
        """Returns list of item ids of current top stories

        Args:
            limit (int): specifies the number of stories to be returned.

        Returns:
            `list` object containing ids of top stories.
        """
        return self._get_page('topstories').json()[:limit]

    def get_max_item(self):
        """Returns list of item ids of current top stories

        Args:
            limit (int): specifies the number of stories to be returned.

        Returns:
            `int` if successful.
        """
        return self._get_page('maxitem').json()


class Item(object):

    """
    Represents stories, comments, jobs, Ask HNs and polls
    """

    def __init__(self, data):
        self.item_id = data.get('id')
        self.deleted = data.get('deleted')
        self.item_type = data.get('type')
        self.by = data.get('by')
        self.submission_time = datetime.datetime.fromtimestamp(
            data.get(
                'time',
                0))
        self.text = data.get('text')
        self.dead = data.get('dead')
        self.parent = data.get('parent')
        self.kids = data.get('kids')
        self.url = data.get('url')
        self.score = data.get('score')
        self.title = data.get('title')
        self.parts = data.get('parts')
        self.raw = json.dumps(data)

    def __repr__(self):
        retval = '<hackernews.Item: {0} - {1}>'.format(self.item_id, self.title)
        if sys.version_info.major < 3:
            return retval.encode('utf-8', errors='backslashreplace')
        return retval


class User(object):

    """
    Represents a hacker i.e. a user on Hacker News
    """

    def __init__(self, data):
        self.user_id = data.get('id')
        self.delay = data.get('delay')
        self.created = datetime.datetime.fromtimestamp(data.get('created', 0))
        self.karma = data.get('karma')
        self.about = data.get('about')
        self.submitted = data.get('submitted')
        self.raw = json.dumps(data)

    def __repr__(self):
        retval = '<hackernews.User: {0}>'.format(self.user_id)
        if sys.version_info.major < 3:
            return retval.encode('utf-8', errors='backslashreplace')
        return retval
