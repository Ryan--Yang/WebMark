import time
from benchmark import Benchmark

class Octane(Benchmark):
    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "Octane"

    @property
    def metric(self):
        return "score"

    @property
    def default_url(self):
        return "http://octane-benchmark.googlecode.com/svn/latest/index.html"

    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 90

    def start(self, driver):
        time.sleep(1)
        driver.find_element_by_id("run-octane").click()
        self.main_banner = driver.find_element_by_id("main-banner")

    def chk_finish(self, driver):
        return self.main_banner.text.find("Score:") != -1

    def get_result(self, driver):
        str = self.main_banner.text
        pos = str.find(":") + 1
        str = str[pos:].strip()
        return int(str)
