from nose.tools import assert_equals, assert_raises
from nose.plugins.skip import SkipTest
from mock import patch, MagicMock

import requests

from blackbelt.config import config

from blackbelt.circle import Client

"""
Integration exploratory playground for CircleCI.
Don't really treat it as a test, but it may still be useful for you.
"""


class TestBuildInfoRetrieval(object):

    def setUp(self):
        try:
            self.client = Client()
        except ValueError:
            raise SkipTest()

    def test_repo_owner(self):
        builds = self.client.get_builds('apiaryio', 'ivy')
        # print builds[0]
        assert len(builds) > 0

