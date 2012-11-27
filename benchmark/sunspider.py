import time
from selenium.webdriver.support import wait
from benchmark import Benchmark
from common.exceptions import WebMarkException

class SunSpider(Benchmark):
    _VERSIONS = {
        "0.9" : "http://www.webkit.org/perf/sunspider-0.9/sunspider-driver.html",
        "0.9.1" : "http://www.webkit.org/perf/sunspider-0.9.1/sunspider-0.9.1/driver.html",
        "inside" : "http://pnp.sh.intel.com/benchmarks/WRTBench_Packages/WRTBench-latest/jsRendering-sunspider/driver.html",
        "isolated" : "http://192.168.1.36/workloads/sunspider/driver.html"
    }

    def __init__(self, driver, logf, appmode=False, offline=False, version = '0.9.1'):
        if self._VERSIONS.has_key(version):
            self.version = version
        else:
            raise WebMarkException("Unsupported version %s, "
            "should be one of '0.9.1', '0.9', 'inside', 'isolated'." % version)
        Benchmark.__init__(self, driver, logf, appmode, offline)

    @property
    def name(self):
        return "SunSpider(%s%s)" % (self.name_common_ext(True), self.version)

    @property
    def metric(self):
        return "ms"

    @property
    def _url(self):
        if self.offline:
            return self.webbench_path + 'SunSpider/sunspider-0.9.1/driver.html'
        return self._VERSIONS[self.version]
        
    def run(self):
        self.open(self._url)
        time.sleep(60)
        wait.WebDriverWait(self.driver, 60, 30).until(lambda x: x.current_url.lower().find("result") != -1)
        elem = self.driver.find_element_by_id("console")
        str = elem.text
        pos = str.find("Total:")+len("Total:")
        str = str[pos:].strip()
        pos = str.find("ms")
        return float(str[:pos])