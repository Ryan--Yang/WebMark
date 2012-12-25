import time
from selenium.webdriver.support import wait
from common.exceptions import WebMarkException
from benchmark import Benchmark

class V8BenchmarkSuite(Benchmark):
    GET_STATUS_JS = 'return document.getElementById("status").innerHTML'
    _VERSIONS = ('v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7')

    def __init__(self, version='v7'):
        if version in self._VERSIONS:
            self.version = version
        else:
            raise WebMarkException("Unsupported version %s, "
            "should be one of ('v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7')" % version)
        Benchmark.__init__(self)

    @property
    def name(self):
        return "V8 Benchmark Suite(%s)" % self.version

    @property
    def metric(self):
        return "score"
        
    @property
    def default_url(self):
        return "http://v8.googlecode.com/svn/data/benchmarks/%s/run.html" % self.version

    @property
    def default_timeout(self):
        return 900

    @property
    def expect_time(self):
        return 70

    def chk_finish(self, driver):
        return driver.execute_script(self.GET_STATUS_JS).find("Score:") != -1

    def get_result(self, driver):
        str = driver.execute_script(self.GET_STATUS_JS)
        pos = len("Score:")
        str = str[pos:].strip()
        return int(str)
