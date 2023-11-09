from unittest import TestCase

from teamcity_extra import messages

class Test(TestCase):
    def test_constructor(self):
        messages.TeamcityServiceMessages()
