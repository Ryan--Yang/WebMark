import time
from selenium.webdriver.support import wait
from benchmark import Benchmark
from common.exceptions import WebMarkException

class GUIMark3(Benchmark):
    _SUITES = {
        "bitmap" : "%s/bitmap/GM3_JS_Bitmap.html",
        "bitmap cache" : "%s/bitmap/GM3_JS_Bitmap_cache.html",
        "vector" : "%s/vector/GM3_JS_Vector.html"
    }

    def __init__(self, suite = 'bitmap'):
        if self._SUITES.has_key(suite.lower()):
            self.suite = suite
        else:
            raise WebMarkException("Unsupported suite %s, "
            "should be one of 'bitmap', 'bitmap cache', 'vector'." % suite)
        Benchmark.__init__(self)

    @property
    def name(self):
        return "GUIMark3 %s" % self.suite

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return self._SUITES[self.suite.lower()] % "http://www.craftymind.com/factory/guimark3"

    def get_result(self, driver):
        elem = driver.find_element_by_id("testlabel")
        fps = 0.0        
        for i in range(1,16):
            time.sleep(20)
            str = elem.text
            start = str.find(":") + 1
            end = str.find("fps")
            str = str[start:end].strip()
            fps += (float(str) - fps) / i
        return round(fps, 2)
