import requests
from libpathod import test

class Test:
    """
        Testing the requests module with 
        a single pathod instance started 
        for the test suite.
    """
    @classmethod
    def setUpAll(cls):
        cls.d = test.Daemon()

    @classmethod
    def tearDownAll(cls):
        cls.d.shutdown()

    def setUp(self):
        # Clear the pathod logs between tests
        self.d.clear_log()

    def test_simple(self):
        # Get a URL for a pathod spec
        url = self.d.p("200:b@100")
        # ... and request it
        r = requests.put(url)

        # Check the returned data
        assert r.status_code == 200
        assert len(r.content) == 100

        # Check pathod's internal log
        log = self.d.last_log()["request"]
        assert log["method"] == "PUT"

    def test_two(self):
        assert not self.d.log()
