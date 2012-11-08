import time
from selenium.webdriver.support import wait
from common.exceptions import WebMarkException
from benchmark import Benchmark

class V8BenchmarkSuite(Benchmark):
    GET_STATUS_JS = 'return document.getElementById("status").innerHTML'
    _VERSIONS = ('v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7')

    def __init__(self, driver, logf, version='v7'):
        if version in self._VERSIONS:
            self.version = version
        else:
            raise WebMarkException("Unsupported version %s, "
            "should be one of ('v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7')" % version)
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "V8 Benchmark Suite(version:%s)" % self.version

    @property
    def metric(self):
        return "score"
        
    @property
    def _url(self):
        return "http://v8.googlecode.com/svn/data/benchmarks/%s/run.html" % self.version
        
    def run(self):
        self.open(self._url)
        time.sleep(30)
        #elem = self.driver.find_element_by_id("status")
        #wait.WebDriverWait(self.driver, 1200, 30).until(lambda x: elem.text.find("Score:") != -1)
        wait.WebDriverWait(self.driver, 900, 30).until(
            lambda x: x.execute_script(self.GET_STATUS_JS).find("Score:") != -1)
        #str = elem.text
        str = self.driver.execute_script(self.GET_STATUS_JS)
        pos = len("Score:")
        str = str[pos:].strip()
        return int(str)