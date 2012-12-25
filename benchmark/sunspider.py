import time
from selenium.webdriver.support import wait
from benchmark import Benchmark
from common.exceptions import WebMarkException

class SunSpider(Benchmark):
    _VERSIONS = {
        "0.9" : "http://www.webkit.org/perf/sunspider-0.9/sunspider-driver.html",
        "0.9.1" : "http://www.webkit.org/perf/sunspider-0.9.1/sunspider-0.9.1/driver.html"
    }

    def __init__(self, version = '0.9.1'):
        if self._VERSIONS.has_key(version):
            self.version = version
        else:
            raise WebMarkException("Unsupported version %s, "
            "should be one of '0.9.1', '0.9'." % version)
        Benchmark.__init__(self)

    @property
    def name(self):
        return "SunSpider(%s)" % (self.version)

    @property
    def metric(self):
        return "ms"

    @property
    def default_url(self):
        return self._VERSIONS[self.version]

    @property
    def default_timeout(self):
        return 600

    @property
    def expect_time(self):
        return 90

    def chk_finish(self, driver):
        return driver.current_url.lower().find("result") != -1

    def get_result(self, driver):
        elem = driver.find_element_by_id("console")
        str = elem.text
        pos = str.find("Total:")+len("Total:")
        str = str[pos:].strip()
        pos = str.find("ms")
        return float(str[:pos])
