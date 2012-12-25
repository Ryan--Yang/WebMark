import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class Kraken(Benchmark):
    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "Kraken"

    @property
    def metric(self):
        return "ms"

    @property
    def default_url(self):
        return "http://krakenbenchmark.mozilla.org/kraken-1.1/driver.html"

    @property
    def default_timeout(self):
        return 900

    @property
    def expect_time(self):
        return 120

    def chk_finish(self, driver):
        return driver.current_url.lower().find("results") != -1

    def get_result(self, driver):
        elem = driver.find_element_by_id("console")
        str = elem.text
        pos = str.find("Total:")+len("Total:")
        str = str[pos:].strip()
        pos = str.find("ms")
        return float(str[:pos])
